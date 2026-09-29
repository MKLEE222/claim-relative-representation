from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from rdflib import Graph, Literal, URIRef

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "vgw_fresh_confirmatory_v1"
CACHE = HERE / "results" / "vgw_fresh_source_cache_v1"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import vgw_contract_constants as C

AUTH = RESULTS / "authoritative_results_v1.json"
DIST = RESULTS / "distribution_manifest_v1.json"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, obj):
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_graph(slug):
    raw = (CACHE / f"{slug}.nt").read_bytes()
    g = Graph()
    g.parse(data=raw.decode("utf-8"), format="nt")
    return g, raw


def objects(g, s, p):
    return list(g.objects(s, URIRef(p)))


def has_type(g, s, t):
    return (s, URIRef(C.RDF_TYPE), URIRef(t)) in g


def exact_f_objects(g, fnum):
    found = []
    for obj in set(
        g.subjects(
            URIRef(C.RDF_TYPE),
            URIRef(C.E22_HUMAN_MADE_OBJECT),
        )
    ):
        if not isinstance(obj, URIRef):
            continue
        matching_ids = []
        for ident in objects(g, obj, C.P1_IDENTIFIED_BY):
            if not has_type(g, ident, C.E42_IDENTIFIER):
                continue
            if URIRef(C.F_NUMBER_TYPE) not in objects(
                g, ident, C.P2_HAS_TYPE
            ):
                continue
            vals = [
                str(x)
                for x in objects(g, ident, C.P190_SYMBOLIC_CONTENT)
                if isinstance(x, Literal)
            ]
            if vals == [fnum]:
                matching_ids.append(ident)
        if len(matching_ids) == 1:
            found.append(obj)
    return sorted(found, key=str)


def audit_one(row, graphs, raw_hashes, frozen_hashes):
    fnum = row["f_number"]
    current_slug = row["current_provider_slug"]
    expected_assignment = row["evidence_id"]
    expected_responsible = row["responsible_agent"]

    baseline_g = graphs[C.BASELINE_SLUG]
    current_g = graphs[current_slug]

    baseline_matches = exact_f_objects(baseline_g, fnum)
    current_matches = exact_f_objects(current_g, fnum)

    checks = {}
    checks["baseline_unique_f_number_object"] = (
        len(baseline_matches) == 1
        and str(baseline_matches[0]) == row["baseline_object_uri"]
    )
    checks["current_unique_f_number_object"] = (
        len(current_matches) == 1
        and str(current_matches[0]) == row["current_object_uri"]
    )
    checks["baseline_distribution_sha"] = (
        raw_hashes[C.BASELINE_SLUG] == frozen_hashes[C.BASELINE_SLUG]
    )
    checks["current_distribution_sha"] = (
        raw_hashes[current_slug] == frozen_hashes[current_slug]
    )

    if len(current_matches) != 1:
        checks.update({
            "one_current_production": False,
            "one_previous_assignment": False,
            "assignment_addressable": False,
            "assignment_type_previous_attribution": False,
            "one_assigned_production": False,
            "assigned_production_van_gogh": False,
            "evidence_id_exact": False,
            "responsible_agent_exact": False,
        })
        return {
            "f_number": fnum,
            "current_provider_slug": current_slug,
            "checks": checks,
            "pass": all(checks.values()),
        }

    current_obj = current_matches[0]
    prods = [
        p for p in objects(current_g, current_obj, C.P108I_WAS_PRODUCED_BY)
        if has_type(current_g, p, C.E12_PRODUCTION)
    ]
    checks["one_current_production"] = len(prods) == 1

    assignments = []
    if len(prods) == 1:
        for a in objects(current_g, prods[0], C.P141I_WAS_ASSIGNED_BY):
            if not has_type(current_g, a, C.E13_ATTRIBUTE_ASSIGNMENT):
                continue
            types = {str(x) for x in objects(current_g, a, C.P2_HAS_TYPE)}
            assigned = objects(current_g, a, C.P141_ASSIGNED)
            if C.PREVIOUS_ATTRIBUTION_TYPE not in types:
                continue
            if len(assigned) != 1:
                continue
            actors = {
                str(x)
                for x in objects(
                    current_g, assigned[0], C.P14_CARRIED_OUT_BY
                )
            }
            if not (actors & set(C.VAN_GOGH_IDS)):
                continue
            assignments.append(a)

    checks["one_previous_assignment"] = len(assignments) == 1
    checks["assignment_addressable"] = (
        len(assignments) == 1 and isinstance(assignments[0], URIRef)
    )

    if len(assignments) == 1:
        assignment = assignments[0]
        types = {str(x) for x in objects(current_g, assignment, C.P2_HAS_TYPE)}
        checks["assignment_type_previous_attribution"] = (
            C.PREVIOUS_ATTRIBUTION_TYPE in types
        )

        assigned = objects(current_g, assignment, C.P141_ASSIGNED)
        checks["one_assigned_production"] = len(assigned) == 1
        if len(assigned) == 1:
            actors = {
                str(x)
                for x in objects(
                    current_g, assigned[0], C.P14_CARRIED_OUT_BY
                )
            }
            checks["assigned_production_van_gogh"] = bool(
                actors & set(C.VAN_GOGH_IDS)
            )
        else:
            checks["assigned_production_van_gogh"] = False

        checks["evidence_id_exact"] = (
            str(assignment) == expected_assignment
        )
        responsible = sorted(
            str(x)
            for x in objects(
                current_g, assignment, C.P14_CARRIED_OUT_BY
            )
        )
        observed_responsible = (
            responsible[0] if len(responsible) == 1 else None
        )
        checks["responsible_agent_exact"] = (
            observed_responsible == expected_responsible
        )
    else:
        checks.update({
            "assignment_type_previous_attribution": False,
            "one_assigned_production": False,
            "assigned_production_van_gogh": False,
            "evidence_id_exact": False,
            "responsible_agent_exact": False,
        })

    return {
        "f_number": fnum,
        "baseline_object_uri": row["baseline_object_uri"],
        "current_object_uri": row["current_object_uri"],
        "current_provider_slug": current_slug,
        "evidence_id": expected_assignment,
        "responsible_agent": expected_responsible,
        "checks": checks,
        "pass": all(checks.values()),
    }


