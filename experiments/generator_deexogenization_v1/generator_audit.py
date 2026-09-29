from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_DIR = HERE.parent / "module_r_scholarly_assertion_reassessment_v1"
if str(R_DIR) not in sys.path:
    sys.path.insert(0, str(R_DIR))

import oracle_r

OPS = ("REPLACE", "ADD_ALTERNATIVE", "REVISE_STATUS", "RESOLVE")


def strip_operation(event):
    out = copy.deepcopy(event)
    out.pop("operation", None)
    return out


def binding_admissible(state, event_without_operation):
    e = event_without_operation
    return all([
        e.get("object_id") == state.get("object_id"),
        e.get("target_property") in state.get("registered_targets", []),
        e.get("source_repository") == state.get("source_repository"),
        e.get("source_version") == state.get("source_version"),
        e.get("applicability_class") == "ASSERTION_LEVEL_ADMISSIBLE",
        bool(e.get("evidence_id")),
        bool(e.get("evidence_locator")),
    ])


def _target_rows(state, event_without_operation):
    target = event_without_operation.get("target_property")
    return list((state.get("assertions") or {}).get(target, []))


def _pair(row):
    return (
        json.dumps(row.get("value"), ensure_ascii=False, sort_keys=True),
        str(row.get("status")),
    )


def _proposal_pair(event_without_operation):
    return (
        json.dumps(
            event_without_operation.get("value"),
            ensure_ascii=False,
            sort_keys=True,
        ),
        str(event_without_operation.get("status")),
    )


def _single_unresolved(rows):
    if len(rows) != 1:
        return False
    row = rows[0]
    return str(row.get("status")) == "UNRESOLVED"


def structural_candidates(state, event_without_operation):
    if not binding_admissible(state, event_without_operation):
        return []

    rows = _target_rows(state, event_without_operation)
    if not rows:
        return []

    existing_pairs = {_pair(x) for x in rows}
    proposal_pair = _proposal_pair(event_without_operation)
    proposal_value = event_without_operation.get("value")

    candidates = []

    # Existing Module-R description: replace the live assertion set.
    candidates.append("REPLACE")

    # Add a genuinely new alternative to a non-unresolved live set.
    if not _single_unresolved(rows) and proposal_pair not in existing_pairs:
        candidates.append("ADD_ALTERNATIVE")

    # Same literal value is the structural prerequisite for status revision.
    if any(x.get("value") == proposal_value for x in rows):
        candidates.append("REVISE_STATUS")

    # Existing Module-R description restricts resolution to unresolved/alternative states.
    if _single_unresolved(rows) or len(rows) > 1:
        candidates.append("RESOLVE")

    return candidates


def execute_candidate(state, event_without_operation, operation):
    e = copy.deepcopy(event_without_operation)
    e["operation"] = operation
    return oracle_r.apply_event(state, e)


def candidate_outcomes(state, event_without_operation):
    out = {}
    for op in structural_candidates(state, event_without_operation):
        transition = execute_candidate(state, event_without_operation, op)
        if transition.get("applicable"):
            out[op] = {
                "after_state": transition.get("after_state"),
                "substantive": transition.get("substantive"),
                "transition_class": transition.get("transition_class"),
            }
    return out


def phenotype_matches(state, event_without_operation, observed_after_state):
    outcomes = candidate_outcomes(state, event_without_operation)
    return sorted(
        op
        for op, row in outcomes.items()
        if row.get("after_state") == observed_after_state
    )


def recovery_record(state, frozen_event):
    held_out_operation = frozen_event.get("operation")
    e = strip_operation(frozen_event)
    frozen_transition = oracle_r.apply_event(state, frozen_event)
    gamma = structural_candidates(state, e)
    matches = phenotype_matches(
        state, e, frozen_transition.get("after_state")
    )
    return {
        "held_out_operation": held_out_operation,
        "gamma_pre": gamma,
        "gamma_pre_count": len(gamma),
        "pre_recovery_class": (
            "EMPTY" if len(gamma) == 0
            else "UNIQUE" if len(gamma) == 1
            else "UNDERIDENTIFIED"
        ),
        "held_out_recovered_pre": gamma == [held_out_operation],
        "observed_after_state": frozen_transition.get("after_state"),
        "observed_substantive": bool(frozen_transition.get("substantive")),
        "observed_transition_class": frozen_transition.get("transition_class"),
        "gamma_match": matches,
        "gamma_match_count": len(matches),
        "phenotype_recovery_class": (
            "NO_MATCH" if len(matches) == 0
            else "UNIQUE_PHENOTYPE" if len(matches) == 1
            else "UNDERIDENTIFIED_PHENOTYPE"
        ),
        "held_out_recovered_from_phenotype": matches == [held_out_operation],
        "candidate_outcomes": candidate_outcomes(state, e),
    }
