from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_oracle
import fp_runtime


PFX = """@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://example.org/cardinality/> .
"""


def fixture(two_creators=True):
    creator_obj = (
        "ex:creatorA, ex:creatorB"
        if two_creators
        else "ex:creatorA"
    )
    return (
        PFX
        + """
ex:np1 a np:Nanopublication ;
    np:hasAssertion ex:a1 ;
    np:hasPublicationInfo ex:i1 .

ex:a1 {
    ex:s ex:p ex:o .
}

ex:i1 {
    ex:np1 dct:creator """
        + creator_obj
        + """ ;
        dct:created "2021-11-17T21:41:33.173+02:00"^^xsd:dateTime .
}
"""
    ).encode("utf-8")


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def norm(x):
    return json.loads(json.dumps(x, sort_keys=True))


def main():
    raw_multi = fixture(two_creators=True)
    o_multi = fp_oracle.parse_trig(raw_multi)
    r_multi = fp_runtime.parse_trig(raw_multi)

    require(norm(o_multi) == norm(r_multi), {
        "oracle": o_multi,
        "runtime": r_multi,
    })

    expected_multi = [
        [
            "https://example.org/cardinality/np1",
            "https://example.org/cardinality/creatorA",
        ],
        [
            "https://example.org/cardinality/np1",
            "https://example.org/cardinality/creatorB",
        ],
    ]
    require(o_multi["creators"] == expected_multi, o_multi)

    raw_single = fixture(two_creators=False)
    o_single = fp_oracle.parse_trig(raw_single)
    r_single = fp_runtime.parse_trig(raw_single)
    require(norm(o_single) == norm(r_single), {
        "oracle": o_single,
        "runtime": r_single,
    })
    require(
        o_single["creators"]
        == [[
            "https://example.org/cardinality/np1",
            "https://example.org/cardinality/creatorA",
        ]],
        o_single,
    )

    require(
        len(o_multi["created"]) == 1
        and len(o_single["created"]) == 1,
        {"multi": o_multi, "single": o_single},
    )

    result = {
        "study": "FORMALIZATION_PAPERS_CREATOR_CARDINALITY_REGRESSION_V2",
        "multi_creator_relation_count": len(
            o_multi["creators"]
        ),
        "single_creator_relation_count": len(
            o_single["creators"]
        ),
        "no_primary_creator_selected": True,
        "oracle_runtime_exact": True,
        "overall": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
