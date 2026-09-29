from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import target_bound_oracle_v2 as qo
import target_bound_runtime_v2 as qr

CLAIMS = ROOT / "data" / "yule_cordier_claim_events.csv"
TRACES = ROOT / "data" / "paper_money_archival_stance_traces_v1.csv"
PANEL = ROOT / "data" / "r3_verified_proposition_panel_v1.csv"
PASS1 = ROOT / "experiments" / "deepening_v1" / "r3_pass1_B02_entry_labels_v1.csv"
ACT_PROTOCOL = ROOT / "experiments" / "deepening_v1" / "R3_ACT_SEGMENTATION_PROTOCOL.md"


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def one(rows, key, value):
    found = [x for x in rows if x.get(key) == value]
    require(len(found) == 1, {"key": key, "value": value, "found": found})
    return found[0]


def norm(result):
    out = copy.deepcopy(result)
    out.pop("engine", None)
    return out


def exact_pair(state, event):
    o = qo.apply(state, event)
    r = qr.execute(state, event)
    require(norm(o) == norm(r), {"oracle": norm(o), "runtime": norm(r)})
    return o


def source_audit():
    claims = read_csv(CLAIMS)
    traces = read_csv(TRACES)
    panel = read_csv(PANEL)
    pass1 = read_csv(PASS1)

    pm = {x: one(claims, "event_id", x) for x in ("PM01", "PM02", "PM03")}
    pmt = {x: one(traces, "trace_id", x) for x in ("PMT01", "PMT02", "PMT03")}
    arbr = {
        x: one(panel, "proposition_id", x)
        for x in ("ARBR-ID-1903", "ARBR-ID-HS", "ARBR-REPLY-CORDIER")
    }
    arbr_entry = one(pass1, "entry_id", "YC1920E-0024")

    require(all(
        pm[x]["verification_status"].strip().lower() == "page image verified"
        for x in pm
    ), pm)
    require(all(pmt[x]["verification_status"] == "PAGE_VERIFIED" for x in pmt), pmt)
    require(all(
        arbr[x]["verification_authority"] == "PAGE_VERIFIED_BOTH"
        for x in arbr
    ), arbr)

    require(arbr["ARBR-ID-HS"]["target_proposition_id"] == "ARBR-ID-1903", arbr)
    require(arbr["ARBR-ID-HS"]["relation_to_target"] == "COMPETING_IDENTIFICATION", arbr)
    require(
        arbr["ARBR-REPLY-CORDIER"]["target_proposition_id"] == "ARBR-ID-HS",
        arbr,
    )
    require(
        arbr["ARBR-REPLY-CORDIER"]["relation_to_target"] == "BIBLIOGRAPHIC_REPLY",
        arbr,
    )
    require(
        "followed by Cordier's response" in arbr_entry["act_note"],
        arbr_entry,
    )

    act_text = ACT_PROTOCOL.read_text(encoding="utf-8")
    require("INTERVENTION_ACT" in act_text, "act-level protocol missing")

    return {
        "paper_money_claims": pm,
        "paper_money_traces": pmt,
        "arbre_sec_propositions": arbr,
        "arbre_sec_entry": arbr_entry,
    }


def state(object_id, source_version, target, claim):
    return {
        "object_id": object_id,
        "source_repository": "YULE_CORDIER_VERIFIED_ARCHIVE",
        "source_version": source_version,
        "registered_targets": [target],
        "assertions": {target: [claim]},
        "evidence_ledger": [],
        "event_ledger": [],
        "transition_ledger": [],
    }


def claim(claim_id, object_id, target, value, status, source_id, locator, agent):
    return {
        "claim_id": claim_id,
        "object_id": object_id,
        "target_property": target,
        "value": value,
        "status": status,
        "source_id": source_id,
        "source_locator": locator,
        "responsible_agent": agent,
    }


def event(
    event_id,
    object_id,
    source_version,
    target,
    evidence_id,
    locator,
    relation,
    relation_target,
    responsible,
    mediator=None,
    new_claim_id=None,
    value=None,
    status=None,
):
    return {
        "event_id": event_id,
        "event_class": "SCHOLARLY_REASSESSMENT",
        "object_id": object_id,
        "target_property": target,
        "source_repository": "YULE_CORDIER_VERIFIED_ARCHIVE",
        "source_version": source_version,
        "evidence_id": evidence_id,
        "evidence_locator": locator,
        "responsible_agent": responsible,
        "mediator_agent": mediator,
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "evidence_relation": relation,
        "relation_target_claim_id": relation_target,
        "new_claim_id": new_claim_id,
        "value": value,
        "status": status,
    }


