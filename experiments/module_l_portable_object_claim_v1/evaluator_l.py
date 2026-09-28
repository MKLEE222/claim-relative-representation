from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
J_DIR = HERE.parent / "module_j_dahn_object_bound_holdout_v1"
if str(J_DIR) not in sys.path:
    sys.path.insert(0, str(J_DIR))

import evaluator_j as base

ALLOWED = {
    "FILE_LEVEL_UNIQUE_OBJECT",
    "INSIDE_SELECTED_OBJECT_BOUNDARY",
}


def _proof_map(claims):
    return {
        c.get("claim_key"): {
            "object_id": c.get("object_id"),
            "object_boundary_signature": c.get("object_boundary_signature"),
            "applicability_class": c.get("applicability_class"),
            "source_repository": c.get("source_repository"),
            "source_version": c.get("source_version"),
            "population_scope": c.get("population_scope"),
            "source_file": c.get("source_file"),
            "source_locator_contract": c.get("source_locator_contract"),
        }
        for c in claims
        if c.get("claim_key")
    }


def evaluate_trace(trace, oracle_doc, runtime_doc):
    ev = base.evaluate_trace(trace, oracle_doc, runtime_doc)

    octx = oracle_doc.get("source_context") or {}
    rctx = runtime_doc.get("source_context") or {}
    tctx = trace.get("source_context") or {}
    source_context_exact = (
        octx == rctx == tctx
        and (trace.get("payload") or {}).get("source_commit") == octx.get("source_version")
        and (trace.get("payload") or {}).get("source_repository") == octx.get("source_repository")
        and (trace.get("payload") or {}).get("population_scope") == octx.get("population_scope")
    )

    oproof = _proof_map(oracle_doc.get("claims", []))
    rproof = _proof_map(runtime_doc.get("claims", []))
    active_claim_applicability_exact = (
        oproof == rproof
        and bool(oproof)
        and all(v.get("applicability_class") in ALLOWED for v in oproof.values())
    )

    oo = oracle_doc.get("origin_claim")
    ro = runtime_doc.get("origin_claim")
    origin_applicability_exact = (
        (oo is None and ro is None)
        or (
            oo is not None
            and ro is not None
            and oo.get("claim_key") == ro.get("claim_key")
            and oo.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT"
            and ro.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT"
            and oo.get("object_boundary_signature")
                == (oracle_doc.get("object_contract") or {}).get("boundary_signature")
            and ro.get("object_boundary_signature")
                == (runtime_doc.get("object_contract") or {}).get("boundary_signature")
            and oo.get("source_repository") == octx.get("source_repository")
            and ro.get("source_repository") == rctx.get("source_repository")
            and oo.get("source_version") == octx.get("source_version")
            and ro.get("source_version") == rctx.get("source_version")
            and oo.get("population_scope") == octx.get("population_scope")
            and ro.get("population_scope") == rctx.get("population_scope")
        )
    )

    object_source_context_exact = (
        (oracle_doc.get("object_contract") or {}).get("source_repository")
            == octx.get("source_repository")
        and (runtime_doc.get("object_contract") or {}).get("source_repository")
            == rctx.get("source_repository")
        and (oracle_doc.get("object_contract") or {}).get("source_version")
            == octx.get("source_version")
        and (runtime_doc.get("object_contract") or {}).get("source_version")
            == rctx.get("source_version")
        and (oracle_doc.get("object_contract") or {}).get("population_scope")
            == octx.get("population_scope")
        and (runtime_doc.get("object_contract") or {}).get("population_scope")
            == rctx.get("population_scope")
    )

    payload = trace.get("payload") or {}
    payload_claims = payload.get("claims") or []
    arm = trace.get("arm")
    if arm == "I_NO_BINDING":
        payload_binding_contract_exact = all(
            c.get("object_id") is None
            and c.get("object_boundary_signature") is None
            and c.get("applicability_class") is None
            for c in payload_claims
        ) and payload.get("object_id") is None
    else:
        payload_binding_contract_exact = all(
            c.get("claim_key") in rproof
            and {
                "object_id": c.get("object_id"),
                "object_boundary_signature": c.get("object_boundary_signature"),
                "applicability_class": c.get("applicability_class"),
                "source_repository": c.get("source_repository"),
                "source_version": c.get("source_version"),
                "population_scope": c.get("population_scope"),
                "source_file": c.get("source_file"),
                "source_locator_contract": c.get("source_locator_contract"),
            } == rproof.get(c.get("claim_key"))
            for c in payload_claims
        )

    ph = payload.get("origin_handle")
    if oo is None and ro is None:
        origin_handle_binding_exact = ph is None
    elif arm == "I_NO_BINDING":
        origin_handle_binding_exact = ph is None
    else:
        origin_handle_binding_exact = bool(ph) and all([
            ph.get("target_document") == oracle_doc.get("path"),
            ph.get("source_file") == oracle_doc.get("path"),
            ph.get("source_repository") == octx.get("source_repository"),
            ph.get("source_commit") == octx.get("source_version"),
            ph.get("source_version") == octx.get("source_version"),
            ph.get("population_scope") == octx.get("population_scope"),
            ph.get("object_id") == (oracle_doc.get("object_contract") or {}).get("object_id"),
            ph.get("object_boundary_signature")
                == (oracle_doc.get("object_contract") or {}).get("boundary_signature"),
            ph.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT",
            ph.get("claim_key") == (oo or {}).get("claim_key"),
        ])

    def excluded_core(doc):
        return sorted(
            (
                x.get("applicability_class"),
                tuple(sorted((x.get("raw_attrs") or {}).items())),
                x.get("source_text"),
            )
            for x in doc.get("excluded_temporal_claims", [])
        )

    excluded_temporal_claims_exact = excluded_core(oracle_doc) == excluded_core(runtime_doc)

    ev.update({
        "source_context_exact": source_context_exact,
        "active_claim_applicability_exact": active_claim_applicability_exact,
        "origin_applicability_exact": origin_applicability_exact,
        "object_source_context_exact": object_source_context_exact,
        "payload_binding_contract_exact": payload_binding_contract_exact,
        "origin_handle_binding_exact": origin_handle_binding_exact,
        "excluded_temporal_claims_exact": excluded_temporal_claims_exact,
    })
    ev["end_to_end_pass"] = bool(
        ev.get("end_to_end_pass")
        and source_context_exact
        and active_claim_applicability_exact
        and origin_applicability_exact
        and object_source_context_exact
        and payload_binding_contract_exact
        and origin_handle_binding_exact
        and excluded_temporal_claims_exact
    )
    return ev


def failed_metrics(evaluation):
    out = base.failed_metrics(evaluation)
    for k in (
        "source_context_exact",
        "active_claim_applicability_exact",
        "origin_applicability_exact",
        "object_source_context_exact",
        "payload_binding_contract_exact",
        "origin_handle_binding_exact",
        "excluded_temporal_claims_exact",
    ):
        if not evaluation.get(k):
            out.append(k)
    return out
