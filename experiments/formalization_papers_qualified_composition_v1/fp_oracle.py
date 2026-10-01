from __future__ import annotations

import copy
from datetime import datetime
from collections import defaultdict
from rdflib import Dataset, URIRef

import fp_constants as C


def _v(x):
    return str(x)


def _canon_time(value):
    s = str(value)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return s
    return dt.isoformat(timespec="microseconds")


def parse_trig(raw: bytes):
    ds = Dataset()
    ds.parse(data=raw.decode("utf-8"), format="trig")

    by_graph = defaultdict(set)
    all_triples = set()
    for s, p, o, g in ds.quads((None, None, None, None)):
        gn = _v(g.identifier if hasattr(g, "identifier") else g)
        row = (_v(s), _v(p), _v(o))
        by_graph[gn].add(row)
        all_triples.add(row)

    return _extract(by_graph, all_triples)


def _extract(by_graph, all_triples):
    assertion_graph = {}
    pubinfo_graph = {}
    nanopubs = set()

    for s, p, o in all_triples:
        if p == C.RDF_TYPE and o == C.NP_NANOPUBLICATION:
            nanopubs.add(s)
        elif p == C.NP_HAS_ASSERTION:
            assertion_graph[s] = o
            nanopubs.add(s)
        elif p == C.NP_HAS_PUBINFO:
            pubinfo_graph[s] = o
            nanopubs.add(s)

    creators = set()
    created = {}
    supersedes = []
    retracts = []
    updates = []
    roots = []
    reviews = []
    responses = []
    decisions = []

    for np in sorted(nanopubs):
        pg = pubinfo_graph.get(np)
        if pg and pg in by_graph:
            for s, p, o in by_graph[pg]:
                if s == np and p == C.DCT_CREATOR:
                    creators.add((np, o))
                if s == np and p == C.DCT_CREATED:
                    created[np] = _canon_time(o)
                if s == np and p == C.LF_IS_UPDATE_OF:
                    updates.append((np, o))
                if s == np and p == C.NPX_SUPERSEDES:
                    supersedes.append((np, o))

        ag = assertion_graph.get(np)
        if ag and ag in by_graph:
            triples = by_graph[ag]
            root_subjects = {
                s for s, p, o in triples
                if p == C.FRBR_PART_OF and o == C.SPECIAL_ISSUE
            }
            for root in root_subjects:
                if (root, C.PSO_WITH_STATUS, C.PSO_SUBMITTED) in triples:
                    roots.append((root, np))

            for s, p, o in triples:
                if p == C.RDF_TYPE and o == C.LF_REVIEW_COMMENT:
                    targets = sorted(
                        oo for ss, pp, oo in triples
                        if ss == s and pp == C.LF_REFERS_TO
                    )
                    reviews.append((np, s, tuple(targets)))

            response_subjects = {
                s for s, p, o in triples if p == C.LF_IS_RESPONSE_TO
            }
            for rs in response_subjects:
                review_targets = sorted(
                    o for s, p, o in triples
                    if s == rs and p == C.LF_IS_RESPONSE_TO
                )
                update_targets = sorted(
                    o for s, p, o in triples
                    if s == rs and p == C.LF_REFERS_TO
                )
                responses.append((
                    np, rs, tuple(review_targets), tuple(update_targets)
                ))

            for s, p, o in triples:
                if p == C.PSO_WITH_STATUS and o != C.PSO_SUBMITTED:
                    decisions.append((np, s, o))

            for s, p, o in triples:
                if p == C.NPX_RETRACTS:
                    retracts.append((np, o))
                if s == np and p == C.NPX_SUPERSEDES:
                    supersedes.append((np, o))

    # Some project generic queries allow update/supersedes/retracts in any graph.
    for s, p, o in all_triples:
        if p == C.NPX_RETRACTS:
            retracts.append((s, o))
        if p == C.NPX_SUPERSEDES:
            supersedes.append((s, o))
        if p == C.LF_IS_UPDATE_OF and s in nanopubs:
            updates.append((s, o))

    surface = {
        "roots": sorted(set(roots)),
        "reviews": sorted(set(reviews)),
        "updates": sorted(set(updates)),
        "responses": sorted(set(responses)),
        "decisions": sorted(set(decisions)),
        "supersedes": sorted(set(supersedes)),
        "retracts": sorted(set(retracts)),
        "creators": sorted(creators),
        "created": sorted(created.items()),
    }
    return surface


