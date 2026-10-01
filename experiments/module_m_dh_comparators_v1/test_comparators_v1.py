from __future__ import annotations

import copy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
if str(L_DIR) not in sys.path:
    sys.path.insert(0, str(L_DIR))

import comparators_m
import evaluator_m
import oracle_l
import runtime_l
from test_portable_contract_v1 import CTX, DIRECT_EXPLICIT


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def main():
    path = "SYNTHETIC/module_m_direct.xml"
    oracle_doc = oracle_l.parse_document(path, DIRECT_EXPLICIT, CTX)
    runtime_doc = runtime_l.parse_document(path, DIRECT_EXPLICIT, CTX)

    require(oracle_doc["full_trajectory_eligible"], oracle_doc["full_trajectory_exclusion_reasons"])
    require(runtime_doc["object_id"] == oracle_doc["object_id"], {
        "oracle": oracle_doc["object_id"],
        "runtime": runtime_doc["object_id"],
    })

    current = comparators_m.current_reopen(runtime_doc)
    snapshots = comparators_m.ordered_snapshots(runtime_doc)
    rstar_trace = runtime_l.execute(runtime_doc, "I_RSTAR")
    rstar = comparators_m.rstar_view(runtime_doc, rstar_trace)

    ev_current = evaluator_m.evaluate_regime(current, oracle_doc)
    ev_snapshots = evaluator_m.evaluate_regime(snapshots, oracle_doc)
    ev_rstar = evaluator_m.evaluate_regime(rstar, oracle_doc)

    # Strong positive-baseline gates.
    require(ev_current["T1_CURRENT_STATE_EXACT"], ev_current)
    require(ev_current["T2_CURRENT_PROVENANCE_EXACT"], ev_current)
    require(ev_current["positive_current_capability"], ev_current)

    require(ev_snapshots["T1_CURRENT_STATE_EXACT"], ev_snapshots)
    require(ev_snapshots["T2_CURRENT_PROVENANCE_EXACT"], ev_snapshots)
    require(ev_snapshots["T3_STATE_DELTA_EXACT"], ev_snapshots)
    require(ev_snapshots["positive_snapshot_capability"], ev_snapshots)

    # The retained interface must satisfy the whole registered task on the positive control.
    require(ev_rstar["T1_CURRENT_STATE_EXACT"], ev_rstar)
    require(ev_rstar["T2_CURRENT_PROVENANCE_EXACT"], ev_rstar)
    require(ev_rstar["T3_STATE_DELTA_EXACT"], ev_rstar)
    require(ev_rstar["T4_TRANSITION_ATTRIBUTION_EXACT"], ev_rstar)
    require(ev_rstar["T5_DELAYED_HISTORY_AUDIT_EXACT"], ev_rstar)
    require(ev_rstar["full_registered_history_capability"], ev_rstar)

    # The comparator contract does not credit a state difference as an authorized event history.
    require(not ev_current["T4_TRANSITION_ATTRIBUTION_EXACT"], ev_current)
    require(not ev_current["T5_DELAYED_HISTORY_AUDIT_EXACT"], ev_current)
    require(not ev_snapshots["T4_TRANSITION_ATTRIBUTION_EXACT"], ev_snapshots)
    require(not ev_snapshots["T5_DELAYED_HISTORY_AUDIT_EXACT"], ev_snapshots)

    # Primary indistinguishability witness:
    # the same observable state sequence is compatible with two different scholarly histories.
    history_a = {
        "events": [
            {
                "event_class": "EVIDENCE_RELEASE",
                "event_id": f"OPEN_ORIGIN::{path}",
                "authorized_evidence_key": oracle_doc["origin_claim"]["claim_key"],
            },
            {
                "event_class": "NON_TEMPORAL_MAINTENANCE",
                "event_id": oracle_doc["neutral_event"]["event_id"],
            },
        ]
    }
    history_b = {
        "events": [
            {
                "event_class": "STATE_IMPORT",
                "event_id": f"IMPORT::{path}",
                "authorized_evidence_key": None,
            },
            {
                "event_class": "PRESENTATION_REBUILD",
                "event_id": "REBUILD::SYNTHETIC",
            },
        ]
    }
    require(history_a != history_b, {"history_a": history_a, "history_b": history_b})

    current_a = comparators_m.history_blind_projection(
        comparators_m.current_reopen(runtime_doc)
    )
    current_b = comparators_m.history_blind_projection(
        comparators_m.current_reopen(copy.deepcopy(runtime_doc))
    )
    snapshots_a = comparators_m.history_blind_projection(
        comparators_m.ordered_snapshots(runtime_doc)
    )
    snapshots_b = comparators_m.history_blind_projection(
        comparators_m.ordered_snapshots(copy.deepcopy(runtime_doc))
    )

    require(current_a == current_b, "CURRENT_REOPEN unexpectedly distinguishes history labels")
    require(snapshots_a == snapshots_b, "ORDERED_SNAPSHOTS unexpectedly distinguishes history labels")

    print({
        "study": "MODULE_M_SYNTHETIC_COMPARATOR_GATE_V1",
        "B_CURRENT_REOPEN": ev_current,
        "B_ORDERED_SNAPSHOTS": ev_snapshots,
        "RSTAR": ev_rstar,
        "indistinguishability": {
            "history_oracles_differ": history_a != history_b,
            "current_reopen_projection_identical": current_a == current_b,
            "ordered_snapshot_projection_identical": snapshots_a == snapshots_b,
        },
    })


if __name__ == "__main__":
    main()
