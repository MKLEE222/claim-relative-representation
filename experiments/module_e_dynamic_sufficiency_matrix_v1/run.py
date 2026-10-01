from __future__ import annotations

import collections
import hashlib
import itertools
import json
import math
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UPSTREAM = "whitmanarchive/whitman-LG_1855_variorum"
PATH = "source/authority/anc.02134.xml"

EVENTS = {
    "D1": {
        "parent": "7cdf5ddc9d0cfff83289f687613ee3d0510e6520",
        "child": "fe63fcfbeca16f85583a29355c2d3a44e09b280f",
        "expected_parent_blob": "013041d1f51d20c6a59fdfbc494e6dd9c03fae0a",
        "expected_child_blob": "41de695ece50bf10d414cf71e688464250e8b4d8",
        "expected_delta": {"changed": 1, "added": 0, "removed": 0, "unchanged": 1435},
    },
    "D2": {
        "parent": "fe63fcfbeca16f85583a29355c2d3a44e09b280f",
        "child": "8c6aba338bd3b8a52ec74d014ec1afc8137cc4a9",
        "expected_parent_blob": "41de695ece50bf10d414cf71e688464250e8b4d8",
        "expected_child_blob": "6a7e23ba67c2e4064312bea4d3598cdbe19e753b",
        "expected_delta": {"changed": 141, "added": 7, "removed": 8, "unchanged": 1287},
    },
}

STATE_ARMS = ("S_FULL", "S_LOCUS_COUNTS", "S_ENDPOINTS")
EVENT_ARMS = ("E_LINK_FULL", "E_LINK_NEW", "E_LOCUS_OPERATION_BAG")
ACCESS_ARMS = ("A_NONE", "A_CHILD_REOPEN")
CERTS = ("high", "low")


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def local(tag):
    return tag.rsplit("}", 1)[-1]


def fetch(ref, expected_blob):
    url = f"https://raw.githubusercontent.com/{UPSTREAM}/{ref}/{PATH}"
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-E/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read()
    got = git_blob(raw)
    if got != expected_blob:
        raise RuntimeError(f"source drift at {ref}: {got} != {expected_blob}")
    return raw


def parse_et(raw):
    root = ET.fromstring(raw)
    rows = []
    for g in root.iter():
        if local(g.tag) != "linkGrp" or g.attrib.get("type") != "relation":
            continue
        ms_file = (g.attrib.get("corresp") or "").strip()
        for e in list(g):
            if local(e.tag) != "link":
                continue
            target = (e.attrib.get("target") or "").strip()
            parts = target.split()
            if len(parts) != 2:
                raise RuntimeError(f"unexpected relation target: {target!r}")
            cert = (e.attrib.get("cert") or "").strip()
            if cert not in CERTS:
                raise RuntimeError(f"unexpected certainty: {cert!r}")
            rows.append(
                {
                    "print_target": parts[0],
                    "ms_file": ms_file,
                    "ms_target": parts[1],
                    "certainty": cert,
                }
            )
    return rows


def parse_regex(raw):
    text = raw.decode("utf-8")
    rows = []
    grp = re.compile(
        r'<linkGrp\b[^>]*\btype="relation"[^>]*\bcorresp="([^"]+)"[^>]*>(.*?)</linkGrp>',
        re.S,
    )
    lnk = re.compile(r"<link\b([^>]*?)/>", re.S)
    for gm in grp.finditer(text):
        ms_file = gm.group(1)
        for lm in lnk.finditer(gm.group(2)):
            attrs = lm.group(1)
            cm = re.search(r'\bcert="([^"]+)"', attrs)
            tm = re.search(r'\btarget="([^"]+)"', attrs)
            if not (cm and tm):
                continue
            parts = tm.group(1).split()
            if len(parts) != 2:
                continue
            rows.append(
                {
                    "print_target": parts[0],
                    "ms_file": ms_file,
                    "ms_target": parts[1],
                    "certainty": cm.group(1),
                }
            )
    return rows


def endpoint(r):
    return (r["ms_file"], r["ms_target"])


def global_key(r):
    return (r["print_target"], r["ms_file"], r["ms_target"])


