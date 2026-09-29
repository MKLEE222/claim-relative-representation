from __future__ import annotations

import copy
import json


REGISTERED_RELATIONS = {
    "CONTRADICTS_PRIOR",
    "CORRECTION_OF_PRIOR_CRITICISM",
}


def psi(state):
    rows = []
    for target in sorted((state.get("assertions") or {})):
        vals = []
        for a in state["assertions"][target]:
            vals.append({
                "claim_id": a.get("claim_id"),
                "object_id": a.get("object_id"),
                "target_property": a.get("target_property"),
                "value": copy.deepcopy(a.get("value")),
                "status": a.get("status"),
            })
        vals.sort(
            key=lambda x: json.dumps(
                x, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
        )
        rows.append({"target_property": target, "assertions": vals})
    return {"object_id": state.get("object_id"), "targets": rows}


def xi(state):
    return {
        "evidence_ledger": copy.deepcopy(state.get("evidence_ledger") or []),
        "event_ledger": copy.deepcopy(state.get("event_ledger") or []),
        "transition_ledger": copy.deepcopy(state.get("transition_ledger") or []),
    }


def _binding_reason(state, event):
    if event.get("object_id") != state.get("object_id"):
        return "WRONG_OBJECT"
    if event.get("target_property") not in (state.get("registered_targets") or []):
        return "WRONG_TARGET"
    if event.get("source_repository") != state.get("source_repository"):
        return "WRONG_SOURCE_REPOSITORY"
    if event.get("source_version") != state.get("source_version"):
        return "WRONG_SOURCE_VERSION"
    if event.get("applicability_class") != "ASSERTION_LEVEL_ADMISSIBLE":
        return "MISSING_APPLICABILITY"
    if not event.get("evidence_id") or not event.get("evidence_locator"):
        return "MISSING_EVIDENCE_BINDING"
    if event.get("evidence_relation") not in REGISTERED_RELATIONS:
        return "UNREGISTERED_EVIDENCE_RELATION"
    if not event.get("relation_target_claim_id"):
        return "MISSING_RELATION_TARGET"
    return None


def _target_rows(state, event):
    return list((state.get("assertions") or {}).get(event["target_property"], []))


def _claim_by_id(rows, claim_id):
    matches = [x for x in rows if x.get("claim_id") == claim_id]
    if len(matches) == 1:
        return matches[0]
    return None


def _critical_history(state, claim_id):
    matches = []
    for row in state.get("transition_ledger") or []:
        if (
            row.get("generated_claim_id") == claim_id
            and row.get("evidence_relation") == "CONTRADICTS_PRIOR"
            and row.get("relation_target_claim_id")
        ):
            matches.append(row)
    return matches


def qualify(state, event):
    reason = _binding_reason(state, event)
    if reason:
        return {
            "qualified": False,
            "generator": None,
            "reason": reason,
        }

    rows = _target_rows(state, event)
    target_claim = _claim_by_id(
        rows, event.get("relation_target_claim_id")
    )
    if target_claim is None:
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_TARGET_NOT_LIVE",
        }

    relation = event["evidence_relation"]

    if relation == "CONTRADICTS_PRIOR":
        if event.get("value") != target_claim.get("value"):
            return {
                "qualified": True,
                "generator": "ADD_ALTERNATIVE",
                "reason": None,
            }
        if event.get("status") != target_claim.get("status"):
            return {
                "qualified": True,
                "generator": "REVISE_STATUS",
                "reason": None,
            }
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_STATE_MISMATCH",
        }

    if relation == "CORRECTION_OF_PRIOR_CRITICISM":
        history = _critical_history(
            state, event.get("relation_target_claim_id")
        )
        if len(history) != 1:
            return {
                "qualified": False,
                "generator": None,
                "reason": "RELATION_TARGET_HISTORY_UNRESOLVED",
            }

        other_matches = [
            x for x in rows
            if x.get("claim_id") != event.get("relation_target_claim_id")
            and x.get("value") == event.get("value")
        ]
        if len(rows) > 1 and len(other_matches) == 1:
            return {
                "qualified": True,
                "generator": "RESOLVE",
                "reason": None,
                "history_support": copy.deepcopy(history[0]),
            }
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_STATE_MISMATCH",
        }

    return {
        "qualified": False,
        "generator": None,
        "reason": "UNREGISTERED_EVIDENCE_RELATION",
    }


def _new_claim(state, event):
    return {
        "claim_id": event.get("new_claim_id"),
        "object_id": state.get("object_id"),
        "target_property": event.get("target_property"),
        "value": copy.deepcopy(event.get("value")),
        "status": event.get("status"),
        "source_id": event.get("evidence_id"),
        "source_locator": event.get("evidence_locator"),
        "responsible_agent": event.get("responsible_agent"),
    }


def apply(state, event):
    before = copy.deepcopy(state)
    before_psi = psi(before)
    before_xi = xi(before)
    current = copy.deepcopy(state)

    q = qualify(before, event)
    if not q.get("qualified"):
        return {
            "engine": "target_bound_oracle_v1",
            "qualified": False,
            "generator": None,
            "rejection_reason": q.get("reason"),
            "before_psi": before_psi,
            "after_psi": before_psi,
            "before_xi": before_xi,
            "after_xi": before_xi,
            "state": current,
            "qualification": q,
        }

    generator = q["generator"]
    target = event["target_property"]
    rows = copy.deepcopy(current["assertions"].get(target, []))
    new = _new_claim(current, event)

    if generator == "ADD_ALTERNATIVE":
        current["assertions"][target] = rows + [new]
    elif generator == "REVISE_STATUS":
        revised = []
        changed = 0
        for row in rows:
            if row.get("claim_id") == event.get("relation_target_claim_id"):
                x = copy.deepcopy(row)
                x["claim_id"] = event.get("new_claim_id")
                x["status"] = event.get("status")
                x["source_id"] = event.get("evidence_id")
                x["source_locator"] = event.get("evidence_locator")
                x["responsible_agent"] = event.get("responsible_agent")
                revised.append(x)
                changed += 1
            else:
                revised.append(row)
        if changed != 1:
            raise AssertionError("qualified REVISE_STATUS target mismatch")
        current["assertions"][target] = revised
    elif generator == "RESOLVE":
        current["assertions"][target] = [new]
    else:
        raise AssertionError(generator)

    after_psi = psi(current)

    evidence_row = {
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": event.get("new_claim_id"),
        "qualified_generator": generator,
        "responsible_agent": event.get("responsible_agent"),
    }
    current.setdefault("evidence_ledger", []).append(
        copy.deepcopy(evidence_row)
    )
    current.setdefault("event_ledger", []).append({
        "event_id": event.get("event_id"),
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": event.get("new_claim_id"),
        "qualified_generator": generator,
    })
    current.setdefault("transition_ledger", []).append({
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": event.get("new_claim_id"),
        "qualified_generator": generator,
        "before_psi": before_psi,
        "after_psi": after_psi,
    })

    return {
        "engine": "target_bound_oracle_v1",
        "qualified": True,
        "generator": generator,
        "rejection_reason": None,
        "before_psi": before_psi,
        "after_psi": after_psi,
        "before_xi": before_xi,
        "after_xi": xi(current),
        "state": current,
        "qualification": q,
    }
