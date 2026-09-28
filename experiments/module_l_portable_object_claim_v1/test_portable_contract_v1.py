from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import oracle_l
import runtime_l
import evaluator_l

CTX = {
    "source_repository": "SYNTHETIC/PORTABLE",
    "source_version": "portable-v1",
    "population_scope": "synthetic-controls",
}

DIRECT_EXPLICIT = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem><docDate when="1900-01-01">1 Jan 1900</docDate></msItem></msContents>
   <history><origin><p xml:lang="en"><origDate when="1900-01-02">2 Jan 1900</origDate></p></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent">
   <date when="1900-01-03">3 Jan 1900</date>
  </correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="letter">
   <opener><dateline><date when="1900-01-01">1 Jan 1900</date></dateline><salute>Dear A,</salute></opener>
   <p>Primary letter.</p>
   <closer><signed>B.</signed></closer>
  </div>
 </body></text>
</TEI>"""

TYPED_NONLETTER = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc><msContents><msItem><docDate when="1900"/></msItem></msContents></msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1900-01-03"/></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="section"><opener><dateline><date when="1900-01-01"/></dateline></opener><p>Not a frozen letter route.</p></div>
 </body></text>
</TEI>"""

SIBLING_DATE = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem><docDate when="1900-01-01"/></msItem></msContents>
   <history><origin><p xml:lang="en"><origDate when="1900-01-02"/></p></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1900-01-03"/></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="letter">
   <opener><dateline><date when="1900-01-01"/></dateline></opener>
   <p>Primary letter.</p>
  </div>
  <div type="address"><p>Address annotation <date when="2099-12-31">future diagnostic date</date></p></div>
 </body></text>
