from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fp_finalize_v1


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def corrected_label(scientific_disposition):
    mapping = {
        "PASS": "POST_FRESH_CORRECTED_REPRODUCTION_PASS",
        "BOUNDED_PARTIAL": (
            "POST_FRESH_CORRECTED_REPRODUCTION_BOUNDED_PARTIAL"
        ),
        "NULL_APPLICABILITY": (
            "POST_FRESH_CORRECTED_REPRODUCTION_NULL_APPLICABILITY"
        ),
        "INVALID": "POST_FRESH_CORRECTED_REPRODUCTION_INVALID",
    }
    return mapping.get(
        scientific_disposition,
        "POST_FRESH_CORRECTED_REPRODUCTION_INVALID",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main-result", required=True)
    ap.add_argument("--audit-result", required=True)
    ap.add_argument("--diagnostic-result", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    main_path = Path(args.main_result)
    audit_path = Path(args.audit_result)
    diagnostic_path = Path(args.diagnostic_result)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    main = json.loads(main_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    diagnostic = json.loads(
        diagnostic_path.read_text(encoding="utf-8")
    )

    scientific_disposition, reasons = fp_finalize_v1.finalize(
        main, audit
    )

    real_parser_exact = (
        diagnostic.get("file_count") == 10
        and diagnostic.get("exact_file_count") == 10
        and not diagnostic.get("mismatch_component_file_counts")
    )
    if not real_parser_exact:
        scientific_disposition = "INVALID"
        reasons = sorted(set(
            list(reasons)
            + ["POSTFRESH_REAL_SOURCE_PARSER_GATE_NOT_EXACT"]
        ))

    result = {
        "study": (
            "FORMALIZATION_PAPERS_CORRECTED_REPRODUCTION_FINAL_V1"
        ),
        "authoritative_fresh_disposition": "INVALID",
        "authoritative_fresh_run": 36657856767,
        "freshness_restored": False,
        "scientific_disposition_under_corrected_execution": (
            scientific_disposition
        ),
        "corrected_disposition": corrected_label(
            scientific_disposition
        ),
        "reasons": reasons,
        "source_archive_sha256": (
            main.get("source", {}).get("archive_sha256")
        ),
        "real_source_parser_exact": real_parser_exact,
        "diagnostic": {
            "file_count": diagnostic.get("file_count"),
            "exact_file_count": diagnostic.get(
                "exact_file_count"
            ),
            "mismatch_component_file_counts": diagnostic.get(
                "mismatch_component_file_counts"
            ),
        },
        "population": {
            "root_count": (
                (main.get("population") or {}).get("root_count")
            ),
            "disposition_counts": (
                (main.get("population") or {}).get(
                    "disposition_counts"
                )
            ),
            "eligible_chain_count": main.get(
                "eligible_chain_count"
            ),
        },
        "prospective_tests": {
            "chain_count": len(
                main.get("chain_results") or []
            ),
            "chain_pass_count": sum(
                bool(x.get("pass"))
                for x in (main.get("chain_results") or [])
            ),
        },
        "documentary_audit": {
            "overall": audit.get("overall"),
            "root_set_exact": audit.get("root_set_exact"),
            "connected_chain_set_exact": audit.get(
                "connected_chain_set_exact"
            ),
            "t0_chain_set_exact": audit.get(
                "t0_chain_set_exact"
            ),
            "chain_pass_count": audit.get(
                "chain_pass_count"
            ),
        },
        "hashes": {
            "main_result_sha256": sha256_file(main_path),
            "documentary_audit_sha256": sha256_file(audit_path),
            "parser_diagnostic_sha256": sha256_file(
                diagnostic_path
            ),
        },
        "claim_ceiling": [
            (
                "The authoritative fresh run remains INVALID and "
                "is not replaced by this result."
            ),
            (
                "A PASS here is post-fresh corrected reproduction "
                "on byte-identical first-opening source only."
            ),
        ],
    }

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
