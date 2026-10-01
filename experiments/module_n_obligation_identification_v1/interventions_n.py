from __future__ import annotations

import copy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
if str(L_DIR) not in sys.path:
    sys.path.insert(0, str(L_DIR))

import runtime_l


ARMS = (
    "N_FULL",
    "N_NO_OBJECT_ID",
    "N_NO_APPLICABILITY",
    "N_NO_CURRENT_PROVENANCE",
    "N_NO_TRANSITION_BINDING",
    "N_COLLATERAL_UPDATE",
    "N_NO_HISTORY",
    "N_COLLAPSE_RESULT_STATUS",
)


PROVENANCE_FIELDS = (
    "source_repository",
    "source_version",
    "population_scope",
    "source_file",
    "source_locator_contract",
    "source_locator_xpath",
)


def _public_claim(c):
    return {k: copy.deepcopy(v) for k, v in c.items() if k != "_bounds"}


def _value_question(state):
    q = runtime_l.base.discover(list(state["claims"].values()))
    if q and state.get("object_id") is not None:
        q["object_id"] = state["object_id"]
    return q


def _finish(state, doc, payload, question, fault=None, drop_history=False):
    before_open = copy.deepcopy(state)
    state, origin_transition = runtime_l.apply_open_origin(
        state, doc, question, fault=fault
    )
    post_origin_state = copy.deepcopy(state)

    neutral_fault = fault if fault and fault.get("type") == "neutral_mutation" else None
    state, neutral_transition, null_stable = runtime_l.base.apply_neutral_event(
        state, doc.get("neutral_event"), fault=neutral_fault
    )

    if drop_history:
        state["transition_ledger"] = []

    audit = runtime_l.base.delayed_audit(state)
    audit["object_id"] = state.get("object_id")
    audit["source_repository"] = state.get("source_repository")
    audit["source_version"] = state.get("source_commit")

    return {
        "payload": payload,
        "q0": copy.deepcopy(payload.get("q0")),
        "root_warrant": copy.deepcopy(before_open["current_warrant"]),
        "question": copy.deepcopy(question),
        "open_origin_applicable": bool(origin_transition.get("applicable")),
        "origin_transition": copy.deepcopy(origin_transition),
        "post_origin_warrant": copy.deepcopy(post_origin_state["current_warrant"]),
        "post_origin_live_claim_keys": sorted(post_origin_state["live_claim_keys"]),
        "collateral_temporal_paths": copy.deepcopy(
            origin_transition.get("collateral_temporal_paths") or []
        ),
        "null_event_stable": bool(null_stable),
        "neutral_transition": copy.deepcopy(neutral_transition),
        "final_warrant": copy.deepcopy(state["current_warrant"]),
        "final_live_claim_keys": sorted(state["live_claim_keys"]),
        "delayed_audit": copy.deepcopy(audit),
        "surface_claims": [
            _public_claim(c) for c in state["claims"].values()
        ],
        "surface_object_id": state.get("object_id"),
        "surface_object_boundary_signature": state.get("object_boundary_signature"),
    }


def _full_trace(doc, arm="I_RSTAR", fault=None):
    trace = runtime_l.execute(doc, arm, fault=fault)
    claims = [copy.deepcopy(c) for c in doc.get("claims", [])]
    if trace.get("open_origin_applicable") and doc.get("origin_claim") is not None:
        claims.append(copy.deepcopy(doc["origin_claim"]))
    trace = copy.deepcopy(trace)
    trace["root_warrant"] = copy.deepcopy(doc.get("warrant_root"))
    trace["surface_claims"] = [_public_claim(c) for c in claims]
    trace["surface_object_id"] = doc.get("object_id")
    trace["surface_object_boundary_signature"] = doc.get(
        "primary_boundary_signature"
    )
    return trace


def _strip_current_provenance(trace):
    out = copy.deepcopy(trace)
    for c in out.get("surface_claims", []):
        for key in PROVENANCE_FIELDS:
            c[key] = None
    return out


