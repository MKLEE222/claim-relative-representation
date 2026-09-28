"""Module C: continuation retention across the pinned Frankenstein C18 native pipeline.

Development evidence only. No LLM calls; no independent transfer claim.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import html
import json
import re
import urllib.request
from pathlib import Path

from lxml import etree as E

PIN = "5a208f869ff1213defa000e3181d5315a072a15f"

STAGES = [
    (
        "RAW_SOURCE",
        "collationChunks/C18/msColl_C18.xml",
        "8e537331ebf46dd4f013da9afcbe38c14092b6fd",
        "SOURCE_XML",
    ),
    (
        "INPUT_PRE",
        "collationChunks/C18/input-pre/msColl_C18.xml",
        "8e537331ebf46dd4f013da9afcbe38c14092b6fd",
        "SOURCE_XML",
    ),
    (
        "INPUT",
        "collationChunks/C18/input/msColl_C18.xml",
        "5bd2088e072805be05f1238dc3312764c8de0417",
        "SOURCE_XML",
    ),
    (
        "PARTWAY_APPARATUS",
        "collationChunks/C18/output/Collation_C18-partway.xml",
        "008910e1a253e2ac2e6245e533f4b5de14ca3708",
        "APPARATUS_XML",
    ),
    (
        "COMPLETE_APPARATUS",
        "collationChunks/C18/output/Collation_C18-complete.xml",
        "bca0548912ab1d7b2676360d33a6468290296d7e",
        "APPARATUS_XML",
    ),
]

TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
NAME_RE = re.compile(r"^</?\s*([A-Za-z_][A-Za-z0-9_.:-]*)")
ATTR_RE = re.compile(
    r"([A-Za-z_][A-Za-z0-9_.:-]*)\s*=\s*(?:\"([^\"]*)\"|'([^']*)')"
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def canon(x: object) -> bytes:
    return json.dumps(
        x,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def norm_text(x: str) -> str:
    return " ".join(x.split())


def tag_local_name(token: str) -> str | None:
    m = NAME_RE.match(token)
    if not m:
        return None
    return m.group(1).split(":")[-1]


def attrs(token: str) -> dict[str, str]:
    out = {}
    for m in ATTR_RE.finditer(token):
        out[m.group(1)] = html.unescape(m.group(2) if m.group(2) is not None else m.group(3))
    return out


def scan_stream(stream: str):
    """Lexically scan source-like markup, retaining state across arbitrary boundaries."""
    scopes = {}
    active_add = {}
    active_cancel = []
    cancel_counter = 0
    errors = []

    def emit(raw_text: str):
        if not raw_text:
            return
        txt = html.unescape(raw_text)
        for sid, scope in active_add.items():
            scope["_text"].append(txt)
            for c in active_cancel:
                cid = c["cid"]
                if cid not in scope["_cancel_meta"]:
                    scope["_cancel_meta"][cid] = {
                        "element": c["element"],
                        "rend": c["rend"],
                        "xml_id": c["xml_id"],
                    }
                    scope["_cancel_text"][cid] = []
                scope["_cancel_text"][cid].append(txt)

    pos = 0
    for m in TAG_RE.finditer(stream):
        emit(stream[pos:m.start()])
        token = m.group()
        pos = m.end()

        if token.startswith("<!--") or token.startswith("<?") or token.startswith("<!"):
            continue

        name = tag_local_name(token)
        if not name:
            continue
        closing = token.startswith("</")
        a = attrs(token)

        if name == "sga-add" and not closing:
            sid, eid = a.get("sID"), a.get("eID")
            if bool(sid) == bool(eid):
                errors.append({"type": "AMBIGUOUS_SGA_ADD_MARKER", "token": token[:200]})
                continue
            if sid:
                if sid in scopes or sid in active_add:
                    errors.append({"type": "DUPLICATE_SID", "sid": sid})
                    continue
                scope = {
                    "sid": sid,
                    "start_attrs": a,
                    "_text": [],
                    "_cancel_meta": {},
                    "_cancel_text": {},
                }
                scopes[sid] = scope
                active_add[sid] = scope
            else:
                if eid not in active_add:
                    errors.append({"type": "UNBOUND_EID", "sid": eid})
                else:
                    active_add.pop(eid)
            continue

        if name in {"del", "mdel"}:
            if closing:
                if not active_cancel or active_cancel[-1]["element"] != name:
                    errors.append({
                        "type": "UNBALANCED_CANCEL_CLOSE",
                        "element": name,
                        "token": token[:200],
                        "active": [x["element"] for x in active_cancel[-5:]],
                    })
                else:
                    active_cancel.pop()
            elif not token.rstrip().endswith("/>"):
                cancel_counter += 1
                active_cancel.append({
                    "cid": cancel_counter,
                    "element": name,
                    "rend": a.get("rend", "NOT_ENCODED"),
                    "xml_id": a.get("xml:id", "NOT_ENCODED"),
                })

    emit(stream[pos:])

    if active_add:
        errors.append({
            "type": "UNCLOSED_SGA_ADD",
            "sids": sorted(active_add)[:20],
            "count": len(active_add),
        })
    if active_cancel:
        errors.append({
            "type": "UNCLOSED_CANCEL",
            "elements": [x["element"] for x in active_cancel[-20:]],
            "count": len(active_cancel),
        })

    for scope in scopes.values():
        cancels = []
        for cid in sorted(scope["_cancel_meta"]):
            txt = norm_text("".join(scope["_cancel_text"][cid]))
            if not txt:
                continue
            meta = scope["_cancel_meta"][cid]
            cancels.append({
                "element": meta["element"],
                "text": txt,
                "rend": meta["rend"],
                "xml_id": meta["xml_id"],
            })
        scope["cancellations"] = cancels
        scope["current_answer"] = {
            "text": norm_text("".join(scope["_text"])),
            "place": scope["start_attrs"].get("place", "NOT_ENCODED"),
            "hand": scope["start_attrs"].get("hand", "NOT_ENCODED"),
        }
        for k in ("_text", "_cancel_meta", "_cancel_text"):
            scope.pop(k)

    xmlid_to_sids = collections.defaultdict(list)
    for sid, scope in scopes.items():
        xid = scope["start_attrs"].get("xml:id")
        scope["xml_id"] = xid
        if xid:
            xmlid_to_sids[xid].append(sid)

    incoming = collections.defaultdict(list)
    for sid, scope in scopes.items():
        nxt = scope["start_attrs"].get("next")
        if nxt and nxt.startswith("#"):
            targets = xmlid_to_sids.get(nxt[1:], [])
            if len(targets) == 1:
                incoming[targets[0]].append(sid)

    for sid, scope in scopes.items():
        nxt = scope["start_attrs"].get("next")
        if not nxt:
            outgoing = {
                "literal": None,
                "resolution": "NONE",
                "target_sid": None,
            }
        elif nxt.startswith("#"):
            targets = xmlid_to_sids.get(nxt[1:], [])
            if len(targets) == 1:
                outgoing = {
                    "literal": nxt,
                    "resolution": "RESOLVED_INTERNAL_UNIQUE",
                    "target_sid": targets[0],
                }
            elif not targets:
                outgoing = {
                    "literal": nxt,
                    "resolution": "UNRESOLVED_INTERNAL_ID",
                    "target_sid": None,
                }
            else:
                outgoing = {
                    "literal": nxt,
                    "resolution": "AMBIGUOUS_INTERNAL_ID",
                    "target_sid": None,
                }
        else:
            outgoing = {
                "literal": nxt,
                "resolution": "EXTERNAL_OR_NONLOCAL",
                "target_sid": None,
            }

        scope["reference"] = {
            "B_INCOMING": sorted(incoming.get(sid, [])),
            "B_OUTGOING": outgoing,
            "B_CANCEL": scope["cancellations"],
        }

    return {
        "scopes": scopes,
        "errors": errors,
        "stream_sha256": sha256(stream.encode("utf-8")),
        "stream_bytes": len(stream.encode("utf-8")),
    }


def download(path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{PIN}/{path}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CRR-module-C/1.0"},
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def apparatus_manuscript_stream(raw: bytes):
    root = E.fromstring(
        raw,
        E.XMLParser(collect_ids=False, resolve_entities=False, no_network=True),
    )
    apps = [e for e in root.iter() if E.QName(e).localname == "app"]
    pieces = []
    multi = []
    missing = []
    fms_count = 0

    for i, app in enumerate(apps, 1):
        rdgs = [
            e
            for e in app.iter()
            if E.QName(e).localname == "rdg"
            and (e.get("wit") or "").strip() == "fMS"
        ]
        if len(rdgs) > 1:
            multi.append({"app_ordinal": i, "count": len(rdgs)})
        if len(rdgs) == 0:
            missing.append(i)
            pieces.append("")
            continue
        fms_count += len(rdgs)
        # If the upstream file has >1 fMS reading in an app, retain all in
        # document order and record the support warning rather than choosing one.
        pieces.append(" ".join("".join(r.itertext()) for r in rdgs))

    stream = "\n".join(pieces)
    return stream, {
        "app_count": len(apps),
        "fms_reading_count": fms_count,
        "apps_with_multiple_fms": multi,
        "apps_without_fms": missing,
    }


def is_positive(family: str, value) -> bool:
    if family == "B_INCOMING":
        return bool(value)
    if family == "B_OUTGOING":
        return value["literal"] is not None
    if family == "B_CANCEL":
        return bool(value)
    raise KeyError(family)


def compare_stage(reference, stage):
    ref_scopes = reference["scopes"]
    st_scopes = stage["scopes"]
    ref_ids = set(ref_scopes)
    st_ids = set(st_scopes)
    missing = sorted(ref_ids - st_ids)
    extra = sorted(st_ids - ref_ids)

    current_exact = 0
    current_changed = []
    branch_exact = 0
    branch_changed = []
    positive_ref = []
    positive_retained = []
    introduced_positive = []

    for sid in sorted(ref_ids):
        if sid not in st_scopes:
            current_changed.append({
                "sid": sid,
                "reason": "MISSING_SCOPE",
            })
            for fam in ("B_INCOMING", "B_OUTGOING", "B_CANCEL"):
                branch_changed.append({
                    "sid": sid,
                    "family": fam,
                    "reason": "MISSING_SCOPE",
                })
                if is_positive(fam, ref_scopes[sid]["reference"][fam]):
                    positive_ref.append([sid, fam])
            continue

        if ref_scopes[sid]["current_answer"] == st_scopes[sid]["current_answer"]:
            current_exact += 1
        else:
            current_changed.append({
                "sid": sid,
                "reference": ref_scopes[sid]["current_answer"],
                "stage": st_scopes[sid]["current_answer"],
            })

        for fam in ("B_INCOMING", "B_OUTGOING", "B_CANCEL"):
            rv = ref_scopes[sid]["reference"][fam]
            sv = st_scopes[sid]["reference"][fam]
            if is_positive(fam, rv):
                positive_ref.append([sid, fam])
            if rv == sv:
                branch_exact += 1
                if is_positive(fam, rv):
                    positive_retained.append([sid, fam])
            else:
                branch_changed.append({
                    "sid": sid,
                    "family": fam,
                    "reference": rv,
                    "stage": sv,
                })
            if (not is_positive(fam, rv)) and is_positive(fam, sv):
                introduced_positive.append([sid, fam])

    return {
        "reference_scope_count": len(ref_ids),
        "stage_scope_count": len(st_ids),
        "scope_inventory_exact": not missing and not extra,
        "missing_scope_ids": missing,
        "extra_scope_ids": extra,
        "current_answer_exact": current_exact,
        "current_answer_changed_count": len(current_changed),
        "current_answer_changes": current_changed,
        "branch_family_decisions_exact": branch_exact,
        "branch_family_decisions_total": 3 * len(ref_ids),
        "branch_changed_count": len(branch_changed),
        "branch_changes": branch_changed,
        "reference_positive_branch_instances": len(positive_ref),
        "positive_branch_instances_exactly_retained": len(positive_retained),
        "retained_positive_coordinates": positive_retained,
        "introduced_positive_count": len(introduced_positive),
        "introduced_positive_coordinates": introduced_positive,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("results"),
    )
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    stage_records = []
    for name, path, expected_blob, kind in STAGES:
        raw = download(path)
        got_blob = git_blob_sha1(raw)
        if got_blob != expected_blob:
            raise RuntimeError(
                f"source drift {name}: expected {expected_blob}, got {got_blob}"
            )

        if kind == "SOURCE_XML":
            stream = raw.decode("utf-8")
            extraction = {
                "kind": kind,
                "source_file_bytes": len(raw),
            }
        else:
            stream, extraction = apparatus_manuscript_stream(raw)
            extraction["kind"] = kind
            extraction["source_file_bytes"] = len(raw)

        scan = scan_stream(stream)
        stage_records.append({
            "name": name,
            "path": path,
            "git_blob_sha1": got_blob,
            "file_sha256": sha256(raw),
            "extraction": extraction,
            "scan": scan,
        })

    reference = stage_records[0]["scan"]
    if reference["errors"]:
        raise RuntimeError(
            "RAW_SOURCE scanner support stop: "
            + json.dumps(reference["errors"][:10])
        )
    if len(reference["scopes"]) != 112:
        raise RuntimeError(
            f"RAW_SOURCE scope count drift: {len(reference['scopes'])}"
        )

    comparisons = {}
    for rec in stage_records:
        if rec["scan"]["errors"]:
            comparisons[rec["name"]] = {
                "supported": False,
                "scan_errors": rec["scan"]["errors"],
            }
        else:
            comp = compare_stage(reference, rec["scan"])
            comp["supported"] = True
            comparisons[rec["name"]] = comp

    positive_coords = []
    for sid in sorted(reference["scopes"]):
        for fam in ("B_INCOMING", "B_OUTGOING", "B_CANCEL"):
            if is_positive(
                fam,
                reference["scopes"][sid]["reference"][fam],
            ):
                positive_coords.append([sid, fam])

    delayed = []
    for sid, fam in positive_coords:
        first_loss = "NEVER_LOST_IN_REGISTERED_PIPELINE"
        stage_states = []
        refval = reference["scopes"][sid]["reference"][fam]
        for rec in stage_records:
            comp_supported = not rec["scan"]["errors"]
            if not comp_supported:
                exact = False
                state = "UNSUPPORTED_STAGE"
            elif sid not in rec["scan"]["scopes"]:
                exact = False
                state = "MISSING_SCOPE"
            else:
                val = rec["scan"]["scopes"][sid]["reference"][fam]
                exact = val == refval
                state = val
            stage_states.append({
                "stage": rec["name"],
                "exact": exact,
                "state": state,
            })
            if (
                rec["name"] != "RAW_SOURCE"
                and not exact
                and first_loss == "NEVER_LOST_IN_REGISTERED_PIPELINE"
            ):
                first_loss = rec["name"]

        delayed.append({
            "sid": sid,
            "family": fam,
            "reference": refval,
            "first_loss": first_loss,
            "stages": stage_states,
        })

    result = {
        "study": "MODULE_C_FV_NATIVE_PIPELINE_CONTINUATION_RETENTION_V1",
        "authority": "DEVELOPMENT_ON_ALREADY_EXPOSED_C18",
        "upstream_commit": PIN,
        "r2_current_task_baseline": (
            "R2 native replay separately established exact C18 collation "
            "reproduction at the published complete apparatus."
        ),
        "stages": [
            {
                "name": r["name"],
                "path": r["path"],
                "git_blob_sha1": r["git_blob_sha1"],
                "file_sha256": r["file_sha256"],
                "extraction": r["extraction"],
                "stream_sha256": r["scan"]["stream_sha256"],
                "stream_bytes": r["scan"]["stream_bytes"],
                "scan_error_count": len(r["scan"]["errors"]),
                "scan_errors": r["scan"]["errors"],
                "scope_count": len(r["scan"]["scopes"]),
            }
            for r in stage_records
        ],
        "comparisons_to_raw": comparisons,
        "reference_positive_branch_instance_count": len(positive_coords),
        "reference_positive_coordinates": positive_coords,
        "delayed_dependence": delayed,
        "first_loss_distribution": dict(
            sorted(
                collections.Counter(
                    x["first_loss"] for x in delayed
                ).items()
            )
        ),
        "claim_boundaries": [
            "All stages belong to already-exposed Frankenstein C18 development material.",
            "The output-stage manuscript stream uses only fMS readings in native document order.",
            "The lexical scanner is independent of Module B's recursive full-XML traversal implementation.",
            "Exact full-stream retention does not imply local UI/API/chunk exposure.",
            "R2, not this experiment, is the authority for exact current collation-task replay.",
            "No human discovery, literary interpretation, arbitrary future-task sufficiency, or independent transfer is established.",
        ],
    }

    out = args.out / "results.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("MODULE_C_FV_NATIVE_PIPELINE_CONTINUATION_RETENTION_V1")
    for rec in stage_records:
        comp = comparisons[rec["name"]]
        print(
            "STAGE,"
            + rec["name"]
            + f",scope_count={len(rec['scan']['scopes'])}"
            + f",scan_errors={len(rec['scan']['errors'])}"
            + (
                ""
                if not comp.get("supported")
                else f",branch_exact={comp['branch_family_decisions_exact']}/336"
                + f",positive_retained={comp['positive_branch_instances_exactly_retained']}/9"
                + f",current_exact={comp['current_answer_exact']}/112"
            )
        )
    print(
        "FIRST_LOSS_DISTRIBUTION="
        + json.dumps(result["first_loss_distribution"], sort_keys=True)
    )
    print("RESULT_SHA256=" + sha256(out.read_bytes()))


if __name__ == "__main__":
    main()
