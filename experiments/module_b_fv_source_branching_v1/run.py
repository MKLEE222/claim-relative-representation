from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import urllib.request
from pathlib import Path

from lxml import etree as E

PIN = "5a208f869ff1213defa000e3181d5315a072a15f"
APP_PATH = "collationChunks/C18/output/Collation_C18-complete.xml"
MS_PATH = "collationChunks/C18/msColl_C18.xml"
EXPECTED = {
    APP_PATH: "bca0548912ab1d7b2676360d33a6468290296d7e",
    MS_PATH: "8e537331ebf46dd4f013da9afcbe38c14092b6fd",
}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()

def name(e):
    return E.QName(e).localname

def xmlparse(raw):
    return E.fromstring(raw, E.XMLParser(collect_ids=False, resolve_entities=False, no_network=True))

def valid_fragment(raw):
    return xmlparse(("<unit>" + raw.replace("&", "&amp;") + "</unit>").encode())

def current_view(app):
    return {
        "app_attributes": dict(app.attrib),
        "namespace_bindings": app.nsmap,
        "children": [
            {
                "tag": name(g),
                "attrs": dict(g.attrib),
                "readings": [
                    {
                        "tag": name(r),
                        "attrs": dict(r.attrib),
                        "raw": "".join(r.itertext()),
                    }
                    for r in g
                ],
            }
            for g in app
        ],
    }

def current_answer(view):
    return [
        {
            "normalized_descriptor": g["attrs"].get("n"),
            "witnesses": [r["attrs"].get("wit") for r in g["readings"]],
        }
        for g in view["children"]
    ]

class ScopeParser:
    def __init__(self, initial=None):
        self.active = dict(initial or {})
        self.spans = {}
        self.segments = []
        self.unit = None

    def text(self, s):
        if s and s.strip():
            self.segments.append(
                {
                    "text": s,
                    "unit": self.unit,
                    "active_ids": list(self.active),
                    "scope_attributes": {k: dict(v) for k, v in self.active.items()},
                }
            )
            for sid in self.active:
                if sid in self.spans:
                    self.spans[sid]["texts"].append(s)

    def walk(self, node):
        tag = name(node)
        if tag == "sga-add":
            start, end = node.get("sID"), node.get("eID")
            if bool(start) == bool(end):
                raise ValueError("ambiguous sga-add marker")
            if start:
                if start in self.active or start in self.spans:
                    raise ValueError("duplicate start " + start)
                attrs = dict(node.attrib)
                self.active[start] = attrs
                self.spans[start] = {
                    "attrs": attrs,
                    "start_unit": self.unit,
                    "end_unit": None,
                    "texts": [],
                }
            else:
                if end not in self.active:
                    raise ValueError("unbound close " + end)
                self.active.pop(end)
                if end in self.spans:
                    self.spans[end]["end_unit"] = self.unit
        self.text(node.text)
        for child in node:
            self.walk(child)
            self.text(child.tail)

    def feed(self, node, unit):
        self.unit = unit
        self.walk(node)

class LocalVisibleParser:
    """Conservative local-only parser. It never treats missing prior context as OUTSIDE."""
    def __init__(self):
        self.active = {}
        self.segments = []
        self.unmatched_close = False
        self.visible_cancellations = []

    def text(self, s):
        if s and s.strip():
            self.segments.append({"text": s, "active_ids": list(self.active)})

    def walk(self, node):
        tag = name(node)
        if tag == "sga-add":
            start, end = node.get("sID"), node.get("eID")
            if start:
                self.active[start] = dict(node.attrib)
            elif end:
                if end in self.active:
                    self.active.pop(end)
                else:
                    self.unmatched_close = True
        if tag in {"del", "mdel"} and self.active:
            txt = " ".join("".join(node.itertext()).split())
            if txt:
                self.visible_cancellations.append(
                    {"active_ids": list(self.active), "element": tag, "text": txt}
                )
        self.text(node.text)
        for child in node:
            self.walk(child)
            self.text(child.tail)

