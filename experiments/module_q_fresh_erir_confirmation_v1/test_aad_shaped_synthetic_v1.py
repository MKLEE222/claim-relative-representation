from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
P_DIR = HERE.parent / "module_p_evidence_release_revision_v1"
for p in (L_DIR, P_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import oracle_l
import runtime_l
import oracle_p
import runtime_p
import evaluator_p

SOURCE_CONTEXT = {
    "source_repository": "SYNTHETIC_AAD_SHAPE",
    "source_version": "pre-fresh-v1",
    "population_scope": "MODULE_Q_AAD_SHAPED_SYNTHETIC_V1",
}


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def fixture(origin_day: str) -> bytes:
    # All names, identifiers, prose and dates are synthetic.
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="aad-synthetic-0001">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>synthetic AAD-shaped correspondence object</title>
      </titleStmt>
      <publicationStmt>
        <p>synthetic pre-fresh fixture</p>
      </publicationStmt>
      <sourceDesc>
        <listWit>
          <witness xml:id="synthetic-witness">
            <msDesc>
              <msIdentifier>
                <repository>synthetic repository</repository>
              </msIdentifier>
              <history>
                <origin>
                  <origDate
                    notBefore-iso="{origin_day}T00:00:00+00:00"
                    notAfter-iso="{origin_day}T00:00:00+00:00">synthetic origin date</origDate>
                  <origPlace>synthetic place</origPlace>
                </origin>
              </history>
            </msDesc>
          </witness>
        </listWit>
      </sourceDesc>
    </fileDesc>
    <profileDesc>
      <correspDesc>
        <correspAction type="sent">
          <persName>synthetic sender</persName>
          <placeName>synthetic origin place</placeName>
          <date
            notBefore-iso="1900-01-01T00:00:00+00:00"
            notAfter-iso="1900-01-01T00:00:00+00:00">synthetic sent date</date>
        </correspAction>
        <correspAction type="received">
          <persName>synthetic recipient</persName>
        </correspAction>
      </correspDesc>
    </profileDesc>
    <revisionDesc status="draft">
      <change when-iso="2026-01-01">synthetic fixture only</change>
    </revisionDesc>
  </teiHeader>

  <text>
    <body>
      <div type="transcription" xml:id="transcription_aad_synthetic_0001">
        <div type="letter" xml:id="letter_aad_synthetic_0001">
          <div type="letter_message">
            <opener>
              <dateline>synthetic manuscript dateline without machine attributes</dateline>
              <salute>Dear synthetic recipient,</salute>
            </opener>
            <p>This prose is fabricated and contains no AAD episode content.</p>
            <closer>
              <signed>synthetic sender</signed>
            </closer>
          </div>
        </div>

        <div type="envelope" xml:id="envelope_aad_synthetic_0001">
          <p>
            Synthetic envelope-side date:
            <date when="1999-12-31">31 December 1999</date>
          </p>
        </div>
      </div>
    </body>
  </text>
</TEI>
"""
    return xml.encode("utf-8")


def contract_summary(doc):
    return {
        "object_status": (doc.get("object_contract") or {}).get("status"),
        "boundary_kind": (doc.get("object_contract") or {}).get("boundary_kind"),
        "object_id": doc.get("object_id"),
        "origin_status": doc.get("origin_contract_status"),
        "origin_count": doc.get("origin_element_count"),
        "p_disposition": doc.get("p_disposition"),
        "p_transition_class": doc.get("p_transition_class"),
        "phi_before": doc.get("p_warrant_before"),
        "phi_after": doc.get("p_warrant_after"),
    }


def main():
    positive_raw = fixture("1900-01-02")
    null_raw = fixture("1900-01-01")

    op = oracle_p.parse_document(
        "synthetic/aad-shaped-positive.xml",
        positive_raw,
        SOURCE_CONTEXT,
    )
    rp = runtime_p.parse_document(
        "synthetic/aad-shaped-positive.xml",
        positive_raw,
        SOURCE_CONTEXT,
    )

    require(
        (op.get("object_contract") or {}).get("status")
        == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        contract_summary(op),
    )
    require(
        (op.get("object_contract") or {}).get("boundary_kind")
        == "EXPLICIT_LETTER_DIV",
        contract_summary(op),
    )
    require(
        op.get("origin_contract_status") == "SINGLE_ORIGIN_ADMISSIBLE",
        contract_summary(op),
    )
    require(op.get("origin_element_count") == 1, contract_summary(op))
    require(op.get("p_erir_eligible") is True, contract_summary(op))
    require(op.get("p_disposition") == "ERIR_ELIGIBLE", contract_summary(op))
    require(
        op.get("p_transition_class") == "P-U1_CONFLICT_FORMATION",
        contract_summary(op),
    )

    require(
        contract_summary(op) == contract_summary(rp),
        {"oracle": contract_summary(op), "runtime": contract_summary(rp)},
    )

    # The synthetic envelope-side machine date must not become an active root claim.
    root_roles = [x.get("role") for x in op.get("claims") or []]
    require(root_roles == ["sent"], {"active_root_roles": root_roles})

    excluded = op.get("excluded_temporal_claims") or []
    require(
        any(
            x.get("raw_attrs", {}).get("when") == "1999-12-31"
            for x in excluded
        ),
        {"excluded_temporal_claims": excluded},
    )

    trace = runtime_p.execute(rp)
    ev = evaluator_p.evaluate(trace, op, rp)
    require(ev.get("reference_end_to_end_pass") is True, ev)

    on = oracle_p.parse_document(
        "synthetic/aad-shaped-null.xml",
        null_raw,
        SOURCE_CONTEXT,
    )
    rn = runtime_p.parse_document(
        "synthetic/aad-shaped-null.xml",
        null_raw,
        SOURCE_CONTEXT,
    )

    require(
        on.get("p_disposition") == "ADMISSIBLE_NULL_EVENT",
        contract_summary(on),
    )
    require(on.get("p_erir_eligible") is False, contract_summary(on))
    require(on.get("p_admissible_null_event") is True, contract_summary(on))
    require(
        on.get("p_transition_class") == "ADMISSIBLE_NULL_EVENT",
        contract_summary(on),
    )
    require(
        contract_summary(on) == contract_summary(rn),
        {"oracle": contract_summary(on), "runtime": contract_summary(rn)},
    )

    print(json.dumps({
        "study": "MODULE_Q_AAD_SHAPED_SYNTHETIC_GATE_V1",
        "uses_real_aad_episode_content": False,
        "positive": {
            "contract": contract_summary(op),
            "P1_P7": {
                k: ev[k]
                for k in (
                    "P1_CURRENT_STATE_BEFORE",
                    "P2_EVENT_APPLICABILITY",
                    "P3_POST_EVENT_RESULT",
                    "P4_SELECTIVE_UPDATE",
                    "P5_PROVENANCE",
                    "P6_TRANSITION_ATTRIBUTION",
                    "P7_DELAYED_HISTORY",
                )
            },
            "reference_end_to_end_pass": ev["reference_end_to_end_pass"],
            "active_root_roles": root_roles,
            "excluded_sibling_date_detected": True,
        },
        "null": {
            "contract": contract_summary(on),
            "admissible_null_preserved": True,
        },
        "gate_pass": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
