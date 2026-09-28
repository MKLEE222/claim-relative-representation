from __future__ import annotations

import calendar
import collections
import hashlib
import io
import json
import re
import tarfile
import urllib.request
from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET

UPSTREAM_REPO = "FloChiff/DAHNProject"
UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
PREFIX = "Correspondence/Berlin_Intellectuals/Corpus/"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"

DATE_ATTRS = (
    "when", "when-iso",
    "notBefore", "notAfter", "notBefore-iso", "notAfter-iso",
    "from", "to", "from-iso", "to-iso",
    "min", "max"
)
UNCERTAINTY_ATTRS = ("cert", "precision", "evidence", "resp")
NOTE_KEYWORDS = (
    "incorrect", "wrong", "contrary", "contradict", "supposition", "supposed",
    "uncertain", "unclear", "probably", "perhaps", "inferred", "deduced",
    "falsch", "irrt", "vermut", "wahrschein", "unsicher", "ungewiss",
    "contraire", "incertain", "suppos", "probable", "déduit", "deduit",
    "postmark", "poststempel", "cachet"
)

def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-DAHN-feasibility/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()

def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]

def norm_text(s: str) -> str:
    return " ".join((s or "").split())

def _month_bounds(y, m):
    return date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])

def _parse_single_partial(v):
    v = (v or "").strip()
    m = re.fullmatch(r"(\d{4})", v)
    if m:
        y = int(m.group(1))
        return date(y, 1, 1), date(y, 12, 31)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", v)
    if m:
        y, mo = map(int, m.groups())
        if 1 <= mo <= 12:
            return _month_bounds(y, mo)
        return None
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", v)
    if m:
        y, mo, d = map(int, m.groups())
        try:
            x = date(y, mo, d)
            return x, x
        except ValueError:
            return None
    return None

def parse_temporal_value(v):
    v = (v or "").strip()
    if not v:
        return None

    # Year range: 1804/1806
    m = re.fullmatch(r"(\d{4})/(\d{4})", v)
    if m:
        y1, y2 = map(int, m.groups())
        return date(y1, 1, 1), date(y2, 12, 31)

    # Month range: 1805-03/05
    m = re.fullmatch(r"(\d{4})-(\d{1,2})/(\d{1,2})", v)
    if m:
        y, m1, m2 = map(int, m.groups())
        if 1 <= m1 <= 12 and 1 <= m2 <= 12:
            lo = _month_bounds(y, m1)[0]
            hi = _month_bounds(y, m2)[1]
            return lo, hi

    # Day range in same month: 1805-04-7/28
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})/(\d{1,2})", v)
    if m:
        y, mo, d1, d2 = map(int, m.groups())
        try:
            return date(y, mo, d1), date(y, mo, d2)
        except ValueError:
            return None

    return _parse_single_partial(v)

def carrier_bounds(attrs):
    when = attrs.get("when-iso") or attrs.get("when")
    if when:
        return parse_temporal_value(when)

    lowv = (
        attrs.get("notBefore-iso") or attrs.get("notBefore")
        or attrs.get("from-iso") or attrs.get("from") or attrs.get("min")
    )
    highv = (
        attrs.get("notAfter-iso") or attrs.get("notAfter")
        or attrs.get("to-iso") or attrs.get("to") or attrs.get("max")
    )

    low = parse_temporal_value(lowv) if lowv else None
    high = parse_temporal_value(highv) if highv else None
    if not low and not high:
        return None
    lo = low[0] if low else date.min
    hi = high[1] if high else date.max
    return lo, hi

def bounds_json(bounds):
    if not bounds:
        return None
    lo, hi = bounds
    return [
        None if lo == date.min else lo.isoformat(),
        None if hi == date.max else hi.isoformat(),
    ]

def bounds_disjoint(a, b):
    return bool(a and b and (a[1] < b[0] or b[1] < a[0]))

def bounds_overlap_nonidentical(a, b):
    return bool(a and b and not bounds_disjoint(a, b) and a != b)

