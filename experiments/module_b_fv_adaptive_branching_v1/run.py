"""Module B: source-triggered branching and selective update on exposed FV C18.

Development evidence only. No LLM calls and no independent transfer claim.
The first execution support stop is documented in IMPLEMENTATION_REPAIR_v1.md.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import statistics
import urllib.request
from pathlib import Path

from lxml import etree as E

PIN = "5a208f869ff1213defa000e3181d5315a072a15f"
MS_PATH = "collationChunks/C18/msColl_C18.xml"
MS_BLOB = "8e537331ebf46dd4f013da9afcbe38c14092b6fd"
URL = f"https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{PIN}/{MS_PATH}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def canon(x: object) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def norm_text(x: str) -> str:
    return " ".join(x.split())


def localname(e: E._Element) -> str:
    return E.QName(e).localname


def parse_tag(tag_text: str) -> E._Element:
    return E.fromstring(
        tag_text.encode("utf-8"),
        E.XMLParser(collect_ids=False, resolve_entities=False, no_network=True),
    )


def find_markers(text: str):
    tag_re = re.compile(r"<sga-add\b[^>]*/>", re.DOTALL)
    starts = {}
    ends = {}
    for m in tag_re.finditer(text):
        elem = parse_tag(m.group())
        sid = elem.get("sID")
        eid = elem.get("eID")
        if bool(sid) == bool(eid):
            raise RuntimeError("ambiguous sga-add marker")
        if sid:
            if sid in starts:
                raise RuntimeError("duplicate sID " + sid)
            starts[sid] = {
                "sid": sid,
                "lo": m.start(),
                "hi": m.end(),
                "tag": m.group(),
                "attrs": dict(elem.attrib),
            }
        else:
            if eid in ends:
                raise RuntimeError("duplicate eID " + eid)
            ends[eid] = {
                "sid": eid,
                "lo": m.start(),
                "hi": m.end(),
                "tag": m.group(),
                "attrs": dict(elem.attrib),
            }
    if set(starts) != set(ends):
        raise RuntimeError(
            "start/end mismatch: "
            f"starts_only={sorted(set(starts)-set(ends))[:5]} "
            f"ends_only={sorted(set(ends)-set(starts))[:5]}"
        )
    return starts, ends


def traverse_source(root: E._Element):
    """Reference traversal across arbitrary XML element boundaries.

    sga-add uses milestone-style start/end elements and is not necessarily a
    standalone subtree. Cancellation context is tracked independently.
    """
    scopes = {}
    active_add = {}
    active_cancel = []
    cancel_counter = 0

    def emit(text: str | None):
        if not text:
            return
        for sid, scope in active_add.items():
            scope["_text_parts"].append(text)
            for cancel in active_cancel:
                cid = cancel["cid"]
                if cid not in scope["_cancel_meta"]:
                    scope["_cancel_meta"][cid] = {
                        "element": cancel["element"],
                        "rend": cancel["rend"],
                        "xml_id": cancel["xml_id"],
                    }
                    scope["_cancel_parts"][cid] = []
                scope["_cancel_parts"][cid].append(text)

    def walk(node: E._Element):
        nonlocal cancel_counter
        tag = localname(node)

        pushed_cancel = False
        if tag in {"del", "mdel"}:
            cancel_counter += 1
            active_cancel.append({
                "cid": cancel_counter,
                "element": tag,
                "rend": node.get("rend", "NOT_ENCODED"),
                "xml_id": node.get(XML_ID, "NOT_ENCODED"),
            })
            pushed_cancel = True

        if tag == "sga-add":
            sid = node.get("sID")
            eid = node.get("eID")
            if bool(sid) == bool(eid):
                raise RuntimeError("ambiguous sga-add element in tree")
            if sid:
                if sid in scopes or sid in active_add:
                    raise RuntimeError("duplicate scope start " + sid)
                scope = {
                    "sid": sid,
                    "start_attrs": dict(node.attrib),
                    "_text_parts": [],
                    "_cancel_meta": {},
                    "_cancel_parts": {},
                }
                scopes[sid] = scope
                active_add[sid] = scope
            else:
                if eid not in active_add:
                    raise RuntimeError("unbound scope end " + eid)
                active_add.pop(eid)

        emit(node.text)
        for child in node:
            walk(child)
            emit(child.tail)

        if pushed_cancel:
            active_cancel.pop()

    walk(root)
    if active_add:
        raise RuntimeError("unclosed additions: " + ",".join(sorted(active_add)[:5]))

    for scope in scopes.values():
        cancels = []
        for cid in sorted(scope["_cancel_meta"]):
            txt = norm_text("".join(scope["_cancel_parts"][cid]))
            if not txt:
                continue
            meta = scope["_cancel_meta"][cid]
            cancels.append({
                "element": meta["element"],
                "text": txt,
                "rend": meta["rend"],
                "xml_id": meta["xml_id"],
            })
        scope["cancellations"] = cancels
        scope["current_answer"] = {
            "text": norm_text("".join(scope["_text_parts"])),
            "place": scope["start_attrs"].get("place", "NOT_ENCODED"),
            "hand": scope["start_attrs"].get("hand", "NOT_ENCODED"),
        }
        for k in ("_text_parts", "_cancel_meta", "_cancel_parts"):
            scope.pop(k)

    return scopes


def build_model(raw: bytes):
    text = raw.decode("utf-8")
    starts, ends = find_markers(text)
    root = E.fromstring(
        raw,
        E.XMLParser(collect_ids=False, resolve_entities=False, no_network=True),
    )
    scopes = traverse_source(root)

    if set(scopes) != set(starts):
        raise RuntimeError(
            f"tree/raw scope inventory differs: tree_only={sorted(set(scopes)-set(starts))[:5]} "
            f"raw_only={sorted(set(starts)-set(scopes))[:5]}"
        )

    xmlid_to_sids = collections.defaultdict(list)
    for sid, scope in scopes.items():
        s = starts[sid]
        e = ends[sid]
        if not (s["hi"] <= e["lo"]):
            raise RuntimeError("end precedes start " + sid)
        scope["source_span"] = [s["lo"], e["hi"]]
        scope["local_scope_serialization"] = text[s["lo"]:e["hi"]]
        scope["xml_id"] = scope["start_attrs"].get(XML_ID)
        if scope["xml_id"]:
            xmlid_to_sids[scope["xml_id"]].append(sid)

    incoming = collections.defaultdict(list)
    for sid, scope in scopes.items():
        nxt = scope["start_attrs"].get("next")
        if not nxt or not nxt.startswith("#"):
            continue
        targets = xmlid_to_sids.get(nxt[1:], [])
        if len(targets) == 1:
            incoming[targets[0]].append(sid)

    for sid, scope in scopes.items():
        nxt = scope["start_attrs"].get("next")
        if not nxt:
            outgoing = {"literal": None, "resolution": "NONE", "target_sid": None}
        elif nxt.startswith("#"):
            targets = xmlid_to_sids.get(nxt[1:], [])
            if len(targets) == 1:
                outgoing = {
                    "literal": nxt,
                    "resolution": "RESOLVED_INTERNAL_UNIQUE",
                    "target_sid": targets[0],
                }
            elif len(targets) == 0:
                outgoing = {
                    "literal": nxt,
                    "resolution": "UNRESOLVED_INTERNAL_ID",
                    "target_sid": None,
                }
            else:
                outgoing = {
                    "literal": nxt,
                    "resolution": "AMBIGUOUS_INTERNAL_ID",
                    "target_sid": None,
                }
        else:
            outgoing = {
                "literal": nxt,
                "resolution": "EXTERNAL_OR_NONLOCAL",
                "target_sid": None,
            }

        scope["reference"] = {
            "B_INCOMING": sorted(incoming.get(sid, [])),
            "B_OUTGOING": outgoing,
            "B_CANCEL": scope["cancellations"],
        }

    return {
        "raw": raw,
        "text": text,
        "scopes": scopes,
        "xmlid_to_sids": {k: sorted(v) for k, v in xmlid_to_sids.items()},
    }


def interface_payload(scope, name: str):
    if name == "CURRENT_SUMMARY":
        return scope["current_answer"]
    if name == "START_ATTRS_PLUS_TEXT":
        return {
            "start_attrs": scope["start_attrs"],
            "text": scope["current_answer"]["text"],
        }
    if name == "LOCAL_SCOPE_SERIALIZATION":
        return {"local_scope_serialization": scope["local_scope_serialization"]}
    if name == "SOURCE_LINKED":
        return {"commit": PIN, "path": MS_PATH, "sid": scope["sid"]}
    raise KeyError(name)


def local_cancel_marker_trigger(scope) -> bool:
    return bool(
        re.search(
            r"</?(?:del|mdel)\b",
            scope["local_scope_serialization"],
            flags=re.IGNORECASE,
        )
    )


def decode(scope, interface: str):
    ref = scope["reference"]
    if interface == "CURRENT_SUMMARY":
        return {
            "B_INCOMING": {"status": "UNKNOWN"},
            "B_OUTGOING": {"status": "UNKNOWN"},
            "B_CANCEL": {"status": "UNKNOWN"},
        }
    if interface == "START_ATTRS_PLUS_TEXT":
        nxt = scope["start_attrs"].get("next")
        outgoing = (
            {"status": "DETERMINED", "value": ref["B_OUTGOING"]}
            if not nxt
            else {
                "status": "UNKNOWN",
                "visible_literal": nxt,
                "licensed_trigger": True,
            }
        )
        return {
            "B_INCOMING": {"status": "UNKNOWN"},
            "B_OUTGOING": outgoing,
            "B_CANCEL": {"status": "UNKNOWN"},
        }
    if interface == "LOCAL_SCOPE_SERIALIZATION":
        nxt = scope["start_attrs"].get("next")
        outgoing = (
            {"status": "DETERMINED", "value": ref["B_OUTGOING"]}
            if not nxt
            else {
                "status": "UNKNOWN",
                "visible_literal": nxt,
                "licensed_trigger": True,
            }
        )
        return {
            "B_INCOMING": {"status": "UNKNOWN"},
            "B_OUTGOING": outgoing,
            "B_CANCEL": {
                "status": "UNKNOWN",
                "visible_marker_trigger": local_cancel_marker_trigger(scope),
            },
        }
    if interface == "SOURCE_LINKED":
        return {
            k: {"status": "DETERMINED", "value": v}
            for k, v in ref.items()
        }
    raise KeyError(interface)


def is_positive(family: str, value) -> bool:
    if family == "B_INCOMING":
        return bool(value)
    if family == "B_OUTGOING":
        return value["literal"] is not None
    if family == "B_CANCEL":
        return bool(value)
    raise KeyError(family)


def eval_interface(model, interface: str):
    rows = []
    byte_counts = []
    exact = unknown = wrong = 0
    positive_immediate = positive_total = 0
    trigger_false_positive = 0

    for sid in sorted(model["scopes"]):
        scope = model["scopes"][sid]
        payload = interface_payload(scope, interface)
        byte_counts.append(len(canon(payload)))
        decoded = decode(scope, interface)
        famrows = {}

        for fam, refval in scope["reference"].items():
            pos = is_positive(fam, refval)
            positive_total += int(pos)
            d = decoded[fam]

            if d["status"] == "UNKNOWN":
                unknown += 1
                trigger = False
                if fam == "B_OUTGOING" and d.get("licensed_trigger"):
                    trigger = True
                if fam == "B_CANCEL" and d.get("visible_marker_trigger"):
                    trigger = True
                if trigger:
                    if pos:
                        positive_immediate += 1
                    else:
                        trigger_false_positive += 1
            else:
                if d["value"] == refval:
                    exact += 1
                    if pos:
                        positive_immediate += 1
                else:
                    wrong += 1

            famrows[fam] = {"reference": refval, "decoded": d}

        rows.append({"sid": sid, "families": famrows})

    return {
        "interface": interface,
        "scope_count": len(model["scopes"]),
        "family_decisions": 3 * len(model["scopes"]),
        "exact_determined": exact,
        "unknown": unknown,
        "informative_wrong": wrong,
        "positive_branch_instances": positive_total,
        "positive_branch_instances_immediately_surfaced": positive_immediate,
        "positive_branch_trigger_coverage": (
            positive_immediate / positive_total if positive_total else 1.0
        ),
        "trigger_false_positive": trigger_false_positive,
        "payload_bytes": {
            "sum": sum(byte_counts),
            "min": min(byte_counts),
            "median": statistics.median(byte_counts),
            "max": max(byte_counts),
        },
        "rows": rows,
    }


def current_collision_groups(model):
    groups = collections.defaultdict(list)
    for sid, s in model["scopes"].items():
        groups[canon(s["current_answer"])].append(sid)

    out = []
    for payload, sids in groups.items():
        if len(sids) < 2:
            continue
        refs = {canon(model["scopes"][sid]["reference"]) for sid in sids}
        if len(refs) <= 1:
            continue
        out.append({
            "current_summary_sha256": sha256(payload),
            "current_summary": json.loads(payload),
            "members": [
                {"sid": sid, "reference": model["scopes"][sid]["reference"]}
                for sid in sorted(sids)
            ],
        })
    return sorted(out, key=lambda x: x["members"][0]["sid"])


def local_serialization_collision_groups(model):
    groups = collections.defaultdict(list)
    for sid, s in model["scopes"].items():
        groups[s["local_scope_serialization"].encode("utf-8")].append(sid)

    out = []
    for payload, sids in groups.items():
        if len(sids) < 2:
            continue
        incoming = {
            canon(model["scopes"][sid]["reference"]["B_INCOMING"])
            for sid in sids
        }
        if len(incoming) <= 1:
            continue
        out.append({
            "local_scope_serialization_sha256": sha256(payload),
            "members": [
                {
                    "sid": sid,
                    "incoming": model["scopes"][sid]["reference"]["B_INCOMING"],
                }
                for sid in sorted(sids)
            ],
        })
    return sorted(out, key=lambda x: x["members"][0]["sid"])


def mutate_remove_next(raw: bytes, source_sid: str):
    root = E.fromstring(
        raw,
        E.XMLParser(collect_ids=False, resolve_entities=False, no_network=True),
    )
    hits = [
        e for e in root.iter()
        if localname(e) == "sga-add" and e.get("sID") == source_sid
    ]
    if len(hits) != 1:
        raise RuntimeError(f"cannot uniquely mutate {source_sid}: {len(hits)}")
    if hits[0].get("next") is None:
        raise RuntimeError("mutation target has no next")
    old = hits[0].get("next")
    del hits[0].attrib["next"]
    mutated = E.tostring(root, encoding="utf-8", xml_declaration=True)
    return mutated, old


def branch_coordinate_diff(before, after):
    diffs = []
    for sid in sorted(before["scopes"]):
        if sid not in after["scopes"]:
            diffs.append([sid, "SCOPE_MISSING"])
            continue
        for fam in ("B_INCOMING", "B_OUTGOING", "B_CANCEL"):
            a = before["scopes"][sid]["reference"][fam]
            b = after["scopes"][sid]["reference"][fam]
            if a != b:
                diffs.append([sid, fam])
    return diffs


def controlled_updates(model):
    eligible = []
    for sid, scope in model["scopes"].items():
        out = scope["reference"]["B_OUTGOING"]
        if out["resolution"] == "RESOLVED_INTERNAL_UNIQUE":
            eligible.append((sid, out["target_sid"], out["literal"]))
    eligible.sort()

    event_results = []
    mutated_by_source = {}

    for source_sid, target_sid, literal in eligible:
        mutated_raw, old = mutate_remove_next(model["raw"], source_sid)
        if old != literal:
            raise AssertionError("mutated literal drift")
        mutated = build_model(mutated_raw)
        mutated_by_source[source_sid] = mutated

        if set(model["scopes"]) != set(mutated["scopes"]):
            raise AssertionError("scope inventory changed under next-only event")

        current_diff = [
            sid for sid in sorted(model["scopes"])
            if model["scopes"][sid]["current_answer"]
            != mutated["scopes"][sid]["current_answer"]
        ]
        diffs = branch_coordinate_diff(model, mutated)
        expected = sorted([
            [source_sid, "B_OUTGOING"],
            [target_sid, "B_INCOMING"],
        ])

        event_results.append({
            "source_sid": source_sid,
            "target_sid": target_sid,
            "literal_next": literal,
            "current_answer_changed_scopes": current_diff,
            "branch_coordinate_diffs": sorted(diffs),
            "expected_branch_coordinate_diffs": expected,
            "selective_update_pass": (
                not current_diff and sorted(diffs) == expected
            ),
            "cancel_ledger_unchanged": all(
                model["scopes"][sid]["reference"]["B_CANCEL"]
                == mutated["scopes"][sid]["reference"]["B_CANCEL"]
                for sid in model["scopes"]
            ),
        })

    controls = []
    for source_sid, target_sid, _ in eligible:
        other = next(
            (
                (s2, t2)
                for s2, t2, _ in eligible
                if {s2, t2}.isdisjoint({source_sid, target_sid})
            ),
            None,
        )
        if not other:
            controls.append({
                "focal_source_sid": source_sid,
                "focal_target_sid": target_sid,
                "control_available": False,
            })
            continue

        mut = mutated_by_source[other[0]]
        focal_coords = [
            [source_sid, "B_OUTGOING"],
            [source_sid, "B_INCOMING"],
            [source_sid, "B_CANCEL"],
            [target_sid, "B_OUTGOING"],
            [target_sid, "B_INCOMING"],
            [target_sid, "B_CANCEL"],
        ]
        unchanged = all(
            model["scopes"][sid]["reference"][fam]
            == mut["scopes"][sid]["reference"][fam]
            for sid, fam in focal_coords
        )
        controls.append({
            "focal_source_sid": source_sid,
            "focal_target_sid": target_sid,
            "control_event_source_sid": other[0],
            "control_event_target_sid": other[1],
            "control_available": True,
            "focal_branch_state_unchanged": unchanged,
        })

    return eligible, event_results, controls


def source_stats(model):
    positive = collections.Counter()
    branch_profiles = collections.Counter()
    unresolved_outgoing = []

    for sid, s in model["scopes"].items():
        r = s["reference"]
        flags = (
            bool(r["B_INCOMING"]),
            r["B_OUTGOING"]["literal"] is not None,
            bool(r["B_CANCEL"]),
        )
        branch_profiles[str(flags)] += 1
        positive["B_INCOMING"] += int(flags[0])
        positive["B_OUTGOING"] += int(flags[1])
        positive["B_CANCEL"] += int(flags[2])

        if (
            r["B_OUTGOING"]["literal"] is not None
            and r["B_OUTGOING"]["resolution"]
            != "RESOLVED_INTERNAL_UNIQUE"
        ):
            unresolved_outgoing.append({
                "sid": sid,
                "outgoing": r["B_OUTGOING"],
            })

    return {
        "scope_count": len(model["scopes"]),
        "positive_scopes_by_family": dict(positive),
        "branch_profile_distribution": dict(sorted(branch_profiles.items())),
        "nonuniquely_resolved_outgoing": unresolved_outgoing,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("results"),
    )
    args = ap.parse_args()

    if args.source:
        raw = args.source.read_bytes()
    else:
        req = urllib.request.Request(
            URL,
            headers={"User-Agent": "CRR-module-B/1.1"},
        )
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()

    got = git_blob_sha1(raw)
    if got != MS_BLOB:
        raise RuntimeError(f"source drift: {got}")

    model = build_model(raw)

    interfaces = [
        eval_interface(model, "CURRENT_SUMMARY"),
        eval_interface(model, "START_ATTRS_PLUS_TEXT"),
        eval_interface(model, "LOCAL_SCOPE_SERIALIZATION"),
        eval_interface(model, "SOURCE_LINKED"),
    ]
    current_collisions = current_collision_groups(model)
    local_collisions = local_serialization_collision_groups(model)
    eligible, events, controls = controlled_updates(model)

    reopen = {
        "cold_source_bytes": len(raw),
        "logical_reopen_per_scope": 1,
        "batch_cache_source_reads": 1,
        "post_reopen_exact_family_decisions": 3 * len(model["scopes"]),
        "post_reopen_informative_wrong": 0,
    }

    result = {
        "study": "MODULE_B_FV_SOURCE_TRIGGERED_BRANCHING_SELECTIVE_UPDATE_V1",
        "authority": "DEVELOPMENT_ON_ALREADY_EXPOSED_C18",
        "implementation_repair": (
            "IMPLEMENTATION_REPAIR_v1.md; first run stopped before outcomes"
        ),
        "source": {
            "commit": PIN,
            "path": MS_PATH,
            "git_blob_sha1": got,
            "sha256": sha256(raw),
            "bytes": len(raw),
        },
        "population": source_stats(model),
        "interfaces": interfaces,
        "natural_current_summary_collision_count": len(current_collisions),
        "natural_current_summary_collisions": current_collisions,
        "byte_identical_local_serialization_incoming_collision_count": len(
            local_collisions
        ),
        "byte_identical_local_serialization_incoming_collisions": local_collisions,
        "charged_source_reopen": reopen,
        "controlled_selective_update": {
            "eligible_internal_next_relations": [
                {
                    "source_sid": s,
                    "target_sid": t,
                    "literal_next": lit,
                }
                for s, t, lit in eligible
            ],
            "event_count": len(events),
            "pass_count": sum(e["selective_update_pass"] for e in events),
            "cancel_ledger_unchanged_count": sum(
                e["cancel_ledger_unchanged"] for e in events
            ),
            "events": events,
            "unrelated_controls_available": sum(
                c.get("control_available", False) for c in controls
            ),
            "unrelated_controls_pass": sum(
                c.get("control_available", False)
                and c.get("focal_branch_state_unchanged", False)
                for c in controls
            ),
            "unrelated_controls": controls,
        },
        "claim_boundaries": [
            "C18 is already exposed development material, not independent transfer.",
            "Branch families are explicit TEI/source operations, not autonomous natural-language question generation.",
            "UNKNOWN is not FALSE and safe abstention is allowed.",
            "SOURCE_LINKED is a strong ordinary provenance/navigation baseline and receives full credit.",
            "Milestone-bounded local serializations may be structurally unbalanced; exact cancellation negatives are not inferred from them.",
            "Removing @next is a controlled relation-status event, not a naturally observed editorial revision.",
            "Current-answer collisions do not imply complete-source identity.",
            "No literary, genetic, authorship, or historical-truth conclusion is inferred from the encoding.",
        ],
    }

    args.out.mkdir(parents=True, exist_ok=True)
    out = args.out / "results.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("MODULE_B_FV_SOURCE_TRIGGERED_BRANCHING_SELECTIVE_UPDATE_V1")
    print(f"scope_count={result['population']['scope_count']}")
    for k, v in result["population"]["positive_scopes_by_family"].items():
        print(f"positive_{k}={v}")
    print(
        "natural_current_summary_collision_count="
        + str(len(current_collisions))
    )
    print(
        "local_serialization_incoming_collision_count="
        + str(len(local_collisions))
    )

    for x in interfaces:
        print(
            "INTERFACE,"
            + x["interface"]
            + f",exact={x['exact_determined']}"
            + f",unknown={x['unknown']}"
            + f",wrong={x['informative_wrong']}"
            + f",trigger_false_positive={x['trigger_false_positive']}"
            + f",positive_trigger_coverage={x['positive_branch_trigger_coverage']:.6f}"
        )

    print(f"controlled_next_events={len(events)}")
    print(
        "controlled_next_pass="
        + str(sum(e["selective_update_pass"] for e in events))
    )
    print(
        "unrelated_controls_available="
        + str(sum(c.get("control_available", False) for c in controls))
    )
    print(
        "unrelated_controls_pass="
        + str(
            sum(
                c.get("control_available", False)
                and c.get("focal_branch_state_unchanged", False)
                for c in controls
            )
        )
    )
    print("RESULT_SHA256=" + sha256(out.read_bytes()))


if __name__ == "__main__":
    main()
