from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def all_counterfactuals_pass(qualification):
    rows = qualification.get("rows", [])
    for row in rows:
        execution = row["execution"]
        for cf in execution.get("counterfactuals", []):
            if not cf.get("pass"):
                return False
    return True


def all_sequences_pass(qualification):
    rows = qualification.get("rows", [])
    for row in rows:
        ex = row["execution"]
        if not ex.get("final_state", {}).get("published"):
            return False
        for step in ex.get("sequence", []):
            q = step.get("qualification", {})
            if not q.get("qualified"):
                return False
            if q.get("generator") != step.get("action", {}).get("generator"):
                return False
    return True


def revised_history_ablation_pass(qualification):
    revised = [
        row for row in qualification.get("rows", [])
        if row.get("disposition") == "COMPLETE_REVISED"
    ]
    if not revised:
        return False
    for row in revised:
        h = row["execution"].get("history_ablation")
        if not h or not h.get("pass"):
            return False
        if not h.get("same_current_version"):
            return False
        if not h.get("same_current_assessment"):
            return False
        if not h.get("same_current_reviews"):
            return False
        if h.get("full_qualified") is not True:
            return False
        if h.get("ablated_qualified") is not False:
            return False
    return True


def registration_history_invariance_pass(qualification):
    found = 0
    for row in qualification.get("rows", []):
        for cf in row["execution"].get("counterfactuals", []):
            if cf.get("type") == "REGISTRATION_HISTORY_ABLATION":
                found += 1
                if not cf.get("pass"):
                    return False
    return found > 0


def exact_source_accounting(source_accounting, mode):
    if not source_accounting.get("accounting_exact"):
        return False
    if mode == "authoritative":
        return all([
            source_accounting.get("file_count") == 568,
            source_accounting.get("total_bytes") == 96584062,
            source_accounting.get("expected_file_count") == 568,
            source_accounting.get("expected_total_bytes") == 96584062,
        ])
    return True


def parser_gate(parser, population):
    return all([
        parser.get("unresolved_count", 0) == 0,
        (
            parser.get("exact_count", 0)
            + parser.get("parse_error_count", 0)
            == population.get("total_files", -1)
        ),
    ])


def coverage_gate(coverage, mode):
    if mode == "synthetic":
        return coverage.get("registered_all_covered") is True
    return True


def artifact_manifest(output_dir: Path, exclude=None):
    exclude = set(exclude or [])
    files = {}
    for path in sorted(output_dir.glob("*.json")):
        if path.name in exclude:
            continue
        files[path.name] = sha256(path.read_bytes())
    return {
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--documentary-audit", required=True)
    ap.add_argument(
        "--mode", required=True, choices=["synthetic", "authoritative"]
    )
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    d = Path(args.input_dir)
    source = load_json(d / "source_accounting_v1.json")
    parser = load_json(d / "parser_comparison_v1.json")
    population = load_json(d / "population_results_v1.json")
    qualification = load_json(d / "qualification_results_v1.json")
    coverage = load_json(d / "coverage_observed_v1.json")
    run_summary = load_json(d / "run_summary_v1.json")
    documentary = load_json(Path(args.documentary_audit))

    gates = {
        "source_accounting": exact_source_accounting(source, args.mode),
        "parser_independent_engine": parser_gate(parser, population),
        "population_accounting": (
            sum(population.get("disposition_counts", {}).values())
            == population.get("total_files")
        ),
        "qualification_sequences": all_sequences_pass(qualification),
        "counterfactuals": all_counterfactuals_pass(qualification),
        "registration_history_invariance": (
            registration_history_invariance_pass(qualification)
        ),
        "coverage": coverage_gate(coverage, args.mode),
        "documentary_audit": (
            documentary.get("all_pass") is True
            and documentary.get("audited_count")
            == population.get("complete_count")
        ),
    }

    if args.mode == "synthetic":
        gates.update({
            "synthetic_expected_population": (
                population.get("disposition_counts")
                == {
                    "COMPLETE_REVISED": 2,
                    "COMPLETE_V1": 3,
                    "INVALID_CURRENT_EVALUATION_BINDING": 7,
                    "INVALID_IDENTITY": 2,
                    "INVALID_PRIOR_HISTORY": 5,
                    "PARSE_ERROR": 1,
                }
            ),
            "synthetic_revised_history_ablation": (
                revised_history_ablation_pass(qualification)
            ),
            "synthetic_complete_count": (
                population.get("complete_count") == 5
            ),
        })
        final_disposition = (
            "SYNTHETIC_EXACT_PATH_FINAL_PASS"
            if all(gates.values())
            else "SYNTHETIC_EXACT_PATH_FINAL_FAIL"
        )

    else:
        gates.update({
            "authoritative_file_count": (
                population.get("total_files") == 568
            ),
            "has_complete_revised": (
                population.get("complete_revised_count", 0) > 0
            ),
            "revised_history_ablation": (
                revised_history_ablation_pass(qualification)
                if population.get("complete_revised_count", 0) > 0
                else False
            ),
            "no_oracle_runtime_unresolved": (
                population.get("disposition_counts", {}).get(
                    "ORACLE_RUNTIME_UNRESOLVED", 0
                ) == 0
            ),
            "no_parse_error": (
                population.get("disposition_counts", {}).get(
                    "PARSE_ERROR", 0
                ) == 0
            ),
        })

        implementation_invalid = not all([
            gates["source_accounting"],
            gates["parser_independent_engine"],
            gates["population_accounting"],
            gates["coverage"],
            gates["no_oracle_runtime_unresolved"],
            gates["no_parse_error"],
        ])

        if implementation_invalid:
            final_disposition = "INVALID"
        elif population.get("complete_count", 0) == 0:
            final_disposition = "NULL_APPLICABILITY"
        elif population.get("complete_revised_count", 0) == 0:
            final_disposition = "BOUNDED_PARTIAL"
        elif all(gates.values()):
            final_disposition = "PASS"
        else:
            final_disposition = "BOUNDED_PARTIAL"

    result = {
        "study": "ELIFE_CLEAN_PROSPECTIVE_CONFIRMATION_FINAL_V1",
        "mode": args.mode,
        "runner_computational_disposition": run_summary.get(
            "computational_disposition"
        ),
        "population": population,
        "documentary_audit_summary": {
            "audited_count": documentary.get("audited_count"),
            "pass_count": documentary.get("pass_count"),
            "fail_count": documentary.get("fail_count"),
            "all_pass": documentary.get("all_pass"),
        },
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "final_disposition": final_disposition,
        "claim_ceiling": [
            "This finalizer applies only to the frozen eLife typed-generator protocol.",
            "Natural INVALID_* source structures remain in complete population accounting and are not silently dropped.",
            "A PASS does not license claims about review text semantics or causal scientific revision.",
        ],
    }
    out = Path(args.output)
    write_json(out, result)

    manifest = artifact_manifest(
        d,
        exclude={"artifact_manifest_v1.json"},
    )
    manifest["files"][out.name] = sha256(out.read_bytes())
    manifest["files"][Path(args.documentary_audit).name] = sha256(
        Path(args.documentary_audit).read_bytes()
    )
    write_json(d / "artifact_manifest_v1.json", manifest)

    print(json.dumps({
        "study": result["study"],
        "mode": args.mode,
        "gates": gates,
        "final_disposition": final_disposition,
    }, ensure_ascii=False, indent=2))

    if args.mode == "synthetic":
        if final_disposition != "SYNTHETIC_EXACT_PATH_FINAL_PASS":
            raise SystemExit(2)
    elif final_disposition == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
