from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_oracle
import fp_runtime


def invoke(engine, state, event):
    fn = getattr(engine, "apply", None)
    if fn is None:
        fn = getattr(engine, "execute")
    return fn(state, event)


def exact_step(state, event):
    o = invoke(fp_oracle, state, event)
    r = invoke(fp_runtime, state, event)
    if o != r:
        raise AssertionError({
            "state": state,
            "event": event,
            "oracle": o,
            "runtime": r,
        })
    return o


def initial(context):
    so = fp_oracle.initial_state(
        context["root"], context["submission_np"]
    )
    sr = fp_runtime.initial_state(
        context["root"], context["submission_np"]
    )
    if so != sr:
        raise AssertionError({
            "oracle": so,
            "runtime": sr,
        })
    return so


def event_review(row):
    return {
        "kind": "REVIEW",
        "review_np": row["review_np"],
        "target_formalization": row["root"],
    }


def event_update(row):
    return {
        "kind": "UPDATE",
        "update_np": row["update_np"],
        "target_root": row["root"],
    }


def event_response(row):
    return {
        "kind": "RESPONSE",
        "response_np": row["response_np"],
        "target_review_np": row["review_np"],
        "target_update_np": row["update_np"],
    }


def event_decision(row):
    return {
        "kind": "DECISION",
        "decision_np": row["decision_np"],
        "target_update_np": row["update_np"],
        "status": row["decision_status"],
    }


def denominators(main):
    reviews = {}
    updates = {}
    responses = {}
    decisions = {}
    contexts_by_review = {}

    for result in main.get("chain_results", []):
        c = result["chain"]

        rkey = (c["root"], c["submission_np"], c["review_np"])
        reviews[rkey] = {
            "root": c["root"],
            "submission_np": c["submission_np"],
            "review_np": c["review_np"],
        }
        contexts_by_review.setdefault(rkey, []).append(c)

        ukey = (c["root"], c["submission_np"], c["update_np"])
        updates[ukey] = {
            "root": c["root"],
            "submission_np": c["submission_np"],
            "update_np": c["update_np"],
        }

        pkey = (
            c["root"],
            c["submission_np"],
            c["review_np"],
            c["update_np"],
            c["response_np"],
        )
        responses[pkey] = {
            "root": c["root"],
            "submission_np": c["submission_np"],
            "review_np": c["review_np"],
            "update_np": c["update_np"],
            "response_np": c["response_np"],
        }

        if c.get("decision_np"):
            dkey = (
                c["root"],
                c["submission_np"],
                c["update_np"],
                c["decision_np"],
                c["decision_status"],
            )
            decisions[dkey] = {
                "root": c["root"],
                "submission_np": c["submission_np"],
                "update_np": c["update_np"],
                "decision_np": c["decision_np"],
                "decision_status": c["decision_status"],
            }

    return {
        "reviews": [reviews[k] for k in sorted(reviews)],
        "updates": [updates[k] for k in sorted(updates)],
        "responses": [responses[k] for k in sorted(responses)],
        "decisions": [decisions[k] for k in sorted(decisions)],
        "contexts_by_review": {
            k: sorted(
                v,
                key=lambda x: (
                    x["update_np"],
                    x["response_np"],
                    x.get("decision_np", ""),
                ),
            )
            for k, v in contexts_by_review.items()
        },
    }


def first_foreign(rows, root, field):
    vals = sorted({
        row[field]
        for row in rows
        if row["root"] != root
    })
    if not vals:
        raise AssertionError({
            "root": root,
            "field": field,
            "error": "NO_FOREIGN_CANDIDATE",
        })
    return vals[0]


def audit_review(row, den):
    s0 = initial(row)
    ev = event_review(row)
    valid = exact_step(s0, ev)

    foreign_root = first_foreign(
        den["reviews"], row["root"], "root"
    )
    wrong = copy.deepcopy(ev)
    wrong["target_formalization"] = foreign_root
    wrong_result = exact_step(s0, wrong)

    rkey = (row["root"], row["submission_np"], row["review_np"])
    connected = den["contexts_by_review"][rkey][0]
    update_ev = event_update(connected)
    after_update = exact_step(s0, update_ev)
    if not after_update["qualified"]:
        raise AssertionError(after_update)
    stale_review = exact_step(after_update["state"], ev)

    passed = all([
        valid["qualified"]
        and valid["generator"] == "RECORD_REVIEW",
        not wrong_result["qualified"],
        wrong_result["reason"] == "RELATION_TARGET_NOT_LIVE",
        not stale_review["qualified"],
        stale_review["reason"] == "RELATION_TARGET_NOT_LIVE",
    ])
    return {
        "action": row,
        "valid": valid["qualified"],
        "wrong_target_rejected": not wrong_result["qualified"],
        "stale_target_rejected": not stale_review["qualified"],
        "wrong_target_reason": wrong_result["reason"],
        "stale_target_reason": stale_review["reason"],
        "history_signature": "ROOT_ACTION_NO_PRIOR_HISTORY",
        "pass": passed,
    }