def initial_state(root, submission_np):
    return {
        "root": root,
        "submission_np": submission_np,
        "current_formalization": root,
        "current_update_np": None,
        "publication_status": C.PSO_SUBMITTED,
        "live_reviews": [],
        "responses": [],
        "history": [],
        "retracted": [],
    }


def qualify(state, event):
    kind = event["kind"]

    if kind == "REVIEW":
        if event["target_formalization"] != state["current_formalization"]:
            return (False, None, "RELATION_TARGET_NOT_LIVE")
        return (True, "RECORD_REVIEW", None)

    if kind == "UPDATE":
        if event["target_root"] != state["root"]:
            return (False, None, "UPDATE_TARGET_UNRESOLVED")
        if event["update_np"] in state["retracted"]:
            return (False, None, "UPDATE_TARGET_RETRACTED")
        return (True, "REPLACE_FORMALIZATION", None)

    if kind == "RESPONSE":
        if event["target_review_np"] not in state["live_reviews"]:
            return (False, None, "RESPONSE_REVIEW_TARGET_NOT_LIVE")
        if event["target_update_np"] != state["current_update_np"]:
            return (False, None, "RESPONSE_UPDATE_TARGET_NOT_LIVE")
        review_history = any(
            h.get("kind") == "REVIEW"
            and h.get("review_np") == event["target_review_np"]
            for h in state["history"]
        )
        update_history = any(
            h.get("kind") == "UPDATE"
            and h.get("update_np") == event["target_update_np"]
            for h in state["history"]
        )
        if not review_history or not update_history:
            return (False, None, "RESPONSE_TARGET_HISTORY_UNRESOLVED")
        if event["response_np"] in state["retracted"]:
            return (False, None, "RESPONSE_TARGET_RETRACTED")
        return (True, "RECORD_RESPONSE", None)

    if kind == "DECISION":
        if event["target_update_np"] != state["current_update_np"]:
            return (False, None, "DECISION_TARGET_NOT_CURRENT")
        return (True, "REVISE_PUBLICATION_STATUS", None)

    if kind == "RETRACT":
        if event["target_np"] not in (
            state["live_reviews"]
            + state["responses"]
            + ([state["current_update_np"]] if state["current_update_np"] else [])
        ):
            return (False, None, "RETRACTION_TARGET_UNKNOWN")
        return (True, "RETRACT_TARGET", None)

    return (False, None, "UNREGISTERED_EVENT_KIND")


def apply(state, event):
    before = copy.deepcopy(state)
    out = copy.deepcopy(state)
    ok, generator, reason = qualify(before, event)
    if not ok:
        return {
            "qualified": False,
            "generator": None,
            "reason": reason,
            "state": out,
        }

    if generator == "RECORD_REVIEW":
        out["live_reviews"].append(event["review_np"])
    elif generator == "REPLACE_FORMALIZATION":
        out["current_formalization"] = event["update_np"]
        out["current_update_np"] = event["update_np"]
    elif generator == "RECORD_RESPONSE":
        out["responses"].append(event["response_np"])
    elif generator == "REVISE_PUBLICATION_STATUS":
        out["publication_status"] = event["status"]
    elif generator == "RETRACT_TARGET":
        target = event["target_np"]
        out["retracted"].append(target)
        out["live_reviews"] = [x for x in out["live_reviews"] if x != target]
        out["responses"] = [x for x in out["responses"] if x != target]
        if out["current_update_np"] == target:
            out["current_update_np"] = None
            out["current_formalization"] = out["root"]

    h = copy.deepcopy(event)
    h["generator"] = generator
    out["history"].append(h)
    return {
        "qualified": True,
        "generator": generator,
        "reason": None,
        "state": out,
    }
