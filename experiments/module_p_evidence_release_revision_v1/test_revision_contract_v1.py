from __future__ import annotations

import copy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
M_DIR = HERE.parent / "module_m_dh_comparators_v1"
for p in (L_DIR, M_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import oracle_p
import runtime_p
import evaluator_p
import comparators_m
import evaluator_m


CTX = {
    "source_repository": "SYNTHETIC/MODULE_P",
    "source_version": "module-p-v1",
    "population_scope": "synthetic-controls",
}


def letter_xml(sent_date: str | None, origin_date: str) -> bytes:
    sent = (
        f'<date when="{sent_date}">{sent_date}</date>'
        if sent_date is not None else
        '<persName>Sender</persName>'
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <history><origin><p xml:lang="en">
    <origDate when="{origin_date}">{origin_date}</origDate>
   </p></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent">
   {sent}
  </correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body><div type="letter"><p>Primary scholarly object.</p></div></body></text>
</TEI>""".encode("utf-8")


CONFLICT = letter_xml("1900-01-01", "1900-01-02")
UNRESOLVED_TO_EXACT = letter_xml(None, "1900-01-02")
BASIS_ONLY = letter_xml("1900-01-01", "1900-01-01")


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def parsed(name, raw):
    path = f"SYNTHETIC/{name}.xml"
    o = oracle_p.parse_document(path, raw, CTX)
    r = runtime_p.parse_document(path, raw, CTX)
    return path, o, r


def main():
    results = {}

    # P-F1: one current exact sent date; disjoint later evidence forms an alternative set.
    p1, o1, r1 = parsed("p_f1_conflict", CONFLICT)
    require(not o1["eligibility"]["eligible"], o1["eligibility"])
    require(not r1["eligibility"]["eligible"], r1["eligibility"])
    require(o1["p_erir_eligible"] and r1["p_erir_eligible"], {
        "oracle": o1["p_disposition"],
        "runtime": r1["p_disposition"],
    })
    require(
        o1["p_transition_class"] == r1["p_transition_class"]
        == "P-U1_CONFLICT_FORMATION",
        {"oracle": o1["p_transition_class"], "runtime": r1["p_transition_class"]},
    )
    t1 = runtime_p.execute(r1)
    e1 = evaluator_p.evaluate(t1, o1, r1)
    debug1 = {
        "evaluation": e1,
        "oracle_root": o1.get("warrant_root"),
        "runtime_root": r1.get("warrant_root"),
        "oracle_post": o1.get("warrant_after"),
        "runtime_post": r1.get("warrant_after"),
        "trace_post": t1.get("post_event_warrant"),
        "oracle_phi_before": o1.get("p_warrant_before"),
        "runtime_phi_before": r1.get("p_warrant_before"),
        "oracle_phi_after": o1.get("p_warrant_after"),
        "runtime_phi_after": r1.get("p_warrant_after"),
        "trace_phi_after": t1.get("post_event_phi"),
        "oracle_origin": o1.get("origin_claim"),
        "runtime_origin": r1.get("origin_claim"),
    }
    require(e1["eligibility_exact"], debug1)
    require(e1["reference_end_to_end_pass"], debug1)
    results["P-F1_VALID_CONFLICT_FORMATION"] = True

    # P-F2: no machine-readable t0 date; later evidence yields a warranted exact state.
    p2, o2, r2 = parsed("p_f2_unresolved", UNRESOLVED_TO_EXACT)
    require(not o2["eligibility"]["eligible"], o2["eligibility"])
    require(not r2["eligibility"]["eligible"], r2["eligibility"])
    require(o2["p_erir_eligible"] and r2["p_erir_eligible"], {
        "oracle": o2["p_disposition"],
        "runtime": r2["p_disposition"],
    })
    require(
        o2["p_transition_class"] == r2["p_transition_class"]
        == "P-U2_RESOLUTION_OR_ACQUISITION",
        {"oracle": o2["p_transition_class"], "runtime": r2["p_transition_class"]},
    )
    t2 = runtime_p.execute(r2)
    e2 = evaluator_p.evaluate(t2, o2, r2)
    require(e2["reference_end_to_end_pass"], e2)
    results["P-F2_VALID_UNRESOLVED_TO_WARRANTED"] = True

    # P-F3 + P-F10: basis-only replacement is admissible but not a substantive revision.
    p3, o3, r3 = parsed("p_f3_basis_only", BASIS_ONLY)
    require(o3["p_admissible_null_event"] and r3["p_admissible_null_event"], {
        "oracle": o3["p_disposition"],
        "runtime": r3["p_disposition"],
    })
    require(not o3["p_erir_eligible"] and not r3["p_erir_eligible"], {
        "oracle": o3["p_erir_eligible"],
        "runtime": r3["p_erir_eligible"],
    })
    require(o3["p_warrant_before"] == o3["p_warrant_after"], {
        "before": o3["p_warrant_before"],
        "after": o3["p_warrant_after"],
    })
    require(r3["p_warrant_before"] == r3["p_warrant_after"], {
        "before": r3["p_warrant_before"],
        "after": r3["p_warrant_after"],
    })
    t3 = runtime_p.execute(r3)
    require(t3["origin_transition"]["applicable"], t3["origin_transition"])
    results["P-F3_BASIS_ONLY_NOT_ELIGIBLE"] = True
    results["P-F10_NULL_EVENT_NOT_PROMOTED"] = True

    # P-F4: wrong object binding rejects event before mutation.
    t4 = runtime_p.execute(r1, fault={"type": "wrong_object"})
    require(not t4["origin_transition"]["applicable"], t4["origin_transition"])
    require(t4["post_event_warrant"] == r1["warrant_root"], t4)
    require(
        t4["origin_transition"].get("collateral_temporal_paths")
        == ["ORIGIN_HANDLE_BINDING_MISMATCH"],
        t4["origin_transition"],
    )
    results["P-F4_WRONG_OBJECT_REJECTED"] = True

    # P-F5: wrong source version rejects event before mutation.
    t5 = runtime_p.execute(r1, fault={"type": "wrong_source_version"})
    require(not t5["origin_transition"]["applicable"], t5["origin_transition"])
    require(t5["post_event_warrant"] == r1["warrant_root"], t5)
    require(
        t5["origin_transition"].get("collateral_temporal_paths")
        == ["ORIGIN_HANDLE_BINDING_MISMATCH"],
        t5["origin_transition"],
    )
    results["P-F5_WRONG_SOURCE_VERSION_REJECTED"] = True

    # P-F6: evidence visibility without applicability proof is insufficient.
    t6 = runtime_p.execute(r1, fault={"type": "missing_applicability"})
    require(not t6["origin_transition"]["applicable"], t6["origin_transition"])
    require(t6["post_event_warrant"] == r1["warrant_root"], t6)
    require(
        t6["origin_transition"].get("collateral_temporal_paths")
        == ["ORIGIN_HANDLE_BINDING_MISMATCH"],
        t6["origin_transition"],
    )
    results["P-F6_MISSING_APPLICABILITY_REJECTED"] = True

    # P-F7: valid evidence can still be applied non-selectively; detect the collateral change.
    t7 = runtime_p.execute(r1, fault={"type": "collateral_mutation"})
    e7 = evaluator_p.evaluate(t7, o1, r1)
    require(t7["origin_transition"]["applicable"], t7["origin_transition"])
    require(not e7["P4_SELECTIVE_UPDATE"], e7)
    require(bool(t7["origin_transition"]["collateral_temporal_paths"]), t7)
    require(e7["P6_TRANSITION_ATTRIBUTION"], e7)
    results["P-F7_COLLATERAL_MUTATION_DETECTED"] = True

    # P-F8: final result can be correct while delayed history is unavailable.
    t8 = runtime_p.execute(r1, drop_history=True)
    e8 = evaluator_p.evaluate(t8, o1, r1)
    require(e8["P3_POST_EVENT_RESULT"], e8)
    require(e8["P4_SELECTIVE_UPDATE"], e8)
    require(e8["P5_PROVENANCE"], e8)
    require(e8["P6_TRANSITION_ATTRIBUTION"], e8)
    require(not e8["P7_DELAYED_HISTORY"], e8)
    results["P-F8_NO_HISTORY_SEPARATION"] = True

    # P-F9: identical ordered state snapshots do not determine event semantics.
    snap_a = comparators_m.ordered_snapshots(r1)
    snap_b = comparators_m.ordered_snapshots(copy.deepcopy(r1))
    proj_a = comparators_m.history_blind_projection(snap_a)
    proj_b = comparators_m.history_blind_projection(snap_b)
    history_a = {
        "event_class": "EVIDENCE_RELEASE",
        "event_id": f"OPEN_ORIGIN::{p1}",
        "evidence_key": o1["origin_claim"]["claim_key"],
    }
    history_b = {
        "event_class": "STATE_IMPORT",
        "event_id": f"IMPORT::{p1}",
        "evidence_key": None,
    }
    require(history_a != history_b, {"a": history_a, "b": history_b})
    require(proj_a == proj_b, "ordered snapshots unexpectedly encode event semantics")
    require(e1["P6_TRANSITION_ATTRIBUTION"] and e1["P7_DELAYED_HISTORY"], e1)
    results["P-F9_SNAPSHOT_NONIDENTIFIABILITY"] = True

    # Comparator positive controls remain strong on the new task.
    current = comparators_m.current_reopen(r1)
    snaps = comparators_m.ordered_snapshots(r1)
    m_current = evaluator_m.evaluate_regime(current, o1)
    m_snaps = evaluator_m.evaluate_regime(snaps, o1)
    require(m_current["T1_CURRENT_STATE_EXACT"], m_current)
    require(m_current["T2_CURRENT_PROVENANCE_EXACT"], m_current)
    require(m_snaps["T1_CURRENT_STATE_EXACT"], m_snaps)
    require(m_snaps["T2_CURRENT_PROVENANCE_EXACT"], m_snaps)
    require(m_snaps["T3_STATE_DELTA_EXACT"], m_snaps)

    print({
        "study": "MODULE_P_SYNTHETIC_GATE_V1",
        "all_controls_passed": all(results.values()),
        "controls": results,
        "reference_conflict_evaluation": e1,
        "reference_resolution_evaluation": e2,
        "basis_only_disposition": {
            "oracle": o3["p_disposition"],
            "runtime": r3["p_disposition"],
        },
        "module_m_positive_controls": {
            "B_CURRENT_REOPEN": m_current,
            "B_ORDERED_SNAPSHOTS": m_snaps,
        },
    })


if __name__ == "__main__":
    main()
