from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from pathlib import Path

import fitz

SRC_1903 = {
    "url": "https://archive.org/download/bookofsermarcopo001polo/bookofsermarcopo001polo.pdf",
    "sha256": "6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7",
}
SRC_1920 = {
    "url": "https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf",
    "sha256": "dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941",
}

PAGES_1903 = {
    408: 113,
    425: 128,
    461: 164,
    462: 165,
    500: 201,
    501: 202,
}
PAGE_1920 = {"pdf_index": 63, "printed_page": 50}

STATE_ARMS = ("S_CORPUS", "S_TARGET_BOUND")
EVENT_ARMS = ("E_NATIVE_FULL", "E_CONTEXT_NEW", "E_PAIR_ONLY")
ACCESS_ARMS = ("A_NONE", "A_ERRATUM_REOPEN")

EXPECTED_FIELDS = {
    "actor": "Chinese Governor of Urumtsi",
    "time": "some years ago",
    "relative_location": "north-west of the Lob-nor",
    "river_location": "banks of the Tarim",
    "distance_relation": "within five days of Charkalyk",
    "object": "a town bearing the same name",
    "site_distinction": "not on the same site as the Lop of Marco Polo",
}
PARENT_ACTION = "found"
CORRECTED_ACTION = "founded"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-F/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(x) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def norm(s: str) -> str:
    return " ".join(s.replace("\u00ad", "").split())


def extract_page(pdf_raw: bytes, index: int) -> str:
    doc = fitz.open(stream=pdf_raw, filetype="pdf")
    if not (0 <= index < len(doc)):
        raise RuntimeError(f"page index out of range: {index}")
    return doc[index].get_text()


def token_occurrences(page_texts):
    pat = re.compile(r"(?<![A-Za-z])found(?![A-Za-z])", re.I)
    out = []
    for pdf_index, rec in sorted(page_texts.items()):
        txt = rec["text"]
        for ordinal, m in enumerate(pat.finditer(txt), 1):
            lo = max(0, m.start() - 150)
            hi = min(len(txt), m.end() + 180)
            out.append(
                {
                    "occurrence_id": f"1903:{rec['printed_page']}:{ordinal}",
                    "pdf_index": pdf_index,
                    "printed_page": rec["printed_page"],
                    "start": m.start(),
                    "end": m.end(),
                    "token": m.group(0),
                    "context": norm(txt[lo:hi]),
                }
            )
    return out


def identify_reference_occurrences(occ):
    u = [
        x
        for x in occ
        if x["printed_page"] == 201 and "Governor of Urumtsi" in x["context"]
    ]
    s = [
        x
        for x in occ
        if x["printed_page"] == 113 and "I found that there was a route" in x["context"]
    ]
    if len(u) != 1:
        raise RuntimeError(f"Urumtsi reference occurrence count={len(u)}")
    if len(s) != 1:
        raise RuntimeError(f"Sykes collateral occurrence count={len(s)}")
    return u[0], s[0]


def verify_parent_fields(page201_norm: str):
    for key, value in EXPECTED_FIELDS.items():
        if value not in page201_norm:
            raise RuntimeError(f"parent field missing from p201 source: {key}={value!r}")
    if "Governor of Urumtsi found" not in page201_norm:
        raise RuntimeError("parent action phrase missing")
    return {**EXPECTED_FIELDS, "action": PARENT_ACTION}


def verify_erratum(page50_norm: str):
    pat = re.compile(
        r"P\.\s*201,\s*Line\s*12\.\s*Read\s+the\s+Governor\s+of\s+Urumtsi\s+founded\s+instead\s+of\s*found\.",
        re.I,
    )
    if not pat.search(page50_norm):
        raise RuntimeError("natural Urumtsi erratum not verified in 1920 page")
    return {
        "target_page": 201,
        "printed_line": 12,
        "context": "Governor of Urumtsi",
        "old": PARENT_ACTION,
        "new": CORRECTED_ACTION,
    }


def state_payload(arm, page_texts, target_occ, parent_record):
    corpus = [
        {
            "pdf_index": i,
            "printed_page": rec["printed_page"],
            "text": rec["text"],
        }
        for i, rec in sorted(page_texts.items())
    ]
    if arm == "S_CORPUS":
        return {"corpus": corpus}
    if arm == "S_TARGET_BOUND":
        return {
            "corpus": corpus,
            "target_binding": {
                "field": "Urumtsi.action",
                "occurrence_id": target_occ["occurrence_id"],
                "printed_page": target_occ["printed_page"],
                "old_token": target_occ["token"].lower(),
            },
            "parent_record": parent_record,
        }
    raise ValueError(arm)


