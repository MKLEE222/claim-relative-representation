from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from rdflib import Dataset

NP = "http://www.nanopub.org/nschema#"
NPX = "http://purl.org/nanopub/x/"
LF = "https://w3id.org/linkflows/reviews/"
PSO = "http://purl.org/spar/pso/"
FRBR = "http://purl.org/vocab/frbr/core#"
DCT = "http://purl.org/dc/terms/"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

SPECIAL_ISSUE = (
    "https://w3id.org/linkflows/formalization-papers/"
    "DataScienceSpecialIssue"
)
NP_HAS_ASSERTION = NP + "hasAssertion"
NP_HAS_PUBINFO = NP + "hasPublicationInfo"
RDF_TYPE = RDF + "type"
FRBR_PART_OF = FRBR + "partOf"
PSO_WITH_STATUS = PSO + "withStatus"
PSO_SUBMITTED = PSO + "submitted"
LF_REVIEW_COMMENT = LF + "ReviewComment"
LF_REFERS_TO = LF + "refersTo"
LF_IS_RESPONSE_TO = LF + "isResponseTo"
LF_IS_UPDATE_OF = LF + "isUpdateOf"
NPX_SUPERSEDES = NPX + "supersedes"
NPX_RETRACTS = NPX + "retracts"
DCT_CREATOR = DCT + "creator"
DCT_CREATED = DCT + "created"


def _v(x):
    return str(x)


def load_raw(source_root):
    nanopubs = source_root / "nanopubs"
    files = sorted(p for p in nanopubs.rglob("*") if p.is_file())
    by_graph = defaultdict(set)
    all_triples = set()
    errors = []

    for path in files:
        raw = path.read_bytes()
        ds = Dataset()
        try:
            ds.parse(data=raw.decode("utf-8"), format="trig")
        except Exception as exc:
            errors.append({
                "path": path.relative_to(source_root).as_posix(),
                "error": f"{type(exc).__name__}: {exc}",
            })
            continue
        for s, p, o, g in ds.quads((None, None, None, None)):
            gn = _v(g.identifier if hasattr(g, "identifier") else g)
            row = (_v(s), _v(p), _v(o))
            by_graph[gn].add(row)
            all_triples.add(row)

    return files, by_graph, all_triples, errors


def graph_links(all_triples):
    assertion = {}
    pubinfo = {}
    for s, p, o in all_triples:
        if p == NP_HAS_ASSERTION:
            assertion[s] = o
        elif p == NP_HAS_PUBINFO:
            pubinfo[s] = o
    return assertion, pubinfo


