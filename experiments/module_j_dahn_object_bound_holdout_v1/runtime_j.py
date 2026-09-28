from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

from lxml import etree as LET

HERE = Path(__file__).resolve().parent
I_DIR = HERE.parent / "module_i_dahn_document_boundary_holdout_v1"
if str(I_DIR) not in sys.path:
    sys.path.insert(0, str(I_DIR))

import runtime_v2 as base

UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
INTERFACES = base.INTERFACES


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _norm(s):
    return " ".join((s or "").split())


def _object_selection(root):
    bodies = root.xpath("//*[local-name()='body']")
    if not bodies:
        return {"status": "NO_PRIMARY_DOCUMENT_OBJECT", "candidates": [], "boundary_kind": None}

    body = bodies[0]
    trans = body.xpath(".//*[local-name()='div' and @type='transcription']")
    if not trans:
        return {"status": "NO_PRIMARY_DOCUMENT_OBJECT", "candidates": [], "boundary_kind": None}

    t = trans[0]
    direct = t.xpath("./*[local-name()='div' and @type='letter']")
    if len(direct) == 1:
        return {"status": "SINGLE_PRIMARY_DOCUMENT_OBJECT", "candidates": direct, "boundary_kind": "EXPLICIT_LETTER_DIV"}
    if len(direct) > 1:
        return {"status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS", "candidates": direct, "boundary_kind": None}

    desc = t.xpath(
        ".//*[local-name()='div' and @type='letter' and "
        "not(ancestor::*[local-name()='div' and @type='annex'])]"
    )
    if len(desc) == 1:
        return {"status": "SINGLE_PRIMARY_DOCUMENT_OBJECT", "candidates": desc, "boundary_kind": "EXPLICIT_LETTER_DIV"}
    if len(desc) > 1:
        return {"status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS", "candidates": desc, "boundary_kind": None}

    if len(trans) != 1:
        return {"status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS", "candidates": trans, "boundary_kind": None}

    corresp_desc = root.xpath("//*[local-name()='correspDesc']")
    sent_actions = root.xpath("//*[local-name()='correspAction' and @type='sent']")
    substantive = bool(_norm(" ".join(t.itertext())))
    if len(corresp_desc) == 1 and sent_actions and substantive:
        return {
            "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
            "candidates": [t],
            "boundary_kind": "TRANSCRIPTION_AS_LETTER",
        }

    return {"status": "NO_PRIMARY_DOCUMENT_OBJECT", "candidates": [], "boundary_kind": None}


