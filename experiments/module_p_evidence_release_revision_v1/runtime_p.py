from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
if str(L_DIR) not in sys.path:
    sys.path.insert(0, str(L_DIR))

import runtime_l


def _reason_class(value):
    r = str(value or "").strip()
    if r in ("NO_MACHINE_TEMPORAL_CARRIER", "NO_MACHINE_ROOT_CARRIER", "ROOT_EMPTY"):
        return "NO_MACHINE_TEMPORAL_CARRIER"
    return r if r else "UNSPECIFIED"


def warrant_projection(warrant):
    w = copy.deepcopy(warrant or {})
    kind = w.get("type")

    if kind == "ALTERNATIVE_SET":
        rows = [
            {
                "role": item.get("role"),
                "interval": copy.deepcopy(item.get("interval")),
            }
            for item in (w.get("alternatives") or [])
        ]
        rows = sorted(
            rows,
            key=lambda x: (
                str(x.get("role")),
                json.dumps(x.get("interval"), ensure_ascii=False, sort_keys=True),
            ),
        )
        return {"type": kind, "alternatives": rows}

    if kind in ("EXACT", "INTERVAL", "OPEN_INTERVAL"):
        return {"type": kind, "interval": copy.deepcopy(w.get("interval"))}

    if kind == "UNRESOLVED":
        return {"type": kind, "reason_class": _reason_class(w.get("reason"))}

    out = {}
    for k, v in sorted(w.items()):
        if k in ("basis", "claim_key", "live_claim_keys"):
            continue
        out[k] = copy.deepcopy(v)
    return out


def _origin_contract_ok(doc):
    origin = doc.get("origin_claim")
    ctx = doc.get("source_context") or {}
    if not origin:
        return False
    checks = (
        origin.get("object_id") == doc.get("object_id"),
        origin.get("object_boundary_signature") == doc.get("primary_boundary_signature"),
        origin.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT",
        origin.get("source_repository") == ctx.get("source_repository"),
        origin.get("source_version") == ctx.get("source_version"),
        origin.get("population_scope") == ctx.get("population_scope"),
    )
    return all(checks)


def classify_transition(before_phi, after_phi):
    if before_phi == after_phi:
        return "ADMISSIBLE_NULL_EVENT"

    bt = (before_phi or {}).get("type")
    at = (after_phi or {}).get("type")

    if bt in ("EXACT", "INTERVAL", "OPEN_INTERVAL") and at == "ALTERNATIVE_SET":
        return "P-U1_CONFLICT_FORMATION"

    if bt == "UNRESOLVED" and at in (
        "EXACT", "INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET"
    ):
        return "P-U2_RESOLUTION_OR_ACQUISITION"

    if bt == "ALTERNATIVE_SET" and at == "ALTERNATIVE_SET":
        return "P-U4_ALTERNATIVE_REVISION"

    if (
        bt not in (None, "UNRESOLVED", "ALTERNATIVE_SET")
        and at in ("EXACT", "INTERVAL", "OPEN_INTERVAL")
    ):
        return "P-U3_NARROWING_OR_QUALIFICATION"

    return "OTHER"


def parse_document(path: str, raw: bytes, source_context: dict):
    doc = runtime_l.parse_document(path, raw, source_context)

    before = warrant_projection(doc.get("warrant_root"))
    after = warrant_projection(doc.get("warrant_after"))

    reasons = []
    if (doc.get("object_contract") or {}).get("status") != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        reasons.append("NO_SINGLE_PRIMARY_OBJECT")

    origin_status = doc.get("origin_contract_status")
    if origin_status != "SINGLE_ORIGIN_ADMISSIBLE":
        reasons.append(origin_status or "NO_SINGLE_ORIGIN")
    elif not _origin_contract_ok(doc):
        reasons.append("ORIGIN_BINDING_MISMATCH")

    changed = before != after
    if reasons:
        disposition = "INELIGIBLE"
    elif changed:
        disposition = "ERIR_ELIGIBLE"
    else:
        disposition = "ADMISSIBLE_NULL_EVENT"

    doc = copy.deepcopy(doc)
    doc["p_warrant_before"] = before
    doc["p_warrant_after"] = after
    doc["p_substantive_change"] = changed
    doc["p_disposition"] = disposition
    doc["p_transition_class"] = (
        classify_transition(before, after) if not reasons else "INELIGIBLE"
    )
    doc["p_eligibility_reasons"] = reasons
    doc["p_erir_eligible"] = disposition == "ERIR_ELIGIBLE"
    doc["p_admissible_null_event"] = disposition == "ADMISSIBLE_NULL_EVENT"
    return doc