def independently_derive(by_graph, all_triples):
    assertion, pubinfo = graph_links(all_triples)

    roots = {}
    reviews = {}
    updates = {}
    responses = {}
    decisions = {}
    creators = {}
    created = {}

    superseded_targets = {
        o for s, p, o in all_triples if p == NPX_SUPERSEDES
    }
    retracted_targets = {
        o for s, p, o in all_triples if p == NPX_RETRACTS
    }

    packages = set(assertion) | set(pubinfo)

    for np in sorted(packages):
        ag = assertion.get(np)
        pg = pubinfo.get(np)

        if pg in by_graph:
            for s, p, o in by_graph[pg]:
                if s == np and p == DCT_CREATOR:
                    creators[np] = o
                elif s == np and p == DCT_CREATED:
                    created[np] = o
                elif s == np and p == LF_IS_UPDATE_OF:
                    updates.setdefault(np, set()).add(o)

        if ag in by_graph:
            triples = by_graph[ag]
            subjects = {s for s, _, _ in triples}
            for subject in subjects:
                if (
                    (subject, FRBR_PART_OF, SPECIAL_ISSUE) in triples
                    and (subject, PSO_WITH_STATUS, PSO_SUBMITTED)
                    in triples
                ):
                    roots.setdefault(subject, set()).add(np)

                if (subject, RDF_TYPE, LF_REVIEW_COMMENT) in triples:
                    targets = {
                        o for s, p, o in triples
                        if s == subject and p == LF_REFERS_TO
                    }
                    reviews.setdefault(np, set()).update(targets)

                review_targets = {
                    o for s, p, o in triples
                    if s == subject and p == LF_IS_RESPONSE_TO
                }
                if review_targets:
                    update_targets = {
                        o for s, p, o in triples
                        if s == subject and p == LF_REFERS_TO
                    }
                    row = responses.setdefault(np, {
                        "review_targets": set(),
                        "update_targets": set(),
                    })
                    row["review_targets"].update(review_targets)
                    row["update_targets"].update(update_targets)

            for s, p, o in triples:
                if p == PSO_WITH_STATUS and o != PSO_SUBMITTED:
                    decisions.setdefault(np, set()).add((s, o))

    # Generic project queries allow update relations in any graph.
    for s, p, o in all_triples:
        if p == LF_IS_UPDATE_OF and s in packages:
            updates.setdefault(s, set()).add(o)

    live_packages = {
        np for np in packages
        if np not in superseded_targets and np not in retracted_targets
    }

    valid_reviews = {}
    for np, targets in reviews.items():
        if np in live_packages and len(targets) == 1:
            valid_reviews[np] = next(iter(targets))

    valid_updates = {}
    for np, targets in updates.items():
        if np in live_packages and len(targets) == 1:
            valid_updates[np] = next(iter(targets))

    valid_responses = {}
    for np, row in responses.items():
        if (
            np in live_packages
            and len(row["review_targets"]) == 1
            and len(row["update_targets"]) == 1
        ):
            valid_responses[np] = (
                next(iter(row["review_targets"])),
                next(iter(row["update_targets"])),
            )

    valid_decisions = {}
    for np, pairs in decisions.items():
        if np in live_packages and len(pairs) == 1:
            valid_decisions[np] = next(iter(pairs))

    t1 = set()
    for response_np, (review_np, update_np) in valid_responses.items():
        root_r = valid_reviews.get(review_np)
        root_u = valid_updates.get(update_np)
        if (
            root_r is not None
            and root_u is not None
            and root_r == root_u
            and root_r in roots
        ):
            # Submission package is independently canonicalized as any live
            # package carrying the same root assertion. Exact package identity
            # is verified separately against the main chain manifest.
            live_submissions = sorted(
                np for np in roots[root_r] if np in live_packages
            )
            if len(live_submissions) == 1:
                t1.add((
                    root_r,
                    live_submissions[0],
                    review_np,
                    update_np,
                    response_np,
                ))

    t0 = set()
    for root, submission_np, review_np, update_np, response_np in t1:
        for decision_np, (target_update, status) in valid_decisions.items():
            if target_update == update_np:
                t0.add((
                    root,
                    submission_np,
                    review_np,
                    update_np,
                    response_np,
                    decision_np,
                    status,
                ))

    return {
        "roots": sorted(roots),
        "root_count": len(roots),
        "live_packages": sorted(live_packages),
        "t1": sorted(t1),
        "t0": sorted(t0),
        "superseded_targets": sorted(superseded_targets),
        "retracted_targets": sorted(retracted_targets),
        "creators": creators,
        "created": created,
        "assertion_graph": assertion,
        "pubinfo_graph": pubinfo,
    }


def audit_chain(chain, raw, by_graph):
    assertion = raw["assertion_graph"]
    pubinfo = raw["pubinfo_graph"]
    errors = []

    root = chain["root"]
    submission_np = chain["submission_np"]
    review_np = chain["review_np"]
    update_np = chain["update_np"]
    response_np = chain["response_np"]

    sag = assertion.get(submission_np)
    if sag not in by_graph:
        errors.append("SUBMISSION_ASSERTION_GRAPH_MISSING")
    else:
        triples = by_graph[sag]
        if (root, FRBR_PART_OF, SPECIAL_ISSUE) not in triples:
            errors.append("ROOT_SPECIAL_ISSUE_BINDING_MISSING")
        if (root, PSO_WITH_STATUS, PSO_SUBMITTED) not in triples:
            errors.append("ROOT_SUBMITTED_STATUS_MISSING")

    rag = assertion.get(review_np)
    review_ok = False
    if rag in by_graph:
        triples = by_graph[rag]
        subjects = {
            s for s, p, o in triples
            if p == RDF_TYPE and o == LF_REVIEW_COMMENT
        }
        review_ok = any(
            (s, LF_REFERS_TO, root) in triples
            for s in subjects
        )
    if not review_ok:
        errors.append("RAW_REVIEW_TARGET_MISMATCH")

    upg = pubinfo.get(update_np)
    update_ok = (
        upg in by_graph
        and (update_np, LF_IS_UPDATE_OF, root) in by_graph[upg]
    )
    if not update_ok:
        # Allow generic graph placement exactly as project queries do.
        update_ok = any(
            s == update_np and p == LF_IS_UPDATE_OF and o == root
            for triples in by_graph.values()
            for s, p, o in triples
        )
    if not update_ok:
        errors.append("RAW_UPDATE_TARGET_MISMATCH")

    aag = assertion.get(response_np)
    response_ok = False
    if aag in by_graph:
        triples = by_graph[aag]
        subjects = {
            s for s, p, o in triples if p == LF_IS_RESPONSE_TO
        }
        response_ok = any(
            (s, LF_IS_RESPONSE_TO, review_np) in triples
            and (s, LF_REFERS_TO, update_np) in triples
            for s in subjects
        )
    if not response_ok:
        errors.append("RAW_RESPONSE_TARGET_MISMATCH")

    if chain.get("decision_np"):
        decision_np = chain["decision_np"]
        dag = assertion.get(decision_np)
        decision_ok = (
            dag in by_graph
            and (
                update_np,
                PSO_WITH_STATUS,
                chain["decision_status"],
            ) in by_graph[dag]
        )
        if not decision_ok:
            errors.append("RAW_DECISION_TARGET_STATUS_MISMATCH")

    chain_packages = [
        submission_np,
        review_np,
        update_np,
        response_np,
    ]
    if chain.get("decision_np"):
        chain_packages.append(chain["decision_np"])

    superseded = set(raw["superseded_targets"])
    retracted = set(raw["retracted_targets"])
    bad_live = sorted(
        p for p in chain_packages
        if p in superseded or p in retracted
    )
    if bad_live:
        errors.append("CHAIN_USES_NONLIVE_RAW_PACKAGE")

    provenance = {}
    for np in chain_packages:
        provenance[np] = {
            "creator_present": np in raw["creators"],
            "created_present": np in raw["created"],
        }

    return {
        "chain": chain,
        "errors": errors,
        "pass": not errors,
        "provenance_presence": provenance,
    }


