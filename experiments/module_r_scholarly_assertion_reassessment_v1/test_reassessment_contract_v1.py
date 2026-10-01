from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import oracle_r
import runtime_r
import evaluator_r


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def assertion(
    claim_id,
    target,
    value,
    status="ACCEPTED",
    source_id="SRC-ROOT",
    source_locator="root:1",
    agent="editor-root",
):
    return {
        "claim_id": claim_id,
        "object_id": "OBJ-1",
        "target_property": target,
        "value": value,
        "status": status,
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "source_repository": "SYNTHETIC/R",
        "source_version": "r-v1",
        "source_id": source_id,
        "source_locator": source_locator,
        "responsible_agent": agent,
    }


def base_state():
    return {
        "object_id": "OBJ-1",
        "source_repository": "SYNTHETIC/R",
        "source_version": "r-v1",
        "registered_targets": [
            "author-attribution",
            "evidence-status",
            "source-status",
        ],
        "assertions": {
            "author-attribution": [
                assertion("C-A", "author-attribution", "Author-A")
            ],
            "source-status": [
                assertion(
                    "C-S",
                    "source-status",
                    "SOURCE-1",
                    status="TRUSTED",
                    source_id="SRC-STATUS",
                    source_locator="status:1",
                )
            ],
            "evidence-status": [
                assertion(
                    "C-E",
                    "evidence-status",
                    "EVIDENCE-1",
                    status="DIRECT",
                    source_id="SRC-EVID",
                    source_locator="evidence:1",
                )
            ],
        },
        "evidence_ledger": [],
        "event_ledger": [],
        "transition_ledger": [],
    }


def event(
    event_id,
    target,
    operation,
    value,
    status,
    evidence_id,
    evidence_locator,
    agent="editor-2",
    event_class="SCHOLARLY_REASSESSMENT",
):
    return {
        "event_id": event_id,
        "event_class": event_class,
        "object_id": "OBJ-1",
        "target_property": target,
        "source_repository": "SYNTHETIC/R",
        "source_version": "r-v1",
        "evidence_id": evidence_id,
        "evidence_locator": evidence_locator,
        "responsible_agent": agent,
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "operation": operation,
        "new_claim_id": "NEW::" + event_id,
        "value": value,
        "status": status,
    }


def oracle_and_runtime(state, ev, **runtime_kwargs):
    otr = oracle_r.apply_event(state, ev)
    out = runtime_r.execute(state, ev, **runtime_kwargs)
    evr = evaluator_r.evaluate(out, otr, otr["state"], ev)
    return otr, out, evr


