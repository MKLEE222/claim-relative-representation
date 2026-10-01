from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

import elife_constants as C
import elife_oracle
import elife_runtime

HERE = Path(__file__).resolve().parent
SOURCE_MANIFEST = HERE / "ELIFE_SOURCE_MANIFEST_v1.json"
SYNTH_EXPECTED = HERE / "ELIFE_SYNTHETIC_EXPECTED_v1.json"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def normalized_exception(exc: Exception):
    return {
        "type": type(exc).__name__,
    }


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_files(source: Path):
    return sorted(
        [p for p in source.rglob("*.xml") if p.is_file()],
        key=lambda p: str(p.relative_to(source)),
    )


def expected_manifest():
    return load_json(SOURCE_MANIFEST)


def observed_source_accounting(source: Path, mode: str):
    files = source_files(source)
    rows = []
    for p in files:
        raw = p.read_bytes()
        rel = str(p.relative_to(source)).replace("\\", "/")
        rows.append({
            "path": rel,
            "name": p.name,
            "size": len(raw),
            "sha256": sha256(raw),
        })

    result = {
        "mode": mode,
        "file_count": len(rows),
        "total_bytes": sum(x["size"] for x in rows),
        "files": rows,
    }

    if mode == "authoritative":
        manifest = expected_manifest()
        expected = {
            x["path"]: x for x in manifest["files"]
        }
        observed = {x["path"]: x for x in rows}
        result["expected_file_count"] = manifest["expected_xml_files"]
        result["expected_total_bytes"] = manifest["expected_total_bytes"]
        result["path_set_exact"] = set(observed) == set(expected)
        result["sizes_exact"] = (
            result["path_set_exact"]
            and all(
                observed[p]["size"] == expected[p]["size"]
                for p in expected
            )
        )
        result["accounting_exact"] = all([
            result["file_count"] == manifest["expected_xml_files"],
            result["total_bytes"] == manifest["expected_total_bytes"],
            result["path_set_exact"],
            result["sizes_exact"],
        ])
    else:
        result["accounting_exact"] = True

    return result


def _engine_case(engine, relpath: str, raw: bytes):
    surface = engine.parse_xml(relpath, raw)
    evaluation = engine.evaluate_surface(surface)
    return {
        "surface": surface,
        "evaluation": evaluation,
    }


def compare_parse(relpath: str, raw: bytes):
    o_exc = None
    r_exc = None
    o = None
    r = None

    try:
        o = _engine_case(elife_oracle, relpath, raw)
    except Exception as exc:
        o_exc = exc

    try:
        r = _engine_case(elife_runtime, relpath, raw)
    except Exception as exc:
        r_exc = exc

    if o_exc is not None and r_exc is not None:
        return {
            "status": "BOTH_PARSE_ERROR",
            "disposition": "PARSE_ERROR",
            "oracle_error": normalized_exception(o_exc),
            "runtime_error": normalized_exception(r_exc),
            "traces": ["PARSE_ERROR"],
        }

    if (o_exc is None) != (r_exc is None):
        return {
            "status": "ENGINE_PARSE_DISAGREEMENT",
            "disposition": "ORACLE_RUNTIME_UNRESOLVED",
            "oracle_error": (
                None if o_exc is None else normalized_exception(o_exc)
            ),
            "runtime_error": (
                None if r_exc is None else normalized_exception(r_exc)
            ),
            "traces": [],
        }

    if o["surface"] != r["surface"]:
        return {
            "status": "SURFACE_DISAGREEMENT",
            "disposition": "ORACLE_RUNTIME_UNRESOLVED",
            "oracle_surface": o["surface"],
            "runtime_surface": r["surface"],
            "traces": sorted(set(
                o["surface"].get("traces", [])
                + r["surface"].get("traces", [])
            )),
        }

    if o["evaluation"] != r["evaluation"]:
        return {
            "status": "EVALUATION_DISAGREEMENT",
            "disposition": "ORACLE_RUNTIME_UNRESOLVED",
            "surface": o["surface"],
            "oracle_evaluation": o["evaluation"],
            "runtime_evaluation": r["evaluation"],
            "traces": sorted(set(
                o["evaluation"].get("traces", [])
                + r["evaluation"].get("traces", [])
            )),
        }

    return {
        "status": "EXACT",
        "disposition": o["evaluation"]["disposition"],
        "surface": o["surface"],
        "evaluation": o["evaluation"],
        "traces": o["evaluation"]["traces"],
    }


