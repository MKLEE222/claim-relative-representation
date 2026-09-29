from __future__ import annotations

from collections import defaultdict

import vgw_contract_constants as C


def _decode_escape(text, i):
    ch = text[i]
    table = {
        "t": "\t",
        "b": "\b",
        "n": "\n",
        "r": "\r",
        "f": "\f",
        '"': '"',
        "\\": "\\",
    }
    if ch in table:
        return table[ch], i + 1
    if ch == "u":
        raw = text[i + 1:i + 5]
        if len(raw) != 4:
            raise ValueError("bad \\u escape")
        return chr(int(raw, 16)), i + 5
    if ch == "U":
        raw = text[i + 1:i + 9]
        if len(raw) != 8:
            raise ValueError("bad \\U escape")
        return chr(int(raw, 16)), i + 9
    raise ValueError("unsupported escape: " + ch)


def _read_iri(text, pos):
    if pos >= len(text) or text[pos] != "<":
        raise ValueError("IRI expected")
    end = text.find(">", pos + 1)
    if end < 0:
        raise ValueError("unterminated IRI")
    return ("I", text[pos + 1:end]), end + 1


def _read_bnode(text, pos):
    end = pos
    while end < len(text) and not text[end].isspace():
        end += 1
    token = text[pos:end]
    if not token.startswith("_:") or len(token) <= 2:
        raise ValueError("bad blank node")
    return ("B", token), end


def _read_literal(text, pos):
    if text[pos] != '"':
        raise ValueError("literal expected")
    i = pos + 1
    out = []
    while i < len(text):
        ch = text[i]
        if ch == '"':
            return ("L", "".join(out)), i + 1
        if ch == "\\":
            if i + 1 >= len(text):
                raise ValueError("trailing escape")
            decoded, i = _decode_escape(text, i + 1)
            out.append(decoded)
            continue
        out.append(ch)
        i += 1
    raise ValueError("unterminated literal")


def _skip_ws(text, pos):
    while pos < len(text) and text[pos].isspace():
        pos += 1
    return pos


def _read_term(text, pos, allow_literal=True):
    pos = _skip_ws(text, pos)
    if text.startswith("_:", pos):
        return _read_bnode(text, pos)
    if pos < len(text) and text[pos] == "<":
        return _read_iri(text, pos)
    if allow_literal and pos < len(text) and text[pos] == '"':
        return _read_literal(text, pos)
    raise ValueError("unsupported term")


