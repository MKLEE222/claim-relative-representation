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


def _public_claim(c):
    if c is None:
        return None
    return {k: copy.deepcopy(v) for k, v in c.items() if k != "_bounds"}


def _claim_core(c):
    return {
        "claim_key": c.get("claim_key"),
        "role": c.get("role"),
        "interval": copy.deepcopy(c.get("interval")),
        "status": c.get("status"),
        "uncertain": c.get("uncertain"),
        "cert": c.get("cert"),
        "precision": c.get("precision"),
        "resp": c.get("resp"),
        "object_id": c.get("object_id"),
        "object_boundary_signature": c.get("object_boundary_signature"),
        "applicability_class": c.get("applicability_class"),
        "source_repository": c.get("source_repository"),
        "source_version": c.get("source_version"),
        "population_scope": c.get("population_scope"),
        "source_file": c.get("source_file"),
        "source_locator_contract": c.get("source_locator_contract"),
    }


def _live_keys(warrant):
    if warrant.get("type") == "ALTERNATIVE_SET":
        return sorted(
            x.get("claim_key")
            for x in warrant.get("alternatives", [])
            if x.get("claim_key")
        )
    return sorted(k for k in warrant.get("basis", []) if k)


def _state(claims):
    private = [copy.deepcopy(c) for c in claims if c is not None]
    warrant = runtime_l.base.runtime_warrant(private)
    live = _live_keys(warrant)
    public = [_claim_core(c) for c in private]
    public.sort(key=lambda x: str(x.get("claim_key")))
    return {
        "claims": public,
        "current_warrant": copy.deepcopy(warrant),
        "live_claim_keys": live,
    }


def _provenance_for_live(state):
    live = set(state["live_claim_keys"])
    return {
        c["claim_key"]: {
            "claim_key": c["claim_key"],
            "source_file": c.get("source_file"),
            "source_locator_contract": c.get("source_locator_contract"),
            "object_id": c.get("object_id"),
            "object_boundary_signature": c.get("object_boundary_signature"),
            "applicability_class": c.get("applicability_class"),
            "source_repository": c.get("source_repository"),
            "source_version": c.get("source_version"),
            "population_scope": c.get("population_scope"),
        }
        for c in state["claims"]
        if c.get("claim_key") in live
    }


def _claim_map(state):
    return {c["claim_key"]: c for c in state["claims"] if c.get("claim_key")}


def _delta(before, after):
    b = _claim_map(before)
    a = _claim_map(after)
    claim_changes = []
    for key in sorted(set(b) | set(a)):
        if key not in b:
            claim_changes.append({"claim_key": key, "change": "ADDED"})
        elif key not in a:
            claim_changes.append({"claim_key": key, "change": "REMOVED"})
        elif b[key] != a[key]:
            claim_changes.append({"claim_key": key, "change": "CHANGED"})
    return {
        "claim_changes": claim_changes,
        "warrant_changed": before["current_warrant"] != after["current_warrant"],
        "before_warrant": copy.deepcopy(before["current_warrant"]),
        "after_warrant": copy.deepcopy(after["current_warrant"]),
        "before_live_claim_keys": list(before["live_claim_keys"]),
        "after_live_claim_keys": list(after["live_claim_keys"]),
    }


