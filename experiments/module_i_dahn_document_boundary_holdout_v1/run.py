from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tarfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import oracle_v2
import runtime_v2
import evaluator_v2

UPSTREAM_REPO = "FloChiff/DAHNProject"
UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
DEFAULT_DEV_PREFIX = "Correspondence/Berlin_Intellectuals/Corpus/"
HOLDOUT_PREFIX = "Correspondence/Nachlassprojekt/StaBi/Correspondence/"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-I-hardened/2.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strip_runtime_doc(doc):
    return {
        "path": doc["path"],
        "source_sha256": doc["source_sha256"],
        "is_correspondence": doc["is_correspondence"],
        "primary_boundary_signature": doc["primary_boundary_signature"],
        "claims": [runtime_v2.public_claim(c) for c in doc["claims"]],
        "origin_claim": runtime_v2.public_claim(doc["origin_claim"]) if doc.get("origin_claim") else None,
        "origin_contract_status": doc.get("origin_contract_status"),
        "origin_element_count": doc.get("origin_element_count"),
        "neutral_event": doc.get("neutral_event"),
        "has_annex": doc.get("has_annex"),
    }


def strip_oracle_doc(doc):
    return {
        k: v for k, v in doc.items()
        if not k.startswith("_")
    }


def semantic_contract_check(runtime_doc, oracle_doc):
    reasons = []

    if runtime_doc.get("source_sha256") != oracle_doc.get("source_sha256"):
        reasons.append("SOURCE_HASH_MISMATCH")

    if runtime_doc.get("primary_boundary_signature") != oracle_doc.get("primary_boundary_signature"):
        reasons.append("PRIMARY_BOUNDARY_MISMATCH")

    runtime_keys = sorted(c.get("claim_key") for c in runtime_doc.get("claims", []) if c.get("claim_key"))
    oracle_keys = sorted(c.get("claim_key") for c in oracle_doc.get("claims", []) if c.get("claim_key"))
    if runtime_keys != oracle_keys:
        reasons.append("T0_CLAIM_SET_MISMATCH")

    r_origin = (runtime_doc.get("origin_claim") or {}).get("claim_key")
    o_origin = (oracle_doc.get("origin_claim") or {}).get("claim_key")
    if r_origin != o_origin:
        reasons.append("ORIGIN_CLAIM_MISMATCH")

    if runtime_doc.get("origin_contract_status") != oracle_doc.get("origin_contract_status"):
        reasons.append("ORIGIN_CONTRACT_STATUS_MISMATCH")
    if runtime_doc.get("origin_element_count") != oracle_doc.get("origin_element_count"):
        reasons.append("ORIGIN_ELEMENT_COUNT_MISMATCH")

    r_neutral = (runtime_doc.get("neutral_event") or {}).get("event_key")
    o_neutral = (oracle_doc.get("neutral_event") or {}).get("event_key")
    if r_neutral != o_neutral:
        reasons.append("NEUTRAL_EVENT_MISMATCH")

    if runtime_v2.runtime_q0(runtime_doc) != oracle_doc.get("q0"):
        reasons.append("Q0_MISMATCH")

    if bool(runtime_doc.get("is_correspondence")) != bool(oracle_doc.get("is_correspondence")):
        reasons.append("CORRESPONDENCE_CLASS_MISMATCH")

    return {
        "ok": not reasons,
        "reasons": reasons,
    }


def archive_documents(prefix, archive_raw):
    rows = []
    parse_errors = []
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
                oracle_doc = oracle_v2.parse_document(rel, raw)
                runtime_doc = runtime_v2.parse_document(rel, raw)
                contract = semantic_contract_check(runtime_doc, oracle_doc)
                rows.append({
                    "path": rel,
                    "raw_sha256": sha256(raw),
                    "runtime": runtime_doc,
                    "oracle": oracle_doc,
                    "contract": contract,
                })
            except Exception as e:
                parse_errors.append({
                    "path": rel,
                    "error": repr(e),
                })
    rows.sort(key=lambda x: x["path"])
    parse_errors.sort(key=lambda x: x["path"])
    return rows, parse_errors


