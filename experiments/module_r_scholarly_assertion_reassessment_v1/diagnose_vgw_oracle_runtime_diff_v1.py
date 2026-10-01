from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import vgw_oracle
import vgw_runtime

ANCHORS = HERE / "VGW_DISTRIBUTION_METADATA_ANCHORS_v1.json"

EXPECTED_SHA = {
    "de_la_faille_1970": "88ae395103d86b5b40afb40465d7d093d88412f16841c936bfa22e68502548e3",
    "works_after_1970": "eed8cd78f3ec811b5302555abb5cad14cc86679ebc23e9132f46943803dac810",
    "van_gogh_museum": "8985296d791366910ae01a954d0ade65f196f461cd78328ce21602e2ed279e43",
    "krollermuller_museum": "78c48e3f7cb1699548e3d7f2e604ce363a663deca1b3747343fb22c013c788b2",
    "rkd_collections": "85ec7afd25c3cd4cf99924d65a7b9954c50254715467231a0a1f56fe1e5d7f03",
}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def fetch_all():
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    by_slug = {x["slug"]: x for x in anchors["datasets"]}
    out = {}
    for slug, expected in EXPECTED_SHA.items():
        req = urllib.request.Request(
            by_slug[slug]["content_url"],
            headers={
                "User-Agent": "CRR-VGW-postfresh-extractor-diff/1.0",
                "Accept": "application/n-triples",
                "Accept-Encoding": "identity",
            },
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw = resp.read()
        if sha256(raw) != expected:
            raise RuntimeError(f"SOURCE_SHA_MISMATCH::{slug}")
        out[slug] = raw
    return out


def disposition_counts(ex):
    return dict(sorted(Counter(x["disposition"] for x in ex["cases"]).items()))


def invalid_counts(ex):
    return dict(sorted(Counter(x["disposition"] for x in ex["invalid_records"]).items()))


def case_map(ex):
    return {x["f_number"]: x for x in ex["cases"]}


def case_science_surface(x):
    event = x.get("event") or {}
    state = x.get("state") or {}
    assertions = state.get("assertions") or {}
    return {
        "disposition": x.get("disposition"),
        "expected_transition_class": x.get("expected_transition_class"),
        "baseline_object_uri": x.get("baseline_object_uri"),
        "current_object_uri": x.get("current_object_uri"),
        "current_provider_slug": x.get("current_provider_slug"),
        "state_object_id": state.get("object_id"),
        "assertions": assertions,
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "responsible_agent": event.get("responsible_agent"),
        "operation": event.get("operation"),
        "status": event.get("status"),
    }


def first_dict_diff(a, b, prefix="$"):
    if type(a) is not type(b):
        return {"path": prefix, "left": a, "right": b, "reason": "type"}
    if isinstance(a, dict):
        if set(a) != set(b):
            return {
                "path": prefix,
                "left_keys": sorted(a),
                "right_keys": sorted(b),
                "reason": "keys",
            }
        for k in sorted(a):
            d = first_dict_diff(a[k], b[k], prefix + "." + str(k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return {
                "path": prefix,
                "left_len": len(a),
                "right_len": len(b),
                "reason": "length",
            }
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_dict_diff(x, y, prefix + f"[{i}]")
            if d:
                return d
        return None
    if a != b:
        return {"path": prefix, "left": a, "right": b, "reason": "value"}
    return None


def main():
    raw = fetch_all()
    source_version = "VGW_POSTFRESH_DIFF_DIAGNOSTIC"
    o = vgw_oracle.extract_population(raw, source_version)
    r = vgw_runtime.extract_population(raw, source_version)

    om = case_map(o)
    rm = case_map(r)
    all_f = sorted(set(om) | set(rm))
    disposition_mismatches = []
    science_surface_mismatches = []

    for fnum in all_f:
        if fnum not in om or fnum not in rm:
            disposition_mismatches.append({
                "f_number": fnum,
                "oracle": om.get(fnum, {}).get("disposition"),
                "runtime": rm.get(fnum, {}).get("disposition"),
                "missing_side": "oracle" if fnum not in om else "runtime",
            })
            continue
        if om[fnum]["disposition"] != rm[fnum]["disposition"]:
            disposition_mismatches.append({
                "f_number": fnum,
                "oracle": om[fnum]["disposition"],
                "runtime": rm[fnum]["disposition"],
            })
        os = case_science_surface(om[fnum])
        rs = case_science_surface(rm[fnum])
        d = first_dict_diff(os, rs)
        if d and len(science_surface_mismatches) < 40:
            science_surface_mismatches.append({
                "f_number": fnum,
                "oracle_disposition": om[fnum]["disposition"],
                "runtime_disposition": rm[fnum]["disposition"],
                "first_diff": d,
            })

    triple_stats = {}
    for slug, source in raw.items():
        triples = vgw_runtime.parse_nt(source)
        frozen = [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in triples]
        counts = Counter(frozen)
        dup_keys = [k for k, v in counts.items() if v > 1]
        triple_stats[slug] = {
            "parsed_triples": len(triples),
            "unique_lexical_triples": len(counts),
            "duplicate_occurrences_beyond_set": len(triples) - len(counts),
            "duplicate_triple_keys": len(dup_keys),
            "max_duplicate_multiplicity": max(counts.values()) if counts else 0,
        }

    o_full = dict(o)
    r_full = dict(r)
    o_full.pop("engine", None)
    r_full.pop("engine", None)
    full_first_diff = first_dict_diff(o_full, r_full)

    report = {
        "study": "VGW_POSTFRESH_ORACLE_RUNTIME_DIFF_V1",
        "source_sha256": EXPECTED_SHA,
        "records_by_slug": {
            "oracle": o["records_by_slug"],
            "runtime": r["records_by_slug"],
            "equal": o["records_by_slug"] == r["records_by_slug"],
        },
        "invalid_dispositions": {
            "oracle": invalid_counts(o),
            "runtime": invalid_counts(r),
        },
        "case_dispositions": {
            "oracle": disposition_counts(o),
            "runtime": disposition_counts(r),
        },
        "case_key_counts": {
            "oracle": len(om),
            "runtime": len(rm),
            "intersection": len(set(om) & set(rm)),
        },
        "disposition_mismatch_count": len(disposition_mismatches),
        "disposition_mismatch_sample": disposition_mismatches[:40],
        "science_surface_mismatch_sample": science_surface_mismatches,
        "post1970_role_exclusions": {
            "oracle": len(o["post1970_role_exclusions"]),
            "runtime": len(r["post1970_role_exclusions"]),
        },
        "runtime_duplicate_triple_stats": triple_stats,
        "full_extraction_first_diff": full_first_diff,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
