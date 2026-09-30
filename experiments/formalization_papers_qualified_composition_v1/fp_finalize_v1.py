from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def finalize(main, audit):
    provisional = main.get("provisional_disposition")
    audit_ok = audit.get("overall") == "PASS"

    reasons = list(main.get("provisional_reasons") or [])
    if not audit_ok:
        reasons.extend(audit.get("errors") or [])

    if provisional == "INVALID":
        disposition = "INVALID"
    elif not audit_ok:
        disposition = "INVALID"
    elif provisional == "PASS_PENDING_DOCUMENTARY_AUDIT":
        disposition = "PASS"
    elif provisional == "BOUNDED_PARTIAL":
        disposition = "BOUNDED_PARTIAL"
    elif provisional == "NULL_APPLICABILITY":
        disposition = "NULL_APPLICABILITY"
    else:
        disposition = "INVALID"
        reasons.append("UNREGISTERED_PROVISIONAL_DISPOSITION")

    return disposition, sorted(set(reasons))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main-result", required=True)
    ap.add_argument("--audit-result", required=True)
    ap.add_argument("--data-open-event", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    main_path = Path(args.main_result)
    audit_path = Path(args.audit_result)
    data_open_path = Path(args.data_open_event)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    main_result = json.loads(main_path.read_text(encoding="utf-8"))
    audit_result = json.loads(audit_path.read_text(encoding="utf-8"))
    data_open = json.loads(data_open_path.read_text(encoding="utf-8"))

    disposition, reasons = finalize(main_result, audit_result)

    population = main_result.get("population") or {}
    chain_results = main_result.get("chain_results") or []

    result = {
        "study": "FORMALIZATION_PAPERS_FRESH_QUALIFIED_COMPOSITION_FINAL_V1",
        "disposition": disposition,
        "reasons": reasons,
        "data_open_event": data_open,
        "source": main_result.get("source"),
        "surface_sha256": main_result.get("surface_sha256"),
        "population_summary": {
            "root_count": population.get("root_count"),
            "complete_accounting": population.get("complete_accounting"),
            "disposition_counts": population.get("disposition_counts"),
            "eligible_chain_count": main_result.get(
                "eligible_chain_count"
            ),
        },
        "prospective_tests": {
            "chain_count": len(chain_results),
            "chain_pass_count": sum(
                bool(x.get("pass")) for x in chain_results
            ),
            "all_chain_pass": (
                all(x.get("pass") for x in chain_results)
                if chain_results
                else None
            ),
        },
        "documentary_audit": {
            "overall": audit_result.get("overall"),
            "root_set_exact": audit_result.get("root_set_exact"),
            "connected_chain_set_exact": audit_result.get(
                "connected_chain_set_exact"
            ),
            "t0_chain_set_exact": audit_result.get(
                "t0_chain_set_exact"
            ),
            "chain_pass_count": audit_result.get(
                "chain_pass_count"
            ),
        },
        "artifact_hashes": {
            "main_result_sha256": sha256_file(main_path),
            "documentary_audit_sha256": sha256_file(audit_path),
            "data_open_event_sha256": sha256_file(data_open_path),
        },
        "claim_ceiling": [
            "PASS, if obtained, is bounded to the frozen Formalization Papers v1.0 population and registered relation/trajectory grammar.",
            "No prevalence claim extends beyond the frozen graph-derived denominator.",
            "No review-text sentiment, quality, acceptance prediction, or claim-level semantic correctness is inferred.",
            "A corrected reproduction after any post-DATA_OPEN implementation defect cannot be relabeled as literal fresh confirmation.",
        ],
    }

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "study": result["study"],
        "disposition": disposition,
        "reasons": reasons,
        "population_summary": result["population_summary"],
        "prospective_tests": result["prospective_tests"],
        "documentary_audit": result["documentary_audit"],
        "artifact_hashes": result["artifact_hashes"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
