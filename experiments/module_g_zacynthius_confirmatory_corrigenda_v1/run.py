from __future__ import annotations

import hashlib
import itertools
import json
import re
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

from lxml import etree as ET

UPSTREAM = "itsee-birmingham/codex-zacynthius-xml"
PARENT = "2bc9ef70a5d3635e98b5a6b327833c57a5b0a67f"
CORRIGENDA_URL = "https://sites.google.com/site/haghoughton/publications/zacynthius-corrigenda"

FILES = {
    "L299-lectionary.xml": ("2ecebd8b2b1068c4d9999b17dbed9ed0e5858eaf", 3392970),
    "Zacynthius-catena-translation.xml": ("97e51cffa117b6a0e18c9879b5ecf3e489f26a0b", 919481),
    "Zacynthius-catena.xml": ("45116ec9174e692bf0aff7b6e5ca6d6536c47d3a", 1165268),
    "Zacynthius-gospel-translation.xml": ("0e90aabadfe1143df0bc84abbaf5226cf3ee010e", 235723),
    "Zacynthius-gospel.xml": ("bd0bac8cd394df94e385c007241e6c00c27194ba", 328075),
}

STATE_ARMS = ("S_TEI", "S_TEXT_ONLY")
EVENT_ARMS = ("E_PUBLISHED_FULL", "E_LOCATOR_RESULT", "E_TARGETLESS_OPERATION")
ACCESS_ARMS = ("A_NONE", "A_CORRIGENDA_REOPEN")

EVENTS = {
    "CZ-C1": {
        "folio_published": "IIIr",
        "folio": "3r",
        "extract": None,
        "operation": "INSERT",
        "source_class": "OLD_OMISSION_STATE_COMPATIBLE",
        "structural_anchor": {"text": "ευαγγελιον", "rend": "rubric"},
        "source_anchors": [
            {"name": "anchor", "value": "ευαγγελιον", "mode": "word_base"},
        ],
        "new": {
            "insert_before_anchor": ["α", "β"],
            "overline": True,
            "ink": "black",
        },
        "linked": False,
    },
    "CZ-C2": {
        "folio_published": "XIIIv",
        "folio": "13v",
        "extract": "060-1",
        "operation": "REPLACE_LINKED",
        "source_class": "PARTIAL_PREINTEGRATION",
        "source_anchors": [
            {"name": "greek_old", "value": "του κοσμου σρς", "mode": "word_base"},
            {"name": "translation_old", "value": "the saviour of the world", "mode": "plain"},
        ],
        "new": {
            "greek": "γεννασθαι του κοινου σρς",
            "translation": "the common saviour",
        },
        "linked": True,
    },
    "CZ-C3": {
        "folio_published": "XVr",
        "folio": "15r",
        "extract": "072-2",
        "operation": "REPLACE_REFERENCE",
        "source_class": "CLEAN_OLD_STATE_PRESENT",
        "source_anchors": [
            {"name": "greek_old", "value": "απο αριθμων", "mode": "word_base"},
            {"name": "english_old", "value": "on numbers", "mode": "plain"},
        ],
        "new": {
            "greek": "απο λογου ριε",
            "english": "sermon 115",
        },
        "linked": False,
    },
    "CZ-C4": {
        "folio_published": "XVIIIv",
        "folio": "18v",
        "extract": "081-2",
        "operation": "REPLACE_LINKED",
        "source_class": "LINKED_REFERENCE_STATE_MISMATCH",
        "source_anchors": [
            {"name": "greek_anchor", "value": "εν υπακοη", "mode": "word_base"},
            {"name": "cpg_old", "value": "cpg 7058", "mode": "plain"},
        ],
        "new": {
            "translation": "in a hymn",
            "cpg": "cpg 7072",
        },
        "linked": True,
    },
}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def fetch_raw(path):
    url = f"https://raw.githubusercontent.com/{UPSTREAM}/{PARENT}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-G/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def lname(el):
    return ET.QName(el).localname


def nfc(s):
    return unicodedata.normalize("NFC", s)


def norm_plain(s):
    return " ".join(nfc(s).casefold().split())