def live_claim_ids(s, target):
    return sorted(x["claim_id"] for x in s["assertions"][target])


def paper_money():
    obj = "YC-PAPER-MONEY"
    version = "PM01_PM02_PM03_PAGE_VERIFIED_SEQUENCE_V2"
    target = "paper-money-material-identification"
    s0 = state(
        obj,
        version,
        target,
        claim(
            "PM01",
            obj,
            target,
            "MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE",
            "NARRATIVE_ASSERTED",
            "PM01",
            "1903 vol. 1 printed p. 423",
            "Marco Polo/Rustichello/Yule translation",
        ),
    )

    e1 = event(
        "PM02_EVENT",
        obj,
        version,
        target,
        "PM02",
        "1903 vol.1 p430 / scan732",
        "CONTRADICTS_PRIOR",
        "PM01",
        "Emil Bretschneider as transmitted by Henri Cordier",
        mediator="Henri Cordier",
        new_claim_id="PM02",
        value="MULBERRY_BARK_IDENTIFICATION_MISTAKEN",
        status="ASSERTED",
    )
    e2 = event(
        "PM03_EVENT",
        obj,
        version,
        target,
        "PM03",
        "1920 pp70-72 / scan84-86",
        "CORRECTION_OF_PRIOR_CRITICISM",
        "PM02",
        "Berthold Laufer as transmitted by Henri Cordier",
        mediator="Henri Cordier",
        new_claim_id="PM03",
        value="MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE",
        status="RESTORED_AS_CORRECT",
    )

    a = exact_pair(s0, e1)
    require(a["qualified"] and a["generator"] == "ADD_ALTERNATIVE", a)
    s1 = a["state"]
    require(live_claim_ids(s1, target) == ["PM01", "PM02"], s1)

    b = exact_pair(s1, e2)
    require(b["qualified"] and b["generator"] == "RESOLVE", b)
    require(live_claim_ids(b["state"], target) == ["PM03"], b["state"])

    reverse = exact_pair(s0, e2)
    require(not reverse["qualified"], reverse)
    require(reverse["rejection_reason"] == "RELATION_TARGET_NOT_LIVE", reverse)

    s1_nohist = copy.deepcopy(s1)
    s1_nohist["evidence_ledger"] = []
    s1_nohist["event_ledger"] = []
    s1_nohist["transition_ledger"] = []
    require(qo.psi(s1) == qo.psi(s1_nohist), {"full": qo.psi(s1), "nohist": qo.psi(s1_nohist)})
    require(qo.xi(s1) != qo.xi(s1_nohist), {"full": qo.xi(s1), "nohist": qo.xi(s1_nohist)})

    hist_fail = exact_pair(s1_nohist, e2)
    require(not hist_fail["qualified"], hist_fail)
    require(
        hist_fail["rejection_reason"] == "RELATION_TARGET_HISTORY_UNRESOLVED",
        hist_fail,
    )

    return {
        "forward_generators": [a["generator"], b["generator"]],
        "after_step1_claims": live_claim_ids(s1, target),
        "final_claims": live_claim_ids(b["state"], target),
        "reverse_reason": reverse["rejection_reason"],
        "history_ablation_reason": hist_fail["rejection_reason"],
        "history_required_for_step2": True,
    }


