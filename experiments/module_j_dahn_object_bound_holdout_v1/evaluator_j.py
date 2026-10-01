from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
I_DIR = HERE.parent / "module_i_dahn_document_boundary_holdout_v1"
if str(I_DIR) not in sys.path:
    sys.path.insert(0, str(I_DIR))

import evaluator_v2 as base


def evaluate_trace(trace, oracle_doc, runtime_doc):
    ev = base.evaluate_trace(trace, oracle_doc, runtime_doc)

    o_obj = oracle_doc.get("object_contract") or {}
    r_obj = runtime_doc.get("object_contract") or {}

    object_status_exact = (
        o_obj.get("status") == r_obj.get("status")
    )
    object_id_exact = (
        o_obj.get("object_id") == r_obj.get("object_id")
        and trace.get("object_id") == o_obj.get("object_id")
    )

    oracle_claims = oracle_doc.get("claims", [])
    runtime_claims = runtime_doc.get("claims", [])
    object_claim_binding_exact = (
        o_obj.get("status") == "SINGLE_PRIMARY_DOCUMENT_OBJECT"
        and all(c.get("object_id") == o_obj.get("object_id") for c in oracle_claims)
        and all(c.get("object_id") == o_obj.get("object_id") for c in runtime_claims)
    )

    o_origin = oracle_doc.get("origin_claim")
    r_origin = runtime_doc.get("origin_claim")
    origin_object_binding_exact = (
        (o_origin is None and r_origin is None)
        or (
            o_origin is not None
            and r_origin is not None
            and o_origin.get("object_id") == o_obj.get("object_id")
            and r_origin.get("object_id") == o_obj.get("object_id")
        )
    )

    expected_q = oracle_doc.get("expected_question")
    runtime_q = trace.get("question")
    question_object_binding_exact = (
        (expected_q is None and runtime_q is None)
        or (
            expected_q is not None
            and runtime_q is not None
            and expected_q.get("object_id") == o_obj.get("object_id")
            and runtime_q.get("object_id") == o_obj.get("object_id")
        )
    )

    transition_object_binding_exact = (
        (trace.get("origin_transition") or {}).get("object_id")
        == o_obj.get("object_id")
    )
    delayed_object_binding_exact = (
        (trace.get("delayed_audit") or {}).get("object_id")
        == o_obj.get("object_id")
    )

    object_contract_exact = all([
        object_status_exact,
        object_id_exact,
        object_claim_binding_exact,
        origin_object_binding_exact,
        question_object_binding_exact,
        transition_object_binding_exact,
        delayed_object_binding_exact,
    ])

    ev.update({
        "object_status_exact": object_status_exact,
        "object_id_exact": object_id_exact,
        "object_claim_binding_exact": object_claim_binding_exact,
        "origin_object_binding_exact": origin_object_binding_exact,
        "question_object_binding_exact": question_object_binding_exact,
        "transition_object_binding_exact": transition_object_binding_exact,
        "delayed_object_binding_exact": delayed_object_binding_exact,
        "object_contract_exact": object_contract_exact,
    })
    ev["end_to_end_pass"] = bool(ev.get("end_to_end_pass") and object_contract_exact)
    return ev


def failed_metrics(evaluation):
    out = base.failed_metrics(evaluation)
    for k in (
        "object_status_exact",
        "object_id_exact",
        "object_claim_binding_exact",
        "origin_object_binding_exact",
        "question_object_binding_exact",
        "transition_object_binding_exact",
        "delayed_object_binding_exact",
        "object_contract_exact",
    ):
        if not evaluation.get(k):
            out.append(k)
    return out
