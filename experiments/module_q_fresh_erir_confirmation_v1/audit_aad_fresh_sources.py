from __future__ import annotations

import hashlib
import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "aad_fresh_results_v1.json"
OUT = HERE / "results" / "aad_fresh_documentary_audit_v1.json"

UPSTREAM_REPO = "auden-in-austria-digital/aad-data"
UPSTREAM_COMMIT = "34c3958686ab03614dedd8d979ffe94b6c0f2a28"
PREFIX = "data/xml/editions/"
EXPECTED_XML = 148

DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
TEMP_ATTRS = (
    "when", "when-iso",
    "notBefore", "notBefore-iso",
    "notAfter", "notAfter-iso",
    "from", "from-iso",
    "to", "to-iso",
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CRR-module-Q-AAD-documentary-audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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

    if lo is None and hi is None:
        return None
    return [lo, hi]


def disjoint(a, b):
    if a is None or b is None:
        return False
    alo, ahi = a
    blo, bhi = b
    if ahi is not None and blo is not None and ahi < blo:
        return True
    if bhi is not None and alo is not None and bhi < alo:
        return True
    return False


def intersection(intervals):
    if not intervals:
        return None

    lows = [x[0] for x in intervals if x and x[0] is not None]
    highs = [x[1] for x in intervals if x and x[1] is not None]

    lo = max(lows) if lows else None
    hi = min(highs) if highs else None

    if lo is not None and hi is not None and lo > hi:
        return None
    return [lo, hi]


def warrant_kind(interval):
    if interval is None:
        return "UNRESOLVED"
    lo, hi = interval
    if lo is not None and hi is not None and lo == hi:
        return "EXACT"
    if lo is None or hi is None:
        return "OPEN_INTERVAL"
    return "INTERVAL"


def phi_root(carriers):
    usable = [x for x in carriers if x.get("interval") is not None]
    if not usable:
        return {
            "type": "UNRESOLVED",
            "reason_class": "NO_MACHINE_TEMPORAL_CARRIER",
        }

    iv = intersection([x["interval"] for x in usable])
    if iv is None:
        alts = [
            {"role": x["role"], "interval": x["interval"]}
            for x in usable
        ]
        alts.sort(
            key=lambda x: (
                str(x.get("role")),
                json.dumps(x.get("interval"), sort_keys=True),
            )
        )
        return {"type": "ALTERNATIVE_SET", "alternatives": alts}

    return {"type": warrant_kind(iv), "interval": iv}


def phi_after(carriers, origin):
    if origin is None or origin.get("interval") is None:
        return phi_root(carriers)

    oi = origin["interval"]
    dis = [
        x for x in carriers
        if x.get("interval") is not None and disjoint(oi, x["interval"])
    ]
    if dis:
        alts = [{"role": "origDate", "interval": oi}] + [
            {"role": x["role"], "interval": x["interval"]}
            for x in dis
        ]
        alts.sort(
            key=lambda x: (
                str(x.get("role")),
                json.dumps(x.get("interval"), sort_keys=True),
            )
        )
        return {"type": "ALTERNATIVE_SET", "alternatives": alts}

    return {"type": warrant_kind(oi), "interval": oi}


def classify_transition(before, after):
    if before == after:
        return "ADMISSIBLE_NULL_EVENT"

    bt = (before or {}).get("type")
    at = (after or {}).get("type")

    if bt in {"EXACT", "INTERVAL", "OPEN_INTERVAL"} and at == "ALTERNATIVE_SET":
        return "P-U1_CONFLICT_FORMATION"
    if bt == "UNRESOLVED" and at in {
        "EXACT", "INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET"
    }:
        return "P-U2_RESOLUTION_OR_ACQUISITION"
    if bt == "ALTERNATIVE_SET" and at == "ALTERNATIVE_SET":
        return "P-U4_ALTERNATIVE_REVISION"
    if bt not in {None, "UNRESOLVED", "ALTERNATIVE_SET"} and at in {
        "EXACT", "INTERVAL", "OPEN_INTERVAL"
    }:
        return "P-U3_NARROWING_OR_QUALIFICATION"
    return "OTHER"


def excluded_container(el, stop=None):
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


def body_node(root):
    rows = root.xpath("//*[local-name()='body']")
    return rows[0] if rows else None


def object_selection(root):
    body = body_node(root)
    if body is None:
        return {
            "status": "NO_PRIMARY_DOCUMENT_OBJECT",
            "boundary_kind": None,
            "selected": None,
            "candidate_count": 0,
        }

    explicit = []
    for el in body.xpath(".//*[local-name()='div' and @type='letter']"):
        if excluded_container(el, stop=body):
            continue
        p = el.getparent()
        nested = False
        while p is not None and p is not body:
            if local(p) == "div" and (p.get("type") or "").lower() == "letter":
                nested = True
                break
            p = p.getparent()
        if not nested:
            explicit.append(el)

    if len(explicit) == 1:
        return {
            "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
            "boundary_kind": "EXPLICIT_LETTER_DIV",
            "selected": explicit[0],
            "candidate_count": 1,
        }
    if len(explicit) > 1:
        return {
            "status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
            "boundary_kind": None,
            "selected": None,
            "candidate_count": len(explicit),
        }

    trans = [
        x for x in body.xpath(".//*[local-name()='div' and @type='transcription']")
        if not excluded_container(x, stop=body)
    ]

    corresp_desc = root.xpath("//*[local-name()='correspDesc']")
    sent_actions = root.xpath(
        "//*[local-name()='correspAction' and @type='sent']"
    )

    if len(trans) == 1:
        substantive = bool(" ".join(" ".join(trans[0].itertext()).split()))
        if len(corresp_desc) == 1 and sent_actions and substantive:
            return {
                "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
                "boundary_kind": "TRANSCRIPTION_AS_LETTER",
                "selected": trans[0],
                "candidate_count": 1,
            }
    elif len(trans) > 1:
        return {
            "status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
            "boundary_kind": None,
            "selected": None,
            "candidate_count": len(trans),
        }

    direct_divs = [
        x for x in body
        if isinstance(x.tag, str) and local(x) == "div"
    ]
    if len(direct_divs) == 1:
        candidate = direct_divs[0]
        markers = {
            local(x) for x in candidate.iter()
            if isinstance(x.tag, str)
            and local(x) in {"opener", "closer", "salute", "signed", "dateline"}
        }
        substantive = bool(" ".join(" ".join(candidate.itertext()).split()))
        if (
            candidate.get("type") is None
            and len(corresp_desc) == 1
            and sent_actions
            and markers
            and substantive
        ):
            return {
                "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
                "boundary_kind": "UNTYPED_BODY_LETTER",
                "selected": candidate,
                "candidate_count": 1,
            }

    return {
        "status": "NO_PRIMARY_DOCUMENT_OBJECT",
        "boundary_kind": None,
        "selected": None,
        "candidate_count": 0,
    }


def root_carriers(root, selected):
    rows = []

    for el in root.xpath("//*[local-name()='msContents']//*[local-name()='docDate']"):
        a = machine_attrs(el)
        iv = interval_from_attrs(a)
        if iv is not None:
            rows.append({
                "role": "docDate",
                "attrs": a,
                "interval": iv,
                "location": "msContents/docDate",
            })

    for action in root.xpath("//*[local-name()='correspAction' and @type='sent']"):
        for el in action.xpath(".//*[local-name()='date']"):
            a = machine_attrs(el)
            iv = interval_from_attrs(a)
            if iv is not None:
                rows.append({
                    "role": "sent",
                    "attrs": a,
                    "interval": iv,
                    "location": "correspAction[@type=sent]/date",
                })

    if selected is not None:
        for el in selected.xpath(
            ".//*[local-name()='date']"
        ):
            a = machine_attrs(el)
            if not a:
                continue
            p = el.getparent()
            marker = False
            while p is not None and p is not selected:
                if local(p) in {"opener", "dateline"}:
                    marker = True
                if (
                    local(p) == "div"
                    and (p.get("type") or "").lower() in {"annex", "annexe"}
                ):
                    marker = False
                    break
                p = p.getparent()
            if marker:
                iv = interval_from_attrs(a)
                if iv is not None:
                    rows.append({
                        "role": "dateline",
                        "attrs": a,
                        "interval": iv,
                        "location": "selected-object/opener-or-dateline/date",
                    })

    return rows


def choose_origin(root):
    histories = root.xpath("//*[local-name()='history']")
    if not histories:
        return []

    origins = [
        x for x in histories[0]
        if isinstance(x.tag, str) and local(x) == "origin"
    ]
    if not origins:
        return []

    origin = origins[0]
    ps = [
        x for x in origin
        if isinstance(x.tag, str) and local(x) == "p"
    ]

    chosen = None
    if ps:
        xml_lang = "{http://www.w3.org/XML/1998/namespace}lang"
        for wanted in ("en", "de", "fr"):
            for p in ps:
                if (p.get(xml_lang) or "").lower() == wanted:
                    chosen = p
                    break
            if chosen is not None:
                break
        if chosen is None:
            chosen = ps[0]
        scope = chosen
    else:
        scope = origin

    rows = []
    for el in scope.xpath(".//*[local-name()='origDate']"):
        a = machine_attrs(el)
        iv = interval_from_attrs(a)
        if iv is not None:
            rows.append({
                "role": "origDate",
                "attrs": a,
                "interval": iv,
                "location": "history/origin/origDate",
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
            if not rel.startswith(PREFIX) or not rel.lower().endswith(".xml"):
                continue
            suffix = rel[len(PREFIX):]
            if "/" in suffix or "\\" in suffix:
                continue
            f = tf.extractfile(member)
            if f is not None:
                out[rel] = f.read()
    return out


def audit_case(item, raw):
    root = etree.fromstring(raw)
    obj = object_selection(root)
    selected = obj["selected"]
    roots = root_carriers(root, selected)
    origins = choose_origin(root)
    origin = origins[0] if len(origins) == 1 else None

    before = phi_root(roots)
    after = phi_after(roots, origin)
    transition_class = classify_transition(before, after)

    source_origin = item.get("origin_claim") or {}

    checks = {
        "source_sha256_exact": sha256(raw) == item.get("source_sha256"),
        "single_primary_object": obj["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        "one_machine_origin": len(origins) == 1,
        "source_file_exact": source_origin.get("source_file") == item.get("path"),
        "origin_applicability_exact": (
            source_origin.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT"
        ),
        "source_repository_exact": (
            source_origin.get("source_repository") == UPSTREAM_REPO
        ),
        "source_version_exact": (
            source_origin.get("source_version") == UPSTREAM_COMMIT
        ),
        "origin_interval_exact": (
            origin is not None
            and source_origin.get("interval") == origin.get("interval")
        ),
        "phi_before_exact": before == item.get("phi_before"),
        "phi_after_exact": after == item.get("phi_after"),
        "transition_class_exact": transition_class == item.get("transition_class"),
    }

    return {
        "path": item["path"],
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "object_status": obj["status"],
        "boundary_kind": obj["boundary_kind"],
        "root_carriers": roots,
        "origin_carriers": origins,
        "independent_phi_before": before,
        "independent_phi_after": after,
        "independent_transition_class": transition_class,
        "expected_transition_class": item.get("transition_class"),
    }


def main():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    manifest = results.get("eligible_manifest") or []

    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    population = read_population(archive_raw)

    population_complete = len(population) == EXPECTED_XML

    audited = []
    missing = []
    for item in manifest:
        raw = population.get(item["path"])
        if raw is None:
            missing.append(item["path"])
            continue
        audited.append(audit_case(item, raw))

    all_audited_pass = (
        not missing
        and len(audited) == len(manifest)
        and all(x["status"] == "PASS" for x in audited)
    )

    ref = results.get("fresh_reference_disposition")

    if not population_complete:
        final = "INVALID"
    elif ref == "INVALID":
        final = "INVALID"
    elif ref == "NULL_APPLICABILITY":
        final = (
            "NULL_APPLICABILITY"
            if len(manifest) == 0
            else "INVALID"
        )
    elif ref == "REFERENCE_PASS_PENDING_DOCUMENTARY_AUDIT":
        final = "PASS" if all_audited_pass else "BOUNDED_PARTIAL"
    elif ref == "BOUNDED_PARTIAL_REFERENCE":
        final = "BOUNDED_PARTIAL"
    else:
        final = "INVALID"

    summary = {
        "study": "MODULE_Q_AAD_FRESH_DOCUMENTARY_AUDIT_V1",
        "data_status": "FRESH_ONE_SHOT_CONFIRMATORY_SOURCE_AUDIT",
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "prefix": PREFIX,
            "archive_sha256": sha256(archive_raw),
            "population_xml": len(population),
            "population_complete": population_complete,
        },
        "eligible_manifest_n": len(manifest),
        "audited_n": len(audited),
        "missing_n": len(missing),
        "pass_n": sum(x["status"] == "PASS" for x in audited),
        "fail_n": sum(x["status"] == "FAIL" for x in audited),
        "missing_paths": missing,
        "cases": audited,
        "fresh_reference_disposition": ref,
        "final_disposition": final,
        "independence_ceiling": (
            "FRESH_CROSS_PROJECT_SAME_FRAMEWORK_REPLICATION"
        ),
        "interpretation_guard": [
            "This audit was frozen before any AAD episode XML was opened.",
            "It independently reconstructs object/carrier/warrant semantics from raw XML.",
            "It does not call Module-P eligibility or warrant helpers.",
            "AAD shares a closely related TEI/edition framework with AMP.",
            "PASS is not cross-encoding or independent-infrastructure confirmation.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": summary["study"],
        "population_xml": summary["upstream"]["population_xml"],
        "population_complete": summary["upstream"]["population_complete"],
        "eligible_manifest_n": summary["eligible_manifest_n"],
        "audited_n": summary["audited_n"],
        "pass_n": summary["pass_n"],
        "fail_n": summary["fail_n"],
        "fresh_reference_disposition": ref,
        "final_disposition": final,
        "audit_sha256": sha256(OUT.read_bytes()),
    }, ensure_ascii=False, indent=2))

    if final == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
