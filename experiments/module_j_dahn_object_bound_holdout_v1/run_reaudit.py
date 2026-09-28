from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tarfile
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

I_DIR = HERE.parent / "module_i_dahn_document_boundary_holdout_v1"
if str(I_DIR) not in sys.path:
    sys.path.insert(0, str(I_DIR))

import oracle_j
import runtime_j
import evaluator_j

UPSTREAM_REPO = "FloChiff/DAHNProject"
UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"

EXPOSED_PREFIXES = {
    "berlin": "Correspondence/Berlin_Intellectuals/Corpus/",
    "paul": "Correspondence/Paul_d_Estournelles_de_Constant/Corpus/",
    "stabi": "Correspondence/Nachlassprojekt/StaBi/Correspondence/",
}

STABI_INVALID_I_CANDIDATES = {
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/AuszugeBriefwechselBoeckhundseinemBruderFriedrich.xml",
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/BriefabschriftenKarlFriedrichHermannanBoeckh.xml",
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/BriefabschriftenKarlJosephHieronymusWindischmannanBoeckh.xml",
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/BriefausschnitteAugustBoeckhanDavidSchulz.xml",
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/BriefauszugeBoeckhanOscarvonSarwey.xml",
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/BriefauszugeCarlRichardLepsiusanBoeckh.xml",
    "Correspondence/Nachlassprojekt/StaBi/Correspondence/BriefauszugeHermannKochlyanBoeckh.xml",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-J-reaudit/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def public_runtime_doc(doc):
    return {
        "path": doc["path"],
        "source_sha256": doc["source_sha256"],
        "is_correspondence": doc["is_correspondence"],
        "object_contract": doc["object_contract"],
        "object_id": doc.get("object_id"),
        "primary_boundary_signature": doc.get("primary_boundary_signature"),
        "claims": [runtime_j.base.public_claim(c) for c in doc.get("claims", [])],
        "origin_claim": runtime_j.base.public_claim(doc["origin_claim"]) if doc.get("origin_claim") else None,
        "origin_contract_status": doc.get("origin_contract_status"),
        "neutral_event": doc.get("neutral_event"),
        "has_annex": doc.get("has_annex"),
    }


def contract_check(runtime_doc, oracle_doc):
    reasons = []

    if runtime_doc.get("source_sha256") != oracle_doc.get("source_sha256"):
        reasons.append("SOURCE_HASH_MISMATCH")

    ro = runtime_doc.get("object_contract") or {}
    oo = oracle_doc.get("object_contract") or {}
    if ro.get("status") != oo.get("status"):
        reasons.append("OBJECT_STATUS_MISMATCH")
    if ro.get("candidate_count") != oo.get("candidate_count"):
        reasons.append("OBJECT_COUNT_MISMATCH")
    if ro.get("object_id") != oo.get("object_id"):
        reasons.append("OBJECT_ID_MISMATCH")
    if ro.get("boundary_signature") != oo.get("boundary_signature"):
        reasons.append("PRIMARY_BOUNDARY_MISMATCH")

    runtime_keys = sorted(c.get("claim_key") for c in runtime_doc.get("claims", []) if c.get("claim_key"))
    oracle_keys = sorted(c.get("claim_key") for c in oracle_doc.get("claims", []) if c.get("claim_key"))
    if runtime_keys != oracle_keys:
        reasons.append("T0_CLAIM_SET_MISMATCH")

    if ro.get("status") == "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        oid = oo.get("object_id")
        if any(c.get("object_id") != oid for c in runtime_doc.get("claims", [])):
            reasons.append("RUNTIME_CROSS_OBJECT_CLAIM")
        if any(c.get("object_id") != oid for c in oracle_doc.get("claims", [])):
            reasons.append("ORACLE_CROSS_OBJECT_CLAIM")

    r_origin = runtime_doc.get("origin_claim")
    o_origin = oracle_doc.get("origin_claim")
    if (r_origin or {}).get("claim_key") != (o_origin or {}).get("claim_key"):
        reasons.append("ORIGIN_CLAIM_MISMATCH")
    if (r_origin or {}).get("object_id") != (o_origin or {}).get("object_id"):
        reasons.append("ORIGIN_OBJECT_MISMATCH")

    if runtime_doc.get("origin_contract_status") != oracle_doc.get("origin_contract_status"):
        reasons.append("ORIGIN_CONTRACT_MISMATCH")

    if runtime_j.runtime_q0(runtime_doc) != oracle_doc.get("q0"):
        reasons.append("Q0_MISMATCH")

    if bool(runtime_doc.get("is_correspondence")) != bool(oracle_doc.get("is_correspondence")):
        reasons.append("CORRESPONDENCE_CLASS_MISMATCH")

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
                o = oracle_j.parse_document(rel, raw)
                r = runtime_j.parse_document(rel, raw)
                rows.append({
                    "path": rel,
                    "raw_sha256": sha256(raw),
                    "oracle": o,
                    "runtime": r,
                    "contract": contract_check(r, o),
                })
            except Exception as e:
                errors.append({"path": rel, "error": repr(e)})
    rows.sort(key=lambda x: x["path"])
    errors.sort(key=lambda x: x["path"])
    return rows, errors


def fail_eval(reason):
    return {
        "end_to_end_pass": False,
        "contract_ok": False,
        "contract_reasons": [reason],
    }


def evaluate_episode(row):
    out = []
    for arm in runtime_j.INTERFACES:
        if not row["contract"]["ok"]:
            out.append({
                "arm": arm,
                "trace": None,
                "evaluation": fail_eval("SOURCE_CONTRACT_UNRESOLVED"),
            })
            continue
        trace = runtime_j.execute(row["runtime"], arm)
        ev = evaluator_j.evaluate_trace(trace, row["oracle"], row["runtime"])
        ev["contract_ok"] = True
        ev["contract_reasons"] = []
        ev["end_to_end_pass"] = bool(ev["end_to_end_pass"] and row["contract"]["ok"])
        out.append({"arm": arm, "trace": trace, "evaluation": ev})
    return {
        "path": row["path"],
        "source_sha256": row["raw_sha256"],
        "object_contract": row["oracle"]["object_contract"],
        "oracle": {
            "eligibility": row["oracle"]["eligibility"],
            "expected_question": row["oracle"]["expected_question"],
            "q0": row["oracle"]["q0"],
            "warrant_root": row["oracle"]["warrant_root"],
            "warrant_after": row["oracle"]["warrant_after"],
            "origin_claim": row["oracle"]["origin_claim"],
            "origin_contract_status": row["oracle"]["origin_contract_status"],
            "required_live_claim_keys_after": row["oracle"]["required_live_claim_keys_after"],
        },
        "contract": row["contract"],
        "arms": out,
    }


def arm_eval(ep, arm):
    return next(x for x in ep["arms"] if x["arm"] == arm)["evaluation"]


def deterministic_audit(rows, episodes, n=12):
    full_paths = {r["path"] for r in rows if r["oracle"]["full_trajectory_eligible"]}
    by_ep = {e["path"]: e for e in episodes}
    ranked = sorted(full_paths, key=lambda p: hashlib.sha256(p.encode()).hexdigest())

    chosen = []
    def add(pred):
        for p in ranked:
            if p in chosen:
                continue
            r = next(x for x in rows if x["path"] == p)
            if pred(r):
                chosen.append(p)
                return

    add(lambda r: r["oracle"]["eligibility"]["trigger"] == "D1")
    add(lambda r: r["oracle"]["eligibility"]["trigger"] == "D2")
    add(lambda r: r["runtime"].get("has_annex"))
    add(lambda r: r["oracle"]["warrant_after"]["type"] == "ALTERNATIVE_SET")
    add(lambda r: r["oracle"]["warrant_after"]["type"] in ("INTERVAL", "OPEN_INTERVAL"))

    for p in ranked:
        if len(chosen) >= n:
            break
        if p not in chosen:
            chosen.append(p)

    out = []
    for p in chosen[:n]:
        r = next(x for x in rows if x["path"] == p)
        ep = by_ep[p]
        rstar = next(x for x in ep["arms"] if x["arm"] == "I_RSTAR")
        out.append({
            "path": p,
            "selection_hash": hashlib.sha256(p.encode()).hexdigest(),
            "object_contract": r["oracle"]["object_contract"],
            "has_annex": r["runtime"].get("has_annex"),
            "root_claims": r["oracle"]["claims"],
            "origin_claim": r["oracle"]["origin_claim"],
            "expected_question": r["oracle"]["expected_question"],
            "runtime_question": (rstar["trace"] or {}).get("question"),
            "warrant_root": r["oracle"]["warrant_root"],
            "warrant_after": r["oracle"]["warrant_after"],
            "runtime_warrant_after": (rstar["trace"] or {}).get("post_origin_warrant"),
            "required_live_claim_keys_after": r["oracle"]["required_live_claim_keys_after"],
            "runtime_live_claim_keys_after": (rstar["trace"] or {}).get("post_origin_live_claim_keys"),
            "origin_transition": (rstar["trace"] or {}).get("origin_transition"),
            "evaluation": rstar["evaluation"],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", choices=sorted(EXPOSED_PREFIXES), required=True)
    args = ap.parse_args()

    prefix = EXPOSED_PREFIXES[args.corpus]
    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    rows, errors = load_prefix(prefix, archive_raw)

    status_counts = Counter(r["oracle"]["object_contract"]["status"] for r in rows)
    single_rows = [r for r in rows if r["oracle"]["object_contract"]["status"] == "SINGLE_PRIMARY_DOCUMENT_OBJECT"]
    primary_rows = [r for r in single_rows if r["oracle"]["eligibility"]["eligible"]]
    full_rows = [r for r in single_rows if r["oracle"]["full_trajectory_eligible"]]
    episodes = [evaluate_episode(r) for r in full_rows]

    aggregates = {}
    for arm in runtime_j.INTERFACES:
        evs = [arm_eval(e, arm) for e in episodes]
        keys = [
            "q0_exact", "discovery_exact", "applicability_exact", "warrant_exact",
            "selective_update", "alternative_persistence", "null_event_stable",
            "provenance_exact", "transition_history_exact", "object_contract_exact",
            "end_to_end_pass",
        ]
        aggregates[arm] = {
            "episodes": len(evs),
            **{k: sum(bool(x.get(k)) for x in evs) for k in keys},
        }

    n = len(full_rows)
    rstar_all = n > 0 and aggregates["I_RSTAR"]["end_to_end_pass"] == n
    native_all = n > 0 and aggregates["I_NATIVE"]["end_to_end_pass"] == n
    alt_sep = any(
        arm_eval(e, "I_RSTAR").get("discovery_exact")
        and not arm_eval(e, "I_NO_ALTERNATIVES").get("question_emerged")
        for e in episodes
    )
    binding_sep = any(
        arm_eval(e, "I_RSTAR").get("applicability_exact")
        and not arm_eval(e, "I_NO_BINDING").get("applicability_exact")
        for e in episodes
    )
    history_sep = any(
        arm_eval(e, "I_RSTAR").get("transition_history_exact")
        and not arm_eval(e, "I_NO_HISTORY").get("transition_history_exact")
        for e in episodes
    )

    stabi_old = []
    if args.corpus == "stabi":
        by_path = {r["path"]: r for r in rows}
        for path in sorted(STABI_INVALID_I_CANDIDATES):
            r = by_path.get(path)
            stabi_old.append({
                "path": path,
                "present": r is not None,
                "object_status": r["oracle"]["object_contract"]["status"] if r else None,
                "eligible_after_J": r["oracle"]["eligibility"]["eligible"] if r else None,
                "full_after_J": r["oracle"]["full_trajectory_eligible"] if r else None,
            })

    result = {
        "study": "MODULE_J_OBJECT_BOUND_EXPOSED_REAUDIT_V1",
        "authority": "DEVELOPMENT_REAUDIT_ON_EXPOSED_CORPORA_ONLY",
        "corpus": args.corpus,
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "prefix": prefix,
            "archive_sha256": sha256(archive_raw),
        },
        "population": {
            "parsed_documents": len(rows),
            "parse_errors": len(errors),
            "object_status_counts": dict(status_counts),
            "single_primary_objects": len(single_rows),
            "primary_discovery_pool": len(primary_rows),
            "full_trajectory_pool": len(full_rows),
            "contract_unresolved_full": sum(not r["contract"]["ok"] for r in full_rows),
        },
        "aggregates": aggregates,
        "development_mechanism_checks": {
            "RSTAR_all_full_trajectories": rstar_all,
            "NATIVE_all_full_trajectories": native_all,
            "alternatives_ablation_witness": alt_sep,
            "binding_ablation_witness": binding_sep,
            "history_ablation_witness": history_sep,
        },
        "stabi_previous_invalid_candidates": stabi_old,
        "primary_manifest": [
            {
                "path": r["path"],
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
        "parse_errors": errors,
        "claim_boundary": [
            "This is a development reaudit because Berlin, Paul and StaBi are exposed.",
            "StaBi is never restored to confirmatory status by this rerun.",
            "File-level temporal metadata is admissible only when exactly one primary scholarly letter object exists.",
            "Multiple sent dates without a single primary letter cannot create a discovery episode.",
            "All temporal claims in one warrant state must share one object_id.",
        ],
    }

    outdir = HERE / "reaudit_results" / args.corpus
    outdir.mkdir(parents=True, exist_ok=True)
    result_path = outdir / "results.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = deterministic_audit(rows, episodes)
    audit_path = outdir / "source_audit_manifest.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "corpus": args.corpus,
        "population": result["population"],
        "aggregates": result["aggregates"],
        "development_mechanism_checks": result["development_mechanism_checks"],
        "stabi_previous_invalid_candidates": stabi_old,
        "results_sha256": sha256(result_path.read_bytes()),
        "source_audit_sha256": sha256(audit_path.read_bytes()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
