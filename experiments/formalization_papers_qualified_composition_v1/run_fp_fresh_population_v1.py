from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_oracle
import fp_runtime
import fp_population


def canonical_json(obj):
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def invoke(engine, state, event):
    fn = getattr(engine, "apply", None)
    if fn is None:
        fn = getattr(engine, "execute")
    return fn(state, event)


def normalize_result(result):
    return json.loads(canonical_json(result))


def exact_engine_step(state, event):
    o = invoke(fp_oracle, state, event)
    r = invoke(fp_runtime, state, event)
    exact = normalize_result(o) == normalize_result(r)
    return o, r, exact


def events_for_chain(chain):
    review = {
        "kind": "REVIEW",
        "review_np": chain["review_np"],
        "target_formalization": chain["root"],
    }
    update = {
        "kind": "UPDATE",
        "update_np": chain["update_np"],
        "target_root": chain["root"],
    }
    response = {
        "kind": "RESPONSE",
        "response_np": chain["response_np"],
        "target_review_np": chain["review_np"],
        "target_update_np": chain["update_np"],
    }
    decision = None
    if chain.get("decision_np"):
        decision = {
            "kind": "DECISION",
            "decision_np": chain["decision_np"],
            "target_update_np": chain["update_np"],
            "status": chain["decision_status"],
        }
    return review, update, response, decision


def foreign_candidate(population, root, field):
    candidates = []
    for row in population["roots"]:
        if row["root"] == root:
            continue
        if row["disposition"].startswith((
            "T8_", "T9_"
        )):
            continue
        candidates.extend(row.get(field, []))
    return sorted(set(candidates))[0] if candidates else None


