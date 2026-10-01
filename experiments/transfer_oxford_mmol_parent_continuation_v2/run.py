"""Oxford MMOL structurally selected prospective transfer v2.

Selection and transfer criteria are frozen in PROTOCOL.md.
The selector inspects only native msItem nesting before the selected
collection's tabular outcomes are opened.
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
API_TREE = (
    f"https://api.github.com/repos/{REPO}/git/trees/"
    f"{PIN}?recursive=1"
)
TABLE_PATH = "tabular_data/output/collection/csv/05_contents.csv"
TABLE_BLOB = "3b67d46018404f84b9f1440e126d1a17dd6c466d"

START_AFTER = "Auct_B"
MIN_NESTED = 5
MIN_FILES_WITH_NESTED = 2

TEI = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


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


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CRR-Oxford-MMOL-transfer-v2/1.0"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def raw_url(path: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{REPO}/{PIN}/{path}"
    )


def fetch_path(path: str) -> bytes:
    return request_bytes(raw_url(path))


def fetch_tree():
    raw = request_bytes(API_TREE)
    data = json.loads(raw.decode("utf-8"))
    if data.get("truncated"):
        raise RuntimeError("GitHub recursive tree is truncated")
    return data


def collection_xml_groups(tree):
    groups = defaultdict(list)
    for rec in tree["tree"]:
        path = rec.get("path", "")
        if (
            rec.get("type") == "blob"
            and path.startswith("collections/")
            and path.endswith(".xml")
        ):
            parts = path.split("/")
            if len(parts) >= 3:
                groups[parts[1]].append({
                    "path": path,
                    "blob": rec["sha"],
                    "size": rec.get("size"),
                })
    for name in groups:
        groups[name].sort(key=lambda x: x["path"])
    return dict(groups)


def structural_scan(raw: bytes):
    root = E.fromstring(
        raw,
        E.XMLParser(
            collect_ids=False,
            resolve_entities=False,
            no_network=True,
        ),
    )
    items = root.xpath(".//tei:msItem", namespaces=NS)
    nested = 0
    for item in items:
        if item.xpath("ancestor::tei:msItem", namespaces=NS):
            nested += 1
    return {
        "msitem_count": len(items),
        "nested_msitem_count": nested,
    }


def structural_select(tree, outdir: Path):
    groups = collection_xml_groups(tree)
    candidates = sorted(
        name
        for name in groups
        if name > START_AFTER
    )
    scanned = []
    selected = None

    for name in candidates:
        files = groups[name]
        total_items = 0
        total_nested = 0
        files_with_nested = 0
        file_records = []
        decision_index = None

        for idx, meta in enumerate(files, 1):
            raw = fetch_path(meta["path"])
            got = git_blob_sha1(raw)
            if got != meta["blob"]:
                raise RuntimeError(
                    f"tree/blob drift {meta['path']}: "
                    f"{meta['blob']} vs {got}"
                )
            s = structural_scan(raw)
            total_items += s["msitem_count"]
            total_nested += s["nested_msitem_count"]
            if s["nested_msitem_count"] > 0:
                files_with_nested += 1

            file_records.append({
                "path": meta["path"],
                "blob": meta["blob"],
                "size": meta["size"],
                "msitem_count": s["msitem_count"],
                "nested_msitem_count": s["nested_msitem_count"],
            })

            if (
                total_nested >= MIN_NESTED
                and files_with_nested >= MIN_FILES_WITH_NESTED
            ):
                decision_index = idx
                selected = name
                break

        scanned.append({
            "collection": name,
            "xml_file_count": len(files),
            "files_scanned_until_decision": len(file_records),
            "total_msitems_scanned": total_items,
            "nested_msitems_scanned": total_nested,
            "files_with_nested_scanned": files_with_nested,
            "eligible_at_scan_stop": (
                selected == name
            ),
            "structural_scan_files": file_records,
        })

        if selected:
            break

    manifest = {
        "study": "OXFORD_MMOL_STRUCTURAL_TRANSFER_SELECTION_V2",
        "authority": "PRE_TABULAR_OUTCOME_STRUCTURAL_SELECTION",
        "repo": REPO,
        "commit": PIN,
        "selector": {
            "start_after": START_AFTER,
            "min_nested_msitems": MIN_NESTED,
            "min_files_with_nested": MIN_FILES_WITH_NESTED,
            "candidate_order": "LEXICOGRAPHIC_COLLECTION_DIRECTORY",
        },
        "scanned_candidates": scanned,
        "selected_collection": selected,
        "selected_collection_files": (
            groups[selected] if selected else []
        ),
        "prohibited_during_selection": [
            "05_contents.csv rows",
            "titles",
            "loci",
            "item IDs",
            "item n",
            "published nest level",
            "parent recovery outcomes",
            "UID duplication outcomes",
        ],
    }

    payload = canon(manifest)
    manifest["manifest_payload_sha256"] = sha256(payload)

    path = outdir / "selection_manifest.json"
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


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


def source_model(meta):
    raw = fetch_path(meta["path"])
    got = git_blob_sha1(raw)
    if got != meta["blob"]:
        raise RuntimeError(
            f"selected source drift {meta['path']}: "
            f"{meta['blob']} vs {got}"
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
            f"missing root xml:id or msID in {meta['path']}"
        )

    items = root.xpath(".//tei:msItem", namespaces=NS)
    elem_to_ord = {
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
        parent_ord = (
            elem_to_ord.get(parent)
            if parent is not None
            else None
        )

        depth = 1 + len(item.xpath(
            "ancestor::tei:msItem",
            namespaces=NS,
        ))
        direct_titles = item.xpath("./tei:title", namespaces=NS)
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
            "parent_source_ordinal": parent_ord,
            "parent_source_identity": (
                f"{root_id}::source-msItem-{parent_ord}"
                if parent_ord is not None
                else None
            ),
        })

    return {
        "path": meta["path"],
        "blob": got,
        "bytes": len(raw),
        "sha256": sha256(raw),
        "root_xml_id": root_id,
        "msid": msid,
        "items": records,
    }


def parse_table():
    raw = fetch_path(TABLE_PATH)
    got = git_blob_sha1(raw)
    if got != TABLE_BLOB:
        raise RuntimeError(
            f"table drift: {TABLE_BLOB} vs {got}"
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
            methods[srcords[0]] = "CURRENT_ROW_FINGERPRINT"

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


def transfer(manifest, outdir: Path):
    selected = manifest["selected_collection"]
    if not selected:
        result = {
            "study": "OXFORD_MMOL_ELIGIBILITY_SELECTED_TRANSFER_V2",
            "authority": "PROSPECTIVE_TRANSFER",
            "selection_manifest_sha256": (
                manifest["manifest_payload_sha256"]
            ),
            "disposition": "V2_SUPPORT_STOP_NO_ELIGIBLE_COLLECTION",
        }
        return result

    # Important sequencing: table access starts only after the structural
    # selection manifest has already been written to disk.
    table_raw, all_rows = parse_table()
    by_file = defaultdict(list)
    for row in all_rows:
        by_file[row.get("metadata: file URL", "")].append(row)

    sources = [
        source_model(meta)
        for meta in manifest["selected_collection_files"]
    ]

    trigger = Counter()
    interface = Counter()
    nested_records = []
    file_reports = []
    native_nested = 0
    aligned_items = 0
    aligned_nested = 0

    for source in sources:
        rows = by_file.get(source["root_xml_id"], [])
        mapping, methods = align_file(source, rows)
        inverse = {ri: so for so, ri in mapping.items()}
        table_parents, table_problems = full_table_parent_rows(rows)

        uid_source = Counter(
            item["upstream_uid"] for item in source["items"]
        )
        uid_rows = Counter(
            row.get("metadata: item UID", "") for row in rows
        )

        for item in source["items"]:
            has_parent = item["parent_source_ordinal"] is not None
            native_nested += int(has_parent)
            src_ord = item["source_ordinal"]

            if src_ord not in mapping:
                if has_parent:
                    interface["nested_child_alignment_unresolved"] += 1
                    nested_records.append({
                        "source_identity": item["source_identity"],
                        "reference_parent_source_identity": item["parent_source_identity"],
                        "status": "CHILD_ALIGNMENT_UNRESOLVED",
                    })
                continue

            aligned_items += 1
            row_i = mapping[src_ord]
            row = rows[row_i]
            depth = parse_depth(row)
            row_trigger = None if depth is None else depth > 1

            if row_trigger is None:
                trigger["invalid_nest_level"] += 1
            elif has_parent and row_trigger:
                trigger["true_positive"] += 1
            elif (not has_parent) and (not row_trigger):
                trigger["true_negative"] += 1
            elif has_parent and (not row_trigger):
                trigger["false_negative"] += 1
            else:
                trigger["false_positive"] += 1

            if not has_parent:
                continue

            aligned_nested += 1
            if row_trigger:
                interface[
                    "single_row_trigger_positive_parent_unresolved"
                ] += 1
            else:
                interface[
                    "single_row_no_valid_parent_trigger"
                ] += 1

            parent_row_i = table_parents.get(row_i, "UNKNOWN")
            if parent_row_i == "UNKNOWN":
                table_pred = "UNKNOWN"
            elif parent_row_i is None:
                table_pred = None
            else:
                pred_src_ord = inverse.get(parent_row_i)
                table_pred = (
                    f"{source['root_xml_id']}::source-msItem-{pred_src_ord}"
                    if pred_src_ord is not None
                    else "UNKNOWN"
                )

            reference = item["parent_source_identity"]
            if table_pred == "UNKNOWN":
                interface["file_table_unknown"] += 1
            elif table_pred == reference:
                interface["file_table_exact"] += 1
            else:
                interface["file_table_wrong"] += 1

            source_pred = reference
            if source_pred == reference:
                interface["source_linked_exact"] += 1
            else:
                interface["source_linked_wrong"] += 1

            nested_records.append({
                "source_identity": item["source_identity"],
                "reference_parent_source_identity": reference,
                "alignment_method": methods[src_ord],
                "published_row_index_within_file": row_i,
                "native_depth": item["depth"],
                "published_depth": depth,
                "row_trigger": row_trigger,
                "file_table_parent": table_pred,
                "source_linked_parent": source_pred,
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
            "alignment_methods": dict(sorted(
                Counter(methods.values()).items()
            )),
            "source_uid_duplicate_classes": {
                k: v for k, v in uid_source.items() if v > 1
            },
            "published_uid_duplicate_classes": {
                k: v for k, v in uid_rows.items() if v > 1
            },
            "full_table_decoder_problem_count": len(table_problems),
            "full_table_decoder_problems": table_problems,
        })

    if native_nested < MIN_NESTED:
        raise RuntimeError(
            "selected collection violated frozen structural threshold"
        )

    if (
        trigger["false_positive"] > 0
        or trigger["false_negative"] > 0
        or interface["file_table_wrong"] > 0
    ):
        disposition = "V2_TRANSFER_GLOBAL_REPRESENTATION_FAILURE"
    elif interface["source_linked_wrong"] > 0:
        disposition = "V2_TRANSFER_SOURCE_LINK_FAILURE"
    elif (
        interface["file_table_exact"] > 0
        and interface["file_table_unknown"] == 0
        and interface["file_table_wrong"] == 0
        and interface["source_linked_exact"] == aligned_nested
        and interface[
            "single_row_trigger_positive_parent_unresolved"
        ] == aligned_nested
    ):
        disposition = (
            "V2_TRANSFER_GLOBAL_PRESERVATION_LOCAL_EXPOSURE_SEPARATION"
        )
    elif (
        interface["file_table_exact"] > 0
        and interface["file_table_unknown"] > 0
        and interface["file_table_wrong"] == 0
        and interface["source_linked_exact"]
        > interface["file_table_exact"]
        and interface["source_linked_wrong"] == 0
    ):
        disposition = "V2_TRANSFER_PARTIAL_GLOBAL_PRESERVATION"
    else:
        disposition = "V2_TRANSFER_SUPPORT_LIMITED"

    return {
        "study": "OXFORD_MMOL_ELIGIBILITY_SELECTED_TRANSFER_V2",
        "authority": "PROSPECTIVE_TRANSFER_AFTER_STRUCTURAL_SELECTION",
        "external_repo": REPO,
        "commit": PIN,
        "selection_manifest_sha256": (
            manifest["manifest_payload_sha256"]
        ),
        "selected_collection": selected,
        "selected_source_file_count": len(sources),
        "published_contents_table": {
            "path": TABLE_PATH,
            "blob": TABLE_BLOB,
            "bytes": len(table_raw),
            "sha256": sha256(table_raw),
            "row_count": len(all_rows),
        },
        "native_item_count": sum(
            len(s["items"]) for s in sources
        ),
        "native_nested_item_count": native_nested,
        "aligned_item_count": aligned_items,
        "aligned_nested_item_count": aligned_nested,
        "trigger_counts": dict(sorted(trigger.items())),
        "interface_counts": dict(sorted(interface.items())),
        "files": file_reports,
        "nested_items": nested_records,
        "disposition": disposition,
        "claim_boundaries": [
            "Collection selection inspected source structure only before tabular outcomes.",
            "All XML files in the selected collection remain in the denominator.",
            "Alignment never uses parent identity or native nesting depth.",
            "FILE_TABLE uses published row order plus exported nest level only.",
            "SOURCE_LINKED receives full credit.",
            "UNKNOWN is not FALSE or WRONG.",
            "Nominal UID duplication is diagnostic and never used as a source-order oracle.",
            "No LLM or post-outcome decoder tuning is used.",
        ],
    }


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    tree = fetch_tree()
    manifest = structural_select(tree, outdir)

    # Verify the manifest exists before any transfer/table access.
    manifest_path = outdir / "selection_manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("selection manifest was not persisted")

    result = transfer(manifest, outdir)
    out = outdir / "transfer_v2_results.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("OXFORD_MMOL_ELIGIBILITY_SELECTED_TRANSFER_V2")
    print(
        "selected_collection="
        + str(manifest["selected_collection"])
    )
    for rec in manifest["scanned_candidates"]:
        print(
            "SELECTOR,"
            + rec["collection"]
            + f",files_scanned={rec['files_scanned_until_decision']}"
            + f",nested={rec['nested_msitems_scanned']}"
            + f",files_with_nested={rec['files_with_nested_scanned']}"
            + f",eligible={int(rec['eligible_at_scan_stop'])}"
        )
    print("selection_manifest_sha256=" + manifest["manifest_payload_sha256"])
    print("TRANSFER_DISPOSITION=" + result["disposition"])
    if "native_nested_item_count" in result:
        print(f"native_nested_items={result['native_nested_item_count']}")
        print(f"aligned_nested_items={result['aligned_nested_item_count']}")
        for k, v in sorted(result["trigger_counts"].items()):
            print(f"trigger_{k}={v}")
        for k, v in sorted(result["interface_counts"].items()):
            print(f"{k}={v}")
    print("RESULT_SHA256=" + sha256(out.read_bytes()))


if __name__ == "__main__":
    main()