def conservative_arm_failure(arm, contract_reasons):
    return {
        "arm": arm,
        "trace": None,
        "evaluation": {
            "q0_exact": False,
            "discovery_exact": False,
            "question_emerged": False,
            "applicability_exact": False,
            "warrant_exact": False,
            "selective_update": False,
            "collateral_revision_count": None,
            "collateral_temporal_paths": [],
            "required_live_claim_keys_after": [],
            "runtime_live_claim_keys_after": [],
            "alternative_persistence": False,
            "neutral_event_agreement": False,
            "null_event_stable": False,
            "provenance_exact": False,
            "transition_history_exact": False,
            "boundary_exact": False,
            "neutral_parser_agreement": False,
            "contract_ok": False,
            "contract_reasons": contract_reasons,
            "end_to_end_pass": False,
        },
    }


def run_episode(row):
    o = row["oracle"]
    r = row["runtime"]
    contract = row["contract"]
    arms = []

    for arm in runtime_v2.INTERFACES:
        if not contract["ok"]:
            arms.append(conservative_arm_failure(arm, contract["reasons"]))
            continue

        trace = runtime_v2.execute(r, arm)
        ev = evaluator_v2.evaluate_trace(trace, o, r)
        ev["contract_ok"] = True
        ev["contract_reasons"] = []
        ev["end_to_end_pass"] = bool(ev["end_to_end_pass"] and contract["ok"])
        arms.append({
            "arm": arm,
            "trace": trace,
            "evaluation": ev,
        })

    return {
        "path": row["path"],
        "source_sha256": row["raw_sha256"],
        "contract": contract,
        "oracle": {
            "eligibility": o["eligibility"],
            "expected_question": o["expected_question"],
            "q0": o["q0"],
            "warrant_root": o["warrant_root"],
            "warrant_after": o["warrant_after"],
            "required_live_claim_keys_after": o["required_live_claim_keys_after"],
            "neutral_event": o["neutral_event"],
            "primary_boundary_signature": o["primary_boundary_signature"],
            "origin_claim": o["origin_claim"],
            "origin_contract_status": o.get("origin_contract_status"),
            "origin_element_count": o.get("origin_element_count"),
        },
        "runtime_source": strip_runtime_doc(r),
        "arms": arms,
    }


def arm_eval(episode, arm):
    return next(x for x in episode["arms"] if x["arm"] == arm)["evaluation"]


def arm_trace(episode, arm):
    return next(x for x in episode["arms"] if x["arm"] == arm)["trace"]


