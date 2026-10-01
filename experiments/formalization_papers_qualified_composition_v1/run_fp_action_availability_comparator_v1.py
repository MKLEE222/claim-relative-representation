from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter
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


def relation_target_available(event):
    return all([
        bool(event.get("target_review_np")),
        bool(event.get("target_update_np")),
    ])


def live_target_available(state, event):
    return all([
        event.get("target_review_np")
        in state.get("live_reviews", []),
        event.get("target_update_np")
        == state.get("current_update_np"),
    ])


def response_event(context):
    return {
        "kind": "RESPONSE",
        "response_np": context["response_np"],
        "target_review_np": context["review_np"],
        "target_update_np": context["update_np"],
    }


def build_before_response(context):
    review = {
        "kind": "REVIEW",
        "review_np": context["review_np"],
        "target_formalization": context["root"],
    }
    update = {
        "kind": "UPDATE",
        "update_np": context["update_np"],
        "target_root": context["root"],
    }

    so = fp_oracle.initial_state(
        context["root"], context["submission_np"]
    )
    sr = fp_runtime.initial_state(
        context["root"], context["submission_np"]
    )
    if so != sr:
        raise AssertionError("initial state disagreement")

    ro = invoke(fp_oracle, so, review)
    rr = invoke(fp_runtime, sr, review)
    if ro != rr or not ro["qualified"]:
        raise AssertionError({
            "stage": "review",
            "oracle": ro,
            "runtime": rr,
        })

    uo = invoke(fp_oracle, ro["state"], update)
    ur = invoke(fp_runtime, rr["state"], update)
    if uo != ur or not uo["qualified"]:
        raise AssertionError({
            "stage": "update",
            "oracle": uo,
            "runtime": ur,
        })
    return uo["state"]


def unique_positive_contexts(main):
    seen = {}
    for row in main.get("chain_results", []):
        c = row["chain"]
        key = (
            c["root"],
            c["review_np"],
            c["update_np"],
            c["response_np"],
        )
        seen[key] = {
            "root": c["root"],
            "submission_np": c["submission_np"],
            "review_np": c["review_np"],
            "update_np": c["update_np"],
            "response_np": c["response_np"],
        }
    return [seen[k] for k in sorted(seen)]


