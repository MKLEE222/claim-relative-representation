from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_constants as C
import fp_oracle
import fp_runtime

PFX = """@prefix np: <http://www.nanopub.org/nschema#> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix lf: <https://w3id.org/linkflows/reviews/> .
@prefix pso: <http://purl.org/spar/pso/> .
@prefix frbr: <http://purl.org/vocab/frbr/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://example.org/fp/> .
"""


def np_block(np_name, a_name, i_name, assertion, pubinfo=""):
    return f"""
ex:{np_name} a np:Nanopublication ;
    np:hasAssertion ex:{a_name} ;
    np:hasPublicationInfo ex:{i_name} .

ex:{a_name} {{
{assertion}
}}

ex:{i_name} {{
    ex:{np_name} dct:creator ex:agent-{np_name} ;
        dct:created "2021-01-01T00:00:00Z"^^xsd:dateTime .
{pubinfo}
}}
"""


def fixture(
    include_review=True,
    include_update=True,
    include_response=True,
    include_decision=True,
    response_review="npR",
    response_update="npU",
    decision_update="npU",
    superseded_review=False,
    retract_response=False,
    cross_root=False,
    duplicate_review_targets=False,
):
    parts = [PFX]

    parts.append(np_block(
        "npS", "aS", "iS",
        "    ex:F0 frbr:partOf <https://w3id.org/linkflows/formalization-papers/DataScienceSpecialIssue> ;\n"
        "        pso:withStatus pso:submitted ."
    ))

    if cross_root:
        parts.append(np_block(
            "npS2", "aS2", "iS2",
            "    ex:F2 frbr:partOf <https://w3id.org/linkflows/formalization-papers/DataScienceSpecialIssue> ;\n"
            "        pso:withStatus pso:submitted ."
        ))

    if include_review:
        target_lines = "ex:F0"
        if duplicate_review_targets:
            assertion = (
                "    ex:review1 a lf:ReviewComment ;\n"
                "        lf:refersTo ex:F0, ex:F2 ."
            )
        else:
            assertion = (
                "    ex:review1 a lf:ReviewComment ;\n"
                f"        lf:refersTo {target_lines} ."
            )
        parts.append(np_block("npR", "aR", "iR", assertion))

    if superseded_review:
        parts.append(np_block(
            "npR2", "aR2", "iR2",
            "    ex:review2 a lf:ReviewComment ;\n"
            "        lf:refersTo ex:F0 .",
            "    ex:npR2 npx:supersedes ex:npR ."
        ))

    if include_update:
        parts.append(np_block(
            "npU", "aU", "iU",
            "    ex:updateContent dct:creator ex:author .",
            "    ex:npU lf:isUpdateOf ex:F0 ."
        ))

    if include_response:
        rr = "ex:" + response_review
        ru = "ex:" + response_update
        parts.append(np_block(
            "npA", "aA", "iA",
            "    ex:response1 "
            f"lf:isResponseTo {rr} ;\n"
            f"        lf:refersTo {ru} ."
        ))

    if include_decision:
        du = "ex:" + decision_update
        parts.append(np_block(
            "npD", "aD", "iD",
            f"    {du} pso:withStatus pso:accepted-for-publication ."
        ))

    if retract_response:
        parts.append(np_block(
            "npX", "aX", "iX",
            "    ex:retractor npx:retracts ex:npA ."
        ))

    return "".join(parts).encode("utf-8")


def norm(surface):
    return json.loads(json.dumps(surface, sort_keys=True))


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def exact_parse(raw):
    o = fp_oracle.parse_trig(raw)
    r = fp_runtime.parse_trig(raw)
    require(norm(o) == norm(r), {"oracle": o, "runtime": r})
    return o


def iri(local):
    return "https://example.org/fp/" + local


def invoke(engine, state, event):
    fn = getattr(engine, "apply", None)
    if fn is None:
        fn = getattr(engine, "execute")
    return fn(state, event)


