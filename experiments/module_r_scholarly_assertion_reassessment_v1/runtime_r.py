from __future__ import annotations

import copy
import json


def psi(state):
    buckets = []
    keys = list(state.get("assertions", {}).keys())
    keys.sort()
    for key in keys:
        vals = []
        for a in state["assertions"][key]:
            vals.append({
                "object_id": a.get("object_id"),
                "target_property": a.get("target_property"),
                "value": copy.deepcopy(a.get("value")),
                "status": a.get("status"),
            })
        vals = sorted(
            vals,
            key=lambda x: json.dumps(
                x,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ),
        )
        buckets.append({"target_property": key, "assertions": vals})
    return {"object_id": state.get("object_id"), "targets": buckets}


def _can_apply(state, event):
    if event.get("object_id") != state.get("object_id"):
        return False, "WRONG_OBJECT"
    if event.get("target_property") not in state.get("registered_targets", []):
        return False, "WRONG_TARGET"
    if event.get("source_repository") != state.get("source_repository"):
        return False, "WRONG_SOURCE_REPOSITORY"
    if event.get("source_version") != state.get("source_version"):
        return False, "WRONG_SOURCE_VERSION"
    if event.get("applicability_class") != "ASSERTION_LEVEL_ADMISSIBLE":
        return False, "MISSING_APPLICABILITY"
    if not event.get("evidence_id") or not event.get("evidence_locator"):
        return False, "MISSING_EVIDENCE_BINDING"
    if event.get("operation") not in (
        "REPLACE", "ADD_ALTERNATIVE", "REVISE_STATUS", "RESOLVE"
    ):
        return False, "UNKNOWN_OPERATION"
    return True, None


def _make_assertion(state, event):
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


def _class_for(op, substantive):
    if not substantive:
        return "ADMISSIBLE_NULL_EVENT"
    if op == "REPLACE":
        return "R-U1_ATTRIBUTION_REPLACEMENT"
    if op == "ADD_ALTERNATIVE":
        return "R-U2_ALTERNATIVE_FORMATION"
    if op == "REVISE_STATUS":
        return "R-U3_EVIDENTIAL_STATUS_REVISION"
    if op == "RESOLVE":
        return "R-U4_RESOLUTION"
    return "OTHER"


