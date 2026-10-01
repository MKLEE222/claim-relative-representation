"""Prospective Oxford MMOL Auct_B parent-continuation transfer v1.

This script opens the three frozen Auct_B files only after
TRANSFER_PROTOCOL_AUCT_B_v1.md was committed.
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
    (
        "collections/Auct_B/MS_Auct_B_subtus_4.xml",
        "0299f8e0cfc774cb01ae4fa11b8ecee832e31c36",
    ),
    (
        "collections/Auct_B/MS_Auct_B_subtus_5.xml",
        "e9add37740d2c24885e7179bff82e52186bb26a9",
    ),
    (
        "collections/Auct_B/MS_Auct_B_subtus_6.xml",
        "827c24bc1b659ac726be2c00c167236c14d8816c",
    ),
]

TEI = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def raw_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{PIN}/{path}"


def fetch(path: str) -> bytes:
    req = urllib.request.Request(
        raw_url(path),
        headers={"User-Agent": "CRR-Oxford-MMOL-transfer-v1/1.0"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


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
    texts = [
        norm("".join(x.itertext()))
        for x in loci
        if norm("".join(x.itertext()))
    ]
    return {
        "locus": norm(" ".join(texts)),
        "from": norm(" ".join(
            x.get("from", "") for x in loci if x.get("from")
        )),
        "to": norm(" ".join(
            x.get("to", "") for x in loci if x.get("to")
        )),
    }


def source_model(path: str, expected_blob: str):
    raw = fetch(path)
    got = git_blob_sha1(raw)
    if got != expected_blob:
        raise RuntimeError(
            f"source drift {path}: expected {expected_blob}, got {got}"
        )

    root = E.fromstring(
        raw,
        E.XMLParser(
            collect_ids=False,
            resolve_entities=False,
            no_network=True,
        ),
    )
    root_id = root.get(XML_ID) or ""
    msids = root.xpath(
        ".//tei:teiHeader/tei:fileDesc/tei:publicationStmt/"
        "tei:idno[@type='msID' and not(@subtype='alt')]",
        namespaces=NS,
    )
    msid = norm("".join(msids[0].itertext())) if msids else ""
    if not root_id or not msid:
        raise RuntimeError(
            f"missing root xml:id or msID in {path}: "
            f"root_id={root_id!r} msid={msid!r}"
        )

    items = root.xpath(".//tei:msItem", namespaces=NS)
    elem_to_source_ord = {
        item: i for i, item in enumerate(items, 1)
    }

    records = []
    for source_ordinal, item in enumerate(items, 1):
        preceding_count = int(item.xpath(
            "count(preceding::tei:msItem)",
            namespaces=NS,
        ))
        upstream_uid = f"{msid}_item_{preceding_count + 1}"

        parent = item.getparent()
        while (
            parent is not None
            and E.QName(parent).localname != "msItem"
        ):
            parent = parent.getparent()
        parent_source_ordinal = (
            elem_to_source_ord.get(parent)
            if parent is not None
            else None
        )

        depth = 1 + len(item.xpath(
            "ancestor::tei:msItem",
            namespaces=NS,
        ))
        direct_titles = item.xpath(
            "./tei:title",
            namespaces=NS,
        )
        title = norm("; ".join(
            norm("".join(t.itertext()))
            for t in direct_titles
        ))
        locus = direct_locus_fields(item)

        records.append({
            "source_ordinal": source_ordinal,
            "source_identity": (
                f"{root_id}::source-msItem-{source_ordinal}"
            ),
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
        raise RuntimeError(
            f"table drift: expected {TABLE_BLOB}, got {got}"
        )
    rows = list(csv.DictReader(
        io.StringIO(raw.decode("utf-8-sig"))
    ))
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
        raise RuntimeError(
            f"published table missing columns: {missing}"
        )
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
    src_items = source["items"]
    src_by_id = defaultdict(list)
    row_by_id = defaultdict(list)

    for item in src_items:
        if item["item_id"]:
            src_by_id[item["item_id"]].append(
                item["source_ordinal"]
            )
    for i, row in enumerate(rows):
        iid = norm(row.get("metadata: item ID", ""))
        if iid:
            row_by_id[iid].append(i)

    mapping = {}
    methods = {}

    for iid, srcords in src_by_id.items():
        rowinds = row_by_id.get(iid, [])
        if len(srcords) == 1 and len(rowinds) == 1:
            mapping[srcords[0]] = rowinds[0]
            methods[srcords[0]] = "ITEM_ID"

    src_fp = defaultdict(list)
    row_fp = defaultdict(list)
    for item in src_items:
        if item["source_ordinal"] not in mapping:
            src_fp[source_fingerprint(item)].append(
                item["source_ordinal"]
            )

    used_rows = set(mapping.values())
    for i, row in enumerate(rows):
        if i not in used_rows:
            row_fp[row_fingerprint(row)].append(i)

    for fp, srcords in src_fp.items():
        rowinds = row_fp.get(fp, [])
        if len(srcords) == 1 and len(rowinds) == 1:
            mapping[srcords[0]] = rowinds[0]
            methods[srcords[0]] = (
                "CURRENT_ROW_FINGERPRINT"
            )

    return mapping, methods


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
                "value": row.get(
                    "metadata: nest level",
                    "",
                ),
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
                "stack_depths": [
                    x[0] for x in stack
                ],
            })

        stack.append((depth, i))

    return parents, problems


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    table_raw, all_rows = parse_table()
    by_file = defaultdict(list)
    for row in all_rows:
        by_file[
            row.get("metadata: file URL", "")
        ].append(row)

    sources = [
        source_model(path, blob)
        for path, blob in SOURCES
    ]

    trigger = Counter()
    interface = Counter()
    nested_records = []
    file_reports = []
    native_nested_count = 0
    aligned_nested_count = 0
    aligned_all_count = 0

    for source in sources:
        rows = by_file.get(source["root_xml_id"], [])
        mapping, methods = align_file(source, rows)
        inverse = {
            row_i: src_ord
            for src_ord, row_i in mapping.items()
        }
        parents_by_row, table_problems = (
            full_table_parent_rows(rows)
        )

        uid_source = Counter(
            x["upstream_uid"]
            for x in source["items"]
        )
        uid_rows = Counter(
            r.get("metadata: item UID", "")
            for r in rows
        )

        for item in source["items"]:
            native_nested = (
                item["parent_source_ordinal"]
                is not None
            )
            native_nested_count += int(native_nested)

            src_ord = item["source_ordinal"]
            if src_ord not in mapping:
                if native_nested:
                    nested_records.append({
                        "source_identity": (
                            item["source_identity"]
                        ),
                        "reference_parent_source_identity": (
                            item["parent_source_identity"]
                        ),
                        "status": (
                            "CHILD_ALIGNMENT_UNRESOLVED"
                        ),
                    })
                    interface[
                        "nested_child_alignment_unresolved"
                    ] += 1
                continue

            aligned_all_count += 1
            row_i = mapping[src_ord]
            row = rows[row_i]
            depth = parse_depth(row)
            row_trigger = (
                None if depth is None else depth > 1
            )

            if row_trigger is None:
                trigger["invalid_nest_level"] += 1
            elif native_nested and row_trigger:
                trigger["true_positive"] += 1
            elif (not native_nested) and (
                not row_trigger
            ):
                trigger["true_negative"] += 1
            elif native_nested and (
                not row_trigger
            ):
                trigger["false_negative"] += 1
            else:
                trigger["false_positive"] += 1

            if not native_nested:
                continue

            aligned_nested_count += 1
            # SINGLE_ROW: trigger can be exposed, target is not.
            if row_trigger:
                interface[
                    "single_row_trigger_positive_parent_unresolved"
                ] += 1
            else:
                interface[
                    "single_row_no_valid_parent_trigger"
                ] += 1

            # FILE_TABLE prediction.
            parent_row_i = parents_by_row.get(
                row_i,
                "UNKNOWN",
            )
            if parent_row_i == "UNKNOWN":
                table_pred = "UNKNOWN"
            elif parent_row_i is None:
                table_pred = None
            else:
                pred_source_ord = inverse.get(
                    parent_row_i
                )
                table_pred = (
                    f"{source['root_xml_id']}"
                    f"::source-msItem-{pred_source_ord}"
                    if pred_source_ord is not None
                    else "UNKNOWN"
                )

            reference = item[
                "parent_source_identity"
            ]
            if table_pred == "UNKNOWN":
                interface["file_table_unknown"] += 1
            elif table_pred == reference:
                interface["file_table_exact"] += 1
            else:
                interface["file_table_wrong"] += 1

            # SOURCE_LINKED: child alignment is already unique;
            # reopening source returns direct parent.
            source_linked_pred = reference
            if source_linked_pred == reference:
                interface[
                    "source_linked_exact"
                ] += 1
            else:
                interface[
                    "source_linked_wrong"
                ] += 1

            parent_row = (
                rows[parent_row_i]
                if isinstance(parent_row_i, int)
                else None
            )

            nested_records.append({
                "source_identity": (
                    item["source_identity"]
                ),
                "reference_parent_source_identity": (
                    reference
                ),
                "alignment_method": methods[src_ord],
                "published_row_index_within_file": (
                    row_i
                ),
                "native_depth": item["depth"],
                "published_depth": depth,
                "row_trigger": row_trigger,
                "file_table_parent": table_pred,
                "source_linked_parent": (
                    source_linked_pred
                ),
                "parent_exported_item_uid": (
                    parent_row.get(
                        "metadata: item UID",
                        "",
                    )
                    if parent_row is not None
                    else ""
                ),
                "parent_exported_item_id": (
                    parent_row.get(
                        "metadata: item ID",
                        "",
                    )
                    if parent_row is not None
                    else ""
                ),
                "parent_exported_title": (
                    parent_row.get(
                        "work: title",
                        "",
                    )
                    if parent_row is not None
                    else ""
                ),
                "selected_row_bytes": len(canon(row)),
                "file_table_row_count": len(rows),
                "file_table_canonical_bytes": sum(
                    len(canon(x)) for x in rows
                ),
                "source_file_bytes": source["bytes"],
            })

        file_reports.append({
            "path": source["path"],
            "blob": source["blob"],
            "source_sha256": source["sha256"],
            "source_bytes": source["bytes"],
            "file_url": source["root_xml_id"],
            "msid": source["msid"],
            "source_item_count": len(source["items"]),
            "source_nested_item_count": sum(
                x["parent_source_ordinal"] is not None
                for x in source["items"]
            ),
            "published_row_count": len(rows),
            "aligned_source_items": len(mapping),
            "alignment_methods": dict(
                sorted(Counter(
                    methods.values()
                ).items())
            ),
            "source_uid_duplicate_classes": {
                k: v
                for k, v in uid_source.items()
                if v > 1
            },
            "published_uid_duplicate_classes": {
                k: v
                for k, v in uid_rows.items()
                if v > 1
            },
            "full_table_decoder_problem_count": (
                len(table_problems)
            ),
            "full_table_decoder_problems": (
                table_problems
            ),
        })

    if native_nested_count == 0:
        disposition = (
            "TRANSFER_SUPPORT_STOP_ZERO_ELIGIBLE_NESTED_ITEMS"
        )
    elif (
        trigger["false_positive"] > 0
        or trigger["false_negative"] > 0
        or interface["file_table_wrong"] > 0
    ):
        disposition = (
            "TRANSFER_GLOBAL_REPRESENTATION_FAILURE"
        )
    elif interface["source_linked_wrong"] > 0:
        disposition = "TRANSFER_SOURCE_LINK_FAILURE"
    elif (
        interface["file_table_exact"] > 0
        and interface["file_table_unknown"] == 0
        and interface[
            "single_row_trigger_positive_parent_unresolved"
        ] == aligned_nested_count
        and interface["source_linked_exact"]
        == aligned_nested_count
    ):
        disposition = (
            "TRANSFER_GLOBAL_PRESERVATION_LOCAL_EXPOSURE_SEPARATION"
        )
    elif (
        interface["file_table_exact"] > 0
        and interface["file_table_unknown"] > 0
        and interface["file_table_wrong"] == 0
        and interface["source_linked_exact"]
        > interface["file_table_exact"]
    ):
        disposition = (
            "TRANSFER_PARTIAL_GLOBAL_PRESERVATION"
        )
    else:
        disposition = "TRANSFER_SUPPORT_LIMITED"

    result = {
        "study": (
            "OXFORD_MMOL_AUCT_B_PARENT_CONTINUATION_TRANSFER_V1"
        ),
        "authority": (
            "PROSPECTIVE_TRANSFER_AFTER_PROTOCOL_FREEZE"
        ),
        "external_repo": REPO,
        "commit": PIN,
        "published_contents_table": {
            "path": TABLE_PATH,
            "blob": TABLE_BLOB,
            "bytes": len(table_raw),
            "sha256": sha256(table_raw),
            "row_count": len(all_rows),
        },
        "frozen_source_file_count": len(sources),
        "native_item_count": sum(
            len(s["items"]) for s in sources
        ),
        "native_nested_item_count": native_nested_count,
        "aligned_item_count": aligned_all_count,
        "aligned_nested_item_count": aligned_nested_count,
        "trigger_counts": dict(sorted(
            trigger.items()
        )),
        "interface_counts": dict(sorted(
            interface.items()
        )),
        "files": file_reports,
        "nested_items": nested_records,
        "disposition": disposition,
        "claim_boundaries": [
            "All three frozen Auct_B files remain in the denominator.",
            "Alignment never uses parent identity or native nesting depth.",
            "SINGLE_ROW can expose a parent-context need through nest level but is not allowed an oracle parent lookup.",
            "FILE_TABLE uses published row order plus published nest level only.",
            "SOURCE_LINKED receives full credit as ordinary source reopening.",
            "UNKNOWN is not FALSE or WRONG.",
            "No LLM, literary interpretation, replacement collection, or post-outcome column was used.",
            "The transfer concerns a bounded parent-continuation relation, not arbitrary future scholarly discovery.",
        ],
    }

    out = outdir / "transfer_results.json"
    out.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "OXFORD_MMOL_AUCT_B_PARENT_CONTINUATION_TRANSFER_V1"
    )
    print(f"native_items={result['native_item_count']}")
    print(
        f"native_nested_items={native_nested_count}"
    )
    print(f"aligned_items={aligned_all_count}")
    print(
        f"aligned_nested_items={aligned_nested_count}"
    )
    for k, v in sorted(trigger.items()):
        print(f"trigger_{k}={v}")
    for k, v in sorted(interface.items()):
        print(f"{k}={v}")
    print(f"TRANSFER_DISPOSITION={disposition}")
    print(
        "RESULT_SHA256="
        + sha256(out.read_bytes())
    )


if __name__ == "__main__":
    main()
