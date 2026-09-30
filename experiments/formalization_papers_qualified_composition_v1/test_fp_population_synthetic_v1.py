from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_oracle
import fp_runtime
import fp_population
import test_fp_prefresh_synthetic_v1 as base


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def parsed(raw):
    o = fp_oracle.parse_trig(raw)
    r = fp_runtime.parse_trig(raw)
    require(
        json.loads(json.dumps(o, sort_keys=True))
        == json.loads(json.dumps(r, sort_keys=True)),
        {"oracle": o, "runtime": r},
    )
    return o


def one_root_disposition(raw):
    pop = fp_population.classify_population(parsed(raw))
    require(pop["complete_accounting"], pop)
    require(pop["root_count"] == 1, pop)
    return pop["roots"][0], pop


def main():
    rows = {}

    root, pop = one_root_disposition(base.fixture())
    require(
        root["disposition"]
        == "T0_COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION",
        root,
    )
    require(len(root["t0_chains"]) == 1, root)
    rows["T0_COMPLETE"] = root["disposition"]

    root, pop = one_root_disposition(
        base.fixture(include_decision=False)
    )
    require(
        root["disposition"]
        == "T1_REVIEW_UPDATE_RESPONSE_NO_DECISION",
        root,
    )
    require(len(root["t1_chains"]) == 1, root)
    rows["T1_NO_DECISION"] = root["disposition"]

    root, pop = one_root_disposition(base.fixture(
        include_update=False,
        include_response=False,
        include_decision=False,
    ))
    require(root["disposition"] == "T3_REVIEW_ONLY", root)
    rows["REVIEW_ONLY"] = root["disposition"]

    root, pop = one_root_disposition(base.fixture(
        include_review=False,
        include_response=False,
        include_decision=False,
    ))
    require(
        root["disposition"]
        == "T4_UPDATE_WITHOUT_CONNECTED_REVIEW",
        root,
    )
    rows["UPDATE_ONLY"] = root["disposition"]

    root, pop = one_root_disposition(
        base.fixture(response_review="missingReview")
    )
    require(
        root["disposition"]
        == "T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET",
        root,
    )
    rows["MISSING_REVIEW_TARGET"] = root["disposition"]

    root, pop = one_root_disposition(
        base.fixture(response_update="missingUpdate")
    )
    require(
        root["disposition"]
        == "T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET",
        root,
    )
    rows["MISSING_UPDATE_TARGET"] = root["disposition"]

    root, pop = one_root_disposition(
        base.fixture(superseded_review=True)
    )
    require(
        root["disposition"]
        == "T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET",
        root,
    )
    rows["SUPERSEDED_REVIEW_TARGET"] = root["disposition"]

    root, pop = one_root_disposition(
        base.fixture(retract_response=True)
    )
    require(
        root["disposition"] == "T2_REVIEW_UPDATE_NO_RESPONSE",
        root,
    )
    rows["RETRACTED_RESPONSE"] = root["disposition"]

    pop = fp_population.classify_population(parsed(base.fixture(
        cross_root=True,
        duplicate_review_targets=True,
    )))
    require(pop["root_count"] == 2, pop)
    disp = {x["root"]: x["disposition"] for x in pop["roots"]}
    require(
        base.iri("F0") in disp and base.iri("F2") in disp,
        disp,
    )
    require(
        "T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET" in set(disp.values()),
        disp,
    )
    rows["MULTIPLE_REVIEW_TARGETS"] = disp

    pop = fp_population.classify_population(
        parsed(base.fixture(cross_root=True))
    )
    require(pop["root_count"] == 2, pop)
    disp = {x["root"]: x["disposition"] for x in pop["roots"]}
    require(
        disp[base.iri("F0")]
        == "T0_COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION",
        disp,
    )
    require(disp[base.iri("F2")] == "T6_ROOT_ONLY", disp)
    rows["CROSS_ROOT_ACCOUNTING"] = disp

    eligible = fp_population.eligible_chains(
        fp_population.classify_population(parsed(base.fixture()))
    )
    require(len(eligible) == 1, eligible)
    require("decision_np" in eligible[0], eligible)

    result = {
        "study": "FORMALIZATION_PAPERS_POPULATION_SYNTHETIC_V1",
        "rows": rows,
        "eligible_chain_count_t0_fixture": len(eligible),
        "complete_accounting": True,
        "overall": "PASS",
        "provider_record_content_opened": False,
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "fp_population_synthetic_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
