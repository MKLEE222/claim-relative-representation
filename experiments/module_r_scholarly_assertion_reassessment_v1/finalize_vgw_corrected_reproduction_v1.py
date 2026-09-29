from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "vgw_corrected_reproduction_v1"

AUTH = RESULTS / "authoritative_results_v1.json"
AUDIT = RESULTS / "documentary_audit_v1.json"
DIST = RESULTS / "distribution_manifest_v1.json"
SOURCE_ID = RESULTS / "source_identity_check_v1.json"
MARKER = RESULTS / "CORRECTED_REPRO_OPEN_EVENT_v1.json"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    auth = load(AUTH)
    audit = load(AUDIT)
    dist = load(DIST)
    source_id = load(SOURCE_ID)
    marker = load(MARKER)

    substantive = int(auth["population"]["substantive_candidates"])
    nulls = int(auth["population"]["admissible_null_events"])

    integrity = {
        "corrected_marker_present": marker.get("event") == "CORRECTED_REPRO_OPEN_EVENT",
        "same_source_bytes_as_first_open": bool(source_id["same_source_bytes_as_first_open"]),
        "distribution_manifest_complete": bool(dist.get("complete")),
        "oracle_runtime_extraction_exact": bool(auth["oracle_runtime_extraction_exact"]),
        "no_execution_failures": len(auth["execution_failure_manifest"]) == 0,
        "documentary_audit_complete": int(audit["audited_count"]) == substantive,
        "documentary_audit_pass": bool(audit["all_substantive_audits_pass"]),
    }

    if not all(integrity.values()):
        disposition = "CORRECTED_REPRODUCTION_INVALID"
    elif substantive > 0:
        disposition = "CORRECTED_REPRODUCTION_PASS"
    elif nulls > 0:
        disposition = "CORRECTED_REPRODUCTION_NULL_REASSESSMENT"
    else:
        disposition = "CORRECTED_REPRODUCTION_NULL_APPLICABILITY"

    report = {
        "study": "MODULE_R_VGW_CORRECTED_REPRODUCTION_V1",
        "scientific_status": "POSTFRESH_CORRECTED_REPRODUCTION_ONLY",
        "authoritative_fresh_run": 36553853190,
        "authoritative_fresh_disposition": "INVALID",
        "final_disposition": disposition,
        "integrity": integrity,
        "population": auth["population"],
        "source_manifest_sha256": auth["source_manifest_sha256"],
        "documentary_audit": {
            "substantive_candidate_count": audit["substantive_candidate_count"],
            "audited_count": audit["audited_count"],
            "all_substantive_audits_pass": audit["all_substantive_audits_pass"],
        },
        "hashes": {
            "authoritative_results_sha256": sha256(AUTH.read_bytes()),
            "documentary_audit_sha256": sha256(AUDIT.read_bytes()),
            "distribution_manifest_sha256": sha256(DIST.read_bytes()),
        },
        "claim_ceiling": [
            "This run verifies the frozen scientific analysis after a lexer-only correction.",
            "It does not retroactively convert the first fresh INVALID into a fresh PASS.",
            "It can establish whether the scientific outcome is stable on the exact same source bytes.",
        ],
    }
    (RESULTS / "FINAL_CORRECTED_RESULT_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if disposition == "CORRECTED_REPRODUCTION_INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