def main():
    results = {}

    # R-F1: attribution replacement.
    s1 = base_state()
    e1 = event(
        "EV-ATTR-REPLACE",
        "author-attribution",
        "REPLACE",
        "Author-B",
        "ACCEPTED",
        "EVID-ATTR-B",
        "archive:B",
    )
    o1, r1, v1 = oracle_and_runtime(s1, e1)
    require(o1["transition_class"] == "R-U1_ATTRIBUTION_REPLACEMENT", o1)
    require(v1["reference_end_to_end_pass"], v1)
    results["R-F1_VALID_ATTRIBUTION_REPLACEMENT"] = True

    # R-F2: alternative formation.
    s2 = base_state()
    e2 = event(
        "EV-ATTR-ALT",
        "author-attribution",
        "ADD_ALTERNATIVE",
        "Author-B",
        "COMPETING",
        "EVID-ATTR-COMPETING",
        "archive:competing",
    )
    o2, r2, v2 = oracle_and_runtime(s2, e2)
    require(o2["transition_class"] == "R-U2_ALTERNATIVE_FORMATION", o2)
    require(v2["reference_end_to_end_pass"], v2)
    require(
        len(
            next(
                x["assertions"]
                for x in o2["after_state"]["targets"]
                if x["target_property"] == "author-attribution"
            )
        ) == 2,
        o2,
    )
    results["R-F2_VALID_ALTERNATIVE_FORMATION"] = True

    # R-F3: same literal value, evidential status revision.
    s3 = base_state()
    e3 = event(
        "EV-EVID-STATUS",
        "evidence-status",
        "REVISE_STATUS",
        "EVIDENCE-1",
        "MEDIATED",
        "EVID-MEDIATION",
        "source:mediation",
    )
    o3, r3, v3 = oracle_and_runtime(s3, e3)
    require(o3["transition_class"] == "R-U3_EVIDENTIAL_STATUS_REVISION", o3)
    require(v3["reference_end_to_end_pass"], v3)
    results["R-F3_VALID_EVIDENTIAL_STATUS_REVISION"] = True

    # R-F4-R-F7: binding failures reject without Psi mutation.
    fault_map = {
        "R-F4_WRONG_OBJECT_REJECTED": {"type": "wrong_object"},
        "R-F5_WRONG_TARGET_REJECTED": {"type": "wrong_target"},
        "R-F6_WRONG_SOURCE_VERSION_REJECTED": {"type": "wrong_source_version"},
        "R-F7_MISSING_APPLICABILITY_REJECTED": {"type": "missing_applicability"},
    }
    for label, fault in fault_map.items():
        out = runtime_r.execute(base_state(), e1, fault=fault)
        require(not out["transition"]["applicable"], out["transition"])
        require(out["before_state"] == out["after_state"], out)
        require(not out["transition"]["changed_targets"], out["transition"])
        results[label] = True

    # R-F8: result/history can remain while current provenance surface is removed.
    o8 = oracle_r.apply_event(base_state(), e1)
    r8 = runtime_r.execute(base_state(), e1, fault={"type": "hide_current_provenance"})
    v8 = evaluator_r.evaluate(r8, o8, o8["state"], e1)
    require(v8["R4_POST_EVENT_RESULT"], v8)
    require(not v8["R6_PROVENANCE"], v8)
    require(v8["R7_TRANSITION_ATTRIBUTION"], v8)
    require(v8["R8_DELAYED_HISTORY"], v8)
    results["R-F8_PROVENANCE_MISSING_BUT_RESULT_INTACT"] = True

    # R-F9: valid target update plus unrelated assertion mutation.
    o9 = oracle_r.apply_event(base_state(), e1)
    r9 = runtime_r.execute(
        base_state(),
        e1,
        fault={"type": "collateral_mutation", "target_property": "source-status"},
    )
    v9 = evaluator_r.evaluate(r9, o9, o9["state"], e1)
    require(r9["transition"]["applicable"], r9["transition"])
    require("source-status" in r9["transition"]["collateral_targets"], r9["transition"])
    require(not v9["R5_SELECTIVE_UPDATE"], v9)
    require(r9["delayed_audit"]["event_id"] == e1["event_id"], r9["delayed_audit"])
    results["R-F9_COLLATERAL_ASSERTION_MUTATION_DETECTED"] = True

    # R-F10: post-state/provenance stay correct while delayed history is dropped.
    o10 = oracle_r.apply_event(base_state(), e1)
    r10 = runtime_r.execute(base_state(), e1, drop_history=True)
    v10 = evaluator_r.evaluate(r10, o10, o10["state"], e1)
    require(v10["R4_POST_EVENT_RESULT"], v10)
    require(v10["R5_SELECTIVE_UPDATE"], v10)
    require(v10["R6_PROVENANCE"], v10)
    require(v10["R7_TRANSITION_ATTRIBUTION"], v10)
    require(not v10["R8_DELAYED_HISTORY"], v10)
    results["R-F10_NO_HISTORY_SEPARATION"] = True

    # Strong comparators on the positive attribution case.
    current = runtime_r.current_reopen(r1)
    snaps = runtime_r.ordered_snapshots(r1)
    clog = runtime_r.change_log_no_justification(r1)

    ec = evaluator_r.evaluate_current_reopen(current, o1, o1["state"])
    es = evaluator_r.evaluate_snapshots(snaps, o1, o1["state"])
    el = evaluator_r.evaluate_change_log(clog, o1)

    require(ec["CURRENT_STATE_EXACT"], ec)
    require(ec["CURRENT_PROVENANCE_EXACT"], ec)
    require(es["PRE_STATE_EXACT"] and es["POST_STATE_EXACT"], es)
    require(es["STATE_DELTA_EXACT"], es)
    require(es["CURRENT_PROVENANCE_EXACT"], es)
    require(el["CHANGE_EVENT_TARGET_DIFF_EXACT"], el)
    require(not el["EVIDENCE_JUSTIFICATION_AVAILABLE"], el)
    require(not el["DELAYED_EVIDENCE_GROUNDED_AUDIT"], el)

    # R-F11: identical snapshots, different event semantics.
    e11a = copy.deepcopy(e1)
    e11b = copy.deepcopy(e1)
    e11b["event_class"] = "STATE_IMPORT"
    r11a = runtime_r.execute(base_state(), e11a)
    r11b = runtime_r.execute(base_state(), e11b)
    s11a = runtime_r.ordered_snapshots(r11a)
    s11b = runtime_r.ordered_snapshots(r11b)
    require(s11a == s11b, {"a": s11a, "b": s11b})
    require(
        r11a["transition"]["event_class"] != r11b["transition"]["event_class"],
        {"a": r11a["transition"], "b": r11b["transition"]},
    )
    results["R-F11_SNAPSHOT_NONIDENTIFIABILITY"] = True

    # R-F12: exact change log can be identical for distinct evidential justifications.
    e12a = copy.deepcopy(e1)
    e12b = copy.deepcopy(e1)
    e12b["evidence_id"] = "EVID-ATTR-B-OTHER"
    e12b["evidence_locator"] = "archive:other"
    r12a = runtime_r.execute(base_state(), e12a)
    r12b = runtime_r.execute(base_state(), e12b)
    l12a = runtime_r.change_log_no_justification(r12a)
    l12b = runtime_r.change_log_no_justification(r12b)
    require(l12a == l12b, {"a": l12a, "b": l12b})
    require(
        r12a["transition"]["evidence_id"] != r12b["transition"]["evidence_id"],
        {"a": r12a["transition"], "b": r12b["transition"]},
    )
    results["R-F12_CHANGE_LOG_NO_JUSTIFICATION"] = True

    # R-F13: claim/storage identity changes, Psi does not.
    e13 = event(
        "EV-BASIS-ONLY",
        "author-attribution",
        "REPLACE",
        "Author-A",
        "ACCEPTED",
        "EVID-BASIS-NEW",
        "archive:basis-new",
        agent="editor-new",
    )
    o13 = oracle_r.apply_event(base_state(), e13)
    r13 = runtime_r.execute(base_state(), e13)
    require(o13["applicable"] and r13["transition"]["applicable"], {"o": o13, "r": r13})
    require(not o13["substantive"], o13)
    require(not r13["transition"]["substantive"], r13["transition"])
    require(
        o13["transition_class"] == r13["transition"]["transition_class"]
        == "ADMISSIBLE_NULL_EVENT",
        {"o": o13, "r": r13["transition"]},
    )
    results["R-F13_BASIS_ONLY_NULL"] = True

    # R-F14: an admitted status reassessment that proposes the already-current status is null.
    e14 = event(
        "EV-NULL-STATUS",
        "evidence-status",
        "REVISE_STATUS",
        "EVIDENCE-1",
        "DIRECT",
        "EVID-NULL-STATUS",
        "source:null",
    )
    o14 = oracle_r.apply_event(base_state(), e14)
    r14 = runtime_r.execute(base_state(), e14)
    require(o14["applicable"] and r14["transition"]["applicable"], {"o": o14, "r": r14})
    require(not o14["substantive"], o14)
    require(not r14["transition"]["substantive"], r14["transition"])
    results["R-F14_NULL_REASSESSMENT"] = True

    print(json.dumps({
        "study": "MODULE_R_SYNTHETIC_GATE_V1",
        "all_controls_passed": all(results.values()),
        "controls": results,
        "positive_vectors": {
            "R-F1": v1,
            "R-F2": v2,
            "R-F3": v3,
        },
        "strong_comparators": {
            "B_CURRENT_REOPEN_R": ec,
            "B_ORDERED_SNAPSHOTS_R": es,
            "B_CHANGE_LOG_NO_JUSTIFICATION_R": el,
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
