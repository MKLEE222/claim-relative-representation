from __future__ import annotations

import copy
import json

_ALLOWED_RELATIONS = (
    "CONTRADICTS_PRIOR",
    "REPLACES_PRIOR",
    "NARROWS_PRIOR",
    "ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT",
    "CORROBORATES_PRIOR",
    "NO_VERIFIED_CONTRAST",
)


def psi(state):
    buckets = []
    for target in sorted((state.get("assertions") or {}).keys()):
        vals = []
        for row in state["assertions"][target]:
            vals.append({
                "object_id": row.get("object_id"),
                "target_property": row.get("target_property"),
                "value": copy.deepcopy(row.get("value")),
                "status": row.get("status"),
            })
        vals.sort(
            key=lambda x: json.dumps(
                x, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
        )
        buckets.append({"target_property": target, "assertions": vals})
    return {"object_id": state.get("object_id"), "targets": buckets}


def xi(state):
    return {
        "evidence_ledger": copy.deepcopy(state.get("evidence_ledger", [])),
        "event_ledger": copy.deepcopy(state.get("event_ledger", [])),
        "transition_ledger": copy.deepcopy(state.get("transition_ledger", [])),
    }


def _binding_ok(state, event):
    checks = (
        event.get("object_id") == state.get("object_id"),
        event.get("target_property") in state.get("registered_targets", []),
        event.get("source_repository") == state.get("source_repository"),
        event.get("source_version") == state.get("source_version"),
        event.get("applicability_class") == "ASSERTION_LEVEL_ADMISSIBLE",
        bool(event.get("evidence_id")),
        bool(event.get("evidence_locator")),
        event.get("evidence_relation") in _ALLOWED_RELATIONS,
    )
    if all(checks):
        return True, None
    reasons = [
        "WRONG_OBJECT",
        "WRONG_TARGET",
        "WRONG_SOURCE_REPOSITORY",
        "WRONG_SOURCE_VERSION",
        "MISSING_APPLICABILITY",
        "MISSING_EVIDENCE_ID",
        "MISSING_EVIDENCE_LOCATOR",
        "UNREGISTERED_EVIDENCE_RELATION",
    ]
    for ok, reason in zip(checks, reasons):
        if not ok:
            return False, reason
    return False, "BINDING_FAILURE"


def _inspect_target(state, event):
    rows = list(
        (state.get("assertions") or {}).get(event.get("target_property"), [])
    )
    same_value_rows = [
        x for x in rows if x.get("value") == event.get("value")
    ]
    exact_rows = [
        x for x in same_value_rows
        if x.get("status") == event.get("status")
    ]
    unresolved = (
        len(rows) == 1
        and (
            rows[0].get("status") == "UNRESOLVED"
            or rows[0].get("value") == "NO_EXPLICIT_ASSIGNMENT"
        )
    )
    return rows, same_value_rows, exact_rows, unresolved


def qualify(state, event):
    ok, reason = _binding_ok(state, event)
    if not ok:
        return {
            "qualified": False,
            "generator": None,
            "reason": reason,
            "evidence_relation": event.get("evidence_relation"),
        }

    rows, same_value_rows, exact_rows, unresolved = _inspect_target(
        state, event
    )
    relation = event.get("evidence_relation")
    generator = None

    if relation == "CORROBORATES_PRIOR":
        generator = "RECORD_EVIDENCE" if exact_rows else None

    elif relation == "CONTRADICTS_PRIOR":
        if same_value_rows and not exact_rows:
            generator = "REVISE_STATUS"
        elif rows and not unresolved and not same_value_rows:
            generator = "ADD_ALTERNATIVE"

    elif relation == "REPLACES_PRIOR":
        if len(rows) > 1:
            matching_values = [
                x for x in rows if x.get("value") == event.get("value")
            ]
            if len(matching_values) == 1:
                generator = "RESOLVE"
        if generator is None and rows:
            generator = "REPLACE"

    elif relation == "NARROWS_PRIOR":
        if same_value_rows and not exact_rows:
            generator = "REVISE_STATUS"
        elif rows:
            generator = "REPLACE"

    elif relation == "ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT":
        if unresolved:
            generator = "RESOLVE"
        elif exact_rows:
            generator = "RECORD_EVIDENCE"

    elif relation == "NO_VERIFIED_CONTRAST":
        return {
            "qualified": False,
            "generator": None,
            "reason": "NO_VERIFIED_CONTRAST",
            "evidence_relation": relation,
            "state_predicates": {
                "same_pair": bool(exact_rows),
                "same_value": bool(same_value_rows),
                "single_unresolved": unresolved,
                "alternative_state": len(rows) > 1,
            },
        }

    return {
        "qualified": generator is not None,
        "generator": generator,
        "reason": None if generator else "RELATION_STATE_MISMATCH",
        "evidence_relation": relation,
        "state_predicates": {
            "same_pair": bool(exact_rows),
            "same_value": bool(same_value_rows),
            "single_unresolved": unresolved,
            "alternative_state": len(rows) > 1,
        },
    }


def _assertion_from_event(state, event):
    return {
        "claim_id": event.get("new_claim_id"),
        "object_id": state.get("object_id"),
        "target_property": event.get("target_property"),
        "value": copy.deepcopy(event.get("value")),
        "status": event.get("status"),
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "source_repository": event.get("source_repository"),
        "source_version": event.get("source_version"),
        "source_id": event.get("evidence_id"),
        "source_locator": event.get("evidence_locator"),
        "responsible_agent": event.get("responsible_agent"),
    }


def _class(generator, assertion_identity):
    if generator == "RECORD_EVIDENCE" or assertion_identity:
        return "ASSERTION_IDENTITY_HISTORY_NONIDENTITY"
    if generator == "REPLACE":
        return "QG_REPLACEMENT"
    if generator == "ADD_ALTERNATIVE":
        return "QG_ALTERNATIVE_FORMATION"
    if generator == "REVISE_STATUS":
        return "QG_STATUS_REVISION"
    if generator == "RESOLVE":
        return "QG_RESOLUTION"
    return "QG_OTHER"


def execute(state, event):
    original = copy.deepcopy(state)
    current = copy.deepcopy(state)
    before_psi = psi(original)
    before_xi = xi(original)
    q = qualify(original, event)

    if not q.get("qualified"):
        return {
            "engine": "qualified_runtime_v1",
            "qualified": False,
            "generator": None,
            "rejection_reason": q.get("reason"),
            "evidence_relation": event.get("evidence_relation"),
            "before_psi": before_psi,
            "after_psi": before_psi,
            "before_xi": before_xi,
            "after_xi": before_xi,
            "assertion_identity": True,
            "history_nonidentity": False,
            "transition_class": "REJECTED",
            "state": current,
            "qualification": q,
        }

    generator = q["generator"]
    target = event["target_property"]
    existing = copy.deepcopy(current["assertions"].get(target, []))
    replacement = _assertion_from_event(current, event)

    if generator == "REPLACE":
        current["assertions"][target] = [replacement]

    elif generator == "ADD_ALTERNATIVE":
        current["assertions"][target] = existing + [replacement]

    elif generator == "REVISE_STATUS":
        revised = []
        count = 0
        for row in existing:
            if row.get("value") == event.get("value"):
                new_row = copy.deepcopy(row)
                new_row.update({
                    "claim_id": event.get("new_claim_id"),
                    "status": event.get("status"),
                    "source_id": event.get("evidence_id"),
                    "source_locator": event.get("evidence_locator"),
                    "responsible_agent": event.get("responsible_agent"),
                })
                revised.append(new_row)
                count += 1
            else:
                revised.append(row)
        if count == 0:
            raise AssertionError("qualified status revision lacks value match")
        current["assertions"][target] = revised

    elif generator == "RESOLVE":
        current["assertions"][target] = [replacement]

    elif generator == "RECORD_EVIDENCE":
        pass

    else:
        raise AssertionError(generator)

    after_psi = psi(current)
    assertion_identity = before_psi == after_psi

    evidence_row = {
        "event_id": event.get("event_id"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "source_repository": event.get("source_repository"),
        "source_version": event.get("source_version"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_relation": event.get("evidence_relation"),
        "qualified_generator": generator,
        "responsible_agent": event.get("responsible_agent"),
    }
    current.setdefault("evidence_ledger", []).append(
        copy.deepcopy(evidence_row)
    )
    current.setdefault("event_ledger", []).append({
        "event_id": event.get("event_id"),
        "event_class": event.get("event_class"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_relation": event.get("evidence_relation"),
        "qualified_generator": generator,
    })
    current.setdefault("transition_ledger", []).append({
        "event_id": event.get("event_id"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_id": event.get("evidence_id"),
        "evidence_relation": event.get("evidence_relation"),
        "qualified_generator": generator,
        "before_psi": before_psi,
        "after_psi": after_psi,
        "assertion_identity": assertion_identity,
        "history_nonidentity": True,
    })

    after_xi = xi(current)

    return {
        "engine": "qualified_runtime_v1",
        "qualified": True,
        "generator": generator,
        "rejection_reason": None,
        "evidence_relation": event.get("evidence_relation"),
        "before_psi": before_psi,
        "after_psi": after_psi,
        "before_xi": before_xi,
        "after_xi": after_xi,
        "assertion_identity": assertion_identity,
        "history_nonidentity": before_xi != after_xi,
        "transition_class": _class(generator, assertion_identity),
        "state": current,
        "qualification": q,
    }
