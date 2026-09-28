from __future__ import annotations

import collections
import hashlib
import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

UPSTREAM_REPO = "FloChiff/DAHNProject"
UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
PREFIX = "Correspondence/Berlin_Intellectuals/Corpus/"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"

DATE_ATTRS = (
    "when", "when-iso", "notBefore", "notAfter", "from", "to",
    "from-iso", "to-iso", "min", "max"
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
    keys = ("notBefore", "notAfter", "from", "to", "from-iso", "to-iso", "min", "max")
    return tuple((k, attrs[k]) for k in keys if k in attrs)

def carrier_role(el, ancestors):
    tag = local(el.tag)
    if tag == "docDate":
        return "docDate"
    if tag == "origDate":
        return "origDate"
    if tag == "date":
        # detect correspAction type
        for a in reversed(ancestors):
            if local(a.tag) == "correspAction":
                t = a.attrib.get("type", "")
                return f"correspAction:{t or 'unspecified'}"
        for a in reversed(ancestors):
            if local(a.tag) in ("opener", "dateline"):
                return "body_or_dateline_date"
        return "date_other"
    return tag

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
        text = norm_text("".join(el.itertext()))
        carriers.append({
            "role": role,
            "tag": tag,
            "attrs": attrs,
            "exact_dates": extract_exact_dates(attrs),
            "interval": interval_signature(attrs),
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
    roles = sorted(role_exact)
    for i, ra in enumerate(roles):
        for rb in roles[i+1:]:
            va, vb = role_exact[ra], role_exact[rb]
            if va and vb and va.isdisjoint(vb):
                disagreements.append({
                    "role_a": ra, "values_a": sorted(va),
                    "role_b": rb, "values_b": sorted(vb),
                })

    uncertain = []
    for c in carriers:
        if c["interval"] or (c["cert"] and c["cert"].lower() not in ("high", "certain")) or c["precision"]:
            uncertain.append(c)

    note_hits = []
    for el in root.iter():
        tag = local(el.tag)
        if tag not in ("note", "p", "origin", "history"):
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

    triggers = []
    if disagreements:
        triggers.append("D1")
    # D2 requires non-singleton/uncertain carrier PLUS another temporal carrier.
    if uncertain and len(role_exact) >= 2:
        triggers.append("D2")
    if note_hits:
        triggers.append("D3")
    # D4 is only a feasibility flag here; explicit relation + at least one machine date.
    if relations and role_exact:
        triggers.append("D4_CANDIDATE")

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
        "date_note_hits": note_hits,
        "facs": facs,
        "relations": relations,
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
                "note_hits": len(d["date_note_hits"]),
                "facs": len(d["facs"]),
                "relations": len(d["relations"]),
                "evidence_layers": d["evidence_layer_count"],
            }
            for d in eligible[:30]
        ],
        "results_sha256": sha256(out.read_bytes()),
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