def audit_update(row, den):
    s0 = initial(row)
    ev = event_update(row)
    valid = exact_step(s0, ev)

    foreign_root = first_foreign(
        den["updates"], row["root"], "root"
    )
    wrong = copy.deepcopy(ev)
    wrong["target_root"] = foreign_root
    wrong_result = exact_step(s0, wrong)

    retracted = copy.deepcopy(s0)
    retracted["retracted"] = [row["update_np"]]
    retracted_result = exact_step(retracted, ev)

    passed = all([
        valid["qualified"]
        and valid["generator"] == "REPLACE_FORMALIZATION",
        not wrong_result["qualified"],
        wrong_result["reason"] == "UPDATE_TARGET_UNRESOLVED",
        not retracted_result["qualified"],
        retracted_result["reason"] == "UPDATE_TARGET_RETRACTED",
        len(s0["history"]) == 0,
    ])
    return {
        "action": row,
        "valid_without_prior_history": valid["qualified"],
        "wrong_root_rejected": not wrong_result["qualified"],
        "retracted_update_rejected": not retracted_result["qualified"],
        "wrong_root_reason": wrong_result["reason"],
        "retraction_reason": retracted_result["reason"],
        "history_signature": "NOT_REQUIRED_IN_REGISTERED_TASK",
        "pass": passed,
    }


def before_response(row):
    s0 = initial(row)
    review = exact_step(s0, event_review(row))
    if not review["qualified"]:
        raise AssertionError(review)
    update = exact_step(review["state"], event_update(row))
    if not update["qualified"]:
        raise AssertionError(update)
    return s0, review["state"], update["state"]


def audit_response(row, den):
    s0, after_review, before = before_response(row)
    ev = event_response(row)
    valid = exact_step(before, ev)

    before_review = exact_step(s0, ev)
    before_update = exact_step(after_review, ev)

    ablated = copy.deepcopy(before)
    current_before = {
        "current_formalization": before["current_formalization"],
        "current_update_np": before["current_update_np"],
        "publication_status": before["publication_status"],
        "live_reviews": sorted(before["live_reviews"]),
    }
    ablated["history"] = []
    current_after = {
        "current_formalization": ablated["current_formalization"],
        "current_update_np": ablated["current_update_np"],
        "publication_status": ablated["publication_status"],
        "live_reviews": sorted(ablated["live_reviews"]),
    }
    history_result = exact_step(ablated, ev)

    wrong_review = copy.deepcopy(ev)
    wrong_review["target_review_np"] = first_foreign(
        den["responses"], row["root"], "review_np"
    )
    wrong_review_result = exact_step(before, wrong_review)

    wrong_update = copy.deepcopy(ev)
    wrong_update["target_update_np"] = first_foreign(
        den["responses"], row["root"], "update_np"
    )
    wrong_update_result = exact_step(before, wrong_update)

    passed = all([
        valid["qualified"]
        and valid["generator"] == "RECORD_RESPONSE",
        not before_review["qualified"]
        and before_review["reason"]
            == "RESPONSE_REVIEW_TARGET_NOT_LIVE",
        not before_update["qualified"]
        and before_update["reason"]
            == "RESPONSE_UPDATE_TARGET_NOT_LIVE",
        current_before == current_after,
        not history_result["qualified"]
        and history_result["reason"]
            == "RESPONSE_TARGET_HISTORY_UNRESOLVED",
        not wrong_review_result["qualified"],
        not wrong_update_result["qualified"],
    ])
    return {
        "action": row,
        "valid": valid["qualified"],
        "review_target_required": not before_review["qualified"],
        "update_target_required": not before_update["qualified"],
        "history_required": not history_result["qualified"],
        "history_reason": history_result["reason"],
        "current_projection_equal_after_history_ablation": (
            current_before == current_after
        ),
        "wrong_review_rejected": not wrong_review_result["qualified"],
        "wrong_update_rejected": not wrong_update_result["qualified"],
        "history_signature": "REQUIRED",
        "pass": passed,
    }


