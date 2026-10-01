from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
J_DIR = HERE.parent / "module_j_dahn_object_bound_holdout_v1"
if str(J_DIR) not in sys.path:
    sys.path.insert(0, str(J_DIR))

import run_reaudit as jr
import runtime_j

UPSTREAM_REPO = "FloChiff/DAHNProject"
UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
PREFIX = "Correspondence/Nachlassprojekt/GeStA/"
EXPECTED_XML = 83

EXPECTED_BLOBS = {
    "runtime_j.py": "002a5a5f9c4253a6bf1ee90bde4b7b4727636146",
    "oracle_j.py": "282b8db3cc44c3d23aaa15b0bf59f84676eef0e9",
    "evaluator_j.py": "6c588f3c1f723f33020e050fc35af7931fb8eb2e",
    "test_object_contract_v1.py": "d7ecddea804e73f53048bfdfc91b84d21eba8c09",
}


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode()
    return hashlib.sha1(header + raw).hexdigest()


def engine_checks():
    out = {}
    for name, expected in EXPECTED_BLOBS.items():
        path = J_DIR / name
        actual = git_blob_sha(path)
        out[name] = {"expected": expected, "actual": actual, "ok": actual == expected}
    return out


def classify(n_full, contract_unresolved_full, aggregates, mechanism_checks, integrity_ok):
    if not integrity_ok:
        return "INVALID"

    if n_full == 0:
        return "NULL_APPLICABILITY"

    if 1 <= n_full < 5:
        return "BOUNDED_PARTIAL"

    if contract_unresolved_full:
        return "BOUNDED_PARTIAL"

    primary_ok = (
        aggregates["I_RSTAR"]["end_to_end_pass"] == n_full
        and mechanism_checks["alternatives_ablation_witness"]
        and mechanism_checks["binding_ablation_witness"]
        and mechanism_checks["history_ablation_witness"]
    )
    return "COMPUTATIONAL_PASS_PENDING_SOURCE_AUDIT" if primary_ok else "BOUNDED_PARTIAL"


