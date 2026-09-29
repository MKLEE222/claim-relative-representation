from __future__ import annotations

import copy


def _expected_provenance(oracle_doc):
    origin = oracle_doc.get("origin_claim")
    if origin is None:
        return None
    return {
        "evidence_key": origin.get("claim_key"),
        "claim_key": origin.get("claim_key"),
        "source_file": origin.get("source_file"),
        "source_locator_contract": origin.get("source_locator_contract"),
        "object_id": origin.get("object_id"),
        "object_boundary_signature": origin.get("object_boundary_signature"),
        "applicability_class": origin.get("applicability_class"),
        "source_repository": origin.get("source_repository"),
        "source_version": origin.get("source_version"),
        "population_scope": origin.get("population_scope"),
    }


def _observed_provenance(trace):
    p = trace.get("evidence_provenance")
    if p is None:
        return None
    return {
        "evidence_key": p.get("evidence_key"),
        "claim_key": p.get("claim_key"),
        "source_file": p.get("source_file"),
        "source_locator_contract": p.get("source_locator_contract"),
        "object_id": p.get("object_id"),
        "object_boundary_signature": p.get("object_boundary_signature"),
        "applicability_class": p.get("applicability_class"),
        "source_repository": p.get("source_repository"),
        "source_version": p.get("source_version"),
        "population_scope": p.get("population_scope"),
    }


def evaluate(trace, oracle_doc, runtime_doc):
    origin = oracle_doc.get("origin_claim") or {}
    tr = trace.get("origin_transition") or {}
    req = trace.get("event_request") or {}
    audit = trace.get("delayed_audit") or {}
    octx = oracle_doc.get("source_context") or {}

    p1 = all([
        trace.get("root_phi") == oracle_doc.get("p_warrant_before"),
        runtime_doc.get("p_warrant_before") == oracle_doc.get("p_warrant_before"),
    ])

    p2 = all([
        bool(tr.get("applicable")),
        req.get("type") == "EVIDENCE_RELEASE_REVISION",
        req.get("event_class") == "EVIDENCE_RELEASE",
        req.get("object_id") == oracle_doc.get("object_id"),
        req.get("target_document") == oracle_doc.get("path"),
        req.get("source_repository") == octx.get("source_repository"),
        req.get("source_version") == octx.get("source_version"),
        req.get("population_scope") == octx.get("population_scope"),
    ])

    p3 = all([
        trace.get("post_event_warrant") == oracle_doc.get("warrant_after"),
        trace.get("post_event_phi") == oracle_doc.get("p_warrant_after"),
        runtime_doc.get("p_warrant_after") == oracle_doc.get("p_warrant_after"),
    ])

    p4 = all([
        bool(tr.get("applicable")),
        list(tr.get("collateral_temporal_paths") or []) == [],
        trace.get("final_warrant") == trace.get("post_event_warrant"),
    ])

    p5 = (
        _observed_provenance(trace)
        == _expected_provenance(oracle_doc)
    )

    p6 = all([
        tr.get("event_id") == f"OPEN_ORIGIN::{oracle_doc.get('path')}",
        tr.get("event_class") == "OPEN_ORIGIN",
        tr.get("target_document") == oracle_doc.get("path"),
        tr.get("evidence_key") == origin.get("claim_key"),
        tr.get("before_warrant") == oracle_doc.get("warrant_root"),
        tr.get("after_warrant") == oracle_doc.get("warrant_after"),
        tr.get("object_id") == oracle_doc.get("object_id"),
        tr.get("source_repository") == octx.get("source_repository"),
        tr.get("source_version") == octx.get("source_version"),
        tr.get("population_scope") == octx.get("population_scope"),
    ])

    p7 = all([
        audit.get("origin_event_id") == f"OPEN_ORIGIN::{oracle_doc.get('path')}",
        audit.get("origin_evidence_key") == origin.get("claim_key"),
        audit.get("origin_before_warrant") == oracle_doc.get("warrant_root"),
        audit.get("origin_after_warrant") == oracle_doc.get("warrant_after"),
        audit.get("object_id") == oracle_doc.get("object_id"),
        audit.get("source_repository") == octx.get("source_repository"),
        audit.get("source_version") == octx.get("source_version"),
    ])

    return {
        "oracle_erir_eligible": bool(oracle_doc.get("p_erir_eligible")),
        "runtime_erir_eligible": bool(runtime_doc.get("p_erir_eligible")),
        "oracle_transition_class": oracle_doc.get("p_transition_class"),
        "runtime_transition_class": runtime_doc.get("p_transition_class"),
        "eligibility_exact": all([
            runtime_doc.get("p_disposition") == oracle_doc.get("p_disposition"),
            runtime_doc.get("p_erir_eligible") == oracle_doc.get("p_erir_eligible"),
            runtime_doc.get("p_admissible_null_event")
                == oracle_doc.get("p_admissible_null_event"),
            runtime_doc.get("p_transition_class")
                == oracle_doc.get("p_transition_class"),
            runtime_doc.get("p_warrant_before")
                == oracle_doc.get("p_warrant_before"),
            runtime_doc.get("p_warrant_after")
                == oracle_doc.get("p_warrant_after"),
        ]),
        "P1_CURRENT_STATE_BEFORE": p1,
        "P2_EVENT_APPLICABILITY": p2,
        "P3_POST_EVENT_RESULT": p3,
        "P4_SELECTIVE_UPDATE": p4,
        "P5_PROVENANCE": p5,
        "P6_TRANSITION_ATTRIBUTION": p6,
        "P7_DELAYED_HISTORY": p7,
        "reference_end_to_end_pass": all([p1, p2, p3, p4, p5, p6, p7]),
    }


def capability_vector(evaluation):
    return {
        k: bool(evaluation.get(k))
        for k in (
            "P1_CURRENT_STATE_BEFORE",
            "P2_EVENT_APPLICABILITY",
            "P3_POST_EVENT_RESULT",
            "P4_SELECTIVE_UPDATE",
            "P5_PROVENANCE",
            "P6_TRANSITION_ATTRIBUTION",
            "P7_DELAYED_HISTORY",
        )
    }
