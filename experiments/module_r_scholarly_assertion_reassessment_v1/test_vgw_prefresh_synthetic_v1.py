from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import evaluator_r
import oracle_r
import runtime_r
import vgw_contract_constants as C
import vgw_oracle
import vgw_runtime


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def I(value):
    return f"<{value}>"


def L(value, typed=False):
    raw = json.dumps(value, ensure_ascii=False)
    if typed:
        return raw + "^^<http://www.w3.org/2001/XMLSchema#string>"
    return raw


def triple(s, p, o):
    return f"{s} {I(p)} {o} ."


def add_artwork(lines, obj, fnums, prod=None, direct_vg=False,
                previous=0, unknown_assignment=False,
                responsible=True, two_productions=False,
                typed_f=False, blank_previous=False):
    lines.append(triple(I(obj), C.RDF_TYPE, I(C.E22_HUMAN_MADE_OBJECT)))
    for idx, fnum in enumerate(fnums, 1):
        ident = f"{obj}/identifier/f/{idx}"
        lines.append(triple(I(obj), C.P1_IDENTIFIED_BY, I(ident)))
        lines.append(triple(I(ident), C.RDF_TYPE, I(C.E42_IDENTIFIER)))
        lines.append(triple(I(ident), C.P2_HAS_TYPE, I(C.F_NUMBER_TYPE)))
        lines.append(triple(I(ident), C.P190_SYMBOLIC_CONTENT, L(fnum, typed=typed_f)))

    if prod is None:
        prod = f"{obj}/production"
    prod_term = prod if prod.startswith("_:") else I(prod)
    lines.append(triple(I(obj), C.P108I_WAS_PRODUCED_BY, prod_term))
    lines.append(triple(prod_term, C.RDF_TYPE, I(C.E12_PRODUCTION)))

    if two_productions:
        p2 = I(f"{obj}/production/2")
        lines.append(triple(I(obj), C.P108I_WAS_PRODUCED_BY, p2))
        lines.append(triple(p2, C.RDF_TYPE, I(C.E12_PRODUCTION)))

    if direct_vg:
        lines.append(
            triple(prod_term, C.P14_CARRIED_OUT_BY,
                   I("http://vocab.getty.edu/ulan/500115588"))
        )

    for idx in range(previous):
        assignment = (
            f"_:assignment_{idx+1}_{obj.rsplit('/', 1)[-1]}"
            if blank_previous
            else I(f"{obj}/assignment/{idx+1}")
        )
        assigned_prod = I(f"{obj}/assigned-production/{idx+1}")
        lines.append(triple(prod_term, C.P141I_WAS_ASSIGNED_BY, assignment))
        lines.append(triple(assignment, C.RDF_TYPE, I(C.E13_ATTRIBUTE_ASSIGNMENT)))
        lines.append(triple(assignment, C.P2_HAS_TYPE, I(C.PREVIOUS_ATTRIBUTION_TYPE)))
        lines.append(triple(assignment, C.P141_ASSIGNED, assigned_prod))
        lines.append(triple(assigned_prod, C.RDF_TYPE, I(C.E12_PRODUCTION)))
        lines.append(
            triple(assigned_prod, C.P14_CARRIED_OUT_BY,
                   I("https://data.rkd.nl/artists/32439"))
        )
        if responsible:
            lines.append(
                triple(
                    assignment,
                    C.P14_CARRIED_OUT_BY,
                    I(f"https://synthetic.example/curator/{idx+1}"),
                )
            )

    if unknown_assignment:
        assignment = I(f"{obj}/assignment/questionable")
        assigned_prod = I(f"{obj}/assigned-production/questionable")
        lines.append(triple(prod_term, C.P141I_WAS_ASSIGNED_BY, assignment))
        lines.append(triple(assignment, C.RDF_TYPE, I(C.E13_ATTRIBUTE_ASSIGNMENT)))
        lines.append(
            triple(
                assignment,
                C.P2_HAS_TYPE,
                I("https://synthetic.example/concept/questionable"),
            )
        )
        lines.append(triple(assignment, C.P141_ASSIGNED, assigned_prod))
        lines.append(triple(assigned_prod, C.RDF_TYPE, I(C.E12_PRODUCTION)))
        lines.append(
            triple(
                assigned_prod,
                C.P14_CARRIED_OUT_BY,
                I("http://vocab.getty.edu/ulan/500115588"),
            )
        )


