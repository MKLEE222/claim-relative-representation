from __future__ import annotations

import copy
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import oracle_r
import runtime_r
import evaluator_r

PANEL_PATH = HERE / "HISTORICAL_REASSESSMENT_PANEL_v1.json"
SOURCE_AUDIT_PATH = ROOT / "experiments" / "deepening_v1" / "r3_B02_B03_contrast_audit_v1.csv"

SOURCE_REPOSITORY = "YULE_CORDIER_HISTORICAL_AUDIT"
SOURCE_VERSION = "R3_OBJECT_VERIFIED_20260927"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_panel():
    return json.loads(PANEL_PATH.read_text(encoding="utf-8"))


def load_source_rows():
    with SOURCE_AUDIT_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def audit_panel(panel, source_rows):
    by_id = {}
    duplicates = []
    for row in source_rows:
        key = row["entry_id"]
        if key in by_id:
            duplicates.append(key)
        by_id[key] = row

    checks = []
    ok = not duplicates and len(panel) == len(source_rows) == 5

    panel_ids = {x["entry_id"] for x in panel}
    source_ids = {x["entry_id"] for x in source_rows}
    if panel_ids != source_ids:
        ok = False

    for item in panel:
        row = by_id.get(item["entry_id"])
        row_ok = row is not None
        fields = {}
        if row is not None:
            expected_pairs = {
                "earlier_target_state": item["expected_earlier_target_state"],
                "contrast_type": item["expected_contrast_type"],
                "final_diachronic_relation": item["expected_final_relation"],
                "evidence_authority": item["expected_authority"],
            }
            for field, expected in expected_pairs.items():
                actual = row.get(field)
                fields[field] = {
                    "expected": expected,
                    "actual": actual,
                    "ok": actual == expected,
                }
                row_ok = row_ok and actual == expected
        else:
            fields["row"] = {"expected": "present", "actual": "missing", "ok": False}

        checks.append({
            "entry_id": item["entry_id"],
            "ok": row_ok,
            "fields": fields,
        })
        ok = ok and row_ok

    return {
        "ok": ok,
        "panel_count": len(panel),
        "source_count": len(source_rows),
        "duplicate_entry_ids": duplicates,
        "panel_ids_equal_source_ids": panel_ids == source_ids,
        "checks": checks,
    }


def make_state(item):
    target = item["target_property"]
    root = {
        "claim_id": f"ROOT::{item['entry_id']}",
        "object_id": item["entry_id"],
        "target_property": target,
        "value": item["initial_value"],
        "status": item["initial_status"],
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "source_repository": SOURCE_REPOSITORY,
        "source_version": SOURCE_VERSION,
        "source_id": f"EARLIER::{item['entry_id']}",
        "source_locator": (
            f"r3_B02_B03_contrast_audit_v1.csv::{item['entry_id']}::earlier_target_state"
        ),
        "responsible_agent": item["root_agent"],
    }
    return {
        "object_id": item["entry_id"],
        "source_repository": SOURCE_REPOSITORY,
        "source_version": SOURCE_VERSION,
        "registered_targets": [target],
        "assertions": {target: [root]},
        "evidence_ledger": [],
        "event_ledger": [],
        "transition_ledger": [],
    }


def make_event(item):
    return {
        "event_id": f"R3_REASSESS::{item['entry_id']}",
        "event_class": "SCHOLARLY_REASSESSMENT",
        "object_id": item["entry_id"],
        "target_property": item["target_property"],
        "source_repository": SOURCE_REPOSITORY,
        "source_version": SOURCE_VERSION,
        "evidence_id": item["entry_id"],
        "evidence_locator": (
            f"r3_B02_B03_contrast_audit_v1.csv::{item['entry_id']}::later_contrast"
        ),
        "responsible_agent": item["event_agent"],
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "operation": item["operation"],
        "new_claim_id": f"LATER::{item['entry_id']}",
        "value": item["event_value"],
        "status": item["event_status"],
    }


def expected_disposition(oracle_transition):
    if not oracle_transition.get("applicable"):
        return "REJECTED"
    if oracle_transition.get("substantive"):
        return "SUBSTANTIVE"
    return "ADMISSIBLE_NULL_EVENT"


def eval_comparators(output, oracle_transition, oracle_after_state):
    current = runtime_r.current_reopen(output)
    snaps = runtime_r.ordered_snapshots(output)
    clog = runtime_r.change_log_no_justification(output)

    return {
        "B_CURRENT_REOPEN_R": evaluator_r.evaluate_current_reopen(
            current, oracle_transition, oracle_after_state
        ),
        "B_ORDERED_SNAPSHOTS_R": evaluator_r.evaluate_snapshots(
            snaps, oracle_transition, oracle_after_state
        ),
        "B_CHANGE_LOG_NO_JUSTIFICATION_R": evaluator_r.evaluate_change_log(
            clog, oracle_transition
        ),
    }