def manifest_sets(main):
    t0 = set()
    t1 = set()
    for row in main.get("chain_results", []):
        c = row["chain"]
        if c.get("decision_np"):
            t0.add((
                c["root"],
                c["submission_np"],
                c["review_np"],
                c["update_np"],
                c["response_np"],
                c["decision_np"],
                c["decision_status"],
            ))
        else:
            t1.add((
                c["root"],
                c["submission_np"],
                c["review_np"],
                c["update_np"],
                c["response_np"],
            ))
    return t0, t1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--main-result", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    source_root = Path(args.source_root)
    main_result = json.loads(
        Path(args.main_result).read_text(encoding="utf-8")
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    files, by_graph, all_triples, parse_errors = load_raw(source_root)
    raw = independently_derive(by_graph, all_triples)

    main_roots = sorted(
        row["root"]
        for row in (main_result.get("population") or {}).get("roots", [])
    )
    root_exact = main_roots == raw["roots"]

    main_t0, main_t1 = manifest_sets(main_result)
    raw_t0 = set(tuple(x) for x in raw["t0"])
    raw_t1 = set(tuple(x) for x in raw["t1"])

    # A T1 tuple that is part of a T0 chain is not separately in the main
    # denominator when the root disposition is T0. Compare the underlying
    # connected review/update/response tuples after projecting T0.
    main_connected = set(main_t1)
    main_connected.update(x[:5] for x in main_t0)
    raw_connected = set(raw_t1)

    chain_audits = [
        audit_chain(row["chain"], raw, by_graph)
        for row in main_result.get("chain_results", [])
    ]

    t0_exact = main_t0 == raw_t0
    connected_exact = main_connected == raw_connected
    all_chain_pass = all(x["pass"] for x in chain_audits)

    errors = []
    if parse_errors:
        errors.append("DOCUMENTARY_PARSE_FAILURE")
    if not root_exact:
        errors.append("DOCUMENTARY_ROOT_SET_MISMATCH")
    if not connected_exact:
        errors.append("DOCUMENTARY_CONNECTED_CHAIN_SET_MISMATCH")
    if not t0_exact:
        errors.append("DOCUMENTARY_T0_CHAIN_SET_MISMATCH")
    if not all_chain_pass:
        errors.append("DOCUMENTARY_CHAIN_RELATION_MISMATCH")

    result = {
        "study": "FORMALIZATION_PAPERS_FRESH_DOCUMENTARY_AUDIT_V1",
        "record_file_count": len(files),
        "parse_errors": parse_errors,
        "root_set_exact": root_exact,
        "main_root_count": len(main_roots),
        "audit_root_count": raw["root_count"],
        "connected_chain_set_exact": connected_exact,
        "t0_chain_set_exact": t0_exact,
        "main_connected_chain_count": len(main_connected),
        "audit_connected_chain_count": len(raw_connected),
        "main_t0_chain_count": len(main_t0),
        "audit_t0_chain_count": len(raw_t0),
        "chain_audits": chain_audits,
        "chain_pass_count": sum(x["pass"] for x in chain_audits),
        "errors": errors,
        "overall": "PASS" if not errors else "FAIL",
    }

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "study": result["study"],
        "root_set_exact": root_exact,
        "connected_chain_set_exact": connected_exact,
        "t0_chain_set_exact": t0_exact,
        "chain_pass_count": result["chain_pass_count"],
        "chain_count": len(chain_audits),
        "overall": result["overall"],
        "errors": errors,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
