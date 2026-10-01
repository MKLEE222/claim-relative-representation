from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_DIR = HERE.parent / "module_r_scholarly_assertion_reassessment_v1"
DEEP_DIR = HERE.parent / "deepening_v1"
for p in (HERE, R_DIR, DEEP_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import qualified_oracle_v1 as qo
import qualified_runtime_v1 as qr
import oracle_r
import run_historical_exposed as hist
import test_reassessment_contract_v1 as synth


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def strip_operation(event):
    out = copy.deepcopy(event)
    out.pop("operation", None)
    return out


def normalized(result):
    out = copy.deepcopy(result)
    out.pop("engine", None)
    return out


def source_relations():
    rows = hist.load_source_rows()
    return {x["entry_id"]: x for x in rows}


def synthetic_fixture(label, state, old_event, relation, expected_generator):
    event = strip_operation(old_event)
    event["evidence_relation"] = relation
    return {
        "label": label,
        "state": state,
        "event": event,
        "old_event": old_event,
        "evidence_relation": relation,
        "expected_generator": expected_generator,
        "source_grounding": "SYNTHETIC_DECLARED_RELATION",
    }


def synthetic_fixtures():
    rows = []

    rows.append(synthetic_fixture(
        "SYNTH_REPLACE",
        synth.base_state(),
        synth.event(
            "QG-S-1",
            "author-attribution",
            "REPLACE",
            "Author-B",
            "ACCEPTED",
            "EVID-QG-S1",
            "qualified:s1",
        ),
        "REPLACES_PRIOR",
        "REPLACE",
    ))

    rows.append(synthetic_fixture(
        "SYNTH_ADD_ALTERNATIVE",
        synth.base_state(),
        synth.event(
            "QG-S-2",
            "author-attribution",
            "ADD_ALTERNATIVE",
            "Author-B",
            "COMPETING",
            "EVID-QG-S2",
            "qualified:s2",
        ),
        "CONTRADICTS_PRIOR",
        "ADD_ALTERNATIVE",
    ))

    rows.append(synthetic_fixture(
        "SYNTH_REVISE_STATUS",
        synth.base_state(),
        synth.event(
            "QG-S-3",
            "evidence-status",
            "REVISE_STATUS",
            "EVIDENCE-1",
            "MEDIATED",
            "EVID-QG-S3",
            "qualified:s3",
        ),
        "NARROWS_PRIOR",
        "REVISE_STATUS",
    ))

    rows.append(synthetic_fixture(
        "SYNTH_BASIS_RECORD",
        synth.base_state(),
        synth.event(
            "QG-S-4",
            "author-attribution",
            "REPLACE",
            "Author-A",
            "ACCEPTED",
            "EVID-QG-S4",
            "qualified:s4",
            agent="editor-new",
        ),
        "CORROBORATES_PRIOR",
        "RECORD_EVIDENCE",
    ))

    rows.append(synthetic_fixture(
        "SYNTH_STATUS_RECORD",
        synth.base_state(),
        synth.event(
            "QG-S-5",
            "evidence-status",
            "REVISE_STATUS",
            "EVIDENCE-1",
            "DIRECT",
            "EVID-QG-S5",
            "qualified:s5",
        ),
        "CORROBORATES_PRIOR",
        "RECORD_EVIDENCE",
    ))

    return rows


def historical_fixtures():
    by_source = source_relations()
    expected = {
        "YC1920E-0022": "REVISE_STATUS",
        "YC1920E-0023": "RECORD_EVIDENCE",
        "YC1920E-0024": "ADD_ALTERNATIVE",
        "YC1920E-0030": "RECORD_EVIDENCE",
        "YC1920E-0049": "RESOLVE",
    }
    rows = []
    for item in hist.load_panel():
        source = by_source[item["entry_id"]]
        require(
            source["contrast_type"] == item["expected_contrast_type"],
            {"item": item, "source": source},
        )
        require(
            source["evidence_authority"] == "OBJECT_VERIFIED",
            source,
        )
        old_event = hist.make_event(item)
        event = strip_operation(old_event)
        event["evidence_relation"] = source["contrast_type"]
        rows.append({
            "label": "HIST_" + item["entry_id"],
            "entry_id": item["entry_id"],
            "state": hist.make_state(item),
            "event": event,
            "old_event": old_event,
            "evidence_relation": source["contrast_type"],
            "expected_generator": expected[item["entry_id"]],
            "source_grounding": {
                "contrast_type": source["contrast_type"],
                "final_diachronic_relation": source[
                    "final_diachronic_relation"
                ],
                "evidence_authority": source["evidence_authority"],
                "notes": source["notes"],
            },
        })
    return rows


def audit_fixture(fx):
    o = qo.apply(fx["state"], fx["event"])
    r = qr.execute(fx["state"], fx["event"])

    require(normalized(o) == normalized(r), {
        "label": fx["label"],
        "oracle": normalized(o),
        "runtime": normalized(r),
    })
    require(o["qualified"] and r["qualified"], {
        "label": fx["label"], "oracle": o, "runtime": r
    })
    require(o["generator"] == fx["expected_generator"], {
        "label": fx["label"],
        "expected": fx["expected_generator"],
        "actual": o["generator"],
    })
    require("operation" not in fx["event"], fx["event"])

    old = oracle_r.apply_event(fx["state"], fx["old_event"])
    require(o["after_psi"] == old["after_state"], {
        "label": fx["label"],
        "qualified_after": o["after_psi"],
        "old_after": old["after_state"],
        "qualified_generator": o["generator"],
        "old_operation": fx["old_event"]["operation"],
    })

    if fx["expected_generator"] == "RECORD_EVIDENCE":
        require(o["assertion_identity"], o)
        require(o["before_psi"] == o["after_psi"], o)
        require(o["history_nonidentity"], o)
        require(o["before_xi"] != o["after_xi"], o)
        require(
            o["transition_class"]
            == "ASSERTION_IDENTITY_HISTORY_NONIDENTITY",
            o,
        )
    else:
        require(not o["assertion_identity"], o)

    return {
        "label": fx["label"],
        "evidence_relation": fx["evidence_relation"],
        "selected_generator": o["generator"],
        "old_operation": fx["old_event"]["operation"],
        "old_transition_class": old["transition_class"],
        "qualified_transition_class": o["transition_class"],
        "assertion_identity": o["assertion_identity"],
        "history_nonidentity": o["history_nonidentity"],
        "source_grounding": fx["source_grounding"],
        "operation_absent_from_input": "operation" not in fx["event"],
        "old_post_psi_preserved": o["after_psi"] == old["after_state"],
        "oracle_runtime_exact": normalized(o) == normalized(r),
    }


def rejection_controls():
    base = synthetic_fixtures()[0]
    state = base["state"]
    event = base["event"]

    variants = {}

    x = copy.deepcopy(event)
    x["object_id"] = "FOREIGN_OBJECT"
    variants["WRONG_OBJECT"] = x

    x = copy.deepcopy(event)
    x["target_property"] = "foreign-target"
    variants["WRONG_TARGET"] = x

    x = copy.deepcopy(event)
    x["source_version"] = "FOREIGN_VERSION"
    variants["WRONG_SOURCE_VERSION"] = x

    x = copy.deepcopy(event)
    x["applicability_class"] = None
    variants["MISSING_APPLICABILITY"] = x

    x = copy.deepcopy(event)
    x["evidence_relation"] = "INVENTED_RELATION"
    variants["UNREGISTERED_RELATION"] = x

    x = copy.deepcopy(event)
    x["evidence_relation"] = "NO_VERIFIED_CONTRAST"
    variants["NO_VERIFIED_CONTRAST"] = x

    rows = []
    for label, ev in variants.items():
        o = qo.apply(state, ev)
        r = qr.execute(state, ev)
        require(normalized(o) == normalized(r), {
            "label": label, "oracle": o, "runtime": r
        })
        require(not o["qualified"], {"label": label, "result": o})
        require(o["generator"] is None, o)
        require(o["before_psi"] == o["after_psi"], o)
        require(o["before_xi"] == o["after_xi"], o)
        require(o["state"] == state, {"label": label, "result": o})
        rows.append({
            "label": label,
            "rejection_reason": o["rejection_reason"],
            "psi_unchanged": True,
            "xi_unchanged": True,
            "oracle_runtime_exact": True,
        })
    return rows


def compose(engine):
    s0 = synth.base_state()

    e1 = strip_operation(synth.event(
        "QG-COMP-1",
        "author-attribution",
        "ADD_ALTERNATIVE",
        "Author-B",
        "COMPETING",
        "EVID-QG-C1",
        "qualified:compose:1",
    ))
    e1["evidence_relation"] = "CONTRADICTS_PRIOR"

    e2 = strip_operation(synth.event(
        "QG-COMP-2",
        "author-attribution",
        "RESOLVE",
        "Author-B",
        "ACCEPTED",
        "EVID-QG-C2",
        "qualified:compose:2",
    ))
    e2["evidence_relation"] = "REPLACES_PRIOR"

    first_forward = engine(s0, e1)
    require(first_forward["qualified"], first_forward)
    second_forward = engine(first_forward["state"], e2)
    require(second_forward["qualified"], second_forward)

    first_reverse = engine(s0, e2)
    require(first_reverse["qualified"], first_reverse)
    second_reverse = engine(first_reverse["state"], e1)
    require(second_reverse["qualified"], second_reverse)

    return {
        "forward_generators": [
            first_forward["generator"],
            second_forward["generator"],
        ],
        "reverse_generators": [
            first_reverse["generator"],
            second_reverse["generator"],
        ],
        "e2_generator_at_s0": first_reverse["generator"],
        "e2_generator_after_e1": second_forward["generator"],
        "state_dependent_generator_selection": (
            first_reverse["generator"] != second_forward["generator"]
        ),
        "forward_final_psi": second_forward["after_psi"],
        "reverse_final_psi": second_reverse["after_psi"],
        "forward_final_xi": second_forward["after_xi"],
        "reverse_final_xi": second_reverse["after_xi"],
        "final_psi_different": (
            second_forward["after_psi"] != second_reverse["after_psi"]
        ),
        "final_full_state_different": (
            second_forward["state"] != second_reverse["state"]
        ),
        "non_commutative": all([
            [
                first_forward["generator"],
                second_forward["generator"],
            ] != [
                first_reverse["generator"],
                second_reverse["generator"],
            ],
            second_forward["state"] != second_reverse["state"],
        ]),
    }


def factorization_probe():
    s0 = synth.base_state()

    base_event = strip_operation(synth.event(
        "QG-FACTOR",
        "author-attribution",
        "REPLACE",
        "Author-B",
        "ACCEPTED",
        "EVID-QG-FACTOR",
        "qualified:factor",
    ))

    contradict = copy.deepcopy(base_event)
    contradict["evidence_relation"] = "CONTRADICTS_PRIOR"

    replace = copy.deepcopy(base_event)
    replace["evidence_relation"] = "REPLACES_PRIOR"

    g_contradict_o = qo.qualify(s0, contradict)["generator"]
    g_replace_o = qo.qualify(s0, replace)["generator"]
    g_contradict_r = qr.qualify(s0, contradict)["generator"]
    g_replace_r = qr.qualify(s0, replace)["generator"]

    require(
        [g_contradict_o, g_replace_o]
        == [g_contradict_r, g_replace_r],
        {
            "oracle": [g_contradict_o, g_replace_o],
            "runtime": [g_contradict_r, g_replace_r],
        },
    )
    require(
        [g_contradict_o, g_replace_o]
        == ["ADD_ALTERNATIVE", "REPLACE"],
        {
            "contradict": g_contradict_o,
            "replace": g_replace_o,
        },
    )

    alt_event = copy.deepcopy(contradict)
    alt_event["event_id"] = "QG-FACTOR-ALT"
    alt_event["status"] = "COMPETING"
    s1 = qo.apply(s0, alt_event)["state"]

    replace_after_alt = copy.deepcopy(replace)
    replace_after_alt["event_id"] = "QG-FACTOR-RESOLVE"
    g_replace_after_alt_o = qo.qualify(
        s1, replace_after_alt
    )["generator"]
    g_replace_after_alt_r = qr.qualify(
        s1, replace_after_alt
    )["generator"]
    require(
        g_replace_after_alt_o == g_replace_after_alt_r == "RESOLVE",
        {
            "oracle": g_replace_after_alt_o,
            "runtime": g_replace_after_alt_r,
        },
    )

    return {
        "fixed_state_same_proposal": {
            "CONTRADICTS_PRIOR": g_contradict_o,
            "REPLACES_PRIOR": g_replace_o,
        },
        "relation_sensitivity": g_contradict_o != g_replace_o,
        "fixed_relation_REPLACES_PRIOR": {
            "singleton_state": g_replace_o,
            "alternative_state": g_replace_after_alt_o,
        },
        "state_sensitivity": g_replace_o != g_replace_after_alt_o,
        "generator_is_joint_function_of_state_and_relation": all([
            g_contradict_o != g_replace_o,
            g_replace_o != g_replace_after_alt_o,
        ]),
    }


def main():
    fixtures = synthetic_fixtures() + historical_fixtures()
    rows = [audit_fixture(x) for x in fixtures]

    require(len(rows) == 10, rows)
    require(all(x["oracle_runtime_exact"] for x in rows), rows)
    require(all(x["operation_absent_from_input"] for x in rows), rows)
    require(all(x["old_post_psi_preserved"] for x in rows), rows)

    hist_rows = [x for x in rows if x["label"].startswith("HIST_")]
    synth_rows = [x for x in rows if x["label"].startswith("SYNTH_")]
    require(len(hist_rows) == 5 and len(synth_rows) == 5, rows)

    reject = rejection_controls()

    factorization = factorization_probe()

    compose_o = compose(qo.apply)
    compose_r = compose(qr.execute)
    require(compose_o == compose_r, {
        "oracle": compose_o, "runtime": compose_r
    })
    require(compose_o["state_dependent_generator_selection"], compose_o)
    require(compose_o["non_commutative"], compose_o)
    require(
        compose_o["forward_generators"]
        == ["ADD_ALTERNATIVE", "RESOLVE"],
        compose_o,
    )
    require(
        compose_o["reverse_generators"]
        == ["REPLACE", "REVISE_STATUS"],
        compose_o,
    )

    record_rows = [
        x for x in rows
        if x["selected_generator"] == "RECORD_EVIDENCE"
    ]
    require(len(record_rows) == 4, record_rows)
    require(all(
        x["assertion_identity"] and x["history_nonidentity"]
        for x in record_rows
    ), record_rows)

    result = {
        "study": "QUALIFIED_SCHOLARLY_GENERATOR_REPAIR_V1",
        "data_status": "SYNTHETIC_PLUS_PREEXISTING_EXPOSED_ONLY",
        "disposition": "QUALIFIED_GENERATOR_REPAIR_PASS",
        "summary": {
            "historical_recovery": "5/5",
            "synthetic_recovery": "5/5",
            "oracle_runtime_exact": "10/10",
            "operation_absent_from_input": "10/10",
            "old_post_psi_preserved": "10/10",
            "record_evidence_cases": "4/4",
            "false_positive_controls_rejected": f"{len(reject)}/{len(reject)}",
            "state_dependent_generator_selection": True,
            "non_commutative_composition": True,
            "relation_sensitivity": factorization["relation_sensitivity"],
            "state_sensitivity": factorization["state_sensitivity"],
            "joint_state_relation_qualification": factorization[
                "generator_is_joint_function_of_state_and_relation"
            ],
        },
        "recovery_rows": rows,
        "rejection_controls": reject,
        "factorization_probe": factorization,
        "composition": compose_o,
        "claim_ceiling": [
            "Generator selection is established only for the registered source-grounded relation vocabulary and audited states.",
            "Historical relation labels come from the pre-existing R3 earlier/later contrast audit, not from held-out Module-R operations.",
            "No claim is made that evidence relations are automatically extractable from arbitrary natural language.",
            "RECORD_EVIDENCE is assertion-state identity but full scholarly-state nonidentity.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "qualified_generator_repair_results_v1.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "disposition": result["disposition"],
        "summary": result["summary"],
        "recovery_compact": [
            {
                "label": x["label"],
                "relation": x["evidence_relation"],
                "generator": x["selected_generator"],
                "old_operation": x["old_operation"],
                "assertion_identity": x["assertion_identity"],
                "history_nonidentity": x["history_nonidentity"],
            }
            for x in rows
        ],
        "rejection_controls": reject,
        "factorization_probe": factorization,
        "composition": {
            "forward_generators": compose_o["forward_generators"],
            "reverse_generators": compose_o["reverse_generators"],
            "e2_generator_at_s0": compose_o["e2_generator_at_s0"],
            "e2_generator_after_e1": compose_o[
                "e2_generator_after_e1"
            ],
            "state_dependent_generator_selection": compose_o[
                "state_dependent_generator_selection"
            ],
            "final_psi_different": compose_o["final_psi_different"],
            "final_full_state_different": compose_o[
                "final_full_state_different"
            ],
            "non_commutative": compose_o["non_commutative"],
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