def execute_chain(chain, population, version):
    review, update, response, decision = events_for_chain(chain)
    s0 = fp_oracle.initial_state(
        chain["root"], chain["submission_np"]
    )
    r0 = fp_runtime.initial_state(
        chain["root"], chain["submission_np"]
    )
    engine_exact = s0 == r0
    errors = []

    o_review, r_review, exact = exact_engine_step(s0, review)
    engine_exact = engine_exact and exact
    if not exact:
        errors.append("ENGINE_DISAGREEMENT_REVIEW")
    if not o_review["qualified"]:
        errors.append("FORWARD_REVIEW_REJECTED")

    o_update, r_update, exact = exact_engine_step(
        o_review["state"], update
    )
    engine_exact = engine_exact and exact
    if not exact:
        errors.append("ENGINE_DISAGREEMENT_UPDATE")
    if not o_update["qualified"]:
        errors.append("FORWARD_UPDATE_REJECTED")

    state_before_response = o_update["state"]
    o_response, r_response, exact = exact_engine_step(
        state_before_response, response
    )
    engine_exact = engine_exact and exact
    if not exact:
        errors.append("ENGINE_DISAGREEMENT_RESPONSE")
    if not o_response["qualified"]:
        errors.append("FORWARD_RESPONSE_REJECTED")

    forward_generators = [
        o_review.get("generator"),
        o_update.get("generator"),
        o_response.get("generator"),
    ]

    final_state = o_response["state"]
    o_decision = None
    if decision is not None:
        o_decision, r_decision, exact = exact_engine_step(
            final_state, decision
        )
        engine_exact = engine_exact and exact
        if not exact:
            errors.append("ENGINE_DISAGREEMENT_DECISION")
        if not o_decision["qualified"]:
            errors.append("FORWARD_DECISION_REJECTED")
        forward_generators.append(o_decision.get("generator"))
        final_state = o_decision["state"]

    # P2 response before review.
    p2_o, p2_r, p2_exact = exact_engine_step(s0, response)
    p2 = (
        p2_exact
        and not p2_o["qualified"]
        and p2_o["reason"] == "RESPONSE_REVIEW_TARGET_NOT_LIVE"
    )
    if not p2:
        errors.append("P2_RESPONSE_BEFORE_REVIEW_FAILED")

    # P3 response after review but before update.
    p3_o, p3_r, p3_exact = exact_engine_step(
        o_review["state"], response
    )
    p3 = (
        p3_exact
        and not p3_o["qualified"]
        and p3_o["reason"] == "RESPONSE_UPDATE_TARGET_NOT_LIVE"
    )
    if not p3:
        errors.append("P3_RESPONSE_BEFORE_UPDATE_FAILED")

    # P4 same current update, history removed only.
    ablated = copy.deepcopy(state_before_response)
    current_projection_before = {
        "current_formalization": state_before_response[
            "current_formalization"
        ],
        "current_update_np": state_before_response["current_update_np"],
        "publication_status": state_before_response[
            "publication_status"
        ],
    }
    ablated["history"] = []
    current_projection_after = {
        "current_formalization": ablated["current_formalization"],
        "current_update_np": ablated["current_update_np"],
        "publication_status": ablated["publication_status"],
    }
    p4_o, p4_r, p4_exact = exact_engine_step(ablated, response)
    p4 = (
        p4_exact
        and current_projection_before == current_projection_after
        and not p4_o["qualified"]
        and p4_o["reason"] == "RESPONSE_TARGET_HISTORY_UNRESOLVED"
    )
    if not p4:
        errors.append("P4_HISTORY_ABLATION_FAILED")

    # P5 decision before update, T0 only.
    if decision is not None:
        p5_o, p5_r, p5_exact = exact_engine_step(s0, decision)
        p5 = (
            p5_exact
            and not p5_o["qualified"]
            and p5_o["reason"] == "DECISION_TARGET_NOT_CURRENT"
        )
        if not p5:
            errors.append("P5_DECISION_BEFORE_UPDATE_FAILED")
    else:
        p5 = None

    # P6 deterministic foreign-root injections.
    foreign_review = foreign_candidate(
        population, chain["root"], "live_reviews"
    )
    if foreign_review is None:
        wrong_review = {
            "status": "STRUCTURALLY_UNAVAILABLE",
            "pass": None,
        }
    else:
        ev = copy.deepcopy(response)
        ev["target_review_np"] = foreign_review
        wr_o, wr_r, wr_exact = exact_engine_step(
            state_before_response, ev
        )
        ok = wr_exact and not wr_o["qualified"]
        wrong_review = {
            "status": "EXECUTED",
            "candidate": foreign_review,
            "pass": ok,
            "reason": wr_o.get("reason"),
        }
        if not ok:
            errors.append("P6_WRONG_REVIEW_TARGET_FAILED")

    foreign_update = foreign_candidate(
        population, chain["root"], "live_updates"
    )
    if foreign_update is None:
        wrong_update = {
            "status": "STRUCTURALLY_UNAVAILABLE",
            "pass": None,
        }
    else:
        ev = copy.deepcopy(response)
        ev["target_update_np"] = foreign_update
        wu_o, wu_r, wu_exact = exact_engine_step(
            state_before_response, ev
        )
        ok = wu_exact and not wu_o["qualified"]
        wrong_update = {
            "status": "EXECUTED",
            "candidate": foreign_update,
            "pass": ok,
            "reason": wu_o.get("reason"),
        }
        if not ok:
            errors.append("P6_WRONG_UPDATE_TARGET_FAILED")

    # P7: every exact package used in the chain is a live terminal.
    chain_packages = [
        chain["submission_np"],
        chain["review_np"],
        chain["update_np"],
        chain["response_np"],
    ]
    if chain.get("decision_np"):
        chain_packages.append(chain["decision_np"])
    live = set(version["live_packages"])
    p7 = all(x in live for x in chain_packages)
    if not p7:
        errors.append("P7_CHAIN_CONTAINS_NONLIVE_PACKAGE")

    return {
        "chain": chain,
        "forward": {
            "generators": forward_generators,
            "engine_exact": engine_exact,
            "final_state": final_state,
        },
        "counterfactuals": {
            "P2_response_before_review": {
                "pass": p2,
                "reason": p2_o.get("reason"),
            },
            "P3_response_before_update": {
                "pass": p3,
                "reason": p3_o.get("reason"),
            },
            "P4_history_ablation": {
                "pass": p4,
                "current_projection_equal": (
                    current_projection_before
                    == current_projection_after
                ),
                "reason": p4_o.get("reason"),
            },
            "P5_decision_before_update": (
                {
                    "pass": p5,
                    "reason": p5_o.get("reason"),
                }
                if decision is not None
                else {"status": "NOT_APPLICABLE", "pass": None}
            ),
            "P6_wrong_review_target": wrong_review,
            "P6_wrong_update_target": wrong_update,
            "P7_live_version_discipline": {"pass": p7},
        },
        "errors": errors,
        "pass": len(errors) == 0,
    }


