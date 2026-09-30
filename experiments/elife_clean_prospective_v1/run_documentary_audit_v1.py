from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

import elife_constants as C


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def children(node, name: str):
    return [x for x in list(node) if lname(x.tag) == name]


def first_child(node, name: str):
    xs = children(node, name)
    return xs[0] if xs else None


def text(node) -> str:
    return "".join(node.itertext()).strip() if node is not None else ""


def attr(node, local: str):
    for key, value in node.attrib.items():
        if lname(key) == local:
            return value
    return None


def canonical_doi(value):
    return C.canonical_doi(value)


def find_article_meta(root):
    front = first_child(root, "front")
    return first_child(front, "article-meta") if front is not None else None


def exact_identity(path: str, meta):
    name = Path(path).name
    fm = C.FILENAME_RE.fullmatch(name)
    if not fm or meta is None:
        return {
            "pass": False,
            "filename_msid": fm.group(1) if fm else None,
            "filename_rp_version": int(fm.group(2)) if fm else None,
        }

    msid = fm.group(1)
    version = int(fm.group(2))
    publisher = []
    version_doi = []
    for node in children(meta, "article-id"):
        if attr(node, "pub-id-type") == "publisher-id":
            publisher.append(text(node))
        if (
            attr(node, "pub-id-type") == "doi"
            and attr(node, "specific-use") == "version"
        ):
            version_doi.append(canonical_doi(text(node)))

    expected = C.expected_version_doi(msid, version)
    return {
        "pass": publisher == [msid] and version_doi == [expected],
        "filename_msid": msid,
        "filename_rp_version": version,
        "publisher_ids": publisher,
        "version_dois": version_doi,
        "expected_version_doi": expected,
    }


def version_state(meta):
    raw = None
    publication_state = None
    if meta is not None:
        ava = first_child(meta, "article-version-alternatives")
        if ava is not None:
            for node in children(ava, "article-version"):
                kind = attr(node, "article-version-type")
                if kind == "preprint-version":
                    raw = text(node)
                elif kind == "publication-state":
                    publication_state = text(node)

    m = re.fullmatch(r"1\.(\d+)", raw or "")
    return {
        "preprint_version_raw": raw,
        "preprint_version": int(m.group(1)) if m else None,
        "publication_state": publication_state,
    }


def current_evaluations(root, version_doi):
    rows = {
        "assessment_dois": [],
        "review_dois": [],
        "response_dois": [],
    }
    unknown_types = []
    for sub in children(root, "sub-article"):
        typ = attr(sub, "article-type")
        front_stub = first_child(sub, "front-stub")
        doi = None
        if front_stub is not None:
            for aid in children(front_stub, "article-id"):
                if attr(aid, "pub-id-type") == "doi":
                    doi = canonical_doi(text(aid))
                    break

        if typ == "editor-report":
            rows["assessment_dois"].append(doi)
        elif typ == "referee-report":
            rows["review_dois"].append(doi)
        elif typ == "author-comment":
            rows["response_dois"].append(doi)
        else:
            unknown_types.append(typ)

    for key in rows:
        rows[key] = sorted(x for x in rows[key] if x)

    expected_prefix = str(version_doi) + ".sa"
    all_dois = (
        rows["assessment_dois"]
        + rows["review_dois"]
        + rows["response_dois"]
    )
    rows["prefix_exact"] = all(
        doi.startswith(expected_prefix) for doi in all_dois
    )
    rows["cardinality_ok"] = all([
        len(rows["assessment_dois"]) == 1,
        len(rows["review_dois"]) >= 1,
        len(rows["response_dois"]) <= 1,
    ])
    rows["unknown_subarticle_types"] = sorted(
        str(x) for x in unknown_types if x is not None
    )
    return rows


def prior_history(meta, msid, rp_version):
    events = []
    ph = first_child(meta, "pub-history") if meta is not None else None
    if ph is not None:
        for event in children(ph, "event"):
            uris = []
            for u in children(event, "self-uri"):
                uris.append({
                    "content_type": attr(u, "content-type"),
                    "doi": canonical_doi(attr(u, "href")),
                })
            roots = sorted(
                x["doi"] for x in uris
                if x["content_type"] == "reviewed-preprint" and x["doi"]
            )
            if not roots:
                continue
            events.append({
                "reviewed_preprint_dois": roots,
                "assessment_dois": sorted(
                    x["doi"] for x in uris
                    if x["content_type"] == "editor-report" and x["doi"]
                ),
                "review_dois": sorted(
                    x["doi"] for x in uris
                    if x["content_type"] == "referee-report" and x["doi"]
                ),
                "response_dois": sorted(
                    x["doi"] for x in uris
                    if x["content_type"] == "author-comment" and x["doi"]
                ),
            })

    expected = {
        C.expected_version_doi(msid, i)
        for i in range(1, rp_version)
    } if msid and rp_version and rp_version > 1 else set()

    observed = set()
    assessment_ok = True
    review_ok = True
    prefix_ok = True
    for row in events:
        if len(row["reviewed_preprint_dois"]) != 1:
            prefix_ok = False
            root = None
        else:
            root = row["reviewed_preprint_dois"][0]
            observed.add(root)
        if len(row["assessment_dois"]) != 1:
            assessment_ok = False
        if len(row["review_dois"]) < 1:
            review_ok = False
        if root:
            for doi in (
                row["assessment_dois"]
                + row["review_dois"]
                + row["response_dois"]
            ):
                if not doi.startswith(root + ".sa"):
                    prefix_ok = False

    if rp_version == 1:
        count_ok = len(events) == 0
        version_set_ok = len(events) == 0
    else:
        count_ok = len(events) == rp_version - 1
        version_set_ok = observed == expected

    events.sort(key=lambda x: x["reviewed_preprint_dois"])
    return {
        "events": events,
        "count_ok": count_ok,
        "version_set_ok": version_set_ok,
        "assessment_ok": assessment_ok,
        "review_ok": review_ok,
        "prefix_ok": prefix_ok,
    }


