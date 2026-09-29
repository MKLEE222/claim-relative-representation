from __future__ import annotations

import copy
import json


def _proj_assertion(a):
    return {
        "object_id": a.get("object_id"),
        "target_property": a.get("target_property"),
        "value": copy.deepcopy(a.get("value")),
        "status": a.get("status"),
    }


def psi(state):
    rows = []
    for target in sorted(state.get("assertions", {})):
        vals = [_proj_assertion(x) for x in state["assertions"][target]]
        vals.sort(key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
        rows.append({"target_property": target, "assertions": vals})
    return {
        "object_id": state.get("object_id"),
        "targets": rows,
    }


def event_applicable(state, event):
    return all([
        event.get("object_id") == state.get("object_id"),
        event.get("target_property") in state.get("registered_targets", []),
        event.get("source_repository") == state.get("source_repository"),
        event.get("source_version") == state.get("source_version"),
        event.get("applicability_class") == "ASSERTION_LEVEL_ADMISSIBLE",
        bool(event.get("evidence_id")),
        bool(event.get("evidence_locator")),
        event.get("operation") in {
            "REPLACE", "ADD_ALTERNATIVE", "REVISE_STATUS", "RESOLVE"
        },
    ])


def _new_assertion(state, event):
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


def _transition_class(operation):
    return {
        "REPLACE": "R-U1_ATTRIBUTION_REPLACEMENT",
        "ADD_ALTERNATIVE": "R-U2_ALTERNATIVE_FORMATION",
        "REVISE_STATUS": "R-U3_EVIDENTIAL_STATUS_REVISION",
        "RESOLVE": "R-U4_RESOLUTION",
    }.get(operation, "OTHER")


def apply_event(state, event):
    before = copy.deepcopy(state)
    before_psi = psi(before)
    out = copy.deepcopy(state)

    if not event_applicable(before, event):
        return {
            "applicable": False,
            "event_id": event.get("event_id"),
            "event_class": event.get("event_class"),
            "object_id": event.get("object_id"),
            "target_property": event.get("target_property"),
            "evidence_id": None,
            "before_state": before_psi,
            "after_state": before_psi,
            "substantive": False,
            "transition_class": "REJECTED",
            "changed_targets": [],
            "collateral_targets": [],
            "state": out,
        }

    target = event["target_property"]
    current = copy.deepcopy(out["assertions"].get(target, []))
    new = _new_assertion(out, event)
    op = event["operation"]

    if op == "REPLACE":
        out["assertions"][target] = [new]
    elif op == "ADD_ALTERNATIVE":
        out["assertions"][target] = current + [new]
    elif op == "REVISE_STATUS":
        matched = [x for x in current if x.get("value") == event.get("value")]
        if not matched:
            return {
                "applicable": False,
                "event_id": event.get("event_id"),
                "event_class": event.get("event_class"),
                "object_id": event.get("object_id"),
                "target_property": target,
                "evidence_id": None,
                "before_state": before_psi,
                "after_state": before_psi,
                "substantive": False,
                "transition_class": "REJECTED_NO_VALUE_MATCH",
                "changed_targets": [],
                "collateral_targets": [],
                "state": out,
            }
        rows = []
        for x in current:
            if x.get("value") == event.get("value"):
                y = copy.deepcopy(x)
                y["claim_id"] = event.get("new_claim_id")
                y["status"] = event.get("status")
                y["source_id"] = event.get("evidence_id")
                y["source_locator"] = event.get("evidence_locator")
                y["responsible_agent"] = event.get("responsible_agent")
                rows.append(y)
            else:
                rows.append(x)
        out["assertions"][target] = rows
    elif op == "RESOLVE":
        out["assertions"][target] = [new]

    after_psi = psi(out)
    substantive = before_psi != after_psi

    return {
        "applicable": True,
        "event_id": event.get("event_id"),
        "event_class": event.get("event_class"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_id": event.get("evidence_id"),
        "before_state": before_psi,
        "after_state": after_psi,
        "substantive": substantive,
        "transition_class": (
            _transition_class(op) if substantive else "ADMISSIBLE_NULL_EVENT"
        ),
        "changed_targets": [target] if substantive else [],
        "collateral_targets": [],
        "state": out,
    }


def expected_current_provenance(state):
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
