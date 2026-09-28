"""Oxford MMOL Add_A parent-continuation development experiment v2.

Repairs evaluator semantics before Auct_B transfer opening.
Development only.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import Counter, defaultdict
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
    ("collections/Add_A/MS_Add_A_117.xml", "1250c65e854c7c2e0e89fc74a3c5a93acd1a7cfa"),
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

TEI = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def raw_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{PIN}/{path}"


def fetch(path: str) -> bytes:
    req = urllib.request.Request(
        raw_url(path),
        headers={"User-Agent": "CRR-Oxford-MMOL-dev-v2/1.0"},
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


def norm_num(x: str | None) -> str:
    s = norm(x)
    if not s:
        return ""
    try:
        f = float(s)
    except ValueError:
        return s
    if math.isfinite(f) and int(f) == f:
        return str(int(f))
    return s


def direct_locus_fields(item):
    loci = item.xpath("./tei:locus", namespaces=NS)
    locus_texts = [norm("".join(x.itertext())) for x in loci if norm("".join(x.itertext()))]
    return {
        "locus": norm(" ".join(locus_texts)),
        "from": norm(" ".join(x.get("from", "") for x in loci if x.get("from"))),
        "to": norm(" ".join(x.get("to", "") for x in loci if x.get("to"))),
    }


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
    elem_to_source_ord = {item: i for i, item in enumerate(items, 1)}
    records = []
    for source_ordinal, item in enumerate(items, 1):
        preceding_count = int(item.xpath(
            "count(preceding::tei:msItem)",
            namespaces=NS,
        ))
        upstream_uid = f"{msid}_item_{preceding_count + 1}"

        parent = item.getparent()
        while parent is not None and E.QName(parent).localname != "msItem":
            parent = parent.getparent()
        parent_source_ordinal = (
            elem_to_source_ord.get(parent)
            if parent is not None
            else None
        )

        depth = 1 + len(item.xpath("ancestor::tei:msItem", namespaces=NS))
        direct_titles = item.xpath("./tei:title", namespaces=NS)
        title = norm("; ".join(
            norm("".join(t.itertext())) for t in direct_titles
        ))
        locus = direct_locus_fields(item)
        records.append({
            "source_ordinal": source_ordinal,
            "source_identity": f"{root_id}::source-msItem-{source_ordinal}",
            "upstream_uid": upstream_uid,
            "item_id": item.get(XML_ID) or "",
            "item_n": norm_num(item.get("n")),
            "title": title,
            "locus": locus["locus"],
            "locus_from": locus["from"],
            "locus_to": locus["to"],
            "depth": depth,
            "parent_source_ordinal": parent_source_ordinal,
            "parent_source_identity": (
                f"{root_id}::source-msItem-{parent_source_ordinal}"
                if parent_source_ordinal is not None
                else None
            ),
        })

    return {
        "path": path,
        "blob": got,
        "bytes": len(raw),
        "sha256": sha256(raw),
        "root_xml_id": root_id,
        "msid": msid,
        "items": records,
    }


def parse_table():
    raw = fetch(TABLE_PATH)
    got = git_blob_sha1(raw)
    if got != TABLE_BLOB:
        raise RuntimeError(f"table drift: expected {TABLE_BLOB}, got {got}")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    required = {
        "metadata: item UID",
        "metadata: item ID",
        "metadata: item n",
        "metadata: file URL",
        "metadata: nest level",
        "locus: locus",
        "locus: from",
        "locus: to",
        "work: title",
    }
    if not rows:
        raise RuntimeError("empty published table")
    missing = sorted(required - set(rows[0]))
    if missing:
        raise RuntimeError(f"published table missing columns: {missing}")
    return raw, rows


def row_fingerprint(row):
    return (
        row.get("metadata: item UID", ""),
        norm_num(row.get("metadata: item n", "")),
        norm(row.get("work: title", "")),
        norm(row.get("locus: locus", "")),
        norm(row.get("locus: from", "")),
        norm(row.get("locus: to", "")),
    )


def source_fingerprint(item):
    return (
        item["upstream_uid"],
        item["item_n"],
        item["title"],
        item["locus"],
        item["locus_from"],
        item["locus_to"],
    )


def align_file(source, rows):
    """Return source ordinal -> published file-row index mapping.

    No parent/depth information is used.
    """
    src_items = source["items"]
    src_by_id = defaultdict(list)
    row_by_id = defaultdict(list)
    for item in src_items:
        if item["item_id"]:
            src_by_id[item["item_id"]].append(item["source_ordinal"])
    for i, row in enumerate(rows):
        iid = norm(row.get("metadata: item ID", ""))
        if iid:
            row_by_id[iid].append(i)

    mapping = {}
    method = {}

    # First use unique source-local xml:id.
    for iid, srcords in src_by_id.items():
        rowinds = row_by_id.get(iid, [])
        if len(srcords) == 1 and len(rowinds) == 1:
            mapping[srcords[0]] = rowinds[0]
            method[srcords[0]] = "ITEM_ID"

    # Fallback to a parent/depth-free current-row fingerprint.
    src_fp = defaultdict(list)
    row_fp = defaultdict(list)
    for item in src_items:
        if item["source_ordinal"] not in mapping:
            src_fp[source_fingerprint(item)].append(item["source_ordinal"])
    used_rows = set(mapping.values())
    for i, row in enumerate(rows):
        if i not in used_rows:
            row_fp[row_fingerprint(row)].append(i)

    for fp, srcords in src_fp.items():
        rowinds = row_fp.get(fp, [])
        if len(srcords) == 1 and len(rowinds) == 1:
            mapping[srcords[0]] = rowinds[0]
            method[srcords[0]] = "CURRENT_ROW_FINGERPRINT"

    return mapping, method


def parse_depth(row):
    s = norm_num(row.get("metadata: nest level", ""))
    if not s:
        return None
    try:
        d = int(s)
    except ValueError:
        return None
    return d if d >= 1 else None


def full_table_parent_rows(rows):
    """Use published row order + exported nest level only."""
    parents = {}
    problems = []
    stack = []

    for i, row in enumerate(rows):
        depth = parse_depth(row)
        if depth is None:
            parents[i] = "UNKNOWN"
            problems.append({
                "row_index_within_file": i,
                "type": "INVALID_NEST_LEVEL",
                "value": row.get("metadata: nest level", ""),
            })
            continue

        while stack and stack[-1][0] >= depth:
            stack.pop()

        if depth == 1:
            parents[i] = None
        elif stack and stack[-1][0] == depth - 1:
            parents[i] = stack[-1][1]
        else:
            parents[i] = "UNKNOWN"
            problems.append({
                "row_index_within_file": i,
                "type": "MISSING_PARENT_DEPTH_CONTEXT",
                "depth": depth,
                "stack_depths": [x[0] for x in stack],
            })

        stack.append((depth, i))

    return parents, problems


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    table_raw, all_rows = parse_table()
    by_file = defaultdict(list)
    for row in all_rows:
        by_file[row.get("metadata: file URL", "")].append(row)

    sources = [source_model(p, b) for p, b in SOURCES]

    file_reports = []
    eligible_eval = []
    interface_counts = Counter()
    total_uid_duplicates = 0
    total_nested = 0
    total_aligned = 0
    total_aligned_nested = 0
    current_depth_agree = 0
    current_depth_checked = 0

    for source in sources:
        rows = by_file.get(source["root_xml_id"], [])
        mapping, methods = align_file(source, rows)
        parents_by_row, table_problems = full_table_parent_rows(rows)
        inverse = {ri: so for so, ri in mapping.items()}

        uid_counts_source = Counter(x["upstream_uid"] for x in source["items"])
        uid_counts_rows = Counter(row.get("metadata: item UID", "") for row in rows)
        uid_duplicate_source = {
            uid: count for uid, count in uid_counts_source.items() if count > 1
        }
        uid_duplicate_rows = {
            uid: count for uid, count in uid_counts_rows.items() if count > 1
        }
        total_uid_duplicates += sum(count - 1 for count in uid_counts_rows.values() if count > 1)

        for item in source["items"]:
            if item["parent_source_ordinal"] is not None:
                total_nested += 1
            if item["source_ordinal"] not in mapping:
                if item["parent_source_ordinal"] is not None:
                    eligible_eval.append({
                        "source_identity": item["source_identity"],
                        "status": "ALIGNMENT_UNRESOLVED",
                        "reference_parent_source_identity": item["parent_source_identity"],
                    })
                    interface_counts["unsupported_alignment"] += 1
                continue

            total_aligned += 1
            row_index = mapping[item["source_ordinal"]]
            row = rows[row_index]
            depth = parse_depth(row)
            current_depth_checked += 1
            if depth == item["depth"]:
                current_depth_agree += 1

            if item["parent_source_ordinal"] is None:
                continue

            total_aligned_nested += 1
            if depth != item["depth"]:
                eligible_eval.append({
                    "source_identity": item["source_identity"],
                    "status": "NEST_LEVEL_MISMATCH",
                    "source_depth": item["depth"],
                    "table_depth": depth,
                    "reference_parent_source_identity": item["parent_source_identity"],
                    "alignment_method": methods[item["source_ordinal"]],
                })
                interface_counts["unsupported_nest_mismatch"] += 1
                continue

            # Single row: safe abstention for any nested item.
            single_pred = "UNKNOWN"

            parent_row_index = parents_by_row.get(row_index, "UNKNOWN")
            if parent_row_index == "UNKNOWN":
                file_table_pred = "UNKNOWN"
            elif parent_row_index is None:
                file_table_pred = None
            else:
                parent_source_ord_pred = inverse.get(parent_row_index)
                file_table_pred = (
                    f"{source['root_xml_id']}::source-msItem-{parent_source_ord_pred}"
                    if parent_source_ord_pred is not None
                    else "UNKNOWN"
                )

            source_linked_pred = item["parent_source_identity"]
            reference = item["parent_source_identity"]

            for name, pred in [
                ("single_row", single_pred),
                ("file_table", file_table_pred),
                ("source_linked", source_linked_pred),
            ]:
                if pred == "UNKNOWN":
                    interface_counts[f"{name}_unknown"] += 1
                elif pred == reference:
                    interface_counts[f"{name}_exact"] += 1
                else:
                    interface_counts[f"{name}_wrong"] += 1

            parent_row = (
                rows[parent_row_index]
                if isinstance(parent_row_index, int)
                else None
            )

            eligible_eval.append({
                "source_identity": item["source_identity"],
                "reference_parent_source_identity": reference,
                "alignment_method": methods[item["source_ordinal"]],
                "published_row_index_within_file": row_index,
                "single_row_parent": single_pred,
                "file_table_parent": file_table_pred,
                "source_linked_parent": source_linked_pred,
                "parent_exported_item_uid": (
                    parent_row.get("metadata: item UID", "")
                    if parent_row is not None else ""
                ),
                "parent_exported_item_id": (
                    parent_row.get("metadata: item ID", "")
                    if parent_row is not None else ""
                ),
                "parent_exported_title": (
                    parent_row.get("work: title", "")
                    if parent_row is not None else ""
                ),
                "selected_row_bytes": len(canon(row)),
                "file_table_row_count": len(rows),
                "file_table_canonical_bytes": sum(len(canon(x)) for x in rows),
                "source_file_bytes": source["bytes"],
            })

        file_reports.append({
            "path": source["path"],
            "file_url": source["root_xml_id"],
            "msid": source["msid"],
            "source_item_count": len(source["items"]),
            "published_row_count": len(rows),
            "aligned_source_items": len(mapping),
            "alignment_methods": dict(Counter(methods.values())),
            "source_uid_duplicates": uid_duplicate_source,
            "published_uid_duplicates": uid_duplicate_rows,
            "full_table_decoder_problem_count": len(table_problems),
            "full_table_decoder_problems": table_problems,
        })

    result = {
        "study": "OXFORD_MMOL_PARENT_CONTINUATION_ADD_A_DEVELOPMENT_V2",
        "authority": "DEVELOPMENT_ONLY_EVALUATOR_REPAIR_BEFORE_AUCT_B_OPENING",
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
        "native_item_count": sum(len(x["items"]) for x in sources),
        "native_nested_item_count": total_nested,
        "aligned_item_count": total_aligned,
        "aligned_nested_item_count": total_aligned_nested,
        "nest_level_agreement": {
            "checked": current_depth_checked,
            "exact": current_depth_agree,
        },
        "published_uid_duplicate_excess_rows": total_uid_duplicates,
        "interface_counts": dict(sorted(interface_counts.items())),
        "files": file_reports,
        "eligible_rows": eligible_eval,
        "claim_boundaries": [
            "Add_A is development only; Auct_B contents and rows remain unopened by this script.",
            "Source-row alignment never uses parent identity or nest level.",
            "FILE_TABLE uses published row order and published nest level only.",
            "Upstream item UID is reproduced with XPath preceding:: semantics and is diagnostic rather than assumed unique.",
            "UNKNOWN is not FALSE.",
            "SOURCE_LINKED receives full credit.",
            "Observed UID duplication is a carrier-quality fact in development and is not by itself a claim of unusability.",
        ],
    }

    out = outdir / "development_v2_results.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("OXFORD_MMOL_PARENT_CONTINUATION_ADD_A_DEVELOPMENT_V2")
    print(f"native_items={result['native_item_count']}")
    print(f"native_nested_items={total_nested}")
    print(f"aligned_items={total_aligned}")
    print(f"aligned_nested_items={total_aligned_nested}")
    print(f"nest_level_agreement={current_depth_agree}/{current_depth_checked}")
    print(f"published_uid_duplicate_excess_rows={total_uid_duplicates}")
    for k, v in sorted(interface_counts.items()):
        print(f"{k}={v}")
    print("RESULT_SHA256=" + sha256(out.read_bytes()))


if __name__ == "__main__":
    main()
