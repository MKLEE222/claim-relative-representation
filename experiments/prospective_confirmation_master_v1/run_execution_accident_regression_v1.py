from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FP = ROOT / "experiments" / "formalization_papers_qualified_composition_v1"
if str(FP) not in sys.path:
    sys.path.insert(0, str(FP))

import fp_oracle
import fp_runtime


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def formalization_regression_fixture() -> bytes:
    # Covers the two natural RDF surfaces that escaped the original
    # pre-fresh synthetic gate: fractional xsd:dateTime lexical form and
    # genuinely multi-valued dct:creator.
    return b"""@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix frbr: <http://purl.org/vocab/frbr/core#> .
@prefix pso: <http://purl.org/spar/pso/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://example.org/> .

ex:np1 a np:Nanopublication ;
    np:hasAssertion ex:np1-assertion ;
    np:hasPublicationInfo ex:np1-pubinfo .

ex:np1-assertion {
    ex:formalization-1 frbr:partOf <https://w3id.org/linkflows/formalization-papers/DataScienceSpecialIssue> ;
        pso:withStatus pso:submitted .
}

ex:np1-pubinfo {
    ex:np1 dct:creator ex:creator-a ;
        dct:creator ex:creator-b ;
        dct:created "2021-01-01T00:00:00.123456Z"^^xsd:dateTime .
}
"""


def main():
    raw = formalization_regression_fixture()
    o = fp_oracle.parse_trig(raw)
    r = fp_runtime.parse_trig(raw)

    require(o == r, {"oracle": o, "runtime": r})
    require(len(o["creators"]) == 2, o["creators"])
    require(len(o["created"]) == 1, o["created"])
    require(o["created"][0][1].endswith("+00:00"), o["created"])
    require(".123456" in o["created"][0][1], o["created"])
    require(len(o["roots"]) == 1, o["roots"])

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "study": "PROSPECTIVE_CONFIRMATION_EXECUTION_ACCIDENT_REGRESSION_V1",
        "formalization_known_failures": {
            "fractional_datetime_surface": "PASS",
            "multi_valued_creator_surface": "PASS",
            "independent_parser_exactness": "PASS",
            "root_surface": "PASS",
        },
        "fixture_sha256": sha256(raw),
        "oracle_surface": o,
        "runtime_surface": r,
        "overall": "PASS",
    }
    out = out_dir / "execution_accident_regression_v1.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "files": {
            out.name: sha256(out.read_bytes()),
        }
    }
    (out_dir / "artifact_manifest_v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
