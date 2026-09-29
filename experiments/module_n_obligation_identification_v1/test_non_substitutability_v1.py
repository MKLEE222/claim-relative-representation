from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
if str(L_DIR) not in sys.path:
    sys.path.insert(0, str(L_DIR))

import evaluator_n
import interventions_n
import oracle_l
import runtime_l
from test_portable_contract_v1 import CTX, DIRECT_EXPLICIT


CAPS = tuple(f"C{i}_" for i in range(1, 9))


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def main():
    path = "SYNTHETIC/module_n_direct.xml"
    oracle_doc = oracle_l.parse_document(path, DIRECT_EXPLICIT, CTX)
    runtime_doc = runtime_l.parse_document(path, DIRECT_EXPLICIT, CTX)
    require(oracle_doc["full_trajectory_eligible"], oracle_doc["full_trajectory_exclusion_reasons"])

    results = {}
    for arm in interventions_n.ARMS:
        trace = interventions_n.run_arm(runtime_doc, arm)
        results[arm] = evaluator_n.evaluate(trace, oracle_doc)

    full = results["N_FULL"]
    for k, v in full.items():
        if k.startswith("C"):
            require(v is True, {"arm": "N_FULL", "metric": k, "evaluation": full})

    no_obj = results["N_NO_OBJECT_ID"]
    no_app = results["N_NO_APPLICABILITY"]
    no_prov = results["N_NO_CURRENT_PROVENANCE"]
    no_transition = results["N_NO_TRANSITION_BINDING"]
    collateral = results["N_COLLATERAL_UPDATE"]
    no_history = results["N_NO_HISTORY"]
    collapse = results["N_COLLAPSE_RESULT_STATUS"]

    # A. O1 vs O2: value-level dispute discovery remains, but authorization fails
    # for distinct registered reasons.
    require(no_obj["C1_CURRENT_STATE"], no_obj)
    require(no_obj["C2_DISCOVERY"], no_obj)
    require(not no_obj["C3_EVENT_APPLICABILITY"], no_obj)
    require(not no_obj["C7_TRANSITION_ATTRIBUTION"], no_obj)
    require(no_obj["rejection_reason"] == "NO_BOUND_OBJECT", no_obj)

    require(no_app["C1_CURRENT_STATE"], no_app)
    require(no_app["C2_DISCOVERY"], no_app)
    require(not no_app["C3_EVENT_APPLICABILITY"], no_app)
    require(not no_app["C7_TRANSITION_ATTRIBUTION"], no_app)
    require(
        no_app["rejection_reason"] == "INVALID_OBJECT_OR_APPLICABILITY_BINDING",
        no_app,
    )

    # B. O6 vs O7 cross-over.
    require(no_prov["C1_CURRENT_STATE"], no_prov)
    require(no_prov["C3_EVENT_APPLICABILITY"], no_prov)
    require(not no_prov["C6_CURRENT_PROVENANCE"], no_prov)
    require(no_prov["C7_TRANSITION_ATTRIBUTION"], no_prov)
    require(no_prov["C8_DELAYED_HISTORY"], no_prov)

    require(no_transition["C1_CURRENT_STATE"], no_transition)
    require(no_transition["C2_DISCOVERY"], no_transition)
    require(no_transition["C6_CURRENT_PROVENANCE"], no_transition)
    require(not no_transition["C3_EVENT_APPLICABILITY"], no_transition)
    require(not no_transition["C7_TRANSITION_ATTRIBUTION"], no_transition)
    require(
        no_transition["rejection_reason"] == "ORIGIN_HANDLE_BINDING_MISMATCH",
        no_transition,
    )

    # C. O5 vs O8 cross-over.
    require(collateral["C3_EVENT_APPLICABILITY"], collateral)
    require(collateral["C7_TRANSITION_ATTRIBUTION"], collateral)
    require(not collateral["C5_SELECTIVITY"], collateral)
    require(collateral["C8_DELAYED_HISTORY"], collateral)

    require(no_history["C4_RESULT_DETERMINACY"], no_history)
    require(no_history["C5_SELECTIVITY"], no_history)
    require(not no_history["C8_DELAYED_HISTORY"], no_history)

    # D. O4 vs O8 cross-over.
    require(collapse["result_status_intervention_applicable"] is True, collapse)
    require(not collapse["C4_RESULT_DETERMINACY"], collapse)
    require(collapse["C5_SELECTIVITY"], collapse)
    require(collapse["C8_DELAYED_HISTORY"], collapse)

    require(no_history["C4_RESULT_DETERMINACY"], no_history)
    require(not no_history["C8_DELAYED_HISTORY"], no_history)

    print({
        "study": "MODULE_N_SYNTHETIC_NON_SUBSTITUTABILITY_V1",
        "results": results,
        "crossovers": {
            "O1_vs_O2": True,
            "O6_vs_O7": True,
            "O5_vs_O8": True,
            "O4_vs_O8": True,
        },
    })


if __name__ == "__main__":
    main()
