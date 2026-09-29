from __future__ import annotations

import copy
import json

_ALLOWED = (
    "CONTRADICTS_PRIOR",
    "CORRECTION_OF_PRIOR_CRITICISM",
    "COMPETING_IDENTIFICATION",
    "BIBLIOGRAPHIC_REPLY",
)


def psi(state):
    out = []
    amap = state.get("assertions") or {}
    for target in sorted(amap):
        rows = []
        for row in amap[target]:
            rows.append({
                "claim_id": row.get("claim_id"),
                "object_id": row.get("object_id"),
                "target_property": row.get("target_property"),
                "value": copy.deepcopy(row.get("value")),
                "status": row.get("status"),
            })
        rows.sort(
            key=lambda x: json.dumps(
                x, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
        )
        out.append({"target_property": target, "assertions": rows})
    return {"object_id": state.get("object_id"), "targets": out}


def xi(state):
    return {
        "evidence_ledger": copy.deepcopy(state.get("evidence_ledger", [])),
        "event_ledger": copy.deepcopy(state.get("event_ledger", [])),
        "transition_ledger": copy.deepcopy(state.get("transition_ledger", [])),
    }


def _preflight(state, event):
    checks = (
        (
            event.get("object_id") == state.get("object_id"),
            "WRONG_OBJECT",
        ),
        (
            event.get("target_property") in state.get("registered_targets", []),
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
    )
    for ok, reason in checks:
        if not ok:
            return False, reason
    return True, None


def _live_rows(state, target_name):
    return list((state.get("assertions") or {}).get(target_name, []))


def _one_claim(rows, claim_id):
    found = [row for row in rows if row.get("claim_id") == claim_id]
    return found[0] if len(found) == 1 else None


def _originating_contradiction(state, claim_id):
    found = []
    for item in state.get("transition_ledger", []):
        if item.get("generated_claim_id") != claim_id:
            continue
        if item.get("evidence_relation") != "CONTRADICTS_PRIOR":
            continue
        found.append(item)
    return found


def qualify(state, event):
    ok, reason = _preflight(state, event)
    if not ok:
        return {
            "qualified": False,
            "generator": None,
            "reason": reason,
        }

    rows = _live_rows(state, event.get("target_property"))
    relation_target = _one_claim(
        rows, event.get("relation_target_claim_id")
    )
    if relation_target is None:
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_TARGET_NOT_LIVE",
        }

    rel = event.get("evidence_relation")

    if rel == "CONTRADICTS_PRIOR" or rel == "COMPETING_IDENTIFICATION":
        if event.get("value") != relation_target.get("value"):
            return {
                "qualified": True,
                "generator": "ADD_ALTERNATIVE",
                "reason": None,
            }
        if event.get("status") != relation_target.get("status"):
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

    if rel == "CORRECTION_OF_PRIOR_CRITICISM":
        origin = _originating_contradiction(
            state, event.get("relation_target_claim_id")
        )
        if len(origin) != 1:
            return {
                "qualified": False,
                "generator": None,
                "reason": "RELATION_TARGET_HISTORY_UNRESOLVED",
            }

        matches = []
        for row in rows:
            if row.get("claim_id") == event.get("relation_target_claim_id"):
                continue
            if row.get("value") == event.get("value"):
                matches.append(row)

        if len(rows) > 1 and len(matches) == 1:
            return {
                "qualified": True,
                "generator": "RESOLVE",
                "reason": None,
                "history_support": copy.deepcopy(origin[0]),
            }
        return {
            "qualified": False,
            "generator": None,
            "reason": "RELATION_STATE_MISMATCH",
        }

    if rel == "BIBLIOGRAPHIC_REPLY":
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


def execute(state, event):
    original = copy.deepcopy(state)
    current = copy.deepcopy(state)
    bpsi = psi(original)
    bxi = xi(original)
    q = qualify(original, event)

    if not q.get("qualified"):
        return {
            "engine": "target_bound_runtime_v2",
            "qualified": False,
            "generator": None,
            "rejection_reason": q.get("reason"),
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
            _new_claim(current, event)
        ]

    elif g == "REVISE_STATUS":
        revised = []
        seen = 0
        for row in live:
            if row.get("claim_id") == event.get("relation_target_claim_id"):
                nr = copy.deepcopy(row)
                nr["claim_id"] = event.get("new_claim_id")
                nr["status"] = event.get("status")
                nr["source_id"] = event.get("evidence_id")
                nr["source_locator"] = event.get("evidence_locator")
                nr["responsible_agent"] = event.get("responsible_agent")
                revised.append(nr)
                seen += 1
            else:
                revised.append(row)
        if seen != 1:
            raise AssertionError("qualified status revision without one live target")
        current["assertions"][target_name] = revised

    elif g == "RESOLVE":
        current["assertions"][target_name] = [
            _new_claim(current, event)
        ]

    elif g == "RECORD_EVIDENCE":
        pass

    else:
        raise AssertionError(g)

    apsi = psi(current)
    generated = event.get("new_claim_id") if g != "RECORD_EVIDENCE" else None

    evidence_row = {
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "object_id": event.get("object_id"),
        "target_property": target_name,
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": generated,
        "qualified_generator": g,
        "responsible_agent": event.get("responsible_agent"),
        "mediator_agent": event.get("mediator_agent"),
    }
    current.setdefault("evidence_ledger", []).append(
        copy.deepcopy(evidence_row)
    )
    current.setdefault("event_ledger", []).append({
        "event_id": event.get("event_id"),
        "evidence_relation": event.get("evidence_relation"),
        "relation_target_claim_id": event.get("relation_target_claim_id"),
        "generated_claim_id": generated,
        "qualified_generator": g,
        "responsible_agent": event.get("responsible_agent"),
        "mediator_agent": event.get("mediator_agent"),
    })
    current.setdefault("transition_ledger", []).append({
        **copy.deepcopy(evidence_row),
        "before_psi": bpsi,
        "after_psi": apsi,
        "assertion_identity": bpsi == apsi,
        "history_nonidentity": True,
    })

    return {
        "engine": "target_bound_runtime_v2",
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
