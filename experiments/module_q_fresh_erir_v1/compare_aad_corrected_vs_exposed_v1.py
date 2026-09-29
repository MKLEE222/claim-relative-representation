from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

CORRECTED = RESULTS / "aad_corrected_reproduction_results_v1.json"
EXPOSED = RESULTS / "aad_exposed_audit_results_v1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


OPAQUE_CLAIM_PATH = re.compile(r"^claims/[0-9a-f]{64}:(.+)$")


def normalize_failure_evaluation(value):
    if isinstance(value, dict):
        return {k: normalize_failure_evaluation(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_failure_evaluation(v) for v in value]
    if isinstance(value, str):
        m = OPAQUE_CLAIM_PATH.match(value)
        if m:
            return "claims/<context-bound-key>:" + m.group(1)
    return value


def slim_manifest(rows):
    out = []
    for x in rows:
        out.append({
            "path": x.get("path"),
            "source_sha256": x.get("source_sha256"),
            "transition_class": x.get("transition_class"),
            "old_d1d2_eligible": x.get("old_d1d2_eligible"),
            "phi_before": x.get("phi_before"),
            "phi_after": x.get("phi_after"),
            "p_evaluation": x.get("p_evaluation"),
            "comparator_evaluation": x.get("comparator_evaluation"),
            "failure_evaluation": normalize_failure_evaluation(
                x.get("failure_evaluation")
            ),
        })
    return out


def slim_nulls(rows):
    return [
        {
            "path": x.get("path"),
            "source_sha256": x.get("source_sha256"),
            "phi_before": x.get("phi_before"),
            "phi_after": x.get("phi_after"),
        }
        for x in rows
    ]


def first_diff(a, b, path="$"):
    if type(a) is not type(b):
        return {"path": path, "left": a, "right": b, "reason": "type"}
    if isinstance(a, dict):
        if set(a) != set(b):
            return {
                "path": path,
                "left_keys": sorted(a),
                "right_keys": sorted(b),
                "reason": "keys",
            }
        for k in sorted(a):
            d = first_diff(a[k], b[k], path + "." + str(k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return {
                "path": path,
                "left_len": len(a),
                "right_len": len(b),
                "reason": "length",
            }
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, path + f"[{i}]")
            if d:
                return d
        return None
    if a != b:
        return {"path": path, "left": a, "right": b, "reason": "value"}
    return None


def main():
    a = load(CORRECTED)
    b = load(EXPOSED)

    checks = {
        "upstream_snapshot": a["upstream"] == b["upstream"],
        "population": a["population"] == b["population"],
        "regime_separation": a["regime_separation"] == b["regime_separation"],
        "reference_capabilities": (
            a["reference_capabilities"] == b["reference_capabilities"]
        ),
        "comparator_capabilities": (
            a["comparator_capabilities"] == b["comparator_capabilities"]
        ),
        "failure_interventions": (
            a["failure_interventions"] == b["failure_interventions"]
        ),
        "eligible_manifest_scientific_surface": (
            slim_manifest(a["eligible_manifest"])
            == slim_manifest(b["eligible_manifest"])
        ),
        "null_manifest_scientific_surface": (
            slim_nulls(a["null_event_manifest"])
            == slim_nulls(b["null_event_manifest"])
        ),
        "parse_errors": a["parse_error_manifest"] == b["parse_error_manifest"],
        "contract_unresolved": (
            a["contract_unresolved_manifest"]
            == b["contract_unresolved_manifest"]
        ),
    }

    left_manifest = slim_manifest(a["eligible_manifest"])
    right_manifest = slim_manifest(b["eligible_manifest"])
    manifest_first_diff = first_diff(left_manifest, right_manifest)

    report = {
        "study": "AAD_CORRECTED_REPRODUCTION_CONSISTENCY_V1",
        "corrected_status": a.get("data_status"),
        "exposed_status": b.get("data_status"),
        "checks": checks,
        "all_scientific_outputs_match": all(checks.values()),
        "eligible_manifest_first_diff": manifest_first_diff,
        "note": (
            "source_context.population_scope and study/data-status labels are intentionally "
            "different and excluded from equality. Opaque claim-key hashes embedded in fault "
            "paths are normalized because those hashes are intentionally source-context-bound; "
            "the mutation type/status must still match exactly. All other scientific surfaces "
            "must match exactly."
        ),
    }

    out = RESULTS / "aad_corrected_reproduction_consistency_v1.json"
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not all(checks.values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