def attrs_date(el):
    return {k: el.attrib[k] for k in DATE_ATTRS if k in el.attrib}

def extract_exact_dates(attrs):
    vals = []
    for key in ("when", "when-iso"):
        v = attrs.get(key)
        if v:
            vals.append(v)
    return tuple(sorted(set(vals)))

def interval_signature(attrs):
    keys = (
        "notBefore", "notAfter", "notBefore-iso", "notAfter-iso",
        "from", "to", "from-iso", "to-iso", "min", "max"
    )
    return tuple((k, attrs[k]) for k in keys if k in attrs)

def carrier_role(el, ancestors):
    tag = local(el.tag)
    if tag == "docDate":
        return "docDate"
    if tag == "origDate":
        return "origDate"
    if tag == "date":
        # Only declared document-dating contexts count.
        for a in reversed(ancestors):
            if local(a.tag) == "correspAction":
                t = a.attrib.get("type", "")
                return f"correspAction:{t or 'unspecified'}"
        for a in reversed(ancestors):
            if local(a.tag) in ("opener", "dateline"):
                return "body_or_dateline_date"
        return None
    return None

def build_parent_map(root):
    parent = {}
    for p in root.iter():
        for c in list(p):
            parent[c] = p
    return parent

def ancestors_of(el, parent_map):
    out = []
    cur = parent_map.get(el)
    while cur is not None:
        out.append(cur)
        cur = parent_map.get(cur)
    return list(reversed(out))

