from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import oracle_v2
import runtime_v2
import evaluator_v2

SYNTHETIC = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <sourceDesc>
        <msDesc>
          <msContents>
            <msItem><docDate when="1900-01-01">1 Jan 1900</docDate></msItem>
          </msContents>
          <history>
            <origin>
              <p xml:lang="en">Editorial origin <origDate when="1900-01-02">2 Jan 1900</origDate>.</p>
            </origin>
          </history>
        </msDesc>
      </sourceDesc>
    </fileDesc>
    <profileDesc>
      <correspDesc>
        <correspAction type="sent"><date when="1900-01-03">3 Jan 1900</date></correspAction>
      </correspDesc>
    </profileDesc>
    <revisionDesc>
      <change when="2020-01-01" who="#ed">Added facsimile identifier and layout metadata.</change>
    </revisionDesc>
  </teiHeader>
  <text>
    <body>
      <div type="transcription">
        <div type="letter">
          <opener><dateline><date when="1900-01-01">1 Jan 1900</date></dateline></opener>
          <p>Primary letter.</p>
        </div>
        <div type="annex">
          <div type="letter">
            <opener><dateline><date when="1905-01-01">1 Jan 1905</date></dateline></opener>
            <p>Annex letter.</p>
          </div>
        </div>
      </div>
    </body>
  </text>