def _qualify_pair(state, action):
    o = elife_oracle.qualify_action(state, action)
    r = elife_runtime.qualify_action(state, action)
    if o != r:
        raise AssertionError({
            "kind": "QUALIFICATION_DISAGREEMENT",
            "state": state,
            "action": action,
            "oracle": o,
            "runtime": r,
        })
    return o


def _apply_pair(state, action):
    o = elife_oracle.apply_action(state, action)
    r = elife_runtime.apply_action(state, action)
    if o != r:
        raise AssertionError({
            "kind": "ACTION_EXECUTION_DISAGREEMENT",
            "state": state,
            "action": action,
            "oracle": o,
            "runtime": r,
        })
    return o


def _trace_for_qualified_generator(generator: str):
    return {
        "REGISTER_PUBLIC_REVIEW": "QUALIFY_REGISTER_PUBLIC_REVIEW",
        "REGISTER_ASSESSMENT": "QUALIFY_REGISTER_ASSESSMENT",
        "REGISTER_AUTHOR_RESPONSE": "QUALIFY_REGISTER_AUTHOR_RESPONSE",
        "PUBLISH_REVIEWED_PREPRINT": "QUALIFY_PUBLISH_V1",
        "PUBLISH_REVISED_REVIEWED_PREPRINT": "QUALIFY_PUBLISH_REVISED",
    }[generator]


