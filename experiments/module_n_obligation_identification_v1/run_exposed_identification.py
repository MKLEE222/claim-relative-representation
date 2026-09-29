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

import evaluator_n
import interventions_n
import run_exposed_regression as lr


CAPABILITIES = (
    "C1_CURRENT_STATE",
    "C2_DISCOVERY",
    "C3_EVENT_APPLICABILITY",
    "C4_RESULT_DETERMINACY",
    "C5_SELECTIVITY",
    "C6_CURRENT_PROVENANCE",
    "C7_TRANSITION_ATTRIBUTION",
    "C8_DELAYED_HISTORY",
)


def evaluate_row(row):
    out = {}
    for arm in interventions_n.ARMS:
        trace = interventions_n.run_arm(row["runtime"], arm)
        out[arm] = evaluator_n.evaluate(trace, row["oracle"])
    return out


def aggregate(evaluations, arm):
    rows = [x[arm] for x in evaluations]
    applicable = rows
    if arm == "N_COLLAPSE_RESULT_STATUS":
        applicable = [
            x for x in rows
            if x.get("result_status_intervention_applicable") is True
        ]
    return {
        "episodes_total": len(rows),
        "episodes_applicable": len(applicable),
        **{
            cap: sum(bool(x.get(cap)) for x in applicable)
            for cap in CAPABILITIES
        },
        "rejection_reasons": {
            reason: sum(1 for x in applicable if x.get("rejection_reason") == reason)
            for reason in sorted({
                x.get("rejection_reason")
                for x in applicable
                if x.get("rejection_reason")
            })
        },
    }


def crossovers(evaluations):
    a_o1o2 = []
    b_o6o7 = []
    c_o5o8 = []
    d_o4o8 = []

    for ev in evaluations:
        no_obj = ev["N_NO_OBJECT_ID"]
        no_app = ev["N_NO_APPLICABILITY"]
        no_prov = ev["N_NO_CURRENT_PROVENANCE"]
        no_trans = ev["N_NO_TRANSITION_BINDING"]
        collateral = ev["N_COLLATERAL_UPDATE"]
        no_hist = ev["N_NO_HISTORY"]
        collapse = ev["N_COLLAPSE_RESULT_STATUS"]

        a_o1o2.append(all([
            no_obj["C1_CURRENT_STATE"],
            no_obj["C2_DISCOVERY"],
            not no_obj["C3_EVENT_APPLICABILITY"],
            not no_obj["C7_TRANSITION_ATTRIBUTION"],
            no_obj["rejection_reason"] == "NO_BOUND_OBJECT",
            no_app["C1_CURRENT_STATE"],
            no_app["C2_DISCOVERY"],
            not no_app["C3_EVENT_APPLICABILITY"],
            not no_app["C7_TRANSITION_ATTRIBUTION"],
            no_app["rejection_reason"] == "INVALID_OBJECT_OR_APPLICABILITY_BINDING",
        ]))

        b_o6o7.append(all([
            no_prov["C1_CURRENT_STATE"],
            no_prov["C3_EVENT_APPLICABILITY"],
            not no_prov["C6_CURRENT_PROVENANCE"],
            no_prov["C7_TRANSITION_ATTRIBUTION"],
            no_prov["C8_DELAYED_HISTORY"],
            no_trans["C1_CURRENT_STATE"],
            no_trans["C2_DISCOVERY"],
            no_trans["C6_CURRENT_PROVENANCE"],
            not no_trans["C3_EVENT_APPLICABILITY"],
            not no_trans["C7_TRANSITION_ATTRIBUTION"],
            no_trans["rejection_reason"] == "ORIGIN_HANDLE_BINDING_MISMATCH",
        ]))

        c_o5o8.append(all([
            collateral["C3_EVENT_APPLICABILITY"],
            collateral["C7_TRANSITION_ATTRIBUTION"],
            not collateral["C5_SELECTIVITY"],
            collateral["C8_DELAYED_HISTORY"],
            no_hist["C4_RESULT_DETERMINACY"],
            no_hist["C5_SELECTIVITY"],
            not no_hist["C8_DELAYED_HISTORY"],
        ]))

        if collapse.get("result_status_intervention_applicable") is True:
            d_o4o8.append(all([
                not collapse["C4_RESULT_DETERMINACY"],
                collapse["C5_SELECTIVITY"],
                collapse["C8_DELAYED_HISTORY"],
                no_hist["C4_RESULT_DETERMINACY"],
                not no_hist["C8_DELAYED_HISTORY"],
            ]))

    return {
        "O1_vs_O2": {
            "denominator": len(a_o1o2),
            "pass": sum(a_o1o2),
        },
        "O6_vs_O7": {
            "denominator": len(b_o6o7),
            "pass": sum(b_o6o7),
        },
        "O5_vs_O8": {
            "denominator": len(c_o5o8),
            "pass": sum(c_o5o8),
        },
        "O4_vs_O8": {
            "denominator": len(d_o4o8),
            "pass": sum(d_o4o8),
        },
    }


def main():
    archive_url = (
        f"https://github.com/{lr.jr.UPSTREAM_REPO}/archive/"
        f"{lr.jr.UPSTREAM_COMMIT}.tar.gz"
    )
    archive_raw = lr.jr.fetch(archive_url)

    report = {
        "study": "MODULE_N_OBLIGATION_IDENTIFICATION_EXPOSED_V1",
        "source_context": lr.SOURCE_CONTEXT,
        "archive_sha256": lr.jr.sha256(archive_raw),
        "interpretation": (
            "EXPOSED DEVELOPMENT IDENTIFICATION ONLY. "
            "Capability crossovers are reported without a scalar representation score."
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
            arm: aggregate(evaluations, arm)
            for arm in interventions_n.ARMS
        }
        xov = crossovers(evaluations)

        full_ok = all(
            aggs["N_FULL"][cap] == len(full)
            for cap in CAPABILITIES
        ) if full else True

        report["corpora"][name] = {
            "prefix": prefix,
            "parse_errors": errors,
            "contract_unresolved": [
                {"path": r["path"], "reasons": r["contract"]["reasons"]}
                for r in unresolved
            ],
            "eligible_full_trajectories": len(full),
            "full_reference_valid": full_ok,
            "aggregates": aggs,
            "crossovers": xov,
            "episode_evaluations": [
                {"path": r["path"], "evaluations": ev}
                for r, ev in zip(full, evaluations)
            ],
        }

        if errors or unresolved or not full_ok:
            hard_failure = True

    report["overall_status"] = "INVALID" if hard_failure else "EXPOSED_RESULTS_RECORDED"
    report["claim_ceiling"] = [
        "Crossovers isolate obligations on exposed development episodes only.",
        "No scalar representation-quality score is licensed.",
        "No general necessity claim is licensed without fresh independent support.",
    ]

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "exposed_obligation_results_v1.json"
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if hard_failure:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