</TEI>"""

MULTIPLE_DIRECT = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc><msContents><msItem><docDate when="1900"/></msItem></msContents></msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1900-01-03"/></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="letter"><opener><dateline><date when="1900-01-01"/></dateline></opener><p>A</p></div>
  <div type="letter"><opener><dateline><date when="1901-01-01"/></dateline></opener><p>B</p></div>
 </body></text>
</TEI>"""


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def main():
    results = {}

    # F17: direct explicit letter works without transcription wrapper.
    o17 = oracle_l.parse_document("SYNTHETIC/direct.xml", DIRECT_EXPLICIT, CTX)
    r17 = runtime_l.parse_document("SYNTHETIC/direct.xml", DIRECT_EXPLICIT, CTX)
    results["F17_DIRECT_EXPLICIT_LETTER_ACCEPTED"] = all([
        o17["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        r17["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        o17["object_contract"]["boundary_kind"] == "EXPLICIT_LETTER_DIV",
        r17["object_contract"]["boundary_kind"] == "EXPLICIT_LETTER_DIV",
        o17["object_id"] == r17["object_id"],
    ])
    require(results["F17_DIRECT_EXPLICIT_LETTER_ACCEPTED"], {
        "oracle": o17["object_contract"],
        "runtime": r17["object_contract"],
    })

    # The direct dateline must be extracted from the selected L boundary.
    odates = [c for c in o17["claims"] if c["role"] == "dateline"]
    rdates = [c for c in r17["claims"] if c["role"] == "dateline"]
    require(len(odates) == len(rdates) == 1, {"oracle": odates, "runtime": rdates})
    require(
        odates[0]["applicability_class"] == rdates[0]["applicability_class"]
        == "INSIDE_SELECTED_OBJECT_BOUNDARY",
        {"oracle": odates, "runtime": rdates},
    )

    # F18: a typed non-letter direct div must not leak into Route C.
    o18 = oracle_l.parse_document("SYNTHETIC/typed_nonletter.xml", TYPED_NONLETTER, CTX)
    r18 = runtime_l.parse_document("SYNTHETIC/typed_nonletter.xml", TYPED_NONLETTER, CTX)
    results["F18_TYPED_DIV_NOT_ROUTE_C"] = all([
        o18["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        r18["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        o18["object_contract"]["boundary_kind"] is None,
        r18["object_contract"]["boundary_kind"] is None,
    ])
    require(results["F18_TYPED_DIV_NOT_ROUTE_C"], {
        "oracle": o18["object_contract"],
        "runtime": r18["object_contract"],
    })

    # F19: sibling date outside the selected explicit letter never becomes an active claim.
    o19 = oracle_l.parse_document("SYNTHETIC/sibling.xml", SIBLING_DATE, CTX)
    r19 = runtime_l.parse_document("SYNTHETIC/sibling.xml", SIBLING_DATE, CTX)
    forbidden = ["2099-12-31", "2099-12-31"]
    results["F19_OUTSIDE_BOUNDARY_DATE_EXCLUDED"] = all([
        all(c.get("interval") != forbidden for c in o19["claims"]),
        all(c.get("interval") != forbidden for c in r19["claims"]),
        any(
            x.get("applicability_class") == "EXCLUDED_OUTSIDE_SELECTED_OBJECT"
            and x.get("raw_attrs", {}).get("when") == "2099-12-31"
            for x in o19.get("excluded_temporal_claims", [])
        ),
        any(
            x.get("applicability_class") == "EXCLUDED_OUTSIDE_SELECTED_OBJECT"
            and x.get("raw_attrs", {}).get("when") == "2099-12-31"
            for x in r19.get("excluded_temporal_claims", [])
        ),
    ])
    require(results["F19_OUTSIDE_BOUNDARY_DATE_EXCLUDED"], {
        "oracle_claims": o19["claims"],
        "runtime_claims": r19["claims"],
        "oracle_excluded": o19.get("excluded_temporal_claims"),
        "runtime_excluded": r19.get("excluded_temporal_claims"),
    })

    # F20: source context participates in object/evidence binding.
    ctx2 = dict(CTX)
    ctx2["source_version"] = "portable-v2"
    o20b = oracle_l.parse_document("SYNTHETIC/direct.xml", DIRECT_EXPLICIT, ctx2)
    r20b = runtime_l.parse_document("SYNTHETIC/direct.xml", DIRECT_EXPLICIT, ctx2)
    mismatch_trace = runtime_l.execute(r17, "I_RSTAR", fault={"type": "source_context_mismatch"})
    results["F20_SOURCE_CONTEXT_BOUND"] = all([
        o17["object_id"] != o20b["object_id"],
        r17["object_id"] != r20b["object_id"],
        o20b["object_id"] == r20b["object_id"],
        not mismatch_trace["open_origin_applicable"],
    ])
    require(results["F20_SOURCE_CONTEXT_BOUND"], {
        "v1_oracle": o17["object_id"],
        "v2_oracle": o20b["object_id"],
        "mismatch_transition": mismatch_trace["origin_transition"],
    })

    # F21: a direct explicit letter can carry the full frozen dynamic trajectory.
    require(o17["full_trajectory_eligible"], o17["full_trajectory_exclusion_reasons"])
    trace21 = runtime_l.execute(r17, "I_RSTAR")
    ev21 = evaluator_l.evaluate_trace(trace21, o17, r17)
    results["F21_DIRECT_EXPLICIT_FULL_TRAJECTORY"] = ev21["end_to_end_pass"]
    require(results["F21_DIRECT_EXPLICIT_FULL_TRAJECTORY"], ev21)

    # F22: multiple direct explicit letters are rejected; no first-letter fallback.
    o22 = oracle_l.parse_document("SYNTHETIC/multiple_direct.xml", MULTIPLE_DIRECT, CTX)
    r22 = runtime_l.parse_document("SYNTHETIC/multiple_direct.xml", MULTIPLE_DIRECT, CTX)
    results["F22_MULTIPLE_DIRECT_EXPLICIT_REJECTED"] = all([
        o22["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        r22["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        o22["object_contract"]["candidate_count"] == 2,
        r22["object_contract"]["candidate_count"] == 2,
        not o22["eligibility"]["eligible"],
    ])
    require(results["F22_MULTIPLE_DIRECT_EXPLICIT_REJECTED"], {
        "oracle": o22["object_contract"],
        "runtime": r22["object_contract"],
    })

    print({
        "portable_fault_detection": results,
        "all_portable_controls_passed": all(results.values()),
        "direct_full_evaluation": ev21,
    })


if __name__ == "__main__":
    main()
