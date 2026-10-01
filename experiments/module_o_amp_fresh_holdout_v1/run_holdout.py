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
ROOT = HERE.parent

L_DIR = ROOT / "module_l_portable_object_claim_v1"
M_DIR = ROOT / "module_m_dh_comparators_v1"
N_DIR = ROOT / "module_n_obligation_identification_v1"
J_DIR = ROOT / "module_j_dahn_object_bound_holdout_v1"

for p in (L_DIR, M_DIR, N_DIR, J_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import oracle_l
import runtime_l
import evaluator_l
import comparators_m
import evaluator_m
import interventions_n
import evaluator_n
import run_exposed_regression as lr

UPSTREAM_REPO = "Auden-Musulin-Papers/amp-data"
UPSTREAM_COMMIT = "289a52de61aef0b6354e3c8298173bf1f889feb2"
PREFIX = "data/editions/"
EXPECTED_XML = 73

SOURCE_CONTEXT = {
    "source_repository": UPSTREAM_REPO,
    "source_version": UPSTREAM_COMMIT,
    "population_scope": "MODULE_O_AMP_FRESH_HOLDOUT_V1",
}

EXPECTED_BLOBS = {
    L_DIR / "runtime_l.py": "34285c65d020f8a5b096abf54133ee2fb3930793",
    L_DIR / "oracle_l.py": "ace9d7fa06c08f17ba9a7edd7b44515390abc4f9",
    L_DIR / "evaluator_l.py": "e5a935153f7e929d491121cce27ff10bf6be72ad",
    M_DIR / "comparators_m.py": "08f0f2d2a1fc2e9e547fa3df2dd350e37d4770f6",
    M_DIR / "evaluator_m.py": "96f9fed32a65047f838a7eb4f1f3673a5425fed2",
    N_DIR / "interventions_n.py": "19672c3b01cfaae858ebb1cec447216c78f0d600",
    N_DIR / "evaluator_n.py": "be049628dbd3aced7187c18ea3518d2fe3318d10",
}

N_ARMS = (
    "N_NO_CURRENT_PROVENANCE",
    "N_NO_TRANSITION_BINDING",
    "N_NO_HISTORY",
    "N_COLLAPSE_RESULT_STATUS",
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-O/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode()
    return hashlib.sha1(header + raw).hexdigest()


def engine_checks():
    out = {}
    for path, expected in EXPECTED_BLOBS.items():
        actual = git_blob_sha(path)
        out[str(path.relative_to(ROOT.parent))] = {
            "expected": expected,
            "actual": actual,
            "ok": actual == expected,
        }
    return out


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
            # Frozen population is direct files under data/editions/.
            suffix = rel[len(PREFIX):]
            if "/" in suffix or "\\" in suffix:
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
                    "raw_sha256": sha256(raw),
                    "oracle": o,
                    "runtime": r,
                    "contract": lr.contract_check(r, o),
                })
            except Exception as e:
                errors.append({"path": rel, "error": repr(e)})
    rows.sort(key=lambda x: x["path"])
    errors.sort(key=lambda x: x["path"])
    return rows, errors


def full_eval(row):
    if not row["contract"]["ok"]:
        return {
            "portable": {"end_to_end_pass": False, "contract_ok": False},
            "comparators": {},
            "obligations": {},
        }

    trace = runtime_l.execute(row["runtime"], "I_RSTAR")
    portable = evaluator_l.evaluate_trace(trace, row["oracle"], row["runtime"])
    portable["contract_ok"] = True

    comparator_outputs = {
        "RSTAR": comparators_m.rstar_view(row["runtime"], trace),
        "B_CURRENT_REOPEN": comparators_m.current_reopen(row["runtime"]),
        "B_ORDERED_SNAPSHOTS": comparators_m.ordered_snapshots(row["runtime"]),
    }
    comp = {
        name: evaluator_m.evaluate_regime(out, row["oracle"])
        for name, out in comparator_outputs.items()
    }

    obligations = {}
    for arm in N_ARMS:
        ntrace = interventions_n.run_arm(row["runtime"], arm)
        obligations[arm] = evaluator_n.evaluate(ntrace, row["oracle"])

    return {
        "portable": portable,
        "comparators": comp,
        "obligations": obligations,
    }