def main():
    auth = json.loads(AUTH.read_text(encoding="utf-8"))
    dist = json.loads(DIST.read_text(encoding="utf-8"))

    frozen_hashes = {
        x["slug"]: x["sha256"] for x in dist["distributions"]
    }
    graphs = {}
    raw_hashes = {}
    for slug in frozen_hashes:
        g, raw = load_graph(slug)
        graphs[slug] = g
        raw_hashes[slug] = sha256(raw)

    source_hashes_exact = raw_hashes == frozen_hashes

    substantive = [
        x for x in auth["executed_cases"]
        if x["disposition"] == "SUBSTANTIVE_CANDIDATE"
    ]
    rows = [
        audit_one(x, graphs, raw_hashes, frozen_hashes)
        for x in substantive
    ]

    report = {
        "study": "MODULE_R_VGW_FRESH_DOCUMENTARY_AUDIT_V1",
        "independence": (
            "RAW_NTRIPLES_RDFLIB_AUDIT_WITHOUT_VGW_ORACLE_OR_RUNTIME_IMPORT"
        ),
        "source_manifest_sha256": auth["source_manifest_sha256"],
        "substantive_candidate_count": len(substantive),
        "audited_count": len(rows),
        "source_cache_hashes_match_manifest": source_hashes_exact,
        "rows": rows,
        "all_substantive_audits_pass": (
            source_hashes_exact and all(x["pass"] for x in rows)
        ),
    }
    write_json(RESULTS / "documentary_audit_v1.json", report)
    print(json.dumps({
        "study": report["study"],
        "substantive_candidate_count": len(substantive),
        "audited_count": len(rows),
        "source_cache_hashes_match_manifest": source_hashes_exact,
        "passed": sum(x["pass"] for x in rows),
        "failed": sum(not x["pass"] for x in rows),
        "all_substantive_audits_pass": report[
            "all_substantive_audits_pass"
        ],
        "documentary_audit_sha256": sha256(
            (RESULTS / "documentary_audit_v1.json").read_bytes()
        ),
    }, ensure_ascii=False, indent=2))

    if not report["all_substantive_audits_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