def deterministic_audit_selection(full_rows, episode_results, limit=10):
    by_path = {e["path"]: e for e in episode_results}

    def rank_path(path):
        return hashlib.sha256(path.encode("utf-8")).hexdigest()

    ordered = sorted(full_rows, key=lambda r: rank_path(r["path"]))
    selected = []

    def add_first(pred):
        for row in ordered:
            if row["path"] in selected:
                continue
            if pred(row):
                selected.append(row["path"])
                return

    add_first(lambda r: r["oracle"]["eligibility"]["trigger"] == "D1")
    add_first(lambda r: r["oracle"]["eligibility"]["trigger"] == "D2")
    add_first(lambda r: r["oracle"]["warrant_after"]["type"] == "EXACT")
    add_first(lambda r: r["oracle"]["warrant_after"]["type"] in ("INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET", "UNRESOLVED"))
    add_first(lambda r: r["runtime"].get("has_annex"))

    for row in ordered:
        if len(selected) >= limit:
            break
        if row["path"] not in selected:
            selected.append(row["path"])

    audit = []
    for path in selected[:limit]:
        row = next(r for r in full_rows if r["path"] == path)
        episode = by_path[path]
        rstar_trace = arm_trace(episode, "I_RSTAR")
        rstar_eval = arm_eval(episode, "I_RSTAR")
        audit.append({
            "path": path,
            "selection_hash": rank_path(path),
            "has_annex": row["runtime"].get("has_annex"),
            "boundary_oracle": row["oracle"]["primary_boundary_signature"],
            "boundary_runtime": row["runtime"]["primary_boundary_signature"],
            "root_claims_oracle": row["oracle"]["claims"],
            "root_claims_runtime": [runtime_v2.public_claim(c) for c in row["runtime"]["claims"]],
            "origin_oracle": row["oracle"]["origin_claim"],
            "origin_runtime": runtime_v2.public_claim(row["runtime"]["origin_claim"]) if row["runtime"].get("origin_claim") else None,
            "neutral_oracle": row["oracle"]["neutral_event"],
            "neutral_runtime": row["runtime"]["neutral_event"],
            "question_oracle": row["oracle"]["expected_question"],
            "question_runtime": rstar_trace.get("question") if rstar_trace else None,
            "warrant_root_oracle": row["oracle"]["warrant_root"],
            "warrant_after_oracle": row["oracle"]["warrant_after"],
            "warrant_after_runtime": rstar_trace.get("post_origin_warrant") if rstar_trace else None,
            "origin_changed_paths": (
                rstar_trace.get("origin_transition", {}).get("changed_paths")
                if rstar_trace else None
            ),
            "origin_collateral_paths": (
                rstar_trace.get("origin_transition", {}).get("collateral_temporal_paths")
                if rstar_trace else None
            ),
            "required_live_claim_keys_after": row["oracle"]["required_live_claim_keys_after"],
            "runtime_live_claim_keys_after": rstar_trace.get("post_origin_live_claim_keys") if rstar_trace else None,
            "delayed_audit_runtime": rstar_trace.get("delayed_audit") if rstar_trace else None,
            "evaluation": rstar_eval,
        })
    return audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default=DEFAULT_DEV_PREFIX)
    ap.add_argument("--mode", choices=("development", "holdout"), default="development")
    args = ap.parse_args()

    if args.mode == "holdout" and args.prefix != HOLDOUT_PREFIX:
        raise SystemExit("holdout mode requires frozen StaBi prefix")
    if args.mode == "development" and args.prefix == HOLDOUT_PREFIX:
        raise SystemExit("development mode is forbidden from inspecting the StaBi holdout")

    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    rows, parse_errors = archive_documents(args.prefix, archive_raw)

    primary_rows = [r for r in rows if r["oracle"]["eligibility"]["eligible"] and r["oracle"]["is_correspondence"]]
    full_rows = [r for r in rows if r["oracle"]["full_trajectory_eligible"]]

    episode_results = [run_episode(r) for r in full_rows]

    aggregates = {}
    for arm in runtime_v2.INTERFACES:
        evs = [arm_eval(e, arm) for e in episode_results]
        aggregates[arm] = {
            "episodes": len(evs),
            "q0_exact": sum(bool(x["q0_exact"]) for x in evs),
            "discovery_exact": sum(bool(x["discovery_exact"]) for x in evs),
            "question_emerged": sum(bool(x["question_emerged"]) for x in evs),
            "applicability_exact": sum(bool(x["applicability_exact"]) for x in evs),
            "warrant_exact": sum(bool(x["warrant_exact"]) for x in evs),
            "selective_update": sum(bool(x["selective_update"]) for x in evs),
            "alternative_persistence": sum(bool(x["alternative_persistence"]) for x in evs),
            "null_event_stable": sum(bool(x["null_event_stable"]) for x in evs),
            "provenance_exact": sum(bool(x["provenance_exact"]) for x in evs),
            "transition_history_exact": sum(bool(x["transition_history_exact"]) for x in evs),
            "contract_ok": sum(bool(x["contract_ok"]) for x in evs),
            "end_to_end_pass": sum(bool(x["end_to_end_pass"]) for x in evs),
        }

    n = len(full_rows)
    rstar_all = n > 0 and aggregates["I_RSTAR"]["end_to_end_pass"] == n
    native_all = n > 0 and aggregates["I_NATIVE"]["end_to_end_pass"] == n

    alt_sep = any(
        arm_eval(e, "I_RSTAR")["discovery_exact"]
        and arm_eval(e, "I_RSTAR")["question_emerged"]
        and not arm_eval(e, "I_NO_ALTERNATIVES")["question_emerged"]
        for e in episode_results
    )
    binding_sep = any(
        arm_eval(e, "I_RSTAR")["applicability_exact"]
        and not arm_eval(e, "I_NO_BINDING")["applicability_exact"]
        for e in episode_results
    )
    history_sep = any(
        arm_eval(e, "I_RSTAR")["transition_history_exact"]
        and not arm_eval(e, "I_NO_HISTORY")["transition_history_exact"]
        for e in episode_results
    )
    unresolved_delay = any(
        e["oracle"]["warrant_after"]["type"] in ("INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET", "UNRESOLVED")
        and arm_eval(e, "I_RSTAR")["alternative_persistence"]
        and arm_eval(e, "I_RSTAR")["transition_history_exact"]
        for e in episode_results
    )
    neutral_witness = any(arm_eval(e, "I_RSTAR")["null_event_stable"] for e in episode_results)
    applicability_witness = any(arm_eval(e, "I_RSTAR")["applicability_exact"] for e in episode_results)
    warrant_change = any(e["oracle"]["warrant_root"] != e["oracle"]["warrant_after"] for e in episode_results)

    contract_unresolved_full = [
        r["path"] for r in full_rows if not r["contract"]["ok"]
    ]

    gate = {
        "full_trajectory_pool_at_least_5": n >= 5,
        "RSTAR_END_TO_END_PASS": rstar_all,
        "NATIVE_END_TO_END_PASS": native_all,
        "QUESTION_EMERGENCE_ABLATION_WITNESS": alt_sep,
        "UNRESOLVED_DELAY_WITNESS": unresolved_delay,
        "BINDING_ABLATION_WITNESS": binding_sep,
        "HISTORY_ABLATION_WITNESS": history_sep,
        "WARRANT_CHANGE_WITNESS": warrant_change,
        "NEUTRAL_EVENT_WITNESS": neutral_witness,
        "SOURCE_VERSION_APPLICABILITY_WITNESS": applicability_witness,
        "NO_FULL_EPISODE_CONTRACT_UNRESOLVED": not contract_unresolved_full,
    }
    gate["MOTHER_PROBLEM_MODULE_I_GATE"] = all(gate.values())

    source_audit = deterministic_audit_selection(full_rows, episode_results, limit=10)

    result = {
        "study": "MODULE_I_DAHN_DOCUMENT_BOUNDARY_HARDENED_V2",
        "mode": args.mode,
        "authority": (
            "HARDENED_DEVELOPMENT_VERIFICATION"
            if args.mode == "development"
            else "PROSPECTIVE_HOLDOUT_EXECUTION"
        ),
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "archive_sha256": sha256(archive_raw),
            "prefix": args.prefix,
        },
        "population": {
            "parsed_documents": len(rows),
            "parse_errors": len(parse_errors),
            "primary_discovery_pool": len(primary_rows),
            "full_trajectory_pool": len(full_rows),
            "full_trajectory_contract_unresolved": len(contract_unresolved_full),
        },
        "aggregates": aggregates,
        "gate": gate,
        "contract_unresolved_full_paths": contract_unresolved_full,
        "episodes": episode_results,
        "primary_pool_manifest": [
            {
                "path": r["path"],
                "trigger": r["oracle"]["eligibility"]["trigger"],
                "expected_question": r["oracle"]["expected_question"],
                "q0": r["oracle"]["q0"],
                "warrant_root": r["oracle"]["warrant_root"],
                "warrant_after": r["oracle"]["warrant_after"],
                "origin_contract_status": r["oracle"].get("origin_contract_status"),
                "origin_element_count": r["oracle"].get("origin_element_count"),
                "full_trajectory_eligible": r["oracle"]["full_trajectory_eligible"],
                "exclusion_reasons": r["oracle"]["full_trajectory_exclusion_reasons"],
                "contract": r["contract"],
            }
            for r in primary_rows
        ],
        "parse_errors": parse_errors,
        "claim_boundary": [
            "Development mode is not confirmatory evidence.",
            "Holdout denominator and gold are generated by the independent raw-source oracle, not by the runtime policy.",
            "Runtime and oracle use different XML libraries and independent eligibility/warrant implementations.",
            "Neutral maintenance stability is measured after executing a real event through the runtime transition operator.",
            "Collateral revision is measured from structural temporal-state diff.",
            "Alternative persistence is checked by source-bound claim key, not inferred from final warrant equality.",
            "Delayed transition audit is reconstructed from retained ledgers.",
            "The temporal warrant remains documentary and contract-relative, not independent historical truth.",
        ],
    }

    outdir = HERE / ("development_results_v2" if args.mode == "development" else "holdout_results_v2")
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_path = outdir / "source_audit_manifest.json"
    audit_path.write_text(json.dumps(source_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "mode": args.mode,
        "population": result["population"],
        "aggregates": result["aggregates"],
        "gate": result["gate"],
        "source_audit_count": len(source_audit),
        "source_audit_paths": [x["path"] for x in source_audit],
        "results_sha256": sha256(out.read_bytes()),
        "source_audit_sha256": sha256(audit_path.read_bytes()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
