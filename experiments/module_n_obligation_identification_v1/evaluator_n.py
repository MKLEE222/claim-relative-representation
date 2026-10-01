from __future__ import annotations


REQUIRED_PROVENANCE = (
    "claim_key",
    "source_repository",
    "source_version",
    "population_scope",
    "source_file",
    "source_locator_contract",
    "object_id",
    "object_boundary_signature",
    "applicability_class",
)


def _live_keys(warrant):
    if (warrant or {}).get("type") == "ALTERNATIVE_SET":
        return sorted(
            x.get("claim_key")
            for x in (warrant or {}).get("alternatives", [])
            if x.get("claim_key")
        )
    return sorted(k for k in (warrant or {}).get("basis", []) if k)


def _question_core(q):
    if q is None:
        return None
    return {
        "type": q.get("type"),
        "trigger": q.get("trigger"),
        "disputed_claim_keys": sorted(q.get("disputed_claim_keys") or []),
    }


def _provenance_complete(trace):
    live = set(trace.get("final_live_claim_keys") or [])
    claims = {
        c.get("claim_key"): c
        for c in trace.get("surface_claims", [])
        if c.get("claim_key")
    }
    if not live:
        return False
    for key in live:
        c = claims.get(key)
        if c is None:
            return False
        if any(c.get(field) in (None, "") for field in REQUIRED_PROVENANCE):
            return False
    return True


def evaluate(trace, oracle_doc):
    origin = oracle_doc.get("origin_claim") or {}
    ot = trace.get("origin_transition") or {}
    audit = trace.get("delayed_audit") or {}
    neutral = oracle_doc.get("neutral_event") or {}

    c1 = trace.get("root_warrant") == oracle_doc.get("warrant_root")

    c2 = (
        _question_core(trace.get("question"))
        == _question_core(oracle_doc.get("expected_question"))
    )

    c3 = bool(trace.get("open_origin_applicable"))

    c4 = all([
        trace.get("post_origin_warrant") == oracle_doc.get("warrant_after"),
        sorted(trace.get("post_origin_live_claim_keys") or [])
            == _live_keys(oracle_doc.get("warrant_after")),
    ])

    c5 = all([
        bool(ot.get("applicable")),
        ot.get("before_warrant") == oracle_doc.get("warrant_root"),
        ot.get("after_warrant") == oracle_doc.get("warrant_after"),
        list(ot.get("collateral_temporal_paths") or []) == [],
    ])

    c6 = _provenance_complete(trace)

    c7 = all([
        bool(ot.get("applicable")),
        ot.get("event_id") == f"OPEN_ORIGIN::{oracle_doc.get('path')}",
        ot.get("target_document") == oracle_doc.get("path"),
        ot.get("evidence_key") == origin.get("claim_key"),
        ot.get("object_id") == oracle_doc.get("object_id"),
    ])

    # C8 asks whether the transition history is retained and reconstructable.
    # It intentionally does not require collateral_temporal_paths == []:
    # a retained history may faithfully reveal a non-selective/bad transition.
    c8 = all([
        audit.get("origin_event_id") == f"OPEN_ORIGIN::{oracle_doc.get('path')}",
        audit.get("origin_evidence_key") == origin.get("claim_key"),
        audit.get("origin_before_warrant") == oracle_doc.get("warrant_root"),
        audit.get("origin_after_warrant") == oracle_doc.get("warrant_after"),
        audit.get("neutral_event_key") == neutral.get("event_key"),
        isinstance(audit.get("origin_collateral_temporal_paths"), list),
    ])

    return {
        "C1_CURRENT_STATE": c1,
        "C2_DISCOVERY": c2,
        "C3_EVENT_APPLICABILITY": c3,
        "C4_RESULT_DETERMINACY": c4,
        "C5_SELECTIVITY": c5,
        "C6_CURRENT_PROVENANCE": c6,
        "C7_TRANSITION_ATTRIBUTION": c7,
        "C8_DELAYED_HISTORY": c8,
        "rejection_reason": (
            (ot.get("collateral_temporal_paths") or [None])[0]
            if not ot.get("applicable")
            else None
        ),
        "result_status_intervention_applicable": trace.get(
            "result_status_intervention_applicable"
        ),
    }
