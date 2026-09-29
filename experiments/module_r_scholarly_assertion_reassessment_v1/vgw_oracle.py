from __future__ import annotations

from collections import defaultdict
from rdflib import Graph, URIRef
from rdflib.term import BNode, Literal

import vgw_contract_constants as C


def _term_id(term):
    if isinstance(term, BNode):
        return "_:" + str(term)
    return str(term)


def _literal_text(term):
    return str(term) if isinstance(term, Literal) else None


def _objects(g, subject, predicate):
    return list(g.objects(subject, URIRef(predicate)))


def _has_type(g, subject, type_uri):
    return (subject, URIRef(C.RDF_TYPE), URIRef(type_uri)) in g


def _extract_records(raw: bytes, slug: str):
    g = Graph()
    g.parse(data=raw.decode("utf-8"), format="nt")

    records = []
    invalid = []

    for obj in sorted(
        set(g.subjects(URIRef(C.RDF_TYPE), URIRef(C.E22_HUMAN_MADE_OBJECT))),
        key=_term_id,
    ):
        if not isinstance(obj, URIRef):
            invalid.append({
                "slug": slug,
                "object_uri": _term_id(obj),
                "disposition": "NON_ADDRESSABLE_ARTWORK_OBJECT",
                "identifier_nodes": [],
                "f_values": [],
            })
            continue
        identifier_nodes = []
        f_values = []
        for ident in _objects(g, obj, C.P1_IDENTIFIED_BY):
            if not _has_type(g, ident, C.E42_IDENTIFIER):
                continue
            if URIRef(C.F_NUMBER_TYPE) not in _objects(g, ident, C.P2_HAS_TYPE):
                continue
            vals = [
                _literal_text(x)
                for x in _objects(g, ident, C.P190_SYMBOLIC_CONTENT)
                if isinstance(x, Literal)
            ]
            identifier_nodes.append(_term_id(ident))
            f_values.extend(v for v in vals if v is not None)

        if len(identifier_nodes) != 1 or len(f_values) != 1:
            invalid.append({
                "slug": slug,
                "object_uri": _term_id(obj),
                "disposition": "INVALID_F_NUMBER_CARDINALITY",
                "identifier_nodes": sorted(identifier_nodes),
                "f_values": sorted(f_values),
            })
            continue

        f_number = f_values[0]
        productions = [
            p for p in _objects(g, obj, C.P108I_WAS_PRODUCED_BY)
            if _has_type(g, p, C.E12_PRODUCTION)
        ]

        direct_van_gogh = False
        qualifying_assignments = []
        unknown_assignments = []

        if len(productions) == 1:
            production = productions[0]
            direct_actors = {
                _term_id(x) for x in _objects(g, production, C.P14_CARRIED_OUT_BY)
            }
            direct_van_gogh = bool(direct_actors & set(C.VAN_GOGH_IDS))

            for assignment in _objects(g, production, C.P141I_WAS_ASSIGNED_BY):
                if not _has_type(g, assignment, C.E13_ATTRIBUTE_ASSIGNMENT):
                    continue
                assignment_types = {
                    _term_id(x) for x in _objects(g, assignment, C.P2_HAS_TYPE)
                }
                assigned_nodes = _objects(g, assignment, C.P141_ASSIGNED)
                assigned_van_gogh = False
                if len(assigned_nodes) == 1:
                    assigned_actors = {
                        _term_id(x)
                        for x in _objects(
                            g, assigned_nodes[0], C.P14_CARRIED_OUT_BY
                        )
                    }
                    assigned_van_gogh = bool(
                        assigned_actors & set(C.VAN_GOGH_IDS)
                    )

                responsible = sorted(
                    _term_id(x)
                    for x in _objects(g, assignment, C.P14_CARRIED_OUT_BY)
                )
                row = {
                    "assignment_id": _term_id(assignment),
                    "assignment_addressable": isinstance(assignment, URIRef),
                    "assignment_types": sorted(assignment_types),
                    "assigned_van_gogh": assigned_van_gogh,
                    "responsible_agents": responsible,
                }
                if (
                    C.PREVIOUS_ATTRIBUTION_TYPE in assignment_types
                    and assigned_van_gogh
                ):
                    qualifying_assignments.append(row)
                else:
                    unknown_assignments.append(row)

        records.append({
            "slug": slug,
            "object_uri": _term_id(obj),
            "f_number": f_number,
            "production_count": len(productions),
            "production_uri": _term_id(productions[0]) if len(productions) == 1 else None,
            "direct_van_gogh": direct_van_gogh,
            "qualifying_assignments": qualifying_assignments,
            "unknown_assignments": unknown_assignments,
        })

    return records, invalid


