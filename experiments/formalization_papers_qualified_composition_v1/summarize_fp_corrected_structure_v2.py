from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main-result", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    main_result = json.loads(
        Path(args.main_result).read_text(encoding="utf-8")
    )

    population = main_result.get("population") or {}
    roots = population.get("roots") or []
    chains = main_result.get("chain_results") or []

    ambiguity_kinds = Counter()
    t8_rows = []
    chain_counts_by_root = Counter()

    for row in roots:
        if row.get("disposition", "").startswith("T8_"):
            kinds = []
            for amb in row.get("ambiguities") or []:
                kind = amb.get("kind", "UNKNOWN")
                ambiguity_kinds[kind] += 1
                kinds.append(kind)
            t8_rows.append({
                "root": row.get("root"),
                "ambiguity_count": len(kinds),
                "ambiguity_kinds": kinds,
            })

    control_counts = defaultdict(lambda: {
        "pass": 0,
        "fail": 0,
        "not_applicable": 0,
        "structurally_unavailable": 0,
    })
    generator_sequences = Counter()
    history_reason_counts = Counter()

    for row in chains:
        chain = row["chain"]
        chain_counts_by_root[chain["root"]] += 1
        generator_sequences[
            tuple(row["forward"]["generators"])
        ] += 1

        for name, ctrl in row["counterfactuals"].items():
            status = ctrl.get("status")
            passed = ctrl.get("pass")
            if status == "NOT_APPLICABLE":
                control_counts[name]["not_applicable"] += 1
            elif status == "STRUCTURALLY_UNAVAILABLE":
                control_counts[name][
                    "structurally_unavailable"
                ] += 1
            elif passed is True:
                control_counts[name]["pass"] += 1
            elif passed is False:
                control_counts[name]["fail"] += 1
            else:
                control_counts[name]["not_applicable"] += 1

        h = row["counterfactuals"]["P4_history_ablation"]
        history_reason_counts[h.get("reason")] += 1

    result = {
        "study": (
            "FORMALIZATION_PAPERS_CORRECTED_RESULT_STRUCTURE_AUDIT_V2"
        ),
        "data_status": "POST_FRESH_EXPOSED_DIAGNOSTIC",
        "root_count": population.get("root_count"),
        "root_disposition_counts": population.get(
            "disposition_counts"
        ),
        "t8_root_count": len(t8_rows),
        "t8_ambiguity_kind_counts": dict(
            sorted(ambiguity_kinds.items())
        ),
        "t8_rows": t8_rows,
        "eligible_chain_count": len(chains),
        "chain_pass_count": sum(
            bool(x.get("pass")) for x in chains
        ),
        "chain_counts_by_root": dict(
            sorted(chain_counts_by_root.items())
        ),
        "generator_sequence_counts": {
            " ; ".join(k): v
            for k, v in sorted(generator_sequences.items())
        },
        "counterfactual_counts": {
            k: v for k, v in sorted(control_counts.items())
        },
        "history_ablation_reasons": dict(
            sorted(history_reason_counts.items())
        ),
        "history_ablation_all_pass": all(
            row["counterfactuals"][
                "P4_history_ablation"
            ].get("pass") is True
            for row in chains
        ),
        "history_ablation_current_projection_all_equal": all(
            row["counterfactuals"][
                "P4_history_ablation"
            ].get("current_projection_equal") is True
            for row in chains
        ),
        "all_chain_pass": all(
            row.get("pass") for row in chains
        ) if chains else False,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "root_count": result["root_count"],
        "root_disposition_counts": result[
            "root_disposition_counts"
        ],
        "t8_ambiguity_kind_counts": result[
            "t8_ambiguity_kind_counts"
        ],
        "eligible_chain_count": result[
            "eligible_chain_count"
        ],
        "chain_pass_count": result["chain_pass_count"],
        "chain_counts_by_root": result[
            "chain_counts_by_root"
        ],
        "generator_sequence_counts": result[
            "generator_sequence_counts"
        ],
        "counterfactual_counts": result[
            "counterfactual_counts"
        ],
        "history_ablation_reasons": result[
            "history_ablation_reasons"
        ],
        "history_ablation_all_pass": result[
            "history_ablation_all_pass"
        ],
        "history_ablation_current_projection_all_equal": (
            result[
                "history_ablation_current_projection_all_equal"
            ]
        ),
        "all_chain_pass": result["all_chain_pass"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
