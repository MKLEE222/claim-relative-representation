from __future__ import annotations

import copy
import json

REGISTERED_RELATIONS = {
    "CONTRADICTS_PRIOR",
    "CORRECTION_OF_PRIOR_CRITICISM",
    "COMPETING_IDENTIFICATION",
    "BIBLIOGRAPHIC_REPLY",
}


def psi(state):
    targets = []
    for target in sorted((state.get("assertions") or {})):
        rows = []
        for a in state["assertions"][target]:
            rows.append({
                "claim_id": a.get("claim_id"),
                "object_id": a.get("object_id"),
                "target_property": a.get("target_property"),
                "value": copy.deepcopy(a.get("value")),
                "status": a.get("status"),
            })
        rows.sort(key=lambda x: json.dumps(
            x, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ))
        targets.append({"target_property": target, "assertions": rows})
    return {"object_id": state.get("object_id"), "targets": targets}


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


def _rows(state, event):
    return list((state.get("assertions") or {}).get(event["target_property"], []))


def _target(rows, claim_id):
    found = [x for x in rows if x.get("claim_id") == claim_id]
    return found[0] if len(found) == 1 else None


def _history_for_generated_claim(state, claim_id, relation=None):
    found = []
    for row in state.get("transition_ledger") or []:
        if row.get("generated_claim_id") != claim_id:
            continue
        if relation is not None and row.get("evidence_relation") != relation:
            continue
        found.append(row)
    return found


def qualify(state, event):
    reason = _binding_reason(state, event)
    if reason:
        return {"qualified": False, "generator": None, "reason": reason}

    rows = _rows(state, event)
    target = _target(rows, event.get("relation_target_claim_id"))
    if target is None:
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_TARGET_NOT_LIVE",
        }

    relation = event["evidence_relation"]

    if relation in {"CONTRADICTS_PRIOR", "COMPETING_IDENTIFICATION"}:
        if event.get("value") != target.get("value"):
            return {
                "qualified": True,
                "generator": "ADD_ALTERNATIVE",
                "reason": None,
            }
        if event.get("status") != target.get("status"):
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
        history = _history_for_generated_claim(
            state,
            event.get("relation_target_claim_id"),
            "CONTRADICTS_PRIOR",
        )
        if len(history) != 1:
            return {
                "qualified": False,
                "generator": None,
                "reason": "RELATION_TARGET_HISTORY_UNRESOLVED",
            }
        other_same_value = [
            x for x in rows
            if x.get("claim_id") != event.get("relation_target_claim_id")
            and x.get("value") == event.get("value")
        ]
        if len(rows) > 1 and len(other_same_value) == 1:
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

    if relation == "BIBLIOGRAPHIC_REPLY":
        return {
            "qualified": True,
            "generator": "RECORD_EVIDENCE",
            "reason": None,
        }

    return {
        "qualified": False,
        "generator": None,
        "reason": "UNREGISTERED_EVIDENCE_RELATION",
    }


def _claim_from_event(state, event):
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
    current = copy.deepcopy(state)
    bpsi = psi(before)
    bxi = xi(before)
    q = qualify(before, event)

    if not q["qualified"]:
        return {
            "engine": "target_bound_oracle_v2",
            "qualified": False,
            "generator": None,
            "rejection_reason": q["reason"],
            "before_psi": bpsi,
            "after_psi": bpsi,
            "before_xi": bxi,
            "after_xi": bxi,
            "state": current,
            "qualification": q,
        }

    g = q["generator"]
    target_name = event["target_property"]
    live = copy.deepcopy(current["assertions"].get(target_name, []))

    if g == "ADD_ALTERNATIVE":
        current["assertions"][target_name] = live + [
            _claim_from_event(current, event)
        ]
    elif g == "REVISE_STATUS":
        revised = []
        hits = 0
        for row in live:
            if row.get("claim_id") == event.get("relation_target_claim_id"):
                nr = copy.deepcopy(row)
                nr["claim_id"] = event.get("new_claim_id")
                nr["status"] = event.get("status")
                nr["source_id"] = event.get("evidence_id")
                nr["source_locator"] = event.get("evidence_locator")
                nr["responsible_agent"] = event.get("responsible_agent")
                revised.append(nr)
                hits += 1
            else:
                revised.append(row)
        if hits != 1:
            raise AssertionError("qualified status revision without one target")
        current["assertions"][target_name] = revised
    elif g == "RESOLVE":
        current["assertions"][target_name] = [
            _claim_from_event(current, event)
        ]
    elif g == "RECORD_EVIDENCE":
        pass
    else:
        raise AssertionError(g)

    apsi = psi(current)
    generated_claim_id = (
        event.get("new_claim_id") if g != "RECORD_EVIDENCE" else None
    )

    base = {
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "object_id": event.get("object_id"),
        "target_property": target_name,
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": generated_claim_id,
        "qualified_generator": g,
        "responsible_agent": event.get("responsible_agent"),
        "mediator_agent": event.get("mediator_agent"),
    }
    current.setdefault("evidence_ledger", []).append(copy.deepcopy(base))
    current.setdefault("event_ledger", []).append({
        k: copy.deepcopy(base[k])
        for k in (
            "event_id",
            "evidence_relation",
            "relation_target_claim_id",
            "generated_claim_id",
            "qualified_generator",
            "responsible_agent",
            "mediator_agent",
        )
    })
    tr = copy.deepcopy(base)
    tr["before_psi"] = bpsi
    tr["after_psi"] = apsi
    tr["assertion_identity"] = bpsi == apsi
    tr["history_nonidentity"] = True
    current.setdefault("transition_ledger", []).append(tr)

    return {
        "engine": "target_bound_oracle_v2",
        "qualified": True,
        "generator": g,
        "rejection_reason": None,
        "before_psi": bpsi,
        "after_psi": apsi,
        "before_xi": bxi,
        "after_xi": xi(current),
        "assertion_identity": bpsi == apsi,
        "history_nonidentity": bxi != xi(current),
        "state": current,
        "qualification": q,
    }
