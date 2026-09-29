from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

CORRECTED = RESULTS / "aad_corrected_reproduction_results_v1.json"
EXPOSED = RESULTS / "aad_exposed_audit_results_v1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


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
            "failure_evaluation": x.get("failure_evaluation"),
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

    report = {
        "study": "AAD_CORRECTED_REPRODUCTION_CONSISTENCY_V1",
        "corrected_status": a.get("data_status"),
        "exposed_status": b.get("data_status"),
        "checks": checks,
        "all_scientific_outputs_match": all(checks.values()),
        "note": (
            "source_context.population_scope and study/data-status labels are intentionally "
            "different and excluded from equality; scientific population/outcome surfaces "
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
