from __future__ import annotations

from collections import defaultdict
from datetime import datetime


SURFACE_KEYS = (
    "roots",
    "reviews",
    "updates",
    "responses",
    "decisions",
    "supersedes",
    "retracts",
    "creators",
    "created",
)


def merge_surfaces(surfaces):
    merged = {k: set() for k in SURFACE_KEYS}
    for surface in surfaces:
        for key in SURFACE_KEYS:
            for row in surface.get(key, []):
                merged[key].add(tuple(row))
    return {k: sorted(v) for k, v in merged.items()}


def _all_packages(surface):
    out = set()
    out.update(np for _, np in surface.get("roots", []))
    out.update(np for np, _, _ in surface.get("reviews", []))
    out.update(np for np, _ in surface.get("updates", []))
    out.update(np for np, _, _, _ in surface.get("responses", []))
    out.update(np for np, _, _ in surface.get("decisions", []))
    for new, old in surface.get("supersedes", []):
        out.add(new)
        out.add(old)
    for retraction, target in surface.get("retracts", []):
        out.add(retraction)
        out.add(target)
    out.update(np for np, _ in surface.get("creators", []))
    out.update(np for np, _ in surface.get("created", []))
    return out


def analyze_versions(surface):
    packages = _all_packages(surface)
    successors = defaultdict(set)
    for new, old in surface.get("supersedes", []):
        successors[old].add(new)

    retracted = {target for _, target in surface.get("retracts", [])}

    memo = {}
    visiting = set()
    cycle_nodes = set()

    def terminals(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            cycle_nodes.add(node)
            return set()
        visiting.add(node)
        nxt = successors.get(node, set())
        if not nxt:
            result = {node}
        else:
            result = set()
            for child in sorted(nxt):
                result.update(terminals(child))
        visiting.remove(node)
        memo[node] = result
        return result

    canonical = {}
    ambiguous = {}
    for package in sorted(packages):
        terms = terminals(package)
        if package in cycle_nodes:
            canonical[package] = None
            ambiguous[package] = "SUPERSESSION_CYCLE"
            continue
        live_terms = sorted(x for x in terms if x not in retracted)
        if len(live_terms) == 1:
            canonical[package] = live_terms[0]
        elif len(live_terms) == 0:
            canonical[package] = None
            ambiguous[package] = "NO_LIVE_TERMINAL_VERSION"
        else:
            canonical[package] = None
            ambiguous[package] = "MULTIPLE_LIVE_TERMINAL_VERSIONS"

    # Propagate any detected cycle to ancestors whose terminal resolution is unsafe.
    if cycle_nodes:
        for package in sorted(packages):
            seen = set()
            stack = [package]
            touches_cycle = False
            while stack:
                node = stack.pop()
                if node in seen:
                    continue
                seen.add(node)
                if node in cycle_nodes:
                    touches_cycle = True
                    break
                stack.extend(successors.get(node, set()))
            if touches_cycle:
                canonical[package] = None
                ambiguous[package] = "SUPERSESSION_CYCLE"

    live_packages = {
        p for p in packages
        if canonical.get(p) == p and p not in retracted
    }

    return {
        "canonical": canonical,
        "ambiguous": ambiguous,
        "retracted": sorted(retracted),
        "live_packages": sorted(live_packages),
        "successors": {
            k: sorted(v) for k, v in sorted(successors.items())
        },
    }


def _parse_time(value):
    if not value:
        return None
    text = str(value)
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _created_index(surface):
    values = defaultdict(set)
    for np, value in surface.get("created", []):
        values[np].add(value)
    unique = {}
    ambiguous = {}
    for np, vals in values.items():
        if len(vals) == 1:
            unique[np] = next(iter(vals))
        else:
            ambiguous[np] = sorted(vals)
    return unique, ambiguous


def _chronology_contradiction(created, prior_np, later_np):
    a = _parse_time(created.get(prior_np))
    b = _parse_time(created.get(later_np))
    if a is None or b is None:
        return False
    return b < a


def classify_population(surface):
    version = analyze_versions(surface)
    canonical = version["canonical"]
    live_packages = set(version["live_packages"])

    roots_raw = defaultdict(set)
    for root, submission_np in surface.get("roots", []):
        roots_raw[root].add(submission_np)
    root_ids = set(roots_raw)

    reviews_by_np = defaultdict(list)
    review_root_raw = {}
    review_root_ambiguous = {}
    for np, subject, targets in surface.get("reviews", []):
        reviews_by_np[np].append((subject, tuple(targets)))
    for np, rows in reviews_by_np.items():
        target_sets = [tuple(t) for _, t in rows]
        flat = set()
        valid_singletons = True
        for targets in target_sets:
            if len(targets) != 1:
                valid_singletons = False
            flat.update(targets)
        if valid_singletons and len(flat) == 1:
            review_root_raw[np] = next(iter(flat))
        else:
            review_root_ambiguous[np] = sorted(flat)

    updates_by_np = defaultdict(set)
    for np, target in surface.get("updates", []):
        updates_by_np[np].add(target)
    update_root_raw = {}
    update_root_ambiguous = {}
    for np, targets in updates_by_np.items():
        if len(targets) == 1:
            update_root_raw[np] = next(iter(targets))
        else:
            update_root_ambiguous[np] = sorted(targets)

    responses_by_np = defaultdict(lambda: {
        "subjects": set(),
        "review_targets": set(),
        "update_targets": set(),
    })
    for np, subject, review_targets, update_targets in surface.get(
        "responses", []
    ):
        row = responses_by_np[np]
        row["subjects"].add(subject)
        row["review_targets"].update(review_targets)
        row["update_targets"].update(update_targets)

    decisions_by_np = defaultdict(set)
    for np, target_update, status in surface.get("decisions", []):
        decisions_by_np[np].add((target_update, status))

    created, created_ambiguous = _created_index(surface)

    # Associate packages with roots using only explicit target structure.
    package_roots = defaultdict(set)
    for root, submissions in roots_raw.items():
        for np in submissions:
            package_roots[np].add(root)

    for np, root in review_root_raw.items():
        if root in root_ids:
            package_roots[np].add(root)
    for np, root in update_root_raw.items():
        if root in root_ids:
            package_roots[np].add(root)

    response_root_raw = {}
    response_ambiguous = {}
    for np, row in responses_by_np.items():
        rr = sorted(row["review_targets"])
        uu = sorted(row["update_targets"])
        candidate_roots = set()
        if len(rr) == 1 and rr[0] in review_root_raw:
            candidate_roots.add(review_root_raw[rr[0]])
        if len(uu) == 1 and uu[0] in update_root_raw:
            candidate_roots.add(update_root_raw[uu[0]])
        if (
            len(rr) == 1
            and len(uu) == 1
            and len(candidate_roots) == 1
        ):
            root = next(iter(candidate_roots))
            response_root_raw[np] = root
            if root in root_ids:
                package_roots[np].add(root)
        else:
            response_ambiguous[np] = {
                "review_targets": rr,
                "update_targets": uu,
                "candidate_roots": sorted(candidate_roots),
            }
            for root in candidate_roots:
                if root in root_ids:
                    package_roots[np].add(root)

    decision_root_raw = {}
    decision_ambiguous = {}
    for np, pairs in decisions_by_np.items():
        if len(pairs) == 1:
            update_np, _ = next(iter(pairs))
            root = update_root_raw.get(update_np)
            if root is not None:
                decision_root_raw[np] = root
                if root in root_ids:
                    package_roots[np].add(root)
            else:
                decision_ambiguous[np] = sorted(pairs)
        else:
            decision_ambiguous[np] = sorted(pairs)

    maintenance_roots = defaultdict(list)
    for rel_name, rows in (
        ("SUPERSEDES", surface.get("supersedes", [])),
        ("RETRACTS", surface.get("retracts", [])),
    ):
        for source, target in rows:
            roots = set(package_roots.get(source, set()))
            roots.update(package_roots.get(target, set()))
            for root in roots:
                maintenance_roots[root].append({
                    "relation": rel_name,
                    "source": source,
                    "target": target,
                })

    root_rows = []
    for root in sorted(root_ids):
        ambiguities = []

        submission_candidates = set()
        for submission_np in sorted(roots_raw[root]):
            if submission_np in version["ambiguous"]:
                ambiguities.append({
                    "kind": "SUBMISSION_VERSION_AMBIGUITY",
                    "package": submission_np,
                    "reason": version["ambiguous"][submission_np],
                })
            live = canonical.get(submission_np)
            if live is not None:
                submission_candidates.add(live)
        if len(submission_candidates) != 1:
            ambiguities.append({
                "kind": "SUBMISSION_LIVE_VERSION_CARDINALITY",
                "values": sorted(submission_candidates),
            })
        submission_np = (
            next(iter(submission_candidates))
            if len(submission_candidates) == 1
            else None
        )

        live_reviews = []
        for np, target_root in review_root_raw.items():
            if target_root != root:
                continue
            if np in review_root_ambiguous:
                ambiguities.append({
                    "kind": "REVIEW_TARGET_AMBIGUITY",
                    "package": np,
                })
                continue
            if canonical.get(np) == np and np in live_packages:
                live_reviews.append(np)
            elif canonical.get(np) is None:
                ambiguities.append({
                    "kind": "REVIEW_VERSION_UNRESOLVED",
                    "package": np,
                })

        # Multi-target review records touching this root are T8.
        for np, targets in review_root_ambiguous.items():
            if root in targets:
                ambiguities.append({
                    "kind": "REVIEW_NONFUNCTIONAL_TARGET",
                    "package": np,
                    "targets": targets,
                })

        live_updates = []
        for np, target_root in update_root_raw.items():
            if target_root != root:
                continue
            if canonical.get(np) == np and np in live_packages:
                live_updates.append(np)
            elif canonical.get(np) is None:
                ambiguities.append({
                    "kind": "UPDATE_VERSION_UNRESOLVED",
                    "package": np,
                })

        for np, targets in update_root_ambiguous.items():
            if root in targets:
                ambiguities.append({
                    "kind": "UPDATE_NONFUNCTIONAL_TARGET",
                    "package": np,
                    "targets": targets,
                })

        live_reviews = sorted(set(live_reviews))
        live_updates = sorted(set(live_updates))

        live_responses = []
        response_records = {}
        for np, target_root in response_root_raw.items():
            if target_root != root:
                continue
            row = responses_by_np[np]
            review_targets = sorted(row["review_targets"])
            update_targets = sorted(row["update_targets"])
            if canonical.get(np) != np or np not in live_packages:
                if canonical.get(np) is None:
                    ambiguities.append({
                        "kind": "RESPONSE_VERSION_UNRESOLVED",
                        "package": np,
                    })
                continue
            if len(review_targets) != 1 or len(update_targets) != 1:
                ambiguities.append({
                    "kind": "RESPONSE_NONFUNCTIONAL_TARGET",
                    "package": np,
                    "review_targets": review_targets,
                    "update_targets": update_targets,
                })
                continue
            review_np = review_targets[0]
            update_np = update_targets[0]
            if review_np not in live_reviews:
                ambiguities.append({
                    "kind": "RESPONSE_REVIEW_TARGET_NOT_LIVE",
                    "package": np,
                    "target": review_np,
                })
                continue
            if update_np not in live_updates:
                ambiguities.append({
                    "kind": "RESPONSE_UPDATE_TARGET_NOT_LIVE",
                    "package": np,
                    "target": update_np,
                })
                continue
            if _chronology_contradiction(created, review_np, np):
                ambiguities.append({
                    "kind": "CHRONOLOGY_CONTRADICTION_REVIEW_RESPONSE",
                    "prior": review_np,
                    "later": np,
                })
                continue
            if _chronology_contradiction(created, update_np, np):
                ambiguities.append({
                    "kind": "CHRONOLOGY_CONTRADICTION_UPDATE_RESPONSE",
                    "prior": update_np,
                    "later": np,
                })
                continue
            live_responses.append(np)
            response_records[np] = {
                "review_np": review_np,
                "update_np": update_np,
            }

        for np, detail in response_ambiguous.items():
            if root in detail.get("candidate_roots", []):
                ambiguities.append({
                    "kind": "RESPONSE_NONFUNCTIONAL_TARGET",
                    "package": np,
                    **detail,
                })

        live_decisions = []
        decision_records = {}
        for np, target_root in decision_root_raw.items():
            if target_root != root:
                continue
            if canonical.get(np) != np or np not in live_packages:
                if canonical.get(np) is None:
                    ambiguities.append({
                        "kind": "DECISION_VERSION_UNRESOLVED",
                        "package": np,
                    })
                continue
            pairs = sorted(decisions_by_np[np])
            if len(pairs) != 1:
                ambiguities.append({
                    "kind": "DECISION_NONFUNCTIONAL_TARGET",
                    "package": np,
                    "pairs": pairs,
                })
                continue
            update_np, status = pairs[0]
            if update_np not in live_updates:
                ambiguities.append({
                    "kind": "DECISION_TARGET_NOT_LIVE",
                    "package": np,
                    "target": update_np,
                })
                continue
            if _chronology_contradiction(created, update_np, np):
                ambiguities.append({
                    "kind": "CHRONOLOGY_CONTRADICTION_UPDATE_DECISION",
                    "prior": update_np,
                    "later": np,
                })
                continue
            live_decisions.append(np)
            decision_records[np] = {
                "update_np": update_np,
                "status": status,
            }

        for np, pairs in decision_ambiguous.items():
            roots = set()
            for update_np, _ in pairs:
                target_root = update_root_raw.get(update_np)
                if target_root:
                    roots.add(target_root)
            if root in roots:
                ambiguities.append({
                    "kind": "DECISION_NONFUNCTIONAL_TARGET",
                    "package": np,
                    "pairs": pairs,
                })

        t1 = []
        for response_np in sorted(set(live_responses)):
            rec = response_records[response_np]
            t1.append({
                "root": root,
                "submission_np": submission_np,
                "review_np": rec["review_np"],
                "update_np": rec["update_np"],
                "response_np": response_np,
            })

        t0 = []
        decisions_by_update = defaultdict(list)
        for decision_np in sorted(set(live_decisions)):
            rec = decision_records[decision_np]
            decisions_by_update[rec["update_np"]].append((
                decision_np, rec["status"]
            ))
        for chain in t1:
            for decision_np, status in sorted(
                decisions_by_update.get(chain["update_np"], [])
            ):
                x = dict(chain)
                x["decision_np"] = decision_np
                x["decision_status"] = status
                t0.append(x)

        maintenance = maintenance_roots.get(root, [])

        if ambiguities:
            disposition = "T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET"
        elif t0:
            disposition = "T0_COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION"
        elif t1:
            disposition = "T1_REVIEW_UPDATE_RESPONSE_NO_DECISION"
        elif live_reviews and live_updates:
            disposition = "T2_REVIEW_UPDATE_NO_RESPONSE"
        elif live_decisions and not live_responses:
            disposition = "T5_DECISION_WITHOUT_CONNECTED_RESPONSE"
        elif live_updates and not live_reviews:
            disposition = "T4_UPDATE_WITHOUT_CONNECTED_REVIEW"
        elif live_reviews and not live_updates:
            disposition = "T3_REVIEW_ONLY"
        elif maintenance:
            disposition = "T7_RETRACTED_OR_SUPERSEDED_ONLY"
        else:
            disposition = "T6_ROOT_ONLY"

        root_rows.append({
            "root": root,
            "submission_np": submission_np,
            "disposition": disposition,
            "live_reviews": live_reviews,
            "live_updates": live_updates,
            "live_responses": sorted(set(live_responses)),
            "live_decisions": sorted(set(live_decisions)),
            "t0_chains": t0,
            "t1_chains": t1,
            "maintenance": maintenance,
            "ambiguities": ambiguities,
        })

    counts = defaultdict(int)
    for row in root_rows:
        counts[row["disposition"]] += 1

    return {
        "root_count": len(root_rows),
        "roots": root_rows,
        "disposition_counts": dict(sorted(counts.items())),
        "version_analysis": {
            "retracted": version["retracted"],
            "ambiguous": version["ambiguous"],
            "live_package_count": len(version["live_packages"]),
        },
        "created_ambiguities": created_ambiguous,
        "complete_accounting": (
            len(root_rows) == len(root_ids)
            and len({r["root"] for r in root_rows}) == len(root_ids)
        ),
    }


def eligible_chains(population):
    out = []
    for row in population.get("roots", []):
        if row["disposition"].startswith("T0_"):
            for chain in row.get("t0_chains", []):
                x = dict(chain)
                x["root_disposition"] = row["disposition"]
                out.append(x)
        elif row["disposition"].startswith("T1_"):
            for chain in row.get("t1_chains", []):
                x = dict(chain)
                x["root_disposition"] = row["disposition"]
                out.append(x)
    return sorted(
        out,
        key=lambda x: (
            x["root"],
            x["review_np"],
            x["update_np"],
            x["response_np"],
            x.get("decision_np", ""),
        ),
    )


def has_connected_review_update_structure(population):
    for row in population.get("roots", []):
        if row["disposition"].startswith((
            "T0_", "T1_", "T2_", "T5_"
        )):
            return True
    return False