def object_contract(path, raw, fault=None):
    parser = LET.XMLParser(resolve_entities=False, no_network=True, recover=False)
    root = LET.fromstring(raw, parser)
    sel = _object_selection(root)
    candidates = sel["candidates"]

    if fault == "force_first_object" and len(candidates) > 1:
        candidates = [candidates[0]]
        sel = {"status": "SINGLE_PRIMARY_DOCUMENT_OBJECT", "candidates": candidates, "boundary_kind": "FAULT_FORCED_FIRST"}

    if sel["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        return {
            "status": sel["status"],
            "object_id": None,
            "candidate_count": len(candidates),
            "boundary_signature": None,
            "boundary_kind": sel["boundary_kind"],
        }

    sig = _sha(_norm(" ".join(candidates[0].itertext())).encode("utf-8"))
    payload = {
        "source_file": path,
        "source_version": UPSTREAM_COMMIT,
        "boundary_kind": sel["boundary_kind"],
        "primary_boundary_signature": sig,
    }
    oid = _sha(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return {
        "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        "object_id": oid,
        "candidate_count": 1,
        "boundary_signature": sig,
        "boundary_kind": sel["boundary_kind"],
    }


def _rekey_claim(c, object_id):
    x = copy.deepcopy(c)
    x["object_id"] = object_id
    payload = {
        "object_id": object_id,
        "role": x.get("role"),
        "interval": x.get("interval"),
        "source_file": x.get("source_file"),
        "source_locator_contract": x.get("source_locator_contract"),
        "raw_attrs": sorted((x.get("raw_attrs") or {}).items()),
        "ordinal": x.get("ordinal"),
    }
    x["claim_key"] = _sha(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return x


def parse_document(path, raw, fault=None):
    obj_fault = "force_first_object" if fault == "force_first_object" else None
    obj = object_contract(path, raw, fault=obj_fault)
    d = base.parse_document(path, raw)

    d["object_contract"] = obj
    d["object_id"] = obj["object_id"]
    d["primary_boundary_signature"] = obj["boundary_signature"]

    if obj["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        d["claims"] = []
        d["origin_claim"] = None
        d["origin_handle"] = None
        d["neutral_event"] = copy.deepcopy(base.CONTROL_NULL_EVENT)
        d["is_correspondence"] = bool(d.get("is_correspondence"))
        return d

    oid = obj["object_id"]
    claims = [_rekey_claim(c, oid) for c in d["claims"]]
    origin = _rekey_claim(d["origin_claim"], oid) if d.get("origin_claim") else None

    if fault == "cross_object_claim" and claims:
        claims[0]["object_id"] = "FOREIGN_OBJECT"
        # keep its source key otherwise intact to model a hidden cross-object injection.

    d["claims"] = claims
    d["origin_claim"] = origin
    if origin and d.get("origin_handle"):
        d["origin_handle"] = copy.deepcopy(d["origin_handle"])
        d["origin_handle"]["object_id"] = oid
        d["origin_handle"]["claim_key"] = origin["claim_key"]
    return d


def runtime_q0(doc):
    if doc.get("object_contract", {}).get("status") != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        return {"source": "none", "intervals": []}
    return base.runtime_q0(doc)


def discover(claims, expected_object_id=None):
    if not claims:
        return None
    if expected_object_id is None:
        ids = {c.get("object_id") for c in claims}
        if len(ids) != 1 or None in ids:
            return None
        expected_object_id = next(iter(ids))
    if any(c.get("object_id") != expected_object_id for c in claims):
        return None
    q = base.discover(claims)
    if q:
        q["object_id"] = expected_object_id
    return q


def make_interface(doc, arm):
    # Refuse all file-level temporal semantics unless exactly one primary scholarly object exists.
    if doc.get("object_contract", {}).get("status") != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        state = {
            "document": doc["path"],
            "object_id": None,
            "source_commit": UPSTREAM_COMMIT,
            "q0": {"source": "none", "intervals": []},
            "claims": {},
            "current_warrant": {"type": "UNRESOLVED", "reason": doc["object_contract"]["status"]},
            "live_claim_keys": [],
            "evidence_ledger": [],
            "event_ledger": [],
            "transition_ledger": [],
            "origin_handle": None,
            "history_retained": arm != "I_NO_HISTORY",
            "interface_arm": arm,
        }
        payload = {
            "document": doc["path"],
            "object_id": None,
            "object_status": doc["object_contract"]["status"],
            "source_commit": UPSTREAM_COMMIT,
            "q0": state["q0"],
            "claims": [],
            "origin_handle": None,
            "history_retained": state["history_retained"],
        }
        return state, payload

    state, payload = base.make_interface(doc, arm)
    state["object_id"] = doc["object_id"]
    payload["object_id"] = doc["object_id"]
    payload["object_status"] = doc["object_contract"]["status"]

    # NO_BINDING must remove object identity together with source binding.
    if arm == "I_NO_BINDING":
        state["object_id"] = None
        payload["object_id"] = None
        for c in state["claims"].values():
            c["object_id"] = None
    return state, payload


def apply_open_origin(state, doc, question, fault=None):
    if state.get("object_id") is None or doc.get("object_id") is None:
        before = copy.deepcopy(state)
        event_id = f"OPEN_ORIGIN::{state['document']}"
        state["event_ledger"].append({
            "event_id": event_id,
            "event_class": "EVIDENCE_RELEASE",
            "target_document": state["document"],
            "applicable": False,
        })
        transition = {
            "event_id": event_id,
            "event_class": "OPEN_ORIGIN",
            "target_document": state["document"],
            "object_id": state.get("object_id"),
            "applicable": False,
            "evidence_key": None,
            "before_warrant": before["current_warrant"],
            "after_warrant": state["current_warrant"],
            "before_temporal_digest": base.temporal_digest(before),
            "after_temporal_digest": base.temporal_digest(state),
            "changed_paths": [],
            "collateral_temporal_paths": [],
        }
        state["transition_ledger"].append(copy.deepcopy(transition))
        return state, transition

    if any(c.get("object_id") != state["object_id"] for c in state["claims"].values()):
        # Cross-object contamination makes the transition inapplicable.
        before = copy.deepcopy(state)
        event_id = f"OPEN_ORIGIN::{state['document']}"
        transition = {
            "event_id": event_id,
            "event_class": "OPEN_ORIGIN",
            "target_document": state["document"],
            "object_id": state.get("object_id"),
            "applicable": False,
            "evidence_key": None,
            "before_warrant": before["current_warrant"],
            "after_warrant": state["current_warrant"],
            "before_temporal_digest": base.temporal_digest(before),
            "after_temporal_digest": base.temporal_digest(state),
            "changed_paths": [],
            "collateral_temporal_paths": ["CROSS_OBJECT_CLAIM"],
        }
        state["transition_ledger"].append(copy.deepcopy(transition))
        return state, transition

    if question is not None and question.get("object_id") != state["object_id"]:
        question = None

    state, transition = base.apply_open_origin(state, doc, question, fault=fault)
    transition["object_id"] = state.get("object_id")
    # applicability also requires the origin claim to share object identity.
    origin = doc.get("origin_claim")
    if origin and origin.get("object_id") != state.get("object_id"):
        transition["applicable"] = False
    return state, transition


def execute(doc, arm, fault=None):
    state, payload = make_interface(doc, arm)
    q = discover(list(state["claims"].values()), expected_object_id=state.get("object_id"))

    before_open = copy.deepcopy(state)
    state, origin_transition = apply_open_origin(state, doc, q, fault=fault)

    post_origin_state = copy.deepcopy(state)
    neutral_fault = fault if fault and fault.get("type") == "neutral_mutation" else None
    state, neutral_transition, null_stable = base.apply_neutral_event(
        state, doc.get("neutral_event"), fault=neutral_fault
    )

    if arm == "I_NO_HISTORY" or (fault and fault.get("type") == "drop_history"):
        state["transition_ledger"] = []

    audit = base.delayed_audit(state)
    audit["object_id"] = state.get("object_id")

    return {
        "arm": arm,
        "payload": payload,
        "payload_bytes": len(base.canonical(payload)),
        "q0": payload["q0"],
        "question": q,
        "object_id": state.get("object_id"),
        "object_status": doc.get("object_contract", {}).get("status"),
        "open_origin_applicable": origin_transition["applicable"],
        "origin_transition": origin_transition,
        "post_origin_warrant": post_origin_state["current_warrant"],
        "post_origin_live_claim_keys": sorted(post_origin_state["live_claim_keys"]),
        "collateral_temporal_paths": origin_transition["collateral_temporal_paths"],
        "null_event_stable": null_stable,
        "neutral_transition": neutral_transition,
        "final_warrant": state["current_warrant"],
        "final_live_claim_keys": sorted(state["live_claim_keys"]),
        "delayed_audit": audit,
        "before_open_temporal_digest": base.temporal_digest(before_open),
        "post_open_temporal_digest": base.temporal_digest(post_origin_state),
        "final_temporal_digest": base.temporal_digest(state),
    }
