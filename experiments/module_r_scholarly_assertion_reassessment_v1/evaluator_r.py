from __future__ import annotations

import copy


def _expected_provenance(state):
    rows = []
    for target in sorted(state.get("assertions", {})):
        for a in state["assertions"][target]:
            rows.append({
                "claim_id": a.get("claim_id"),
                "object_id": a.get("object_id"),
                "target_property": a.get("target_property"),
                "source_repository": a.get("source_repository"),
                "source_version": a.get("source_version"),
                "source_id": a.get("source_id"),
                "source_locator": a.get("source_locator"),
                "responsible_agent": a.get("responsible_agent"),
                "applicability_class": a.get("applicability_class"),
            })
    rows.sort(key=lambda x: (str(x.get("target_property")), str(x.get("claim_id"))))
    return rows


def evaluate(output, oracle_transition, oracle_after_state, event):
    tr = output.get("transition") or {}
    audit = output.get("delayed_audit") or {}

    r1 = output.get("before_state") == oracle_transition.get("before_state")

    r2 = all([
        tr.get("target_property") == event.get("target_property"),
        tr.get("object_id") == event.get("object_id"),
    ])

    r3 = bool(tr.get("applicable")) == bool(oracle_transition.get("applicable"))

    r4 = output.get("after_state") == oracle_transition.get("after_state")

    r5 = (
        list(tr.get("collateral_targets") or [])
        == list(oracle_transition.get("collateral_targets") or [])
    )

    expected_prov = _expected_provenance(oracle_after_state)
    r6 = output.get("current_provenance") == expected_prov

    r7 = all([
        tr.get("applicable") == oracle_transition.get("applicable"),
        tr.get("event_id") == oracle_transition.get("event_id"),
        tr.get("event_class") == oracle_transition.get("event_class"),
        tr.get("object_id") == oracle_transition.get("object_id"),
        tr.get("target_property") == oracle_transition.get("target_property"),
        tr.get("evidence_id") == oracle_transition.get("evidence_id"),
        tr.get("before_state") == oracle_transition.get("before_state"),
        tr.get("after_state") == oracle_transition.get("after_state"),
        tr.get("transition_class") == oracle_transition.get("transition_class"),
    ])

    if oracle_transition.get("applicable"):
        r8 = all([
            audit.get("event_id") == oracle_transition.get("event_id"),
            audit.get("object_id") == oracle_transition.get("object_id"),
            audit.get("target_property") == oracle_transition.get("target_property"),
            audit.get("evidence_id") == oracle_transition.get("evidence_id"),
            audit.get("before_state") == oracle_transition.get("before_state"),
            audit.get("after_state") == oracle_transition.get("after_state"),
            audit.get("transition_class")
                == oracle_transition.get("transition_class"),
        ])
    else:
        r8 = audit.get("event_id") is None

    return {
        "R1_PRE_STATE_EXACT": r1,
        "R2_TARGET_DETERMINACY": r2,
        "R3_EVENT_APPLICABILITY": r3,
        "R4_POST_EVENT_RESULT": r4,
        "R5_SELECTIVE_UPDATE": r5,
        "R6_PROVENANCE": r6,
        "R7_TRANSITION_ATTRIBUTION": r7,
        "R8_DELAYED_HISTORY": r8,
        "reference_end_to_end_pass": all([r1,r2,r3,r4,r5,r6,r7,r8]),
    }


def evaluate_current_reopen(view, oracle_transition, oracle_after_state):
    return {
        "CURRENT_STATE_EXACT": view.get("current_state") == oracle_transition.get("after_state"),
        "CURRENT_PROVENANCE_EXACT": (
            view.get("current_provenance") == _expected_provenance(oracle_after_state)
        ),
        "TRANSITION_ATTRIBUTION_EXACT": False,
        "DELAYED_HISTORY_EXACT": False,
    }


def evaluate_snapshots(view, oracle_transition, oracle_after_state):
    return {
        "PRE_STATE_EXACT": view.get("S0") == oracle_transition.get("before_state"),
        "POST_STATE_EXACT": view.get("S1") == oracle_transition.get("after_state"),
        "STATE_DELTA_EXACT": (
            view.get("delta", {}).get("changed_targets")
            == oracle_transition.get("changed_targets")
            and view.get("delta", {}).get("collateral_targets")
            == oracle_transition.get("collateral_targets")
        ),
        "CURRENT_PROVENANCE_EXACT": (
            view.get("current_provenance") == _expected_provenance(oracle_after_state)
        ),
        "TRANSITION_ATTRIBUTION_EXACT": False,
        "DELAYED_HISTORY_EXACT": False,
    }


def evaluate_change_log(view, oracle_transition):
    core = all([
        view.get("event_id") == oracle_transition.get("event_id"),
        view.get("event_class") == oracle_transition.get("event_class"),
        view.get("object_id") == oracle_transition.get("object_id"),
        view.get("target_property") == oracle_transition.get("target_property"),
        view.get("before_state") == oracle_transition.get("before_state"),
        view.get("after_state") == oracle_transition.get("after_state"),
        view.get("changed_targets") == oracle_transition.get("changed_targets"),
    ])
    return {
        "CHANGE_EVENT_TARGET_DIFF_EXACT": core,
        "EVIDENCE_JUSTIFICATION_AVAILABLE": False,
        "DELAYED_EVIDENCE_GROUNDED_AUDIT": False,
    }