def status_from_segments(segments):
    nonempty = [s for s in segments if s["text"].strip()]
    if not nonempty:
        return "NO_TEXT"
    inside = [bool(s["active_ids"]) for s in nonempty]
    if all(inside):
        return "INSIDE"
    if not any(inside):
        return "OUTSIDE"
    return "MIXED"

def active_ids_from_segments(segments):
    return sorted({sid for s in segments for sid in s.get("active_ids", [])})

def build_source_scope_index(source_raw):
    text = source_raw.decode("utf-8")
    tag_re = re.compile(r"<sga-add\b[^>]*?/>")
    starts = {}
    spans = {}
    marker_attrs = {}
    for m in tag_re.finditer(text):
        e = xmlparse(m.group().encode())
        attrs = dict(e.attrib)
        sid = e.get("sID")
        eid = e.get("eID")
        if sid:
            starts[sid] = (m.end(), attrs, m.start())
            marker_attrs[sid] = attrs
        elif eid:
            if eid not in starts:
                raise RuntimeError("raw source unbound close " + eid)
            lo, attrs, marker_start = starts.pop(eid)
            inner = text[lo : m.start()]
            frag = xmlparse(("<fragment>" + inner + "</fragment>").encode())
            cancellations = []
            for n in frag.iter():
                if name(n) in {"del", "mdel"}:
                    t = " ".join("".join(n.itertext()).split())
                    if t:
                        cancellations.append({"element": name(n), "text": t})
            spans[eid] = {
                "sid": eid,
                "attrs": attrs,
                "text": " ".join("".join(frag.itertext()).split()),
                "cancellations": cancellations,
                "source_char_span": [marker_start, m.end()],
            }
    if starts:
        raise RuntimeError("raw source unclosed sga-add spans")

    id_to_sid = {}
    for sid, rec in spans.items():
        xid = rec["attrs"].get(XML_ID)
        if xid:
            id_to_sid[xid] = sid

    incoming = collections.defaultdict(list)
    for predecessor_sid, rec in spans.items():
        nxt = rec["attrs"].get("next")
        if nxt and nxt.startswith("#") and nxt[1:] in id_to_sid:
            incoming[id_to_sid[nxt[1:]]].append(predecessor_sid)

    return spans, {k: sorted(v) for k, v in incoming.items()}

def branch_for(active_ids, source_spans, incoming):
    if not active_ids:
        return [], {
            "predecessor_relation": "NOT_ASSESSED",
            "internal_cancellation": "NOT_ASSESSED",
            "predecessors": {},
            "cancellations": {},
        }
    preds = {sid: incoming.get(sid, []) for sid in active_ids if incoming.get(sid)}
    canc = {
        sid: source_spans[sid]["cancellations"]
        for sid in active_ids
        if source_spans[sid]["cancellations"]
    }
    branches = []
    if preds:
        branches.append("B_PREDECESSOR")
    if canc:
        branches.append("B_INTERNAL_CANCELLATION")
    if not branches:
        branches.append("B_SCOPE_ONLY")
    return sorted(branches), {
        "predecessor_relation": "PRESENT" if preds else "ABSENT_AFTER_INSPECTION",
        "internal_cancellation": "PRESENT" if canc else "ABSENT_AFTER_INSPECTION",
        "predecessors": preds,
        "cancellations": canc,
    }

def reference_state(segments, source_spans, incoming):
    status = status_from_segments(segments)
    ids = active_ids_from_segments(segments)
    branches, rich = branch_for(ids, source_spans, incoming)
    if status in {"OUTSIDE", "NO_TEXT"}:
        branches = []
        rich = {
            "predecessor_relation": "NOT_ASSESSED",
            "internal_cancellation": "NOT_ASSESSED",
            "predecessors": {},
            "cancellations": {},
        }
    return {
        "insertion_scope": status,
        "branches": branches,
        **rich,
        "active_scope_ids": ids,
    }

