from __future__ import annotations

import hashlib
import json
from pathlib import Path

from r3_generic_access_transfer_v1 import (
    URLS, EXPECTED, WINDOW, STRIDE, QUERY_K,
    fetch, sha, make_windows, locate_addenda, seed_span, find_seed_window,
    build_query, ranked_candidates, find_anchor_windows, group_rank,
    all_groups_in_one_window, collective_complete, toks,
)

INQUIRY_ID = "R3Q-DES-EVIDENCE"
SEED_ANCHOR = "The waste and desert places of the Earth"
TASK = (
    "Find later editorial treatment bearing on the Great Desert folklore source "
    "interpretation and the distance or marches described in the earlier note."
)
GROUPS = {
    "FOLKLORE_SOURCE":
        "faithful reflex of old folklore beliefs he must have heard on the spot",
    "MEASUREMENT":
        "plane-table survey checked by cyclometer readings",
}


def main() -> None:
    raw = {k: fetch(v) for k, v in URLS.items()}
    got = {k: sha(v) for k, v in raw.items()}
    if got != EXPECTED:
        raise RuntimeError(f"source drift: {got}")

    text = {k: raw[k].decode("utf-8", errors="replace") for k in raw}
    boundary = locate_addenda(text["V2"])

    v1_ws = make_windows("V1", text["V1"])
    v2_base_ws = make_windows("V2_BASE", text["V2"][:boundary])
    v2_full_ws = make_windows("V2", text["V2"])
    later_ws = make_windows("V2_LATER", text["V2"][boundary:])

    base_ws = v1_ws + v2_base_ws
    full_ws = v1_ws + v2_full_ws

    seed = seed_span(text["V1"], SEED_ANCHOR)
    seed_w = find_seed_window(v1_ws, SEED_ANCHOR)
    q = build_query(seed, TASK, base_ws)

    qterms = {t for t, _ in q}
    seed_terms = set(toks(seed))
    eval_terms = set()
    for anchor in GROUPS.values():
        eval_terms.update(toks(anchor))
    leaked = sorted(t for t in qterms if t in eval_terms and t not in seed_terms)
    if leaked:
        raise RuntimeError(f"INVALID_LEAKAGE: {leaked}")

    scopes = {}
    for name, ws, seed_exclusion in [
        ("GSA_FULL_OBJECT", full_ws, seed_w),
        ("GSA_LATER_LAYER", later_ws, None),
    ]:
        ranked = ranked_candidates(ws, q, seed_exclusion)
        group_windows = {
            gid: find_anchor_windows(ws, anchor)
            for gid, anchor in GROUPS.items()
        }

        groups = {}
        for gid, hits in group_windows.items():
            rank, score = group_rank(ranked, hits)
            groups[gid] = {
                "target_window_count": len(hits),
                "rank": rank,
                "score": score,
                "rr": 0.0 if rank is None else 1.0 / rank,
                "H10": int(rank is not None and rank <= 10),
                "H20": int(rank is not None and rank <= 20),
                "H50": int(rank is not None and rank <= 50),
            }

        scopes[name] = {
            "candidate_count": len(ranked),
            "groups": groups,
            "single_window_complete": all_groups_in_one_window(ws, GROUPS),
            "collective_H10_complete": collective_complete(ranked, group_windows, 10),
            "collective_H20_complete": collective_complete(ranked, group_windows, 20),
            "collective_H50_complete": collective_complete(ranked, group_windows, 50),
        }

    result = {
        "study": "R3_GREAT_DESERT_EXACT_START_V1",
        "inquiry_id": INQUIRY_ID,
        "entry_state": "HISTORICAL_START_FROM_1903_I_P202",
        "seed_anchor": SEED_ANCHOR,
        "seed_sha256": hashlib.sha256(seed.encode("utf-8")).hexdigest(),
        "task": TASK,
        "query_terms": [t for t, _ in q],
        "leakage_overlap": [],
        "source_sha256": got,
        "parameters": {
            "window": WINDOW,
            "stride": STRIDE,
            "query_k": QUERY_K,
            "ranking": "weighted lexical overlap",
            "idf_scope": "V1 + V2 pre-Addenda",
        },
        "scopes": scopes,
        "comparison_reference": {
            "study": "R3_GENERIC_ACCESS_TRANSFER_V1",
            "broader_start": {
                "GSA_FULL_OBJECT": {
                    "FOLKLORE_SOURCE_rank": 77,
                    "MEASUREMENT_rank": 146,
                    "collective_H50_complete": 0,
                },
                "GSA_LATER_LAYER": {
                    "FOLKLORE_SOURCE_rank": 15,
                    "MEASUREMENT_rank": 31,
                    "collective_H50_complete": 1,
                },
            },
        },
    }

    out = Path("experiments/deepening_v1/results")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "r3_great_desert_exact_start_v1.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("R3_GREAT_DESERT_EXACT_START_V1")
    print("source_sha256_V1=" + got["V1"])
    print("source_sha256_V2=" + got["V2"])
    print("seed_anchor=" + SEED_ANCHOR)
    print("query_terms=" + "|".join(result["query_terms"]))
    print("leakage_overlap=0")
    for name, s in scopes.items():
        gs = ";".join(f"{gid}:r{g['rank']}" for gid, g in s["groups"].items())
        print(",".join([
            "RESULT", name,
            f"candidates={s['candidate_count']}",
            f"groups={gs}",
            f"single={int(s['single_window_complete'])}",
            f"H10all={int(s['collective_H10_complete'])}",
            f"H20all={int(s['collective_H20_complete'])}",
            f"H50all={int(s['collective_H50_complete'])}",
        ]))


if __name__ == "__main__":
    main()
