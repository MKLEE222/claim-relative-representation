from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_DIR = HERE.parent / "module_r_scholarly_assertion_reassessment_v1"
for p in (HERE, R_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import generator_audit as G
import oracle_r
import runtime_r
import test_reassessment_contract as synth
import run_historical_exposed as hist


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def synthetic_cases():
    cases = []

    s1 = synth.base_state()
    e1 = synth.event(
        "G-F1-REPLACE",
        "author-attribution",
        "REPLACE",
        "Author-B",
        "ACCEPTED",
        "EVID-G-F1",
        "audit:g:f1",
    )
    cases.append(("SYNTH_REPLACE", s1, e1))

    s2 = synth.base_state()
    e2 = synth.event(
        "G-F2-ALTERNATIVE",
        "author-attribution",
        "ADD_ALTERNATIVE",
        "Author-B",
        "COMPETING",
        "EVID-G-F2",
        "audit:g:f2",
    )
    cases.append(("SYNTH_ADD_ALTERNATIVE", s2, e2))

    s3 = synth.base_state()
    e3 = synth.event(
        "G-F3-STATUS",
        "evidence-status",
        "REVISE_STATUS",
        "EVIDENCE-1",
        "MEDIATED",
        "EVID-G-F3",
        "audit:g:f3",
    )
    cases.append(("SYNTH_REVISE_STATUS", s3, e3))

    s13 = synth.base_state()
    e13 = synth.event(
        "G-F13-BASIS-NULL",
        "author-attribution",
        "REPLACE",
        "Author-A",
        "ACCEPTED",
        "EVID-G-F13",
        "audit:g:f13",
        agent="editor-new",
    )
    cases.append(("SYNTH_BASIS_NULL", s13, e13))

    s14 = synth.base_state()
    e14 = synth.event(
        "G-F14-STATUS-NULL",
        "evidence-status",
        "REVISE_STATUS",
        "EVIDENCE-1",
        "DIRECT",
        "EVID-G-F14",
        "audit:g:f14",
    )
    cases.append(("SYNTH_STATUS_NULL", s14, e14))

    return cases


def historical_cases():
    out = []
    for item in hist.load_panel():
        out.append((
            "HIST_" + item["entry_id"],
            hist.make_state(item),
            hist.make_event(item),
        ))
    return out


def future_probe_for(state, target, tag):
    return {
        "event_id": "FUTURE_PROBE::" + tag,
        "event_class": "SCHOLARLY_REASSESSMENT",
        "object_id": state["object_id"],
        "target_property": target,
        "source_repository": state["source_repository"],
        "source_version": state["source_version"],
        "evidence_id": "FUTURE_EVIDENCE::" + tag,
        "evidence_locator": "future-probe::" + tag,
        "responsible_agent": "future-auditor",
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "new_claim_id": "FUTURE_CLAIM::" + tag,
        "value": "FUTURE_COMPETING_VALUE::" + tag,
        "status": "COMPETING",
    }


def null_audit(label, state, event):
    frozen = oracle_r.apply_event(state, event)
    require(not frozen["substantive"], {
        "label": label,
        "transition": frozen,
    })

    runtime = runtime_r.execute(state, event)
    psi_equal = runtime["before_state"] == runtime["after_state"]
    full_changed = runtime["state"] != state
    ledger_changed = any([
        bool(runtime["state"].get("evidence_ledger")),
        bool(runtime["state"].get("event_ledger")),
        bool(runtime["state"].get("transition_ledger")),
    ])

    probe = future_probe_for(
        state,
        event["target_property"],
        label,
    )
    before_gamma = G.structural_candidates(state, probe)
    after_gamma = G.structural_candidates(runtime["state"], probe)
    gamma_equal = before_gamma == after_gamma

    if psi_equal and not gamma_equal:
        classification = "STATE_NULL_ACTION_NON_NULL"
    elif psi_equal and full_changed and ledger_changed and gamma_equal:
        classification = "FUTURE_SENSITIVITY_NOT_REPRESENTED"
    elif psi_equal and gamma_equal:
        classification = "TRUE_ACTION_IDENTITY"
    else:
        classification = "NOT_A_PSI_NULL"

    return {
        "label": label,
        "psi_equal": psi_equal,
        "full_representation_changed": full_changed,
        "ledger_changed": ledger_changed,
        "future_gamma_before": before_gamma,
        "future_gamma_after": after_gamma,
        "future_gamma_equal": gamma_equal,
        "classification": classification,
    }


def composition_probe():
    s0 = synth.base_state()

    e1 = synth.event(
        "COMPOSE-ALT",
        "author-attribution",
        "ADD_ALTERNATIVE",
        "Author-B",
        "COMPETING",
        "EVID-COMPOSE-ALT",
        "compose:alt",
    )
    t1 = oracle_r.apply_event(s0, e1)
    require(t1["applicable"], t1)
    s1 = t1["state"]

    e2 = synth.event(
        "COMPOSE-RESOLVE",
        "author-attribution",
        "RESOLVE",
        "Author-B",
        "ACCEPTED",
        "EVID-COMPOSE-RESOLVE",
        "compose:resolve",
    )
    e2_bar = G.strip_operation(e2)

    gamma_s0 = G.structural_candidates(s0, e2_bar)
    gamma_s1 = G.structural_candidates(s1, e2_bar)

    forward = oracle_r.apply_event(s1, e2)

    return {
        "gamma_before_alternative": gamma_s0,
        "gamma_after_alternative": gamma_s1,
        "resolve_enabled_before": "RESOLVE" in gamma_s0,
        "resolve_enabled_after": "RESOLVE" in gamma_s1,
        "forward_sequence_defined": bool(forward.get("applicable")),
        "forward_transition_class": forward.get("transition_class"),
        "reverse_resolution_structurally_defined": "RESOLVE" in gamma_s0,
        "state_dependent_enablement": (
            "RESOLVE" not in gamma_s0
            and "RESOLVE" in gamma_s1
        ),
        "partial_noncommutativity": (
            bool(forward.get("applicable"))
            and "RESOLVE" not in gamma_s0
        ),
    }


def main():
    recovery_rows = []

    for label, state, event in synthetic_cases() + historical_cases():
        row = G.recovery_record(state, event)
        row["label"] = label
        row["frozen_operation"] = event["operation"]
        recovery_rows.append(row)

    require(all(
        row["frozen_operation"] in row["gamma_pre"]
        for row in recovery_rows
    ), recovery_rows)
    require(all(
        row["frozen_operation"] in row["gamma_match"]
        for row in recovery_rows
    ), recovery_rows)

    null_rows = []
    for label, state, event in synthetic_cases() + historical_cases():
        tr = oracle_r.apply_event(state, event)
        if not tr["substantive"]:
            null_rows.append(null_audit(label, state, event))

    compose = composition_probe()

    summary = {
        "episode_count": len(recovery_rows),
        "pre_unique": sum(
            row["pre_recovery_class"] == "UNIQUE"
            for row in recovery_rows
        ),
        "pre_underidentified": sum(
            row["pre_recovery_class"] == "UNDERIDENTIFIED"
            for row in recovery_rows
        ),
        "phenotype_unique": sum(
            row["phenotype_recovery_class"] == "UNIQUE_PHENOTYPE"
            for row in recovery_rows
        ),
        "phenotype_underidentified": sum(
            row["phenotype_recovery_class"]
            == "UNDERIDENTIFIED_PHENOTYPE"
            for row in recovery_rows
        ),
        "full_state_unique": sum(
            row["full_state_recovery_class"] == "UNIQUE_FULL_STATE"
            for row in recovery_rows
        ),
        "full_state_underidentified": sum(
            row["full_state_recovery_class"]
            == "UNDERIDENTIFIED_FULL_STATE"
            for row in recovery_rows
        ),
        "null_count": len(null_rows),
        "state_null_action_non_null": sum(
            row["classification"] == "STATE_NULL_ACTION_NON_NULL"
            for row in null_rows
        ),
        "future_sensitivity_not_represented": sum(
            row["classification"] == "FUTURE_SENSITIVITY_NOT_REPRESENTED"
            for row in null_rows
        ),
    }

    findings = {
        "EXOGENOUS_OPERATION_PROBLEM": summary["pre_underidentified"] > 0,
        "GENERATOR_NONIDENTIFIABILITY": (
            summary["full_state_underidentified"] > 0
        ),
        "COMPOSITION_REQUIRED": bool(compose["state_dependent_enablement"]),
        "NULL_MODEL_INCOMPLETE": (
            summary["state_null_action_non_null"] > 0
        ),
        "FUTURE_QUALIFICATION_BLIND_SPOT": (
            summary["future_sensitivity_not_represented"] > 0
        ),
    }
    findings["NO_DEEPER_PROBLEM"] = not any(findings.values())

    result = {
        "study": "GENERATOR_DEEXOGENIZATION_COMPOSITION_AUDIT_V1",
        "data_status": "SYNTHETIC_PLUS_PREEXISTING_EXPOSED_ONLY",
        "summary": summary,
        "findings": findings,
        "recovery_rows": recovery_rows,
        "null_rows": null_rows,
        "composition_probe": compose,
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "generator_audit_results_v1.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "summary": summary,
        "findings": findings,
        "composition_probe": compose,
        "recovery_compact": [
            {
                "label": row["label"],
                "frozen_operation": row["frozen_operation"],
                "gamma_pre": row["gamma_pre"],
                "gamma_match": row["gamma_match"],
                "gamma_full_state_match": row[
                    "gamma_full_state_match"
                ],
            }
            for row in recovery_rows
        ],
        "null_compact": null_rows,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
