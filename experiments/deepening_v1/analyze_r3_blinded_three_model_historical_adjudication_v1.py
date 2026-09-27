from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

MODELS = ["qwen2.5:7b", "gemma3:12b", "llama3.1:8b"]
PERTURBATIONS = ["P0_CANONICAL", "P1_SOURCES_FIRST", "P2_REVERSE_PAGE_ORDER"]

# Frozen before model execution. Values are normalized encodings of the
# pre-existing sealed proposition panel, with row IDs retained for audit.
EXPECTED = {
    "R3R2-01": {
        "corroborated_target_identity": (
            "SOURCE_ATTRIBUTION_NON_EYEWITNESS",
            ["R3OBJ-PASH-01", "R3OBJ-PASH-02"],
        ),
        "corroboration_relation_direction": (
            "CORROBORATES",
            ["R3OBJ-PASH-02"],
        ),
        "challenged_target_identity": (
            "ROUTE_NECESSITY",
            ["R3OBJ-PASH-03", "R3OBJ-PASH-04"],
        ),
        "challenge_relation_direction": (
            "CRITICIZES",
            ["R3OBJ-PASH-04"],
        ),
        "alternative_modality": (
            "POSSIBLE",
            ["R3OBJ-PASH-04"],
        ),
        "later_actor_responsibility": (
            "STEIN_AS_REPORTED_BY_CORDIER",
            ["R3OBJ-PASH-02", "R3OBJ-PASH-04"],
        ),
    },
    "R3R2-02": {
        "cypress_commitment_holder": (
            "HOUTUM_SCHINDLER",
            ["R3OBJ-ARBR-02"],
        ),
        "cordier_transmission_reply_role": (
            "TRANSMITS_AND_REPLIES",
            ["R3OBJ-ARBR-02", "R3OBJ-ARBR-03"],
        ),
        "cordier_adoption_status": (
            "NOT_ESTABLISHED",
            ["R3OBJ-ARBR-03"],
        ),
    },
    "R3R2-03": {
        "distance_marches_evidence_assignment": (
            "SURVEY_MEASUREMENTS",
            ["R3OBJ-DES-03"],
        ),
        "folklore_source_evidence_assignment": (
            "LOCAL_FOLKLORE",
            ["R3OBJ-DES-02"],
        ),
        "later_actor_source_responsibility": (
            "STEIN_AS_REPORTED_BY_CORDIER",
            ["R3OBJ-DES-02", "R3OBJ-DES-03"],
        ),
        "proposition_specific_evidence_distinction": (
            "DISTINCT_BINDINGS",
            ["R3OBJ-DES-02", "R3OBJ-DES-03"],
        ),
    },
    "R3R2-04": {
        "earlier_action_reading": (
            "FOUND",
            ["R3OBJ-URM-01"],
        ),
        "replacement_action_reading": (
            "FOUNDED",
            ["R3OBJ-URM-02"],
        ),
        "correction_direction": (
            "FOUND_TO_FOUNDED",
            ["R3OBJ-URM-01", "R3OBJ-URM-02"],
        ),
    },
    "R3R2-05": {
        "controversy_resolution_state": (
            "COMPETING_POSITIONS",
            ["R3OBJ-TUN-01", "R3OBJ-TUN-02", "R3OBJ-TUN-03"],
        ),
        "sykes_relation_direction": (
            "REVISES_OR_CRITICIZES_YULE",
            ["R3OBJ-TUN-02"],
        ),
        "hedin_relation_direction": (
            "SUPPORTS_YULE",
            ["R3OBJ-TUN-03"],
        ),
        "hedin_modality": (
            "EXTREMELY_PROBABLE",
            ["R3OBJ-TUN-03"],
        ),
        "quoted_scholar_vs_editor_responsibility": (
            "SCHOLARS_AS_REPORTED_BY_CORDIER",
            ["R3OBJ-TUN-02", "R3OBJ-TUN-03"],
        ),
    },
}