def _canonical_snapshot(state):
    return json.dumps(
        state,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _root_claims(doc):
    return [copy.deepcopy(c) for c in doc.get("claims", [])]


def _terminal_claims(doc):
    claims = _root_claims(doc)
    if doc.get("origin_claim") is not None:
        claims.append(copy.deepcopy(doc["origin_claim"]))
    return claims


def current_reopen(doc):
    """Strong current/latest-source baseline.

    This function deliberately has no access to an RSTAR trace or any transition/evidence
    ledger. It reconstructs the terminal scholarly state from currently visible claims.
    """
    terminal = _state(_terminal_claims(doc))
    return {
        "regime": "B_CURRENT_REOPEN",
        "object_id": doc.get("object_id"),
        "source_context": copy.deepcopy(doc.get("source_context")),
        "current_state": terminal,
        "current_provenance": _provenance_for_live(terminal),
        "state_delta": None,
        "transition_attribution": None,
        "delayed_history_audit": None,
    }


def ordered_snapshots(doc):
    """Strong ordered-state-snapshot baseline without transition semantics."""
    s0 = _state(_root_claims(doc))
    s1 = _state(_terminal_claims(doc))
    s2 = copy.deepcopy(s1)

    d01 = _delta(s0, s1)
    d12 = _delta(s1, s2)

    newly_visible = [
        x["claim_key"]
        for x in d01["claim_changes"]
        if x["change"] == "ADDED"
    ]

    return {
        "regime": "B_ORDERED_SNAPSHOTS",
        "object_id": doc.get("object_id"),
        "source_context": copy.deepcopy(doc.get("source_context")),
        "snapshots": [
            {"snapshot_id": "S0", "state": s0, "canonical": _canonical_snapshot(s0)},
            {"snapshot_id": "S1", "state": s1, "canonical": _canonical_snapshot(s1)},
            {"snapshot_id": "S2", "state": s2, "canonical": _canonical_snapshot(s2)},
        ],
        "current_state": s2,
        "current_provenance": _provenance_for_live(s2),
        "state_delta": {
            "S0_to_S1": d01,
            "S1_to_S2": d12,
        },
        # The baseline may report what became visible. It may not promote that
        # observation into an authorized event/evidence claim.
        "newly_visible_claim_candidates": newly_visible,
        "transition_attribution": {
            "event_class": None,
            "event_id": None,
            "target_document": None,
            "authorized_evidence_key": None,
            "before_warrant": copy.deepcopy(s0["current_warrant"]),
            "after_warrant": copy.deepcopy(s1["current_warrant"]),
            "collateral_temporal_paths": None,
        },
        "delayed_history_audit": None,
    }


def rstar_view(doc, trace):
    """Project an RSTAR trace into the same task surface used by the comparators."""
    terminal = _state(_terminal_claims(doc))
    ot = trace.get("origin_transition") or {}
    audit = trace.get("delayed_audit") or {}
    return {
        "regime": "RSTAR",
        "object_id": doc.get("object_id"),
        "source_context": copy.deepcopy(doc.get("source_context")),
        "current_state": {
            "claims": terminal["claims"],
            "current_warrant": copy.deepcopy(trace.get("final_warrant")),
            "live_claim_keys": sorted(trace.get("final_live_claim_keys") or []),
        },
        "current_provenance": _provenance_for_live(terminal),
        "state_delta": {
            "S0_to_S1": {
                "claim_changes": (
                    [{"claim_key": ot.get("evidence_key"), "change": "ADDED"}]
                    if ot.get("evidence_key") else []
                ),
                "warrant_changed": ot.get("before_warrant") != ot.get("after_warrant"),
                "before_warrant": copy.deepcopy(ot.get("before_warrant")),
                "after_warrant": copy.deepcopy(ot.get("after_warrant")),
                "before_live_claim_keys": _live_keys(ot.get("before_warrant") or {}),
                "after_live_claim_keys": _live_keys(ot.get("after_warrant") or {}),
            },
            "S1_to_S2": {
                "claim_changes": [],
                "warrant_changed": False,
                "before_warrant": copy.deepcopy(trace.get("post_origin_warrant")),
                "after_warrant": copy.deepcopy(trace.get("final_warrant")),
                "before_live_claim_keys": sorted(trace.get("post_origin_live_claim_keys") or []),
                "after_live_claim_keys": sorted(trace.get("final_live_claim_keys") or []),
            },
        },
        "transition_attribution": {
            "event_class": ot.get("event_class"),
            "event_id": ot.get("event_id"),
            "target_document": ot.get("target_document"),
            "authorized_evidence_key": ot.get("evidence_key"),
            "before_warrant": copy.deepcopy(ot.get("before_warrant")),
            "after_warrant": copy.deepcopy(ot.get("after_warrant")),
            "collateral_temporal_paths": copy.deepcopy(ot.get("collateral_temporal_paths")),
        },
        "delayed_history_audit": {
            "origin_event_id": audit.get("origin_event_id"),
            "origin_evidence_key": audit.get("origin_evidence_key"),
            "origin_before_warrant": copy.deepcopy(audit.get("origin_before_warrant")),
            "origin_after_warrant": copy.deepcopy(audit.get("origin_after_warrant")),
            "origin_collateral_temporal_paths": copy.deepcopy(
                audit.get("origin_collateral_temporal_paths")
            ),
            "neutral_event_key": audit.get("neutral_event_key"),
        },
    }


def history_blind_projection(comparator_output):
    """Canonical information actually visible to a comparator.

    Used for the H_A/H_B indistinguishability test.
    """
    if comparator_output["regime"] == "B_CURRENT_REOPEN":
        payload = {
            "current_state": comparator_output["current_state"],
            "current_provenance": comparator_output["current_provenance"],
        }
    elif comparator_output["regime"] == "B_ORDERED_SNAPSHOTS":
        payload = {
            "snapshots": comparator_output["snapshots"],
            "current_provenance": comparator_output["current_provenance"],
            "state_delta": comparator_output["state_delta"],
            "newly_visible_claim_candidates": comparator_output[
                "newly_visible_claim_candidates"
            ],
        }
    else:
        raise ValueError("history_blind_projection is only defined for comparator regimes")
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
