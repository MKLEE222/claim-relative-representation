from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FP_DIR = ROOT / "experiments" / "formalization_papers_qualified_composition_v1"
YC_DIR = ROOT / "experiments" / "natural_act_composition_v2"
CROSS_DIR = ROOT / "experiments" / "cross_ecology_generator_signature_v1"

for p in (FP_DIR, YC_DIR, CROSS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import fp_oracle
import fp_runtime
import run_fp_generator_signature_audit_v1 as fpsig
import target_bound_oracle_v2 as yo
import target_bound_runtime_v2 as yr
import run_natural_act_composition_v2 as ynat
import run_cross_ecology_signature_audit_v1 as cross


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def fp_exact(state, event):
    o = fpsig.invoke(fp_oracle, state, event)
    r = fpsig.invoke(fp_runtime, state, event)
    require(o == r, {"state": state, "event": event, "oracle": o, "runtime": r})
    return o


def y_norm(x):
    out = copy.deepcopy(x)
    out.pop("engine", None)
    return out


def y_exact(state, event):
    o = yo.apply(state, event)
    r = yr.execute(state, event)
    require(y_norm(o) == y_norm(r), {
        "state": state,
        "event": event,
        "oracle": y_norm(o),
        "runtime": y_norm(r),
    })
    return o


def add_irrelevant_fp_history(state, tag):
    out = copy.deepcopy(state)
    out.setdefault("history", []).append({
        "kind": "UNRELATED_REGISTERED_NOISE",
        "id": "noise::" + tag,
    })
    return out


def add_irrelevant_y_history(state, tag):
    out = copy.deepcopy(state)
    noise = {
        "event_id": "NOISE::" + tag,
        "evidence_id": "NOISE::" + tag,
        "evidence_relation": "UNRELATED_HISTORY_NOISE",
        "relation_target_claim_id": "UNRELATED",
        "generated_claim_id": None,
        "qualified_generator": "NOISE",
    }
    out.setdefault("evidence_ledger", []).append(copy.deepcopy(noise))
    out.setdefault("event_ledger", []).append(copy.deepcopy(noise))
    out.setdefault("transition_ledger", []).append(copy.deepcopy(noise))
    return out


def same_qualification(a, b, expected):
    return all([
        a.get("qualified") is True,
        b.get("qualified") is True,
        a.get("generator") == expected,
        b.get("generator") == expected,
    ])


def formalization_equivalence(main):
    den = fpsig.denominators(main)

    rows = []
    required = []
    nonrequired = []

    # RECORD_REVIEW
    for row in den["reviews"]:
        s0 = fpsig.initial(row)
        ev = fpsig.event_review(row)
        base = fp_exact(s0, ev)
        noise = fp_exact(add_irrelevant_fp_history(s0, row["review_np"]), ev)
        require(same_qualification(base, noise, "RECORD_REVIEW"), {
            "row": row, "base": base, "noise": noise
        })
        sig = fpsig.audit_review(row, den)
        require(sig["pass"], sig)
        rows.append({
            "generator": "RECORD_REVIEW",
            "context": row,
            "equivalence_invariance": True,
            "irrelevant_history_changed": True,
        })
        required.extend([
            {"generator": "RECORD_REVIEW", "dimension": "BETA_TARGET_IDENTITY", "witness": "wrong_target", "pass": sig["wrong_target_rejected"]},
            {"generator": "RECORD_REVIEW", "dimension": "KAPPA_TARGET_LIVE_CURRENT", "witness": "stale_target", "pass": sig["stale_target_rejected"]},
        ])

    # REPLACE_FORMALIZATION
    for row in den["updates"]:
        s0 = fpsig.initial(row)
        ev = fpsig.event_update(row)
        base = fp_exact(s0, ev)
        with_history = add_irrelevant_fp_history(s0, row["update_np"])
        hist = fp_exact(with_history, ev)
        require(same_qualification(base, hist, "REPLACE_FORMALIZATION"), {
            "row": row, "base": base, "history": hist
        })
        sig = fpsig.audit_update(row, den)
        require(sig["pass"], sig)
        rows.append({
            "generator": "REPLACE_FORMALIZATION",
            "context": row,
            "equivalence_invariance": True,
            "nonrequired_history_invariance": True,
        })
        required.extend([
            {"generator": "REPLACE_FORMALIZATION", "dimension": "BETA_ROOT_IDENTITY", "witness": "wrong_root", "pass": sig["wrong_root_rejected"]},
            {"generator": "REPLACE_FORMALIZATION", "dimension": "KAPPA_VERSION_VALIDITY", "witness": "retracted_update", "pass": sig["retracted_update_rejected"]},
        ])
        nonrequired.append({
            "generator": "REPLACE_FORMALIZATION",
            "dimension": "KAPPA_RETAINED_HISTORY",
            "witness": "irrelevant_history_variation",
            "pass": True,
        })

    # RECORD_RESPONSE
    for row in den["responses"]:
        s0, after_review, before = fpsig.before_response(row)
        ev = fpsig.event_response(row)
        base = fp_exact(before, ev)
        noisy = fp_exact(add_irrelevant_fp_history(before, row["response_np"]), ev)
        require(same_qualification(base, noisy, "RECORD_RESPONSE"), {
            "row": row, "base": base, "noise": noisy
        })
        sig = fpsig.audit_response(row, den)
        require(sig["pass"], sig)
        rows.append({
            "generator": "RECORD_RESPONSE",
            "context": row,
            "equivalence_invariance": True,
            "required_history_preserved_under_noise": True,
        })
        required.extend([
            {"generator": "RECORD_RESPONSE", "dimension": "BETA_REVIEW_TARGET_IDENTITY", "witness": "wrong_review", "pass": sig["wrong_review_rejected"]},
            {"generator": "RECORD_RESPONSE", "dimension": "BETA_UPDATE_TARGET_IDENTITY", "witness": "wrong_update", "pass": sig["wrong_update_rejected"]},
            {"generator": "RECORD_RESPONSE", "dimension": "KAPPA_REVIEW_TARGET_LIVE", "witness": "before_review", "pass": sig["review_target_required"]},
            {"generator": "RECORD_RESPONSE", "dimension": "KAPPA_UPDATE_TARGET_CURRENT", "witness": "before_update", "pass": sig["update_target_required"]},
            {"generator": "RECORD_RESPONSE", "dimension": "KAPPA_RETAINED_HISTORY", "witness": "same_current_history_ablation", "pass": sig["history_required"]},
        ])

    # REVISE_PUBLICATION_STATUS
    for row in den["decisions"]:
        s0 = fpsig.initial(row)
        upd = fp_exact(s0, fpsig.event_update(row))
        ev = fpsig.event_decision(row)
        base = fp_exact(upd["state"], ev)
        ablated = copy.deepcopy(upd["state"])
        ablated["history"] = []
        hist = fp_exact(ablated, ev)
        require(same_qualification(base, hist, "REVISE_PUBLICATION_STATUS"), {
            "row": row, "base": base, "ablated": hist
        })
        sig = fpsig.audit_decision(row, den)
        require(sig["pass"], sig)
        rows.append({
            "generator": "REVISE_PUBLICATION_STATUS",
            "context": row,
            "equivalence_invariance": True,
            "nonrequired_history_invariance": True,
        })
        required.extend([
            {"generator": "REVISE_PUBLICATION_STATUS", "dimension": "BETA_UPDATE_TARGET_IDENTITY", "witness": "wrong_update", "pass": sig["wrong_update_rejected"]},
            {"generator": "REVISE_PUBLICATION_STATUS", "dimension": "KAPPA_UPDATE_TARGET_CURRENT", "witness": "before_update", "pass": sig["current_update_required"]},
        ])
        nonrequired.append({
            "generator": "REVISE_PUBLICATION_STATUS",
            "dimension": "KAPPA_RETAINED_HISTORY",
            "witness": "history_ablation",
            "pass": sig["history_ablated_still_qualified"],
        })

    return {
        "rows": rows,
        "required_witnesses": required,
        "nonrequired_witnesses": nonrequired,
        "denominators": {
            "RECORD_REVIEW": len(den["reviews"]),
            "REPLACE_FORMALIZATION": len(den["updates"]),
            "RECORD_RESPONSE": len(den["responses"]),
            "REVISE_PUBLICATION_STATUS": len(den["decisions"]),
        },
        "den": den,
    }


def yule_equivalence():
    rows = []
    required = []
    nonrequired = []

    # ADD_ALTERNATIVE: Paper Money and Arbre Sec
    for label, fixture in [
        ("PAPER_MONEY", cross.paper_money_fixture),
        ("ARBRE_SEC", cross.arbre_fixture),
    ]:
        s0, e_add, _ = fixture()
        base = y_exact(s0, e_add)
        noisy = y_exact(add_irrelevant_y_history(s0, label), e_add)
        require(same_qualification(base, noisy, "ADD_ALTERNATIVE"), {
            "label": label, "base": base, "noisy": noisy
        })
        sig = cross.audit_yule_add(label, s0, e_add)
        require(sig["pass"], sig)
        rows.append({
            "generator": "ADD_ALTERNATIVE",
            "context": label,
            "equivalence_invariance": True,
            "nonrequired_history_invariance": True,
        })
        required.append({
            "generator": "ADD_ALTERNATIVE",
            "dimension": "BETA_TARGET_BINDING_PLUS_KAPPA_LIVE_TARGET",
            "witness": "nonlive_foreign_target",
            "typed_limitation": "existing natural engine couples event target identity to live-target lookup",
            "pass": sig["wrong_or_nonlive_target_rejected"],
        })
        nonrequired.append({
            "generator": "ADD_ALTERNATIVE",
            "dimension": "KAPPA_RETAINED_HISTORY",
            "witness": "irrelevant_history_variation",
            "pass": True,
        })

    # RESOLVE
    s0, e_add, e_resolve = cross.paper_money_fixture()
    add = y_exact(s0, e_add)
    s1 = add["state"]
    base = y_exact(s1, e_resolve)
    noisy = y_exact(add_irrelevant_y_history(s1, "PM_RESOLVE"), e_resolve)
    require(same_qualification(base, noisy, "RESOLVE"), {
        "base": base, "noisy": noisy
    })
    sig = cross.audit_yule_resolve()
    require(sig["pass"], sig)
    rows.append({
        "generator": "RESOLVE",
        "context": "PAPER_MONEY_PM03",
        "equivalence_invariance": True,
        "required_history_preserved_under_noise": True,
    })
    required.extend([
        {
            "generator": "RESOLVE",
            "dimension": "BETA_TARGET_IDENTITY",
            "witness": "wrong_live_target",
            "pass": sig["wrong_target_rejected"],
        },
        {
            "generator": "RESOLVE",
            "dimension": "KAPPA_RETAINED_HISTORY",
            "witness": "same_current_assertions_history_ablation",
            "pass": sig["history_ablation_rejected"],
        },
    ])

    # RECORD_EVIDENCE
    s0, e_add, e_record = cross.arbre_fixture()
    add = y_exact(s0, e_add)
    s1 = add["state"]
    base = y_exact(s1, e_record)
    nohist = copy.deepcopy(s1)
    nohist["evidence_ledger"] = []
    nohist["event_ledger"] = []
    nohist["transition_ledger"] = []
    hist = y_exact(nohist, e_record)
    require(same_qualification(base, hist, "RECORD_EVIDENCE"), {
        "base": base, "history_ablated": hist
    })
    sig = cross.audit_yule_record_evidence()
    require(sig["pass"], sig)
    rows.append({
        "generator": "RECORD_EVIDENCE",
        "context": "ARBRE_SEC_REPLY",
        "equivalence_invariance": True,
        "nonrequired_history_invariance": True,
    })
    required.append({
        "generator": "RECORD_EVIDENCE",
        "dimension": "BETA_TARGET_BINDING_PLUS_KAPPA_LIVE_TARGET",
        "witness": "before_target_exists",
        "typed_limitation": "existing natural engine couples event target identity to live-target lookup",
        "pass": sig["target_before_live_rejected"],
    })
    nonrequired.append({
        "generator": "RECORD_EVIDENCE",
        "dimension": "KAPPA_RETAINED_HISTORY",
        "witness": "history_ablation",
        "pass": sig["history_ablated_still_qualified"],
    })

    return {
        "rows": rows,
        "required_witnesses": required,
        "nonrequired_witnesses": nonrequired,
    }


def formalization_sequence_closure(main):
    closures = []
    for result in main.get("chain_results", []):
        c = result["chain"]
        s0 = fp_oracle.initial_state(c["root"], c["submission_np"])
        review_ev = fpsig.event_review(c)
        update_ev = fpsig.event_update(c)
        response_ev = fpsig.event_response(c)
        decision_ev = fpsig.event_decision(c)

        review = fp_exact(s0, review_ev)
        update = fp_exact(review["state"], update_ev)

        before_response = update["state"]
        reads_response = {
            "review_target_live": c["review_np"] in before_response["live_reviews"],
            "update_target_current": before_response["current_update_np"] == c["update_np"],
            "review_history_written": any(
                h.get("kind") == "REVIEW" and h.get("review_np") == c["review_np"]
                for h in before_response["history"]
            ),
            "update_history_written": any(
                h.get("kind") == "UPDATE" and h.get("update_np") == c["update_np"]
                for h in before_response["history"]
            ),
        }
        require(all(reads_response.values()), {
            "chain": c, "reads_response": reads_response
        })

        response = fp_exact(before_response, response_ev)
        require(response["qualified"] and response["generator"] == "RECORD_RESPONSE", response)

        before_decision = response["state"]
        reads_decision = {
            "update_target_current": before_decision["current_update_np"] == c["update_np"],
        }
        require(all(reads_decision.values()), {
            "chain": c, "reads_decision": reads_decision
        })
        decision = fp_exact(before_decision, decision_ev)
        require(
            decision["qualified"]
            and decision["generator"] == "REVISE_PUBLICATION_STATUS",
            decision,
        )

        closures.append({
            "chain": c,
            "response_reads": reads_response,
            "response_writers": {
                "live_review_target": "RECORD_REVIEW",
                "current_update_target": "REPLACE_FORMALIZATION",
                "review_history": "RECORD_REVIEW",
                "update_history": "REPLACE_FORMALIZATION",
            },
            "decision_reads": reads_decision,
            "decision_writers": {
                "current_update_target": "REPLACE_FORMALIZATION",
            },
            "pass": True,
        })

    require(len(closures) == 52, {"count": len(closures)})
    return closures


def yule_sequence_closure():
    out = []

    # Paper Money
    s0, e_add, e_resolve = cross.paper_money_fixture()
    add = y_exact(s0, e_add)
    s1 = add["state"]
    live_ids = {
        x.get("claim_id")
        for rows in s1.get("assertions", {}).values()
        for x in rows
    }
    hist = [
        x for x in s1.get("transition_ledger", [])
        if x.get("generated_claim_id") == "PM02"
        and x.get("evidence_relation") == "CONTRADICTS_PRIOR"
    ]
    reads = {
        "target_PM02_live": "PM02" in live_ids,
        "contradiction_history_present": len(hist) == 1,
    }
    require(all(reads.values()), reads)
    resolved = y_exact(s1, e_resolve)
    require(resolved["qualified"] and resolved["generator"] == "RESOLVE", resolved)
    out.append({
        "sequence": "PAPER_MONEY",
        "g1": "ADD_ALTERNATIVE",
        "g2": "RESOLVE",
        "g1_writes": ["live_target_PM02", "contradiction_transition_history"],
        "g2_reads": ["live_target_PM02", "contradiction_transition_history"],
        "reads_satisfied": reads,
        "pass": True,
    })

    # Arbre Sec
    s0, e_add, e_record = cross.arbre_fixture()
    add = y_exact(s0, e_add)
    s1 = add["state"]
    live_ids = {
        x.get("claim_id")
        for rows in s1.get("assertions", {}).values()
        for x in rows
    }
    reads = {"target_ARBR_ID_HS_live": "ARBR-ID-HS" in live_ids}
    require(all(reads.values()), reads)
    record = y_exact(s1, e_record)
    require(record["qualified"] and record["generator"] == "RECORD_EVIDENCE", record)
    out.append({
        "sequence": "ARBRE_SEC",
        "g1": "ADD_ALTERNATIVE",
        "g2": "RECORD_EVIDENCE",
        "g1_writes": ["live_target_ARBR-ID-HS", "transition_history"],
        "g2_reads": ["live_target_ARBR-ID-HS"],
        "history_read_by_g2": False,
        "reads_satisfied": reads,
        "pass": True,
    })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formalization-main", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    main_result = json.loads(
        Path(args.formalization_main).read_text(encoding="utf-8")
    )
    require(len(main_result.get("chain_results", [])) == 52, {
        "chain_count": len(main_result.get("chain_results", []))
    })
    require(all(x.get("pass") for x in main_result["chain_results"]), "formalization chain failure")

    fp = formalization_equivalence(main_result)
    yc = yule_equivalence()

    fp_closure = formalization_sequence_closure(main_result)
    yc_closure = yule_sequence_closure()

    required = fp["required_witnesses"] + yc["required_witnesses"]
    nonrequired = fp["nonrequired_witnesses"] + yc["nonrequired_witnesses"]
    invariance_rows = fp["rows"] + yc["rows"]

    typed_limitations = [
        x for x in required if x.get("typed_limitation")
    ]

    gates = {
        "qualification_invariance_all_contexts": all(
            x["equivalence_invariance"] for x in invariance_rows
        ),
        "required_witnesses_all_pass": all(x["pass"] for x in required),
        "nonrequired_witnesses_all_pass": all(x["pass"] for x in nonrequired),
        "formalization_sequence_closure_52_of_52": (
            len(fp_closure) == 52 and all(x["pass"] for x in fp_closure)
        ),
        "yule_sequence_closure_2_of_2": (
            len(yc_closure) == 2 and all(x["pass"] for x in yc_closure)
        ),
        "oracle_runtime_exact": True,
    }

    result = {
        "study": "ACTION_RELATIVE_STATE_EQUIVALENCE_SEQUENCE_CLOSURE_V1",
        "data_status": "EXISTING_POST_FRESH_AND_PREEXISTING_EXPOSED_ONLY",
        "formalization_denominators": fp["denominators"],
        "qualification_invariance": {
            "context_count": len(invariance_rows),
            "rows": invariance_rows,
        },
        "required_dimension_witnesses": required,
        "nonrequired_dimension_witnesses": nonrequired,
        "typed_limitations": typed_limitations,
        "sequence_closure": {
            "formalization": {
                "chain_count": len(fp_closure),
                "rows": fp_closure,
            },
            "yule_cordier": yc_closure,
        },
        "gates": gates,
        "overall": (
            "ACTION_RELATIVE_EQUIVALENCE_SEQUENCE_CLOSURE_PASS"
            if all(gates.values())
            else "ACTION_RELATIVE_EQUIVALENCE_SEQUENCE_CLOSURE_INCOMPLETE"
        ),
        "formal_statement": (
            "Within the registered action families, qualification is invariant "
            "under state changes outside each generator's registered state-side "
            "qualification signature; registered required dimensions have "
            "counterexamples, and prior actions write the target/state/history "
            "conditions read by later generators in the audited sequences."
        ),
        "claim_ceiling": [
            "State equivalence is generator-relative and event binding is typed separately.",
            "Yule ADD_ALTERNATIVE and RECORD_EVIDENCE currently couple exact target binding to live-target lookup, so those two axes are not independently identified there.",
            "The closure is bounded to registered tasks and does not establish universal minimality.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "formalization_denominators": result["formalization_denominators"],
        "qualification_invariance_context_count": result[
            "qualification_invariance"
        ]["context_count"],
        "required_witness_count": len(required),
        "nonrequired_witness_count": len(nonrequired),
        "typed_limitation_count": len(typed_limitations),
        "formalization_sequence_closure": f"{sum(x['pass'] for x in fp_closure)}/{len(fp_closure)}",
        "yule_sequence_closure": f"{sum(x['pass'] for x in yc_closure)}/{len(yc_closure)}",
        "gates": gates,
        "overall": result["overall"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