SEALED_PANEL_BLOB_SHA = "f1ffa2aefde17f731fc9d0a19781aed81c94622c"
SEALED_PANEL_PATH = Path("data/r3_verified_proposition_panel_v1.csv")


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("utf-8")
    return hashlib.sha1(header + raw).hexdigest()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        default="experiments/deepening_v1/llm_second_pass_v1/raw_results_v1.jsonl",
    )
    parser.add_argument(
        "--out-dir",
        default="experiments/deepening_v1/llm_second_pass_v1",
    )
    args = parser.parse_args()

    if git_blob_sha(SEALED_PANEL_PATH) != SEALED_PANEL_BLOB_SHA:
        raise SystemExit(
            "Sealed proposition-panel blob has changed. Refusing analysis."
        )

    results_path = Path(args.results)
    if not results_path.exists():
        raise SystemExit(f"Missing frozen results: {results_path}")

    raw_lines = [
        line
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    records = [json.loads(line) for line in raw_lines]

    expected_call_ids = {
        f"{model}::{case_id}::{perturbation}"
        for model in MODELS
        for case_id in EXPECTED
        for perturbation in PERTURBATIONS
    }
    observed_call_ids = {r.get("call_id") for r in records}

    if len(records) != 45:
        raise SystemExit(f"Expected 45 frozen calls, found {len(records)}")
    if observed_call_ids != expected_call_ids:
        missing = sorted(expected_call_ids - observed_call_ids)
        extra = sorted(observed_call_ids - expected_call_ids)
        raise SystemExit(
            f"Call matrix mismatch. Missing={missing} Extra={extra}"
        )

    by_key = {
        (r["model"], r["case_id"], r["perturbation"]): r
        for r in records
    }

    component_results = []
    model_sensitivity = collections.Counter()
    model_stable = collections.Counter()

    for case_id, component_map in EXPECTED.items():
        for component, (sealed_value, row_ids) in component_map.items():
            per_model = {}

            for model in MODELS:
                vals = []
                eligible = True
                details = []

                for perturbation in PERTURBATIONS:
                    rec = by_key[(model, case_id, perturbation)]
                    if not rec.get("schema_valid"):
                        eligible = False
                        details.append(
                            {
                                "perturbation": perturbation,
                                "schema_valid": False,
                                "validation_errors": rec.get(
                                    "validation_errors", []
                                ),
                            }
                        )
                        continue

                    obj = (
                        rec.get("parsed", {})
                        .get("components", {})
                        .get(component)
                    )
                    if not isinstance(obj, dict):
                        eligible = False
                        details.append(
                            {
                                "perturbation": perturbation,
                                "schema_valid": True,
                                "component_missing": True,
                            }
                        )
                        continue

                    value = obj.get("value")
                    vals.append(value)
                    details.append(
                        {
                            "perturbation": perturbation,
                            "schema_valid": True,
                            "value": value,
                            "evidence_pages": obj.get("evidence_pages", []),
                            "supporting_quote": obj.get(
                                "supporting_quote", ""
                            ),
                            "confidence": obj.get("confidence"),
                        }
                    )

                stable = (
                    eligible
                    and len(vals) == 3
                    and vals[0] == vals[1] == vals[2]
                )
                stable_value = vals[0] if stable else None

                per_model[model] = {
                    "stable": stable,
                    "stable_value": stable_value,
                    "perturbations": details,
                }

                if stable:
                    model_stable[model] += 1
                else:
                    model_sensitivity[model] += 1

            stable_values = [
                x["stable_value"]
                for x in per_model.values()
                if x["stable"]
            ]
            counts = collections.Counter(stable_values)

            consensus = None
            consensus_kind = "NO_CONSENSUS"

            if counts.get("UNRESOLVED", 0) >= 2:
                consensus = "UNRESOLVED"
                consensus_kind = "CONSENSUS_UNRESOLVED"
            else:
                non_unresolved = {
                    value: count
                    for value, count in counts.items()
                    if value != "UNRESOLVED" and count >= 2
                }
                if non_unresolved:
                    consensus = sorted(
                        non_unresolved.items(),
                        key=lambda x: (-x[1], x[0]),
                    )[0][0]
                    consensus_kind = "ENSEMBLE_CONSENSUS"

            if consensus_kind == "ENSEMBLE_CONSENSUS":
                comparison = (
                    "MATCH"
                    if consensus == sealed_value
                    else "CONTRADICTION"
                )
            elif consensus_kind == "CONSENSUS_UNRESOLVED":
                comparison = "CONSENSUS_UNRESOLVED"
            else:
                comparison = "NO_CONSENSUS"

            component_results.append(
                {
                    "case_id": case_id,
                    "component": component,
                    "sealed_value": sealed_value,
                    "sealed_proposition_rows": row_ids,
                    "models": per_model,
                    "stable_value_counts": dict(counts),
                    "consensus": consensus,
                    "consensus_kind": consensus_kind,
                    "comparison": comparison,
                }
            )

    counts = collections.Counter(
        r["comparison"] for r in component_results
    )

    if counts["CONTRADICTION"] > 0:
        gate = "HISTORICAL_READING_REOPENED"
    elif (
        counts["NO_CONSENSUS"] > 0
        or counts["CONSENSUS_UNRESOLVED"] > 0
    ):
        gate = "BOUNDED_PARTIAL"
    else:
        gate = "BLINDED_MODEL_REPLICATION_PASS"

    summary = {
        "protocol": "R3_BLINDED_THREE_MODEL_HISTORICAL_ADJUDICATION_PROTOCOL_v1",
        "sealed_panel_blob_sha": SEALED_PANEL_BLOB_SHA,
        "raw_results_sha256": sha256(results_path.read_bytes()),
        "models": MODELS,
        "perturbations": PERTURBATIONS,
        "component_count": len(component_results),
        "comparison_counts": dict(counts),
        "model_stable_component_counts": dict(model_stable),
        "model_sensitive_or_invalid_component_counts": dict(
            model_sensitivity
        ),
        "gate_disposition": gate,
        "claim_ceiling": (
            "Source-grounded answer-blinded three-model replication only; "
            "not human historian validation."
        ),
        "components": component_results,
    }

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    analysis_path = out / "analysis_v1.json"
    analysis_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# R3 Blinded Three-Model Historical Adjudication Results v1",
        "",
        "Status: EXECUTED ANALYSIS OF FROZEN MODEL OUTPUTS",
        "",
        "## Gate disposition",
        "",
        gate,
        "",
        "## Counts",
        "",
        f"- atomic components: {len(component_results)}",
        f"- MATCH: {counts['MATCH']}",
        f"- CONTRADICTION: {counts['CONTRADICTION']}",
        f"- NO_CONSENSUS: {counts['NO_CONSENSUS']}",
        f"- CONSENSUS_UNRESOLVED: {counts['CONSENSUS_UNRESOLVED']}",
        "",
        "## Model stability",
        "",
    ]

    for model in MODELS:
        lines.append(
            f"- {model}: stable={model_stable[model]}, "
            f"sensitive_or_invalid={model_sensitivity[model]}"
        )

    lines.extend(
        [
            "",
            "## Atomic results",
            "",
            "| Case | Component | Consensus | Sealed | Comparison |",
            "|---|---|---|---|---|",
        ]
    )

    for row in component_results:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["case_id"],
                    row["component"],
                    str(row["consensus"]),
                    row["sealed_value"],
                    row["comparison"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Claim ceiling",
            "",
            "This result is a source-grounded, answer-blinded, "
            "model-separated replication with prompt-order stability checks.",
            "",
            "It is not independent human validation, historian consensus, "
            "or evidence that language models generally replace expert review.",
            "",
            "No prompt, model, source page, atomic field, or normalized answer "
            "key may be changed after these outputs are opened to rescue a "
            "failed component.",
        ]
    )

    (out / "RESULTS_v1.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(
        {
            "gate_disposition": gate,
            "comparison_counts": dict(counts),
            "model_stable_component_counts": dict(model_stable),
            "model_sensitive_or_invalid_component_counts": dict(
                model_sensitivity
            ),
            "analysis_sha256": sha256(analysis_path.read_bytes()),
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
