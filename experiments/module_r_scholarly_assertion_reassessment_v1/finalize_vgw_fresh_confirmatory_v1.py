from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "vgw_fresh_confirmatory_v1"

AUTH = RESULTS / "authoritative_results_v1.json"
AUDIT = RESULTS / "documentary_audit_v1.json"
DIST = RESULTS / "distribution_manifest_v1.json"
MARKER = RESULTS / "DATA_OPEN_EVENT_v1.json"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, obj):
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    auth = load(AUTH)
    audit = load(AUDIT)
    dist = load(DIST)
    marker = load(MARKER)

    pop = auth["population"]
    substantive = int(pop["substantive_candidates"])
    nulls = int(pop["admissible_null_events"])

    integrity = {
        "data_open_marker_present": marker.get("event") == "DATA_OPEN_EVENT",
        "distribution_manifest_complete": bool(dist.get("complete")),
        "source_manifest_consistent": (
            auth.get("source_manifest_sha256")
            == dist.get("source_manifest_sha256")
            == audit.get("source_manifest_sha256")
        ),
        "oracle_runtime_extraction_exact": bool(
            auth.get("oracle_runtime_extraction_exact")
        ),
        "no_execution_failures": (
            len(auth.get("execution_failure_manifest") or []) == 0
        ),
        "documentary_audit_complete": (
            int(audit.get("audited_count") or 0) == substantive
        ),
        "documentary_audit_pass": bool(
            audit.get("all_substantive_audits_pass")
        ),
    }

    if not all(integrity.values()):
        final = "INVALID"
    elif substantive > 0:
        final = "PASS"
    elif nulls > 0:
        final = "NULL_REASSESSMENT"
    else:
        final = "NULL_APPLICABILITY"

    report = {
        "study": "MODULE_R_VGW_FRESH_CONFIRMATORY_V1",
        "final_disposition": final,
        "integrity": integrity,
        "population": pop,
        "computational_disposition": auth.get(
            "computational_disposition"
        ),
        "documentary_audit": {
            "substantive_candidate_count": audit.get(
                "substantive_candidate_count"
            ),
            "audited_count": audit.get("audited_count"),
            "all_substantive_audits_pass": audit.get(
                "all_substantive_audits_pass"
            ),
        },
        "hashes": {
            "data_open_event_sha256": sha256(MARKER.read_bytes()),
            "distribution_manifest_sha256": sha256(DIST.read_bytes()),
            "authoritative_results_sha256": sha256(AUTH.read_bytes()),
            "documentary_audit_sha256": sha256(AUDIT.read_bytes()),
        },
        "claim_ceiling": [
            "The result concerns VGW project-relative attribution status, not true authorship.",
            "A PASS is one prospective fresh non-temporal scholarly reassessment ecology.",
            "It does not establish prevalence or universal representational necessity.",
        ],
    }
    write_json(RESULTS / "FINAL_RESULT_v1.json", report)
    write_json(RESULTS / "run_summary_v1.json", report)

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if final == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
