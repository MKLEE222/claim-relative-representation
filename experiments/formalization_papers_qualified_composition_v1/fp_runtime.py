from __future__ import annotations

import copy
from datetime import datetime
from collections import defaultdict

from pyoxigraph import RdfFormat, Store

import fp_constants as C


def _v(term):
    if hasattr(term, "value"):
        return str(term.value)
    return str(term)


def _canon_time(value):
    s = str(value)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return s
    return dt.isoformat(timespec="microseconds")


def parse_trig(raw: bytes):
    store = Store()
    store.load(input=raw, format=RdfFormat.TRIG)

    by_graph = defaultdict(set)
    all_triples = set()
    for q in store:
        gn = _v(q.graph_name)
        row = (_v(q.subject), _v(q.predicate), _v(q.object))
        by_graph[gn].add(row)
        all_triples.add(row)

    nanopubs = set()
    assertion_graph = {}
    pubinfo_graph = {}

    for row in all_triples:
        s, p, o = row
        if p == C.NP_HAS_ASSERTION:
            assertion_graph[s] = o
            nanopubs.add(s)
        if p == C.NP_HAS_PUBINFO:
            pubinfo_graph[s] = o
            nanopubs.add(s)
        if p == C.RDF_TYPE and o == C.NP_NANOPUBLICATION:
            nanopubs.add(s)

    roots = set()
    reviews = set()
    updates = set()
    responses = set()
    decisions = set()
    supersedes = set()
    retracts = set()
    creators = set()
    created = {}

    for np in nanopubs:
        ag = assertion_graph.get(np)
        pg = pubinfo_graph.get(np)

        if pg in by_graph:
            triples = by_graph[pg]
            for s, p, o in triples:
                if s == np and p == C.DCT_CREATOR:
                    creators.add((np, o))
                elif s == np and p == C.DCT_CREATED:
                    created[np] = _canon_time(o)
                elif s == np and p == C.LF_IS_UPDATE_OF:
                    updates.add((np, o))
                elif s == np and p == C.NPX_SUPERSEDES:
                    supersedes.add((np, o))

        if ag in by_graph:
            triples = by_graph[ag]
            subjects = {s for s, _, _ in triples}

            for sub in subjects:
                if (
                    (sub, C.FRBR_PART_OF, C.SPECIAL_ISSUE) in triples
                    and (sub, C.PSO_WITH_STATUS, C.PSO_SUBMITTED) in triples
                ):
                    roots.add((sub, np))

                if (sub, C.RDF_TYPE, C.LF_REVIEW_COMMENT) in triples:
                    targets = tuple(sorted(
                        o for s, p, o in triples
                        if s == sub and p == C.LF_REFERS_TO
                    ))
                    reviews.add((np, sub, targets))

                review_targets = tuple(sorted(
                    o for s, p, o in triples
                    if s == sub and p == C.LF_IS_RESPONSE_TO
                ))
                if review_targets:
                    update_targets = tuple(sorted(
                        o for s, p, o in triples
                        if s == sub and p == C.LF_REFERS_TO
                    ))
                    responses.add(
                        (np, sub, review_targets, update_targets)
                    )

            for s, p, o in triples:
                if p == C.PSO_WITH_STATUS and o != C.PSO_SUBMITTED:
                    decisions.add((np, s, o))
                if p == C.NPX_RETRACTS:
                    retracts.add((np, o))
                if s == np and p == C.NPX_SUPERSEDES:
                    supersedes.add((np, o))

    # Broad generic relation capture, independently of graph placement.
    for s, p, o in all_triples:
        if p == C.LF_IS_UPDATE_OF and s in nanopubs:
            updates.add((s, o))
        elif p == C.NPX_SUPERSEDES:
            supersedes.add((s, o))
        elif p == C.NPX_RETRACTS:
            retracts.add((s, o))

    return {
        "roots": sorted(roots),
        "reviews": sorted(reviews),
        "updates": sorted(updates),
        "responses": sorted(responses),
        "decisions": sorted(decisions),
        "supersedes": sorted(supersedes),
        "retracts": sorted(retracts),
        "creators": sorted(creators),
        "created": sorted(created.items()),
    }


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
    k = event.get("kind")

    if k == "REVIEW":
        target_ok = event.get("target_formalization") == state.get(
            "current_formalization"
        )
        return (
            (True, "RECORD_REVIEW", None)
            if target_ok
            else (False, None, "RELATION_TARGET_NOT_LIVE")
        )

    if k == "UPDATE":
        if event.get("target_root") != state.get("root"):
            return (False, None, "UPDATE_TARGET_UNRESOLVED")
        if event.get("update_np") in state.get("retracted", []):
            return (False, None, "UPDATE_TARGET_RETRACTED")
        return (True, "REPLACE_FORMALIZATION", None)

    if k == "RESPONSE":
        review = event.get("target_review_np")
        update = event.get("target_update_np")
        if review not in state.get("live_reviews", []):
            return (False, None, "RESPONSE_REVIEW_TARGET_NOT_LIVE")
        if update != state.get("current_update_np"):
            return (False, None, "RESPONSE_UPDATE_TARGET_NOT_LIVE")

        seen_review = False
        seen_update = False
        for h in state.get("history", []):
            if h.get("kind") == "REVIEW" and h.get("review_np") == review:
                seen_review = True
            if h.get("kind") == "UPDATE" and h.get("update_np") == update:
                seen_update = True
        if not (seen_review and seen_update):
            return (False, None, "RESPONSE_TARGET_HISTORY_UNRESOLVED")
        if event.get("response_np") in state.get("retracted", []):
            return (False, None, "RESPONSE_TARGET_RETRACTED")
        return (True, "RECORD_RESPONSE", None)

    if k == "DECISION":
        if event.get("target_update_np") != state.get("current_update_np"):
            return (False, None, "DECISION_TARGET_NOT_CURRENT")
        return (True, "REVISE_PUBLICATION_STATUS", None)

    if k == "RETRACT":
        target = event.get("target_np")
        live = set(state.get("live_reviews", []))
        live.update(state.get("responses", []))
        if state.get("current_update_np"):
            live.add(state["current_update_np"])
        if target not in live:
            return (False, None, "RETRACTION_TARGET_UNKNOWN")
        return (True, "RETRACT_TARGET", None)

    return (False, None, "UNREGISTERED_EVENT_KIND")


def execute(state, event):
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    ok, gen, reason = qualify(before, event)

    if not ok:
        return {
            "qualified": False,
            "generator": None,
            "reason": reason,
            "state": after,
        }

    if gen == "RECORD_REVIEW":
        after["live_reviews"] = after["live_reviews"] + [event["review_np"]]

    elif gen == "REPLACE_FORMALIZATION":
        after["current_formalization"] = event["update_np"]
        after["current_update_np"] = event["update_np"]

    elif gen == "RECORD_RESPONSE":
        after["responses"] = after["responses"] + [event["response_np"]]

    elif gen == "REVISE_PUBLICATION_STATUS":
        after["publication_status"] = event["status"]

    elif gen == "RETRACT_TARGET":
        tgt = event["target_np"]
        after["retracted"] = after["retracted"] + [tgt]
        after["live_reviews"] = [x for x in after["live_reviews"] if x != tgt]
        after["responses"] = [x for x in after["responses"] if x != tgt]
        if after["current_update_np"] == tgt:
            after["current_update_np"] = None
            after["current_formalization"] = after["root"]

    history_row = copy.deepcopy(event)
    history_row["generator"] = gen
    after["history"] = after["history"] + [history_row]

    return {
        "qualified": True,
        "generator": gen,
        "reason": None,
        "state": after,
    }