def build_fixture():
    d = {slug: [] for slug in (
        C.BASELINE_SLUG,
        C.POST1970_SLUG,
        *C.CURRENT_PROVIDER_SLUGS,
    )}

    # Baseline F1001-F1006 plus duplicate F1008 and two extra boundary cases.
    for fnum in ["F1001", "F1002", "F1003", "F1004", "F1005", "F1006", "F1010", "F1011", "F1012", "F1013"]:
        add_artwork(
            d[C.BASELINE_SLUG],
            f"https://synthetic.example/baseline/{fnum}",
            [fnum],
            direct_vg=True,
            typed_f=(fnum == "F1002"),
        )

    add_artwork(
        d[C.BASELINE_SLUG],
        "https://synthetic.example/baseline/F1008/a",
        ["F1008"],
        direct_vg=True,
    )
    add_artwork(
        d[C.BASELINE_SLUG],
        "https://synthetic.example/baseline/F1008/b",
        ["F1008"],
        direct_vg=True,
    )

    # F1001 = natural null with a blank-node production.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1001",
        ["F1001"],
        prod="_:prod_f1001",
        direct_vg=True,
    )

    # F1002 = substantive previous-attribution R-U3.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1002",
        ["F1002"],
        previous=1,
    )

    # F1003 = direct + previous conflict.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1003",
        ["F1003"],
        direct_vg=True,
        previous=1,
    )

    # F1004 = machine status outside the registered vocabulary.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1004",
        ["F1004"],
        unknown_assignment=True,
    )

    # F1005 = duplicate current provider record.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1005/vgm",
        ["F1005"],
        direct_vg=True,
    )
    add_artwork(
        d["krollermuller_museum"],
        "https://synthetic.example/current/F1005/kmm",
        ["F1005"],
        direct_vg=True,
    )

    # F1006 = one current object with two F-number identifiers -> invalid record.
    add_artwork(
        d["rkd_collections"],
        "https://synthetic.example/current/F1006",
        ["F1006", "F9996"],
        direct_vg=True,
    )

    # F1008 = current exists, but baseline is duplicated.
    add_artwork(
        d["rkd_collections"],
        "https://synthetic.example/current/F1008",
        ["F1008"],
        direct_vg=True,
    )

    # F1009 = current object without a 1970 baseline.
    add_artwork(
        d["rkd_collections"],
        "https://synthetic.example/current/F1009",
        ["F1009"],
        direct_vg=True,
    )

    # F1011 = two production activities -> strict ineligible.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1011",
        ["F1011"],
        direct_vg=True,
        two_productions=True,
    )

    # F1012 = multiple previous-attribution assignments -> strict ineligible.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1012",
        ["F1012"],
        previous=2,
    )

    # F1013 = qualifying reassessment encoded only as a blank node -> not addressable.
    add_artwork(
        d["van_gogh_museum"],
        "https://synthetic.example/current/F1013",
        ["F1013"],
        previous=1,
        blank_previous=True,
    )

    # Post-1970 role exclusion is counted but never used as 1970 baseline.
    add_artwork(
        d[C.POST1970_SLUG],
        "https://synthetic.example/post1970/F2001",
        ["F2001"],
        direct_vg=True,
    )

    return {
        slug: ("\n".join(lines) + "\n").encode("utf-8")
        for slug, lines in d.items()
    }


def normalized_extraction(result):
    out = copy.deepcopy(result)
    out.pop("engine", None)
    return out


def by_f(cases):
    return {x["f_number"]: x for x in cases}


def add_collateral_guard(state):
    state = copy.deepcopy(state)
    state["registered_targets"].append("synthetic-unrelated-status")
    state["assertions"]["synthetic-unrelated-status"] = [{
        "claim_id": "GUARD::" + state["object_id"],
        "object_id": state["object_id"],
        "target_property": "synthetic-unrelated-status",
        "value": "GUARD",
        "status": "STABLE",
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "source_repository": state["source_repository"],
        "source_version": state["source_version"],
        "source_id": "SYNTHETIC-GUARD",
        "source_locator": "synthetic:guard",
        "responsible_agent": "synthetic",
    }]
    return state