def event_payload(arm, native_event):
    envelope = {
        "correction_witness": "1920 addenda/errata",
        "printed_page": 50,
        "pdf_index": 63,
        "source_sha256": SRC_1920["sha256"],
    }
    if arm == "E_NATIVE_FULL":
        payload = dict(native_event)
    elif arm == "E_CONTEXT_NEW":
        payload = {
            "target_page": native_event["target_page"],
            "context": native_event["context"],
            "new": native_event["new"],
        }
    elif arm == "E_PAIR_ONLY":
        payload = {"old": native_event["old"], "new": native_event["new"]}
    else:
        raise ValueError(arm)
    return {"envelope": envelope, "payload": payload}


def effective_event(arm, access_arm, native_event):
    if access_arm == "A_ERRATUM_REOPEN":
        return dict(native_event), "NATIVE_REOPEN"
    ep = event_payload(arm, native_event)["payload"]
    return dict(ep), "DELIVERED_CHANNEL"


def select_candidates(state_arm, event_arm, access_arm, event, occurrences, target_occ):
    # Reopening the native erratum supplies full target binding.
    if access_arm == "A_ERRATUM_REOPEN":
        return [
            x
            for x in occurrences
            if x["printed_page"] == event["target_page"]
            and event["context"] in x["context"]
            and x["token"].lower() == event["old"]
        ]

    if event_arm == "E_NATIVE_FULL":
        return [
            x
            for x in occurrences
            if x["printed_page"] == event["target_page"]
            and event["context"] in x["context"]
            and x["token"].lower() == event["old"]
        ]

    if event_arm == "E_CONTEXT_NEW":
        return [
            x
            for x in occurrences
            if x["printed_page"] == event["target_page"]
            and event["context"] in x["context"]
        ]

    if event_arm == "E_PAIR_ONLY":
        if state_arm == "S_TARGET_BOUND":
            return [target_occ]
        return [x for x in occurrences if x["token"].lower() == event["old"]]

    raise ValueError(event_arm)


def candidate_overlay(candidate, event, event_arm, access_arm):
    new = event.get("new")
    if not new:
        return None
    if "old" in event:
        old = event["old"]
        if candidate["token"].lower() != old.lower():
            return None
    else:
        old = candidate["token"].lower()

    return {
        "base_witness": {
            "year": 1903,
            "printed_page": candidate["printed_page"],
            "pdf_index": candidate["pdf_index"],
            "occurrence_id": candidate["occurrence_id"],
        },
        "target_identity": candidate["occurrence_id"],
        "old_reading": old.lower(),
        "corrected_reading": new.lower(),
        "correction_witness": {
            "year": 1920,
            "printed_page": 50,
            "pdf_index": 63,
            "source_sha256": SRC_1920["sha256"],
            "delivery": "reopen" if access_arm == "A_ERRATUM_REOPEN" else "event_channel",
        },
        "correction_scope": {
            "page": event.get("target_page"),
            "context": event.get("context"),
            "old_explicit": "old" in event,
        },
    }


def current_token_for(occurrence, overlay):
    if overlay and overlay["target_identity"] == occurrence["occurrence_id"]:
        return overlay["corrected_reading"]
    return occurrence["token"].lower()


def evaluate_cell(
    state_arm,
    event_arm,
    access_arm,
    native_event,
    occurrences,
    target_occ,
    collateral_occ,
    parent_record,
    state_bytes,
    event_bytes,
    erratum_page_text_bytes,
):
    event, delivery = effective_event(event_arm, access_arm, native_event)
    candidates = select_candidates(
        state_arm, event_arm, access_arm, event, occurrences, target_occ
    )
    overlays = [
        o
        for o in (candidate_overlay(c, event, event_arm, access_arm) for c in candidates)
        if o is not None
    ]

    current_actions = {
        current_token_for(target_occ, o)
        for o in overlays
    }
    target_ids = {o["target_identity"] for o in overlays}
    transitions = {
        (
            o["target_identity"],
            o["old_reading"],
            o["corrected_reading"],
            o["base_witness"]["printed_page"],
            o["correction_witness"]["printed_page"],
        )
        for o in overlays
    }
    collateral_readings = {
        current_token_for(collateral_occ, o)
        for o in overlays
    }

    current_exact = bool(overlays) and current_actions == {CORRECTED_ACTION}
    transition_exact = bool(overlays) and transitions == {
        (
            target_occ["occurrence_id"],
            PARENT_ACTION,
            CORRECTED_ACTION,
            201,
            50,
        )
    }
    target_exact = bool(overlays) and target_ids == {target_occ["occurrence_id"]}
    parent_provenance_exact = target_exact
    correction_provenance_exact = bool(overlays) and all(
        o["correction_witness"]["year"] == 1920
        and o["correction_witness"]["printed_page"] == 50
        for o in overlays
    )

    # Overlay semantics never mutate the base witness.
    witness_preserved = True

    # Only action may differ in the structured Urumtsi record.
    child_record = dict(parent_record)
    if current_exact:
        child_record["action"] = CORRECTED_ACTION
    local_changed_non_action = sum(
        child_record[k] != parent_record[k]
        for k in parent_record
        if k != "action"
    )

    collateral_stable = bool(overlays) and collateral_readings == {PARENT_ACTION}

    return {
        "state_arm": state_arm,
        "event_arm": event_arm,
        "access_arm": access_arm,
        "event_delivery": delivery,
        "candidate_target_count": len(candidates),
        "overlay_candidate_count": len(overlays),
        "candidate_target_ids": [x["occurrence_id"] for x in candidates],
        "T_CURRENT_ACTION": (
            "EXACT" if current_exact else "AMBIGUOUS" if len(overlays) > 1 else "UNSUPPORTED"
        ),
        "T_TRANSITION_AUDIT": (
            "EXACT" if transition_exact else "AMBIGUOUS" if len(overlays) > 1 else "UNSUPPORTED"
        ),
        "target_binding_exact": target_exact,
        "parent_provenance_exact": parent_provenance_exact,
        "correction_provenance_exact": correction_provenance_exact,
        "T_WITNESS_PRESERVATION": witness_preserved,
        "T_LOCAL_STABILITY_non_action_changes": local_changed_non_action,
        "T_COLLATERAL_STABILITY": collateral_stable,
        "current_action_candidates": sorted(current_actions),
        "collateral_reading_candidates": sorted(collateral_readings),
        "state_payload_bytes": state_bytes,
        "event_payload_bytes": event_bytes,
        "erratum_reopen_page_text_bytes": (
            erratum_page_text_bytes if access_arm == "A_ERRATUM_REOPEN" else 0
        ),
    }


