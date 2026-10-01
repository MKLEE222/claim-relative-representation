from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P_DIR = HERE.parent / "module_p_evidence_release_revision_v1"
if str(P_DIR) not in sys.path:
    sys.path.insert(0, str(P_DIR))

import oracle_p
import runtime_p
import test_revision_contract_v1 as ptest


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def parsed(name, raw):
    path = "SYNTHETIC/CROSS/" + name + ".xml"
    o = oracle_p.parse_document(path, raw, ptest.CTX)
    r = runtime_p.parse_document(path, raw, ptest.CTX)
    return o, r


def audit_case(label, raw):
    o, r = parsed(label, raw)
    trace = runtime_p.execute(r)

    event = trace["event_request"]
    event_has_operation = "operation" in event
    phenotype_exact = (
        o["p_transition_class"]
        == oracle_p.classify_transition(
            o["p_warrant_before"],
            o["p_warrant_after"],
        )
    )

    return {
        "label": label,
        "event_type": event.get("type"),
        "event_class": event.get("event_class"),
        "event_has_operation_field": event_has_operation,
        "binding_preconditions_present": all([
            (o.get("object_contract") or {}).get("status")
                == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
            o.get("origin_contract_status") == "SINGLE_ORIGIN_ADMISSIBLE",
        ]),
        "phi_before": o["p_warrant_before"],
        "phi_after": o["p_warrant_after"],
        "phi_changed": o["p_warrant_before"] != o["p_warrant_after"],
        "disposition": o["p_disposition"],
        "transition_class": o["p_transition_class"],
        "transition_class_is_state_pair_phenotype": phenotype_exact,
        "event_applied": bool(
            trace["origin_transition"].get("applicable")
        ),
        "evidence_ledger_nonempty": bool(trace.get("evidence_ledger")),
        "event_ledger_nonempty": bool(trace.get("event_ledger")),
        "transition_ledger_nonempty": bool(
            trace.get("transition_ledger")
        ),
    }


def main():
    rows = [
        audit_case("CONFLICT", ptest.CONFLICT),
        audit_case("UNRESOLVED_TO_EXACT", ptest.UNRESOLVED_TO_EXACT),
        audit_case("BASIS_ONLY_NULL", ptest.BASIS_ONLY),
    ]

    require(all(
        not row["event_has_operation_field"] for row in rows
    ), rows)
    require(all(
        row["transition_class_is_state_pair_phenotype"]
        for row in rows
    ), rows)

    null = next(
        x for x in rows if x["label"] == "BASIS_ONLY_NULL"
    )
    require(null["disposition"] == "ADMISSIBLE_NULL_EVENT", null)
    require(not null["phi_changed"], null)
    require(null["event_applied"], null)
    require(all([
        null["evidence_ledger_nonempty"],
        null["event_ledger_nonempty"],
        null["transition_ledger_nonempty"],
    ]), null)

    sig = str(inspect.signature(runtime_p.execute))
    wrapper_accepts_prior_state = "state" in sig
    wrapper_accepts_event_sequence = "events" in sig

    result = {
        "study": "MODULE_P_GENERATOR_CROSS_AUDIT_V1",
        "rows": rows,
        "findings": {
            "FIXED_GENERATOR_NOT_EXPLICIT_OPERATION_LABEL": True,
            "TRANSITION_CLASS_IS_POST_STATE_PHENOTYPE": True,
            "EVIDENCE_RELEASE_ACTIVATION_EXTERNALLY_DECLARED": True,
            "SUBSTANTIVE_ELIGIBILITY_REQUIRES_POST_STATE_COMPARISON": True,
            "PSI_NULL_ACTION_RECORD_NON_NULL": True,
            "MULTI_EVENT_COMPOSITION_WRAPPER_PRESENT": bool(
                wrapper_accepts_prior_state
                or wrapper_accepts_event_sequence
            ),
        },
        "runtime_execute_signature": sig,
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "module_p_generator_cross_audit_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