def rows_by_locus(rows):
    out = collections.defaultdict(dict)
    for r in rows:
        ep = endpoint(r)
        if ep in out[r["print_target"]]:
            raise RuntimeError(f"duplicate logical identity at {r['print_target']} {ep}")
        out[r["print_target"]][ep] = r["certainty"]
    return dict(out)


def full_state(rows):
    return {global_key(r): r["certainty"] for r in rows}


def derive_delta(parent_rows, child_rows):
    ps = full_state(parent_rows)
    cs = full_state(child_rows)
    changed, added, removed, unchanged = [], [], [], []
    for k in sorted(set(ps) | set(cs)):
        p = ps.get(k)
        c = cs.get(k)
        base = {"print_target": k[0], "ms_file": k[1], "ms_target": k[2]}
        if p == c:
            unchanged.append({**base, "certainty": p})
        elif p is None:
            added.append({**base, "new": c})
        elif c is None:
            removed.append({**base, "old": p})
        else:
            changed.append({**base, "old": p, "new": c})
    return {
        "changed": changed,
        "added": added,
        "removed": removed,
        "unchanged": unchanged,
    }


def project_state(parent_by_locus, arm):
    if arm == "S_FULL":
        return {
            p: [
                {"endpoint": list(ep), "certainty": cert}
                for ep, cert in sorted(m.items())
            ]
            for p, m in sorted(parent_by_locus.items())
        }
    if arm == "S_LOCUS_COUNTS":
        out = {}
        for p, m in sorted(parent_by_locus.items()):
            h = sum(v == "high" for v in m.values())
            l = sum(v == "low" for v in m.values())
            out[p] = {
                "endpoints": [list(ep) for ep in sorted(m)],
                "high_count": h,
                "low_count": l,
                "status": "MIXED" if h and l else "HIGH_ONLY" if h else "LOW_ONLY",
            }
        return out
    if arm == "S_ENDPOINTS":
        return {
            p: {"endpoints": [list(ep) for ep in sorted(m)]}
            for p, m in sorted(parent_by_locus.items())
        }
    raise ValueError(arm)


def delta_by_locus(delta):
    out = collections.defaultdict(lambda: {"changed": [], "added": [], "removed": []})
    for kind in ("changed", "added", "removed"):
        for x in delta[kind]:
            out[x["print_target"]][kind].append(x)
    return dict(out)


def project_event(delta, arm):
    by = delta_by_locus(delta)
    if arm == "E_LINK_FULL":
        return {
            p: {
                "changed": [
                    {
                        "endpoint": [x["ms_file"], x["ms_target"]],
                        "old": x["old"],
                        "new": x["new"],
                    }
                    for x in sorted(v["changed"], key=lambda z: (z["ms_file"], z["ms_target"]))
                ],
                "added": [
                    {"endpoint": [x["ms_file"], x["ms_target"]], "new": x["new"]}
                    for x in sorted(v["added"], key=lambda z: (z["ms_file"], z["ms_target"]))
                ],
                "removed": [
                    {"endpoint": [x["ms_file"], x["ms_target"]], "old": x["old"]}
                    for x in sorted(v["removed"], key=lambda z: (z["ms_file"], z["ms_target"]))
                ],
            }
            for p, v in sorted(by.items())
        }
    if arm == "E_LINK_NEW":
        return {
            p: {
                "changed": [
                    {"endpoint": [x["ms_file"], x["ms_target"]], "new": x["new"]}
                    for x in sorted(v["changed"], key=lambda z: (z["ms_file"], z["ms_target"]))
                ],
                "added": [
                    {"endpoint": [x["ms_file"], x["ms_target"]], "new": x["new"]}
                    for x in sorted(v["added"], key=lambda z: (z["ms_file"], z["ms_target"]))
                ],
                "removed": [
                    {"endpoint": [x["ms_file"], x["ms_target"]]}
                    for x in sorted(v["removed"], key=lambda z: (z["ms_file"], z["ms_target"]))
                ],
            }
            for p, v in sorted(by.items())
        }
    if arm == "E_LOCUS_OPERATION_BAG":
        out = {}
        for p, v in sorted(by.items()):
            directions = collections.Counter(f"{x['old']}->{x['new']}" for x in v["changed"])
            add_certs = collections.Counter(x["new"] for x in v["added"])
            rem_certs = collections.Counter(x["old"] for x in v["removed"])
            out[p] = {
                "changed_directions": dict(sorted(directions.items())),
                "added_certainties": dict(sorted(add_certs.items())),
                "removed_certainties": dict(sorted(rem_certs.items())),
            }
        return out
    raise ValueError(arm)


