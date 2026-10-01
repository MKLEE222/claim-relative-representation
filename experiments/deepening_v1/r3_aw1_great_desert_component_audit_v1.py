from __future__ import annotations

import runpy
from pathlib import Path
import json

AW1 = Path("experiments/deepening_v1/r3_aw1_entry_span_repair_v2.py")
ns = runpy.run_path(str(AW1))

case = next(c for c in ns["CASES"] if c["id"] == "R3Q-DES-EVIDENCE")
text = ns["text"]
base_ws = ns["base_ws"]
full_ws = ns["full_ws"]
later_ws = ns["later_ws"]
frame = ns["frame"]

seed, pa, pb, dist = ns["seed_paragraph"](
    text["V1"], case["seed_a"], case["seed_b"], focus_on_b=True
)
q = ns["query"](seed, case["task"], base_ws, case["forbidden"])
qterms = [t for t, _ in q]

expected_query = [
    "charkalyk","evil","ouash","shahri","spirits","charchan",
    "days","supports","wastes","roads","beneficent","malignant"
]
if qterms != expected_query:
    raise RuntimeError(f"AW1 query replay mismatch: {qterms}")

entry = frame[case["gold_entry"]]

def ranked(ws):
    return sorted(
        ((ns["score"](w, q), w) for w in ws),
        key=lambda z: (-z[0], z[1].scope, z[1].start),
    )

def entry_rank(ranked_list):
    for i, (_, w) in enumerate(ranked_list, 1):
        if w.scope in ("V2", "LATER") and ns["overlap"](
            w, entry["source_start"], entry["source_end"]
        ):
            return i
    return None

full_ranked = ranked(full_ws)
later_ranked = ranked(later_ws)

if entry_rank(full_ranked) != 6:
    raise RuntimeError(f"AW1 full entry rank mismatch: {entry_rank(full_ranked)}")
if entry_rank(later_ranked) != 1:
    raise RuntimeError(f"AW1 later entry rank mismatch: {entry_rank(later_ranked)}")

anchors = {
    "FOLKLORE_SOURCE": "faithful reflex of old folklore beliefs he must have heard on the spot",
    "MEASUREMENT": "plane-table survey, checked by cyclometer readings",
}

v2_tokens = ns["token_stream"](text["V2"])

def find_span(anchor):
    # Evaluation-only locator: exact token sequence, insensitive to Gutenberg
    # line wrapping, punctuation and emphasis markup.
    need = ns["toks"](anchor)
    vals = [x for x, _, __ in v2_tokens]
    for i in range(0, len(vals) - len(need) + 1):
        if vals[i:i + len(need)] == need:
            return v2_tokens[i][1], v2_tokens[i + len(need) - 1][2]
    raise RuntimeError(f"component anchor missing: {anchor}")

spans = {k: find_span(v) for k, v in anchors.items()}

def component_rank(ranked_list, span):
    lo, hi = span
    for i, (score, w) in enumerate(ranked_list, 1):
        if w.scope in ("V2", "LATER") and ns["overlap"](w, lo, hi):
            return i, score
    return None, None

def scope_result(ranked_list):
    groups = {}
    for gid, span in spans.items():
        r, s = component_rank(ranked_list, span)
        groups[gid] = {"rank": r, "score": s}

    one_window = False
    for _, w in ranked_list:
        if w.scope not in ("V2", "LATER"):
            continue
        if all(ns["overlap"](w, lo, hi) for lo, hi in spans.values()):
            one_window = True
            break

    collective = {}
    for budget in (10, 20, 50):
        ok = True
        for span in spans.values():
            if not any(
                w.scope in ("V2", "LATER") and ns["overlap"](w, span[0], span[1])
                for _, w in ranked_list[:budget]
            ):
                ok = False
                break
        collective[str(budget)] = ok

    return {
        "groups": groups,
        "single_window_complete": one_window,
        "collective_complete": collective,
    }

result = {
    "study": "R3_AW1_GREAT_DESERT_COMPONENT_AUDIT_V1",
    "status": "RETROSPECTIVE_POST_OUTCOME_DIAGNOSTIC",
    "aw1_query_terms": qterms,
    "aw1_entry_ranks_reproduced": {
        "GSA_FULL_OBJECT": 6,
        "GSA_LATER_LAYER": 1,
    },
    "seed_anchor_distance_chars": dist,
    "component_spans_v2": {
        k: {"char_lo": lo, "char_hi": hi} for k, (lo, hi) in spans.items()
    },
    "scopes": {
        "GSA_FULL_OBJECT": scope_result(full_ranked),
        "GSA_LATER_LAYER": scope_result(later_ranked),
    },
}

out = Path("experiments/deepening_v1/results")
out.mkdir(parents=True, exist_ok=True)
(out / "r3_aw1_great_desert_component_audit_v1.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)

print("R3_AW1_GREAT_DESERT_COMPONENT_AUDIT_V1")
print("aw1_query_reproduced=1")
print("aw1_full_entry_rank=6")
print("aw1_later_entry_rank=1")
for name, s in result["scopes"].items():
    g = s["groups"]
    print(",".join([
        "RESULT", name,
        f"folklore_rank={g['FOLKLORE_SOURCE']['rank']}",
        f"measurement_rank={g['MEASUREMENT']['rank']}",
        f"single={int(s['single_window_complete'])}",
        f"H10all={int(s['collective_complete']['10'])}",
        f"H20all={int(s['collective_complete']['20'])}",
        f"H50all={int(s['collective_complete']['50'])}",
    ]))