def independent_intervals(raws):
    offsets = []
    pos = 0
    for raw in raws:
        offsets.append(pos)
        pos += len(raw)
    text = "".join(raws)
    starts = {}
    intervals = {}
    tag_re = re.compile(r"<[^>]*>")
    for m in tag_re.finditer(text):
        if not m.group().startswith("<sga-add"):
            continue
        e = xmlparse(m.group().replace("&", "&amp;").encode())
        if e.get("sID"):
            starts[e.get("sID")] = m.end()
        elif e.get("eID"):
            sid = e.get("eID")
            if sid not in starts:
                raise RuntimeError("independent scanner unbound close " + sid)
            intervals[sid] = (starts.pop(sid), m.start())
    if starts:
        raise RuntimeError("independent scanner unclosed spans")

    by_unit = []
    for raw, off in zip(raws, offsets):
        segs = []
        last = 0
        for m in list(tag_re.finditer(raw)) + [None]:
            end = len(raw) if m is None else m.start()
            part = raw[last:end]
            if part.strip():
                lo, hi = off + last, off + end
                ids = [sid for sid, (a, b) in intervals.items() if a <= lo and hi <= b]
                segs.append({"text": part, "active_ids": sorted(ids)})
            if m is not None:
                last = m.end()
        by_unit.append(segs)
    return by_unit

def local_only_prediction(raw):
    parser = LocalVisibleParser()
    try:
        parser.walk(valid_fragment(raw))
    except Exception:
        return {
            "insertion_scope": "UNRESOLVED",
            "branches": [],
            "predecessor_relation": "NOT_ASSESSED",
            "internal_cancellation": "NOT_ASSESSED",
        }
    nonempty = [s for s in parser.segments if s["text"].strip()]
    if not nonempty:
        scope = "NO_TEXT"
    elif all(s["active_ids"] for s in nonempty) and not parser.unmatched_close:
        scope = "INSIDE"
    else:
        scope = "UNRESOLVED"
    branches = []
    internal = "NOT_ASSESSED"
    if parser.visible_cancellations:
        branches.append("B_INTERNAL_CANCELLATION")
        internal = "PRESENT"
    return {
        "insertion_scope": scope,
        "branches": branches,
        "predecessor_relation": "NOT_ASSESSED",
        "internal_cancellation": internal,
    }