def wrong_global_replace(page_texts):
    pat = re.compile(r"(?<![A-Za-z])found(?![A-Za-z])", re.I)
    mutated = {}
    replacements = 0
    changed_pages = []
    for idx, rec in sorted(page_texts.items()):
        def repl(m):
            nonlocal replacements
            replacements += 1
            return "founded"
        new, n = pat.subn(repl, rec["text"])
        mutated[idx] = new
        if n:
            changed_pages.append(rec["printed_page"])
    page201 = norm(mutated[500])
    page113 = norm(mutated[408])
    return {
        "replacement_count": replacements,
        "changed_printed_pages": changed_pages,
        "urumtsi_current_correct": "Governor of Urumtsi founded" in page201,
        "sykes_collateral_corrupted": "I founded that there was a route" in page113,
        "source_witness_mutated": any(
            mutated[i] != page_texts[i]["text"] for i in page_texts
        ),
    }


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    raw1903 = fetch(SRC_1903["url"])
    raw1920 = fetch(SRC_1920["url"])
    if sha256(raw1903) != SRC_1903["sha256"]:
        raise RuntimeError("1903 source drift")
    if sha256(raw1920) != SRC_1920["sha256"]:
        raise RuntimeError("1920 source drift")

    page_texts = {}
    for pdf_index, printed in PAGES_1903.items():
        txt = extract_page(raw1903, pdf_index)
        page_texts[pdf_index] = {
            "printed_page": printed,
            "text": txt,
            "sha256": sha256(txt.encode("utf-8")),
        }

    erratum_text = extract_page(raw1920, PAGE_1920["pdf_index"])
    page201_norm = norm(page_texts[500]["text"])
    erratum_norm = norm(erratum_text)

    parent_record = verify_parent_fields(page201_norm)
    native_event = verify_erratum(erratum_norm)

    occurrences = token_occurrences(page_texts)
    target_occ, collateral_occ = identify_reference_occurrences(occurrences)

    # The exact two-occurrence collateral structure was inspected before execution
    # and frozen in the protocol.
    if len(occurrences) != 2:
        raise RuntimeError(f"expected exactly 2 frozen-corpus 'found' occurrences, got {len(occurrences)}")

    if {x["printed_page"] for x in occurrences} != {113, 201}:
        raise RuntimeError("unexpected found-token page distribution")

    state_payloads = {
        arm: state_payload(arm, page_texts, target_occ, parent_record)
        for arm in STATE_ARMS
    }
    event_payloads = {
        arm: event_payload(arm, native_event)
        for arm in EVENT_ARMS
    }

    matrix = []
    for s in STATE_ARMS:
        for e in EVENT_ARMS:
            for a in ACCESS_ARMS:
                matrix.append(
                    evaluate_cell(
                        s,
                        e,
                        a,
                        native_event,
                        occurrences,
                        target_occ,
                        collateral_occ,
                        parent_record,
                        len(canonical(state_payloads[s])),
                        len(canonical(event_payloads[e])),
                        len(erratum_text.encode("utf-8")),
                    )
                )

    wrong = wrong_global_replace(page_texts)

    def find_cell(s, e, a):
        return next(
            x
            for x in matrix
            if x["state_arm"] == s and x["event_arm"] == e and x["access_arm"] == a
        )

    pair_corpus = find_cell("S_CORPUS", "E_PAIR_ONLY", "A_NONE")
    pair_bound = find_cell("S_TARGET_BOUND", "E_PAIR_ONLY", "A_NONE")
    context_corpus = find_cell("S_CORPUS", "E_CONTEXT_NEW", "A_NONE")
    pair_reopen = find_cell("S_CORPUS", "E_PAIR_ONLY", "A_ERRATUM_REOPEN")

    dispositions = {
        "ERRATUM_SCOPE_BINDING_SEPARATION": (
            pair_corpus["T_TRANSITION_AUDIT"] != "EXACT"
            and (
                pair_bound["T_TRANSITION_AUDIT"] == "EXACT"
                or context_corpus["T_TRANSITION_AUDIT"] == "EXACT"
            )
        ),
        "PROVENANCE_PRESERVING_CORRECTION": any(
            x["T_CURRENT_ACTION"] == "EXACT"
            and x["T_WITNESS_PRESERVATION"]
            and x["correction_provenance_exact"]
            for x in matrix
        ),
        "COLLATERAL_CONTROL_PASS": all(
            x["T_COLLATERAL_STABILITY"]
            for x in matrix
            if x["T_CURRENT_ACTION"] == "EXACT"
            and x["T_TRANSITION_AUDIT"] == "EXACT"
        ),
        "GLOBAL_REPLACEMENT_FAILS_SELECTIVITY": (
            wrong["urumtsi_current_correct"]
            and (
                wrong["sykes_collateral_corrupted"]
                or wrong["source_witness_mutated"]
            )
        ),
        "ACCESS_REPAIRS_EVENT_ABLATION": (
            pair_corpus["T_TRANSITION_AUDIT"] != "EXACT"
            and pair_reopen["T_TRANSITION_AUDIT"] == "EXACT"
        ),
    }

    result = {
        "study": "MODULE_F_URUMTSI_PUBLISHED_ERRATUM_V1",
        "authority": "HETEROGENEOUS_REVISION_ECOLOGY_PRESSURE_TEST_ON_ALREADY_EXPOSED_SOURCES",
        "sources": {
            "1903": {
                "url": SRC_1903["url"],
                "sha256": sha256(raw1903),
                "bytes": len(raw1903),
                "selected_pages": [
                    {
                        "pdf_index": i,
                        "printed_page": rec["printed_page"],
                        "text_sha256": rec["sha256"],
                        "text_bytes": len(rec["text"].encode("utf-8")),
                    }
                    for i, rec in sorted(page_texts.items())
                ],
            },
            "1920": {
                "url": SRC_1920["url"],
                "sha256": sha256(raw1920),
                "bytes": len(raw1920),
                "erratum_pdf_index": 63,
                "printed_page": 50,
                "erratum_text_sha256": sha256(erratum_text.encode("utf-8")),
                "erratum_text_bytes": len(erratum_text.encode("utf-8")),
            },
        },
        "parent_record": parent_record,
        "natural_event": native_event,
        "frozen_corpus_found_occurrences": occurrences,
        "reference_target_occurrence": target_occ,
        "collateral_occurrence": collateral_occ,
        "matrix_cells": len(matrix),
        "matrix": matrix,
        "wrong_global_replace_control": wrong,
        "dispositions": dispositions,
        "claim_boundary": [
            "The 1903 witness remains unchanged; corrected current reading is represented by an overlay.",
            "The 1920 erratum establishes a published editorial correction, not independent historical truth about the Governor's action.",
            "The six-page 1903 corpus was frozen for an earlier review bundle before Module F.",
            "E_PAIR_ONLY is a controlled ablation of a real erratum, not a claim about historical editorial practice.",
            "Urumtsi was already used in R3 development, so Module F is heterogeneous pressure evidence rather than independent replication.",
        ],
    }

    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "found_occurrences": [
                    {
                        "id": x["occurrence_id"],
                        "printed_page": x["printed_page"],
                        "context": x["context"],
                    }
                    for x in occurrences
                ],
                "matrix": [
                    {
                        "state": x["state_arm"],
                        "event": x["event_arm"],
                        "access": x["access_arm"],
                        "targets": x["candidate_target_count"],
                        "current": x["T_CURRENT_ACTION"],
                        "transition": x["T_TRANSITION_AUDIT"],
                        "collateral_stable": x["T_COLLATERAL_STABILITY"],
                        "witness_preserved": x["T_WITNESS_PRESERVATION"],
                    }
                    for x in matrix
                ],
                "wrong_global_replace_control": wrong,
                "dispositions": dispositions,
                "results_sha256": sha256(out.read_bytes()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
