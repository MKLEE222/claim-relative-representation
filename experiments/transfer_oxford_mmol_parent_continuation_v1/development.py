"""Oxford MMOL Add_A parent-continuation development experiment.

Development only. Auct_B transfer content is not accessed by this script.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

from lxml import etree as E

REPO = "Digital-Scholarship-Oxford/enabling-digital-research"
PIN = "7763fe63b51fd20ddb29a546e8af960641785ed1"
TABLE_PATH = "tabular_data/output/collection/csv/05_contents.csv"
TABLE_BLOB = "3b67d46018404f84b9f1440e126d1a17dd6c466d"

SOURCES = [
    ("collections/Add_A/MS_Add_A_10.xml", "6a13086de93e5a41e58ee98132ed0724b609482b"),
    ("collections/Add_A/MS_Add_A_100.xml", "6b068eadfd12aacc6cce5bb95b21ee4a3bb06ae4"),
    ("collections/Add_A/MS_Add_A_103.xml", "7b6950faab59748c6c2315911d8e912b1577f587"),
    ("collections/Add_A/MS_Add_A_105.xml", "0fdc0154d94b84ec478e3e317592c71b495e5b21"),
    ("collections/Add_A/MS_Add_A_106.xml", "7f3a082baee230e10fd7ed81ad8b3f71f73a9ddf"),
    ("collections/Add_A/MS_Add_A_107.xml", "1fe849c21565d150bfb83002b5efb7d27cf31754"),
    ("collections/Add_A/MS_Add_A_108.xml", "8c023e7ee34870c35f5871dcf7acdfab13d28221"),
    ("collections/Add_A/MS_Add_A_109.xml", "769febef26dcff837399f9d9e60d041c4a92893f"),
    ("collections/Add_A/MS_Add_A_11.xml", "5bbceb6015bcd8f7be6ceccc28ee51d3ed45a2ad"),
    ("collections/Add_A/MS_Add_A_113.xml", "517fdc95c2ce5558ad5c25efde3a7d1b968f2d18"),
    ("collections/Add_A/MS_Add_A_117.xml", "1250c65e8546c2e0e89fc74a3c5a93acd1a7cfa"),
    ("collections/Add_A/MS_Add_A_118.xml", "c2e488947063b3d2951b09d77f9626b4bf7a404c"),
    ("collections/Add_A/MS_Add_A_12.xml", "246c390605f8f69b340e1accaa264ccd39970c26"),
    ("collections/Add_A/MS_Add_A_13.xml", "91d2dbbf9df46ac33e72cfb388355e0722a6c8c0"),
    ("collections/Add_A/MS_Add_A_135.xml", "d55428b4e33ae623db92bf2c9bd43aa04f56d75b"),
    ("collections/Add_A/MS_Add_A_15.xml", "b979ed15cabdb962e05bdc70c4b3acdbfc63f66a"),
    ("collections/Add_A/MS_Add_A_163.xml", "e690ef084aeda155d3e13e063c4dcbd230abc646"),
    ("collections/Add_A/MS_Add_A_164.xml", "418bc0fd57971ddc60cc300a9541e459ff685be3"),
    ("collections/Add_A/MS_Add_A_165.xml", "6956134f2c5f3cb55b4c18f88b23abd984a373ab"),
    ("collections/Add_A/MS_Add_A_166.xml", "f978ab8fae460b9e768c3627da1e3b7c6db5b80d"),
]

# Correct one typo-safe expected blob from the pinned tree.
SOURCES[10] = (
    "collections/Add_A/MS_Add_A_117.xml",
    "1250c65e854c7c2e0e89fc74a3c5a93acd1a7cfa",
)

TEI = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def raw_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{PIN}/{path}"


def fetch(path: str) -> bytes:
    req = urllib.request.Request(
        raw_url(path),
        headers={"User-Agent": "CRR-Oxford-MMOL-dev/1.0"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(x) -> bytes:
    return json.dumps(
        x,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def norm(x: str | None) -> str:
    return " ".join((x or "").split())


def source_model(path: str, expected_blob: str):
    raw = fetch(path)
    got = git_blob_sha1(raw)
    if got != expected_blob:
        raise RuntimeError(f"source drift {path}: expected {expected_blob}, got {got}")
    root = E.fromstring(
        raw,
        E.XMLParser(collect_ids=False, resolve_entities=False, no_network=True),
    )
    root_id = root.get(XML_ID) or ""

    msids = root.xpath(
        ".//tei:teiHeader/tei:fileDesc/tei:publicationStmt/"
        "tei:idno[@type='msID' and not(@subtype='alt')]",
        namespaces=NS,
    )
    msid = norm("".join(msids[0].itertext())) if msids else ""
    if not msid:
        raise RuntimeError(f"no msID in {path}")

    items = root.xpath(".//tei:msItem", namespaces=NS)
    elem_to_uid = {}
    item_records = []
    for ordinal, item in enumerate(items, 1):
        uid = f"{msid}_item_{ordinal}"
        elem_to_uid[item] = uid

    for ordinal, item in enumerate(items, 1):
        uid = elem_to_uid[item]
        parent = item.getparent()
        while parent is not None and E.QName(parent).localname != "msItem":
            parent = parent.getparent()
        parent_uid = elem_to_uid.get(parent) if parent is not None else None
        depth = 1 + len(item.xpath("ancestor::tei:msItem", namespaces=NS))
        direct_titles = item.xpath("./tei:title", namespaces=NS)
        title = norm("; ".join(norm("".join(t.itertext())) for t in direct_titles))
        item_records.append({
            "uid": uid,
            "ordinal": ordinal,
            "item_id": item.get(XML_ID) or "",
            "depth": depth,
            "parent_uid": parent_uid,
            "source_title": title,
        })

    return {
        "path": path,
        "blob": got,
        "bytes": len(raw),
        "sha256": sha256(raw),
        "root_xml_id": root_id,
        "msid": msid,
        "items": item_records,
    }


def parse_table():
    raw = fetch(TABLE_PATH)
    got = git_blob_sha1(raw)
    if got != TABLE_BLOB:
        raise RuntimeError(f"table drift: expected {TABLE_BLOB}, got {got}")
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    required = {
        "metadata: item UID",
        "metadata: file URL",
        "metadata: nest level",
        "work: title",
    }
    missing = sorted(required - set(rows[0] if rows else []))
    if missing:
        raise RuntimeError(f"published table missing columns: {missing}")
    return raw, rows


def parse_intish(x: str):
    s = (x or "").strip()
    if not s:
        return None
    try:
        f = float(s)
    except ValueError:
        return None
    if int(f) != f:
        return None
    return int(f)


UID_ORD_RE = re.compile(r"_item_(\d+)$")


def file_table_parent_map(rows):
    problems = []
    seen_ord = {}
    parsed = []
    for row in rows:
        uid = row.get("metadata: item UID", "")
        m = UID_ORD_RE.search(uid)
        ordinal = int(m.group(1)) if m else None
        depth = parse_intish(row.get("metadata: nest level", ""))
        if ordinal is None:
            problems.append({"uid": uid, "type": "MALFORMED_UID_ORDINAL"})
            continue
        if depth is None or depth < 1:
            problems.append({"uid": uid, "type": "INVALID_NEST_LEVEL"})
            continue
        if ordinal in seen_ord:
            problems.append({
                "uid": uid,
                "type": "DUPLICATE_SOURCE_ORDER_ORDINAL",
                "other_uid": seen_ord[ordinal],
            })
            continue
        seen_ord[ordinal] = uid
        parsed.append((ordinal, depth, row))

    parsed.sort(key=lambda x: x[0])
    stack = []
    parents = {}
    for ordinal, depth, row in parsed:
        uid = row["metadata: item UID"]
        if stack and depth > stack[-1][0] + 1:
            problems.append({
                "uid": uid,
                "type": "DEPTH_JUMP_GT_1",
                "previous_depth": stack[-1][0],
                "depth": depth,
            })
        while stack and stack[-1][0] >= depth:
            stack.pop()
        if depth == 1:
            parents[uid] = None
        elif stack and stack[-1][0] == depth - 1:
            parents[uid] = stack[-1][1]["metadata: item UID"]
        else:
            parents[uid] = "UNKNOWN"
            problems.append({
                "uid": uid,
                "type": "MISSING_PREDECESSOR_AT_PARENT_DEPTH",
                "depth": depth,
            })
        stack.append((depth, row))
    return parents, problems


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    table_raw, all_rows = parse_table()
    by_file_url = defaultdict(list)
    by_uid = defaultdict(list)
    for row in all_rows:
        by_file_url[row.get("metadata: file URL", "")].append(row)
        by_uid[row.get("metadata: item UID", "")].append(row)

    sources = [source_model(p, b) for p, b in SOURCES]

    selected_uids = {i["uid"] for s in sources for i in s["items"]}
    eligible = [
        (s, i)
        for s in sources
        for i in s["items"]
        if i["parent_uid"] is not None
    ]

    row_match_counts = {
        uid: len(by_uid.get(uid, []))
        for uid in sorted(selected_uids)
    }

    source_nest_agree = 0
    source_nest_checked = 0
    row_mismatches = []
    file_decoders = {}
    for s in sources:
        frows = by_file_url.get(s["root_xml_id"], [])
        parent_map, problems = file_table_parent_map(frows)
        file_decoders[s["root_xml_id"]] = {
            "parent_map": parent_map,
            "problems": problems,
            "row_count": len(frows),
            "canonical_rows_bytes": sum(len(canon(r)) for r in frows),
        }
        for item in s["items"]:
            matches = by_uid.get(item["uid"], [])
            if len(matches) != 1:
                continue
            source_nest_checked += 1
            d = parse_intish(matches[0].get("metadata: nest level", ""))
            if d == item["depth"]:
                source_nest_agree += 1
            else:
                row_mismatches.append({
                    "uid": item["uid"],
                    "source_depth": item["depth"],
                    "table_depth": matches[0].get("metadata: nest level", ""),
                })

    eval_rows = []
    counts = defaultdict(int)
    for s, item in eligible:
        matches = by_uid.get(item["uid"], [])
        if len(matches) != 1:
            eval_rows.append({
                "uid": item["uid"],
                "status": "ROW_MATCH_NOT_UNIQUE",
                "row_match_count": len(matches),
                "reference_parent_uid": item["parent_uid"],
            })
            counts["unsupported_row_match"] += 1
            continue
        row = matches[0]
        table_depth = parse_intish(row.get("metadata: nest level", ""))
        if table_depth != item["depth"]:
            eval_rows.append({
                "uid": item["uid"],
                "status": "NEST_LEVEL_MISMATCH",
                "reference_parent_uid": item["parent_uid"],
                "source_depth": item["depth"],
                "table_depth": table_depth,
            })
            counts["unsupported_nest_mismatch"] += 1
            continue

        # SINGLE_ROW safe semantics
        single = "UNKNOWN" if item["depth"] > 1 else None

        fdec = file_decoders[s["root_xml_id"]]
        full = fdec["parent_map"].get(item["uid"], "UNKNOWN")

        # SOURCE_LINKED uses the direct source parent from the independently parsed source.
        source_linked = item["parent_uid"]

        for name, value in (
            ("single_row", single),
            ("file_table", full),
            ("source_linked", source_linked),
        ):
            if value == "UNKNOWN":
                counts[f"{name}_unknown"] += 1
            elif value == item["parent_uid"]:
                counts[f"{name}_exact"] += 1
            else:
                counts[f"{name}_wrong"] += 1

        parent_matches = by_uid.get(item["parent_uid"], [])
        parent_title = (
            parent_matches[0].get("work: title", "")
            if len(parent_matches) == 1
            else ""
        )
        eval_rows.append({
            "uid": item["uid"],
            "file_url": s["root_xml_id"],
            "source_depth": item["depth"],
            "reference_parent_uid": item["parent_uid"],
            "single_row_parent": single,
            "file_table_parent": full,
            "source_linked_parent": source_linked,
            "parent_exported_title": parent_title,
            "selected_row_bytes": len(canon(row)),
            "file_table_rows": fdec["row_count"],
            "file_table_canonical_bytes": fdec["canonical_rows_bytes"],
            "source_file_bytes": s["bytes"],
        })

    result = {
        "study": "OXFORD_MMOL_PARENT_CONTINUATION_ADD_A_DEVELOPMENT_V1",
        "authority": "DEVELOPMENT_ONLY_TRANSFER_DESIGN",
        "external_repo": REPO,
        "commit": PIN,
        "published_contents_table": {
            "path": TABLE_PATH,
            "blob": TABLE_BLOB,
            "bytes": len(table_raw),
            "sha256": sha256(table_raw),
            "row_count": len(all_rows),
        },
        "selected_source_count": len(sources),
        "selected_sources": [
            {
                k: s[k]
                for k in (
                    "path",
                    "blob",
                    "bytes",
                    "sha256",
                    "root_xml_id",
                    "msid",
                )
            }
            for s in sources
        ],
        "native_item_count": sum(len(s["items"]) for s in sources),
        "eligible_nested_item_count": len(eligible),
        "row_match_distribution": dict(
            sorted(defaultdict(int, {
                str(n): list(row_match_counts.values()).count(n)
                for n in set(row_match_counts.values())
            }).items())
        ),
        "nest_level_agreement": {
            "checked": source_nest_checked,
            "exact": source_nest_agree,
            "mismatches": row_mismatches,
        },
        "interface_counts": dict(sorted(counts.items())),
        "file_table_decoder": {
            file_url: {
                "row_count": rec["row_count"],
                "canonical_rows_bytes": rec["canonical_rows_bytes"],
                "problem_count": len(rec["problems"]),
                "problems": rec["problems"],
            }
            for file_url, rec in file_decoders.items()
        },
        "eligible_rows": eval_rows,
        "claim_boundaries": [
            "Add_A is development only; Auct_B has not been opened by this script.",
            "Parenthood is native XML hierarchy, not a literary interpretation.",
            "UNKNOWN is not FALSE.",
            "FILE_TABLE uses only upstream published item UID and nest level plus row order reconstructed from the UID ordinal.",
            "SOURCE_LINKED receives full credit as ordinary source reopening.",
            "A local row's unique identifier is not treated as a hidden oracle mapping to its parent.",
            "Exact FILE_TABLE recovery, if observed, is a preservation result rather than a failure.",
        ],
    }

    out = outdir / "development_results.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("OXFORD_MMOL_PARENT_CONTINUATION_ADD_A_DEVELOPMENT_V1")
    print(f"published_table_rows={len(all_rows)}")
    print(f"selected_sources={len(sources)}")
    print(f"native_items={result['native_item_count']}")
    print(f"eligible_nested_items={len(eligible)}")
    print(
        "nest_level_agreement="
        f"{source_nest_agree}/{source_nest_checked}"
    )
    for k, v in sorted(counts.items()):
        print(f"{k}={v}")
    total_problem = sum(
        len(x["problems"]) for x in file_decoders.values()
    )
    print(f"file_table_decoder_problems={total_problem}")
    print("RESULT_SHA256=" + sha256(out.read_bytes()))


if __name__ == "__main__":
    main()