def _state_event_for_pair(base, current, source_version):
    object_id = base["f_number"]
    baseline_claim = {
        "claim_id": "BASELINE::" + object_id,
        "object_id": object_id,
        "target_property": C.TARGET_PROPERTY,
        "value": C.VALUE_VAN_GOGH,
        "status": C.STATUS_ATTRIBUTED,
        "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
        "source_repository": C.STUDY_REPOSITORY,
        "source_version": source_version,
        "source_id": base["object_uri"],
        "source_locator": C.BASELINE_SLUG + "::" + base["object_uri"],
        "responsible_agent": "DE_LA_FAILLE_1970",
    }
    state = {
        "object_id": object_id,
        "source_repository": C.STUDY_REPOSITORY,
        "source_version": source_version,
        "registered_targets": [C.TARGET_PROPERTY],
        "assertions": {C.TARGET_PROPERTY: [baseline_claim]},
        "evidence_ledger": [],
        "event_ledger": [],
        "transition_ledger": [],
    }

    q = current["qualifying_assignments"]
    direct = current["direct_van_gogh"]

    if current["production_count"] != 1:
        return {
            "disposition": "INVALID_PRODUCTION_CARDINALITY",
            "state": None,
            "event": None,
        }
    if direct and q:
        return {
            "disposition": "CONFLICTING_CURRENT_ATTRIBUTION_ENCODING",
            "state": None,
            "event": None,
        }
    if len(q) > 1:
        return {
            "disposition": "MULTIPLE_PREVIOUS_ATTRIBUTION_ASSIGNMENTS",
            "state": None,
            "event": None,
        }

    if len(q) == 1:
        assignment = q[0]
        if not assignment.get("assignment_addressable"):
            return {
                "disposition": "NON_ADDRESSABLE_REASSESSMENT_EVENT",
                "state": None,
                "event": None,
            }
        responsible = (
            assignment["responsible_agents"][0]
            if len(assignment["responsible_agents"]) == 1
            else None
        )
        event = {
            "event_id": "VGW_REASSESS::" + object_id,
            "event_class": "SCHOLARLY_REASSESSMENT",
            "object_id": object_id,
            "target_property": C.TARGET_PROPERTY,
            "source_repository": C.STUDY_REPOSITORY,
            "source_version": source_version,
            "evidence_id": assignment["assignment_id"],
            "evidence_locator": (
                current["slug"] + "::" + assignment["assignment_id"]
            ),
            "responsible_agent": responsible,
            "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
            "operation": "REVISE_STATUS",
            "new_claim_id": "CURRENT::" + object_id,
            "value": C.VALUE_VAN_GOGH,
            "status": C.STATUS_PREVIOUS,
        }
        return {
            "disposition": "SUBSTANTIVE_CANDIDATE",
            "expected_transition_class": "R-U3_EVIDENTIAL_STATUS_REVISION",
            "state": state,
            "event": event,
        }

    if direct:
        event = {
            "event_id": "VGW_CURRENT::" + object_id,
            "event_class": "SCHOLARLY_REASSESSMENT",
            "object_id": object_id,
            "target_property": C.TARGET_PROPERTY,
            "source_repository": C.STUDY_REPOSITORY,
            "source_version": source_version,
            "evidence_id": current["object_uri"],
            "evidence_locator": (
                current["slug"]
                + "::"
                + current["object_uri"]
                + "::"
                + C.P108I_WAS_PRODUCED_BY
            ),
            "responsible_agent": None,
            "applicability_class": "ASSERTION_LEVEL_ADMISSIBLE",
            "operation": "REVISE_STATUS",
            "new_claim_id": "CURRENT::" + object_id,
            "value": C.VALUE_VAN_GOGH,
            "status": C.STATUS_ATTRIBUTED,
        }
        return {
            "disposition": "ADMISSIBLE_NULL_EVENT",
            "expected_transition_class": "ADMISSIBLE_NULL_EVENT",
            "state": state,
            "event": event,
        }

    return {
        "disposition": "UNREGISTERED_CURRENT_ATTRIBUTION_STATUS",
        "state": None,
        "event": None,
    }


def extract_population(dataset_bytes: dict[str, bytes], source_version: str):
    by_slug = {}
    invalid_records = []
    for slug, raw in dataset_bytes.items():
        recs, invalid = _extract_records(raw, slug)
        by_slug[slug] = recs
        invalid_records.extend(invalid)

    baseline_by_f = defaultdict(list)
    for row in by_slug.get(C.BASELINE_SLUG, []):
        baseline_by_f[row["f_number"]].append(row)

    current_by_f = defaultdict(list)
    for slug in C.CURRENT_PROVIDER_SLUGS:
        for row in by_slug.get(slug, []):
            current_by_f[row["f_number"]].append(row)

    post1970 = [
        {
            "f_number": row["f_number"],
            "object_uri": row["object_uri"],
            "disposition": "NO_1970_BASELINE_BY_DATASET_ROLE",
        }
        for row in by_slug.get(C.POST1970_SLUG, [])
    ]

    all_keys = sorted(set(baseline_by_f) | set(current_by_f))
    cases = []
    for fnum in all_keys:
        b = baseline_by_f.get(fnum, [])
        c = current_by_f.get(fnum, [])
        if len(b) == 0:
            cases.append({
                "f_number": fnum,
                "disposition": "NO_1970_BASELINE",
                "state": None,
                "event": None,
            })
            continue
        if len(b) > 1:
            cases.append({
                "f_number": fnum,
                "disposition": "AMBIGUOUS_1970_BASELINE",
                "state": None,
                "event": None,
            })
            continue
        if len(c) == 0:
            cases.append({
                "f_number": fnum,
                "disposition": "NO_CURRENT_PROVIDER_OBJECT",
                "state": None,
                "event": None,
            })
            continue
        if len(c) > 1:
            cases.append({
                "f_number": fnum,
                "disposition": "MULTIPLE_CURRENT_PROVIDER_OBJECTS",
                "state": None,
                "event": None,
            })
            continue

        mapped = _state_event_for_pair(b[0], c[0], source_version)
        mapped["f_number"] = fnum
        mapped["baseline_object_uri"] = b[0]["object_uri"]
        mapped["current_object_uri"] = c[0]["object_uri"]
        mapped["current_provider_slug"] = c[0]["slug"]
        cases.append(mapped)

    return {
        "engine": "RDFLIB_ORACLE",
        "records_by_slug": {
            k: len(v) for k, v in sorted(by_slug.items())
        },
        "invalid_records": sorted(
            invalid_records,
            key=lambda x: (x["slug"], x["object_uri"]),
        ),
        "post1970_role_exclusions": sorted(
            post1970,
            key=lambda x: (x["f_number"], x["object_uri"]),
        ),
        "cases": sorted(cases, key=lambda x: x["f_number"]),
    }
