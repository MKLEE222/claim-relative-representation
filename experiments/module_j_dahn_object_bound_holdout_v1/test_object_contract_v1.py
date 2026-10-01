from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import oracle_j
import runtime_j
import evaluator_j

SINGLE = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem><docDate when="1900-01-01">1 Jan 1900</docDate></msItem></msContents>
   <history><origin><p xml:lang="en"><origDate when="1900-01-02">2 Jan 1900</origDate></p></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1900-01-03">3 Jan 1900</date></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body><div type="transcription">
   <div type="letter"><opener><dateline><date when="1900-01-01">1 Jan 1900</date></dateline></opener><p>Primary.</p></div>
   <div type="annex"><div type="letter"><opener><dateline><date when="1905-01-01">1 Jan 1905</date></dateline></opener></div></div>
 </div></body></text>
</TEI>"""

NO_PRIMARY = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc><msContents><msItem><docDate when="1832">1832</docDate></msItem></msContents></msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent">
    <date when="1832-01-01">1832</date><date when="1849-01-01">1849</date>
  </correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body><p>Aggregate correspondence extracts; no letter object.</p></body></text>
</TEI>"""

MULTIPLE = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc><msContents><msItem><docDate when="1900">1900</docDate></msItem></msContents></msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1900-01-01">1900</date></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body><div type="transcription">
   <div type="letter"><opener><dateline><date when="1900-01-02">2 Jan</date></dateline></opener><p>Letter A.</p></div>
   <div type="letter"><opener><dateline><date when="1901-01-02">2 Jan 1901</date></dateline></opener><p>Letter B.</p></div>
 </div></body></text>
</TEI>"""

DIRECT_TRANSCRIPTION = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem><docDate when="1804-01-01">1 Jan 1804</docDate></msItem></msContents>
   <history><origin><p xml:lang="en"><origDate when="1804-01-02">2 Jan 1804</origDate></p></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1804-01-03">3 Jan 1804</date></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body><div type="transcription">
   <opener><dateline><date when="1804-01-01">1 Jan 1804</date></dateline></opener>
   <p>Direct transcription letter content.</p>
 </div></body></text>
</TEI>"""

TWO_TRANSCRIPTIONS = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc><msContents><msItem><docDate when="1900">1900</docDate></msItem></msContents></msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1900-01-01">1900</date></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="transcription"><p>Document A.</p></div>
  <div type="transcription"><p>Document B.</p></div>
 </body></text>
</TEI>"""


UNTYPED_LETTER = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem><docDate when="1810-01-01">1 Jan 1810</docDate></msItem></msContents>
   <history><origin><p xml:lang="en"><origDate when="1810-01-02">2 Jan 1810</origDate></p></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent"><date when="1810-01-03">3 Jan 1810</date></correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
   <div>
     <opener><salute>Dear friend,</salute><dateline><date when="1810-01-01">1 Jan 1810</date></dateline></opener>
     <p>Untyped body letter.</p>
     <closer><signed>A.</signed></closer>
   </div>
 </body></text>
</TEI>"""

UNTYPED_PLACEHOLDER = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc><msContents><msItem><docDate when="1832">1832</docDate></msItem></msContents></msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent">
    <date when="1832-01-01">1832</date><date when="1849-01-01">1849</date>
  </correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body><div><p>[Transcription to come - See metadata]</p></div></body></text>
