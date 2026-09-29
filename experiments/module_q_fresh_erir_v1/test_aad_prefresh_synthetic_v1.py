from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P_DIR = HERE.parent / "module_p_evidence_release_revision_v1"
L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
for p in (P_DIR, L_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import oracle_p
import runtime_p
import evaluator_p

SOURCE_CONTEXT = {
    "source_repository": "SYNTHETIC/AAD_SHAPE",
    "source_version": "AAD_PREFRESH_V1",
    "population_scope": "MODULE_Q_AAD_PREFRESH_SYNTHETIC_V1",
}

PATH = "synthetic/aad-shape.xml"

XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="aad_synth_0001">
  <teiHeader>
    <fileDesc>
      <titleStmt><title>AAD synthetic shape</title></titleStmt>
      <publicationStmt><p>synthetic</p></publicationStmt>
      <sourceDesc>
        <msDesc>
          <msIdentifier><repository>SYNTHETIC</repository><idno>0001</idno></msIdentifier>
          <history>
            <origin>
              <origDate notBefore-iso="1950-01-03T00:00:00+00:00"
                        notAfter-iso="1950-01-03T23:59:59+00:00"/>
            </origin>
          </history>
        </msDesc>
      </sourceDesc>
    </fileDesc>
    <profileDesc>
      <correspDesc>
        <correspAction type="sent">
          <persName>Sender A</persName>
          <date when-iso="1950-01-01T12:00:00+00:00">1 January 1950</date>
        </correspAction>
        <correspAction type="received">
          <persName>Receiver B</persName>
        </correspAction>
      </correspDesc>
    </profileDesc>
  </teiHeader>
  <text>
    <body>
      <div type="transcription" xml:id="transcription_aad_synth_0001">
        <div type="letter" xml:id="letter_aad_synth_0001">
          <div type="letter_message">
            <opener>
              <dateline><date when-iso="1950-01-01T12:00:00+00:00">1 January 1950</date></dateline>
            </opener>
            <p>Synthetic message.</p>
          </div>
        </div>
      </div>
    </body>
  </text>
</TEI>
"""


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    odoc = oracle_p.parse_document(PATH, XML, SOURCE_CONTEXT)
    rdoc = runtime_p.parse_document(PATH, XML, SOURCE_CONTEXT)

    require(odoc["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT", odoc["object_contract"])
    require(rdoc["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT", rdoc["object_contract"])
    require(odoc["object_contract"]["boundary_kind"] == "EXPLICIT_LETTER_DIV", odoc["object_contract"])
    require(rdoc["object_contract"]["boundary_kind"] == "EXPLICIT_LETTER_DIV", rdoc["object_contract"])

    require(odoc["origin_contract_status"] == "SINGLE_ORIGIN_ADMISSIBLE", odoc["origin_contract_status"])
    require(rdoc["origin_contract_status"] == "SINGLE_ORIGIN_ADMISSIBLE", rdoc["origin_contract_status"])

    require(odoc["p_disposition"] == "ERIR_ELIGIBLE", odoc["p_disposition"])
    require(rdoc["p_disposition"] == "ERIR_ELIGIBLE", rdoc["p_disposition"])
    require(odoc["p_warrant_before"] != odoc["p_warrant_after"], {
        "before": odoc["p_warrant_before"],
        "after": odoc["p_warrant_after"],
    })
    require(rdoc["p_warrant_before"] == odoc["p_warrant_before"], {
        "oracle": odoc["p_warrant_before"],
        "runtime": rdoc["p_warrant_before"],
    })
    require(rdoc["p_warrant_after"] == odoc["p_warrant_after"], {
        "oracle": odoc["p_warrant_after"],
        "runtime": rdoc["p_warrant_after"],
    })
    require(rdoc["p_transition_class"] == odoc["p_transition_class"], {
        "oracle": odoc["p_transition_class"],
        "runtime": rdoc["p_transition_class"],
    })

    trace = runtime_p.execute(rdoc)
    ev = evaluator_p.evaluate(trace, odoc, rdoc)
    require(ev["reference_end_to_end_pass"], ev)

    wrong_object = runtime_p.execute(rdoc, fault={"type": "wrong_object"})
    wrong_source = runtime_p.execute(rdoc, fault={"type": "wrong_source_version"})
    missing_app = runtime_p.execute(rdoc, fault={"type": "missing_applicability"})
    collateral = runtime_p.execute(rdoc, fault={"type": "collateral_mutation"})
    no_history = runtime_p.execute(rdoc, drop_history=True)

    collateral_eval = evaluator_p.evaluate(collateral, odoc, rdoc)
    no_history_eval = evaluator_p.evaluate(no_history, odoc, rdoc)

    controls = {
        "wrong_object_rejected": not wrong_object["origin_transition"]["applicable"],
        "wrong_source_version_rejected": not wrong_source["origin_transition"]["applicable"],
        "missing_applicability_rejected": not missing_app["origin_transition"]["applicable"],
        "collateral_mutation_detected": (
            collateral_eval["P2_EVENT_APPLICABILITY"]
            and not collateral_eval["P4_SELECTIVE_UPDATE"]
            and bool(collateral["collateral_temporal_paths"])
        ),
        "history_drop_detected": (
            no_history_eval["P3_POST_EVENT_RESULT"]
            and no_history_eval["P4_SELECTIVE_UPDATE"]
            and no_history_eval["P5_PROVENANCE"]
            and no_history_eval["P6_TRANSITION_ATTRIBUTION"]
            and not no_history_eval["P7_DELAYED_HISTORY"]
        ),
    }
    require(all(controls.values()), controls)

    result = {
        "study": "MODULE_Q_AAD_PREFRESH_SYNTHETIC_V1",
        "aad_real_episode_opened": False,
        "object_status": odoc["object_contract"]["status"],
        "boundary_kind": odoc["object_contract"]["boundary_kind"],
        "origin_contract_status": odoc["origin_contract_status"],
        "p_disposition": odoc["p_disposition"],
        "p_transition_class": odoc["p_transition_class"],
        "p_warrant_before": odoc["p_warrant_before"],
        "p_warrant_after": odoc["p_warrant_after"],
        "reference_capabilities": {
            k: v for k, v in ev.items() if k.startswith("P")
        },
        "controls": controls,
        "overall": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