def events():
    return {
        "review": {
            "kind": "REVIEW",
            "review_np": iri("npR"),
            "target_formalization": iri("F0"),
        },
        "update": {
            "kind": "UPDATE",
            "update_np": iri("npU"),
            "target_root": iri("F0"),
        },
        "response": {
            "kind": "RESPONSE",
            "response_np": iri("npA"),
            "target_review_np": iri("npR"),
            "target_update_np": iri("npU"),
        },
        "decision": {
            "kind": "DECISION",
            "decision_np": iri("npD"),
            "target_update_np": iri("npU"),
            "status": C.PSO_ACCEPTED,
        },
    }


def run_chain(engine):
    ev = events()
    s0 = engine.initial_state(iri("F0"), iri("npS"))

    review_first = invoke(engine, s0, ev["review"])
    require(review_first["qualified"], review_first)

    response_before_update = invoke(engine, 
        review_first["state"], ev["response"]
    )
    require(
        not response_before_update["qualified"]
        and response_before_update["reason"]
            == "RESPONSE_UPDATE_TARGET_NOT_LIVE",
        response_before_update,
    )

    update = invoke(engine, review_first["state"], ev["update"])
    require(update["qualified"], update)

    full_before_response = update["state"]

    response = invoke(engine, full_before_response, ev["response"])
    require(response["qualified"], response)

    decision = invoke(engine, response["state"], ev["decision"])
    require(decision["qualified"], decision)

    response_at_s0 = invoke(engine, s0, ev["response"])
    require(
        not response_at_s0["qualified"]
        and response_at_s0["reason"]
            == "RESPONSE_REVIEW_TARGET_NOT_LIVE",
        response_at_s0,
    )

    decision_at_s0 = invoke(engine, s0, ev["decision"])
    require(
        not decision_at_s0["qualified"]
        and decision_at_s0["reason"]
            == "DECISION_TARGET_NOT_CURRENT",
        decision_at_s0,
    )

    # Same current update, erased history and live review registration.
    ablated = copy.deepcopy(full_before_response)
    ablated["history"] = []
    ablated["live_reviews"] = []
    require(
        ablated["current_formalization"]
            == full_before_response["current_formalization"],
        {"ablated": ablated, "full": full_before_response},
    )
    response_ablated = invoke(engine, ablated, ev["response"])
    require(
        not response_ablated["qualified"]
        and response_ablated["reason"]
            == "RESPONSE_REVIEW_TARGET_NOT_LIVE",
        response_ablated,
    )

    wrong = copy.deepcopy(ev["response"])
    wrong["target_review_np"] = iri("foreignReview")
    wrong_result = invoke(engine, full_before_response, wrong)
    require(not wrong_result["qualified"], wrong_result)

    return {
        "generators": [
            review_first["generator"],
            update["generator"],
            response["generator"],
            decision["generator"],
        ],
        "response_before_review_rejected": True,
        "response_before_update_rejected": True,
        "history_ablation_rejected": True,
        "decision_before_update_rejected": True,
        "wrong_target_rejected": True,
        "final_state": decision["state"],
    }