def parent_candidates(parent_truth, state_arm):
    eps = sorted(parent_truth)
    n = len(eps)
    if state_arm == "S_FULL":
        yield dict(parent_truth)
        return
    if state_arm == "S_LOCUS_COUNTS":
        h = sum(parent_truth[e] == "high" for e in eps)
        for highs in itertools.combinations(range(n), h):
            hs = set(highs)
            yield {ep: ("high" if i in hs else "low") for i, ep in enumerate(eps)}
        return
    if state_arm == "S_ENDPOINTS":
        for bits in itertools.product(CERTS, repeat=n):
            yield dict(zip(eps, bits))
        return
    raise ValueError(state_arm)


def transition_signature(parent_map, child_map):
    changed, added, removed = [], [], []
    for ep in sorted(set(parent_map) | set(child_map)):
        p = parent_map.get(ep)
        c = child_map.get(ep)
        if p == c:
            continue
        if p is None:
            added.append((ep[0], ep[1], c))
        elif c is None:
            removed.append((ep[0], ep[1], p))
        else:
            changed.append((ep[0], ep[1], p, c))
    return (
        tuple(changed),
        tuple(added),
        tuple(removed),
    )


def truth_transition(parent_truth, child_truth):
    return transition_signature(parent_truth, child_truth)


def apply_link_channel(parent_map, packet, full):
    child = dict(parent_map)
    # changed
    for x in packet["changed"]:
        ep = tuple(x["endpoint"])
        if ep not in parent_map:
            return None
        if full and parent_map[ep] != x["old"]:
            return None
        # operation semantics say CERT_CHANGED, not merely SET.
        if parent_map[ep] == x["new"]:
            return None
        child[ep] = x["new"]
    # removed
    for x in packet["removed"]:
        ep = tuple(x["endpoint"])
        if ep not in parent_map:
            return None
        if full and parent_map[ep] != x["old"]:
            return None
        child.pop(ep)
    # added
    for x in packet["added"]:
        ep = tuple(x["endpoint"])
        if ep in parent_map:
            return None
        child[ep] = x["new"]
    return [child]


def choose_by_cert(endpoints, parent_map, cert, k):
    pool = [ep for ep in endpoints if parent_map[ep] == cert]
    return itertools.combinations(pool, k)


def bag_children(parent_map, parent_truth, child_truth, packet):
    """Enumerate child maps compatible with an identity-free operation bag.

    The endpoint universe is bounded to natural parent U child endpoints.
    """
    parent_eps = set(parent_map)
    universe = set(parent_truth) | set(child_truth)
    add_pool = sorted(universe - parent_eps)

    directions = packet["changed_directions"]
    hl = directions.get("high->low", 0)
    lh = directions.get("low->high", 0)
    # Reject any unexpected direction under the binary frozen domain.
    for k in directions:
        if k not in {"high->low", "low->high"} and directions[k]:
            return

    rem_h = packet["removed_certainties"].get("high", 0)
    rem_l = packet["removed_certainties"].get("low", 0)
    add_h = packet["added_certainties"].get("high", 0)
    add_l = packet["added_certainties"].get("low", 0)

    if len(add_pool) != add_h + add_l:
        return

    # Added endpoint identities are deliberately bounded to U(parent,child).
    # Certainty binding among >1 added endpoints may still be ambiguous.
    for rem_high in choose_by_cert(sorted(parent_eps), parent_map, "high", rem_h):
        rem_high = set(rem_high)
        remaining1 = parent_eps - rem_high
        for rem_low in itertools.combinations(
            [ep for ep in sorted(remaining1) if parent_map[ep] == "low"], rem_l
        ):
            removed = rem_high | set(rem_low)
            remaining = parent_eps - removed
            high_pool = [ep for ep in sorted(remaining) if parent_map[ep] == "high"]
            low_pool = [ep for ep in sorted(remaining) if parent_map[ep] == "low"]
            for hl_eps in itertools.combinations(high_pool, hl):
                hl_set = set(hl_eps)
                for lh_eps in itertools.combinations(low_pool, lh):
                    lh_set = set(lh_eps)
                    base = {ep: parent_map[ep] for ep in remaining}
                    for ep in hl_set:
                        base[ep] = "low"
                    for ep in lh_set:
                        base[ep] = "high"
                    # Assign added certainty multiset over fixed bounded add identities.
                    for add_high in itertools.combinations(add_pool, add_h):
                        ah = set(add_high)
                        child = dict(base)
                        for ep in add_pool:
                            child[ep] = "high" if ep in ah else "low"
                        yield child


