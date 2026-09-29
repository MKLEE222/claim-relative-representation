from __future__ import annotations

import copy
import json

_ALLOWED = (
    "CONTRADICTS_PRIOR",
    "CORRECTION_OF_PRIOR_CRITICISM",
)


def psi(state):
    targets = []
    assertions_map = state.get("assertions") or {}
    for name in sorted(assertions_map):
        rows = []
        for item in assertions_map[name]:
            rows.append({
                "claim_id": item.get("claim_id"),
                "object_id": item.get("object_id"),
                "target_property": item.get("target_property"),
                "value": copy.deepcopy(item.get("value")),
                "status": item.get("status"),
            })
        rows.sort(
            key=lambda x: json.dumps(
                x, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
        )
        targets.append({"target_property": name, "assertions": rows})
    return {"object_id": state.get("object_id"), "targets": targets}


def xi(state):
    return {
        "evidence_ledger": copy.deepcopy(state.get("evidence_ledger", [])),
        "event_ledger": copy.deepcopy(state.get("event_ledger", [])),
        "transition_ledger": copy.deepcopy(state.get("transition_ledger", [])),
    }


def _preflight(state, event):
    checks = [
        (event.get("object_id") == state.get("object_id"), "WRONG_OBJECT"),
        (
            event.get("target_property")
            in state.get("registered_targets", []),
            "WRONG_TARGET",
        ),
        (
            event.get("source_repository") == state.get("source_repository"),
            "WRONG_SOURCE_REPOSITORY",
        ),
        (
            event.get("source_version") == state.get("source_version"),
            "WRONG_SOURCE_VERSION",
        ),
        (
            event.get("applicability_class")
            == "ASSERTION_LEVEL_ADMISSIBLE",
            "MISSING_APPLICABILITY",
        ),
        (
            bool(event.get("evidence_id"))
            and bool(event.get("evidence_locator")),
            "MISSING_EVIDENCE_BINDING",
        ),
        (
            event.get("evidence_relation") in _ALLOWED,
            "UNREGISTERED_EVIDENCE_RELATION",
        ),
        (
            bool(event.get("relation_target_claim_id")),
            "MISSING_RELATION_TARGET",
        ),
    ]
    for ok, reason in checks:
        if not ok:
            return False, reason
    return True, None


def _current_rows(state, event):
    return list(
        (state.get("assertions") or {}).get(event.get("target_property"), [])
    )


def _live_target(rows, claim_id):
    found = [x for x in rows if x.get("claim_id") == claim_id]
    return found[0] if len(found) == 1 else None


def _criticism_history(state, target_claim_id):
    found = []
    for tr in state.get("transition_ledger", []):
        if tr.get("generated_claim_id") != target_claim_id:
            continue
        if tr.get("evidence_relation") != "CONTRADICTS_PRIOR":
            continue
        if not tr.get("relation_target_claim_id"):
            continue
        found.append(tr)
    return found


def qualify(state, event):
    ok, reason = _preflight(state, event)
    if not ok:
        return {"qualified": False, "generator": None, "reason": reason}

    rows = _current_rows(state, event)
    target_id = event.get("relation_target_claim_id")
    target = _live_target(rows, target_id)

    if target is None:
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_TARGET_NOT_LIVE",
        }

    relation = event.get("evidence_relation")

    if relation == "CONTRADICTS_PRIOR":
        if target.get("value") != event.get("value"):
            return {
                "qualified": True,
                "generator": "ADD_ALTERNATIVE",
                "reason": None,
            }
        if target.get("status") != event.get("status"):
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
        hist = _criticism_history(state, target_id)
        if len(hist) != 1:
            return {
                "qualified": False,
                "generator": None,
                "reason": "RELATION_TARGET_HISTORY_UNRESOLVED",
            }

        other_same_value = []
        for row in rows:
            if row.get("claim_id") == target_id:
                continue
            if row.get("value") == event.get("value"):
                other_same_value.append(row)

        if len(rows) > 1 and len(other_same_value) == 1:
            return {
                "qualified": True,
                "generator": "RESOLVE",
                "reason": None,
                "history_support": copy.deepcopy(hist[0]),
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


def execute(state, event):
    original = copy.deepcopy(state)
    current = copy.deepcopy(state)
    bpsi = psi(original)
    bxi = xi(original)

    q = qualify(original, event)
    if not q["qualified"]:
        return {
            "engine": "target_bound_runtime_v1",
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
    proposed = _claim_from_event(current, event)

    if g == "ADD_ALTERNATIVE":
        current["assertions"][target_name] = live + [proposed]

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
            raise AssertionError("status target mismatch")
        current["assertions"][target_name] = revised

    elif g == "RESOLVE":
        current["assertions"][target_name] = [proposed]

    else:
        raise AssertionError(g)

    apsi = psi(current)

    erow = {
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "object_id": event.get("object_id"),
        "target_property": target_name,
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": event.get("new_claim_id"),
        "qualified_generator": g,
        "responsible_agent": event.get("responsible_agent"),
    }
    current.setdefault("evidence_ledger", []).append(copy.deepcopy(erow))
    current.setdefault("event_ledger", []).append({
        "event_id": event.get("event_id"),
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": event.get("new_claim_id"),
        "qualified_generator": g,
    })
    current.setdefault("transition_ledger", []).append({
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": event.get("new_claim_id"),
        "qualified_generator": g,
        "before_psi": bpsi,
        "after_psi": apsi,
    })

    return {
        "engine": "target_bound_runtime_v1",
        "qualified": True,
        "generator": g,
        "rejection_reason": None,
        "before_psi": bpsi,
        "after_psi": apsi,
        "before_xi": bxi,
        "after_xi": xi(current),
        "state": current,
        "qualification": q,
    }