def state_exact(pred, ref):
    keys = [
        "insertion_scope",
        "branches",
        "predecessor_relation",
        "internal_cancellation",
    ]
    return all(pred.get(k) == ref.get(k) for k in keys)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", type=Path, default=Path(__file__).with_name("sources"))
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("results"))
    ap.add_argument("--download-sources", action="store_true")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if args.download_sources:
        for rel in EXPECTED:
            dest = args.sources / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            url = f"https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{PIN}/{rel}"
            req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-B/1.0"})
            with urllib.request.urlopen(req, timeout=90) as response:
                dest.write_bytes(response.read())

    raw_sources = {rel: (args.sources / rel).read_bytes() for rel in EXPECTED}
    for rel, expected in EXPECTED.items():
        got = git_blob(raw_sources[rel])
        if got != expected:
            raise RuntimeError(f"source drift {rel}: {got}")

    root = xmlparse(raw_sources[APP_PATH])
    apps = list(root)
    if len(apps) != 493:
        raise RuntimeError("unexpected C18 apparatus population")

    raw_ms = []
    views = []
    q0 = []
    native_xml = []
    for app in apps:
        view = current_view(app)
        views.append(view)
        q0.append(current_answer(view))
        native_xml.append(E.tostring(app, with_tail=False))
        ms = app.xpath('.//rdg[@wit="fMS"]')
        if len(ms) > 1:
            raise RuntimeError("multiple fMS readings in app")
        raw_ms.append("".join(ms[0].itertext()) if ms else "")

    source_spans, incoming = build_source_scope_index(raw_sources[MS_PATH])

    # Primary full-stream reference.
    parser = ScopeParser()
    contexts = []
    ref_segments = []
    ref_states = []
    for i, raw in enumerate(raw_ms):
        contexts.append(json.loads(json.dumps(parser.active)))
        begin = len(parser.segments)
        parser.feed(valid_fragment(raw), i)
        segs = parser.segments[begin:]
        ref_segments.append(segs)
        ref_states.append(reference_state(segs, source_spans, incoming))
    if parser.active:
        raise RuntimeError("unclosed apparatus addition state")
    missing = set(active_ids_from_segments([s for group in ref_segments for s in group])) - set(source_spans)
    if missing:
        raise RuntimeError("apparatus scope IDs absent from raw source: " + repr(sorted(missing)))

    # Independent source-linked decoder: interval containment, then pinned source relation lookup.
    independent = independent_intervals(raw_ms)
    source_linked = [reference_state(segs, source_spans, incoming) for segs in independent]
    source_linked_exact = [state_exact(p, r) for p, r in zip(source_linked, ref_states)]
    if not all(source_linked_exact):
        bad = [i + 1 for i, ok in enumerate(source_linked_exact) if not ok]
        raise RuntimeError("independent source-linked decoder disagrees at " + repr(bad[:20]))

    # Open-scope-state interface: local app + inherited state + source relation lookup by discovered SID.
    scope_state_predictions = []
    for i, raw in enumerate(raw_ms):
        p = ScopeParser(contexts[i])
        begin = len(p.segments)
        p.feed(valid_fragment(raw), i)
        segs = p.segments[begin:]
        scope_state_predictions.append(reference_state(segs, source_spans, incoming))
    scope_state_exact = [state_exact(p, r) for p, r in zip(scope_state_predictions, ref_states)]

    local_predictions = [local_only_prediction(raw) for raw in raw_ms]
    local_exact = [state_exact(p, r) for p, r in zip(local_predictions, ref_states)]

    # Byte-identical native local payload equivalence classes.
    classes = collections.defaultdict(list)
    for i, raw in enumerate(native_xml):
        classes[raw].append(i)
    ambiguous_classes = []
    for raw, ids in classes.items():
        signatures = collections.defaultdict(list)
        for i in ids:
            sig = canonical(
                {
                    "insertion_scope": ref_states[i]["insertion_scope"],
                    "branches": ref_states[i]["branches"],
                    "predecessor_relation": ref_states[i]["predecessor_relation"],
                    "internal_cancellation": ref_states[i]["internal_cancellation"],
                }
            )
            signatures[sig].append(i)
        if len(signatures) <= 1:
            continue
        members = []
        for i in ids:
            members.append(
                {
                    "app_ordinal_1_based": i + 1,
                    "q0_sha256": sha256(canonical(q0[i])),
                    "reference": ref_states[i],
                }
            )
        ambiguous_classes.append(
            {
                "native_app_sha256": sha256(raw),
                "native_app_bytes": len(raw),
                "members": members,
                "distinct_continuation_states": len(signatures),
            }
        )
    ambiguous_classes.sort(key=lambda x: min(m["app_ordinal_1_based"] for m in x["members"]))

    # Equal-byte wrong locator controls for every member in an ambiguous local class.
    locator_controls = []
    for c in ambiguous_classes:
        members = c["members"]
        for m in members:
            i = m["app_ordinal_1_based"] - 1
            other = next(
                n
                for n in members
                if canonical(n["reference"]) != canonical(m["reference"])
            )
            j = other["app_ordinal_1_based"] - 1
            correct = {"commit": PIN, "path": APP_PATH, "app_ordinal": f"{i + 1:06d}"}
            wrong = {"commit": PIN, "path": APP_PATH, "app_ordinal": f"{j + 1:06d}"}
            if len(canonical(correct)) != len(canonical(wrong)):
                raise AssertionError("locator byte mismatch")
            locator_controls.append(
                {
                    "app_ordinal_1_based": i + 1,
                    "wrong_ordinal": j + 1,
                    "locator_bytes": len(canonical(correct)),
                    "current_answer_same": q0[i] == q0[j],
                    "correct_state_exact": state_exact(source_linked[i], ref_states[i]),
                    "wrong_state_fails": not state_exact(source_linked[j], ref_states[i]),
                    "correct_branches": source_linked[i]["branches"],
                    "wrong_branches": source_linked[j]["branches"],
                }
            )

    # Branch and dependency-aware summaries.
    branch_counts = collections.Counter()
    scope_counts = collections.Counter()
    unique_scope_by_branch = collections.defaultdict(set)
    for st in ref_states:
        scope_counts[st["insertion_scope"]] += 1
        for b in st["branches"]:
            branch_counts[b] += 1
            unique_scope_by_branch[b].update(st["active_scope_ids"])

    # Precision/recall of conservative local-only branch emission.
    tp = fp = fn = 0
    for pred, ref in zip(local_predictions, ref_states):
        ps, rs = set(pred["branches"]), set(ref["branches"])
        tp += len(ps & rs)
        fp += len(ps - rs)
        fn += len(rs - ps)

    # Selective state update: q0 immutable, only continuation fields differ from initial state.
    initial = {
        "insertion_scope": "UNRESOLVED",
        "predecessor_relation": "NOT_ASSESSED",
        "internal_cancellation": "NOT_ASSESSED",
    }
    updates = []
    for i, ref in enumerate(ref_states):
        before = {"alignment": q0[i], **initial}
        after = {
            "alignment": q0[i],
            "insertion_scope": ref["insertion_scope"],
            "predecessor_relation": ref["predecessor_relation"],
            "internal_cancellation": ref["internal_cancellation"],
        }
        changed = [k for k in initial if before[k] != after[k]]
        updates.append(
            {
                "app_ordinal_1_based": i + 1,
                "changed_fields": changed,
                "alignment_unchanged": before["alignment"] == after["alignment"],
                "branches": ref["branches"],
            }
        )
    selective_state_update = all(x["alignment_unchanged"] for x in updates)

    # Source-linked route cost is an implemented upper bound, not a minimum.
    link_payloads = [
        {"commit": PIN, "path": APP_PATH, "app_ordinal": f"{i + 1:06d}"}
        for i in range(len(apps))
    ]
    state_payloads = contexts

    result = {
        "study": "MODULE_B_FV_SOURCE_BRANCHING_V1",
        "authority": "POST_INSPECTION_DEVELOPMENT_NOT_CONFIRMATORY",
        "protocol_status": "FROZEN_BEFORE_THIS_EXECUTION",
        "upstream_commit": PIN,
        "sources": {
            p: {
                "git_blob": EXPECTED[p],
                "sha256": sha256(b),
                "bytes": len(b),
            }
            for p, b in raw_sources.items()
        },
        "population": {
            "apparatus_units": len(apps),
            "scope_status_counts": dict(scope_counts),
            "source_addition_spans": len(source_spans),
            "branch_checkpoint_counts": dict(branch_counts),
            "unique_source_scope_counts_by_branch": {
                k: len(v) for k, v in unique_scope_by_branch.items()
            },
        },
        "reference_branch_grammar": {
            "B_PREDECESSOR": "incoming source sga-add @next targets enclosing addition xml:id",
            "B_INTERNAL_CANCELLATION": "enclosing source addition contains textual del/mdel",
            "B_SCOPE_ONLY": "inside encoded addition with neither richer branch",
            "outside": "no insertion-specific branch licensed",
        },
        "interfaces": {
            "I_NATIVE_FULL": {
                "reference_states": len(ref_states),
                "q0_preserved": len(apps),
            },
            "I_SOURCE_LINKED": {
                "exact_continuation_states": sum(source_linked_exact),
                "denominator": len(apps),
                "q0_preserved": len(apps),
                "one_cold_apparatus_reopen_bytes": len(raw_sources[APP_PATH]),
                "one_cold_manuscript_source_bytes": len(raw_sources[MS_PATH]),
                "all_locator_payload_bytes": len(canonical(link_payloads)),
                "method": "independent global interval scanner plus pinned source relation lookup",
            },
            "I_SCOPE_STATE": {
                "exact_continuation_states": sum(scope_state_exact),
                "denominator": len(apps),
                "q0_preserved": len(apps),
                "all_inherited_state_payload_bytes": len(canonical(state_payloads)),
                "construction_requires_prior_full-stream_scan": True,
            },
            "I_LOCAL_ONLY": {
                "exact_continuation_states": sum(local_exact),
                "denominator": len(apps),
                "branch_true_positives": tp,
                "branch_false_positives": fp,
                "branch_false_negatives": fn,
                "precision": None if tp + fp == 0 else tp / (tp + fp),
                "recall": None if tp + fn == 0 else tp / (tp + fn),
                "policy": "emit only directly visible internal-cancellation branch; never infer OUTSIDE from absent inherited state",
            },
        },
        "local_identifiability": {
            "byte_identical_classes_with_different_continuation_state": len(ambiguous_classes),
            "checkpoint_count": sum(len(c["members"]) for c in ambiguous_classes),
            "classes": ambiguous_classes,
        },
        "wrong_locator_control": {
            "tested": len(locator_controls),
            "correct_exact": sum(x["correct_state_exact"] for x in locator_controls),
            "wrong_fails": sum(x["wrong_state_fails"] for x in locator_controls),
            "all_current_answers_same": all(x["current_answer_same"] for x in locator_controls),
            "matched_locator_bytes": len({x["locator_bytes"] for x in locator_controls}) <= 1,
            "details": locator_controls,
        },
        "selective_state_update": {
            "alignment_invariant_all": selective_state_update,
            "updated_checkpoint_count": sum(bool(x["changed_fields"]) for x in updates),
            "field_change_counts": dict(
                collections.Counter(k for x in updates for k in x["changed_fields"])
            ),
            "note": "Resolution of UNRESOLVED/NOT_ASSESSED fields is state refinement, not established belief revision.",
        },
        "dispositions": {
            "MODULE_B_BRANCHING_OBSERVED": len(branch_counts) >= 2,
            "LOCAL_CURRENT_EQUIVALENCE_CONTINUATION_SEPARATION": len(ambiguous_classes) > 0,
            "SOURCE_LINKED_BRANCH_RECOVERY": all(source_linked_exact),
            "SCOPE_STATE_BRANCH_RECOVERY": all(scope_state_exact),
            "SELECTIVE_STATE_UPDATE": selective_state_update,
            "AUTONOMOUS_QUESTION_DISCOVERY": False,
            "SELECTIVE_BELIEF_REVISION": False,
            "INDEPENDENT_TRANSFER": False,
        },
        "claim_boundary": [
            "C18 is exposed development material.",
            "Branch eligibility is source-structural and frozen; it is not an LLM question-generation result.",
            "The source-linked baseline is credited if it solves the task.",
            "Resolving an unassessed state is not a demonstrated reversal of a substantive scholarly belief.",
            "Byte-identical local collisions omit global ordinal, inherited state, and source reopening.",
            "Multiple checkpoints can share one addition scope and are not independent replications.",
            "No absence of insertion-specific branch implies absence of every possible scholarly follow-up.",
        ],
    }

    out = args.out / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "updates.json").write_text(
        json.dumps(updates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    scientific = dict(result)
    print(json.dumps({
        "population": result["population"],
        "interfaces": result["interfaces"],
        "local_identifiability": {
            k: v for k, v in result["local_identifiability"].items() if k != "classes"
        },
        "wrong_locator_control": {
            k: v for k, v in result["wrong_locator_control"].items() if k != "details"
        },
        "selective_state_update": result["selective_state_update"],
        "dispositions": result["dispositions"],
        "results_sha256": sha256(out.read_bytes()),
        "scientific_payload_sha256": sha256(canonical(scientific)),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