def child_state_tuple(m):
    return tuple((ep[0], ep[1], cert) for ep, cert in sorted(m.items()))


def enumerate_affected_locus(
    parent_truth,
    child_truth,
    state_arm,
    event_arm,
    packet,
    access_arm,
    truth_unchanged_eps,
):
    child_truth_tuple = child_state_tuple(child_truth)
    truth_trans = truth_transition(parent_truth, child_truth)

    child_states = set()
    trans_states = set()
    stable_options = {ep: set() for ep in truth_unchanged_eps}
    realizations = 0

    for pmap in parent_candidates(parent_truth, state_arm):
        if event_arm == "E_LINK_FULL":
            children = apply_link_channel(pmap, packet, full=True)
            if children is None:
                continue
        elif event_arm == "E_LINK_NEW":
            children = apply_link_channel(pmap, packet, full=False)
            if children is None:
                continue
        elif event_arm == "E_LOCUS_OPERATION_BAG":
            children = bag_children(pmap, parent_truth, child_truth, packet)
        else:
            raise ValueError(event_arm)

        for cmap in children:
            ctuple = child_state_tuple(cmap)
            if access_arm == "A_CHILD_REOPEN" and ctuple != child_truth_tuple:
                continue
            realizations += 1
            child_states.add(ctuple)
            trans_states.add(transition_signature(pmap, cmap))
            for ep in truth_unchanged_eps:
                stable_options[ep].add((pmap.get(ep, "ABSENT"), cmap.get(ep, "ABSENT")))

    child_exact = len(child_states) == 1 and next(iter(child_states), None) == child_truth_tuple
    trans_exact = len(trans_states) == 1 and next(iter(trans_states), None) == truth_trans

    stable_exact = {
        ep: opts == {(parent_truth[ep], child_truth[ep])}
        for ep, opts in stable_options.items()
    }

    return {
        "realizations": realizations,
        "distinct_child_states": len(child_states),
        "distinct_transition_states": len(trans_states),
        "child_exact": child_exact,
        "transition_exact": trans_exact,
        "incompatible": realizations == 0,
        "stable_exact": stable_exact,
    }


def parent_assignment_count(parent_truth, state_arm):
    n = len(parent_truth)
    if state_arm == "S_FULL":
        return 1
    if state_arm == "S_LOCUS_COUNTS":
        h = sum(v == "high" for v in parent_truth.values())
        return math.comb(n, h)
    if state_arm == "S_ENDPOINTS":
        return 2 ** n
    raise ValueError(state_arm)


def unchanged_locus_metrics(parent_truth, state_arm, access_arm):
    """Complete event packets declare an unlisted locus unchanged."""
    n_candidates = parent_assignment_count(parent_truth, state_arm)
    if access_arm == "A_CHILD_REOPEN":
        # Child truth plus complete 'unchanged locus' declaration fixes parent=child.
        return {
            "distinct_child_states": 1,
            "child_exact": True,
            "stable_exact_relations": len(parent_truth),
        }
    if n_candidates == 1:
        return {
            "distinct_child_states": 1,
            "child_exact": True,
            "stable_exact_relations": len(parent_truth),
        }
    # With only symmetric aggregate/endpoint state, no individual status is fixed
    # at a genuinely ambiguous locus.
    return {
        "distinct_child_states": n_candidates,
        "child_exact": False,
        "stable_exact_relations": 0,
    }