def execute(state, event, fault=None, drop_history=False):
    s = copy.deepcopy(state)
    before = copy.deepcopy(s)
    before_view = psi(before)

    if fault:
        event = copy.deepcopy(event)
        kind = fault.get("type")
        if kind == "wrong_object":
            event["object_id"] = "FOREIGN_OBJECT"
        elif kind == "wrong_target":
            event["target_property"] = "foreign-property"
        elif kind == "wrong_source_version":
            event["source_version"] = "FOREIGN_VERSION"
        elif kind == "missing_applicability":
            event["applicability_class"] = None

    ok, reason = _can_apply(s, event)
    transition = {
        "event_id": event.get("event_id"),
        "event_class": event.get("event_class"),
        "object_id": event.get("object_id"),
        "target_property": event.get("target_property"),
        "applicable": ok,
        "rejection_reason": reason,
        "evidence_id": None,
        "before_state": before_view,
        "after_state": before_view,
        "substantive": False,
        "transition_class": "REJECTED" if not ok else None,
        "changed_targets": [],
        "collateral_targets": [],
    }

    if ok:
        target = event["target_property"]
        old = copy.deepcopy(s["assertions"].get(target, []))
        new = _make_assertion(s, event)
        op = event["operation"]

        if op == "REPLACE":
            s["assertions"][target] = [new]
        elif op == "ADD_ALTERNATIVE":
            s["assertions"][target] = old + [new]
        elif op == "REVISE_STATUS":
            found = False
            rows = []
            for a in old:
                if a.get("value") == event.get("value"):
                    b = copy.deepcopy(a)
                    b["claim_id"] = event.get("new_claim_id")
                    b["status"] = event.get("status")
                    b["source_id"] = event.get("evidence_id")
                    b["source_locator"] = event.get("evidence_locator")
                    b["responsible_agent"] = event.get("responsible_agent")
                    rows.append(b)
                    found = True
                else:
                    rows.append(a)
            if not found:
                ok = False
                reason = "NO_VALUE_MATCH"
                s = copy.deepcopy(before)
            else:
                s["assertions"][target] = rows
        elif op == "RESOLVE":
            s["assertions"][target] = [new]

        if ok and fault and fault.get("type") == "collateral_mutation":
            collateral_target = fault.get("target_property") or "source-status"
            if collateral_target in s["assertions"] and collateral_target != target:
                s["assertions"][collateral_target][0]["status"] = "FAULT_MUTATED"

        after_view = psi(s)
        substantive = before_view != after_view

        transition.update({
            "applicable": ok,
            "rejection_reason": reason,
            "evidence_id": event.get("evidence_id") if ok else None,
            "after_state": after_view if ok else before_view,
            "substantive": substantive if ok else False,
            "transition_class": (
                _class_for(op, substantive) if ok else "REJECTED_NO_VALUE_MATCH"
            ),
            "changed_targets": (
                [target] if ok and substantive else []
            ),
            "collateral_targets": [],
        })

        if ok:
            # Detect task-unrelated assertion changes.
            for t in sorted(set(before["assertions"]) | set(s["assertions"])):
                if t == target:
                    continue
                b = psi({
                    "object_id": before["object_id"],
                    "assertions": {t: before["assertions"].get(t, [])},
                })
                a = psi({
                    "object_id": s["object_id"],
                    "assertions": {t: s["assertions"].get(t, [])},
                })
                if a != b:
                    transition["collateral_targets"].append(t)

    if transition["applicable"]:
        s.setdefault("evidence_ledger", []).append({
            "event_id": event.get("event_id"),
            "evidence_id": event.get("evidence_id"),
            "evidence_locator": event.get("evidence_locator"),
            "source_repository": event.get("source_repository"),
            "source_version": event.get("source_version"),
            "target_property": event.get("target_property"),
        })
        s.setdefault("event_ledger", []).append({
            "event_id": event.get("event_id"),
            "event_class": event.get("event_class"),
            "object_id": event.get("object_id"),
            "target_property": event.get("target_property"),
            "responsible_agent": event.get("responsible_agent"),
        })

    s.setdefault("transition_ledger", []).append(copy.deepcopy(transition))

    current_provenance = []
    for target in sorted(s.get("assertions", {})):
        for a in s["assertions"][target]:
            current_provenance.append({
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

    current_provenance.sort(
        key=lambda x: (str(x.get("target_property")), str(x.get("claim_id")))
    )

    if fault and fault.get("type") == "hide_current_provenance":
        current_provenance = []

    if drop_history or (fault and fault.get("type") == "drop_history"):
        s["transition_ledger"] = []

    audit_transition = next(
        (x for x in s.get("transition_ledger", []) if x.get("applicable")),
        None,
    )
    audit_evidence = next(
        (x for x in s.get("evidence_ledger", []) if x.get("event_id") == event.get("event_id")),
        None,
    )

    delayed_audit = {
        "event_id": audit_transition.get("event_id") if audit_transition else None,
        "object_id": audit_transition.get("object_id") if audit_transition else None,
        "target_property": (
            audit_transition.get("target_property") if audit_transition else None
        ),
        "evidence_id": audit_evidence.get("evidence_id") if audit_evidence else None,
        "before_state": (
            copy.deepcopy(audit_transition.get("before_state"))
            if audit_transition else None
        ),
        "after_state": (
            copy.deepcopy(audit_transition.get("after_state"))
            if audit_transition else None
        ),
        "transition_class": (
            audit_transition.get("transition_class") if audit_transition else None
        ),
    }

    return {
        "before_state": before_view,
        "after_state": psi(s),
        "transition": transition,
        "current_provenance": current_provenance,
        "delayed_audit": delayed_audit,
        "state": s,
    }


def current_reopen(output):
    return {
        "regime": "B_CURRENT_REOPEN_R",
        "current_state": copy.deepcopy(output["after_state"]),
        "current_provenance": copy.deepcopy(output["current_provenance"]),
    }


def ordered_snapshots(output):
    return {
        "regime": "B_ORDERED_SNAPSHOTS_R",
        "S0": copy.deepcopy(output["before_state"]),
        "S1": copy.deepcopy(output["after_state"]),
        "delta": {
            "changed_targets": copy.deepcopy(
                output["transition"].get("changed_targets") or []
            ),
            "collateral_targets": copy.deepcopy(
                output["transition"].get("collateral_targets") or []
            ),
        },
        "current_provenance": copy.deepcopy(output["current_provenance"]),
    }


def change_log_no_justification(output):
    tr = output["transition"]
    return {
        "regime": "B_CHANGE_LOG_NO_JUSTIFICATION_R",
        "event_id": tr.get("event_id"),
        "event_class": tr.get("event_class"),
        "object_id": tr.get("object_id"),
        "target_property": tr.get("target_property"),
        "before_state": copy.deepcopy(tr.get("before_state")),
        "after_state": copy.deepcopy(tr.get("after_state")),
        "changed_targets": copy.deepcopy(tr.get("changed_targets") or []),
        # Deliberately omits evidence_id / source / justification.
    }