</TEI>
"""


def contract(runtime_doc, oracle_doc):
    return {
        "boundary": runtime_doc["primary_boundary_signature"] == oracle_doc["primary_boundary_signature"],
        "claims": sorted(c["claim_key"] for c in runtime_doc["claims"])
        == sorted(c["claim_key"] for c in oracle_doc["claims"]),
        "origin": runtime_doc["origin_claim"]["claim_key"] == oracle_doc["origin_claim"]["claim_key"],
        "neutral": runtime_doc["neutral_event"]["event_key"] == oracle_doc["neutral_event"]["event_key"],
        "q0": runtime_v2.runtime_q0(runtime_doc) == oracle_doc["q0"],
    }


def evaluate(runtime_doc, oracle_doc, fault=None):
    trace = runtime_v2.execute(runtime_doc, "I_RSTAR", fault=fault)
    return trace, evaluator_v2.evaluate_trace(trace, oracle_doc, runtime_doc)


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def main():
    path = "SYNTHETIC/primary.xml"
    oracle_doc = oracle_v2.parse_document(path, SYNTHETIC)
    runtime_doc = runtime_v2.parse_document(path, SYNTHETIC)

    c = contract(runtime_doc, oracle_doc)
    require(all(c.values()), f"baseline independent parser contract failed: {c}")
    require(oracle_doc["full_trajectory_eligible"], "synthetic fixture is not full-trajectory eligible")

    baseline_trace, baseline = evaluate(runtime_doc, oracle_doc)
    require(baseline["end_to_end_pass"], f"baseline R* did not pass: {baseline}")

    detections = {}

    # Branch coverage: natural Berlin/Paul full trajectories do not expose an
    # EXACT post-origin warrant. Exercise INTERVAL -> EXACT independently here.
    exact_fixture = SYNTHETIC.replace(
        b'<msItem><docDate when="1900-01-01">1 Jan 1900</docDate></msItem>',
        b'<msItem><docDate from="1900-01-01" to="1900-01-31">January 1900</docDate></msItem>',
    ).replace(
        b'<correspAction type="sent"><date when="1900-01-03">3 Jan 1900</date></correspAction>',
        b'<correspAction type="sent"><date from="1900-01-01" to="1900-01-15">early January 1900</date></correspAction>',
    ).replace(
        b'<opener><dateline><date when="1900-01-01">1 Jan 1900</date></dateline></opener>',
        b'<opener><dateline><date from="1900-01-01" to="1900-01-31">January 1900</date></dateline></opener>',
    ).replace(
        b'<origDate when="1900-01-02">2 Jan 1900</origDate>',
        b'<origDate when="1900-01-03">3 Jan 1900</origDate>',
    )
    exact_oracle = oracle_v2.parse_document("SYNTHETIC/exact.xml", exact_fixture)
    exact_runtime = runtime_v2.parse_document("SYNTHETIC/exact.xml", exact_fixture)
    require(exact_oracle["eligibility"]["trigger"] == "D2", f"exact fixture trigger drift: {exact_oracle['eligibility']}")
    require(exact_oracle["warrant_root"]["type"] == "INTERVAL", f"exact fixture root drift: {exact_oracle['warrant_root']}")
    require(exact_oracle["warrant_after"]["type"] == "EXACT", f"exact fixture post drift: {exact_oracle['warrant_after']}")
    require(exact_oracle["full_trajectory_eligible"], "exact fixture must be full-trajectory eligible")
    exact_trace = runtime_v2.execute(exact_runtime, "I_RSTAR")
    exact_eval = evaluator_v2.evaluate_trace(exact_trace, exact_oracle, exact_runtime)
    require(exact_eval["end_to_end_pass"], f"exact branch failed: {exact_eval}")

    # F1 annex contamination
    rt_annex = runtime_v2.parse_document(path, SYNTHETIC, fault="annex_contamination")
    tr, ev = evaluate(rt_annex, oracle_doc)
    detections["F1_ANNEX_CONTAMINATION"] = not ev["discovery_exact"]
    require(detections["F1_ANNEX_CONTAMINATION"], f"annex contamination escaped discovery oracle: {ev}")

    # F2 wrong origin binding
    tr, ev = evaluate(runtime_doc, oracle_doc, {"type": "wrong_origin_binding"})
    detections["F2_WRONG_ORIGIN_BINDING"] = not ev["applicability_exact"] and not ev["provenance_exact"]
    require(detections["F2_WRONG_ORIGIN_BINDING"], f"wrong origin binding escaped: {ev}")

    # F3 wrong warrant
    tr, ev = evaluate(runtime_doc, oracle_doc, {"type": "wrong_warrant"})
    detections["F3_WRONG_WARRANT"] = not ev["warrant_exact"]
    require(detections["F3_WRONG_WARRANT"], f"wrong warrant escaped: {ev}")

    # F4 collateral mutation
    tr, ev = evaluate(runtime_doc, oracle_doc, {"type": "collateral_mutation"})
    detections["F4_COLLATERAL_MUTATION"] = ev["collateral_revision_count"] > 0 and not ev["selective_update"]
    require(detections["F4_COLLATERAL_MUTATION"], f"collateral mutation escaped: {ev}")

    # F5 dropped live alternative
    required = oracle_doc["required_live_claim_keys_after"]
    require(bool(required), "synthetic fixture needs a required live alternative")
    tr, ev = evaluate(
        runtime_doc,
        oracle_doc,
        {"type": "drop_live_key", "claim_key": required[0]},
    )
    detections["F5_DROPPED_LIVE_ALTERNATIVE"] = not ev["alternative_persistence"]
    require(detections["F5_DROPPED_LIVE_ALTERNATIVE"], f"dropped alternative escaped: {ev}")

    # F6 fake null stability
    tr, ev = evaluate(runtime_doc, oracle_doc, {"type": "neutral_mutation"})
    detections["F6_NEUTRAL_MUTATION"] = not ev["null_event_stable"]
    require(detections["F6_NEUTRAL_MUTATION"], f"neutral mutation escaped: {ev}")

    # F7 missing history
    tr, ev = evaluate(runtime_doc, oracle_doc, {"type": "drop_history"})
    detections["F7_MISSING_HISTORY"] = not ev["transition_history_exact"]
    require(detections["F7_MISSING_HISTORY"], f"missing history escaped: {ev}")

    # F8 wrong document boundary
    rt_wrong_boundary = runtime_v2.parse_document(path, SYNTHETIC, fault="wrong_boundary")
    tr, ev = evaluate(rt_wrong_boundary, oracle_doc)
    detections["F8_WRONG_DOCUMENT_BOUNDARY"] = not ev["boundary_exact"]
    require(detections["F8_WRONG_DOCUMENT_BOUNDARY"], f"wrong boundary escaped: {ev}")

    # F9 / contract control: composite chosen origin statement must not be simplified.
    composite = SYNTHETIC.replace(
        b'Editorial origin <origDate when="1900-01-02">2 Jan 1900</origDate>.',
        b'Editorial origin <origDate when="1900-01-02">2 Jan 1900</origDate> or '
        b'<origDate when="1900-01-04">4 Jan 1900</origDate>.',
    )
    odc = oracle_v2.parse_document("SYNTHETIC/composite.xml", composite)
    rdc = runtime_v2.parse_document("SYNTHETIC/composite.xml", composite)
    detections["F9_COMPOSITE_ORIGIN_REJECTED"] = all([
        odc["origin_contract_status"] == "COMPOSITE_ORIGIN_UNRESOLVED",
        rdc["origin_contract_status"] == "COMPOSITE_ORIGIN_UNRESOLVED",
        odc["origin_element_count"] == 2,
        rdc["origin_element_count"] == 2,
        odc["origin_claim"] is None,
        rdc["origin_claim"] is None,
        not odc["full_trajectory_eligible"],
        "COMPOSITE_ORIGIN_UNRESOLVED" in odc["full_trajectory_exclusion_reasons"],
    ])
    require(detections["F9_COMPOSITE_ORIGIN_REJECTED"], "composite origin was silently simplified")

    # Negative control: compatible dates should not invent a live question.
    compatible = SYNTHETIC.replace(b'when="1900-01-03"', b'when="1900-01-01"', 1)
    compatible = compatible.replace(b'when="1900-01-02"', b'when="1900-01-01"', 1)
    od2 = oracle_v2.parse_document("SYNTHETIC/compatible.xml", compatible)
    rd2 = runtime_v2.parse_document("SYNTHETIC/compatible.xml", compatible)
    require(not od2["eligibility"]["eligible"], f"oracle invented eligibility: {od2['eligibility']}")
    require(runtime_v2.discover(rd2["claims"]) is None, "runtime invented discovery on compatible fixture")

    print({
        "baseline_pass": baseline["end_to_end_pass"],
        "fault_detection": detections,
        "all_faults_detected": all(detections.values()),
        "exact_branch_coverage": exact_eval["end_to_end_pass"],
        "negative_control_no_question": True,
    })


if __name__ == "__main__":
    main()