def main():
    engine = engine_checks()
    engine_ok = all(x["ok"] for x in engine.values())

    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = jr.fetch(archive_url)
    rows, errors = jr.load_prefix(PREFIX, archive_raw)

    parsed = len(rows)
    total = parsed + len(errors)
    population_ok = total == EXPECTED_XML

    status_counts = Counter(r["oracle"]["object_contract"]["status"] for r in rows)
    single_rows = [
        r for r in rows
        if r["oracle"]["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT"
    ]
    primary_rows = [
        r for r in single_rows
        if r["oracle"]["eligibility"]["eligible"]
    ]
    full_rows = [
        r for r in single_rows
        if r["oracle"]["full_trajectory_eligible"]
    ]
    episodes = [jr.evaluate_episode(r) for r in full_rows]

    aggregates = {}
    for arm in runtime_j.INTERFACES:
        evs = [jr.arm_eval(e, arm) for e in episodes]
        keys = [
            "q0_exact",
            "discovery_exact",
            "applicability_exact",
            "warrant_exact",
            "selective_update",
            "alternative_persistence",
            "null_event_stable",
            "provenance_exact",
            "transition_history_exact",
            "object_contract_exact",
            "end_to_end_pass",
        ]
        aggregates[arm] = {
            "episodes": len(evs),
            **{k: sum(bool(x.get(k)) for x in evs) for k in keys},
        }

    n_full = len(full_rows)
    mechanism_checks = {
        "RSTAR_all_full_trajectories": (
            n_full > 0 and aggregates["I_RSTAR"]["end_to_end_pass"] == n_full
        ),
        "NATIVE_all_full_trajectories": (
            n_full > 0 and aggregates["I_NATIVE"]["end_to_end_pass"] == n_full
        ),
        "alternatives_ablation_witness": any(
            jr.arm_eval(e, "I_RSTAR").get("discovery_exact")
            and not jr.arm_eval(e, "I_NO_ALTERNATIVES").get("question_emerged")
            for e in episodes
        ),
        "binding_ablation_witness": any(
            jr.arm_eval(e, "I_RSTAR").get("applicability_exact")
            and not jr.arm_eval(e, "I_NO_BINDING").get("applicability_exact")
            for e in episodes
        ),
        "history_ablation_witness": any(
            jr.arm_eval(e, "I_RSTAR").get("transition_history_exact")
            and not jr.arm_eval(e, "I_NO_HISTORY").get("transition_history_exact")
            for e in episodes
        ),
    }

    contract_unresolved_full = sum(not r["contract"]["ok"] for r in full_rows)
    integrity_ok = engine_ok and population_ok

    computational_classification = classify(
        n_full,
        contract_unresolved_full,
        aggregates,
        mechanism_checks,
        integrity_ok,
    )

    # Protocol: audit all if <=12, otherwise use the frozen deterministic J routine at n=12.
    audit_n = n_full if n_full <= 12 else 12
    audit = jr.deterministic_audit(rows, episodes, n=audit_n) if n_full else []

    result = {
        "study": "MODULE_K_GESTA_FRESH_HOLDOUT_V1",
        "authority": "FIRST_COMPLETED_PREREGISTERED_RUN_ONLY",
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "prefix": PREFIX,
            "archive_sha256": jr.sha256(archive_raw),
        },
        "engine_blob_checks": engine,
        "population": {
            "expected_xml": EXPECTED_XML,
            "parsed_documents": parsed,
            "parse_errors": len(errors),
            "complete_accounting": population_ok,
            "object_status_counts": dict(status_counts),
            "single_primary_objects": len(single_rows),
            "primary_discovery_pool": len(primary_rows),
            "full_trajectory_pool": n_full,
            "contract_unresolved_full": contract_unresolved_full,
        },
        "aggregates": aggregates,
        "mechanism_checks": mechanism_checks,
        "computational_classification": computational_classification,
        "object_status_manifest": [
            {
                "path": r["path"],
                "source_sha256": r["raw_sha256"],
                "status": r["oracle"]["object_contract"]["status"],
                "candidate_count": r["oracle"]["object_contract"]["candidate_count"],
                "boundary_kind": r["oracle"]["object_contract"].get("boundary_kind"),
                "contract": r["contract"],
            }
            for r in rows
        ],
        "primary_manifest": [
            {
                "path": r["path"],
                "source_sha256": r["raw_sha256"],
                "object_contract": r["oracle"]["object_contract"],
                "trigger": r["oracle"]["eligibility"]["trigger"],
                "q0": r["oracle"]["q0"],
                "warrant_root": r["oracle"]["warrant_root"],
                "warrant_after": r["oracle"]["warrant_after"],
                "full_trajectory_eligible": r["oracle"]["full_trajectory_eligible"],
                "exclusion_reasons": r["oracle"]["full_trajectory_exclusion_reasons"],
                "contract": r["contract"],
            }
            for r in primary_rows
        ],
        "episodes": episodes,
        "parse_error_manifest": errors,
        "documentary_audit_status": "PENDING_HUMAN_SOURCE_AUDIT" if audit else "NOT_APPLICABLE",
        "claim_boundary": [
            "GeStA was selected as a complete population before XML content opening.",
            "Module J Routes A/B/C are unchanged; no Route D is authorized.",
            "A zero full-trajectory population is an applicability result, not 0/83 evaluator accuracy.",
            "A computational pass is not final PASS until deterministic source audit is complete.",
            "Because GeStA shares the DAHN encoding ecology, this holdout does not by itself establish cross-project transfer.",
        ],
    }

    OUT = HERE / "results"
    OUT.mkdir(parents=True, exist_ok=True)
    result_path = OUT / "results.json"
    audit_path = OUT / "documentary_audit_manifest.json"
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "study": result["study"],
        "engine_ok": engine_ok,
        "population": result["population"],
        "aggregates": aggregates,
        "mechanism_checks": mechanism_checks,
        "computational_classification": computational_classification,
        "documentary_audit_cases": len(audit),
        "results_sha256": jr.sha256(result_path.read_bytes()),
        "audit_manifest_sha256": jr.sha256(audit_path.read_bytes()),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if computational_classification == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
