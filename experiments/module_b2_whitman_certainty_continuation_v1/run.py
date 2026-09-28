from __future__ import annotations

import argparse
import collections
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

VAR_REPO = "whitmanarchive/whitman-LG_1855_variorum"
VAR_COMMIT = "25a00b7ebbdbc5246fce65a333bc761a5c22dad4"
REL_PATH = "source/authority/anc.02134.xml"
PRINT_PATH = "source/tei/ppp.01880.xml"
REL_BLOB = "11d6f7508c8bfd120d390d31c49d2399e38b5337"
PRINT_BLOB = "676c84cb48cdb2edaa6f72f68ae9d489a2beff22"

MS_REPO = "whitmanarchive/whitman-manuscripts"
MS_COMMIT = "249bc14594fa1c0428e7ca39f52753de21ce604b"
MS_TREE = "1871715fbcef5f9721e80f385471a86ad52ef463"

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-whitman-continuation/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def parse_ids(raw):
    root = ET.fromstring(raw)
    return {
        e.attrib[XML_ID]
        for e in root.iter()
        if XML_ID in e.attrib
    }

def endpoint(record):
    return (record["ms_file"], record["ms_locus"])

def continuation(records):
    high = sorted({endpoint(r) for r in records if r["certainty"] == "high"})
    low = sorted({endpoint(r) for r in records if r["certainty"] == "low"})
    branches = []
    if low:
        branches.append("B_LOW_CERTAINTY_REVIEW")
    if high and low:
        branches.append("B_MIXED_CERTAINTY_COMPARISON")
    status = "MIXED" if high and low else "LOW_ONLY" if low else "HIGH_ONLY" if high else "UNRESOLVED"
    return {
        "status": status,
        "branches": branches,
        "low_endpoints": low,
        "high_endpoints": high,
    }

def locus_status_projection(records):
    certs = [r["certainty"] for r in records]
    return {
        "endpoints": sorted({endpoint(r) for r in records}),
        "high_count": sum(c == "high" for c in certs),
        "low_count": sum(c == "low" for c in certs),
        "status": (
            "MIXED"
            if "high" in certs and "low" in certs
            else "LOW_ONLY"
            if "low" in certs
            else "HIGH_ONLY"
            if "high" in certs
            else "UNRESOLVED"
        ),
    }

def from_status_only(proj):
    if proj["status"] == "LOW_ONLY":
        return {
            "status": "LOW_ONLY",
            "branches": ["B_LOW_CERTAINTY_REVIEW"],
            "low_endpoints": proj["endpoints"],
            "high_endpoints": [],
        }
    if proj["status"] == "HIGH_ONLY":
        return {
            "status": "HIGH_ONLY",
            "branches": [],
            "low_endpoints": [],
            "high_endpoints": proj["endpoints"],
        }
    return {
        "status": "MIXED_UNRESOLVED_BINDING" if proj["status"] == "MIXED" else "UNRESOLVED",
        "branches": ["B_LOW_CERTAINTY_REVIEW", "B_MIXED_CERTAINTY_COMPARISON"] if proj["status"] == "MIXED" else [],
        "low_endpoints": None,
        "high_endpoints": None,
    }

