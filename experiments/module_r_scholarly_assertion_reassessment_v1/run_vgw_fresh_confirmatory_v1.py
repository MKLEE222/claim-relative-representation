from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "vgw_fresh_confirmatory_v1"
CACHE = HERE / "results" / "vgw_fresh_source_cache_v1"
ANCHORS = HERE / "VGW_DISTRIBUTION_METADATA_ANCHORS_v1.json"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import evaluator_r
import oracle_r
import runtime_r
import vgw_contract_constants as C
import vgw_oracle
import vgw_runtime

EXPECTED_SLUGS = (
    C.BASELINE_SLUG,
    C.POST1970_SLUG,
    *C.CURRENT_PROVIDER_SLUGS,
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(obj) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def git_context():
    return {
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_ref": os.environ.get("GITHUB_REF"),
    }


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_anchors():
    obj = json.loads(ANCHORS.read_text(encoding="utf-8"))
    rows = {x["slug"]: x for x in obj["datasets"]}
    if set(rows) != set(EXPECTED_SLUGS):
        raise RuntimeError("FROZEN_ANCHOR_SLUG_SET_MISMATCH")
    return rows


def write_data_open_marker(anchor_rows):
    marker = {
        "study": "MODULE_R_VGW_FRESH_CONFIRMATORY_V1",
        "event": "DATA_OPEN_EVENT",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "frozen_slugs": list(EXPECTED_SLUGS),
        "protocol": "VGW_FRESH_REASSESSMENT_PROTOCOL_v1.md",
        "execution_contract": "VGW_CONFIRMATORY_EXECUTION_CONTRACT_v1.md",
        "source_urls": {
            slug: anchor_rows[slug]["content_url"]
            for slug in EXPECTED_SLUGS
        },
        "git_context": git_context(),
        "scientific_engine_blobs": {
            "vgw_contract_constants.py": "acac49b2312131100e3f47d5ac258697cb8e4afc",
            "vgw_oracle.py": "57796319953fb6639f8789fbf62f81a82e571472",
            "vgw_runtime.py": "87d63cdbdc4d6c2a59910b57481294a75cd39e7b",
            "oracle_r.py": "f5cefb84d8957b5e887fd133ef1122213b2419dd",
            "runtime_r.py": "52ea3ebb788b414036d3f086aa0d51c0dba424f7",
            "evaluator_r.py": "370b92f3934577af21a318797e75d177ece32097",
        },
    }
    write_json(RESULTS / "DATA_OPEN_EVENT_v1.json", marker)
    print(json.dumps(marker, ensure_ascii=False))


def download_one(slug: str, row: dict) -> bytes:
    req = urllib.request.Request(
        row["content_url"],
        headers={
            "User-Agent": "CRR-Module-R-VGW-fresh/1.0",
            "Accept": "application/n-triples",
            "Accept-Encoding": "identity",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        ctype = str(resp.headers.get("Content-Type") or "").lower()
        raw = resp.read()
        status = getattr(resp, "status", None)

    if status is not None and not (200 <= int(status) < 300):
        raise RuntimeError(f"DOWNLOAD_HTTP_STATUS::{slug}::{status}")
    if "n-triples" not in ctype and "text/plain" not in ctype:
        raise RuntimeError(f"DOWNLOAD_CONTENT_TYPE::{slug}::{ctype}")
    expected_size = int(row["content_size"])
    if len(raw) != expected_size:
        raise RuntimeError(
            f"DOWNLOAD_SIZE_MISMATCH::{slug}::{expected_size}::{len(raw)}"
        )
    return raw


def normalized_extraction(result):
    out = copy.deepcopy(result)
    out.pop("engine", None)
    return out


def case_surface(case):
    event = case.get("event") or {}
    return {
        "f_number": case.get("f_number"),
        "disposition": case.get("disposition"),
        "expected_transition_class": case.get("expected_transition_class"),
        "baseline_object_uri": case.get("baseline_object_uri"),
        "current_object_uri": case.get("current_object_uri"),
        "current_provider_slug": case.get("current_provider_slug"),
        "evidence_id": event.get("evidence_id"),
        "evidence_locator": event.get("evidence_locator"),
        "responsible_agent": event.get("responsible_agent"),
    }


def comparator_eval(output, oracle_transition):
    state = oracle_transition["state"]
    return {
        "B_CURRENT_REOPEN_R": evaluator_r.evaluate_current_reopen(
            runtime_r.current_reopen(output), oracle_transition, state
        ),
        "B_ORDERED_SNAPSHOTS_R": evaluator_r.evaluate_snapshots(
            runtime_r.ordered_snapshots(output), oracle_transition, state
        ),
        "B_CHANGE_LOG_NO_JUSTIFICATION_R": evaluator_r.evaluate_change_log(
            runtime_r.change_log_no_justification(output), oracle_transition
        ),
    }


def comparator_positive_ok(x):
    a = x["B_CURRENT_REOPEN_R"]
    b = x["B_ORDERED_SNAPSHOTS_R"]
    c = x["B_CHANGE_LOG_NO_JUSTIFICATION_R"]
    return all([
        a["CURRENT_STATE_EXACT"],
        a["CURRENT_PROVENANCE_EXACT"],
        not a["TRANSITION_ATTRIBUTION_EXACT"],
        not a["DELAYED_HISTORY_EXACT"],
        b["PRE_STATE_EXACT"],
        b["POST_STATE_EXACT"],
        b["STATE_DELTA_EXACT"],
        b["CURRENT_PROVENANCE_EXACT"],
        not b["TRANSITION_ATTRIBUTION_EXACT"],
        not b["DELAYED_HISTORY_EXACT"],
        c["CHANGE_EVENT_TARGET_DIFF_EXACT"],
        not c["EVIDENCE_JUSTIFICATION_AVAILABLE"],
        not c["DELAYED_EVIDENCE_GROUNDED_AUDIT"],
    ])


def fault_eval(runtime_case, oracle_case):
    state = runtime_case["state"]
    event = runtime_case["event"]
    oevent = oracle_case["event"]
    oracle_transition = oracle_r.apply_event(
        oracle_case["state"], oevent
    )

    rejected = {}
    for name, fault in {
        "wrong_object": {"type": "wrong_object"},
        "wrong_source_version": {"type": "wrong_source_version"},
        "missing_applicability": {"type": "missing_applicability"},
    }.items():
        out = runtime_r.execute(state, event, fault=fault)
        rejected[name] = all([
            not out["transition"]["applicable"],
            out["before_state"] == out["after_state"],
        ])

    no_history = runtime_r.execute(state, event, drop_history=True)
    ev_no_history = evaluator_r.evaluate(
        no_history, oracle_transition, oracle_transition["state"], oevent
    )
    rejected["no_history_separation"] = all([
        ev_no_history["R4_POST_EVENT_RESULT"],
        ev_no_history["R5_SELECTIVE_UPDATE"],
        ev_no_history["R6_PROVENANCE"],
        ev_no_history["R7_TRANSITION_ATTRIBUTION"],
        not ev_no_history["R8_DELAYED_HISTORY"],
    ])
    return rejected


def execute_case(oracle_case, runtime_case):
    otransition = oracle_r.apply_event(
        oracle_case["state"], oracle_case["event"]
    )
    routput = runtime_r.execute(
        runtime_case["state"], runtime_case["event"]
    )
    evaluation = evaluator_r.evaluate(
        routput, otransition, otransition["state"], oracle_case["event"]
    )
    comparators = comparator_eval(routput, otransition)

    return {
        "transition_class": otransition.get("transition_class"),
        "substantive": bool(otransition.get("substantive")),
        "evaluation": evaluation,
        "comparators": comparators,
        "comparator_contract_pass": comparator_positive_ok(comparators),
        "fault_controls": fault_eval(runtime_case, oracle_case),
        "oracle_transition": {
            "event_id": otransition.get("event_id"),
            "object_id": otransition.get("object_id"),
            "target_property": otransition.get("target_property"),
            "evidence_id": otransition.get("evidence_id"),
            "transition_class": otransition.get("transition_class"),
            "before_state": otransition.get("before_state"),
            "after_state": otransition.get("after_state"),
        },
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    anchors = load_anchors()
    write_data_open_marker(anchors)

    raw_by_slug = {}
    source_manifest = {}
    download_rows = []

    try:
        for slug in EXPECTED_SLUGS:
            raw = download_one(slug, anchors[slug])
            raw_by_slug[slug] = raw
            digest = sha256(raw)
            source_manifest[slug] = digest
            cache_path = CACHE / f"{slug}.nt"
            cache_path.write_bytes(raw)
            download_rows.append({
                "slug": slug,
                "url": anchors[slug]["content_url"],
                "expected_size": int(anchors[slug]["content_size"]),
                "actual_size": len(raw),
                "sha256": digest,
            })
    except Exception as exc:
        write_json(RESULTS / "distribution_manifest_v1.json", {
            "complete": False,
            "downloads": download_rows,
            "error": repr(exc),
        })
        write_json(RESULTS / "authoritative_results_v1.json", {
            "study": "MODULE_R_VGW_FRESH_CONFIRMATORY_V1",
            "computational_disposition": "INVALID",
            "reason": "SOURCE_DOWNLOAD_OR_ACCOUNTING_FAILURE",
            "error": repr(exc),
        })
        raise

    manifest_sha = sha256(canonical_json(source_manifest))
    source_version = "VGW_MANIFEST::" + manifest_sha
    write_json(RESULTS / "distribution_manifest_v1.json", {
        "complete": len(source_manifest) == len(EXPECTED_SLUGS),
        "source_manifest_sha256": manifest_sha,
        "source_version": source_version,
        "distributions": download_rows,
    })

    oracle_extract = vgw_oracle.extract_population(
        raw_by_slug, source_version
    )
    runtime_extract = vgw_runtime.extract_population(
        raw_by_slug, source_version
    )

    extraction_exact = (
        normalized_extraction(oracle_extract)
        == normalized_extraction(runtime_extract)
    )

    oracle_cases = {
        x["f_number"]: x for x in oracle_extract["cases"]
    }
    runtime_cases = {
        x["f_number"]: x for x in runtime_extract["cases"]
    }

    disposition_counts = Counter(
        x["disposition"] for x in oracle_extract["cases"]
    )
    substantive = sorted(
        f for f, x in oracle_cases.items()
        if x["disposition"] == "SUBSTANTIVE_CANDIDATE"
    )
    nulls = sorted(
        f for f, x in oracle_cases.items()
        if x["disposition"] == "ADMISSIBLE_NULL_EVENT"
    )

    executions = []
    execution_failures = []

    if extraction_exact:
        for fnum in substantive + nulls:
            ocase = oracle_cases[fnum]
            rcase = runtime_cases[fnum]
            ex = execute_case(ocase, rcase)
            row = {
                **case_surface(ocase),
                "module_r": ex,
            }
            executions.append(row)

            expected_substantive = (
                ocase["disposition"] == "SUBSTANTIVE_CANDIDATE"
            )
            row_ok = all([
                ex["evaluation"]["reference_end_to_end_pass"],
                ex["comparator_contract_pass"],
                all(ex["fault_controls"].values()),
                (
                    ex["transition_class"]
                    == "R-U3_EVIDENTIAL_STATUS_REVISION"
                    if expected_substantive
                    else ex["transition_class"] == "ADMISSIBLE_NULL_EVENT"
                ),
                ex["substantive"] == expected_substantive,
            ])
            if not row_ok:
                execution_failures.append({
                    "f_number": fnum,
                    "case": row,
                })

    valid_record_counts = oracle_extract["records_by_slug"]
    invalid_by_slug = Counter(
        x["slug"] for x in oracle_extract["invalid_records"]
    )
    population_by_slug = {
        slug: {
            "valid_records": int(valid_record_counts.get(slug, 0)),
            "invalid_records": int(invalid_by_slug.get(slug, 0)),
            "total_accounted_records": (
                int(valid_record_counts.get(slug, 0))
                + int(invalid_by_slug.get(slug, 0))
            ),
        }
        for slug in EXPECTED_SLUGS
    }

    all_cases_manifest = [
        case_surface(x) for x in oracle_extract["cases"]
    ]

    computational_invalid = any([
        not extraction_exact,
        bool(execution_failures),
        set(oracle_cases) != set(runtime_cases),
    ])

    if computational_invalid:
        computational_disposition = "INVALID"
    elif len(substantive) > 0:
        computational_disposition = "COMPUTATIONAL_PASS_PENDING_DOCUMENTARY_AUDIT"
    elif len(nulls) > 0:
        computational_disposition = "NULL_REASSESSMENT_PENDING_DOCUMENTARY_FINALIZATION"
    else:
        computational_disposition = "NULL_APPLICABILITY_PENDING_DOCUMENTARY_FINALIZATION"

    result = {
        "study": "MODULE_R_VGW_FRESH_CONFIRMATORY_V1",
        "authority": "FIRST_DATA_OPEN_EXECUTION_ONLY",
        "git_context": git_context(),
        "source_manifest_sha256": manifest_sha,
        "source_version": source_version,
        "oracle_runtime_extraction_exact": extraction_exact,
        "population": {
            "per_slug": population_by_slug,
            "invalid_record_count": len(oracle_extract["invalid_records"]),
            "post1970_role_exclusion_count": len(
                oracle_extract["post1970_role_exclusions"]
            ),
            "unique_f_number_cases": len(oracle_extract["cases"]),
            "case_disposition_counts": dict(
                sorted(disposition_counts.items())
            ),
            "substantive_candidates": len(substantive),
            "admissible_null_events": len(nulls),
        },
        "all_cases_manifest": all_cases_manifest,
        "invalid_records": oracle_extract["invalid_records"],
        "post1970_role_exclusions": (
            oracle_extract["post1970_role_exclusions"]
        ),
        "executed_cases": executions,
        "execution_failure_manifest": execution_failures,
        "computational_disposition": computational_disposition,
        "claim_ceiling": [
            "This is the first opened VGW distribution execution for the frozen Module-R task.",
            "The task concerns project-relative Van Gogh attribution status, not true authorship.",
            "PASS requires the independent raw-triple documentary audit.",
        ],
    }
    write_json(RESULTS / "authoritative_results_v1.json", result)

    summary = {
        "study": result["study"],
        "source_manifest_sha256": manifest_sha,
        "oracle_runtime_extraction_exact": extraction_exact,
        "population": result["population"],
        "computational_disposition": computational_disposition,
        "executed_case_count": len(executions),
        "execution_failure_count": len(execution_failures),
        "authoritative_results_sha256": sha256(
            (RESULTS / "authoritative_results_v1.json").read_bytes()
        ),
    }
    write_json(RESULTS / "run_summary_v1.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if computational_invalid:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
