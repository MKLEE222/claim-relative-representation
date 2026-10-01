from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
I_DIR = HERE.parent / "module_i_dahn_document_boundary_holdout_v1"
J_DIR = HERE.parent / "module_j_dahn_object_bound_holdout_v1"
for p in (str(HERE), str(I_DIR), str(J_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_hardening_v2 as i_fx
import test_object_contract_v1 as j_fx
import oracle_l
import runtime_l
import evaluator_l

CTX = {
    "source_repository": "SYNTHETIC/PORTABLE-INHERITED",
    "source_version": "frozen-test-v1",
    "population_scope": "SYNTHETIC_INHERITED_OBLIGATIONS",
}


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def claim_core(c):
    return (
        c.get("role"),
        tuple(c.get("interval") or []),
        c.get("source_locator_contract"),
        c.get("object_id"),
        c.get("object_boundary_signature"),
        c.get("applicability_class"),
    )


def parse_pair(path, raw, fault=None):
    o = oracle_l.parse_document(path, raw, CTX)
    r = runtime_l.parse_document(path, raw, CTX, fault=fault)
    return o, r


def evaluate(o, r, fault=None):
    t = runtime_l.execute(r, "I_RSTAR", fault=fault)
    return t, evaluator_l.evaluate_trace(t, o, r)


def main():
    out = {}

    # Portable baseline on the inherited synthetic fixture.
    o, r = parse_pair("SYNTHETIC/inherited_primary.xml", i_fx.SYNTHETIC)
    require(o["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT", o["object_contract"])
    require(r["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT", r["object_contract"])
    require(o["object_id"] == r["object_id"], "portable inherited baseline object IDs differ")
    require(o["full_trajectory_eligible"], o["full_trajectory_exclusion_reasons"])
    t, e = evaluate(o, r)
    require(e["end_to_end_pass"], e)
    out["L_R0_BASELINE"] = True

    # I/F1: lower-level annex contamination cannot enter portable active claims.
    _, r_annex = parse_pair("SYNTHETIC/inherited_primary.xml", i_fx.SYNTHETIC, fault="annex_contamination")
    out["L_R1_ANNEX_CONTAMINATION_CONTAINED"] = sorted(map(claim_core, r_annex["claims"])) == sorted(map(claim_core, r["claims"]))
    require(out["L_R1_ANNEX_CONTAMINATION_CONTAINED"], {
        "normal": r["claims"],
        "fault": r_annex["claims"],
    })

    # I/F2-F7: inherited dynamic faults must still be rejected/detected.
    _, e2 = evaluate(o, r, {"type": "wrong_origin_binding"})
    out["L_R2_WRONG_ORIGIN_BINDING"] = not e2["end_to_end_pass"] and not e2["applicability_exact"]
    require(out["L_R2_WRONG_ORIGIN_BINDING"], e2)

    _, e3 = evaluate(o, r, {"type": "wrong_warrant"})
    out["L_R3_WRONG_WARRANT"] = not e3["end_to_end_pass"] and not e3["warrant_exact"]
    require(out["L_R3_WRONG_WARRANT"], e3)

    _, e4 = evaluate(o, r, {"type": "collateral_mutation"})
    out["L_R4_COLLATERAL_MUTATION"] = not e4["end_to_end_pass"] and not e4["selective_update"]
    require(out["L_R4_COLLATERAL_MUTATION"], e4)

    required = o["required_live_claim_keys_after"]
    require(bool(required), "baseline must require at least one live alternative")
    _, e5 = evaluate(o, r, {"type": "drop_live_key", "claim_key": required[0]})
    out["L_R5_DROPPED_LIVE_ALTERNATIVE"] = not e5["end_to_end_pass"] and not e5["alternative_persistence"]
    require(out["L_R5_DROPPED_LIVE_ALTERNATIVE"], e5)

    _, e6 = evaluate(o, r, {"type": "neutral_mutation"})
    out["L_R6_NEUTRAL_MUTATION"] = not e6["end_to_end_pass"] and not e6["null_event_stable"]
    require(out["L_R6_NEUTRAL_MUTATION"], e6)

    _, e7 = evaluate(o, r, {"type": "drop_history"})
    out["L_R7_MISSING_HISTORY"] = not e7["end_to_end_pass"] and not e7["transition_history_exact"]
    require(out["L_R7_MISSING_HISTORY"], e7)

    # I/F8: an inherited lower-level wrong-boundary fault cannot override L's
    # independently recomputed scholarly-object boundary.
    _, r8 = parse_pair("SYNTHETIC/inherited_primary.xml", i_fx.SYNTHETIC, fault="wrong_boundary")
    _, e8 = evaluate(o, r8)
    out["L_R8_WRONG_LEGACY_BOUNDARY_CONTAINED"] = all([
        r8["object_id"] == r["object_id"],
        r8["primary_boundary_signature"] == r["primary_boundary_signature"],
        e8["object_contract_exact"],
        e8["end_to_end_pass"],
    ])
    require(out["L_R8_WRONG_LEGACY_BOUNDARY_CONTAINED"], e8)

    # I/F9: composite origin remains unresolved.
    composite = i_fx.SYNTHETIC.replace(
        b'Editorial origin <origDate when="1900-01-02">2 Jan 1900</origDate>.',
        b'Editorial origin <origDate when="1900-01-02">2 Jan 1900</origDate> or '
        b'<origDate when="1900-01-04">4 Jan 1900</origDate>.',
    )
    o9, r9 = parse_pair("SYNTHETIC/composite_origin.xml", composite)
    out["L_R9_COMPOSITE_ORIGIN_REJECTED"] = all([
        o9["origin_contract_status"] == "COMPOSITE_ORIGIN_UNRESOLVED",
        r9["origin_contract_status"] == "COMPOSITE_ORIGIN_UNRESOLVED",
        o9["origin_claim"] is None,
        r9["origin_claim"] is None,
        not o9["full_trajectory_eligible"],
        not r9["full_trajectory_eligible"],
    ])
    require(out["L_R9_COMPOSITE_ORIGIN_REJECTED"], {
        "oracle": o9["full_trajectory_exclusion_reasons"],
        "runtime": r9["full_trajectory_exclusion_reasons"],
    })

    # Compatible dates remain a negative control.
    compatible = i_fx.SYNTHETIC.replace(b'when="1900-01-03"', b'when="1900-01-01"', 1)
    compatible = compatible.replace(b'when="1900-01-02"', b'when="1900-01-01"', 1)
    oc, rc = parse_pair("SYNTHETIC/compatible.xml", compatible)
    out["L_RNEG_NO_INVENTED_QUESTION"] = (
        not oc["eligibility"]["eligible"]
        and not rc["eligibility"]["eligible"]
        and runtime_l.discover(rc["claims"], expected_object_id=rc.get("object_id")) is None
    )
    require(out["L_RNEG_NO_INVENTED_QUESTION"], {
        "oracle": oc["eligibility"],
        "runtime": rc["eligibility"],
    })

    # J/F10: aggregate metadata without one scholarly object.
    o10, r10 = parse_pair("SYNTHETIC/no_primary.xml", j_fx.NO_PRIMARY)
    out["L_R10_AGGREGATE_REJECTED"] = all([
        o10["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        r10["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        not o10["eligibility"]["eligible"],
        not r10["eligibility"]["eligible"],
    ])
    require(out["L_R10_AGGREGATE_REJECTED"], {"oracle": o10["object_contract"], "runtime": r10["object_contract"]})

    # J/F11: multiple explicit primary letters.
    o11, r11 = parse_pair("SYNTHETIC/multiple.xml", j_fx.MULTIPLE)
    out["L_R11_MULTIPLE_PRIMARY_REJECTED"] = all([
        o11["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        r11["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        o11["object_contract"]["candidate_count"] == 2,
        r11["object_contract"]["candidate_count"] == 2,
    ])
    require(out["L_R11_MULTIPLE_PRIMARY_REJECTED"], {"oracle": o11["object_contract"], "runtime": r11["object_contract"]})

    # J/F12: claim/object rebinding fault remains fatal.
    o12 = oracle_l.parse_document("SYNTHETIC/cross_object.xml", j_fx.SINGLE, CTX)
    r12 = runtime_l.parse_document("SYNTHETIC/cross_object.xml", j_fx.SINGLE, CTX, fault="cross_object_claim")
    _, e12 = evaluate(o12, r12)
    out["L_R12_CROSS_OBJECT_CLAIM_REJECTED"] = not e12["end_to_end_pass"] and not e12["object_claim_binding_exact"]
    require(out["L_R12_CROSS_OBJECT_CLAIM_REJECTED"], e12)

    # J/F13-F15 positive/negative object routes.
    o13, r13 = parse_pair("SYNTHETIC/direct_transcription.xml", j_fx.DIRECT_TRANSCRIPTION)
    out["L_R13_TRANSCRIPTION_AS_LETTER"] = all([
        o13["object_contract"]["boundary_kind"] == "TRANSCRIPTION_AS_LETTER",
        r13["object_contract"]["boundary_kind"] == "TRANSCRIPTION_AS_LETTER",
        o13["object_id"] == r13["object_id"],
    ])
    require(out["L_R13_TRANSCRIPTION_AS_LETTER"], {"oracle": o13["object_contract"], "runtime": r13["object_contract"]})

    o14, r14 = parse_pair("SYNTHETIC/two_transcriptions.xml", j_fx.TWO_TRANSCRIPTIONS)
    out["L_R14_MULTIPLE_TRANSCRIPTIONS_REJECTED"] = all([
        o14["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        r14["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        o14["object_contract"]["candidate_count"] == 2,
        r14["object_contract"]["candidate_count"] == 2,
    ])
    require(out["L_R14_MULTIPLE_TRANSCRIPTIONS_REJECTED"], {"oracle": o14["object_contract"], "runtime": r14["object_contract"]})

    o15, r15 = parse_pair("SYNTHETIC/untyped_letter.xml", j_fx.UNTYPED_LETTER)
    out["L_R15_UNTYPED_BODY_LETTER"] = all([
        o15["object_contract"]["boundary_kind"] == "UNTYPED_BODY_LETTER",
        r15["object_contract"]["boundary_kind"] == "UNTYPED_BODY_LETTER",
        o15["object_id"] == r15["object_id"],
    ])
    require(out["L_R15_UNTYPED_BODY_LETTER"], {"oracle": o15["object_contract"], "runtime": r15["object_contract"]})

    o16, r16 = parse_pair("SYNTHETIC/untyped_placeholder.xml", j_fx.UNTYPED_PLACEHOLDER)
    out["L_R16_UNTYPED_PLACEHOLDER_REJECTED"] = all([
        o16["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        r16["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        not o16["eligibility"]["eligible"],
        not r16["eligibility"]["eligible"],
    ])
    require(out["L_R16_UNTYPED_PLACEHOLDER_REJECTED"], {"oracle": o16["object_contract"], "runtime": r16["object_contract"]})

    # Annex date remains excluded in portable parsing.
    annex_interval = ["1905-01-01", "1905-01-01"]
    out["L_RANNEX_DATE_EXCLUDED"] = all(
        c.get("interval") != annex_interval for c in o["claims"] + r["claims"]
    )
    require(out["L_RANNEX_DATE_EXCLUDED"], {"oracle": o["claims"], "runtime": r["claims"]})

    print({
        "portable_inherited_obligations": out,
        "all_pass": all(out.values()),
    })


if __name__ == "__main__":
    main()
