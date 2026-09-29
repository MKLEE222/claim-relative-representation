from __future__ import annotations

import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "amp_exposed_development_results_v1.json"
OUT = HERE / "results" / "amp_exposed_documentary_audit_v1.json"

UPSTREAM_REPO = "Auden-Musulin-Papers/amp-data"
UPSTREAM_COMMIT = "289a52de61aef0b6354e3c8298173bf1f889feb2"
PREFIX = "data/editions/"

DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
TEMP_ATTRS = (
    "when", "when-iso",
    "notBefore", "notBefore-iso",
    "notAfter", "notAfter-iso",
    "from", "from-iso",
    "to", "to-iso",
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-P-audit/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def local(el):
    return etree.QName(el).localname


def attrs(el):
    return {k.split("}")[-1]: v for k, v in el.attrib.items()}


def machine_attrs(el):
    a = attrs(el)
    return {k: a[k] for k in TEMP_ATTRS if k in a}


def local_day(value):
    m = DATE_RE.match(str(value or ""))
    return m.group(0) if m else None


def interval_from_attrs(a):
    for key in ("when", "when-iso"):
        if a.get(key):
            d = local_day(a[key])
            return [d, d] if d else None

    lo = None
    hi = None
    for key in ("notBefore", "notBefore-iso", "from", "from-iso"):
        if a.get(key):
            lo = local_day(a[key])
            break
    for key in ("notAfter", "notAfter-iso", "to", "to-iso"):
        if a.get(key):
            hi = local_day(a[key])
            break

    if lo or hi:
        return [lo, hi]
    return None


def disjoint(a, b):
    if a is None or b is None:
        return False
    alo, ahi = a
    blo, bhi = b
    if alo is None or ahi is None or blo is None or bhi is None:
        return False
    return ahi < blo or bhi < alo


def has_excluded_ancestor(el, stop=None):
    p = el.getparent()
    while p is not None and p is not stop:
        lname = local(p)
        typ = (p.get("type") or "").lower()
        if lname == "floatingText":
            return True
        if typ in {"annex", "annexe", "envelope", "enclosure"}:
            return True
        p = p.getparent()
    return False


def primary_letters(root):
    out = []
    for el in root.xpath("//*[local-name()='div' and @type='letter']"):
        if has_excluded_ancestor(el):
            continue
        # A letter nested inside another admitted letter is embedded, not another primary.
        p = el.getparent()
        nested_letter = False
        while p is not None:
            if local(p) == "div" and (p.get("type") or "").lower() == "letter":
                nested_letter = True
                break
            if local(p) == "body":
                break
            p = p.getparent()
        if not nested_letter:
            out.append(el)
    return out


def root_carriers(root, selected):
    rows = []

    for el in root.xpath("//*[local-name()='msContents']//*[local-name()='docDate']"):
        a = machine_attrs(el)
        if a:
            rows.append({
                "role": "docDate",
                "attrs": a,
                "interval": interval_from_attrs(a),
                "location": "msContents/docDate",
                "excluded": False,
            })

    for action in root.xpath("//*[local-name()='correspAction' and @type='sent']"):
        for el in action.xpath(".//*[local-name()='date']"):
            a = machine_attrs(el)
            if a:
                rows.append({
                    "role": "sent",
                    "attrs": a,
                    "interval": interval_from_attrs(a),
                    "location": "correspAction[@type=sent]/date",
                    "excluded": False,
                })

    if selected is not None:
        for el in selected.xpath(
            ".//*[local-name()='dateline']//*[local-name()='date']"
            " | ./*[local-name()='dateline']/*[local-name()='date']"
        ):
            a = machine_attrs(el)
            if not a:
                continue
            excluded = has_excluded_ancestor(el, stop=selected)
            rows.append({
                "role": "dateline",
                "attrs": a,
                "interval": interval_from_attrs(a),
                "location": "selected-letter/dateline/date",
                "excluded": excluded,
            })

    return rows


def origin_carriers(root):
    rows = []
    for origin in root.xpath("//*[local-name()='history']/*[local-name()='origin']"):
        for el in origin.xpath(".//*[local-name()='origDate']"):
            a = machine_attrs(el)
            if a:
                rows.append({
                    "attrs": a,
                    "interval": interval_from_attrs(a),
                    "location": "history/origin//origDate",
                })
    return rows


def read_population(archive_raw):
    out = {}
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            parts = Path(member.name).parts
            if len(parts) < 2:
                continue
            rel = str(Path(*parts[1:]))
            if not rel.startswith(PREFIX) or not rel.endswith(".xml"):
                continue
            suffix = rel[len(PREFIX):]
            if "/" in suffix or "\\" in suffix:
                continue
            f = tf.extractfile(member)
            if f:
                out[rel] = f.read()
    return out


def audit_case(item, raw):
    root = etree.fromstring(raw)
    letters = primary_letters(root)
    selected = letters[0] if len(letters) == 1 else None

    roots_all = root_carriers(root, selected)
    active_roots = [x for x in roots_all if not x["excluded"] and x["interval"] is not None]
    excluded_roots = [x for x in roots_all if x["excluded"]]
    origins = origin_carriers(root)
    machine_origins = [x for x in origins if x["interval"] is not None]

    expected_class = item["transition_class"]
    source_origin = item.get("origin_claim") or {}

    checks = {
        "one_primary_letter": len(letters) == 1,
        "one_machine_origin": len(machine_origins) == 1,
        "excluded_carriers_separated": all(x.get("excluded") is True for x in excluded_roots),
        "source_file_exact": source_origin.get("source_file") == item["path"],
        "origin_applicability_exact": (
            source_origin.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT"
        ),
        "source_repository_exact": (
            source_origin.get("source_repository") == UPSTREAM_REPO
        ),
        "source_version_exact": (
            source_origin.get("source_version") == UPSTREAM_COMMIT
        ),
    }

    independent_class = "UNRESOLVED"
    class_evidence = {}

    if len(machine_origins) == 1:
        oi = machine_origins[0]["interval"]
        if expected_class == "P-U1_CONFLICT_FORMATION":
            independent_class = (
                "P-U1_CONFLICT_FORMATION"
                if len(active_roots) == 1 and disjoint(active_roots[0]["interval"], oi)
                else "UNRESOLVED"
            )
            class_evidence = {
                "root_count": len(active_roots),
                "root_interval": active_roots[0]["interval"] if len(active_roots) == 1 else None,
                "origin_interval": oi,
                "disjoint": (
                    disjoint(active_roots[0]["interval"], oi)
                    if len(active_roots) == 1 else None
                ),
            }
        elif expected_class == "P-U2_RESOLUTION_OR_ACQUISITION":
            independent_class = (
                "P-U2_RESOLUTION_OR_ACQUISITION"
                if len(active_roots) == 0
                else "UNRESOLVED"
            )
            class_evidence = {
                "root_count": len(active_roots),
                "origin_interval": oi,
            }
        else:
            independent_class = "OTHER_NOT_INDEPENDENTLY_CLASSIFIED"
            class_evidence = {
                "root_count": len(active_roots),
                "origin_interval": oi,
            }

    checks["transition_class_exact"] = independent_class == expected_class

    status = "PASS" if all(checks.values()) else "FAIL"

    return {
        "path": item["path"],
        "expected_transition_class": expected_class,
        "independent_transition_class": independent_class,
        "status": status,
        "checks": checks,
        "primary_letter_count": len(letters),
        "active_root_carriers": active_roots,
        "excluded_root_carriers": excluded_roots,
        "origin_carriers": machine_origins,
        "class_evidence": class_evidence,
    }


def main():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    manifest = results.get("eligible_manifest") or []

    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    population = read_population(archive_raw)

    audited = []
    missing = []
    for item in manifest:
        raw = population.get(item["path"])
        if raw is None:
            missing.append(item["path"])
            continue
        audited.append(audit_case(item, raw))

    summary = {
        "study": "MODULE_P_AMP_EXPOSED_DOCUMENTARY_AUDIT_V1",
        "data_status": "EXPOSED_DEVELOPMENT_ONLY",
        "eligible_manifest_n": len(manifest),
        "audited_n": len(audited),
        "missing_n": len(missing),
        "pass_n": sum(x["status"] == "PASS" for x in audited),
        "fail_n": sum(x["status"] == "FAIL" for x in audited),
        "class_counts": {
            cls: sum(x["independent_transition_class"] == cls for x in audited)
            for cls in sorted({x["independent_transition_class"] for x in audited})
        },
        "missing_paths": missing,
        "cases": audited,
        "interpretation_guard": [
            "This audit is post-exposure development validation.",
            "It does not alter authoritative Module O NULL_APPLICABILITY.",
            "It is independent of Module-P oracle/runtime eligibility helpers.",
        ],
    }

    OUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": summary["study"],
        "eligible_manifest_n": summary["eligible_manifest_n"],
        "audited_n": summary["audited_n"],
        "pass_n": summary["pass_n"],
        "fail_n": summary["fail_n"],
        "class_counts": summary["class_counts"],
        "missing_paths": summary["missing_paths"],
    }, ensure_ascii=False, indent=2))

    if missing or any(x["status"] != "PASS" for x in audited):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
