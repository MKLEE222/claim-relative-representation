from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[1] / "experiments"
O_DIR = EXP / "module_o_amp_fresh_holdout_v1"
L_DIR = EXP / "module_l_portable_object_claim_v1"

for p in (O_DIR, L_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import run_holdout as oh
import oracle_l


def claim_roles(row):
    return tuple(sorted(c.get("role") for c in row["oracle"].get("claims", [])))


def pair_taxonomy(row):
    claims = row["oracle"].get("_claims_private", [])
    out = Counter()
    for i, a in enumerate(claims):
        for b in claims[i + 1:]:
            if not a.get("_bounds") or not b.get("_bounds"):
                out["PAIR_WITHOUT_BOUNDS"] += 1
            elif oracle_l.base._disjoint(a["_bounds"], b["_bounds"]):
                out["DISJOINT_D1"] += 1
            elif oracle_l.base._overlap_nonidentical(a["_bounds"], b["_bounds"]):
                if a.get("uncertain") or b.get("uncertain"):
                    out["OVERLAP_NONIDENTICAL_UNCERTAIN_D2"] += 1
                else:
                    out["OVERLAP_NONIDENTICAL_CERTAIN"] += 1
            else:
                out["IDENTICAL_OR_NESTED_EQUIVALENT"] += 1
    return out


def origin_relation(row):
    doc = row["oracle"]
    origin = doc.get("_origin_private")
    roots = doc.get("_claims_private", [])
    if origin is None or not origin.get("_bounds"):
        return "NO_MACHINE_ORIGIN"
    if not roots:
        return "ORIGIN_WITHOUT_ROOT_CLAIMS"

    rel = Counter()
    for c in roots:
        if not c.get("_bounds"):
            rel["ROOT_WITHOUT_BOUNDS"] += 1
        elif oracle_l.base._disjoint(origin["_bounds"], c["_bounds"]):
            rel["ORIGIN_DISJOINT_ROOT"] += 1
        elif oracle_l.base._overlap_nonidentical(origin["_bounds"], c["_bounds"]):
            rel["ORIGIN_OVERLAP_NONIDENTICAL"] += 1
        else:
            rel["ORIGIN_COMPATIBLE_OR_IDENTICAL"] += 1
    return dict(rel)


def main():
    archive_url = (
        f"https://github.com/{oh.UPSTREAM_REPO}/archive/"
        f"{oh.UPSTREAM_COMMIT}.tar.gz"
    )
    archive_raw = oh.fetch(archive_url)
    rows, errors = oh.load_population(archive_raw)

    single = [
        r for r in rows
        if (r["oracle"].get("object_contract") or {}).get("status")
            == "SINGLE_PRIMARY_DOCUMENT_OBJECT"
    ]

    reason_counter = Counter()
    role_pattern_counter = Counter()
    role_presence = Counter()
    pair_counter = Counter()
    origin_status = Counter()
    warrant_change = Counter()
    correspondence = Counter()
    origin_rel_counter = Counter()
    per_doc = []

    for row in single:
        doc = row["oracle"]
        reasons = tuple(doc.get("full_trajectory_exclusion_reasons") or [])
        for x in reasons:
            reason_counter[x] += 1

        roles = claim_roles(row)
        role_pattern_counter[str(roles)] += 1
        for role in set(roles):
            role_presence[role] += 1

        pairs = pair_taxonomy(row)
        pair_counter.update(pairs)

        origin_status[doc.get("origin_contract_status") or "NONE"] += 1
        warrant_change[
            "CHANGED" if doc.get("warrant_root") != doc.get("warrant_after")
            else "UNCHANGED"
        ] += 1
        correspondence[
            "CORRESPONDENCE" if doc.get("is_correspondence") else "NOT_CORRESPONDENCE"
        ] += 1

        orel = origin_relation(row)
        if isinstance(orel, str):
            origin_rel_counter[orel] += 1
        else:
            for k, v in orel.items():
                origin_rel_counter[k] += v

        per_doc.append({
            "path": row["path"],
            "roles": list(roles),
            "claim_count": len(doc.get("claims", [])),
            "eligibility": doc.get("eligibility"),
            "origin_contract_status": doc.get("origin_contract_status"),
            "origin_present": doc.get("origin_claim") is not None,
            "root_warrant": doc.get("warrant_root"),
            "post_warrant": doc.get("warrant_after"),
            "warrant_changed": doc.get("warrant_root") != doc.get("warrant_after"),
            "exclusion_reasons": list(reasons),
            "pair_taxonomy": dict(pairs),
            "origin_relation": orel,
        })

    report = {
        "study": "AMP_POSTHOC_TRIGGER_DIAGNOSTIC_V1",
        "status": "POSTHOC_DIAGNOSTIC_ONLY_DOES_NOT_CHANGE_MODULE_O",
        "upstream": {
            "repo": oh.UPSTREAM_REPO,
            "commit": oh.UPSTREAM_COMMIT,
            "prefix": oh.PREFIX,
            "archive_sha256": oh.sha256(archive_raw),
        },
        "population": {
            "parsed": len(rows),
            "parse_errors": len(errors),
            "single_primary_objects": len(single),
        },
        "single_object_summary": {
            "is_correspondence": dict(correspondence),
            "active_role_presence": dict(role_presence),
            "active_role_patterns": dict(role_pattern_counter),
            "pair_taxonomy": dict(pair_counter),
            "origin_contract_status": dict(origin_status),
            "root_to_post_warrant": dict(warrant_change),
            "full_exclusion_reasons": dict(reason_counter),
            "origin_vs_root_pair_relations": dict(origin_rel_counter),
        },
        "documents": per_doc,
        "interpretation_guard": [
            "This diagnostic was run only after authoritative Module O completed.",
            "It cannot rescue, replace or reclassify the Module O NULL_APPLICABILITY result.",
            "Its sole purpose is to locate the missing eligibility ingredient for future study design.",
        ],
    }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "amp_posthoc_trigger_diagnostic_v1.json"
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": report["study"],
        "population": report["population"],
        "single_object_summary": report["single_object_summary"],
        "results_sha256": oh.sha256(out_path.read_bytes()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