def build_packets(delta, event_arm):
    proj = project_event(delta, event_arm)
    return proj


def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    all_event_results = {}
    matrix = []
    diagnostics = []

    for event_name, spec in EVENTS.items():
        praw = fetch(spec["parent"], spec["expected_parent_blob"])
        craw = fetch(spec["child"], spec["expected_child_blob"])
        P = parse_et(praw)
        C = parse_et(craw)
        # independent parser checks
        if full_state(P) != full_state(parse_regex(praw)):
            raise RuntimeError(f"{event_name}: parent parser disagreement")
        if full_state(C) != full_state(parse_regex(craw)):
            raise RuntimeError(f"{event_name}: child parser disagreement")

        PB = rows_by_locus(P)
        CB = rows_by_locus(C)
        delta = derive_delta(P, C)
        observed = {
            "changed": len(delta["changed"]),
            "added": len(delta["added"]),
            "removed": len(delta["removed"]),
            "unchanged": len(delta["unchanged"]),
        }
        if observed != spec["expected_delta"]:
            raise RuntimeError(f"{event_name}: authoritative delta mismatch {observed}")

        delta_locus = delta_by_locus(delta)
        affected = set(delta_locus)
        loci = sorted(set(PB) | set(CB))
        unchanged_truth_keys = {
            (x["print_target"], x["ms_file"], x["ms_target"]): x["certainty"]
            for x in delta["unchanged"]
        }

        state_bytes = {
            arm: len(canonical(project_state(PB, arm))) for arm in STATE_ARMS
        }
        event_payloads = {arm: build_packets(delta, arm) for arm in EVENT_ARMS}
        event_bytes = {arm: len(canonical(event_payloads[arm])) for arm in EVENT_ARMS}

        event_summary = {
            "source": {
                "parent": {
                    "commit": spec["parent"],
                    "git_blob": spec["expected_parent_blob"],
                    "sha256": sha256(praw),
                    "bytes": len(praw),
                },
                "child": {
                    "commit": spec["child"],
                    "git_blob": spec["expected_child_blob"],
                    "sha256": sha256(craw),
                    "bytes": len(craw),
                },
            },
            "population": {
                "parent_relations": len(P),
                "child_relations": len(C),
                "parent_loci": len(PB),
                "child_loci": len(CB),
                "affected_loci": len(affected),
                "unchanged_relation_identities": len(delta["unchanged"]),
                **observed,
            },
            "state_payload_bytes": state_bytes,
            "event_payload_bytes": event_bytes,
        }

        for s_arm in STATE_ARMS:
            for e_arm in EVENT_ARMS:
                packets = event_payloads[e_arm]
                for a_arm in ACCESS_ARMS:
                    affected_child_exact = 0
                    affected_child_ambiguous = 0
                    affected_child_incompatible = 0
                    affected_trans_exact = 0
                    affected_trans_ambiguous = 0
                    affected_trans_incompatible = 0
                    sum_child_candidates = 0
                    max_child_candidates = 0
                    sum_trans_candidates = 0
                    max_trans_candidates = 0
                    sum_realizations = 0
                    stable_exact_relations = 0

                    global_child_exact = True
                    cell_diag = []

                    for p in loci:
                        p_truth = PB.get(p, {})
                        c_truth = CB.get(p, {})
                        if p in affected:
                            packet = packets[p]
                            truth_unchanged_eps = {
                                ep
                                for ep in set(p_truth) & set(c_truth)
                                if p_truth[ep] == c_truth[ep]
                            }
                            m = enumerate_affected_locus(
                                p_truth,
                                c_truth,
                                s_arm,
                                e_arm,
                                packet,
                                a_arm,
                                truth_unchanged_eps,
                            )
                            sum_realizations += m["realizations"]
                            sum_child_candidates += m["distinct_child_states"]
                            max_child_candidates = max(max_child_candidates, m["distinct_child_states"])
                            sum_trans_candidates += m["distinct_transition_states"]
                            max_trans_candidates = max(max_trans_candidates, m["distinct_transition_states"])

                            if m["incompatible"]:
                                affected_child_incompatible += 1
                                affected_trans_incompatible += 1
                                global_child_exact = False
                            else:
                                if m["child_exact"]:
                                    affected_child_exact += 1
                                else:
                                    affected_child_ambiguous += 1
                                    global_child_exact = False
                                if m["transition_exact"]:
                                    affected_trans_exact += 1
                                else:
                                    affected_trans_ambiguous += 1

                            stable_exact_relations += sum(m["stable_exact"].values())

                            if (
                                not m["child_exact"]
                                or not m["transition_exact"]
                                or m["distinct_child_states"] > 1
                                or m["distinct_transition_states"] > 1
                            ):
                                cell_diag.append(
                                    {
                                        "print_target": p,
                                        "child_candidates": m["distinct_child_states"],
                                        "transition_candidates": m["distinct_transition_states"],
                                        "realizations": m["realizations"],
                                        "child_exact": m["child_exact"],
                                        "transition_exact": m["transition_exact"],
                                    }
                                )
                        else:
                            um = unchanged_locus_metrics(p_truth, s_arm, a_arm)
                            if not um["child_exact"]:
                                global_child_exact = False
                            stable_exact_relations += um["stable_exact_relations"]

                    total_unchanged = len(delta["unchanged"])
                    unaffected_audit_exact = stable_exact_relations == total_unchanged
                    complete_warranted_update = (
                        global_child_exact
                        and affected_trans_exact == len(affected)
                        and unaffected_audit_exact
                    )

                    row = {
                        "event": event_name,
                        "state_arm": s_arm,
                        "event_arm": e_arm,
                        "access_arm": a_arm,
                        "affected_loci": len(affected),
                        "affected_child_exact": affected_child_exact,
                        "affected_child_ambiguous": affected_child_ambiguous,
                        "affected_child_incompatible": affected_child_incompatible,
                        "affected_transition_exact": affected_trans_exact,
                        "affected_transition_ambiguous": affected_trans_ambiguous,
                        "affected_transition_incompatible": affected_trans_incompatible,
                        "global_child_exact": global_child_exact,
                        "unaffected_stability_exact_relations": stable_exact_relations,
                        "unaffected_stability_denominator": total_unchanged,
                        "unaffected_stability_audit_exact": unaffected_audit_exact,
                        "complete_warranted_update": complete_warranted_update,
                        "sum_affected_child_candidates": sum_child_candidates,
                        "max_affected_child_candidates": max_child_candidates,
                        "sum_affected_transition_candidates": sum_trans_candidates,
                        "max_affected_transition_candidates": max_trans_candidates,
                        "sum_affected_realizations": sum_realizations,
                        "state_payload_bytes": state_bytes[s_arm],
                        "event_payload_bytes": event_bytes[e_arm],
                        "child_source_bytes": len(craw) if a_arm == "A_CHILD_REOPEN" else 0,
                    }
                    matrix.append(row)
                    diagnostics.append(
                        {
                            "event": event_name,
                            "state_arm": s_arm,
                            "event_arm": e_arm,
                            "access_arm": a_arm,
                            "nonexact_affected_loci": cell_diag,
                        }
                    )

        all_event_results[event_name] = event_summary

    # Dispositions over the complete matrix.
    def rows_for(event, state, access):
        return {
            r["event_arm"]: r
            for r in matrix
            if r["event"] == event and r["state_arm"] == state and r["access_arm"] == access
        }

    channel_sep = False
    sep_witnesses = []
    for event in EVENTS:
        for state in STATE_ARMS:
            for access in ACCESS_ARMS:
                rs = rows_for(event, state, access)
                bag = rs["E_LOCUS_OPERATION_BAG"]
                for rich_name in ("E_LINK_FULL", "E_LINK_NEW"):
                    rich = rs[rich_name]
                    rich_good = (
                        rich["affected_child_exact"] == rich["affected_loci"]
                        and rich["affected_transition_exact"] == rich["affected_loci"]
                    )
                    bag_bad = (
                        bag["affected_child_exact"] < bag["affected_loci"]
                        or bag["affected_transition_exact"] < bag["affected_loci"]
                    )
                    if rich_good and bag_bad:
                        channel_sep = True
                        sep_witnesses.append(
                            {
                                "event": event,
                                "state_arm": state,
                                "access_arm": access,
                                "rich_event_arm": rich_name,
                                "bag_child_exact": bag["affected_child_exact"],
                                "bag_transition_exact": bag["affected_transition_exact"],
                            }
                        )

    reopen_child_not_transition = any(
        r["access_arm"] == "A_CHILD_REOPEN"
        and r["global_child_exact"]
        and r["affected_transition_exact"] < r["affected_loci"]
        for r in matrix
    )

    current_task_not_dynamic = any(
        r["state_arm"] == "S_ENDPOINTS"
        and r["access_arm"] == "A_NONE"
        and not r["complete_warranted_update"]
        for r in matrix
    )

    successful = [r for r in matrix if r["complete_warranted_update"]]
    distributed = False
    distributed_witness = None
    for a, b in itertools.combinations(successful, 2):
        if a["event"] != b["event"]:
            continue
        diffs = sum(
            a[k] != b[k] for k in ("state_arm", "event_arm", "access_arm")
        )
        if diffs >= 2:
            distributed = True
            distributed_witness = {
                "event": a["event"],
                "cell_a": {
                    "state": a["state_arm"],
                    "event": a["event_arm"],
                    "access": a["access_arm"],
                },
                "cell_b": {
                    "state": b["state_arm"],
                    "event": b["event_arm"],
                    "access": b["access_arm"],
                },
            }
            break

    result = {
        "study": "MODULE_E_DYNAMIC_SUFFICIENCY_MATRIX_V1",
        "authority": "CONTROLLED_CHANNEL_ABLATION_AROUND_ALREADY_OBSERVED_NATURAL_EVENTS",
        "events": all_event_results,
        "matrix_cells": len(matrix),
        "matrix": matrix,
        "dispositions": {
            "EVENT_CHANNEL_BINDING_SEPARATION": channel_sep,
            "REOPEN_CHILD_NOT_TRANSITION": reopen_child_not_transition,
            "CURRENT_TASK_NOT_DYNAMIC_SUFFICIENCY": current_task_not_dynamic,
            "DISTRIBUTED_SUFFICIENCY_OBSERVED": distributed,
        },
        "witnesses": {
            "event_channel_binding_separation": sep_witnesses,
            "distributed_sufficiency": distributed_witness,
        },
        "claim_boundary": [
            "D1/D2 natural parent-child states were already observed; Module E is a controlled interface ablation, not a blind natural replication.",
            "All state arms preserve the parent endpoint task Q0.",
            "E_LOCUS_OPERATION_BAG uses a bounded union-of-natural-endpoints universe, which is deliberately generous to the weak channel.",
            "Child-source reopening reveals the exact child object but does not by definition reveal the parent binding; transition audit is evaluated separately.",
            "The certainty domain in these frozen events is binary high/low, so E_LINK_NEW plus operation type can imply the old value for CERT_CHANGED records.",
            "Finite successful cells are not globally minimal representations.",
        ],
    }

    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Compact console summary.
    compact = []
    for r in matrix:
        compact.append(
            {
                "event": r["event"],
                "state": r["state_arm"],
                "event_channel": r["event_arm"],
                "access": r["access_arm"],
                "affected_child_exact": f"{r['affected_child_exact']}/{r['affected_loci']}",
                "affected_transition_exact": f"{r['affected_transition_exact']}/{r['affected_loci']}",
                "global_child_exact": r["global_child_exact"],
                "unaffected_audit_exact": r["unaffected_stability_audit_exact"],
                "complete_warranted_update": r["complete_warranted_update"],
            }
        )
    print(
        json.dumps(
            {
                "events": all_event_results,
                "matrix": compact,
                "dispositions": result["dispositions"],
                "witnesses": result["witnesses"],
                "results_sha256": sha256(out.read_bytes()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
