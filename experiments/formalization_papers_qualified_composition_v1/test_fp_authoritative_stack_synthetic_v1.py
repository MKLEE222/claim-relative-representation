from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_population
import fp_documentary_audit_v1 as documentary
import fp_finalize_v1 as finalizer
import run_fp_fresh_population_v1 as runner
import test_fp_prefresh_synthetic_v1 as base


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        nanopubs = root / "nanopubs"
        nanopubs.mkdir(parents=True)
        (nanopubs / "synthetic_complete.trig").write_bytes(
            base.fixture()
        )
        archive = root / "synthetic_source.tar.gz"
        archive.write_bytes(b"synthetic-archive-placeholder")

        parsed = runner.parse_source(root)
        require(not parsed["parse_errors"], parsed)
        require(parsed["per_file_exact"], parsed)
        require(parsed["aggregate_exact"], parsed)

        surface = parsed["surface"]
        population = fp_population.classify_population(surface)
        require(population["complete_accounting"], population)
        require(population["root_count"] == 1, population)
        require(
            population["roots"][0]["disposition"]
            == "T0_COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION",
            population,
        )

        chains = fp_population.eligible_chains(population)
        require(len(chains) == 1, chains)
        version = fp_population.analyze_versions(surface)
        chain_result = runner.execute_chain(
            chains[0], population, version
        )
        require(chain_result["pass"], chain_result)
        require(
            chain_result["forward"]["generators"]
            == [
                "RECORD_REVIEW",
                "REPLACE_FORMALIZATION",
                "RECORD_RESPONSE",
                "REVISE_PUBLICATION_STATUS",
            ],
            chain_result,
        )
        require(
            chain_result["counterfactuals"][
                "P4_history_ablation"
            ]["pass"],
            chain_result,
        )

        main_result = {
            "study": "SYNTHETIC_MAIN",
            "source": {
                "record_file_count": len(parsed["files"]),
            },
            "surface_sha256": "synthetic",
            "population": population,
            "eligible_chain_count": 1,
            "chain_results": [chain_result],
            "provisional_disposition": (
                "PASS_PENDING_DOCUMENTARY_AUDIT"
            ),
            "provisional_reasons": [],
        }

        files, by_graph, all_triples, audit_parse_errors = (
            documentary.load_raw(root)
        )
        require(not audit_parse_errors, audit_parse_errors)
        raw = documentary.independently_derive(
            by_graph, all_triples
        )

        audit_row = documentary.audit_chain(
            chains[0], raw, by_graph
        )
        require(audit_row["pass"], audit_row)

        main_t0, main_t1 = documentary.manifest_sets(main_result)
        main_connected = set(main_t1)
        main_connected.update(x[:5] for x in main_t0)
        raw_connected = set(tuple(x) for x in raw["t1"])
        raw_t0 = set(tuple(x) for x in raw["t0"])

        require(
            main_connected == raw_connected,
            {
                "main_connected": sorted(main_connected),
                "raw_connected": sorted(raw_connected),
            },
        )
        require(
            main_t0 == raw_t0,
            {
                "main_t0": sorted(main_t0),
                "raw_t0": sorted(raw_t0),
            },
        )

        audit_result = {
            "overall": "PASS",
            "errors": [],
        }
        disposition, reasons = finalizer.finalize(
            main_result, audit_result
        )
        require(
            disposition == "PASS" and not reasons,
            {"disposition": disposition, "reasons": reasons},
        )

        result = {
            "study": "FORMALIZATION_PAPERS_AUTHORITATIVE_STACK_SYNTHETIC_V1",
            "parser_exact": True,
            "population_disposition": population["roots"][0][
                "disposition"
            ],
            "eligible_chain_count": len(chains),
            "forward_generators": chain_result["forward"][
                "generators"
            ],
            "history_ablation_pass": True,
            "documentary_chain_pass": True,
            "documentary_chain_set_exact": True,
            "final_disposition": disposition,
            "overall": "PASS",
            "provider_record_content_opened": False,
        }

        out_dir = HERE / "results"
        out_dir.mkdir(parents=True, exist_ok=True)
        (
            out_dir
            / "fp_authoritative_stack_synthetic_v1.json"
        ).write_text(
            json.dumps(result, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print(json.dumps(
            result, ensure_ascii=False, indent=2
        ))


if __name__ == "__main__":
    main()