def _collapse_warrant(warrant):
    w = copy.deepcopy(warrant or {})
    kind = w.get("type")
    if kind == "ALTERNATIVE_SET":
        alts = list(w.get("alternatives") or [])
        if not alts:
            return None
        chosen = alts[0]
        interval = chosen.get("interval")
        if not interval:
            return None
        point = interval[0] if interval[0] is not None else interval[1]
        if point is None:
            return None
        return {
            "type": "EXACT",
            "interval": [point, point],
            "basis": [chosen.get("claim_key")] if chosen.get("claim_key") else [],
            "forced_collapse": True,
        }
    if kind in ("INTERVAL", "OPEN_INTERVAL"):
        interval = list(w.get("interval") or [])
        if len(interval) != 2:
            return None
        point = interval[0] if interval[0] is not None else interval[1]
        if point is None:
            return None
        basis = list(w.get("basis") or [])
        return {
            "type": "EXACT",
            "interval": [point, point],
            "basis": basis[:1],
            "forced_collapse": True,
        }
    if kind == "UNRESOLVED":
        return {
            "type": "EXACT",
            "interval": ["FORCED_UNRESOLVED_COLLAPSE", "FORCED_UNRESOLVED_COLLAPSE"],
            "basis": [],
            "forced_collapse": True,
        }
    return None


def _collapse_result_surface(trace):
    out = copy.deepcopy(trace)
    collapsed = _collapse_warrant(out.get("post_origin_warrant"))
    if collapsed is None:
        out["result_status_intervention_applicable"] = False
        return out
    out["result_status_intervention_applicable"] = True
    out["post_origin_warrant"] = copy.deepcopy(collapsed)
    out["final_warrant"] = copy.deepcopy(collapsed)
    if collapsed.get("type") == "EXACT":
        out["post_origin_live_claim_keys"] = sorted(collapsed.get("basis") or [])
        out["final_live_claim_keys"] = sorted(collapsed.get("basis") or [])
    return out


def _mutated_binding_trace(doc, arm):
    state, payload = runtime_l.make_interface(doc, "I_RSTAR")

    if arm == "N_NO_OBJECT_ID":
        state["object_id"] = None
        state["object_boundary_signature"] = None
        payload["object_id"] = None
        payload["object_boundary_signature"] = None
        for c in state["claims"].values():
            c["object_id"] = None
            c["object_boundary_signature"] = None
        for c in payload.get("claims", []):
            c["object_id"] = None
            c["object_boundary_signature"] = None

    elif arm == "N_NO_APPLICABILITY":
        for c in state["claims"].values():
            c["applicability_class"] = None
        for c in payload.get("claims", []):
            c["applicability_class"] = None

    elif arm == "N_NO_TRANSITION_BINDING":
        state["origin_handle"] = None
        payload["origin_handle"] = None

    else:
        raise ValueError(arm)

    question = _value_question(state)
    return _finish(state, doc, payload, question)


def run_arm(doc, arm):
    if arm not in ARMS:
        raise ValueError(arm)

    if arm == "N_FULL":
        return _full_trace(doc)

    if arm in {
        "N_NO_OBJECT_ID",
        "N_NO_APPLICABILITY",
        "N_NO_TRANSITION_BINDING",
    }:
        return _mutated_binding_trace(doc, arm)

    if arm == "N_NO_CURRENT_PROVENANCE":
        return _strip_current_provenance(_full_trace(doc))

    if arm == "N_COLLATERAL_UPDATE":
        return _full_trace(doc, fault={"type": "collateral_mutation"})

    if arm == "N_NO_HISTORY":
        return _full_trace(doc, arm="I_NO_HISTORY")

    if arm == "N_COLLAPSE_RESULT_STATUS":
        return _collapse_result_surface(_full_trace(doc))

    raise AssertionError(arm)