def main():
    fixture = build_fixture()

    oracle_extract = vgw_oracle.extract_population(
        fixture, C.SYNTHETIC_SOURCE_VERSION
    )
    runtime_extract = vgw_runtime.extract_population(
        fixture, C.SYNTHETIC_SOURCE_VERSION
    )

    require(
        normalized_extraction(oracle_extract)
        == normalized_extraction(runtime_extract),
        {
            "oracle": normalized_extraction(oracle_extract),
            "runtime": normalized_extraction(runtime_extract),
        },
    )

    cases = by_f(oracle_extract["cases"])
    expected = {
        "F1001": "ADMISSIBLE_NULL_EVENT",
        "F1002": "SUBSTANTIVE_CANDIDATE",
        "F1003": "CONFLICTING_CURRENT_ATTRIBUTION_ENCODING",
        "F1004": "UNREGISTERED_CURRENT_ATTRIBUTION_STATUS",
        "F1005": "MULTIPLE_CURRENT_PROVIDER_OBJECTS",
        "F1006": "NO_CURRENT_PROVIDER_OBJECT",
        "F1008": "AMBIGUOUS_1970_BASELINE",
        "F1009": "NO_1970_BASELINE",
        "F1010": "NO_CURRENT_PROVIDER_OBJECT",
        "F1011": "INVALID_PRODUCTION_CARDINALITY",
        "F1012": "MULTIPLE_PREVIOUS_ATTRIBUTION_ASSIGNMENTS",
        "F1013": "NON_ADDRESSABLE_REASSESSMENT_EVENT",
    }
    for fnum, disposition in expected.items():
        require(cases[fnum]["disposition"] == disposition, {
            "f_number": fnum,
            "expected": disposition,
            "actual": cases[fnum],
        })

    require(len(oracle_extract["invalid_records"]) == 1, oracle_extract["invalid_records"])
    require(
        oracle_extract["invalid_records"][0]["disposition"]
        == "INVALID_F_NUMBER_CARDINALITY",
        oracle_extract["invalid_records"],
    )
    require(
        [x["f_number"] for x in oracle_extract["post1970_role_exclusions"]]
        == ["F2001"],
        oracle_extract["post1970_role_exclusions"],
    )

    # Null: current provider source changes, task-level Psi does not.
    o_null = cases["F1001"]
    r_null = by_f(runtime_extract["cases"])["F1001"]
    ot_null = oracle_r.apply_event(o_null["state"], o_null["event"])
    rt_null = runtime_r.execute(r_null["state"], r_null["event"])
    ev_null = evaluator_r.evaluate(
        rt_null, ot_null, ot_null["state"], o_null["event"]
    )
    require(ot_null["transition_class"] == "ADMISSIBLE_NULL_EVENT", ot_null)
    require(not ot_null["substantive"], ot_null)
    require(ev_null["reference_end_to_end_pass"], ev_null)

    # Substantive: ATTRIBUTED -> PREVIOUSLY_ATTRIBUTED.
    o_pos = cases["F1002"]
    r_pos = by_f(runtime_extract["cases"])["F1002"]
    ot_pos = oracle_r.apply_event(o_pos["state"], o_pos["event"])
    rt_pos = runtime_r.execute(r_pos["state"], r_pos["event"])
    ev_pos = evaluator_r.evaluate(
        rt_pos, ot_pos, ot_pos["state"], o_pos["event"]
    )
    require(
        ot_pos["transition_class"] == "R-U3_EVIDENTIAL_STATUS_REVISION",
        ot_pos,
    )
    require(ot_pos["substantive"], ot_pos)
    require(ev_pos["reference_end_to_end_pass"], ev_pos)

    # Strong comparator budgets remain unchanged.
    current = runtime_r.current_reopen(rt_pos)
    snaps = runtime_r.ordered_snapshots(rt_pos)
    clog = runtime_r.change_log_no_justification(rt_pos)

    ec = evaluator_r.evaluate_current_reopen(current, ot_pos, ot_pos["state"])
    es = evaluator_r.evaluate_snapshots(snaps, ot_pos, ot_pos["state"])
    el = evaluator_r.evaluate_change_log(clog, ot_pos)

    require(ec["CURRENT_STATE_EXACT"] and ec["CURRENT_PROVENANCE_EXACT"], ec)
    require(not ec["TRANSITION_ATTRIBUTION_EXACT"], ec)
    require(not ec["DELAYED_HISTORY_EXACT"], ec)
    require(
        es["PRE_STATE_EXACT"]
        and es["POST_STATE_EXACT"]
        and es["STATE_DELTA_EXACT"]
        and es["CURRENT_PROVENANCE_EXACT"],
        es,
    )
    require(not es["TRANSITION_ATTRIBUTION_EXACT"], es)
    require(not es["DELAYED_HISTORY_EXACT"], es)
    require(el["CHANGE_EVENT_TARGET_DIFF_EXACT"], el)
    require(not el["EVIDENCE_JUSTIFICATION_AVAILABLE"], el)
    require(not el["DELAYED_EVIDENCE_GROUNDED_AUDIT"], el)

    # Binding failures on the VGW-shaped substantive case.
    for label, fault in {
        "wrong_object": {"type": "wrong_object"},
        "wrong_source_version": {"type": "wrong_source_version"},
        "missing_applicability": {"type": "missing_applicability"},
    }.items():
        out = runtime_r.execute(r_pos["state"], r_pos["event"], fault=fault)
        require(not out["transition"]["applicable"], {label: out["transition"]})
        require(out["before_state"] == out["after_state"], {label: out})

    # Provenance and history remain independently removable.
    no_prov = runtime_r.execute(
        r_pos["state"], r_pos["event"], fault={"type": "hide_current_provenance"}
    )
    ev_no_prov = evaluator_r.evaluate(
        no_prov, ot_pos, ot_pos["state"], o_pos["event"]
    )
    require(ev_no_prov["R4_POST_EVENT_RESULT"], ev_no_prov)
    require(not ev_no_prov["R6_PROVENANCE"], ev_no_prov)
    require(ev_no_prov["R8_DELAYED_HISTORY"], ev_no_prov)

    no_hist = runtime_r.execute(r_pos["state"], r_pos["event"], drop_history=True)
    ev_no_hist = evaluator_r.evaluate(
        no_hist, ot_pos, ot_pos["state"], o_pos["event"]
    )
    require(ev_no_hist["R4_POST_EVENT_RESULT"], ev_no_hist)
    require(ev_no_hist["R6_PROVENANCE"], ev_no_hist)
    require(not ev_no_hist["R8_DELAYED_HISTORY"], ev_no_hist)

    # Collateral selectivity with a deliberately unrelated synthetic guard.
    guard_state = add_collateral_guard(r_pos["state"])
    guard_oracle_state = add_collateral_guard(o_pos["state"])
    guard_oracle_transition = oracle_r.apply_event(
        guard_oracle_state, o_pos["event"]
    )
    collateral = runtime_r.execute(
        guard_state,
        r_pos["event"],
        fault={
            "type": "collateral_mutation",
            "target_property": "synthetic-unrelated-status",
        },
    )
    collateral_eval = evaluator_r.evaluate(
        collateral,
        guard_oracle_transition,
        guard_oracle_transition["state"],
        o_pos["event"],
    )
    require(
        "synthetic-unrelated-status"
        in collateral["transition"]["collateral_targets"],
        collateral["transition"],
    )
    require(not collateral_eval["R5_SELECTIVE_UPDATE"], collateral_eval)

    result = {
        "study": "MODULE_R_VGW_PREFRESH_SYNTHETIC_GATE_V1",
        "provider_distribution_opened": False,
        "oracle_runtime_extraction_exact": True,
        "expected_dispositions": expected,
        "invalid_record_count": len(oracle_extract["invalid_records"]),
        "post1970_role_exclusion_count": len(
            oracle_extract["post1970_role_exclusions"]
        ),
        "null_case": {
            "f_number": "F1001",
            "transition_class": ot_null["transition_class"],
            "R1_R8_pass": ev_null["reference_end_to_end_pass"],
        },
        "substantive_case": {
            "f_number": "F1002",
            "transition_class": ot_pos["transition_class"],
            "R1_R8_pass": ev_pos["reference_end_to_end_pass"],
        },
        "strong_comparators": {
            "B_CURRENT_REOPEN_R": ec,
            "B_ORDERED_SNAPSHOTS_R": es,
            "B_CHANGE_LOG_NO_JUSTIFICATION_R": el,
        },
        "fault_controls": {
            "wrong_object_rejected": True,
            "wrong_source_version_rejected": True,
            "missing_applicability_rejected": True,
            "provenance_loss_isolated": True,
            "history_loss_isolated": True,
            "collateral_mutation_detected": True,
        },
        "overall": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