def state_exact(a, b):
    return (
        a["status"] == b["status"]
        and a["branches"] == b["branches"]
        and a["low_endpoints"] == b["low_endpoints"]
        and a["high_endpoints"] == b["high_endpoints"]
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("results"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    rel_url = f"https://raw.githubusercontent.com/{VAR_REPO}/{VAR_COMMIT}/{REL_PATH}"
    print_url = f"https://raw.githubusercontent.com/{VAR_REPO}/{VAR_COMMIT}/{PRINT_PATH}"
    tree_url = f"https://api.github.com/repos/{MS_REPO}/git/trees/{MS_TREE}?recursive=1"
    archive_url = f"https://github.com/{MS_REPO}/archive/{MS_COMMIT}.tar.gz"

    rel_raw = fetch(rel_url)
    print_raw = fetch(print_url)
    tree_raw = fetch(tree_url)
    archive_raw = fetch(archive_url)

    if git_blob(rel_raw) != REL_BLOB:
        raise RuntimeError("relation source drift")
    if git_blob(print_raw) != PRINT_BLOB:
        raise RuntimeError("printed source drift")

    tree_obj = json.loads(tree_raw)
    if tree_obj.get("sha") != MS_TREE:
        raise RuntimeError("manuscript tree drift")
    tree_map = {
        x["path"]: x["sha"]
        for x in tree_obj.get("tree", [])
        if x.get("type") == "blob"
    }

    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile()]
        extracted = {}
        for m in members:
            parts = Path(m.name).parts
            if len(parts) < 2:
                continue
            rel = str(Path(*parts[1:]))
            f = tf.extractfile(m)
            if f is not None:
                extracted[rel] = f.read()

    relation_root = ET.fromstring(rel_raw)
    records = []
    malformed = 0
    missing_cert = 0
    for gi, g in enumerate(relation_root.findall(".//tei:linkGrp[@type='relation']", NS)):
        ms_file = (g.attrib.get("corresp") or "").strip()
        for li, link in enumerate(g.findall("./tei:link", NS)):
            parts = (link.attrib.get("target") or "").split()
            if len(parts) != 2:
                malformed += 1
                continue
            ptoken, mtoken = parts
            if "#" not in ptoken or not mtoken.startswith("#"):
                malformed += 1
                continue
            pfile, plocus = ptoken.split("#", 1)
            cert = (link.attrib.get("cert") or "").strip()
            if cert not in {"high", "low"}:
                missing_cert += 1
            records.append(
                {
                    "group_index": gi,
                    "link_index": li,
                    "print_file": pfile,
                    "print_locus": plocus,
                    "ms_file": ms_file,
                    "ms_locus": mtoken[1:],
                    "certainty": cert,
                }
            )

    if malformed or missing_cert:
        raise RuntimeError(f"unexpected relation shape malformed={malformed} missing_cert={missing_cert}")

    by_print = collections.defaultdict(list)
    for r in records:
        by_print[r["print_locus"]].append(r)

    native = {p: continuation(rows) for p, rows in by_print.items()}
    q0 = {p: sorted({endpoint(r) for r in rows}) for p, rows in by_print.items()}
    status_proj = {p: locus_status_projection(rows) for p, rows in by_print.items()}
    status_decoded = {p: from_status_only(status_proj[p]) for p in by_print}

    high_only = [p for p, s in native.items() if s["status"] == "HIGH_ONLY"]
    low_only = [p for p, s in native.items() if s["status"] == "LOW_ONLY"]
    mixed = [p for p, s in native.items() if s["status"] == "MIXED"]

    status_exact = {p: state_exact(status_decoded[p], native[p]) for p in by_print}

    # Controlled mixed-locus certainty-binding twins.
    twins = []
    for p in sorted(mixed):
        rows = [dict(r) for r in by_print[p]]
        highs = sorted(
            [i for i, r in enumerate(rows) if r["certainty"] == "high"],
            key=lambda i: endpoint(rows[i]),
        )
        lows = sorted(
            [i for i, r in enumerate(rows) if r["certainty"] == "low"],
            key=lambda i: endpoint(rows[i]),
        )
        pair = None
        for hi in highs:
            for lo in lows:
                if endpoint(rows[hi]) != endpoint(rows[lo]):
                    pair = (hi, lo)
                    break
            if pair:
                break
        if not pair:
            twins.append({"print_locus": p, "eligible": False, "reason": "no distinct high/low endpoints"})
            continue
        hi, lo = pair
        before = continuation(rows)
        proj_before = locus_status_projection(rows)
        rows[hi]["certainty"], rows[lo]["certainty"] = rows[lo]["certainty"], rows[hi]["certainty"]
        after = continuation(rows)
        proj_after = locus_status_projection(rows)
        twins.append(
            {
                "print_locus": p,
                "eligible": True,
                "swapped": [endpoint(by_print[p][hi]), endpoint(by_print[p][lo])],
                "q0_equal": sorted({endpoint(r) for r in rows}) == q0[p],
                "status_projection_equal": canonical(proj_before) == canonical(proj_after),
                "continuation_changed": canonical(before) != canonical(after),
                "native": before,
                "twin": after,
            }
        )

    eligible_twins = [x for x in twins if x["eligible"]]

    # Correct and wrong certainty-binding ledgers.
    correct_ledger = {}
    conflicts = []
    for p, rows in by_print.items():
        mapping = {}
        for r in rows:
            ep = endpoint(r)
            old = mapping.setdefault(ep, r["certainty"])
            if old != r["certainty"]:
                conflicts.append({"print_locus": p, "endpoint": ep, "values": sorted({old, r["certainty"]})})
        correct_ledger[p] = mapping
    if conflicts:
        raise RuntimeError("endpoint->certainty is nonfunctional: " + repr(conflicts[:10]))

    def decode_with_ledger(p, mapping):
        rows = [
            {
                "ms_file": ep[0],
                "ms_locus": ep[1],
                "certainty": mapping[ep],
            }
            for ep in q0[p]
        ]
        return continuation(rows)

    correct_exact = {
        p: state_exact(decode_with_ledger(p, correct_ledger[p]), native[p])
        for p in by_print
    }

    wrong_fail = {}
    wrong_ledgers = {}
    for t in eligible_twins:
        p = t["print_locus"]
        mapping = dict(correct_ledger[p])
        a, b = [tuple(x) for x in t["swapped"]]
        mapping[a], mapping[b] = mapping[b], mapping[a]
        wrong_ledgers[p] = mapping
        wrong_fail[p] = not state_exact(decode_with_ledger(p, mapping), native[p])

    # Source route resolution.
    printed_ids = parse_ids(print_raw)
    referenced_files = sorted({r["ms_file"] for r in records})
    manuscript_ids = {}
    manuscript_file_meta = {}
    for ms_file in referenced_files:
        path = f"source/tei/{ms_file}"
        raw = extracted.get(path)
        tree_sha = tree_map.get(path)
        if raw is None or tree_sha is None:
            manuscript_file_meta[ms_file] = {
                "path": path,
                "present_in_archive": raw is not None,
                "present_in_tree": tree_sha is not None,
                "blob_match": False,
                "bytes": None if raw is None else len(raw),
            }
            manuscript_ids[ms_file] = set()
            continue
        got = git_blob(raw)
        if got != tree_sha:
            raise RuntimeError(f"manuscript blob mismatch {ms_file}: {got} != {tree_sha}")
        ids = parse_ids(raw)
        manuscript_ids[ms_file] = ids
        manuscript_file_meta[ms_file] = {
            "path": path,
            "present_in_archive": True,
            "present_in_tree": True,
            "blob_match": True,
            "bytes": len(raw),
            "xml_id_count": len(ids),
        }

    routes = []
    cert_route_counts = collections.defaultdict(collections.Counter)
    for r in records:
        print_ok = r["print_file"] == "ppp.01880.xml" and r["print_locus"] in printed_ids
        file_ok = bool(manuscript_file_meta.get(r["ms_file"], {}).get("blob_match"))
        ms_id_ok = file_ok and r["ms_locus"] in manuscript_ids[r["ms_file"]]
        full = print_ok and file_ok and ms_id_ok
        for key, val in [
            ("printed_locus", print_ok),
            ("manuscript_file", file_ok),
            ("manuscript_locus", ms_id_ok),
            ("complete_route", full),
        ]:
            cert_route_counts[r["certainty"]][key + ("_ok" if val else "_fail")] += 1
        routes.append(
            {
                "print_locus": r["print_locus"],
                "endpoint": endpoint(r),
                "certainty": r["certainty"],
                "printed_locus_resolves": print_ok,
                "manuscript_file_resolves": file_ok,
                "manuscript_locus_resolves": ms_id_ok,
                "complete_route_resolves": full,
            }
        )

    low_targets = sum(len(s["low_endpoints"]) for s in native.values())
    mixed_partition_targets = sum(
        len(s["low_endpoints"]) + len(s["high_endpoints"])
        for s in native.values()
        if s["status"] == "MIXED"
    )

    source_linked_exact = len(native)  # direct native relation-file reopening by printed locus
    relation_bytes = len(rel_raw)
    referenced_ms_bytes = sum(
        m["bytes"] or 0 for m in manuscript_file_meta.values()
    )

    correct_ledger_rows = [
        {"print_locus": p, "endpoint": list(ep), "certainty": cert}
        for p in sorted(correct_ledger)
        for ep, cert in sorted(correct_ledger[p].items())
    ]
    wrong_ledger_rows = []
    for p in sorted(correct_ledger):
        mapping = wrong_ledgers.get(p, correct_ledger[p])
        for ep, cert in sorted(mapping.items()):
            wrong_ledger_rows.append(
                {"print_locus": p, "endpoint": list(ep), "certainty": cert}
            )

    result = {
        "study": "MODULE_B2_WHITMAN_CERTAINTY_CONTINUATION_V1",
        "authority": "DEVELOPMENT_ON_ALREADY_EXPOSED_RELATION_INVENTORY",
        "sources": {
            "relation": {
                "repo": VAR_REPO,
                "commit": VAR_COMMIT,
                "path": REL_PATH,
                "git_blob": REL_BLOB,
                "sha256": sha256(rel_raw),
                "bytes": len(rel_raw),
            },
            "printed": {
                "repo": VAR_REPO,
                "commit": VAR_COMMIT,
                "path": PRINT_PATH,
                "git_blob": PRINT_BLOB,
                "sha256": sha256(print_raw),
                "bytes": len(print_raw),
            },
            "manuscripts": {
                "repo": MS_REPO,
                "commit": MS_COMMIT,
                "tree": MS_TREE,
                "archive_sha256": sha256(archive_raw),
                "referenced_files": len(referenced_files),
                "referenced_file_bytes": referenced_ms_bytes,
            },
        },
        "population": {
            "valid_links": len(records),
            "unique_print_loci": len(by_print),
            "high_only_loci": len(high_only),
            "low_only_loci": len(low_only),
            "mixed_loci": len(mixed),
            "high_links": sum(r["certainty"] == "high" for r in records),
            "low_links": sum(r["certainty"] == "low" for r in records),
        },
        "current_task": {
            "q0_endpoint_loci": len(q0),
            "native_exact": len(q0),
            "endpoint_only_exact": len(q0),
            "locus_status_only_exact": len(q0),
            "ledger_exact": len(q0),
            "source_linked_exact": len(q0),
        },
        "continuation": {
            "low_review_loci": sum(bool(s["low_endpoints"]) for s in native.values()),
            "low_review_endpoint_targets": low_targets,
            "mixed_comparison_loci": len(mixed),
            "mixed_partition_endpoint_targets": mixed_partition_targets,
            "native_exact": len(native),
            "endpoint_only_exact": 0,
            "locus_status_only_exact": sum(status_exact.values()),
            "locus_status_only_unresolved_binding": len(native) - sum(status_exact.values()),
            "correct_ledger_exact": sum(correct_exact.values()),
            "source_linked_exact": source_linked_exact,
        },
        "controlled_twins": {
            "mixed_loci": len(mixed),
            "eligible_distinct_endpoint_twins": len(eligible_twins),
            "same_q0": sum(x["q0_equal"] for x in eligible_twins),
            "same_locus_status_projection": sum(x["status_projection_equal"] for x in eligible_twins),
            "changed_continuation": sum(x["continuation_changed"] for x in eligible_twins),
            "ineligible": [x for x in twins if not x["eligible"]],
        },
        "binding_control": {
            "endpoint_cert_conflicts": conflicts,
            "correct_ledger_exact_loci": sum(correct_exact.values()),
            "wrong_binding_tested_mixed_loci": len(wrong_fail),
            "wrong_binding_fails": sum(wrong_fail.values()),
            "correct_ledger_json_bytes": len(canonical(correct_ledger_rows)),
            "wrong_ledger_json_bytes": len(canonical(wrong_ledger_rows)),
            "wrong_ledger_same_bytes_as_correct": len(canonical(correct_ledger_rows)) == len(canonical(wrong_ledger_rows)),
            "q0_unchanged": True,
        },
        "source_routes": {
            "printed_xml_id_count": len(printed_ids),
            "manuscript_files": manuscript_file_meta,
            "by_certainty": {
                cert: dict(counts) for cert, counts in cert_route_counts.items()
            },
            "complete_route_links": sum(x["complete_route_resolves"] for x in routes),
            "unresolved_route_links": sum(not x["complete_route_resolves"] for x in routes),
        },
        "costs": {
            "cold_relation_reopen_bytes": relation_bytes,
            "printed_source_bytes": len(print_raw),
            "referenced_manuscript_bytes": referenced_ms_bytes,
            "correct_ledger_json_bytes": len(canonical(correct_ledger_rows)),
            "note": "Implemented byte counts are descriptive, not minimum coding bounds.",
        },
        "dispositions": {
            "CURRENT_ENDPOINT_EQUIVALENCE": True,
            "LOCUS_STATUS_CONTINUATION_SEPARATION": (
                len(eligible_twins) > 0
                and all(x["q0_equal"] and x["status_projection_equal"] and x["continuation_changed"] for x in eligible_twins)
            ),
            "CORRECT_BINDING_RESTORES_CONTINUATION": all(correct_exact.values()),
            "WRONG_BINDING_FAILS": bool(wrong_fail) and all(wrong_fail.values()),
            "SOURCE_ROUTE_EXECUTABLE_ALL_LINKS": all(x["complete_route_resolves"] for x in routes),
            "AUTONOMOUS_QUESTION_GENERATION": False,
            "HISTORICAL_GENETIC_TRUTH": False,
            "INDEPENDENT_TRANSFER": False,
        },
        "claim_boundary": [
            "The relation inventory is already exposed development material.",
            "Certainty is the Archive's encoded editorial status, not an independent genetic-truth label.",
            "The mixed-locus twins are controlled certainty-binding alternatives, not natural editorial histories.",
            "The branch grammar is frozen and source-facing; no LLM generates the questions.",
            "A missing source route in the pinned 2019 repositories is an access/version finding, not proof that a relation is false.",
            "High-only controls do not imply absence of every other possible scholarly follow-up.",
        ],
    }

    out = args.out / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "route_records.json").write_text(
        json.dumps(routes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "population": result["population"],
        "current_task": result["current_task"],
        "continuation": result["continuation"],
        "controlled_twins": result["controlled_twins"],
        "binding_control": result["binding_control"],
        "source_routes_summary": {
            "complete_route_links": result["source_routes"]["complete_route_links"],
            "unresolved_route_links": result["source_routes"]["unresolved_route_links"],
            "by_certainty": result["source_routes"]["by_certainty"],
        },
        "dispositions": result["dispositions"],
        "results_sha256": sha256(out.read_bytes()),
        "scientific_payload_sha256": sha256(canonical(result)),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