def parse_document(path, raw):
    root = ET.fromstring(raw)
    parent_map = build_parent_map(root)

    carriers = []
    for el in root.iter():
        tag = local(el.tag)
        if tag not in ("docDate", "origDate", "date"):
            continue
        attrs = attrs_date(el)
        if not attrs:
            continue
        anc = ancestors_of(el, parent_map)
        role = carrier_role(el, anc)
        if role is None:
            continue
        text = norm_text("".join(el.itertext()))
        b = carrier_bounds(attrs)
        carriers.append({
            "role": role,
            "tag": tag,
            "attrs": attrs,
            "exact_dates": extract_exact_dates(attrs),
            "interval": interval_signature(attrs),
            "bounds": bounds_json(b),
            "_bounds": b,
            "text": text,
            "cert": el.attrib.get("cert"),
            "precision": el.attrib.get("precision"),
            "resp": el.attrib.get("resp"),
        })

    # Deduplicate multilingual repetitions by semantic role + machine values.
    dedup = {}
    for c in carriers:
        key = (
            c["role"],
            c["exact_dates"],
            c["interval"],
            c["cert"],
            c["precision"],
        )
        if key not in dedup:
            dedup[key] = dict(c)
            dedup[key]["texts"] = [c["text"]] if c["text"] else []
            dedup[key].pop("text", None)
        elif c["text"] and c["text"] not in dedup[key]["texts"]:
            dedup[key]["texts"].append(c["text"])
    carriers = list(dedup.values())

    role_exact = collections.defaultdict(set)
    for c in carriers:
        for v in c["exact_dates"]:
            role_exact[c["role"]].add(v)

    disagreements = []
    for i, a in enumerate(carriers):
        for j in range(i + 1, len(carriers)):
            b = carriers[j]
            if bounds_disjoint(a.get("_bounds"), b.get("_bounds")):
                disagreements.append({
                    "carrier_a": i,
                    "role_a": a["role"],
                    "bounds_a": a["bounds"],
                    "attrs_a": a["attrs"],
                    "carrier_b": j,
                    "role_b": b["role"],
                    "bounds_b": b["bounds"],
                    "attrs_b": b["attrs"],
                })

    uncertain = []
    for c in carriers:
        if c["interval"] or (c["cert"] and c["cert"].lower() not in ("high", "certain")) or c["precision"]:
            uncertain.append(c)

    narrowing_or_competing = []
    for u in uncertain:
        for o in carriers:
            if o is u:
                continue
            if bounds_overlap_nonidentical(u.get("_bounds"), o.get("_bounds")):
                narrowing_or_competing.append({
                    "uncertain_role": u["role"],
                    "uncertain_bounds": u["bounds"],
                    "other_role": o["role"],
                    "other_bounds": o["bounds"],
                })

    note_hits = []
    for el in root.iter():
        tag = local(el.tag)
        if tag not in ("note", "p"):
            continue
        anc = ancestors_of(el, parent_map)
        anc_tags = {local(a.tag) for a in anc}
        # Restrict commentary to declared dating/history/correspondence contexts.
        if not (anc_tags & {"history", "origin", "msDesc", "correspDesc", "opener", "dateline"}):
            continue
        txt = norm_text(" ".join(el.itertext()))
        low = txt.casefold()
        matched = sorted({k for k in NOTE_KEYWORDS if k in low})
        if matched and any(ch.isdigit() for ch in txt):
            note_hits.append({
                "tag": tag,
                "resp": el.attrib.get("resp"),
                "keywords": matched,
                "text": txt[:1200],
            })

    facs = []
    for el in root.iter():
        for k, v in el.attrib.items():
            if local(k) == "facs" and v:
                facs.append(v)
    facs = sorted(set(facs))

    relations = []
    for el in root.iter():
        tag = local(el.tag)
        if tag in ("relation", "ref", "ptr"):
            target = el.attrib.get("target") or el.attrib.get("ref") or el.attrib.get("active") or el.attrib.get("passive")
            if target and ("Brief" in target or target.startswith("#")):
                relations.append({
                    "tag": tag,
                    "target": target,
                    "type": el.attrib.get("type") or el.attrib.get("name"),
                })
    relations = relations[:100]

    revisions = []
    for el in root.iter():
        if local(el.tag) == "change":
            revisions.append({
                "when": el.attrib.get("when") or el.attrib.get("when-iso"),
                "who": el.attrib.get("who"),
                "text": norm_text(" ".join(el.itertext()))[:500],
            })

    has_corresp_desc = any(local(el.tag) == "correspDesc" for el in root.iter())
    corresp_actions = sum(local(el.tag) == "correspAction" for el in root.iter())
    is_correspondence = has_corresp_desc and corresp_actions > 0

    triggers = []
    if is_correspondence and disagreements:
        triggers.append("D1")
    # D2 requires source-native uncertainty plus another compatible but non-identical constraint.
    if is_correspondence and uncertain and narrowing_or_competing:
        triggers.append("D2")
    if is_correspondence and note_hits:
        triggers.append("D3")
    # D4 cannot create eligibility without a separately validated temporal relation.
    d4_candidate = bool(is_correspondence and relations and role_exact)

    evidence_layers = 0
    if role_exact:
        evidence_layers += 1
    if note_hits:
        evidence_layers += 1
    if facs:
        evidence_layers += 1
    if relations:
        evidence_layers += 1

    return {
        "path": path,
        "carriers": carriers,
        "role_exact_dates": {k: sorted(v) for k, v in role_exact.items()},
        "disagreements": disagreements,
        "uncertain_carriers": uncertain,
        "narrowing_or_competing_constraints": narrowing_or_competing,
        "date_note_hits": note_hits,
        "facs": facs,
        "relations": relations,
        "d4_candidate": d4_candidate,
        "is_correspondence": is_correspondence,
        "revisionDesc": revisions,
        "triggers": triggers,
        "evidence_layer_count": evidence_layers,
    }