def execute_complete_case(surface: dict):
    traces = set()
    actions_o = elife_oracle.actions_for_surface(surface)
    actions_r = elife_runtime.actions_for_surface(surface)
    if actions_o != actions_r:
        raise AssertionError({
            "kind": "ACTION_CONSTRUCTION_DISAGREEMENT",
            "oracle": actions_o,
            "runtime": actions_r,
        })
    actions = actions_o

    state_o = elife_oracle.initial_state(surface, include_current=False)
    state_r = elife_runtime.initial_state(surface, include_current=False)
    if state_o != state_r:
        raise AssertionError("INITIAL_STATE_DISAGREEMENT")
    state = state_o

    sequence = []
    for action in actions:
        result = _apply_pair(state, action)
        q = result["qualification"]
        if not q["qualified"] or q["generator"] != action["generator"]:
            raise AssertionError({
                "kind": "NATURAL_ACTION_NOT_QUALIFIED",
                "action": action,
                "qualification": q,
            })
        traces.add(_trace_for_qualified_generator(action["generator"]))
        sequence.append({
            "action": action,
            "qualification": q,
        })
        state = result["state"]

    if not state.get("published"):
        raise AssertionError("SEQUENCE_DID_NOT_PUBLISH")
    traces.add("SEQUENCE_CLOSURE_PASS")

    full_state_o = elife_oracle.initial_state(
        surface, include_current=True
    )
    full_state_r = elife_runtime.initial_state(
        surface, include_current=True
    )
    if full_state_o != full_state_r:
        raise AssertionError("FULL_STATE_DISAGREEMENT")
    full_state = full_state_o

    publication = actions[-1]
    pub_q = _qualify_pair(full_state, publication)
    if not pub_q["qualified"]:
        raise AssertionError({
            "kind": "FULL_PUBLICATION_NOT_QUALIFIED",
            "qualification": pub_q,
        })

    counterfactuals = []

    registrations = [
        a for a in actions
        if a["generator"].startswith("REGISTER_")
    ]
    for action in registrations:
        wrong_target = copy.deepcopy(action)
        wrong_target["target_version_doi"] = (
            str(action["target_version_doi"]) + ".WRONG"
        )
        q = _qualify_pair(
            elife_oracle.initial_state(surface, include_current=False),
            wrong_target,
        )
        if q["qualified"]:
            raise AssertionError("WRONG_TARGET_ACCEPTED")
        traces.add("REJECT_WRONG_TARGET")
        counterfactuals.append({
            "type": "WRONG_TARGET",
            "generator": action["generator"],
            "pass": True,
            "reason": q["reason"],
        })

        wrong_binding = copy.deepcopy(action)
        wrong_binding["evaluation_doi"] = (
            "10.7554/eLife.999999.9.sa999"
        )
        q = _qualify_pair(
            elife_oracle.initial_state(surface, include_current=False),
            wrong_binding,
        )
        if q["qualified"]:
            raise AssertionError("WRONG_EVALUATION_BINDING_ACCEPTED")
        traces.add("REJECT_WRONG_EVALUATION_BINDING")
        counterfactuals.append({
            "type": "WRONG_EVALUATION_BINDING",
            "generator": action["generator"],
            "pass": True,
            "reason": q["reason"],
        })

        hist_ablated = elife_oracle.initial_state(
            surface, include_current=False
        )
        hist_ablated["prior_events"] = []
        q = _qualify_pair(hist_ablated, action)
        if not q["qualified"] or q["generator"] != action["generator"]:
            raise AssertionError({
                "kind": "REGISTRATION_HISTORY_ABLATION_CHANGED",
                "action": action,
                "qualification": q,
            })
        traces.add("HISTORY_ABLATION_REGISTRATION_INVARIANT")
        counterfactuals.append({
            "type": "REGISTRATION_HISTORY_ABLATION",
            "generator": action["generator"],
            "pass": True,
        })

    missing_assessment = copy.deepcopy(full_state)
    missing_assessment["current_assessment_dois"] = []
    q = _qualify_pair(missing_assessment, publication)
    if q["qualified"]:
        raise AssertionError("MISSING_CURRENT_ASSESSMENT_ACCEPTED")
    traces.add("REJECT_MISSING_CURRENT_ASSESSMENT")
    counterfactuals.append({
        "type": "MISSING_CURRENT_ASSESSMENT",
        "pass": True,
        "reason": q["reason"],
    })

    missing_reviews = copy.deepcopy(full_state)
    missing_reviews["current_review_dois"] = []
    q = _qualify_pair(missing_reviews, publication)
    if q["qualified"]:
        raise AssertionError("MISSING_CURRENT_REVIEWS_ACCEPTED")
    traces.add("REJECT_MISSING_CURRENT_REVIEWS")
    counterfactuals.append({
        "type": "MISSING_CURRENT_REVIEWS",
        "pass": True,
        "reason": q["reason"],
    })

    history_ablation = None
    if publication["generator"] == "PUBLISH_REVISED_REVIEWED_PREPRINT":
        no_history = copy.deepcopy(full_state)
        no_history["prior_events"] = []
        q = _qualify_pair(no_history, publication)
        if q["qualified"]:
            raise AssertionError("REVISED_PUBLICATION_WITHOUT_HISTORY_ACCEPTED")
        traces.add("REJECT_MISSING_PRIOR_HISTORY")
        traces.add("HISTORY_ABLATION_REVISED_PUBLICATION_REJECTED")
        history_ablation = {
            "same_current_version": (
                no_history["version_doi"] == full_state["version_doi"]
            ),
            "same_current_assessment": (
                no_history["current_assessment_dois"]
                == full_state["current_assessment_dois"]
            ),
            "same_current_reviews": (
                no_history["current_review_dois"]
                == full_state["current_review_dois"]
            ),
            "full_qualified": pub_q["qualified"],
            "ablated_qualified": q["qualified"],
            "ablated_reason": q["reason"],
            "pass": True,
        }
        counterfactuals.append({
            "type": "REVISED_HISTORY_ABLATION",
            **history_ablation,
        })

        bad_history = copy.deepcopy(full_state)
        first = copy.deepcopy(bad_history["prior_events"][0])
        first["reviewed_preprint_dois"] = [
            C.expected_version_doi(
                state["manuscript_id"], state["rp_version"] + 7
            )
        ]
        bad_history["prior_events"][0] = first
        q = _qualify_pair(bad_history, publication)
        if q["qualified"]:
            raise AssertionError("BAD_PRIOR_HISTORY_ACCEPTED")
        traces.add("REJECT_BAD_PRIOR_HISTORY")
        counterfactuals.append({
            "type": "BAD_PRIOR_HISTORY",
            "pass": True,
            "reason": q["reason"],
        })

    return {
        "sequence": sequence,
        "final_state": state,
        "publication_qualification": pub_q,
        "counterfactuals": counterfactuals,
        "history_ablation": history_ablation,
        "traces": sorted(traces),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument(
        "--mode", required=True, choices=["synthetic", "authoritative"]
    )
    ap.add_argument("--coverage-manifest")
    args = ap.parse_args()

    source = Path(args.source).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    accounting = observed_source_accounting(source, args.mode)
    write_json(out / "source_accounting_v1.json", accounting)
    if not accounting["accounting_exact"]:
        raise SystemExit("SOURCE_ACCOUNTING_MISMATCH")

    parse_rows = []
    qualification_rows = []
    dispositions = Counter()
    observed_traces = set()
    action_denominators = Counter()

    for p in source_files(source):
        rel = str(p.relative_to(source)).replace("\\", "/")
        raw = p.read_bytes()
        row = compare_parse(rel, raw)
        dispositions[row["disposition"]] += 1
        observed_traces.update(row.get("traces", []))

        parse_row = {
            "path": rel,
            "size": len(raw),
            "sha256": sha256(raw),
            "status": row["status"],
            "disposition": row["disposition"],
        }
        if row["status"] != "EXACT":
            parse_row["detail"] = {
                k: v for k, v in row.items()
                if k not in {
                    "status", "disposition", "traces"
                }
            }
        parse_rows.append(parse_row)

        if row["disposition"] in {"COMPLETE_V1", "COMPLETE_REVISED"}:
            execution = execute_complete_case(row["surface"])
            observed_traces.update(execution["traces"])
            for seq in execution["sequence"]:
                action_denominators[seq["action"]["generator"]] += 1
            qualification_rows.append({
                "path": rel,
                "disposition": row["disposition"],
                "surface": row["surface"],
                "execution": execution,
            })

    write_json(out / "parser_comparison_v1.json", {
        "rows": parse_rows,
        "exact_count": sum(x["status"] == "EXACT" for x in parse_rows),
        "parse_error_count": dispositions["PARSE_ERROR"],
        "unresolved_count": dispositions["ORACLE_RUNTIME_UNRESOLVED"],
    })

    population = {
        "mode": args.mode,
        "total_files": sum(dispositions.values()),
        "disposition_counts": dict(sorted(dispositions.items())),
        "complete_count": (
            dispositions["COMPLETE_V1"]
            + dispositions["COMPLETE_REVISED"]
        ),
        "complete_revised_count": dispositions["COMPLETE_REVISED"],
        "action_denominators": dict(sorted(action_denominators.items())),
    }
    write_json(out / "population_results_v1.json", population)
    write_json(out / "qualification_results_v1.json", {
        "rows": qualification_rows,
    })

    if args.mode == "synthetic":
        expected = load_json(SYNTH_EXPECTED)
        observed_by_name = {
            Path(x["path"]).name: x["disposition"]
            for x in parse_rows
        }
        if observed_by_name != expected["dispositions"]:
            write_json(out / "synthetic_expected_mismatch_v1.json", {
                "expected": expected["dispositions"],
                "observed": observed_by_name,
            })
            raise SystemExit("SYNTHETIC_DISPOSITION_MISMATCH")

        expected_counts = expected["expected_counts"]
        observed_counts = {
            key: dispositions[key] for key in expected_counts
        }
        if observed_counts != expected_counts:
            raise SystemExit("SYNTHETIC_COUNT_MISMATCH")

        missing_coverage = sorted(C.TRACE_REGISTRY - observed_traces)
        if missing_coverage:
            write_json(out / "synthetic_coverage_failure_v1.json", {
                "registered": sorted(C.TRACE_REGISTRY),
                "observed": sorted(observed_traces),
                "missing": missing_coverage,
            })
            raise SystemExit("SYNTHETIC_COVERAGE_INCOMPLETE")

    else:
        if not args.coverage_manifest:
            raise SystemExit("AUTHORITATIVE_COVERAGE_MANIFEST_REQUIRED")
        coverage = load_json(Path(args.coverage_manifest))
        covered = set(coverage["covered_traces"])
        unexpected = sorted(observed_traces - covered)
        if unexpected:
            write_json(out / "uncovered_natural_surface_v1.json", {
                "covered_traces": sorted(covered),
                "natural_traces": sorted(observed_traces),
                "unexpected": unexpected,
            })
            raise SystemExit("INVALID_UNCOVERED_EXECUTION_SURFACE")

    coverage_result = {
        "mode": args.mode,
        "registered_traces": sorted(C.TRACE_REGISTRY),
        "covered_traces": sorted(observed_traces),
        "registered_all_covered": (
            C.TRACE_REGISTRY.issubset(observed_traces)
            if args.mode == "synthetic"
            else None
        ),
    }
    write_json(out / "coverage_observed_v1.json", coverage_result)

    invalid_engine = dispositions["ORACLE_RUNTIME_UNRESOLVED"] > 0
    has_parse_errors = dispositions["PARSE_ERROR"] > 0

    if args.mode == "synthetic":
        disposition = "SYNTHETIC_EXACT_PATH_PASS"
    elif invalid_engine or has_parse_errors:
        disposition = "INVALID"
    elif population["complete_count"] == 0:
        disposition = "NULL_APPLICABILITY"
    elif population["complete_revised_count"] == 0:
        disposition = "BOUNDED_PARTIAL"
    else:
        disposition = "COMPUTATIONAL_PASS_PENDING_DOCUMENTARY_AUDIT"

    summary = {
        "study": "ELIFE_CLEAN_PROSPECTIVE_CONFIRMATION_V1",
        "mode": args.mode,
        "source_accounting_exact": accounting["accounting_exact"],
        "population": population,
        "trace_count": len(observed_traces),
        "computational_disposition": disposition,
    }
    write_json(out / "run_summary_v1.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.mode == "authoritative" and disposition == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