def arbre_sec():
    obj = "YC-ARBRE-SEC"
    version = "ARBR_1903_1920_PAGE_VERIFIED_V2"
    target = "arbre-sec-identification"

    s0 = state(
        obj,
        version,
        target,
        claim(
            "ARBR-ID-1903",
            obj,
            target,
            "ORIENTAL_PLANE_CHINAR",
            "ASSERTED",
            "ARBR-ID-1903",
            "1903 I:113,128",
            "EARLIER_EDITORIAL_NOTE",
        ),
    )

    e1 = event(
        "ARBR-ID-HS-EVENT",
        obj,
        version,
        target,
        "ARBR-ID-HS",
        "1920 p.31",
        "COMPETING_IDENTIFICATION",
        "ARBR-ID-1903",
        "HOUTUM_SCHINDLER",
        mediator="CORDIER",
        new_claim_id="ARBR-ID-HS",
        value="CYPRESS_OF_ZOROASTER",
        status="ASSERTED_PROPOSAL",
    )

    e2 = event(
        "ARBR-REPLY-CORDIER-EVENT",
        obj,
        version,
        target,
        "ARBR-REPLY-CORDIER",
        "1920 p.31",
        "BIBLIOGRAPHIC_REPLY",
        "ARBR-ID-HS",
        "CORDIER",
        mediator=None,
        new_claim_id=None,
        value=None,
        status=None,
    )

    a = exact_pair(s0, e1)
    require(a["qualified"] and a["generator"] == "ADD_ALTERNATIVE", a)
    s1 = a["state"]
    require(
        live_claim_ids(s1, target)
        == ["ARBR-ID-1903", "ARBR-ID-HS"],
        s1,
    )

    b = exact_pair(s1, e2)
    require(b["qualified"] and b["generator"] == "RECORD_EVIDENCE", b)
    require(b["assertion_identity"], b)
    require(b["history_nonidentity"], b)
    require(b["before_psi"] == b["after_psi"], b)
    require(b["before_xi"] != b["after_xi"], b)
    require(
        live_claim_ids(b["state"], target)
        == ["ARBR-ID-1903", "ARBR-ID-HS"],
        b["state"],
    )

    reverse = exact_pair(s0, e2)
    require(not reverse["qualified"], reverse)
    require(reverse["rejection_reason"] == "RELATION_TARGET_NOT_LIVE", reverse)
    require(reverse["before_psi"] == reverse["after_psi"], reverse)
    require(reverse["before_xi"] == reverse["after_xi"], reverse)

    return {
        "forward_generators": [a["generator"], b["generator"]],
        "after_step1_claims": live_claim_ids(s1, target),
        "final_claims": live_claim_ids(b["state"], target),
        "reply_assertion_identity": b["assertion_identity"],
        "reply_history_nonidentity": b["history_nonidentity"],
        "reverse_reason": reverse["rejection_reason"],
        "target_bound_enablement": True,
    }


def no_case_specific_branches():
    forbidden = (
        "PM01",
        "PM02",
        "PM03",
        "ARBR",
        "paper-money",
        "arbre-sec",
        "YC-PAPER",
        "YC-ARBRE",
    )
    files = [
        HERE / "target_bound_oracle_v2.py",
        HERE / "target_bound_runtime_v2.py",
    ]
    findings = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        hits = [x for x in forbidden if x in text]
        findings[path.name] = hits
        require(not hits, findings)
    return findings


def main():
    source = source_audit()
    branch_scan = no_case_specific_branches()
    pm = paper_money()
    arbr = arbre_sec()

    result = {
        "study": "NATURAL_ACT_LEVEL_QUALIFIED_COMPOSITION_V2",
        "data_status": "PREEXISTING_EXPOSED_PAGE_VERIFIED_PROPOSITION_AND_TRACE_ROWS",
        "disposition": "NATURAL_ACT_COMPOSITION_REPLICATION_PASS",
        "source_audit": {
            "paper_money_page_verified": True,
            "arbre_sec_page_verified_both": True,
            "arbre_sec_source_order_confirmed": True,
            "act_segmentation_contract_present": True,
        },
        "paper_money": pm,
        "arbre_sec": arbr,
        "engine_case_specific_branch_scan": branch_scan,
        "oracle_runtime_exact": True,
        "cross_relation_family_portability": {
            "contrast_relations": [
                "CONTRADICTS_PRIOR",
                "CORRECTION_OF_PRIOR_CRITICISM",
            ],
            "proposition_relations": [
                "COMPETING_IDENTIFICATION",
                "BIBLIOGRAPHIC_REPLY",
            ],
            "same_engine": True,
        },
        "claim_ceiling": [
            "Two natural page-verified sequences are supported, but this is not a prevalence estimate.",
            "Arbre Sec is act-level; Paper Money remains event-level for the PM03 compound source event.",
            "The result supports target-bound qualification across two pre-existing relation families.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "natural_act_composition_v2.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "disposition": result["disposition"],
        "paper_money": pm,
        "arbre_sec": arbr,
        "case_specific_branch_scan": branch_scan,
        "cross_relation_family_portability": result[
            "cross_relation_family_portability"
        ],
        "oracle_runtime_exact": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