def main():
    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    raw_archive = fetch(archive_url)
    docs = []
    parse_errors = []

    with tarfile.open(fileobj=io.BytesIO(raw_archive), mode="r:gz") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            parts = Path(member.name).parts
            if len(parts) < 2:
                continue
            rel = str(Path(*parts[1:]))
            if not rel.startswith(PREFIX) or not rel.lower().endswith(".xml"):
                continue
            f = tf.extractfile(member)
            if f is None:
                continue
            raw = f.read()
            try:
                docs.append(parse_document(rel, raw))
            except Exception as e:
                parse_errors.append({"path": rel, "error": repr(e)})

    for d in docs:
        for carrier in d["carriers"]:
            carrier.pop("_bounds", None)
        for carrier in d["uncertain_carriers"]:
            carrier.pop("_bounds", None)

    docs.sort(key=lambda x: x["path"])
    eligible = [d for d in docs if d["triggers"]]
    multi = [d for d in eligible if len(d["triggers"]) > 1]
    two_layer = [d for d in eligible if d["evidence_layer_count"] >= 2]
    unresolved_delay = [
        d for d in eligible
        if d["uncertain_carriers"] and d["evidence_layer_count"] >= 2
    ]
    null_event = [d for d in eligible if len(d["revisionDesc"]) > 0]

    trig_counts = collections.Counter()
    for d in docs:
        if not d["triggers"]:
            trig_counts["NO_LIVE_TEMPORAL_DISTINCTION"] += 1
        else:
            for t in d["triggers"]:
                trig_counts[t] += 1
            if len(d["triggers"]) > 1:
                trig_counts["MULTI_TRIGGER"] += 1

    result = {
        "study": "DAHN_FRESH_HOLDOUT_FEASIBILITY_SCAN_V1",
        "authority": "PRE_SCAN_SELECTION_CONTRACT_AT_COMMIT_800da475d47d335ae699c59d9b0b76bcf43686e4",
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "archive_sha256": sha256(raw_archive),
        },
        "population": {
            "parsed_xml_documents": len(docs),
            "parse_errors": len(parse_errors),
            "eligible_documents": len(eligible),
            "multi_trigger_documents": len(multi),
            "eligible_with_2plus_evidence_layers": len(two_layer),
            "eligible_with_uncertainty_and_2plus_layers": len(unresolved_delay),
            "eligible_with_revisionDesc_for_null_event_candidate": len(null_event),
        },
        "trigger_counts": dict(trig_counts),
        "feasibility_thresholds": {
            "at_least_5_eligible": len(eligible) >= 5,
            "at_least_3_two_layer": len(two_layer) >= 3,
            "at_least_1_uncertainty_delay": len(unresolved_delay) >= 1,
            "at_least_1_null_event_candidate": len(null_event) >= 1,
            "source_handles_present_in_at_least_1": any(d["facs"] for d in eligible),
        },
        "candidate_viable": (
            len(eligible) >= 5
            and len(two_layer) >= 3
            and len(unresolved_delay) >= 1
            and len(null_event) >= 1
            and any(d["facs"] for d in eligible)
        ),
        "eligible_documents": eligible,
        "parse_errors": parse_errors,
        "claim_boundary": [
            "D4_CANDIDATE is not yet a validated temporal constraint; explicit related-document semantics require a later protocol.",
            "revisionDesc is not historical evidence and is used only as a candidate irrelevant/null event source.",
            "Repeated multilingual origDate prose with identical machine date values is deduplicated.",
            "Date disagreement is based on disjoint normalized temporal intervals, not raw string inequality.",
            "Only XML documents with correspDesc and correspAction can become holdout episodes.",
            "This scan identifies source-feasible episodes only; it does not test discovery or warrant.",
        ],
    }

    outdir = Path(__file__).with_name("dahn_feasibility_results")
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    compact = {
        "population": result["population"],
        "trigger_counts": result["trigger_counts"],
        "feasibility_thresholds": result["feasibility_thresholds"],
        "candidate_viable": result["candidate_viable"],
        "eligible_sample": [
            {
                "path": d["path"],
                "triggers": d["triggers"],
                "roles": d["role_exact_dates"],
                "disagreements": d["disagreements"],
                "uncertain": len(d["uncertain_carriers"]),
                "narrowing_or_competing": len(d["narrowing_or_competing_constraints"]),
                "note_hits": len(d["date_note_hits"]),
                "facs": len(d["facs"]),
                "relations": len(d["relations"]),
                "d4_candidate": d["d4_candidate"],
                "evidence_layers": d["evidence_layer_count"],
            }
            for d in eligible[:30]
        ],
        "results_sha256": sha256(out.read_bytes()),
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