def _event_request(state):
    return {
        "type": "EVIDENCE_RELEASE_REVISION",
        "event_class": "EVIDENCE_RELEASE",
        "event_id": f"OPEN_ORIGIN::{state.get('document')}",
        "target_document": state.get("document"),
        "object_id": state.get("object_id"),
        "source_repository": state.get("source_repository"),
        "source_version": state.get("source_commit"),
        "population_scope": state.get("population_scope"),
    }


def _surface_provenance(origin, transition):
    if not origin or not transition.get("applicable"):
        return None
    return {
        "evidence_key": transition.get("evidence_key"),
        "claim_key": origin.get("claim_key"),
        "source_file": origin.get("source_file"),
        "source_locator_contract": origin.get("source_locator_contract"),
        "source_locator_xpath": origin.get("source_locator_xpath"),
        "object_id": origin.get("object_id"),
        "object_boundary_signature": origin.get("object_boundary_signature"),
        "applicability_class": origin.get("applicability_class"),
        "source_repository": origin.get("source_repository"),
        "source_version": origin.get("source_version"),
        "population_scope": origin.get("population_scope"),
    }


def execute(doc, fault=None, drop_history=False):
    state, payload = runtime_l.make_interface(doc, "I_RSTAR")
    before = copy.deepcopy(state)
    event = _event_request(state)

    action_doc = copy.deepcopy(doc)
    action_state = copy.deepcopy(state)
    translated_fault = fault

    if fault and fault.get("type") == "wrong_object":
        translated_fault = {"type": "object_context_mismatch"}

    elif fault and fault.get("type") == "wrong_source_version":
        translated_fault = {"type": "source_context_mismatch"}

    elif fault and fault.get("type") == "missing_applicability":
        translated_fault = None
        if action_state.get("origin_handle") is not None:
            action_state["origin_handle"]["applicability_class"] = None
        if action_doc.get("origin_claim") is not None:
            action_doc["origin_claim"]["applicability_class"] = None

    state, transition = runtime_l.apply_open_origin(
        action_state,
        action_doc,
        event,
        fault=translated_fault,
    )
    post = copy.deepcopy(state)

    state, neutral_transition, null_stable = runtime_l.base.apply_neutral_event(
        state,
        doc.get("neutral_event"),
        fault=None,
    )

    if drop_history or (fault and fault.get("type") == "drop_history"):
        state["transition_ledger"] = []

    audit = runtime_l.base.delayed_audit(state)
    audit["object_id"] = state.get("object_id")
    audit["source_repository"] = state.get("source_repository")
    audit["source_version"] = state.get("source_commit")

    return {
        "event_request": event,
        "root_warrant": copy.deepcopy(before.get("current_warrant")),
        "root_phi": warrant_projection(before.get("current_warrant")),
        "origin_transition": copy.deepcopy(transition),
        "post_event_warrant": copy.deepcopy(post.get("current_warrant")),
        "post_event_phi": warrant_projection(post.get("current_warrant")),
        "post_event_live_claim_keys": sorted(post.get("live_claim_keys") or []),
        # Compatibility aliases for the frozen Module-M comparator projection.
        "post_origin_warrant": copy.deepcopy(post.get("current_warrant")),
        "post_origin_live_claim_keys": sorted(post.get("live_claim_keys") or []),
        "final_warrant": copy.deepcopy(state.get("current_warrant")),
        "final_live_claim_keys": sorted(state.get("live_claim_keys") or []),
        "collateral_temporal_paths": copy.deepcopy(
            transition.get("collateral_temporal_paths") or []
        ),
        "evidence_provenance": _surface_provenance(
            action_doc.get("origin_claim"),
            transition,
        ),
        "evidence_ledger": copy.deepcopy(state.get("evidence_ledger") or []),
        "event_ledger": copy.deepcopy(state.get("event_ledger") or []),
        "transition_ledger": copy.deepcopy(state.get("transition_ledger") or []),
        "delayed_audit": copy.deepcopy(audit),
        "neutral_transition": copy.deepcopy(neutral_transition),
        "neutral_event_stable": bool(null_stable),
        "p_erir_eligible": bool(doc.get("p_erir_eligible")),
        "p_admissible_null_event": bool(doc.get("p_admissible_null_event")),
        "p_transition_class": doc.get("p_transition_class"),
        "payload": copy.deepcopy(payload),
    }