def surface_from_raw(path: str, raw: bytes):
    root = ET.fromstring(raw)
    meta = find_article_meta(root)
    ident = exact_identity(path, meta)
    vstate = version_state(meta)
    evals = current_evaluations(root, ident.get("expected_version_doi"))
    history = prior_history(
        meta,
        ident.get("filename_msid"),
        ident.get("filename_rp_version"),
    )
    return {
        "identity": ident,
        "version_state": vstate,
        "current_evaluations": evals,
        "history": history,
    }


def compare_runner_surface(audit, runner_surface):
    runner_history = []
    for row in runner_surface.get("prior_events", []):
        runner_history.append({
            "reviewed_preprint_dois": row.get("reviewed_preprint_dois", []),
            "assessment_dois": row.get("assessment_dois", []),
            "review_dois": row.get("review_dois", []),
            "response_dois": row.get("response_dois", []),
        })
    runner_history.sort(key=lambda x: x["reviewed_preprint_dois"])

    expected_version = audit["identity"].get("expected_version_doi")
    checks = {
        "filename_msid": (
            audit["identity"].get("filename_msid")
            == runner_surface.get("filename_msid")
        ),
        "filename_rp_version": (
            audit["identity"].get("filename_rp_version")
            == runner_surface.get("filename_rp_version")
        ),
        "version_doi": expected_version == runner_surface.get("version_doi"),
        "preprint_version": (
            audit["version_state"]["preprint_version"]
            == runner_surface.get("preprint_version")
        ),
        "publication_state": (
            audit["version_state"]["publication_state"]
            == runner_surface.get("publication_state")
        ),
        "assessment_dois": (
            audit["current_evaluations"]["assessment_dois"]
            == sorted(
                x.get("doi") for x in runner_surface.get("assessments", [])
                if x.get("doi")
            )
        ),
        "review_dois": (
            audit["current_evaluations"]["review_dois"]
            == sorted(
                x.get("doi") for x in runner_surface.get("reviews", [])
                if x.get("doi")
            )
        ),
        "response_dois": (
            audit["current_evaluations"]["response_dois"]
            == sorted(
                x.get("doi") for x in runner_surface.get("responses", [])
                if x.get("doi")
            )
        ),
        "prior_history": (
            audit["history"]["events"] == runner_history
        ),
    }
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--qualification-results", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    source = Path(args.source).resolve()
    qualification = load_json(Path(args.qualification_results))
    rows = []

    for item in qualification.get("rows", []):
        rel = item["path"]
        raw = (source / rel).read_bytes()
        audit = surface_from_raw(rel, raw)
        surface = item["surface"]
        checks = compare_runner_surface(audit, surface)

        structural_checks = {
            "identity_pass": audit["identity"]["pass"],
            "current_evaluation_cardinality": (
                audit["current_evaluations"]["cardinality_ok"]
            ),
            "current_evaluation_prefix": (
                audit["current_evaluations"]["prefix_exact"]
            ),
            "history_count": audit["history"]["count_ok"],
            "history_version_set": audit["history"]["version_set_ok"],
            "history_assessment": audit["history"]["assessment_ok"],
            "history_review": audit["history"]["review_ok"],
            "history_prefix": audit["history"]["prefix_ok"],
        }

        row_pass = all(checks.values()) and all(structural_checks.values())
        rows.append({
            "path": rel,
            "disposition": item["disposition"],
            "source_sha256": sha256(raw),
            "runner_surface_checks": checks,
            "structural_checks": structural_checks,
            "pass": row_pass,
        })

    result = {
        "study": "ELIFE_CLEAN_PROSPECTIVE_DOCUMENTARY_AUDIT_V1",
        "independence": (
            "XML_ETREE_RAW_SOURCE_AUDIT_WITHOUT_ORACLE_OR_RUNTIME_IMPORT"
        ),
        "eligible_case_count": len(rows),
        "audited_count": len(rows),
        "pass_count": sum(x["pass"] for x in rows),
        "fail_count": sum(not x["pass"] for x in rows),
        "all_pass": bool(rows) and all(x["pass"] for x in rows),
        "rows": rows,
    }
    write_json(Path(args.output), result)
    print(json.dumps({
        k: result[k] for k in (
            "study",
            "eligible_case_count",
            "audited_count",
            "pass_count",
            "fail_count",
            "all_pass",
        )
    }, ensure_ascii=False, indent=2))

    if rows and not result["all_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
