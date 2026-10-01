from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
QG_DIR = HERE.parent / "qualified_scholarly_generators_v1"
for p in (HERE, QG_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import target_bound_oracle_v1 as tbo
import target_bound_runtime_v1 as tbr
import qualified_oracle_v1 as qgo
import qualified_runtime_v1 as qgr

CLAIMS = ROOT / "data" / "yule_cordier_claim_events.csv"
TRACES = ROOT / "data" / "paper_money_archival_stance_traces_v1.csv"
ONTOLOGY = (
    ROOT / "experiments" / "deepening_v1"
    / "R3_RELATION_ONTOLOGY_AMENDMENT_v2.md"
)


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def one(rows, key, value):
    found = [x for x in rows if x.get(key) == value]
    require(len(found) == 1, {
        "key": key,
        "value": value,
        "count": len(found),
        "rows": found,
    })
    return found[0]


def norm(result):
    out = copy.deepcopy(result)
    out.pop("engine", None)
    return out


def source_audit():
    claims = read_csv(CLAIMS)
    traces = read_csv(TRACES)
    pm = {x: one(claims, "event_id", x) for x in ("PM01", "PM02", "PM03")}
    pt = {x: one(traces, "trace_id", x) for x in ("PMT01", "PMT02", "PMT03")}

    require(all(
        pm[x]["verification_status"].strip().lower() == "page image verified"
        for x in pm
    ), pm)
    require(all(
        pt[x]["verification_status"] == "PAGE_VERIFIED"
        for x in pt
    ), pt)

    require(pm["PM02"]["operation"] == "adds challenge", pm["PM02"])
    require(pm["PM03"]["operation"] == "corrects prior note", pm["PM03"])
    require(
        "contradicts PM02" in pm["PM03"]["evidence_relation"],
        pm["PM03"],
    )
    require(
        pt["PMT01"]["trace_type"] == "ST_CRITICISM",
        pt["PMT01"],
    )
    require(
        pt["PMT01"]["target"] == "Marco Polo material identification",
        pt["PMT01"],
    )
    require(
        pt["PMT02"]["trace_type"] == "ST_PRIOR_CRITIC_CORRECTION",
        pt["PMT02"],
    )
    require(
        pt["PMT02"]["target"] == "Bretschneider's prior statement",
        pt["PMT02"],
    )
    require(
        pt["PMT03"]["trace_type"] == "ST_ENDORSEMENT",
        pt["PMT03"],
    )
    require(
        pt["PMT03"]["target"] == "Marco Polo material identification",
        pt["PMT03"],
    )

    ontology_text = ONTOLOGY.read_text(encoding="utf-8")
    require(
        "CORRECTION_OF_PRIOR_CRITICISM" in ontology_text,
        "registered relation missing from frozen ontology",
    )

    return {
        "claims": pm,
        "traces": pt,
        "ontology_contains_prior_critic_correction": True,
    }


def initial_state():
    return {
        "object_id": "YC-PAPER-MONEY",
        "source_repository": "YULE_CORDIER_VERIFIED_ARCHIVE",
        "source_version": "PM01_PM02_PM03_PAGE_VERIFIED_SEQUENCE_V1",
        "registered_targets": ["paper-money-material-identification"],
        "assertions": {
            "paper-money-material-identification": [{
                "claim_id": "PM01",
                "object_id": "YC-PAPER-MONEY",
                "target_property": "paper-money-material-identification",
                "value": "MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE",
                "status": "NARRATIVE_ASSERTED",
                "source_id": "PM01",
                "source_locator": "1903 vol. 1 printed p. 423",
                "responsible_agent": "Marco Polo/Rustichello/Yule translation",
            }]
        },
        "evidence_ledger": [],
        "event_ledger": [],
        "transition_ledger": [],
    }


def common_event(event_id, evidence_id, locator, agent, relation, target_claim, new_claim, value, status):
    return {
        "event_id": event_id,
        "event_class": "SCHOLARLY_REASSESSMENT",
        "object_id": "YC-PAPER-MONEY",
        "target_property": "paper-money-material-identification",
        "source_repository": "YULE_CORDIER_VERIFIED_ARCHIVE",
        "source_version": "PM01_PM02_PM03_PAGE_VERIFIED_SEQUENCE_V1",
        "evidence_id": evidence_id,
        "evidence_locator": locator,
        "responsible_agent": agent,
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "evidence_relation": relation,
        "relation_target_claim_id": target_claim,
        "new_claim_id": new_claim,
        "value": value,
        "status": status,
    }


def pm02_event():
    return common_event(
        "PM02_EVENT",
        "PM02",
        "1903 vol.1 p430 / scan732",
        "Emil Bretschneider as transmitted by Henri Cordier",
        "CONTRADICTS_PRIOR",
        "PM01",
        "PM02",
        "MULBERRY_BARK_IDENTIFICATION_MISTAKEN",
        "ASSERTED",
    )


def pm03_event():
    return common_event(
        "PM03_EVENT",
        "PM03",
        "1920 pp70-72 / scan84-86",
        "Berthold Laufer as transmitted by Henri Cordier",
        "CORRECTION_OF_PRIOR_CRITICISM",
        "PM02",
        "PM03",
        "MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE",
        "RESTORED_AS_CORRECT",
    )


def exact_pair(state, event, oracle_fn, runtime_fn):
    o = oracle_fn(state, event)
    r = runtime_fn(state, event)
    require(norm(o) == norm(r), {
        "oracle": norm(o),
        "runtime": norm(r),
    })
    return o


def live_claim_ids(state):
    rows = state["assertions"]["paper-money-material-identification"]
    return sorted(x["claim_id"] for x in rows)


def v1_diagnostic(s0, e2):
    projected = copy.deepcopy(e2)
    projected.pop("relation_target_claim_id", None)
    projected["evidence_relation"] = "REPLACES_PRIOR"

    o = qgo.apply(s0, projected)
    r = qgr.execute(s0, projected)
    require(norm(o) == norm(r), {
        "oracle": norm(o), "runtime": norm(r)
    })
    return {
        "projection": (
            "CORRECTION_OF_PRIOR_CRITICISM -> REPLACES_PRIOR"
        ),
        "qualified": o["qualified"],
        "generator": o["generator"],
        "rejection_reason": o["rejection_reason"],
        "false_generator_availability_if_target_identity_omitted": (
            o["qualified"]
        ),
    }


def main():
    source = source_audit()
    s0 = initial_state()
    e1 = pm02_event()
    e2 = pm03_event()

    require("operation" not in e1 and "operation" not in e2, {
        "e1": e1, "e2": e2
    })

    # Forward natural history.
    step1 = exact_pair(s0, e1, tbo.apply, tbr.execute)
    require(step1["qualified"], step1)
    require(step1["generator"] == "ADD_ALTERNATIVE", step1)
    s1 = step1["state"]
    require(live_claim_ids(s1) == ["PM01", "PM02"], s1)

    step2 = exact_pair(s1, e2, tbo.apply, tbr.execute)
    require(step2["qualified"], step2)
    require(step2["generator"] == "RESOLVE", step2)
    s2 = step2["state"]
    require(live_claim_ids(s2) == ["PM03"], s2)

    transitions = s2["transition_ledger"]
    require(len(transitions) == 2, transitions)
    require(
        [
            (
                x["generated_claim_id"],
                x["evidence_relation"],
                x["relation_target_claim_id"],
                x["qualified_generator"],
            )
            for x in transitions
        ]
        == [
            (
                "PM02",
                "CONTRADICTS_PRIOR",
                "PM01",
                "ADD_ALTERNATIVE",
            ),
            (
                "PM03",
                "CORRECTION_OF_PRIOR_CRITICISM",
                "PM02",
                "RESOLVE",
            ),
        ],
        transitions,
    )

    # Reverse order: PM03 cannot precede PM02 because its relation target is absent.
    reverse = exact_pair(s0, e2, tbo.apply, tbr.execute)
    require(not reverse["qualified"], reverse)
    require(
        reverse["rejection_reason"] == "RELATION_TARGET_NOT_LIVE",
        reverse,
    )
    require(reverse["before_psi"] == reverse["after_psi"], reverse)
    require(reverse["before_xi"] == reverse["after_xi"], reverse)
    require(reverse["state"] == s0, reverse)

    # Same visible assertions, but no retained transition history.
    s1_psi_only = copy.deepcopy(s1)
    s1_psi_only["evidence_ledger"] = []
    s1_psi_only["event_ledger"] = []
    s1_psi_only["transition_ledger"] = []
    require(tbo.psi(s1) == tbo.psi(s1_psi_only), {
        "full": tbo.psi(s1),
        "ablated": tbo.psi(s1_psi_only),
    })
    require(tbo.xi(s1) != tbo.xi(s1_psi_only), {
        "full": tbo.xi(s1),
        "ablated": tbo.xi(s1_psi_only),
    })

    history_ablated = exact_pair(
        s1_psi_only, e2, tbo.apply, tbr.execute
    )
    require(not history_ablated["qualified"], history_ablated)
    require(
        history_ablated["rejection_reason"]
        == "RELATION_TARGET_HISTORY_UNRESOLVED",
        history_ablated,
    )

    diag = v1_diagnostic(s0, e2)
    require(diag[
        "false_generator_availability_if_target_identity_omitted"
    ], diag)

    result = {
        "study": "NATURAL_QUALIFIED_COMPOSITION_PAPER_MONEY_V1",
        "data_status": "PREEXISTING_EXPOSED_PAGE_VERIFIED_SOURCE_ROWS",
        "disposition": "NATURAL_COMPOSITION_PASS",
        "source_audit": {
            "claim_events": {
                k: {
                    "operation": v["operation"],
                    "evidence_relation": v["evidence_relation"],
                    "verification_status": v["verification_status"],
                }
                for k, v in source["claims"].items()
            },
            "stance_traces": {
                k: {
                    "trace_type": v["trace_type"],
                    "target": v["target"],
                    "verbatim_cue": v["verbatim_cue"],
                    "verification_status": v["verification_status"],
                }
                for k, v in source["traces"].items()
            },
            "ontology_contains_prior_critic_correction": True,
        },
        "forward": {
            "initial_claims": live_claim_ids(s0),
            "step1_relation": e1["evidence_relation"],
            "step1_relation_target": e1["relation_target_claim_id"],
            "step1_generator": step1["generator"],
            "after_step1_claims": live_claim_ids(s1),
            "step2_relation": e2["evidence_relation"],
            "step2_relation_target": e2["relation_target_claim_id"],
            "step2_generator": step2["generator"],
            "final_claims": live_claim_ids(s2),
            "transition_history": transitions,
        },
        "reverse_order": {
            "pm03_at_s0_qualified": reverse["qualified"],
            "rejection_reason": reverse["rejection_reason"],
            "psi_unchanged": reverse["before_psi"] == reverse["after_psi"],
            "xi_unchanged": reverse["before_xi"] == reverse["after_xi"],
            "partial_noncommutativity": True,
        },
        "history_ablation": {
            "psi_equal": tbo.psi(s1) == tbo.psi(s1_psi_only),
            "xi_equal": tbo.xi(s1) == tbo.xi(s1_psi_only),
            "pm03_with_full_history_generator": step2["generator"],
            "pm03_without_history_qualified": history_ablated["qualified"],
            "pm03_without_history_reason": history_ablated[
                "rejection_reason"
            ],
            "future_generator_availability_depends_on_history": True,
        },
        "v1_relation_type_only_diagnostic": diag,
        "oracle_runtime_exact": True,
        "operation_absent_from_input": True,
        "claim_ceiling": [
            "This is one natural page-verified multi-step sequence, not a prevalence estimate.",
            "The reverse order is a controlled qualification counterfactual, not an observed historical chronology.",
            "The result establishes relation-target and retained-history dependence for this sequence.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "natural_paper_money_composition_v1.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "disposition": result["disposition"],
        "forward": {
            "generators": [
                step1["generator"],
                step2["generator"],
            ],
            "after_step1_claims": live_claim_ids(s1),
            "final_claims": live_claim_ids(s2),
        },
        "reverse_order": result["reverse_order"],
        "history_ablation": result["history_ablation"],
        "v1_diagnostic": diag,
        "oracle_runtime_exact": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