def deterministic_audit_manifest(full_rows):
    if not full_rows:
        return []

    if len(full_rows) <= 12:
        chosen = list(full_rows)
    else:
        chosen = []
        seen = set()

        def add(row, reason):
            if row["path"] in seen or len(chosen) >= 12:
                return
            seen.add(row["path"])
            chosen.append({
                "row": row,
                "reasons": [reason],
            })

        by_warrant = {}
        for row in full_rows:
            kind = (row["oracle"].get("warrant_after") or {}).get("type") or "NONE"
            by_warrant.setdefault(kind, []).append(row)
        for kind in sorted(by_warrant):
            row = sorted(by_warrant[kind], key=lambda x: sha256(x["path"].encode()))[0]
            add(row, f"WARRANT_TYPE:{kind}")

        by_boundary = {}
        for row in full_rows:
            kind = (
                (row["oracle"].get("object_contract") or {}).get("boundary_kind")
                or "NONE"
            )
            by_boundary.setdefault(kind, []).append(row)
        for kind in sorted(by_boundary):
            row = sorted(by_boundary[kind], key=lambda x: sha256(x["path"].encode()))[0]
            if row["path"] in seen:
                for entry in chosen:
                    if entry["row"]["path"] == row["path"]:
                        entry["reasons"].append(f"BOUNDARY_KIND:{kind}")
                        break
            else:
                add(row, f"BOUNDARY_KIND:{kind}")

        for row in sorted(full_rows, key=lambda x: sha256(x["path"].encode())):
            if len(chosen) >= 12:
                break
            add(row, "HASH_FILL")

        out = []
        for entry in chosen:
            row = entry["row"]
            out.append({
                "path": row["path"],
                "source_sha256": row["raw_sha256"],
                "selection_reasons": entry["reasons"],
                "object_boundary_kind": (
                    row["oracle"].get("object_contract") or {}
                ).get("boundary_kind"),
                "warrant_after_type": (
                    row["oracle"].get("warrant_after") or {}
                ).get("type"),
                "trigger": (row["oracle"].get("eligibility") or {}).get("trigger"),
            })
        return out

    return [
        {
            "path": row["path"],
            "source_sha256": row["raw_sha256"],
            "selection_reasons": ["AUDIT_ALL_N_LE_12"],
            "object_boundary_kind": (
                row["oracle"].get("object_contract") or {}
            ).get("boundary_kind"),
            "warrant_after_type": (
                row["oracle"].get("warrant_after") or {}
            ).get("type"),
            "trigger": (row["oracle"].get("eligibility") or {}).get("trigger"),
        }
        for row in chosen
    ]


def classify(engine_ok, population_ok, full_rows, evaluations):
    if not engine_ok or not population_ok:
        return "INVALID"

    unresolved = [r for r in full_rows if not r["contract"]["ok"]]
    if unresolved:
        return "INVALID"

    n = len(full_rows)
    if n == 0:
        return "NULL_APPLICABILITY"
    if n < 5:
        return "BOUNDED_PARTIAL"

    portable_ok = all(
        ev["portable"].get("end_to_end_pass")
        for ev in evaluations
    )
    current_ok = all(
        ev["comparators"]["B_CURRENT_REOPEN"].get("T1_CURRENT_STATE_EXACT")
        and ev["comparators"]["B_CURRENT_REOPEN"].get("T2_CURRENT_PROVENANCE_EXACT")
        for ev in evaluations
    )
    snapshots_ok = all(
        ev["comparators"]["B_ORDERED_SNAPSHOTS"].get("T1_CURRENT_STATE_EXACT")
        and ev["comparators"]["B_ORDERED_SNAPSHOTS"].get("T2_CURRENT_PROVENANCE_EXACT")
        and ev["comparators"]["B_ORDERED_SNAPSHOTS"].get("T3_STATE_DELTA_EXACT")
        for ev in evaluations
    )
    rstar_tasks_ok = all(
        all(
            ev["comparators"]["RSTAR"].get(k)
            for k in (
                "T1_CURRENT_STATE_EXACT",
                "T2_CURRENT_PROVENANCE_EXACT",
                "T3_STATE_DELTA_EXACT",
                "T4_TRANSITION_ATTRIBUTION_EXACT",
                "T5_DELAYED_HISTORY_AUDIT_EXACT",
            )
        )
        for ev in evaluations
    )

    if portable_ok and current_ok and snapshots_ok and rstar_tasks_ok:
        return "COMPUTATIONAL_PASS_PENDING_SOURCE_AUDIT"
    return "BOUNDED_PARTIAL"


def aggregate_comparators(evaluations):
    tasks = (
        "T1_CURRENT_STATE_EXACT",
        "T2_CURRENT_PROVENANCE_EXACT",
        "T3_STATE_DELTA_EXACT",
        "T4_TRANSITION_ATTRIBUTION_EXACT",
        "T5_DELAYED_HISTORY_AUDIT_EXACT",
    )
    out = {}
    for regime in ("RSTAR", "B_CURRENT_REOPEN", "B_ORDERED_SNAPSHOTS"):
        rows = [ev["comparators"][regime] for ev in evaluations]
        out[regime] = {
            "episodes": len(rows),
            **{task: sum(bool(x.get(task)) for x in rows) for task in tasks},
        }
    return out


