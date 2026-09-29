from __future__ import annotations

import copy
import json

RELATIONS = {
    "CONTRADICTS_PRIOR",
    "REPLACES_PRIOR",
    "NARROWS_PRIOR",
    "ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT",
    "CORROBORATES_PRIOR",
    "NO_VERIFIED_CONTRAST",
}

GENERATORS = {
    "RECORD_EVIDENCE",
    "REPLACE",
    "ADD_ALTERNATIVE",
    "REVISE_STATUS",
    "RESOLVE",
}


def psi(state):
    rows = []
    for target in sorted((state.get("assertions") or {})):
        assertions = []
        for a in state["assertions"][target]:
            assertions.append({
                "object_id": a.get("object_id"),
                "target_property": a.get("target_property"),
                "value": copy.deepcopy(a.get("value")),
                "status": a.get("status"),
            })
        assertions.sort(
            key=lambda x: json.dumps(
                x, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
        )
        rows.append({"target_property": target, "assertions": assertions})
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
    if event.get("evidence_relation") not in RELATIONS:
        return "UNREGISTERED_EVIDENCE_RELATION"
    return None


def _target_rows(state, event):
    return list((state.get("assertions") or {}).get(event.get("target_property"), []))


def _same_pair(rows, event):
    return any(
        x.get("value") == event.get("value")
        and x.get("status") == event.get("status")
        for x in rows
    )


def _same_value(rows, event):
    return any(x.get("value") == event.get("value") for x in rows)


def _single_unresolved(rows):
    return (
        len(rows) == 1
        and (
            rows[0].get("status") == "UNRESOLVED"
            or rows[0].get("value") == "NO_EXPLICIT_ASSIGNMENT"
        )
    )


def qualify(state, event):
    reason = _binding_reason(state, event)
    if reason:
        return {
            "qualified": False,
            "generator": None,
            "reason": reason,
            "evidence_relation": event.get("evidence_relation"),
        }

    rows = _target_rows(state, event)
    relation = event.get("evidence_relation")
    same_pair = _same_pair(rows, event)
    same_value = _same_value(rows, event)
    single_unresolved = _single_unresolved(rows)
    alternative_state = len(rows) > 1

    generator = None
    reason = None

    if relation == "CORROBORATES_PRIOR":
        if same_pair:
            generator = "RECORD_EVIDENCE"
        else:
            reason = "RELATION_STATE_MISMATCH"

    elif relation == "CONTRADICTS_PRIOR":
        if same_value and not same_pair:
            generator = "REVISE_STATUS"
        elif rows and not single_unresolved and not same_value:
            generator = "ADD_ALTERNATIVE"
        else:
            reason = "RELATION_STATE_MISMATCH"

    elif relation == "REPLACES_PRIOR":
        value_matches = [x for x in rows if x.get("value") == event.get("value")]
        if alternative_state and len(value_matches) == 1:
            generator = "RESOLVE"
        elif rows:
            generator = "REPLACE"
        else:
            reason = "RELATION_STATE_MISMATCH"

    elif relation == "NARROWS_PRIOR":
        if same_value and not same_pair:
            generator = "REVISE_STATUS"
        elif rows:
            generator = "REPLACE"
        else:
            reason = "RELATION_STATE_MISMATCH"

    elif relation == "ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT":
        if single_unresolved:
            generator = "RESOLVE"
        elif same_pair:
            generator = "RECORD_EVIDENCE"
        else:
            reason = "RELATION_STATE_MISMATCH"

    elif relation == "NO_VERIFIED_CONTRAST":
        reason = "NO_VERIFIED_CONTRAST"

    return {
        "qualified": generator is not None,
        "generator": generator,
        "reason": reason,
        "evidence_relation": relation,
        "state_predicates": {
            "same_pair": same_pair,
            "same_value": same_value,
            "single_unresolved": single_unresolved,
            "alternative_state": alternative_state,
        },
    }


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


def _transition_class(generator, assertion_identity):
    if generator == "RECORD_EVIDENCE":
        return "ASSERTION_IDENTITY_HISTORY_NONIDENTITY"
    if assertion_identity:
        return "ASSERTION_IDENTITY_HISTORY_NONIDENTITY"
    return {
        "REPLACE": "QG_REPLACEMENT",
        "ADD_ALTERNATIVE": "QG_ALTERNATIVE_FORMATION",
        "REVISE_STATUS": "QG_STATUS_REVISION",
        "RESOLVE": "QG_RESOLUTION",
    }.get(generator, "QG_OTHER")


def apply(state, event):
    before = copy.deepcopy(state)
    before_psi = psi(before)
    before_xi = xi(before)
    out = copy.deepcopy(state)

    q = qualify(before, event)
    if not q["qualified"]:
        return {
            "engine": "qualified_oracle_v1",
            "qualified": False,
            "generator": None,
            "rejection_reason": q["reason"],
            "evidence_relation": event.get("evidence_relation"),
            "before_psi": before_psi,
            "after_psi": before_psi,
            "before_xi": before_xi,
            "after_xi": before_xi,
            "assertion_identity": True,
            "history_nonidentity": False,
            "transition_class": "REJECTED",
            "state": out,
            "qualification": q,
        }

    generator = q["generator"]
    target = event.get("target_property")
    rows = copy.deepcopy(out["assertions"].get(target, []))
    new = _new_assertion(out, event)

    if generator == "RECORD_EVIDENCE":
        pass
    elif generator == "REPLACE":
        out["assertions"][target] = [new]
    elif generator == "ADD_ALTERNATIVE":
        out["assertions"][target] = rows + [new]
    elif generator == "REVISE_STATUS":
        updated = []
        matched = False
        for row in rows:
            if row.get("value") == event.get("value"):
                x = copy.deepcopy(row)
                x["claim_id"] = event.get("new_claim_id")
                x["status"] = event.get("status")
                x["source_id"] = event.get("evidence_id")
                x["source_locator"] = event.get("evidence_locator")
                x["responsible_agent"] = event.get("responsible_agent")
                updated.append(x)
                matched = True
            else:
                updated.append(row)
        if not matched:
            raise AssertionError("qualified REVISE_STATUS without matching value")
        out["assertions"][target] = updated
    elif generator == "RESOLVE":
        out["assertions"][target] = [new]
    else:
        raise AssertionError(generator)

    after_psi_preledger = psi(out)
    assertion_identity = before_psi == after_psi_preledger

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
    out.setdefault("evidence_ledger", []).append(copy.deepcopy(evidence_row))
    out.setdefault("event_ledger", []).append({
        "event_id": event.get("event_id"),
        "event_class": event.get("event_class"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_relation": event.get("evidence_relation"),
        "qualified_generator": generator,
    })

    transition_row = {
        "event_id": event.get("event_id"),
        "object_id": event.get("object_id"),
        "target_property": target,
        "evidence_id": event.get("evidence_id"),
        "evidence_relation": event.get("evidence_relation"),
        "qualified_generator": generator,
        "before_psi": before_psi,
        "after_psi": after_psi_preledger,
        "assertion_identity": assertion_identity,
        "history_nonidentity": True,
    }
    out.setdefault("transition_ledger", []).append(copy.deepcopy(transition_row))

    after_xi = xi(out)

    return {
        "engine": "qualified_oracle_v1",
        "qualified": True,
        "generator": generator,
        "rejection_reason": None,
        "evidence_relation": event.get("evidence_relation"),
        "before_psi": before_psi,
        "after_psi": after_psi_preledger,
        "before_xi": before_xi,
        "after_xi": after_xi,
        "assertion_identity": assertion_identity,
        "history_nonidentity": before_xi != after_xi,
        "transition_class": _transition_class(generator, assertion_identity),
        "state": out,
        "qualification": q,
    }
