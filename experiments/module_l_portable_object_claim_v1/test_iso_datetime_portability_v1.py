from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import evaluator_l
import oracle_l
import runtime_l
from test_portable_contract_v1 import CTX, DIRECT_EXPLICIT


ISO_DOCUMENT = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem>
    <docDate when-iso="1900-01-01T23:30:00-05:00">encoded local day</docDate>
   </msItem></msContents>
   <history><origin>
    <origDate notBefore-iso="1900-01-02T00:00:00+01:00"
              notAfter-iso="1900-01-04T23:59:59+01:00">2-4 Jan 1900</origDate>
   </origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent">
   <date when-iso="1900-01-03T00:00:00Z">3 Jan 1900</date>
  </correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="letter">
   <opener><dateline>
    <date when="1900-01-01">1 Jan 1900</date>
   </dateline><salute>Dear A,</salute></opener>
   <p>Primary letter.</p>
   <closer><signed>B.</signed></closer>
  </div>
 </body></text>
</TEI>"""


INVALID_ISO_DOCUMENT = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc><sourceDesc><msDesc>
   <msContents><msItem>
    <docDate when-iso="1900-13-40T25:61:61+99:99">invalid</docDate>
   </msItem></msContents>
   <history><origin><origDate when="1900-01-02"/></origin></history>
  </msDesc></sourceDesc></fileDesc>
  <profileDesc><correspDesc><correspAction type="sent">
   <date when="1900-01-03"/>
  </correspAction></correspDesc></profileDesc>
 </teiHeader>
 <text><body>
  <div type="letter">
   <opener><dateline><date when="1900-01-01"/></dateline></opener>
   <p>Primary letter.</p>
  </div>
 </body></text>
</TEI>"""


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def by_role(doc, role):
    return [c for c in doc.get("claims", []) if c.get("role") == role]


def main():
    results = {}

    oracle = oracle_l.parse_document("SYNTHETIC/iso.xml", ISO_DOCUMENT, CTX)
    runtime = runtime_l.parse_document("SYNTHETIC/iso.xml", ISO_DOCUMENT, CTX)

    # F31: local date must be retained. 23:30 at -05:00 would be Jan 2 in UTC.
    odoc = by_role(oracle, "docDate")
    rdoc = by_role(runtime, "docDate")
    results["F31_ISO_DATETIME_EXACT_LOCAL_DAY"] = all([
        len(odoc) == len(rdoc) == 1,
        odoc[0]["interval"] == ["1900-01-01", "1900-01-01"],
        rdoc[0]["interval"] == ["1900-01-01", "1900-01-01"],
    ])
    require(results["F31_ISO_DATETIME_EXACT_LOCAL_DAY"], {
        "oracle": odoc,
        "runtime": rdoc,
    })

    # F32: Z datetime is accepted as the encoded UTC calendar day.
    osent = by_role(oracle, "sent")
    rsent = by_role(runtime, "sent")
    results["F32_ISO_DATETIME_Z_EXACT_LOCAL_DAY"] = all([
        len(osent) == len(rsent) == 1,
        osent[0]["interval"] == ["1900-01-03", "1900-01-03"],
        rsent[0]["interval"] == ["1900-01-03", "1900-01-03"],
    ])
    require(results["F32_ISO_DATETIME_Z_EXACT_LOCAL_DAY"], {
        "oracle": osent,
        "runtime": rsent,
    })

    # F33: bounded offset datetime range maps to inclusive local calendar days.
    oo = oracle.get("origin_claim")
    ro = runtime.get("origin_claim")
    results["F33_ISO_DATETIME_BOUNDED_RANGE"] = all([
        oo is not None,
        ro is not None,
        oo["interval"] == ["1900-01-02", "1900-01-04"],
        ro["interval"] == ["1900-01-02", "1900-01-04"],
        oo["status"] == ro["status"] == "BOUNDED",
    ])
    require(results["F33_ISO_DATETIME_BOUNDED_RANGE"], {
        "oracle": oo,
        "runtime": ro,
    })

    # F34: original lexical source attributes survive and oracle/runtime claim identity agrees.
    expected_doc_attr = "1900-01-01T23:30:00-05:00"
    expected_lo = "1900-01-02T00:00:00+01:00"
    expected_hi = "1900-01-04T23:59:59+01:00"
    results["F34_ISO_DATETIME_RAW_ATTRS_PRESERVED"] = all([
        odoc[0]["raw_attrs"].get("when-iso") == expected_doc_attr,
        rdoc[0]["raw_attrs"].get("when-iso") == expected_doc_attr,
        oo["raw_attrs"].get("notBefore-iso") == expected_lo,
        ro["raw_attrs"].get("notBefore-iso") == expected_lo,
        oo["raw_attrs"].get("notAfter-iso") == expected_hi,
        ro["raw_attrs"].get("notAfter-iso") == expected_hi,
        odoc[0]["claim_key"] == rdoc[0]["claim_key"],
        osent[0]["claim_key"] == rsent[0]["claim_key"],
        oo["claim_key"] == ro["claim_key"],
    ])
    require(results["F34_ISO_DATETIME_RAW_ATTRS_PRESERVED"], {
        "oracle_doc": odoc,
        "runtime_doc": rdoc,
        "oracle_origin": oo,
        "runtime_origin": ro,
    })

    # F35: malformed datetime remains non-machine-readable.
    oi = oracle_l.parse_document(
        "SYNTHETIC/invalid_iso.xml", INVALID_ISO_DOCUMENT, CTX
    )
    ri = runtime_l.parse_document(
        "SYNTHETIC/invalid_iso.xml", INVALID_ISO_DOCUMENT, CTX
    )
    oidoc = by_role(oi, "docDate")
    ridoc = by_role(ri, "docDate")
    results["F35_ISO_DATETIME_INVALID_REJECTED"] = all([
        len(oidoc) == len(ridoc) == 1,
        oidoc[0]["interval"] is None,
        ridoc[0]["interval"] is None,
        oidoc[0]["status"] == ridoc[0]["status"] == "MISSING",
    ])
    require(results["F35_ISO_DATETIME_INVALID_REJECTED"], {
        "oracle": oidoc,
        "runtime": ridoc,
    })

    # F36: the existing date-only full trajectory keeps its exact semantics and passes.
    legacy_o = oracle_l.parse_document(
        "SYNTHETIC/legacy_direct.xml", DIRECT_EXPLICIT, CTX
    )
    legacy_r = runtime_l.parse_document(
        "SYNTHETIC/legacy_direct.xml", DIRECT_EXPLICIT, CTX
    )
    legacy_trace = runtime_l.execute(legacy_r, "I_RSTAR")
    legacy_eval = evaluator_l.evaluate_trace(legacy_trace, legacy_o, legacy_r)

    results["F36_LEGACY_DATE_SEMANTICS_UNCHANGED"] = all([
        legacy_o["full_trajectory_eligible"],
        legacy_r["full_trajectory_eligible"],
        legacy_o["warrant_root"] == legacy_r["warrant_root"],
        legacy_o["warrant_after"] == legacy_r["warrant_after"],
        legacy_eval["end_to_end_pass"],
    ])
    require(results["F36_LEGACY_DATE_SEMANTICS_UNCHANGED"], {
        "oracle": legacy_o,
        "runtime": legacy_r,
        "evaluation": legacy_eval,
    })

    print({
        "study": "PORTABLE_ISO_DATETIME_CONTROLS_V1",
        "results": results,
        "all_iso_datetime_controls_passed": all(results.values()),
    })


if __name__ == "__main__":
    main()
