from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
if str(L_DIR) not in sys.path:
    sys.path.insert(0, str(L_DIR))

import oracle_l


def _norm_reason(reason):
    r = str(reason or "").strip()
    if r in {"NO_MACHINE_TEMPORAL_CARRIER", "NO_MACHINE_ROOT_CARRIER", "ROOT_EMPTY"}:
        return "NO_MACHINE_TEMPORAL_CARRIER"
    return r or "UNSPECIFIED"


def warrant_projection(warrant):
    w = copy.deepcopy(warrant or {})
    kind = w.get("type")

    if kind in {"EXACT", "INTERVAL", "OPEN_INTERVAL"}:
        return {
            "type": kind,
            "interval": copy.deepcopy(w.get("interval")),
        }

    if kind == "ALTERNATIVE_SET":
        alts = []
        for x in w.get("alternatives") or []:
            alts.append({
                "role": x.get("role"),
                "interval": copy.deepcopy(x.get("interval")),
            })
        alts.sort(
            key=lambda x: (
                str(x.get("role")),
                json.dumps(x.get("interval"), ensure_ascii=False, sort_keys=True),
            )
        )
        return {"type": "ALTERNATIVE_SET", "alternatives": alts}

    if kind == "UNRESOLVED":
        return {
            "type": "UNRESOLVED",
            "reason_class": _norm_reason(w.get("reason")),
        }

    return {
        k: copy.deepcopy(v)
        for k, v in sorted(w.items())
        if k not in {"basis", "claim_key", "live_claim_keys"}
    }


def _origin_binding_ok(doc):
    origin = doc.get("origin_claim")
    ctx = doc.get("source_context") or {}
    if origin is None:
        return False
    return all([
        origin.get("object_id") == doc.get("object_id"),
        origin.get("object_boundary_signature") == doc.get("primary_boundary_signature"),
        origin.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT",
        origin.get("source_repository") == ctx.get("source_repository"),
        origin.get("source_version") == ctx.get("source_version"),
        origin.get("population_scope") == ctx.get("population_scope"),
    ])


def classify_transition(before_phi, after_phi):
    bt = (before_phi or {}).get("type")
    at = (after_phi or {}).get("type")

    if before_phi == after_phi:
        return "ADMISSIBLE_NULL_EVENT"

    if bt == "UNRESOLVED" and at in {
        "EXACT", "INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET"
    }:
        return "P-U2_RESOLUTION_OR_ACQUISITION"

    if bt in {"EXACT", "INTERVAL", "OPEN_INTERVAL"} and at == "ALTERNATIVE_SET":
        return "P-U1_CONFLICT_FORMATION"

    if bt == "ALTERNATIVE_SET" and at == "ALTERNATIVE_SET":
        return "P-U4_ALTERNATIVE_REVISION"

    if bt not in {None, "UNRESOLVED", "ALTERNATIVE_SET"} and at in {
        "EXACT", "INTERVAL", "OPEN_INTERVAL"
    }:
        return "P-U3_NARROWING_OR_QUALIFICATION"

    return "OTHER"


def parse_document(path: str, raw: bytes, source_context: dict):
    doc = oracle_l.parse_document(path, raw, source_context)

    before_phi = warrant_projection(doc.get("warrant_root"))
    after_phi = warrant_projection(doc.get("warrant_after"))

    status = (doc.get("object_contract") or {}).get("status")
    origin_status = doc.get("origin_contract_status")

    reasons = []
    if status != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        reasons.append("NO_SINGLE_PRIMARY_OBJECT")
    if origin_status != "SINGLE_ORIGIN_ADMISSIBLE":
        reasons.append(origin_status or "NO_SINGLE_ORIGIN")
    if origin_status == "SINGLE_ORIGIN_ADMISSIBLE" and not _origin_binding_ok(doc):
        reasons.append("ORIGIN_BINDING_MISMATCH")

    substantive = before_phi != after_phi
    if not reasons and not substantive:
        disposition = "ADMISSIBLE_NULL_EVENT"
    elif reasons:
        disposition = "INELIGIBLE"
    else:
        disposition = "ERIR_ELIGIBLE"

    transition_class = (
        classify_transition(before_phi, after_phi)
        if not reasons
        else "INELIGIBLE"
    )

    out = copy.deepcopy(doc)
    out["p_warrant_before"] = before_phi
    out["p_warrant_after"] = after_phi
    out["p_substantive_change"] = substantive
    out["p_disposition"] = disposition
    out["p_transition_class"] = transition_class
    out["p_eligibility_reasons"] = reasons
    out["p_erir_eligible"] = disposition == "ERIR_ELIGIBLE"
    out["p_admissible_null_event"] = disposition == "ADMISSIBLE_NULL_EVENT"
    out["p_expected_event"] = {
        "type": "EVIDENCE_RELEASE_REVISION",
        "event_class": "EVIDENCE_RELEASE",
        "event_id": f"OPEN_ORIGIN::{path}",
        "target_document": path,
        "object_id": doc.get("object_id"),
        "evidence_key": (doc.get("origin_claim") or {}).get("claim_key"),
    }
    return out
