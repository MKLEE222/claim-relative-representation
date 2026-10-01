from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FP_DIR = ROOT / "experiments" / "formalization_papers_qualified_composition_v1"
YC_DIR = ROOT / "experiments" / "natural_act_composition_v2"

for p in (FP_DIR, YC_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import run_fp_generator_signature_audit_v1 as fpsig
import target_bound_oracle_v2 as y_oracle
import target_bound_runtime_v2 as y_runtime
import run_natural_act_composition_v2 as ynat


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def ynorm(result):
    out = copy.deepcopy(result)
    out.pop("engine", None)
    return out


def yexact(state, event):
    o = y_oracle.apply(state, event)
    r = y_runtime.execute(state, event)
    require(ynorm(o) == ynorm(r), {
        "state": state,
        "event": event,
        "oracle": ynorm(o),
        "runtime": ynorm(r),
    })
    return o


def paper_money_fixture():
    obj = "YC-PAPER-MONEY"
    version = "PM01_PM02_PM03_PAGE_VERIFIED_SEQUENCE_V2"
    target = "paper-money-material-identification"
    s0 = ynat.state(
        obj,
        version,
        target,
        ynat.claim(
            "PM01",
            obj,
            target,
            "MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE",
            "NARRATIVE_ASSERTED",
            "PM01",
            "1903 vol. 1 printed p. 423",
            "Marco Polo/Rustichello/Yule translation",
        ),
    )
    e_add = ynat.event(
        "PM02_EVENT",
        obj,
        version,
        target,
        "PM02",
        "1903 vol.1 p430 / scan732",
        "CONTRADICTS_PRIOR",
        "PM01",
        "Emil Bretschneider as transmitted by Henri Cordier",
        mediator="Henri Cordier",
        new_claim_id="PM02",
        value="MULBERRY_BARK_IDENTIFICATION_MISTAKEN",
        status="ASSERTED",
    )
    e_resolve = ynat.event(
        "PM03_EVENT",
        obj,
        version,
        target,
        "PM03",
        "1920 pp70-72 / scan84-86",
        "CORRECTION_OF_PRIOR_CRITICISM",
        "PM02",
        "Berthold Laufer as transmitted by Henri Cordier",
        mediator="Henri Cordier",
        new_claim_id="PM03",
        value="MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE",
        status="RESTORED_AS_CORRECT",
    )
    return s0, e_add, e_resolve


def arbre_fixture():
    obj = "YC-ARBRE-SEC"
    version = "ARBR_1903_1920_PAGE_VERIFIED_V2"
    target = "arbre-sec-identification"
    s0 = ynat.state(
        obj,
        version,
        target,
        ynat.claim(
            "ARBR-ID-1903",
            obj,
            target,
            "ORIENTAL_PLANE_CHINAR",
            "ASSERTED",
            "ARBR-ID-1903",
            "1903 I:113,128",
            "EARLIER_EDITORIAL_NOTE",
        ),
    )
    e_add = ynat.event(
        "ARBR-ID-HS-EVENT",
        obj,
        version,
        target,
        "ARBR-ID-HS",
        "1920 p.31",
        "COMPETING_IDENTIFICATION",
        "ARBR-ID-1903",
        "HOUTUM_SCHINDLER",
        mediator="CORDIER",
        new_claim_id="ARBR-ID-HS",
        value="CYPRESS_OF_ZOROASTER",
        status="ASSERTED_PROPOSAL",
    )
    e_record = ynat.event(
        "ARBR-REPLY-CORDIER-EVENT",
        obj,
        version,
        target,
        "ARBR-REPLY-CORDIER",
        "1920 p.31",
        "BIBLIOGRAPHIC_REPLY",
        "ARBR-ID-HS",
        "CORDIER",
        mediator=None,
        new_claim_id=None,
        value=None,
        status=None,
    )
    return s0, e_add, e_record


def audit_yule_add(label, s0, event):
    require(not s0["transition_ledger"], s0)
    valid = yexact(s0, event)
    require(
        valid["qualified"] and valid["generator"] == "ADD_ALTERNATIVE",
        valid,
    )

    missing = copy.deepcopy(event)
    missing["relation_target_claim_id"] = "FOREIGN-NONLIVE-CLAIM"
    rejected = yexact(s0, missing)
    require(
        not rejected["qualified"]
        and rejected["rejection_reason"] == "RELATION_TARGET_NOT_LIVE",
        rejected,
    )

    return {
        "label": label,
        "generator": "ADD_ALTERNATIVE",
        "valid_with_empty_prior_history": True,
        "wrong_or_nonlive_target_rejected": True,
        "wrong_or_nonlive_target_reason": rejected["rejection_reason"],
        "signature": {
            "TARGET_IDENTITY": "REQUIRED",
            "TARGET_LIVE_OR_CURRENT": "REQUIRED",
            "RETAINED_TRANSITION_HISTORY": (
                "NOT_REQUIRED_IN_REGISTERED_TASK"
            ),
        },
        "pass": True,
    }


def audit_yule_resolve():
    s0, e_add, e_resolve = paper_money_fixture()
    add = yexact(s0, e_add)
    require(add["qualified"] and add["generator"] == "ADD_ALTERNATIVE", add)
    s1 = add["state"]

    valid = yexact(s1, e_resolve)
    require(valid["qualified"] and valid["generator"] == "RESOLVE", valid)

    nohist = copy.deepcopy(s1)
    nohist["evidence_ledger"] = []
    nohist["event_ledger"] = []
    nohist["transition_ledger"] = []
    require(y_oracle.psi(s1) == y_oracle.psi(nohist), {
        "full": y_oracle.psi(s1),
        "nohist": y_oracle.psi(nohist),
    })
    hist_fail = yexact(nohist, e_resolve)
    require(
        not hist_fail["qualified"]
        and hist_fail["rejection_reason"]
            == "RELATION_TARGET_HISTORY_UNRESOLVED",
        hist_fail,
    )

    wrong_target = copy.deepcopy(e_resolve)
    wrong_target["relation_target_claim_id"] = "PM01"
    target_fail = yexact(s1, wrong_target)
    require(not target_fail["qualified"], target_fail)

    return {
        "label": "PAPER_MONEY_PM03",
        "generator": "RESOLVE",
        "valid": True,
        "same_current_assertions_after_history_ablation": True,
        "history_ablation_rejected": True,
        "history_reason": hist_fail["rejection_reason"],
        "wrong_target_rejected": True,
        "wrong_target_reason": target_fail["rejection_reason"],
        "signature": {
            "TARGET_IDENTITY": "REQUIRED",
            "TARGET_LIVE_OR_CURRENT": "REQUIRED",
            "RETAINED_TRANSITION_HISTORY": "REQUIRED",
        },
        "pass": True,
    }


def audit_yule_record_evidence():
    s0, e_add, e_record = arbre_fixture()
    add = yexact(s0, e_add)
    require(add["qualified"] and add["generator"] == "ADD_ALTERNATIVE", add)
    s1 = add["state"]

    valid = yexact(s1, e_record)
    require(
        valid["qualified"]
        and valid["generator"] == "RECORD_EVIDENCE",
        valid,
    )

    nohist = copy.deepcopy(s1)
    nohist["evidence_ledger"] = []
    nohist["event_ledger"] = []
    nohist["transition_ledger"] = []
    require(y_oracle.psi(s1) == y_oracle.psi(nohist), {
        "full": y_oracle.psi(s1),
        "nohist": y_oracle.psi(nohist),
    })
    nohist_result = yexact(nohist, e_record)
    require(
        nohist_result["qualified"]
        and nohist_result["generator"] == "RECORD_EVIDENCE",
        nohist_result,
    )

    before_target = yexact(s0, e_record)
    require(
        not before_target["qualified"]
        and before_target["rejection_reason"] == "RELATION_TARGET_NOT_LIVE",
        before_target,
    )

    return {
        "label": "ARBRE_SEC_BIBLIOGRAPHIC_REPLY",
        "generator": "RECORD_EVIDENCE",
        "valid": True,
        "same_current_assertions_after_history_ablation": True,
        "history_ablated_still_qualified": True,
        "target_before_live_rejected": True,
        "target_before_live_reason": before_target["rejection_reason"],
        "signature": {
            "TARGET_IDENTITY": "REQUIRED",
            "TARGET_LIVE_OR_CURRENT": "REQUIRED",
            "RETAINED_TRANSITION_HISTORY": (
                "NOT_REQUIRED_IN_REGISTERED_TASK"
            ),
        },
        "pass": True,
    }


def formalization_signature(main_result):
    den = fpsig.denominators(main_result)
    review_rows = [fpsig.audit_review(x, den) for x in den["reviews"]]
    update_rows = [fpsig.audit_update(x, den) for x in den["updates"]]
    response_rows = [
        fpsig.audit_response(x, den) for x in den["responses"]
    ]
    decision_rows = [
        fpsig.audit_decision(x, den) for x in den["decisions"]
    ]
    all_rows = review_rows + update_rows + response_rows + decision_rows
    require(all(x["pass"] for x in all_rows), all_rows)
    return {
        "denominators": {
            "RECORD_REVIEW": len(review_rows),
            "REPLACE_FORMALIZATION": len(update_rows),
            "RECORD_RESPONSE": len(response_rows),
            "REVISE_PUBLICATION_STATUS": len(decision_rows),
        },
        "pass_counts": {
            "RECORD_REVIEW": sum(x["pass"] for x in review_rows),
            "REPLACE_FORMALIZATION": sum(x["pass"] for x in update_rows),
            "RECORD_RESPONSE": sum(x["pass"] for x in response_rows),
            "REVISE_PUBLICATION_STATUS": sum(
                x["pass"] for x in decision_rows
            ),
        },
        "signatures": {
            "RECORD_REVIEW": {
                "TARGET_IDENTITY": "REQUIRED",
                "TARGET_LIVE_OR_CURRENT": "REQUIRED",
                "RETAINED_TRANSITION_HISTORY": (
                    "ROOT_ACTION_NO_PRIOR_HISTORY"
                ),
            },
            "REPLACE_FORMALIZATION": {
                "TARGET_IDENTITY": "REQUIRED",
                "VERSION_OR_VALIDITY_STATE": "REQUIRED",
                "RETAINED_TRANSITION_HISTORY": (
                    "NOT_REQUIRED_IN_REGISTERED_TASK"
                ),
            },
            "RECORD_RESPONSE": {
                "TARGET_IDENTITY": "REQUIRED",
                "TARGET_LIVE_OR_CURRENT": "REQUIRED",
                "RETAINED_TRANSITION_HISTORY": "REQUIRED",
            },
            "REVISE_PUBLICATION_STATUS": {
                "TARGET_IDENTITY": "REQUIRED",
                "TARGET_LIVE_OR_CURRENT": "REQUIRED",
                "RETAINED_TRANSITION_HISTORY": (
                    "NOT_REQUIRED_IN_REGISTERED_TASK"
                ),
            },
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formalization-main", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    ynat.source_audit()
    branch_scan = ynat.no_case_specific_branches()

    fp_main = json.loads(
        Path(args.formalization_main).read_text(encoding="utf-8")
    )
    formalization = formalization_signature(fp_main)

    pm_s0, pm_add, _ = paper_money_fixture()
    ar_s0, ar_add, _ = arbre_fixture()

    y_add_rows = [
        audit_yule_add("PAPER_MONEY_PM02", pm_s0, pm_add),
        audit_yule_add("ARBRE_SEC_HS", ar_s0, ar_add),
    ]
    y_resolve = audit_yule_resolve()
    y_record = audit_yule_record_evidence()

    require(all(x["pass"] for x in y_add_rows), y_add_rows)
    require(y_resolve["pass"], y_resolve)
    require(y_record["pass"], y_record)

    history_required_formalization = {
        g for g, sig in formalization["signatures"].items()
        if sig.get("RETAINED_TRANSITION_HISTORY") == "REQUIRED"
    }
    history_not_required_formalization = {
        g for g, sig in formalization["signatures"].items()
        if sig.get("RETAINED_TRANSITION_HISTORY")
        == "NOT_REQUIRED_IN_REGISTERED_TASK"
    }
    yule_signatures = {
        "ADD_ALTERNATIVE": y_add_rows[0]["signature"],
        "RESOLVE": y_resolve["signature"],
        "RECORD_EVIDENCE": y_record["signature"],
    }
    history_required_yule = {
        g for g, sig in yule_signatures.items()
        if sig.get("RETAINED_TRANSITION_HISTORY") == "REQUIRED"
    }
    history_not_required_yule = {
        g for g, sig in yule_signatures.items()
        if sig.get("RETAINED_TRANSITION_HISTORY")
        == "NOT_REQUIRED_IN_REGISTERED_TASK"
    }

    required_structure = {
        "formalization_has_history_required": bool(
            history_required_formalization
        ),
        "formalization_has_history_not_required": bool(
            history_not_required_formalization
        ),
        "yule_has_history_required": bool(history_required_yule),
        "yule_has_history_not_required": bool(history_not_required_yule),
        "oracle_runtime_exact_yule": True,
        "no_case_specific_yule_branches": all(
            not hits for hits in branch_scan.values()
        ),
    }

    result = {
        "study": "CROSS_ECOLOGY_GENERATOR_QUALIFICATION_SIGNATURE_AUDIT_V1",
        "data_status": "POST_FRESH_AND_PREEXISTING_EXPOSED_CONDITIONAL_MINIMALITY",
        "formalization_papers": formalization,
        "yule_cordier": {
            "ADD_ALTERNATIVE": {
                "denominator": len(y_add_rows),
                "pass_count": sum(x["pass"] for x in y_add_rows),
                "signature": y_add_rows[0]["signature"],
                "rows": y_add_rows,
            },
            "RESOLVE": {
                "denominator": 1,
                "pass_count": 1 if y_resolve["pass"] else 0,
                "signature": y_resolve["signature"],
                "rows": [y_resolve],
            },
            "RECORD_EVIDENCE": {
                "denominator": 1,
                "pass_count": 1 if y_record["pass"] else 0,
                "signature": y_record["signature"],
                "rows": [y_record],
            },
            "case_specific_branch_scan": branch_scan,
        },
        "history_required_generators": {
            "Formalization_Papers": sorted(
                history_required_formalization
            ),
            "Yule_Cordier": sorted(history_required_yule),
        },
        "history_not_required_generators": {
            "Formalization_Papers": sorted(
                history_not_required_formalization
            ),
            "Yule_Cordier": sorted(history_not_required_yule),
        },
        "required_structure": required_structure,
        "overall": (
            "PASS"
            if all(required_structure.values())
            else "FAIL"
        ),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "formalization_denominators": formalization["denominators"],
        "formalization_pass_counts": formalization["pass_counts"],
        "formalization_signatures": formalization["signatures"],
        "yule_signatures": yule_signatures,
        "yule_add_pass": (
            f"{sum(x['pass'] for x in y_add_rows)}/{len(y_add_rows)}"
        ),
        "yule_resolve_pass": "1/1",
        "yule_record_evidence_pass": "1/1",
        "history_required_generators": result[
            "history_required_generators"
        ],
        "history_not_required_generators": result[
            "history_not_required_generators"
        ],
        "required_structure": required_structure,
        "overall": result["overall"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
