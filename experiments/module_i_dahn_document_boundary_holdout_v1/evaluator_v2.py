from __future__ import annotations

import copy


def warrant_live_keys(w):
    if not isinstance(w, dict):
        return []
    if w.get("type") == "ALTERNATIVE_SET":
        return sorted(
            x.get("claim_key")
            for x in w.get("alternatives", [])
            if isinstance(x, dict) and x.get("claim_key")
        )
    return sorted(k for k in w.get("basis", []) if k)


def expected_question_exact(runtime_question, oracle_doc):
    expected = oracle_doc.get("expected_question")
    if expected is None:
        return runtime_question is None
    if runtime_question is None:
        return False
    return (
        runtime_question.get("type") == expected.get("type")
        and runtime_question.get("trigger") == expected.get("trigger")
        and sorted(runtime_question.get("disputed_claim_keys", []))
        == sorted(expected.get("disputed_claim_keys", []))
    )


def delayed_audit_exact(runtime_audit, oracle_doc):
    origin = oracle_doc.get("origin_claim")
    neutral = oracle_doc.get("neutral_event")
    if origin is None:
        return False
    expected_origin_event = f"OPEN_ORIGIN::{oracle_doc['path']}"
    expected_live = warrant_live_keys(oracle_doc["warrant_after"])

    return all([
        runtime_audit.get("document") == oracle_doc["path"],
        runtime_audit.get("current_warrant") == oracle_doc["warrant_after"],
        sorted(runtime_audit.get("live_claim_keys", [])) == expected_live,
        runtime_audit.get("origin_event_id") == expected_origin_event,
        runtime_audit.get("origin_evidence_key") == origin["claim_key"],
        runtime_audit.get("origin_before_warrant") == oracle_doc["warrant_root"],
        runtime_audit.get("origin_after_warrant") == oracle_doc["warrant_after"],
        runtime_audit.get("origin_collateral_temporal_paths") == [],
        runtime_audit.get("neutral_event_key")
        == (neutral.get("event_key") if neutral else None),
        isinstance(runtime_audit.get("origin_changed_paths"), list),
        bool(runtime_audit.get("origin_changed_paths")),
    ])


def evaluate_trace(trace, oracle_doc, runtime_doc):
    expected_live = warrant_live_keys(oracle_doc["warrant_after"])
    required_live = sorted(oracle_doc.get("required_live_claim_keys_after", []))

    q0_exact = trace.get("q0") == oracle_doc.get("q0")
    discovery_exact = expected_question_exact(trace.get("question"), oracle_doc)

    origin = oracle_doc.get("origin_claim")
    origin_key = origin.get("claim_key") if origin else None
    origin_transition = trace.get("origin_transition") or {}

    applicability_exact = all([
        bool(trace.get("open_origin_applicable")),
        origin_transition.get("target_document") == oracle_doc.get("path"),
        origin_transition.get("event_id") == f"OPEN_ORIGIN::{oracle_doc.get('path')}",
        origin_transition.get("evidence_key") == origin_key,
    ])

    warrant_exact = trace.get("post_origin_warrant") == oracle_doc.get("warrant_after")

    collateral_paths = list(trace.get("collateral_temporal_paths") or [])
    collateral_revision_count = len(collateral_paths)
    selective_update = all([
        applicability_exact,
        warrant_exact,
        oracle_doc.get("warrant_root") != oracle_doc.get("warrant_after"),
        collateral_revision_count == 0,
        origin_transition.get("before_warrant") == oracle_doc.get("warrant_root"),
        origin_transition.get("after_warrant") == oracle_doc.get("warrant_after"),
    ])

    runtime_live = sorted(trace.get("post_origin_live_claim_keys", []))
    required_live_preserved = all(k in runtime_live for k in required_live)
    live_state_exact = runtime_live == expected_live

    post_type = (oracle_doc.get("warrant_after") or {}).get("type")
    explicit_unresolved_status_preserved = (
        trace.get("post_origin_warrant", {}).get("type") == post_type
        if post_type in ("INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET", "UNRESOLVED")
        else True
    )

    alternative_persistence = all([
        required_live_preserved,
        live_state_exact,
        explicit_unresolved_status_preserved,
    ])

    neutral = oracle_doc.get("neutral_event")
    neutral_transition = trace.get("neutral_transition")
    neutral_event_agreement = (
        neutral is not None
        and neutral_transition is not None
        and neutral_transition.get("event_id") == (neutral.get("event_id") or f"NEUTRAL::{neutral['event_key']}")
        and neutral_transition.get("target_document") == oracle_doc.get("path")
    )
    null_event_stable = all([
        neutral_event_agreement,
        bool(trace.get("null_event_stable")),
        neutral_transition.get("changed_paths") == [],
        neutral_transition.get("collateral_temporal_paths") == [],
        trace.get("final_warrant") == oracle_doc.get("warrant_after"),
        sorted(trace.get("final_live_claim_keys", [])) == expected_live,
    ])

    provenance_exact = all([
        applicability_exact,
        origin_transition.get("evidence_key") == origin_key,
        runtime_doc.get("origin_claim") is not None,
        runtime_doc["origin_claim"].get("source_file") == oracle_doc.get("path"),
        runtime_doc["origin_claim"].get("source_locator_contract")
        == origin.get("source_locator_contract") if origin else False,
    ])

    history_exact = delayed_audit_exact(trace.get("delayed_audit") or {}, oracle_doc)

    boundary_exact = (
        runtime_doc.get("primary_boundary_signature")
        == oracle_doc.get("primary_boundary_signature")
    )
    neutral_parser_agreement = (
        (runtime_doc.get("neutral_event") or {}).get("event_key")
        == (oracle_doc.get("neutral_event") or {}).get("event_key")
    )

    end_to_end = all([
        boundary_exact,
        neutral_parser_agreement,
        q0_exact,
        discovery_exact,
        applicability_exact,
        warrant_exact,
        selective_update,
        alternative_persistence,
        null_event_stable,
        provenance_exact,
        history_exact,
    ])

    return {
        "q0_exact": q0_exact,
        "discovery_exact": discovery_exact,
        "question_emerged": trace.get("question") is not None,
        "applicability_exact": applicability_exact,
        "warrant_exact": warrant_exact,
        "selective_update": selective_update,
        "collateral_revision_count": collateral_revision_count,
        "collateral_temporal_paths": collateral_paths,
        "required_live_claim_keys_after": required_live,
        "runtime_live_claim_keys_after": runtime_live,
        "alternative_persistence": alternative_persistence,
        "neutral_event_agreement": neutral_event_agreement,
        "null_event_stable": null_event_stable,
        "provenance_exact": provenance_exact,
        "transition_history_exact": history_exact,
        "boundary_exact": boundary_exact,
        "neutral_parser_agreement": neutral_parser_agreement,
        "end_to_end_pass": end_to_end,
    }


def failed_metrics(evaluation):
    keys = [
        "q0_exact",
        "discovery_exact",
        "applicability_exact",
        "warrant_exact",
        "selective_update",
        "alternative_persistence",
        "neutral_event_agreement",
        "null_event_stable",
        "provenance_exact",
        "transition_history_exact",
        "boundary_exact",
        "neutral_parser_agreement",
        "end_to_end_pass",
    ]
    return [k for k in keys if not evaluation.get(k)]