def audit_decision(row, den):
    s0 = initial(row)
    update = exact_step(s0, event_update(row))
    if not update["qualified"]:
        raise AssertionError(update)

    ev = event_decision(row)
    valid = exact_step(update["state"], ev)
    before_update = exact_step(s0, ev)

    ablated = copy.deepcopy(update["state"])
    current_before = {
        "current_formalization": update["state"]["current_formalization"],
        "current_update_np": update["state"]["current_update_np"],
        "publication_status": update["state"]["publication_status"],
    }
    ablated["history"] = []
    current_after = {
        "current_formalization": ablated["current_formalization"],
        "current_update_np": ablated["current_update_np"],
        "publication_status": ablated["publication_status"],
    }
    history_result = exact_step(ablated, ev)

    wrong = copy.deepcopy(ev)
    wrong["target_update_np"] = first_foreign(
        den["decisions"], row["root"], "update_np"
    )
    wrong_result = exact_step(update["state"], wrong)

    passed = all([
        valid["qualified"]
        and valid["generator"] == "REVISE_PUBLICATION_STATUS",
        not before_update["qualified"]
        and before_update["reason"] == "DECISION_TARGET_NOT_CURRENT",
        current_before == current_after,
        history_result["qualified"]
        and history_result["generator"]
            == "REVISE_PUBLICATION_STATUS",
        not wrong_result["qualified"],
        wrong_result["reason"] == "DECISION_TARGET_NOT_CURRENT",
    ])
    return {
        "action": row,
        "valid": valid["qualified"],
        "current_update_required": not before_update["qualified"],
        "history_ablated_still_qualified": history_result["qualified"],
        "current_projection_equal_after_history_ablation": (
            current_before == current_after
        ),
        "wrong_update_rejected": not wrong_result["qualified"],
        "history_signature": "NOT_REQUIRED_IN_REGISTERED_TASK",
        "pass": passed,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main-result", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    main_result = json.loads(
        Path(args.main_result).read_text(encoding="utf-8")
    )
    den = denominators(main_result)

    review_rows = [
        audit_review(x, den) for x in den["reviews"]
    ]
    update_rows = [
        audit_update(x, den) for x in den["updates"]
    ]
    response_rows = [
        audit_response(x, den) for x in den["responses"]
    ]
    decision_rows = [
        audit_decision(x, den) for x in den["decisions"]
    ]

    signature = {
        "RECORD_REVIEW": {
            "TARGET_IDENTITY": "REQUIRED",
            "CURRENT_OR_LIVE_TARGET": "REQUIRED",
            "RETAINED_HISTORY": "ROOT_ACTION_NO_PRIOR_HISTORY",
        },
        "REPLACE_FORMALIZATION": {
            "TARGET_IDENTITY": "REQUIRED",
            "RETRACTION_STATUS": "REQUIRED",
            "RETAINED_HISTORY": (
                "NOT_REQUIRED_IN_REGISTERED_TASK"
            ),
        },
        "RECORD_RESPONSE": {
            "REVIEW_TARGET_LIVE": "REQUIRED",
            "UPDATE_TARGET_CURRENT": "REQUIRED",
            "TARGET_IDENTITY": "REQUIRED",
            "RETAINED_HISTORY": "REQUIRED",
        },
        "REVISE_PUBLICATION_STATUS": {
            "UPDATE_TARGET_CURRENT": "REQUIRED",
            "TARGET_IDENTITY": "REQUIRED",
            "RETAINED_HISTORY": (
                "NOT_REQUIRED_IN_REGISTERED_TASK"
            ),
        },
    }

    all_rows = (
        review_rows + update_rows + response_rows + decision_rows
    )
    result = {
        "study": (
            "FORMALIZATION_PAPERS_GENERATOR_QUALIFICATION_SIGNATURE_AUDIT_V1"
        ),
        "data_status": "POST_FRESH_EXPOSED_CONDITIONAL_MINIMALITY_AUDIT",
        "denominators": {
            "D_REVIEW": len(review_rows),
            "D_UPDATE": len(update_rows),
            "D_RESPONSE": len(response_rows),
            "D_DECISION": len(decision_rows),
        },
        "pass_counts": {
            "RECORD_REVIEW": sum(x["pass"] for x in review_rows),
            "REPLACE_FORMALIZATION": sum(
                x["pass"] for x in update_rows
            ),
            "RECORD_RESPONSE": sum(
                x["pass"] for x in response_rows
            ),
            "REVISE_PUBLICATION_STATUS": sum(
                x["pass"] for x in decision_rows
            ),
        },
        "qualification_signature": signature,
        "rows": {
            "reviews": review_rows,
            "updates": update_rows,
            "responses": response_rows,
            "decisions": decision_rows,
        },
        "history_heterogeneity": {
            "REPLACE_FORMALIZATION": (
                "NOT_REQUIRED_IN_REGISTERED_TASK"
            ),
            "RECORD_RESPONSE": "REQUIRED",
            "REVISE_PUBLICATION_STATUS": (
                "NOT_REQUIRED_IN_REGISTERED_TASK"
            ),
        },
        "overall": "PASS" if all(x["pass"] for x in all_rows) else "FAIL",
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "denominators": result["denominators"],
        "pass_counts": result["pass_counts"],
        "qualification_signature": signature,
        "history_heterogeneity": result["history_heterogeneity"],
        "overall": result["overall"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
