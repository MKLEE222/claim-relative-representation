from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
L_DIR = HERE.parent / "module_l_portable_object_claim_v1"
M_DIR = HERE.parent / "module_m_dh_comparators_v1"
for p in (HERE, L_DIR, M_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import oracle_p
import runtime_p
import evaluator_p
import comparators_m
import evaluator_m

UPSTREAM_REPO = "Auden-Musulin-Papers/amp-data"
UPSTREAM_COMMIT = "289a52de61aef0b6354e3c8298173bf1f889feb2"
PREFIX = "data/editions/"
EXPECTED_XML = 73

SOURCE_CONTEXT = {
    "source_repository": UPSTREAM_REPO,
    "source_version": UPSTREAM_COMMIT,
    "population_scope": "MODULE_P_AMP_EXPOSED_DEVELOPMENT_V1",
}

P_CAPS = (
    "P1_CURRENT_STATE_BEFORE",
    "P2_EVENT_APPLICABILITY",
    "P3_POST_EVENT_RESULT",
    "P4_SELECTIVE_UPDATE",
    "P5_PROVENANCE",
    "P6_TRANSITION_ATTRIBUTION",
    "P7_DELAYED_HISTORY",
)

M_TASKS = (
    "T1_CURRENT_STATE_EXACT",
    "T2_CURRENT_PROVENANCE_EXACT",
    "T3_STATE_DELTA_EXACT",
    "T4_TRANSITION_ATTRIBUTION_EXACT",
    "T5_DELAYED_HISTORY_AUDIT_EXACT",
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-P/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def p_contract(o, r):
    reasons = []

    checks = {
        "object_status": (
            (o.get("object_contract") or {}).get("status"),
            (r.get("object_contract") or {}).get("status"),
        ),
        "object_id": (o.get("object_id"), r.get("object_id")),
        "boundary_signature": (
            o.get("primary_boundary_signature"),
            r.get("primary_boundary_signature"),
        ),
        "source_context": (o.get("source_context"), r.get("source_context")),
        "origin_status": (
            o.get("origin_contract_status"),
            r.get("origin_contract_status"),
        ),
        "origin_key": (
            (o.get("origin_claim") or {}).get("claim_key"),
            (r.get("origin_claim") or {}).get("claim_key"),
        ),
        "p_disposition": (o.get("p_disposition"), r.get("p_disposition")),
        "p_transition_class": (
            o.get("p_transition_class"),
            r.get("p_transition_class"),
        ),
        "p_phi_before": (
            o.get("p_warrant_before"),
            r.get("p_warrant_before"),
        ),
        "p_phi_after": (
            o.get("p_warrant_after"),
            r.get("p_warrant_after"),
        ),
    }
    for name, (a, b) in checks.items():
        if a != b:
            reasons.append(name)

    return {"ok": not reasons, "reasons": reasons}


def load_population(archive_raw: bytes):
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
            if not rel.startswith(PREFIX) or not rel.lower().endswith(".xml"):
                continue
            suffix = rel[len(PREFIX):]
            if "/" in suffix or "\\" in suffix:
                continue
            f = tf.extractfile(member)
            if f is None:
                continue
            raw = f.read()
            try:
                o = oracle_p.parse_document(rel, raw, SOURCE_CONTEXT)
                r = runtime_p.parse_document(rel, raw, SOURCE_CONTEXT)
                rows.append({
                    "path": rel,
                    "raw_sha256": sha256(raw),
                    "oracle": o,
                    "runtime": r,
                    "contract": p_contract(o, r),
                })
            except Exception as e:
                errors.append({"path": rel, "error": repr(e)})

    rows.sort(key=lambda x: x["path"])
    errors.sort(key=lambda x: x["path"])
    return rows, errors


def reference_eval(row):
    trace = runtime_p.execute(row["runtime"])
    p_eval = evaluator_p.evaluate(trace, row["oracle"], row["runtime"])

    regimes = {
        "RSTAR": comparators_m.rstar_view(row["runtime"], trace),
        "B_CURRENT_REOPEN": comparators_m.current_reopen(row["runtime"]),
        "B_ORDERED_SNAPSHOTS": comparators_m.ordered_snapshots(row["runtime"]),
    }
    m_eval = {
        name: evaluator_m.evaluate_regime(out, row["oracle"])
        for name, out in regimes.items()
    }

    return trace, p_eval, m_eval


def failure_eval(row):
    rdoc = row["runtime"]
    odoc = row["oracle"]

    wrong_object = runtime_p.execute(rdoc, fault={"type": "wrong_object"})
    wrong_source = runtime_p.execute(rdoc, fault={"type": "wrong_source_version"})
    missing_app = runtime_p.execute(rdoc, fault={"type": "missing_applicability"})

    collateral_trace = runtime_p.execute(rdoc, fault={"type": "collateral_mutation"})
    collateral_eval = evaluator_p.evaluate(collateral_trace, odoc, rdoc)

    no_history_trace = runtime_p.execute(rdoc, drop_history=True)
    no_history_eval = evaluator_p.evaluate(no_history_trace, odoc, rdoc)

    return {
        "Q1_WRONG_OBJECT": {
            "rejected": not wrong_object["origin_transition"].get("applicable"),
            "root_unchanged": wrong_object["post_event_warrant"] == rdoc.get("warrant_root"),
            "reason": wrong_object["origin_transition"].get("collateral_temporal_paths"),
        },
        "Q2_WRONG_SOURCE_VERSION": {
            "rejected": not wrong_source["origin_transition"].get("applicable"),
            "root_unchanged": wrong_source["post_event_warrant"] == rdoc.get("warrant_root"),
            "reason": wrong_source["origin_transition"].get("collateral_temporal_paths"),
        },
        "Q3_MISSING_APPLICABILITY": {
            "rejected": not missing_app["origin_transition"].get("applicable"),
            "root_unchanged": missing_app["post_event_warrant"] == rdoc.get("warrant_root"),
            "reason": missing_app["origin_transition"].get("collateral_temporal_paths"),
        },
        "Q4_COLLATERAL_MUTATION": {
            "event_applicable": collateral_eval["P2_EVENT_APPLICABILITY"],
            "selectivity": collateral_eval["P4_SELECTIVE_UPDATE"],
            "transition_attribution": collateral_eval["P6_TRANSITION_ATTRIBUTION"],
            "collateral_paths": collateral_trace["collateral_temporal_paths"],
        },
        "Q5_NO_HISTORY": {
            "post_result": no_history_eval["P3_POST_EVENT_RESULT"],
            "selectivity": no_history_eval["P4_SELECTIVE_UPDATE"],
            "provenance": no_history_eval["P5_PROVENANCE"],
            "transition_attribution": no_history_eval["P6_TRANSITION_ATTRIBUTION"],
            "delayed_history": no_history_eval["P7_DELAYED_HISTORY"],
        },
    }


def aggregate_reference(evals):
    return {
        "episodes": len(evals),
        **{
            cap: sum(bool(x["p_eval"].get(cap)) for x in evals)
            for cap in P_CAPS
        },
        "reference_end_to_end_pass": sum(
            bool(x["p_eval"].get("reference_end_to_end_pass"))
            for x in evals
        ),
    }


def aggregate_comparators(evals):
    out = {}
    for regime in ("RSTAR", "B_CURRENT_REOPEN", "B_ORDERED_SNAPSHOTS"):
        rows = [x["m_eval"][regime] for x in evals]
        out[regime] = {
            "episodes": len(rows),
            **{
                task: sum(bool(x.get(task)) for x in rows)
                for task in M_TASKS
            },
        }
    return out


def aggregate_failures(evals):
    names = (
        "Q1_WRONG_OBJECT",
        "Q2_WRONG_SOURCE_VERSION",
        "Q3_MISSING_APPLICABILITY",
        "Q4_COLLATERAL_MUTATION",
        "Q5_NO_HISTORY",
    )
    out = {}

    for name in names:
        rows = [x["failures"][name] for x in evals]
        if name in {
            "Q1_WRONG_OBJECT",
            "Q2_WRONG_SOURCE_VERSION",
            "Q3_MISSING_APPLICABILITY",
        }:
            out[name] = {
                "episodes": len(rows),
                "rejected": sum(bool(x["rejected"]) for x in rows),
                "root_unchanged": sum(bool(x["root_unchanged"]) for x in rows),
            }
        elif name == "Q4_COLLATERAL_MUTATION":
            out[name] = {
                "episodes": len(rows),
                "event_applicable": sum(bool(x["event_applicable"]) for x in rows),
                "selectivity_pass": sum(bool(x["selectivity"]) for x in rows),
                "transition_attribution": sum(
                    bool(x["transition_attribution"]) for x in rows
                ),
                "collateral_detected": sum(
                    bool(x["collateral_paths"]) for x in rows
                ),
            }
        else:
            out[name] = {
                "episodes": len(rows),
                "post_result": sum(bool(x["post_result"]) for x in rows),
                "selectivity": sum(bool(x["selectivity"]) for x in rows),
                "provenance": sum(bool(x["provenance"]) for x in rows),
                "transition_attribution": sum(
                    bool(x["transition_attribution"]) for x in rows
                ),
                "delayed_history": sum(bool(x["delayed_history"]) for x in rows),
            }
    return out


def main():
    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    rows, errors = load_population(archive_raw)

    complete = len(rows) + len(errors) == EXPECTED_XML
    unresolved = [r for r in rows if not r["contract"]["ok"]]

    dispositions = Counter(r["oracle"].get("p_disposition") for r in rows)
    transition_classes = Counter(
        r["oracle"].get("p_transition_class")
        for r in rows
        if r["oracle"].get("p_disposition") == "ERIR_ELIGIBLE"
    )
    object_status = Counter(
        (r["oracle"].get("object_contract") or {}).get("status")
        for r in rows
    )

    eligible = [
        r for r in rows
        if r["contract"]["ok"]
        and r["oracle"].get("p_erir_eligible")
    ]

    evaluated = []
    for row in eligible:
        trace, p_eval, m_eval = reference_eval(row)
        failures = failure_eval(row)
        evaluated.append({
            "row": row,
            "trace": trace,
            "p_eval": p_eval,
            "m_eval": m_eval,
            "failures": failures,
        })

    regime_separation = {
        "eligible_erir": len(eligible),
        "old_d1d2_not_eligible": sum(
            not bool(x["row"]["oracle"].get("eligibility", {}).get("eligible"))
            for x in evaluated
        ),
        "old_d1d2_eligible": sum(
            bool(x["row"]["oracle"].get("eligibility", {}).get("eligible"))
            for x in evaluated
        ),
    }

    report = {
        "study": "MODULE_P_AMP_EXPOSED_DEVELOPMENT_V1",
        "data_status": "EXPOSED_DEVELOPMENT_ONLY",
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "prefix": PREFIX,
            "archive_sha256": sha256(archive_raw),
        },
        "source_context": SOURCE_CONTEXT,
        "population": {
            "expected_xml": EXPECTED_XML,
            "parsed_documents": len(rows),
            "parse_errors": len(errors),
            "complete_accounting": complete,
            "object_status_counts": dict(object_status),
            "p_disposition_counts": dict(dispositions),
            "p_transition_class_counts": dict(transition_classes),
            "oracle_runtime_contract_unresolved": len(unresolved),
        },
        "regime_separation": regime_separation,
        "reference_capabilities": aggregate_reference(evaluated),
        "comparator_capabilities": aggregate_comparators(evaluated),
        "failure_interventions": aggregate_failures(evaluated),
        "eligible_manifest": [
            {
                "path": x["row"]["path"],
                "source_sha256": x["row"]["raw_sha256"],
                "transition_class": x["row"]["oracle"].get("p_transition_class"),
                "old_d1d2_eligible": bool(
                    x["row"]["oracle"].get("eligibility", {}).get("eligible")
                ),
                "phi_before": x["row"]["oracle"].get("p_warrant_before"),
                "phi_after": x["row"]["oracle"].get("p_warrant_after"),
                "root_warrant": x["row"]["oracle"].get("warrant_root"),
                "post_warrant": x["row"]["oracle"].get("warrant_after"),
                "origin_claim": x["row"]["oracle"].get("origin_claim"),
                "p_evaluation": x["p_eval"],
                "comparator_evaluation": x["m_eval"],
                "failure_evaluation": x["failures"],
            }
            for x in evaluated
        ],
        "null_event_manifest": [
            {
                "path": r["path"],
                "source_sha256": r["raw_sha256"],
                "phi_before": r["oracle"].get("p_warrant_before"),
                "phi_after": r["oracle"].get("p_warrant_after"),
            }
            for r in rows
            if r["contract"]["ok"]
            and r["oracle"].get("p_admissible_null_event")
        ],
        "contract_unresolved_manifest": [
            {"path": r["path"], "reasons": r["contract"]["reasons"]}
            for r in unresolved
        ],
        "parse_error_manifest": errors,
        "claim_ceiling": [
            "AMP is exposed development evidence, not fresh confirmation.",
            "ERIR eligibility is defined by the frozen Phi contract, not by post-run tuning.",
            "No prevalence or cross-event-family generality is licensed.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "amp_exposed_development_results_v1.json"
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "study": report["study"],
        "population": report["population"],
        "regime_separation": report["regime_separation"],
        "reference_capabilities": report["reference_capabilities"],
        "comparator_capabilities": report["comparator_capabilities"],
        "failure_interventions": report["failure_interventions"],
        "results_sha256": sha256(out_path.read_bytes()),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if not complete or unresolved:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
