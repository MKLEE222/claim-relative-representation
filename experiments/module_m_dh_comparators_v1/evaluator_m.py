from __future__ import annotations

import copy


def _live_keys(warrant):
    if warrant.get("type") == "ALTERNATIVE_SET":
        return sorted(
            x.get("claim_key")
            for x in warrant.get("alternatives", [])
            if x.get("claim_key")
        )
    return sorted(k for k in warrant.get("basis", []) if k)


def _all_oracle_claims(doc):
    out = [copy.deepcopy(c) for c in doc.get("claims", [])]
    if doc.get("origin_claim") is not None:
        out.append(copy.deepcopy(doc["origin_claim"]))
    return out


def _expected_current_provenance(doc):
    live = set(_live_keys(doc.get("warrant_after") or {}))
    rows = {}
    for c in _all_oracle_claims(doc):
        key = c.get("claim_key")
        if key not in live:
            continue
        rows[key] = {
            "claim_key": key,
            "source_file": c.get("source_file"),
            "source_locator_contract": c.get("source_locator_contract"),
            "source_locator_xpath": c.get("source_locator_xpath"),
            "object_id": c.get("object_id"),
            "object_boundary_signature": c.get("object_boundary_signature"),
            "applicability_class": c.get("applicability_class"),
            "source_repository": c.get("source_repository"),
            "source_version": c.get("source_version"),
            "population_scope": c.get("population_scope"),
        }
    return rows


def _expected_delta(doc):
    origin = doc.get("origin_claim") or {}
    root = doc.get("warrant_root") or {}
    after = doc.get("warrant_after") or {}
    origin_key = origin.get("claim_key")
    return {
        "S0_to_S1": {
            "claim_changes": (
                [{"claim_key": origin_key, "change": "ADDED"}]
                if origin_key else []
            ),
            "warrant_changed": root != after,
            "before_warrant": copy.deepcopy(root),
            "after_warrant": copy.deepcopy(after),
            "before_live_claim_keys": _live_keys(root),
            "after_live_claim_keys": _live_keys(after),
        },
        "S1_to_S2": {
            "claim_changes": [],
            "warrant_changed": False,
            "before_warrant": copy.deepcopy(after),
            "after_warrant": copy.deepcopy(after),
            "before_live_claim_keys": _live_keys(after),
            "after_live_claim_keys": _live_keys(after),
        },
    }


def _expected_transition(doc):
    origin = doc.get("origin_claim") or {}
    return {
        "event_class": "OPEN_ORIGIN",
        "event_id": f"OPEN_ORIGIN::{doc.get('path')}",
        "target_document": doc.get("path"),
        "authorized_evidence_key": origin.get("claim_key"),
        "before_warrant": copy.deepcopy(doc.get("warrant_root")),
        "after_warrant": copy.deepcopy(doc.get("warrant_after")),
        "collateral_temporal_paths": [],
    }


def _expected_history(doc):
    origin = doc.get("origin_claim") or {}
    neutral = doc.get("neutral_event") or {}
    return {
        "origin_event_id": f"OPEN_ORIGIN::{doc.get('path')}",
        "origin_evidence_key": origin.get("claim_key"),
        "origin_before_warrant": copy.deepcopy(doc.get("warrant_root")),
        "origin_after_warrant": copy.deepcopy(doc.get("warrant_after")),
        "origin_collateral_temporal_paths": [],
        "neutral_event_key": neutral.get("event_key"),
    }


def evaluate_regime(output, oracle_doc):
    current = output.get("current_state") or {}
    current_state_exact = all([
        current.get("current_warrant") == oracle_doc.get("warrant_after"),
        sorted(current.get("live_claim_keys") or [])
            == _live_keys(oracle_doc.get("warrant_after") or {}),
    ])

    current_provenance_exact = (
        output.get("current_provenance") == _expected_current_provenance(oracle_doc)
    )

    expected_delta = _expected_delta(oracle_doc)
    state_delta_exact = output.get("state_delta") == expected_delta

    transition_attribution_exact = (
        output.get("transition_attribution") == _expected_transition(oracle_doc)
    )

    delayed_history_audit_exact = (
        output.get("delayed_history_audit") == _expected_history(oracle_doc)
    )

    return {
        "regime": output.get("regime"),
        "T1_CURRENT_STATE_EXACT": current_state_exact,
        "T2_CURRENT_PROVENANCE_EXACT": current_provenance_exact,
        "T3_STATE_DELTA_EXACT": state_delta_exact,
        "T4_TRANSITION_ATTRIBUTION_EXACT": transition_attribution_exact,
        "T5_DELAYED_HISTORY_AUDIT_EXACT": delayed_history_audit_exact,
        "positive_current_capability": bool(
            current_state_exact and current_provenance_exact
        ),
        "positive_snapshot_capability": bool(
            current_state_exact
            and current_provenance_exact
            and state_delta_exact
        ),
        "full_registered_history_capability": bool(
            current_state_exact
            and current_provenance_exact
            and state_delta_exact
            and transition_attribution_exact
            and delayed_history_audit_exact
        ),
    }