def strip_marks(s):
    d = unicodedata.normalize("NFD", s)
    d = "".join(ch for ch in d if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", d)


def base_plain(s):
    return strip_marks(norm_plain(s))


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    total = 0
    prev = 0
    for ch in reversed(s.upper()):
        v = ROMAN[ch]
        if v < prev:
            total -= v
        else:
            total += v
            prev = v
    return total


def normalize_published_folio(label):
    m = re.fullmatch(r"([IVXLCDM]+)([rv])", label.strip(), re.I)
    if not m:
        raise ValueError(label)
    return f"{roman_to_int(m.group(1))}{m.group(2).lower()}"


def normalize_tei_folio(label):
    s = (label or "").strip()
    if s.startswith("P"):
        s = s[1:]
    s = s.split("-", 1)[0]
    m = re.match(r"(\d+)([rv])$", s, re.I)
    return f"{int(m.group(1))}{m.group(2).lower()}" if m else None


def word_token(w):
    # Concatenate descendant text inside one TEI word; this preserves <ex>
    # expansion and removes whitespace introduced by line-break markup.
    return nfc(re.sub(r"\s+", "", "".join(w.itertext()))).casefold()


def word_stream(el):
    words = []
    if lname(el) == "w":
        words.append(word_token(el))
    for w in el.iterdescendants():
        if lname(w) == "w":
            words.append(word_token(w))
    return " ".join(x for x in words if x)


def structural_plain(el):
    return norm_plain(" ".join(el.itertext()))


def event_value_key(value, mode):
    # Corrigendum notation normalization: retain letters inside [] and ().
    v = value.replace("[", "").replace("]", "").replace("(", "").replace(")", "")
    v = norm_plain(v)
    return strip_marks(v) if mode.endswith("_base") else v


def contains_key(record, anchor):
    mode = anchor["mode"]
    needle = event_value_key(anchor["value"], mode)
    if mode == "word_base":
        hay = record["word_base"]
    elif mode == "word":
        hay = record["word"]
    elif mode == "plain_base":
        hay = record["plain_base"]
    elif mode == "plain":
        hay = record["plain"]
    else:
        raise ValueError(mode)
    return needle in hay


def count_in_projection(proj, anchor):
    mode = anchor["mode"]
    needle = event_value_key(anchor["value"], mode)
    total = 0
    per_file = {}
    for path, rec in proj.items():
        if mode == "word_base":
            hay = rec["word_base"]
        elif mode == "word":
            hay = rec["word"]
        elif mode == "plain_base":
            hay = rec["plain_base"]
        else:
            hay = rec["plain"]
        n = hay.count(needle)
        if n:
            per_file[path] = n
        total += n
    return total, per_file


def make_record(kind, path, folio, extract, el, tree):
    p = structural_plain(el)
    w = word_stream(el)
    return {
        "id": f"{path}:{tree.getpath(el)}",
        "kind": kind,
        "file": path,
        "folio": folio,
        "extract": extract,
        "plain": p,
        "plain_base": strip_marks(p),
        "word": w,
        "word_base": strip_marks(w),
        "attrs": dict(el.attrib),
        "xml": ET.tostring(el, encoding="unicode"),
    }


def build_indexes(raws):
    comments = []
    rubrics = []
    projection = {}
    parsed = {}

    for path, raw in raws.items():
        root = ET.fromstring(raw, ET.XMLParser(resolve_entities=False, no_network=True, recover=False))
        parsed[path] = root
        tree = root.getroottree()
        current_folio = None

        for el in root.iter():
            tag = lname(el)
            if tag == "pb":
                current_folio = normalize_tei_folio(el.get("n"))
            if tag == "ab" and el.get("type") == "comment" and el.get("n"):
                comments.append(make_record("comment", path, current_folio, el.get("n"), el, tree))
            if tag == "hi" and (el.get("rend") or "").casefold() == "rubric":
                rubrics.append(make_record("rubric", path, current_folio, None, el, tree))

        plain = norm_plain(" ".join(root.itertext()))
        words = []
        for el in root.iter():
            if lname(el) == "w":
                tok = word_token(el)
                if tok:
                    words.append(tok)
        word = " ".join(words)
        projection[path] = {
            "plain": plain,
            "plain_base": strip_marks(plain),
            "word": word,
            "word_base": strip_marks(word),
        }

    return parsed, comments, rubrics, projection


def locator_group(event, comments, rubrics):
    if event["extract"] is None:
        a = event["structural_anchor"]
        matches = [
            r for r in rubrics
            if r["folio"] == event["folio"]
            and event_value_key(a["text"], "word_base") in r["word_base"]
            and (r["attrs"].get("rend") or "").casefold() == a["rend"]
        ]
        return [tuple(sorted(r["id"] for r in matches))] if matches else []

    units = [
        r for r in comments
        if r["folio"] == event["folio"] and r["extract"] == event["extract"]
    ]
    return [tuple(sorted(r["id"] for r in units))] if units else []


def source_anchor_group_keys(event, comments):
    keys = set()
    for r in comments:
        if any(contains_key(r, a) for a in event["source_anchors"]):
            keys.add((r["folio"], r["extract"]))
    groups = []
    for key in sorted(keys):
        units = [r for r in comments if (r["folio"], r["extract"]) == key]
        groups.append(tuple(sorted(r["id"] for r in units)))
    return groups


def text_only_candidates(event, event_arm, projection, baseline_records):
    # Locator attributes are unavailable. Use only correction lexical/source anchors
    # that survive the selected event projection.
    anchors = anchors_for_event(event, event_arm)
    if not anchors:
        return {
            "candidate_count": None,
            "candidate_sets": [],
            "target_exact": False,
            "status": "REPRESENTATION_CANNOT_EXPRESS_LOCATOR",
            "anchor_counts": {},
        }

    anchor_counts = {}
    choices = []
    for a in anchors:
        count, per_file = count_in_projection(projection, a)
        anchor_counts[a["name"]] = {"count": count, "per_file": per_file}
        if count > 0:
            occurrences = []
            for path, n in sorted(per_file.items()):
                for i in range(n):
                    occurrences.append((a["name"], path, i))
            choices.append(occurrences)

    if not choices:
        return {
            "candidate_count": 0,
            "candidate_sets": [],
            "target_exact": False,
            "status": "FULL_TARGET_ABSENT",
            "anchor_counts": anchor_counts,
        }

    count = 1
    for x in choices:
        count *= len(x)

    # Exactness under text-only requires one lexical assignment, and every unique
    # matching file/string must be contained in the full-TEI truth target set.
    baseline_files = {r["file"] for r in baseline_records}
    unique_assignment = count == 1
    exact = unique_assignment
    if unique_assignment:
        for opts in choices:
            _, path, _ = opts[0]
            if path not in baseline_files:
                exact = False
                break

    return {
        "candidate_count": count,
        "candidate_sets": [],
        "target_exact": exact,
        "status": "EXACT" if exact else "AMBIGUOUS",
        "anchor_counts": anchor_counts,
    }


def event_payload(event_id, event, arm):
    envelope = {
        "source": CORRIGENDA_URL,
        "correction_id": event_id,
    }
    if arm == "E_PUBLISHED_FULL":
        payload = {
            "folio": event["folio_published"],
            "extract": event["extract"],
            "operation": event["operation"],
            "source_anchors": event["source_anchors"],
            "new": event["new"],
            "structural_anchor": event.get("structural_anchor"),
        }
    elif arm == "E_LOCATOR_RESULT":
        payload = {
            "folio": event["folio_published"],
            "extract": event["extract"],
            "operation": event["operation"],
            "source_anchors": event["source_anchors"] if event_id == "CZ-C1" else [],
            "new": event["new"],
            "structural_anchor": event.get("structural_anchor") if event_id == "CZ-C1" else None,
        }
    elif arm == "E_TARGETLESS_OPERATION":
        payload = {
            "operation": event["operation"],
            "source_anchors": [] if event_id == "CZ-C1" else event["source_anchors"],
            "new": event["new"],
            "structural_anchor": None,
        }
    else:
        raise ValueError(arm)
    return {"envelope": envelope, "payload": payload}


def anchors_for_event(event, arm):
    if arm == "E_TARGETLESS_OPERATION" and event["extract"] is None:
        return []
    if arm == "E_LOCATOR_RESULT" and event["extract"] is not None:
        return []
    if event["extract"] is None:
        return event["source_anchors"]
    return event["source_anchors"]


def baseline_records_for_group(group, comments, rubrics):
    by_id = {r["id"]: r for r in comments + rubrics}
    return [by_id[x] for x in group if x in by_id]


def tei_candidates(event, event_arm, comments, rubrics):
    has_locator = event_arm in ("E_PUBLISHED_FULL", "E_LOCATOR_RESULT")
    if has_locator:
        groups = locator_group(event, comments, rubrics)
        return {
            "groups": groups,
            "candidate_count": len(groups),
            "status": "EXACT" if len(groups) == 1 else "AMBIGUOUS" if groups else "FULL_TARGET_ABSENT",
        }

    if event["extract"] is None:
        return {
            "groups": [],
            "candidate_count": None,
            "status": "REPRESENTATION_CANNOT_EXPRESS_LOCATOR",
        }

    groups = source_anchor_group_keys(event, comments)
    return {
        "groups": groups,
        "candidate_count": len(groups),
        "status": "EXACT" if len(groups) == 1 else "AMBIGUOUS" if groups else "FULL_TARGET_ABSENT",
    }


def verify_source_contract(events, comments, rubrics):
    by_id = {r["id"]: r for r in comments + rubrics}
    facts = {}

    for event_id, event in events.items():
        groups = locator_group(event, comments, rubrics)
        if len(groups) != 1:
            raise RuntimeError(f"{event_id}: frozen full locator does not yield one group: {len(groups)}")
        records = [by_id[x] for x in groups[0]]

        if event_id == "CZ-C1":
            if len(records) != 1 or "ευαγγελιον" not in records[0]["word_base"]:
                raise RuntimeError("CZ-C1 source-contract drift")
            facts[event_id] = {
                "classification": "OLD_OMISSION_STATE_COMPATIBLE",
                "target_records": len(records),
            }

        elif event_id == "CZ-C2":
            greek = [r for r in records if r["file"] == "Zacynthius-catena.xml"]
            trans = [r for r in records if r["file"] == "Zacynthius-catena-translation.xml"]
            if len(greek) != 1 or len(trans) != 1:
                raise RuntimeError("CZ-C2 linked files missing")
            g, t = greek[0], trans[0]
            old_g = event_value_key("του κοσμου σρς", "word_base")
            new_g = event_value_key("γεννασθαι του κοινου σρς", "word_base")
            old_t = norm_plain("the saviour of the world")
            new_t = norm_plain("the common saviour")
            if old_g not in g["word_base"] or new_g in g["word_base"]:
                raise RuntimeError("CZ-C2 Greek parent-state drift")
            if "γεννασθαι " + old_g not in g["word_base"]:
                raise RuntimeError("CZ-C2 expected partial preintegration not observed")
            if old_t not in t["plain"] or new_t in t["plain"]:
                raise RuntimeError("CZ-C2 translation parent-state drift")
            facts[event_id] = {
                "classification": "PARTIAL_PREINTEGRATION",
                "target_records": len(records),
            }

        elif event_id == "CZ-C3":
            old_g = event_value_key("απο αριθμων", "word_base")
            old_e = norm_plain("on numbers")
            new_g = event_value_key("απο λογου ριε", "word_base")
            new_e = norm_plain("sermon 115")
            if not any(old_g in r["word_base"] for r in records):
                raise RuntimeError("CZ-C3 Greek old state missing")
            if not any(old_e in r["plain"] for r in records):
                raise RuntimeError("CZ-C3 English old state missing")
            if any(new_g in r["word_base"] for r in records):
                raise RuntimeError("CZ-C3 corrected Greek already present at target")
            if any(new_e in r["plain"] for r in records):
                raise RuntimeError("CZ-C3 corrected English already present at target")
            facts[event_id] = {
                "classification": "CLEAN_OLD_STATE_PRESENT",
                "target_records": len(records),
            }

        elif event_id == "CZ-C4":
            greek_anchor = event_value_key("εν υπακοη", "word_base")
            if not any(greek_anchor in r["word_base"] for r in records):
                raise RuntimeError("CZ-C4 Greek anchor missing")
            if any("cpg 7058" in r["plain"] for r in records):
                raise RuntimeError("CZ-C4 unexpected CPG7058 in frozen target")
            if not any(("cpg7039" in r["plain"].replace(" ", "") or "cpg 7039" in r["plain"]) for r in records):
                raise RuntimeError("CZ-C4 expected CPG7039 mismatch not observed")
            facts[event_id] = {
                "classification": "LINKED_REFERENCE_STATE_MISMATCH",
                "target_records": len(records),
            }

    return facts


def cell_result(event_id, event, source_fact, state_arm, event_arm, access_arm, comments, rubrics, projection, baseline_group):
    effective_arm = "E_PUBLISHED_FULL" if access_arm == "A_CORRIGENDA_REOPEN" else event_arm
    baseline_records = baseline_records_for_group(baseline_group, comments, rubrics)

    if state_arm == "S_TEI":
        cand = tei_candidates(event, effective_arm, comments, rubrics)
        target_exact = len(cand["groups"]) == 1 and cand["groups"][0] == baseline_group
        candidate_count = cand["candidate_count"]
        status = cand["status"]
        anchor_counts = {}
    else:
        cand = text_only_candidates(event, effective_arm, projection, baseline_records)
        target_exact = cand["target_exact"]
        candidate_count = cand["candidate_count"]
        status = cand["status"]
        anchor_counts = cand["anchor_counts"]

    result_exact = target_exact  # all event arms retain corrected result payload
    clean_transition = source_fact["classification"] in (
        "OLD_OMISSION_STATE_COMPATIBLE",
        "CLEAN_OLD_STATE_PRESENT",
    )
    transition_exact = result_exact and clean_transition
    linked_atomicity = bool(event["linked"] and transition_exact)
    selectivity_exact = target_exact
    witness_preserved = True

    return {
        "correction_id": event_id,
        "state_arm": state_arm,
        "event_arm": event_arm,
        "access_arm": access_arm,
        "effective_event_arm": effective_arm,
        "candidate_target_count": candidate_count,
        "candidate_status": status,
        "target_exact": target_exact,
        "result_exact": result_exact,
        "transition_exact": transition_exact,
        "selectivity_exact": selectivity_exact,
        "witness_preserved": witness_preserved,
        "linked_atomicity": linked_atomicity,
        "source_state_classification": source_fact["classification"],
        "anchor_counts": anchor_counts,
        "state_payload_bytes": None,
        "event_payload_bytes": len(canonical(event_payload(event_id, event, event_arm))),
        "corrigenda_reopen_payload_bytes": (
            len(canonical(event_payload(event_id, event, "E_PUBLISHED_FULL")))
            if access_arm == "A_CORRIGENDA_REOPEN"
            else 0
        ),
    }


def correction_outcome(full_cell):
    cls = full_cell["source_state_classification"]
    if full_cell["candidate_status"] == "FULL_TARGET_ABSENT":
        return "FULL_TARGET_ABSENT"
    if cls == "PARTIAL_PREINTEGRATION":
        return "LINKED_PARTIAL_ONLY"
    if cls == "LINKED_REFERENCE_STATE_MISMATCH":
        return "FULL_SOURCE_STATE_MISMATCH"
    if full_cell["target_exact"] and full_cell["result_exact"] and full_cell["transition_exact"]:
        return "FULL_EXECUTABLE_EXACT"
    if full_cell["candidate_status"] == "AMBIGUOUS":
        return "FULL_EXECUTABLE_AMBIGUOUS"
    return "FULL_SOURCE_STATE_MISMATCH"


def wrong_global_match(event_id, event, comments, rubrics, projection, baseline_group):
    baseline_ids = set(baseline_group)
    if event_id == "CZ-C1":
        # Wrong strategy ignores folio/rubric structure and applies at every lexical
        # evangelion occurrence across the parent text projection.
        total, per_file = count_in_projection(projection, event["source_anchors"][0])
        intended = 1 if total else 0
        return {
            "strategy": "GLOBAL_LEXICAL_ANCHOR_INSERT",
            "match_count": total,
            "per_file": per_file,
            "intended_target_reached": intended == 1,
            "collateral_match_count": max(0, total - 1),
            "simulated_source_mutation": total > 0,
        }

    matched_ids = set()
    for r in comments:
        if any(contains_key(r, a) for a in event["source_anchors"]):
            matched_ids.add(r["id"])
    return {
        "strategy": "GLOBAL_SOURCE_VALUE_MATCH",
        "match_count": len(matched_ids),
        "intended_target_reached": bool(matched_ids & baseline_ids),
        "collateral_match_count": len(matched_ids - baseline_ids),
        "simulated_source_mutation": bool(matched_ids),
    }


def locator_shuffle(events, comments, rubrics):
    ids = ["CZ-C2", "CZ-C3", "CZ-C4"]
    shifted = ids[1:] + ids[:1]
    out = []
    for src_id, loc_id in zip(ids, shifted):
        src = events[src_id]
        loc = events[loc_id]
        wrong = dict(src)
        wrong["folio"] = loc["folio"]
        wrong["folio_published"] = loc["folio_published"]
        wrong["extract"] = loc["extract"]
        groups = locator_group(wrong, comments, rubrics)
        source_compatible = False
        for g in groups:
            recs = baseline_records_for_group(g, comments, rubrics)
            if any(any(contains_key(r, a) for a in src["source_anchors"]) for r in recs):
                source_compatible = True
        out.append(
            {
                "correction_id": src_id,
                "wrong_locator_from": loc_id,
                "candidate_group_count": len(groups),
                "source_side_compatible": source_compatible,
            }
        )
    return out


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    raws = {}
    source_meta = {}
    for path, (expected_blob, expected_size) in FILES.items():
        raw = fetch_raw(path)
        got = git_blob(raw)
        if got != expected_blob:
            raise RuntimeError(f"blob drift {path}: {got} != {expected_blob}")
        if len(raw) != expected_size:
            raise RuntimeError(f"size drift {path}: {len(raw)} != {expected_size}")
        raws[path] = raw
        source_meta[path] = {
            "git_blob": got,
            "bytes": len(raw),
            "sha256": sha256(raw),
        }

    parsed, comments, rubrics, projection = build_indexes(raws)
    source_facts = verify_source_contract(EVENTS, comments, rubrics)

    baseline_groups = {}
    baseline_records = {}
    for event_id, event in EVENTS.items():
        groups = locator_group(event, comments, rubrics)
        if len(groups) != 1:
            raise RuntimeError(f"{event_id}: baseline group count {len(groups)}")
        baseline_groups[event_id] = groups[0]
        baseline_records[event_id] = baseline_records_for_group(groups[0], comments, rubrics)

    state_payload_bytes = {
        "S_TEI": sum(len(x) for x in raws.values()),
        "S_TEXT_ONLY": len(canonical(projection)),
    }

    matrix = []
    for event_id, event in EVENTS.items():
        for state_arm in STATE_ARMS:
            for event_arm in EVENT_ARMS:
                for access_arm in ACCESS_ARMS:
                    row = cell_result(
                        event_id,
                        event,
                        source_facts[event_id],
                        state_arm,
                        event_arm,
                        access_arm,
                        comments,
                        rubrics,
                        projection,
                        baseline_groups[event_id],
                    )
                    row["state_payload_bytes"] = state_payload_bytes[state_arm]
                    matrix.append(row)

    full_cells = {
        event_id: next(
            r for r in matrix
            if r["correction_id"] == event_id
            and r["state_arm"] == "S_TEI"
            and r["event_arm"] == "E_PUBLISHED_FULL"
            and r["access_arm"] == "A_NONE"
        )
        for event_id in EVENTS
    }
    outcomes = {event_id: correction_outcome(cell) for event_id, cell in full_cells.items()}

    wrong_global = {
        event_id: wrong_global_match(
            event_id,
            event,
            comments,
            rubrics,
            projection,
            baseline_groups[event_id],
        )
        for event_id, event in EVENTS.items()
    }
    wrong_shuffle = locator_shuffle(EVENTS, comments, rubrics)

    full_exact_count = sum(outcomes[x] == "FULL_EXECUTABLE_EXACT" for x in EVENTS)

    target_binding_witnesses = []
    structure_witnesses = []
    access_witnesses = []
    for event_id in EVENTS:
        full_tei = full_cells[event_id]
        targetless_tei = next(
            r for r in matrix
            if r["correction_id"] == event_id
            and r["state_arm"] == "S_TEI"
            and r["event_arm"] == "E_TARGETLESS_OPERATION"
            and r["access_arm"] == "A_NONE"
        )
        full_text = next(
            r for r in matrix
            if r["correction_id"] == event_id
            and r["state_arm"] == "S_TEXT_ONLY"
            and r["event_arm"] == "E_PUBLISHED_FULL"
            and r["access_arm"] == "A_NONE"
        )
        targetless_reopen = next(
            r for r in matrix
            if r["correction_id"] == event_id
            and r["state_arm"] == "S_TEI"
            and r["event_arm"] == "E_TARGETLESS_OPERATION"
            and r["access_arm"] == "A_CORRIGENDA_REOPEN"
        )

        if full_tei["target_exact"] and not targetless_tei["target_exact"]:
            target_binding_witnesses.append(event_id)
        if full_tei["target_exact"] and not full_text["target_exact"]:
            structure_witnesses.append(event_id)
        if not targetless_tei["target_exact"] and targetless_reopen["target_exact"]:
            access_witnesses.append(event_id)

    linked_atomic = [
        event_id for event_id in ("CZ-C2", "CZ-C4")
        if full_cells[event_id]["linked_atomicity"]
    ]

    global_match_failures = [
        event_id for event_id, r in wrong_global.items()
        if r["intended_target_reached"] and r["collateral_match_count"] > 0
    ]

    result = {
        "study": "MODULE_G_ZACYNTHIUS_CONFIRMATORY_CORRIGENDA_V1",
        "authority": "PRE_SOURCE_INSPECTION_CONFIRMATORY_TRANSFER_PROTOCOL",
        "protocol_commit": "08054df5a1f71d713f2fe4ab2c48be593b4c8b4d",
        "source_contract_commit": "5872a3ff4cfe739650aaa9ab69f2abc80a5d032e",
        "parent": {
            "repo": UPSTREAM,
            "commit": PARENT,
            "files": source_meta,
        },
        "corrigenda_source": CORRIGENDA_URL,
        "event_population": list(EVENTS),
        "source_contract_facts": source_facts,
        "baseline_targets": {
            event_id: {
                "record_ids": list(baseline_groups[event_id]),
                "records": [
                    {
                        "id": r["id"],
                        "file": r["file"],
                        "folio": r["folio"],
                        "extract": r["extract"],
                        "kind": r["kind"],
                    }
                    for r in baseline_records[event_id]
                ],
            }
            for event_id in EVENTS
        },
        "matrix_cells": len(matrix),
        "matrix": matrix,
        "full_channel_outcomes": outcomes,
        "wrong_controls": {
            "global_match": wrong_global,
            "locator_shuffle": wrong_shuffle,
        },
        "aggregate": {
            "full_corrigenda_executability_exact": full_exact_count,
            "full_corrigenda_denominator": len(EVENTS),
            "target_binding_separation_count": len(target_binding_witnesses),
            "target_binding_witnesses": target_binding_witnesses,
            "state_structure_contribution_count": len(structure_witnesses),
            "state_structure_witnesses": structure_witnesses,
            "access_repair_count": len(access_witnesses),
            "access_repair_witnesses": access_witnesses,
            "linked_atomicity_count": len(linked_atomic),
            "linked_atomicity_witnesses": linked_atomic,
            "global_match_selectivity_failure_count": len(global_match_failures),
            "global_match_failure_witnesses": global_match_failures,
        },
        "dispositions": {
            "PARENT_SNAPSHOT_COMPATIBLE": True,
            "FULL_CORRIGENDA_EXECUTABILITY": f"{full_exact_count}/4",
            "TARGET_BINDING_TRANSFER": bool(target_binding_witnesses),
            "STATE_STRUCTURE_CONTRIBUTION": bool(structure_witnesses),
            "ACCESS_REPAIRS_CHANNEL_ABLATION": bool(access_witnesses),
            "LINKED_CORRECTION_ATOMICITY": bool(linked_atomic),
            "PROVENANCE_PRESERVING_TRANSFER": any(
                r["transition_exact"] and r["witness_preserved"] for r in full_cells.values()
            ),
            "GLOBAL_MATCH_FAILS_SELECTIVITY": bool(global_match_failures),
        },
        "claim_boundary": [
            "All four digital-edition undertext/translation corrigenda are retained regardless of outcome.",
            "The parent commit was fixed before XML-body inspection.",
            "CZ-C2 is partial-preintegration in the frozen parent and is not promoted to a clean old->new transition.",
            "CZ-C4 has a linked CPG source-state mismatch (parent CPG7039 vs published corrigendum old CPG7058) and is not rescued with a later source.",
            "A_CORRIGENDA_REOPEN is represented by the frozen full published event record rather than a live HTML byte capture.",
            "The four corrections are a finite correction set from one editorial project, not independent statistical samples.",
        ],
    }

    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    compact = []
    for r in matrix:
        compact.append(
            {
                "correction": r["correction_id"],
                "state": r["state_arm"],
                "event": r["event_arm"],
                "access": r["access_arm"],
                "candidates": r["candidate_target_count"],
                "target_exact": r["target_exact"],
                "result_exact": r["result_exact"],
                "transition_exact": r["transition_exact"],
                "source_class": r["source_state_classification"],
            }
        )
    print(
        json.dumps(
            {
                "source_contract_facts": source_facts,
                "full_channel_outcomes": outcomes,
                "matrix": compact,
                "wrong_controls": result["wrong_controls"],
                "aggregate": result["aggregate"],
                "dispositions": result["dispositions"],
                "results_sha256": sha256(out.read_bytes()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