def t8_instances(main):
    nonlive = {}
    nonfunctional = {}
    for root in (main.get("population") or {}).get("roots", []):
        if not root.get("disposition", "").startswith("T8_"):
            continue
        for amb in root.get("ambiguities", []):
            kind = amb.get("kind")
            package = amb.get("package")
            if kind == "RESPONSE_UPDATE_TARGET_NOT_LIVE":
                key = (root["root"], package, amb.get("target"))
                nonlive[key] = {
                    "root": root["root"],
                    "response_np": package,
                    "target_update_np": amb.get("target"),
                }
            elif kind == "RESPONSE_NONFUNCTIONAL_TARGET":
                key = (root["root"], package)
                nonfunctional[key] = {
                    "root": root["root"],
                    "response_np": package,
                    "detail": amb,
                }
    return (
        [nonlive[k] for k in sorted(nonlive)],
        [nonfunctional[k] for k in sorted(nonfunctional)],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main-result", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    main_result = json.loads(
        Path(args.main_result).read_text(encoding="utf-8")
    )

    positives = unique_positive_contexts(main_result)
    nonlive, nonfunctional = t8_instances(main_result)

    positive_rows = []
    history_rows = []

    for context in positives:
        state = build_before_response(context)
        event = response_event(context)

        b_relation = relation_target_available(event)
        b_live = live_target_available(state, event)

        qo = invoke(fp_oracle, state, event)
        qr = invoke(fp_runtime, state, event)
        if qo != qr:
            raise AssertionError({
                "context": context,
                "oracle": qo,
                "runtime": qr,
            })
        q_full = bool(qo["qualified"])

        positive_rows.append({
            "context": context,
            "B_RELATION_TARGET": b_relation,
            "B_LIVE_TARGET": b_live,
            "Q_FULL_HISTORY": q_full,
            "Q_generator": qo.get("generator"),
        })

        ablated = copy.deepcopy(state)
        current_projection_before = {
            "current_formalization": state["current_formalization"],
            "current_update_np": state["current_update_np"],
            "publication_status": state["publication_status"],
            "live_reviews": sorted(state["live_reviews"]),
        }
        ablated["history"] = []
        current_projection_after = {
            "current_formalization": ablated["current_formalization"],
            "current_update_np": ablated["current_update_np"],
            "publication_status": ablated["publication_status"],
            "live_reviews": sorted(ablated["live_reviews"]),
        }

        aqo = invoke(fp_oracle, ablated, event)
        aqr = invoke(fp_runtime, ablated, event)
        if aqo != aqr:
            raise AssertionError({
                "context": context,
                "oracle": aqo,
                "runtime": aqr,
            })

        history_rows.append({
            "context": context,
            "current_projection_equal": (
                current_projection_before == current_projection_after
            ),
            "B_RELATION_TARGET": relation_target_available(event),
            "B_LIVE_TARGET": live_target_available(ablated, event),
            "Q_FULL_HISTORY": bool(aqo["qualified"]),
            "Q_reason": aqo.get("reason"),
        })

    natural_nonlive_rows = [
        {
            **row,
            "B_RELATION_TARGET": True,
            "B_LIVE_TARGET": False,
            "Q_FULL_HISTORY": False,
            "reference_reason": "RESPONSE_UPDATE_TARGET_NOT_LIVE",
        }
        for row in nonlive
    ]

    nonfunctional_rows = [
        {
            **row,
            "B_RELATION_TARGET": False,
            "B_LIVE_TARGET": False,
            "Q_FULL_HISTORY": False,
            "reference_reason": "RESPONSE_NONFUNCTIONAL_TARGET",
        }
        for row in nonfunctional
    ]

    def count_available(rows, key):
        return sum(bool(x[key]) for x in rows)

    result = {
        "study": "FORMALIZATION_PAPERS_ACTION_AVAILABILITY_COMPARATOR_AUDIT_V1",
        "data_status": "POST_FRESH_EXPOSED_MECHANISM_AUDIT",
        "denominators": {
            "D_POSITIVE_unique_response_contexts": len(positive_rows),
            "D_NONLIVE_unique_response_acts": len(natural_nonlive_rows),
            "D_NONFUNCTIONAL_unique_response_acts": len(
                nonfunctional_rows
            ),
            "D_HISTORY_ABLATED_unique_response_contexts": len(
                history_rows
            ),
        },
        "positive_availability": {
            "B_RELATION_TARGET": count_available(
                positive_rows, "B_RELATION_TARGET"
            ),
            "B_LIVE_TARGET": count_available(
                positive_rows, "B_LIVE_TARGET"
            ),
            "Q_FULL_HISTORY": count_available(
                positive_rows, "Q_FULL_HISTORY"
            ),
        },
        "nonlive_false_availability": {
            "B_RELATION_TARGET": count_available(
                natural_nonlive_rows, "B_RELATION_TARGET"
            ),
            "B_LIVE_TARGET": count_available(
                natural_nonlive_rows, "B_LIVE_TARGET"
            ),
            "Q_FULL_HISTORY": count_available(
                natural_nonlive_rows, "Q_FULL_HISTORY"
            ),
        },
        "history_ablated_false_availability": {
            "B_RELATION_TARGET": count_available(
                history_rows, "B_RELATION_TARGET"
            ),
            "B_LIVE_TARGET": count_available(
                history_rows, "B_LIVE_TARGET"
            ),
            "Q_FULL_HISTORY": count_available(
                history_rows, "Q_FULL_HISTORY"
            ),
        },
        "nonfunctional_availability": {
            "B_RELATION_TARGET": count_available(
                nonfunctional_rows, "B_RELATION_TARGET"
            ),
            "B_LIVE_TARGET": count_available(
                nonfunctional_rows, "B_LIVE_TARGET"
            ),
            "Q_FULL_HISTORY": count_available(
                nonfunctional_rows, "Q_FULL_HISTORY"
            ),
        },
        "history_rejection_reasons": dict(sorted(Counter(
            x.get("Q_reason") for x in history_rows
        ).items())),
        "positive_rows": positive_rows,
        "nonlive_rows": natural_nonlive_rows,
        "nonfunctional_rows": nonfunctional_rows,
        "history_ablated_rows": history_rows,
    }

    required = {
        "positive_preservation": all([
            result["positive_availability"]["B_RELATION_TARGET"]
                == len(positive_rows),
            result["positive_availability"]["B_LIVE_TARGET"]
                == len(positive_rows),
            result["positive_availability"]["Q_FULL_HISTORY"]
                == len(positive_rows),
        ]),
        "live_target_separation": all([
            result["nonlive_false_availability"]["B_RELATION_TARGET"]
                == len(natural_nonlive_rows),
            result["nonlive_false_availability"]["B_LIVE_TARGET"] == 0,
            result["nonlive_false_availability"]["Q_FULL_HISTORY"] == 0,
        ]),
        "history_separation": all([
            result["history_ablated_false_availability"][
                "B_RELATION_TARGET"
            ] == len(history_rows),
            result["history_ablated_false_availability"][
                "B_LIVE_TARGET"
            ] == len(history_rows),
            result["history_ablated_false_availability"][
                "Q_FULL_HISTORY"
            ] == 0,
            all(
                x["current_projection_equal"] for x in history_rows
            ),
            all(
                x["Q_reason"]
                == "RESPONSE_TARGET_HISTORY_UNRESOLVED"
                for x in history_rows
            ),
        ]),
        "nonfunctional_discipline": (
            result["nonfunctional_availability"][
                "B_RELATION_TARGET"
            ] == 0
        ),
    }
    result["required_separations"] = required
    result["overall"] = (
        "PASS" if all(required.values()) else "FAIL"
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "denominators": result["denominators"],
        "positive_availability": result["positive_availability"],
        "nonlive_false_availability": result[
            "nonlive_false_availability"
        ],
        "history_ablated_false_availability": result[
            "history_ablated_false_availability"
        ],
        "nonfunctional_availability": result[
            "nonfunctional_availability"
        ],
        "history_rejection_reasons": result[
            "history_rejection_reasons"
        ],
        "required_separations": required,
        "overall": result["overall"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