def parse_source(source_root):
    nanopubs = source_root / "nanopubs"
    if not nanopubs.is_dir():
        return {
            "files": [],
            "parse_errors": [{
                "path": "nanopubs/",
                "engine": "source",
                "error": "MISSING_NANOPUBS_DIRECTORY",
            }],
            "per_file_exact": False,
            "aggregate_exact": False,
            "surface": None,
        }

    files = sorted(p for p in nanopubs.rglob("*") if p.is_file())
    oracle_surfaces = []
    runtime_surfaces = []
    manifest = []
    errors = []
    per_file_exact = True

    for path in files:
        raw = path.read_bytes()
        rel = path.relative_to(source_root).as_posix()
        row = {
            "path": rel,
            "size": len(raw),
            "sha256": sha256_bytes(raw),
        }
        o = None
        r = None
        try:
            o = fp_oracle.parse_trig(raw)
        except Exception as exc:
            errors.append({
                "path": rel,
                "engine": "RDFLib_oracle",
                "error": f"{type(exc).__name__}: {exc}",
            })
        try:
            r = fp_runtime.parse_trig(raw)
        except Exception as exc:
            errors.append({
                "path": rel,
                "engine": "pyoxigraph_runtime",
                "error": f"{type(exc).__name__}: {exc}",
            })

        if o is not None and r is not None:
            exact = canonical_json(o) == canonical_json(r)
            row["parser_exact"] = exact
            if not exact:
                per_file_exact = False
                errors.append({
                    "path": rel,
                    "engine": "comparison",
                    "error": "REGISTERED_SURFACE_MISMATCH",
                })
            oracle_surfaces.append(o)
            runtime_surfaces.append(r)
        else:
            row["parser_exact"] = False
            per_file_exact = False
        manifest.append(row)

    if errors:
        aggregate_exact = False
        surface = None
    else:
        o_agg = fp_population.merge_surfaces(oracle_surfaces)
        r_agg = fp_population.merge_surfaces(runtime_surfaces)
        aggregate_exact = canonical_json(o_agg) == canonical_json(r_agg)
        surface = o_agg if aggregate_exact else None
        if not aggregate_exact:
            errors.append({
                "path": "<aggregate>",
                "engine": "comparison",
                "error": "AGGREGATE_REGISTERED_SURFACE_MISMATCH",
            })

    return {
        "files": manifest,
        "parse_errors": errors,
        "per_file_exact": per_file_exact,
        "aggregate_exact": aggregate_exact,
        "surface": surface,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--source-archive", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    source_root = Path(args.source_root)
    archive = Path(args.source_archive)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    parsed = parse_source(source_root)

    result = {
        "study": "FORMALIZATION_PAPERS_FRESH_QUALIFIED_COMPOSITION_V1",
        "source": {
            "repository": "LaraHack/formalization_papers_supplemental",
            "commit": "2f68d8498aeeb724e3438deda13e74ae7fb076d8",
            "tag": "v1.0",
            "archive_sha256": (
                sha256_file(archive) if archive.is_file() else None
            ),
            "record_file_count": len(parsed["files"]),
            "files": parsed["files"],
        },
        "parse": {
            "errors": parsed["parse_errors"],
            "per_file_exact": parsed["per_file_exact"],
            "aggregate_exact": parsed["aggregate_exact"],
        },
        "surface_sha256": None,
        "population": None,
        "eligible_chain_count": 0,
        "chain_results": [],
        "provisional_disposition": "INVALID",
        "provisional_reasons": [],
    }

    if parsed["parse_errors"] or not parsed["aggregate_exact"]:
        result["provisional_reasons"].append(
            "PARSER_OR_REGISTERED_SURFACE_FAILURE"
        )
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({
            "study": result["study"],
            "provisional_disposition": result["provisional_disposition"],
            "reasons": result["provisional_reasons"],
        }, ensure_ascii=False, indent=2))
        return

    surface = parsed["surface"]
    result["surface_sha256"] = sha256_bytes(
        canonical_json(surface).encode("utf-8")
    )

    population = fp_population.classify_population(surface)
    result["population"] = population
    if not population["complete_accounting"]:
        result["provisional_reasons"].append(
            "INCOMPLETE_POPULATION_ACCOUNTING"
        )
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({
            "study": result["study"],
            "provisional_disposition": result["provisional_disposition"],
            "reasons": result["provisional_reasons"],
        }, ensure_ascii=False, indent=2))
        return

    version = fp_population.analyze_versions(surface)
    chains = fp_population.eligible_chains(population)
    result["eligible_chain_count"] = len(chains)

    chain_results = [
        execute_chain(chain, population, version)
        for chain in chains
    ]
    result["chain_results"] = chain_results

    technical_errors = [
        err
        for row in chain_results
        for err in row["errors"]
        if err.startswith("ENGINE_DISAGREEMENT")
    ]
    if technical_errors:
        result["provisional_reasons"].extend(technical_errors)
        result["provisional_disposition"] = "INVALID"
    elif chains and all(x["pass"] for x in chain_results):
        result["provisional_disposition"] = "PASS_PENDING_DOCUMENTARY_AUDIT"
    elif chains:
        result["provisional_disposition"] = "BOUNDED_PARTIAL"
        result["provisional_reasons"].append(
            "ONE_OR_MORE_PROSPECTIVE_CRITERIA_NOT_SUPPORTED"
        )
    elif fp_population.has_connected_review_update_structure(population):
        result["provisional_disposition"] = "BOUNDED_PARTIAL"
        result["provisional_reasons"].append(
            "CONNECTED_STRUCTURE_WITHOUT_T0_T1_DENOMINATOR"
        )
    else:
        result["provisional_disposition"] = "NULL_APPLICABILITY"

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "record_file_count": result["source"]["record_file_count"],
        "surface_sha256": result["surface_sha256"],
        "root_count": population["root_count"],
        "disposition_counts": population["disposition_counts"],
        "eligible_chain_count": len(chains),
        "chain_pass_count": sum(x["pass"] for x in chain_results),
        "provisional_disposition": result["provisional_disposition"],
        "provisional_reasons": result["provisional_reasons"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