def aggregate_obligations(evaluations):
    caps = (
        "C1_CURRENT_STATE",
        "C2_DISCOVERY",
        "C3_EVENT_APPLICABILITY",
        "C4_RESULT_DETERMINACY",
        "C5_SELECTIVITY",
        "C6_CURRENT_PROVENANCE",
        "C7_TRANSITION_ATTRIBUTION",
        "C8_DELAYED_HISTORY",
    )
    out = {}
    for arm in N_ARMS:
        rows = [ev["obligations"][arm] for ev in evaluations]
        applicable = rows
        if arm == "N_COLLAPSE_RESULT_STATUS":
            applicable = [
                x for x in rows
                if x.get("result_status_intervention_applicable") is True
            ]
        out[arm] = {
            "episodes_total": len(rows),
            "episodes_applicable": len(applicable),
            **{cap: sum(bool(x.get(cap)) for x in applicable) for cap in caps},
        }
    return out


def main():
    engine = engine_checks()
    engine_ok = all(x["ok"] for x in engine.values())

    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    rows, errors = load_population(archive_raw)

    total = len(rows) + len(errors)
    population_ok = total == EXPECTED_XML

    status_counts = Counter(
        (r["oracle"].get("object_contract") or {}).get("status")
        for r in rows
    )
    single = [
        r for r in rows
        if (r["oracle"].get("object_contract") or {}).get("status")
            == "SINGLE_PRIMARY_DOCUMENT_OBJECT"
    ]
    discovery = [
        r for r in single
        if (r["oracle"].get("eligibility") or {}).get("eligible")
    ]
    full = [
        r for r in single
        if r["oracle"].get("full_trajectory_eligible")
    ]

    evaluations = [full_eval(r) for r in full]
    classification = classify(
        engine_ok,
        population_ok,
        full,
        evaluations,
    )

    audit_manifest = deterministic_audit_manifest(full)

    result = {
        "study": "MODULE_O_AMP_FRESH_HOLDOUT_V1",
        "authority": "FIRST_COMPLETED_PREREGISTERED_OPENING_RUN_ONLY",
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "prefix": PREFIX,
            "archive_sha256": sha256(archive_raw),
        },
        "source_context": SOURCE_CONTEXT,
        "engine_blob_checks": engine,
        "population": {
            "expected_xml": EXPECTED_XML,
            "parsed_documents": len(rows),
            "parse_errors": len(errors),
            "complete_accounting": population_ok,
            "object_status_counts": dict(status_counts),
            "single_primary_objects": len(single),
            "primary_discovery_pool": len(discovery),
            "full_trajectory_pool": len(full),
            "contract_unresolved_full": sum(
                not r["contract"]["ok"] for r in full
            ),
        },
        "computational_classification": classification,
        "comparator_aggregates": aggregate_comparators(evaluations),
        "obligation_subset_aggregates": aggregate_obligations(evaluations),
        "object_status_manifest": [
            {
                "path": r["path"],
                "source_sha256": r["raw_sha256"],
                "object_contract": r["oracle"].get("object_contract"),
                "contract": r["contract"],
            }
            for r in rows
        ],
        "full_trajectory_results": [
            {
                "path": r["path"],
                "source_sha256": r["raw_sha256"],
                "oracle_summary": {
                    "object_contract": r["oracle"].get("object_contract"),
                    "eligibility": r["oracle"].get("eligibility"),
                    "q0": r["oracle"].get("q0"),
                    "warrant_root": r["oracle"].get("warrant_root"),
                    "warrant_after": r["oracle"].get("warrant_after"),
                    "origin_contract_status": r["oracle"].get("origin_contract_status"),
                    "full_trajectory_exclusion_reasons": r["oracle"].get(
                        "full_trajectory_exclusion_reasons"
                    ),
                },
                "evaluation": ev,
            }
            for r, ev in zip(full, evaluations)
        ],
        "parse_error_manifest": errors,
        "documentary_audit_status": (
            "PENDING_SOURCE_AUDIT" if audit_manifest else "NOT_APPLICABLE"
        ),
        "claim_ceiling": [
            "This is one fresh independent AMP ecology under the frozen portable contract.",
            "A positive computational result is not final PASS until documentary audit completes.",
            "NULL/BOUNDED_PARTIAL outcomes are retained without corpus rescue.",
            "No cross-event-family generality is licensed by this temporal holdout.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    result_path = out_dir / "results.json"
    audit_path = out_dir / "documentary_audit_manifest.json"

    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    audit_path.write_text(
        json.dumps(audit_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "study": result["study"],
        "engine_ok": engine_ok,
        "population": result["population"],
        "computational_classification": classification,
        "comparator_aggregates": result["comparator_aggregates"],
        "obligation_subset_aggregates": result["obligation_subset_aggregates"],
        "documentary_audit_cases": len(audit_manifest),
        "results_sha256": sha256(result_path.read_bytes()),
        "audit_manifest_sha256": sha256(audit_path.read_bytes()),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if classification == "INVALID":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
