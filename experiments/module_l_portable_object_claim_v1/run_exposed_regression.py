from __future__ import annotations

import io
import json
import sys
import tarfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

J_DIR = HERE.parent / "module_j_dahn_object_bound_holdout_v1"
if str(J_DIR) not in sys.path:
    sys.path.insert(0, str(J_DIR))

import run_reaudit as jr
import oracle_l
import runtime_l
import evaluator_l

SOURCE_CONTEXT = {
    "source_repository": jr.UPSTREAM_REPO,
    "source_version": jr.UPSTREAM_COMMIT,
    "population_scope": "EXPOSED_DAHN_REGRESSION_ONLY",
}

HISTORICAL_J_BASELINE = {
    "berlin": {
        "parsed_documents": 190,
        "single_primary_objects": 178,
        "primary_discovery_pool": 26,
        "full_trajectory_pool": 17,
        "I_RSTAR_end_to_end_pass": 17,
    },
    "paul": {
        "parsed_documents": 1515,
        "single_primary_objects": 1515,
        "primary_discovery_pool": 26,
        "full_trajectory_pool": 21,
        "I_RSTAR_end_to_end_pass": 21,
    },
    "stabi": {
        "parsed_documents": 465,
        "single_primary_objects": 0,
        "primary_discovery_pool": 0,
        "full_trajectory_pool": 0,
        "I_RSTAR_end_to_end_pass": 0,
    },
}


def proof_core(c):
    return {
        "claim_key": c.get("claim_key"),
        "object_id": c.get("object_id"),
        "object_boundary_signature": c.get("object_boundary_signature"),
        "applicability_class": c.get("applicability_class"),
        "source_repository": c.get("source_repository"),
        "source_version": c.get("source_version"),
        "population_scope": c.get("population_scope"),
        "source_file": c.get("source_file"),
        "source_locator_contract": c.get("source_locator_contract"),
        "source_locator_xpath": c.get("source_locator_xpath"),
    }


def excluded_core(doc):
    return sorted(
        (
            x.get("applicability_class"),
            tuple(sorted((x.get("raw_attrs") or {}).items())),
            x.get("source_text"),
        )
        for x in doc.get("excluded_temporal_claims", [])
    )


def contract_check(runtime_doc, oracle_doc):
    reasons = []

    if runtime_doc.get("source_sha256") != oracle_doc.get("source_sha256"):
        reasons.append("SOURCE_HASH_MISMATCH")
    if runtime_doc.get("source_context") != oracle_doc.get("source_context"):
        reasons.append("SOURCE_CONTEXT_MISMATCH")

    ro = runtime_doc.get("object_contract") or {}
    oo = oracle_doc.get("object_contract") or {}
    for key in (
        "status",
        "candidate_count",
        "object_id",
        "boundary_signature",
        "boundary_kind",
        "source_repository",
        "source_version",
        "population_scope",
    ):
        if ro.get(key) != oo.get(key):
            reasons.append(f"OBJECT_{key.upper()}_MISMATCH")

    rc = sorted((proof_core(c) for c in runtime_doc.get("claims", [])), key=lambda x: str(x))
    oc = sorted((proof_core(c) for c in oracle_doc.get("claims", [])), key=lambda x: str(x))
    if rc != oc:
        reasons.append("ACTIVE_CLAIM_PROOF_MISMATCH")

    rr = proof_core(runtime_doc.get("origin_claim") or {})
    oor = proof_core(oracle_doc.get("origin_claim") or {})
    if rr != oor:
        reasons.append("ORIGIN_PROOF_MISMATCH")

    if runtime_doc.get("origin_contract_status") != oracle_doc.get("origin_contract_status"):
        reasons.append("ORIGIN_CONTRACT_MISMATCH")

    if runtime_l.runtime_q0(runtime_doc) != oracle_doc.get("q0"):
        reasons.append("Q0_MISMATCH")

    if excluded_core(runtime_doc) != excluded_core(oracle_doc):
        reasons.append("EXCLUDED_TEMPORAL_DIAGNOSTIC_MISMATCH")

    return {"ok": not reasons, "reasons": reasons}