def comparator_positive_ok(row):
    c = row["comparators"]["B_CURRENT_REOPEN_R"]
    s = row["comparators"]["B_ORDERED_SNAPSHOTS_R"]
    l = row["comparators"]["B_CHANGE_LOG_NO_JUSTIFICATION_R"]
    return all([
        c["CURRENT_STATE_EXACT"],
        c["CURRENT_PROVENANCE_EXACT"],
        s["PRE_STATE_EXACT"],
        s["POST_STATE_EXACT"],
        s["STATE_DELTA_EXACT"],
        s["CURRENT_PROVENANCE_EXACT"],
        l["CHANGE_EVENT_TARGET_DIFF_EXACT"],
    ])


def main():
    panel = load_panel()
    source_rows = load_source_rows()
    grounding = audit_panel(panel, source_rows)

    results = []
    hard_failure = not grounding["ok"]

    for item in panel:
        state = make_state(item)
        event = make_event(item)

        oracle_transition = oracle_r.apply_event(state, event)
        runtime_output = runtime_r.execute(state, event)
        evaluation = evaluator_r.evaluate(
            runtime_output,
            oracle_transition,
            oracle_transition["state"],
            event,
        )
        comparators = eval_comparators(
            runtime_output,
            oracle_transition,
            oracle_transition["state"],
        )

        disposition = expected_disposition(oracle_transition)
        expected_class = item["expected_transition_class"]

        contract_exact = all([
            disposition == item["expected_disposition"],
            oracle_transition.get("transition_class") == expected_class,
            runtime_output["transition"].get("transition_class") == expected_class,
            runtime_output["transition"].get("applicable")
                == oracle_transition.get("applicable"),
            runtime_output["transition"].get("before_state")
                == oracle_transition.get("before_state"),
            runtime_output["transition"].get("after_state")
                == oracle_transition.get("after_state"),
        ])

        reference_ok = evaluation["reference_end_to_end_pass"]
        comp_ok = comparator_positive_ok({
            "comparators": comparators
        })

        row_ok = contract_exact and reference_ok and comp_ok
        hard_failure = hard_failure or not row_ok

        results.append({
            "entry_id": item["entry_id"],
            "target_property": item["target_property"],
            "expected_disposition": item["expected_disposition"],
            "observed_disposition": disposition,
            "expected_transition_class": expected_class,
            "oracle_transition_class": oracle_transition.get("transition_class"),
            "runtime_transition_class": runtime_output["transition"].get(
                "transition_class"
            ),
            "contract_exact": contract_exact,
            "reference_evaluation": evaluation,
            "comparators": comparators,
            "row_pass": row_ok,
            "source_grounding": {
                "contrast_type": item["expected_contrast_type"],
                "final_diachronic_relation": item["expected_final_relation"],
                "authority": item["expected_authority"],
            },
        })

    substantive = [x for x in results if x["observed_disposition"] == "SUBSTANTIVE"]
    nulls = [
        x for x in results
        if x["observed_disposition"] == "ADMISSIBLE_NULL_EVENT"
    ]

    class_counts = {}
    for row in substantive:
        k = row["oracle_transition_class"]
        class_counts[k] = class_counts.get(k, 0) + 1

    disposition = (
        "INVALID"
        if not grounding["ok"]
        else "EXPOSED_DEVELOPMENT_PARTIAL"
        if hard_failure
        else "EXPOSED_DEVELOPMENT_PASS"
    )

    report = {
        "study": "MODULE_R_YULE_CORDIER_EXPOSED_HISTORICAL_V1",
        "scientific_status": (
            "SOURCE_GROUNDED_NATURAL_EPISODES_PLUS_CONTROLLED_REPRESENTATION_EXECUTION"
        ),
        "source_grounding": {
            "source_audit_file": str(SOURCE_AUDIT_PATH.relative_to(ROOT)),
            "source_audit_sha256": sha256(SOURCE_AUDIT_PATH.read_bytes()),
            "panel_file": str(PANEL_PATH.relative_to(ROOT)),
            "panel_sha256": sha256(PANEL_PATH.read_bytes()),
            "integrity": grounding,
        },
        "denominator": {
            "total_panel_rows": len(results),
            "substantive_reassessments": len(substantive),
            "admissible_null_events": len(nulls),
            "transition_class_counts": class_counts,
        },
        "results": results,
        "overall_disposition": disposition,
        "claim_ceiling": [
            "All five rows were frozen in a pre-Module-R source contrast audit.",
            "The study uses source-grounded human-coded abstractions, not automatic extraction.",
            "A pass is exposed development evidence, not fresh confirmation.",
            "OBJECT_VERIFIED does not substitute for independent historian adjudication.",
            "FRUS was not opened or used by this study.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "historical_exposed_results_v1.json"
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": report["study"],
        "source_grounding_ok": grounding["ok"],
        "denominator": report["denominator"],
        "overall_disposition": disposition,
        "row_summary": [
            {
                "entry_id": x["entry_id"],
                "expected_disposition": x["expected_disposition"],
                "observed_disposition": x["observed_disposition"],
                "transition_class": x["oracle_transition_class"],
                "row_pass": x["row_pass"],
            }
            for x in results
        ],
        "results_sha256": sha256(out_path.read_bytes()),
    }, ensure_ascii=False, indent=2))

    if disposition == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
