from __future__ import annotations

import json
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
import run_exposed_regression as lr
import runtime_l


TASKS = (
    "T1_CURRENT_STATE_EXACT",
    "T2_CURRENT_PROVENANCE_EXACT",
    "T3_STATE_DELTA_EXACT",
    "T4_TRANSITION_ATTRIBUTION_EXACT",
    "T5_DELAYED_HISTORY_AUDIT_EXACT",
)


def evaluate_row(row):
    trace = runtime_l.execute(row["runtime"], "I_RSTAR")
    outputs = {
        "RSTAR": comparators_m.rstar_view(row["runtime"], trace),
        "B_CURRENT_REOPEN": comparators_m.current_reopen(row["runtime"]),
        "B_ORDERED_SNAPSHOTS": comparators_m.ordered_snapshots(row["runtime"]),
    }
    return {
        name: evaluator_m.evaluate_regime(out, row["oracle"])
        for name, out in outputs.items()
    }


def aggregate(evaluations, regime):
    rows = [x[regime] for x in evaluations]
    return {
        "episodes": len(rows),
        **{
            task: sum(bool(x.get(task)) for x in rows)
            for task in TASKS
        },
        "positive_current_capability": sum(
            bool(x.get("positive_current_capability")) for x in rows
        ),
        "positive_snapshot_capability": sum(
            bool(x.get("positive_snapshot_capability")) for x in rows
        ),
        "full_registered_history_capability": sum(
            bool(x.get("full_registered_history_capability")) for x in rows
        ),
    }


def corpus_disposition(n, aggs):
    if n == 0:
        return "NO_ELIGIBLE_EXPOSED_EPISODES"

    current = aggs["B_CURRENT_REOPEN"]
    snapshots = aggs["B_ORDERED_SNAPSHOTS"]
    rstar = aggs["RSTAR"]

    positive_ok = all([
        current["T1_CURRENT_STATE_EXACT"] == n,
        current["T2_CURRENT_PROVENANCE_EXACT"] == n,
        snapshots["T1_CURRENT_STATE_EXACT"] == n,
        snapshots["T2_CURRENT_PROVENANCE_EXACT"] == n,
        snapshots["T3_STATE_DELTA_EXACT"] == n,
        all(rstar[t] == n for t in TASKS),
    ])
    if not positive_ok:
        return "INVALID_POSITIVE_CAPABILITY_GATE"

    current_history = (
        current["T4_TRANSITION_ATTRIBUTION_EXACT"] == n
        and current["T5_DELAYED_HISTORY_AUDIT_EXACT"] == n
    )
    snapshot_history = (
        snapshots["T4_TRANSITION_ATTRIBUTION_EXACT"] == n
        and snapshots["T5_DELAYED_HISTORY_AUDIT_EXACT"] == n
    )

    if current_history or snapshot_history:
        return "COMPARATOR_RECOVERS_REGISTERED_HISTORY"

    return "EXPOSED_HISTORY_SEPARATION"


def main():
    archive_url = (
        f"https://github.com/{lr.jr.UPSTREAM_REPO}/archive/"
        f"{lr.jr.UPSTREAM_COMMIT}.tar.gz"
    )
    archive_raw = lr.jr.fetch(archive_url)

    report = {
        "study": "MODULE_M_DH_COMPARATORS_EXPOSED_V1",
        "source_context": lr.SOURCE_CONTEXT,
        "archive_sha256": lr.jr.sha256(archive_raw),
        "interpretation": (
            "EXPOSED DEVELOPMENT COMPARATOR STUDY ONLY. "
            "This run cannot establish unseen-corpus superiority."
        ),
        "corpora": {},
    }

    hard_failure = False

    for name, prefix in lr.jr.EXPOSED_PREFIXES.items():
        rows, errors = lr.load_prefix(prefix, archive_raw)
        unresolved = [r for r in rows if not r["contract"]["ok"]]
        full = [
            r for r in rows
            if (r["oracle"].get("object_contract") or {}).get("status")
                == "SINGLE_PRIMARY_DOCUMENT_OBJECT"
            and r["oracle"].get("full_trajectory_eligible")
        ]

        evaluations = [evaluate_row(r) for r in full]
        aggs = {
            regime: aggregate(evaluations, regime)
            for regime in ("RSTAR", "B_CURRENT_REOPEN", "B_ORDERED_SNAPSHOTS")
        }

        disposition = corpus_disposition(len(full), aggs)

        report["corpora"][name] = {
            "prefix": prefix,
            "parse_errors": errors,
            "contract_unresolved": [
                {"path": r["path"], "reasons": r["contract"]["reasons"]}
                for r in unresolved
            ],
            "eligible_full_trajectories": len(full),
            "aggregates": aggs,
            "disposition": disposition,
            "episode_evaluations": [
                {
                    "path": r["path"],
                    "evaluations": ev,
                }
                for r, ev in zip(full, evaluations)
            ],
        }

        if errors or unresolved or disposition == "INVALID_POSITIVE_CAPABILITY_GATE":
            hard_failure = True

    nonempty = [
        x for x in report["corpora"].values()
        if x["eligible_full_trajectories"] > 0
    ]
    if hard_failure:
        overall = "INVALID"
    elif nonempty and all(
        x["disposition"] == "EXPOSED_HISTORY_SEPARATION"
        for x in nonempty
    ):
        overall = "EXPOSED_HISTORY_SEPARATION"
    elif nonempty:
        overall = "MIXED"
    else:
        overall = "NO_ELIGIBLE_EPISODES"

    report["overall_disposition"] = overall
    report["claim_ceiling"] = [
        "Current-source reopening is tested as a positive current-state baseline.",
        "Ordered snapshots are tested as a positive current-state and state-delta baseline.",
        "Any observed history separation is exposed development evidence only.",
        "No fresh independent superiority claim is licensed by Module M.",
    ]

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "exposed_comparator_results_v1.json"
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if hard_failure:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