</TEI>"""


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def main():
    detections = {}

    # Baseline single scholarly object.
    o = oracle_j.parse_document("SYNTHETIC/single.xml", SINGLE)
    r = runtime_j.parse_document("SYNTHETIC/single.xml", SINGLE)
    require(o["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT", o["object_contract"])
    require(r["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT", r["object_contract"])
    require(o["object_id"] == r["object_id"], "independent object IDs disagree")
    require(o["full_trajectory_eligible"], o["full_trajectory_exclusion_reasons"])
    trace = runtime_j.execute(r, "I_RSTAR")
    ev = evaluator_j.evaluate_trace(trace, o, r)
    require(ev["end_to_end_pass"], ev)

    # F10: aggregate metadata with two sent dates but no letter object.
    o10 = oracle_j.parse_document("SYNTHETIC/no_primary.xml", NO_PRIMARY)
    r10 = runtime_j.parse_document("SYNTHETIC/no_primary.xml", NO_PRIMARY)
    detections["F10_AGGREGATE_WITHOUT_PRIMARY_REJECTED"] = all([
        o10["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        r10["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        not o10["eligibility"]["eligible"],
        o10["expected_question"] is None,
        runtime_j.discover(r10["claims"], expected_object_id=r10.get("object_id")) is None,
    ])
    require(detections["F10_AGGREGATE_WITHOUT_PRIMARY_REJECTED"], {
        "oracle": o10["object_contract"],
        "runtime": r10["object_contract"],
        "eligibility": o10["eligibility"],
    })

    # F11: multiple sibling primary letters must not silently select the first.
    o11 = oracle_j.parse_document("SYNTHETIC/multiple.xml", MULTIPLE)
    r11 = runtime_j.parse_document("SYNTHETIC/multiple.xml", MULTIPLE)
    detections["F11_MULTIPLE_PRIMARY_REJECTED"] = all([
        o11["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        r11["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        o11["object_contract"]["candidate_count"] == 2,
        r11["object_contract"]["candidate_count"] == 2,
        not o11["eligibility"]["eligible"],
        runtime_j.discover(r11["claims"], expected_object_id=r11.get("object_id")) is None,
    ])
    require(detections["F11_MULTIPLE_PRIMARY_REJECTED"], {
        "oracle": o11["object_contract"],
        "runtime": r11["object_contract"],
    })

    # F12: cross-object claim injection must break discovery/object contract.
    r12 = runtime_j.parse_document("SYNTHETIC/single.xml", SINGLE, fault="cross_object_claim")
    t12 = runtime_j.execute(r12, "I_RSTAR")
    e12 = evaluator_j.evaluate_trace(t12, o, r12)
    detections["F12_CROSS_OBJECT_INJECTION_DETECTED"] = (
        not e12["object_claim_binding_exact"]
        and not e12["end_to_end_pass"]
    )
    require(detections["F12_CROSS_OBJECT_INJECTION_DETECTED"], e12)

    # F13 positive contract control: direct transcription can itself be one letter object.
    o13 = oracle_j.parse_document("SYNTHETIC/direct.xml", DIRECT_TRANSCRIPTION)
    r13 = runtime_j.parse_document("SYNTHETIC/direct.xml", DIRECT_TRANSCRIPTION)
    detections["F13_TRANSCRIPTION_AS_LETTER_ACCEPTED"] = all([
        o13["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        r13["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        o13["object_contract"]["boundary_kind"] == "TRANSCRIPTION_AS_LETTER",
        r13["object_contract"]["boundary_kind"] == "TRANSCRIPTION_AS_LETTER",
        o13["object_id"] == r13["object_id"],
    ])
    require(detections["F13_TRANSCRIPTION_AS_LETTER_ACCEPTED"], {
        "oracle": o13["object_contract"],
        "runtime": r13["object_contract"],
    })

    # F14: multiple transcription containers cannot be silently collapsed.
    o14 = oracle_j.parse_document("SYNTHETIC/two_transcriptions.xml", TWO_TRANSCRIPTIONS)
    r14 = runtime_j.parse_document("SYNTHETIC/two_transcriptions.xml", TWO_TRANSCRIPTIONS)
    detections["F14_MULTIPLE_TRANSCRIPTIONS_REJECTED"] = all([
        o14["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        r14["object_contract"]["status"] == "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
        o14["object_contract"]["candidate_count"] == 2,
        r14["object_contract"]["candidate_count"] == 2,
        not o14["eligibility"]["eligible"],
    ])
    require(detections["F14_MULTIPLE_TRANSCRIPTIONS_REJECTED"], {
        "oracle": o14["object_contract"],
        "runtime": r14["object_contract"],
    })


    # F15: one untyped body letter with letter-specific structure is a valid single object.
    o15 = oracle_j.parse_document("SYNTHETIC/untyped_letter.xml", UNTYPED_LETTER)
    r15 = runtime_j.parse_document("SYNTHETIC/untyped_letter.xml", UNTYPED_LETTER)
    detections["F15_UNTYPED_BODY_LETTER_ACCEPTED"] = all([
        o15["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        r15["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        o15["object_contract"]["boundary_kind"] == "UNTYPED_BODY_LETTER",
        r15["object_contract"]["boundary_kind"] == "UNTYPED_BODY_LETTER",
        o15["object_id"] == r15["object_id"],
    ])
    require(detections["F15_UNTYPED_BODY_LETTER_ACCEPTED"], {
        "oracle": o15["object_contract"],
        "runtime": r15["object_contract"],
    })

    # F16: metadata plus placeholder body is not a scholarly letter object.
    o16 = oracle_j.parse_document("SYNTHETIC/untyped_placeholder.xml", UNTYPED_PLACEHOLDER)
    r16 = runtime_j.parse_document("SYNTHETIC/untyped_placeholder.xml", UNTYPED_PLACEHOLDER)
    detections["F16_PLACEHOLDER_NOT_OBJECT"] = all([
        o16["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        r16["object_contract"]["status"] == "NO_PRIMARY_DOCUMENT_OBJECT",
        not o16["eligibility"]["eligible"],
        o16["expected_question"] is None,
        runtime_j.discover(r16["claims"], expected_object_id=r16.get("object_id")) is None,
    ])
    require(detections["F16_PLACEHOLDER_NOT_OBJECT"], {
        "oracle": o16["object_contract"],
        "runtime": r16["object_contract"],
        "eligibility": o16["eligibility"],
    })

    # Annex remains excluded from the single primary object.
    annex_interval = ["1905-01-01", "1905-01-01"]
    detections["ANNEX_EXCLUDED"] = all(
        c.get("interval") != annex_interval for c in o["claims"]
    )
    require(detections["ANNEX_EXCLUDED"], o["claims"])

    print({
        "baseline_end_to_end": ev["end_to_end_pass"],
        "fault_detection": detections,
        "all_object_faults_detected": all(detections.values()),
    })


if __name__ == "__main__":
    main()