def parse_nt(raw: bytes):
    triples = []
    for line_no, raw_line in enumerate(raw.decode("utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        s, p0 = _read_term(line, 0, allow_literal=False)
        if s[0] == "L":
            raise ValueError(f"literal subject at line {line_no}")
        pred, p1 = _read_term(line, p0, allow_literal=False)
        if pred[0] != "I":
            raise ValueError(f"non-IRI predicate at line {line_no}")
        obj, p2 = _read_term(line, p1, allow_literal=True)
        p2 = _skip_ws(line, p2)

        # Optional language/datatype suffix on literals.
        if obj[0] == "L":
            if line.startswith("@", p2):
                p2 += 1
                while p2 < len(line) and not line[p2].isspace():
                    p2 += 1
            elif line.startswith("^^", p2):
                p2 += 2
                _, p2 = _read_term(line, p2, allow_literal=False)
            p2 = _skip_ws(line, p2)

        if p2 >= len(line) or line[p2] != ".":
            raise ValueError(f"missing terminal dot at line {line_no}")

        triples.append((s, pred[1], obj))
    return triples


class MiniGraph:
    def __init__(self, triples):
        self.out = defaultdict(list)
        self.types = defaultdict(set)
        for s, p, o in triples:
            sid = self._node_id(s)
            self.out[(sid, p)].append(o)
            if p == C.RDF_TYPE and o[0] in {"I", "B"}:
                self.types[sid].add(self._node_id(o))

    @staticmethod
    def _node_id(term):
        return term[1]

    def objects(self, subject, predicate):
        return list(self.out.get((subject, predicate), []))

    def has_type(self, subject, type_uri):
        return type_uri in self.types.get(subject, set())

    def subjects_of_type(self, type_uri):
        return sorted(
            s for s, types in self.types.items()
            if type_uri in types
        )


def _node_value(term):
    if term[0] not in {"I", "B"}:
        return None
    return term[1]


def _literal_value(term):
    return term[1] if term[0] == "L" else None


def _extract_records(raw: bytes, slug: str):
    g = MiniGraph(parse_nt(raw))
    records = []
    invalid = []

    for obj in g.subjects_of_type(C.E22_HUMAN_MADE_OBJECT):
        identifier_nodes = []
        f_values = []
        for ident_term in g.objects(obj, C.P1_IDENTIFIED_BY):
            ident = _node_value(ident_term)
            if ident is None or not g.has_type(ident, C.E42_IDENTIFIER):
                continue
            type_values = {
                _node_value(x)
                for x in g.objects(ident, C.P2_HAS_TYPE)
                if _node_value(x) is not None
            }
            if C.F_NUMBER_TYPE not in type_values:
                continue
            vals = [
                _literal_value(x)
                for x in g.objects(ident, C.P190_SYMBOLIC_CONTENT)
                if _literal_value(x) is not None
            ]
            identifier_nodes.append(ident)
            f_values.extend(vals)

        if len(identifier_nodes) != 1 or len(f_values) != 1:
            invalid.append({
                "slug": slug,
                "object_uri": obj,
                "disposition": "INVALID_F_NUMBER_CARDINALITY",
                "identifier_nodes": sorted(identifier_nodes),
                "f_values": sorted(f_values),
            })
            continue

        productions = []
        for pterm in g.objects(obj, C.P108I_WAS_PRODUCED_BY):
            p = _node_value(pterm)
            if p is not None and g.has_type(p, C.E12_PRODUCTION):
                productions.append(p)

        direct_van_gogh = False
        qualifying_assignments = []
        unknown_assignments = []

        if len(productions) == 1:
            production = productions[0]
            direct_actors = {
                _node_value(x)
                for x in g.objects(production, C.P14_CARRIED_OUT_BY)
                if _node_value(x) is not None
            }
            direct_van_gogh = bool(direct_actors & set(C.VAN_GOGH_IDS))

            for aterm in g.objects(production, C.P141I_WAS_ASSIGNED_BY):
                assignment = _node_value(aterm)
                if (
                    assignment is None
                    or not g.has_type(assignment, C.E13_ATTRIBUTE_ASSIGNMENT)
                ):
                    continue
                assignment_types = {
                    _node_value(x)
                    for x in g.objects(assignment, C.P2_HAS_TYPE)
                    if _node_value(x) is not None
                }
                assigned_nodes = [
                    _node_value(x)
                    for x in g.objects(assignment, C.P141_ASSIGNED)
                    if _node_value(x) is not None
                ]
                assigned_van_gogh = False
                if len(assigned_nodes) == 1:
                    assigned_actors = {
                        _node_value(x)
                        for x in g.objects(
                            assigned_nodes[0], C.P14_CARRIED_OUT_BY
                        )
                        if _node_value(x) is not None
                    }
                    assigned_van_gogh = bool(
                        assigned_actors & set(C.VAN_GOGH_IDS)
                    )

                responsible = sorted(
                    _node_value(x)
                    for x in g.objects(assignment, C.P14_CARRIED_OUT_BY)
                    if _node_value(x) is not None
                )
                row = {
                    "assignment_id": assignment,
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
            "object_uri": obj,
            "f_number": f_values[0],
            "production_count": len(productions),
            "production_uri": productions[0] if len(productions) == 1 else None,
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
            "evidence_locator": current["slug"] + "::" + assignment["assignment_id"],
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
            "evidence_id": current["production_uri"],
            "evidence_locator": current["slug"] + "::" + str(current["production_uri"]),
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
        "engine": "LEXICAL_NTRIPLES_RUNTIME",
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