def main():
    fixtures = {}

    fixtures["T0_COMPLETE"] = exact_parse(fixture())
    fixtures["T1_NO_DECISION"] = exact_parse(
        fixture(include_decision=False)
    )
    fixtures["REVIEW_ONLY"] = exact_parse(
        fixture(
            include_update=False,
            include_response=False,
            include_decision=False,
        )
    )
    fixtures["UPDATE_WITHOUT_REVIEW"] = exact_parse(
        fixture(
            include_review=False,
            include_response=False,
            include_decision=False,
        )
    )
    fixtures["MISSING_REVIEW_TARGET"] = exact_parse(
        fixture(response_review="missingReview")
    )
    fixtures["MISSING_UPDATE_TARGET"] = exact_parse(
        fixture(response_update="missingUpdate")
    )
    fixtures["WRONG_DECISION_TARGET"] = exact_parse(
        fixture(decision_update="missingUpdate")
    )
    fixtures["SUPERSEDED_REVIEW"] = exact_parse(
        fixture(superseded_review=True)
    )
    fixtures["RETRACTED_RESPONSE"] = exact_parse(
        fixture(retract_response=True)
    )
    fixtures["MULTIPLE_REVIEW_TARGETS"] = exact_parse(
        fixture(cross_root=True, duplicate_review_targets=True)
    )
    fixtures["CROSS_ROOT"] = exact_parse(fixture(cross_root=True))

    # Parser-level registered checks.
    t0 = fixtures["T0_COMPLETE"]
    require(len(t0["roots"]) == 1, t0)
    require(len(t0["reviews"]) == 1, t0)
    require(len(t0["updates"]) == 1, t0)
    require(len(t0["responses"]) == 1, t0)
    require(len(t0["decisions"]) == 1, t0)

    require(
        (iri("npR2"), iri("npR"))
        in fixtures["SUPERSEDED_REVIEW"]["supersedes"],
        fixtures["SUPERSEDED_REVIEW"],
    )
    require(
        any(
            target == iri("npA")
            for _, target in fixtures["RETRACTED_RESPONSE"]["retracts"]
        ),
        fixtures["RETRACTED_RESPONSE"],
    )
    require(
        len(fixtures["MULTIPLE_REVIEW_TARGETS"]["reviews"][0][2]) == 2,
        fixtures["MULTIPLE_REVIEW_TARGETS"],
    )

    o_chain = run_chain(fp_oracle)
    r_chain = run_chain(fp_runtime)
    require(o_chain == r_chain, {"oracle": o_chain, "runtime": r_chain})
    require(
        o_chain["generators"]
        == [
            "RECORD_REVIEW",
            "REPLACE_FORMALIZATION",
            "RECORD_RESPONSE",
            "REVISE_PUBLICATION_STATUS",
        ],
        o_chain,
    )

    # Explicit retraction discipline.
    s = fp_oracle.initial_state(iri("F0"), iri("npS"))
    s = fp_oracle.apply(s, events()["review"])["state"]
    retract = {
        "kind": "RETRACT",
        "target_np": iri("npR"),
        "retraction_np": iri("npX"),
    }
    ro = invoke(fp_oracle, s, retract)
    rr = invoke(fp_runtime, s, retract)
    require(ro == rr, {"oracle": ro, "runtime": rr})
    require(ro["qualified"] and iri("npR") not in ro["state"]["live_reviews"], ro)

    # Timestamp/order ambiguity is not guessed by the qualification layer.
    ambiguous_order_policy = {
        "rule": (
            "If source ordering needed for a connected chain cannot be "
            "determined from retained project-native chronology, classify T8 "
            "rather than invent an order."
        ),
        "status": "FROZEN_SYNTHETIC_POLICY",
    }

    result = {
        "study": "FORMALIZATION_PAPERS_PREFRESH_SYNTHETIC_GATE_V1",
        "fixture_count": len(fixtures) + 2,
        "parser_exact_fixture_count": len(fixtures),
        "parser_exact": True,
        "qualification_exact": True,
        "t0_generator_sequence": o_chain["generators"],
        "counterfactuals": {
            "response_before_review": "PASS_REJECT",
            "response_before_update": "PASS_REJECT",
            "history_ablation": "PASS_REJECT",
            "decision_before_update": "PASS_REJECT",
            "wrong_target": "PASS_REJECT",
            "retraction": "PASS",
        },
        "supersedes_edge_detected": True,
        "retraction_edge_detected": True,
        "multiple_review_targets_detected": True,
        "ambiguous_order_policy": ambiguous_order_policy,
        "overall": "PASS",
        "provider_record_content_opened": False,
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "fp_prefresh_synthetic_gate_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