def load_prefix(prefix, archive_raw):
    rows = []
    errors = []
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            parts = Path(member.name).parts
            if len(parts) < 2:
                continue
            rel = str(Path(*parts[1:]))
            if not rel.startswith(prefix) or not rel.lower().endswith(".xml"):
                continue
            f = tf.extractfile(member)
            if f is None:
                continue
            raw = f.read()
            try:
                o = oracle_l.parse_document(rel, raw, SOURCE_CONTEXT)
                r = runtime_l.parse_document(rel, raw, SOURCE_CONTEXT)
                rows.append({
                    "path": rel,
                    "raw_sha256": jr.sha256(raw),
                    "oracle": o,
                    "runtime": r,
                    "contract": contract_check(r, o),
                })
            except Exception as e:
                errors.append({"path": rel, "error": repr(e)})
    rows.sort(key=lambda x: x["path"])
    errors.sort(key=lambda x: x["path"])
    return rows, errors


def arm_eval(row, arm):
    if not row["contract"]["ok"]:
        return {
            "end_to_end_pass": False,
            "contract_ok": False,
            "contract_reasons": row["contract"]["reasons"],
        }
    trace = runtime_l.execute(row["runtime"], arm)
    ev = evaluator_l.evaluate_trace(trace, row["oracle"], row["runtime"])
    ev["contract_ok"] = True
    ev["contract_reasons"] = []
    return ev


def delta(current, baseline):
    return {k: current.get(k, 0) - baseline.get(k, 0) for k in baseline}


def main():
    archive_url = f"https://github.com/{jr.UPSTREAM_REPO}/archive/{jr.UPSTREAM_COMMIT}.tar.gz"
    archive_raw = jr.fetch(archive_url)

    report = {
        "study": "MODULE_L_PORTABLE_EXPOSED_REGRESSION_V1",
        "source_context": SOURCE_CONTEXT,
        "archive_sha256": jr.sha256(archive_raw),
        "interpretation": (
            "EXPOSED REGRESSION ONLY. Counts may change under the repaired portable contract. "
            "No result in this report is fresh confirmatory evidence."
        ),
        "corpora": {},
    }

    hard_failure = False

    for name, prefix in jr.EXPOSED_PREFIXES.items():
        rows, errors = load_prefix(prefix, archive_raw)
        status_counts = Counter(
            (r["oracle"].get("object_contract") or {}).get("status")
            for r in rows
        )
        single = [
            r for r in rows
            if (r["oracle"].get("object_contract") or {}).get("status")
                == "SINGLE_PRIMARY_DOCUMENT_OBJECT"
        ]
        discovery = [r for r in single if r["oracle"].get("eligibility", {}).get("eligible")]
        full = [r for r in single if r["oracle"].get("full_trajectory_eligible")]
        unresolved = [r for r in rows if not r["contract"]["ok"]]

        aggregates = {}
        for arm in runtime_l.INTERFACES:
            evs = [arm_eval(r, arm) for r in full]
            aggregates[arm] = {
                "episodes": len(evs),
                "end_to_end_pass": sum(bool(e.get("end_to_end_pass")) for e in evs),
                "contract_ok": sum(bool(e.get("contract_ok")) for e in evs),
            }

        current = {
            "parsed_documents": len(rows),
            "single_primary_objects": len(single),
            "primary_discovery_pool": len(discovery),
            "full_trajectory_pool": len(full),
            "I_RSTAR_end_to_end_pass": aggregates["I_RSTAR"]["end_to_end_pass"],
        }
        baseline = HISTORICAL_J_BASELINE[name]
        report["corpora"][name] = {
            "prefix": prefix,
            "parse_errors": errors,
            "object_status_counts": dict(status_counts),
            "contract_unresolved": [
                {"path": r["path"], "reasons": r["contract"]["reasons"]}
                for r in unresolved
            ],
            "current": current,
            "historical_module_j_baseline": baseline,
            "delta_from_j": delta(current, baseline),
            "aggregates": aggregates,
        }

        if errors or unresolved:
            hard_failure = True

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "exposed_regression_v1.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if hard_failure:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
