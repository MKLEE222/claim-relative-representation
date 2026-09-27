from __future__ import annotations

import collections
import hashlib
import json
import math
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

URLS = {
    "V1": "https://www.gutenberg.org/cache/epub/10636/pg10636.txt",
    "V2": "https://www.gutenberg.org/cache/epub/12410/pg12410.txt",
}
EXPECTED = {
    "V1": "7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5",
    "V2": "c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c",
}

WINDOW = 180
STRIDE = 90
QUERY_K = 12

# Inherited from Generic Seed-Task Access Policy v1 / EP_KS_01 transfer implementation.
STOP = {
    "the","and","that","this","with","from","have","has","had","were","was","are","for","not","but",
    "his","her","their","there","which","into","than","then","they","them","you","your","its","who",
    "whom","what","when","where","how","all","any","some","more","most","such","only","been","being",
    "will","would","could","should","about","over","under","after","before","between","also","very",
    "upon","our","out","off","one","two","same","find","material","edition","bears","whether"
}

CASES = [
    {
        "id": "R3Q-PASH-STANCE",
        "seed_anchor": "speaking here from hearsay",
        "task": "Find later editorial treatment bearing on the source attribution and route reconstruction in the earlier Pashai note.",
        "groups": {
            "CORROBORATION": "Sir Henry Yule was undoubtedly right in assuming that Marco Polo had never personally visited",
            "ROUTE_CHALLENGE": "may very well have made his way over the Hindu",
        },
    },
    {
        "id": "R3Q-ARBR-COMMIT",
        "seed_anchor": "There can be no doubt that the tree described is",
        "task": "Find later editorial treatment bearing on the identification and editorial uptake of the Arbre Sec in the earlier note.",
        "groups": {
            "COMPETING_IDENTIFICATION": "Cypress of Zoroaster",
            "EDITORIAL_REPLY": "If General Houtum Schindler had seen the third edition",
        },
    },
    {
        "id": "R3Q-DES-EVIDENCE",
        "seed_anchor": "It is at the entrance of the great Desert",
        "task": "Find later editorial treatment bearing on the Great Desert folklore source interpretation and the distance or marches described in the earlier note.",
        "groups": {
            "FOLKLORE_SOURCE": "faithful reflex of old folklore beliefs he must have heard on the spot",
            "MEASUREMENT": "plane-table survey checked by cyclometer readings",
        },
    },
    {
        "id": "R3Q-URM-ERRATUM",
        "seed_anchor": "The Chinese Governor of Urumtsi found some years ago",
        "task": "Find later editorial correction bearing on the Governor of Urumtsi passage in the earlier note.",
        "groups": {
            "CORRECTION": "Governor of Urumtsi founded instead of found",
        },
    },
    {
        "id": "R3Q-TUN-CONTROVERSY",
        "seed_anchor": "No city in particular is indicated as visited by the traveller",
        "task": "Find later editorial treatment bearing on the route through Tun-o-Kain in the earlier note and determine whether later discussion settles or preserves competing positions.",
        "groups": {
            "SYKES_REVISION": "Major Sykes had adopted Sir Henry Yule's theory",
            "YULE_SUPPORT": "Support to Yule's theory has been brought by Sven Hedin",
            "UNRESOLVED_COMPETITION": "cannot decide with full certainty whether Marco Polo travelled",
        },
    },
]


@dataclass(frozen=True)
class W:
    doc: str
    start: int
    words: tuple[str, ...]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "claim-relative-representation/1.0 research reproducibility"},
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def normalize_text(s: str) -> str:
    return (
        s.replace("’", "'")
         .replace("‘", "'")
         .replace("–", "-")
         .replace("—", "-")
    )


def toks(s: str) -> list[str]:
    s = normalize_text(s).lower()
    base = re.findall(r"[a-z][a-z'-]{2,}", s)
    out: list[str] = []
    for x in base:
        out.append(x)
        if "-" in x:
            out.extend(p for p in x.split("-") if len(p) >= 3)
    return out


def make_windows(doc: str, text: str) -> list[W]:
    ts = toks(text)
    out: list[W] = []
    for s in range(0, max(1, len(ts) - WINDOW + 1), STRIDE):
        chunk = ts[s:s + WINDOW]
        if len(chunk) >= WINDOW // 2:
            out.append(W(doc=doc, start=s, words=tuple(chunk)))
    return out


def locate_addenda(text: str) -> int:
    m = re.search(
        r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",
        text,
        flags=re.I,
    )
    if not m:
        raise RuntimeError("native Addenda boundary not found")
    return m.start()


def seed_span(text: str, anchor: str) -> str:
    # Format-insensitive locator: preserve anchor word order while allowing
    # Gutenberg emphasis markers, punctuation, and line wrapping between words.
    norm = normalize_text(text)
    words = re.findall(r"[A-Za-z]+", normalize_text(anchor))
    if not words:
        raise RuntimeError(f"empty seed anchor: {anchor}")
    pat = r"\\b" + r"[^A-Za-z0-9]+".join(re.escape(w) for w in words) + r"\\b"
    m = re.search(pat, norm, flags=re.I)
    if not m:
        raise RuntimeError(f"seed anchor not found: {anchor}")
    p = m.start()

    # Native paragraph first; deterministic bounded fallback if Gutenberg wrapping lacks blank lines.
    left = text.rfind("\n\n", max(0, p - 2200), p)
    right = text.find("\n\n", p, min(len(text), p + 2200))
    if left >= 0 and right >= 0 and 160 <= right - left <= 2400:
        return text[left + 2:right]

    return text[max(0, p - 900):min(len(text), p + 900)]


def find_anchor_windows(ws: list[W], anchor: str) -> list[W]:
    need = set(toks(anchor))
    if not need:
        raise RuntimeError(f"empty anchor: {anchor}")
    hits = [w for w in ws if need <= set(w.words)]
    if not hits:
        raise RuntimeError(f"evaluation anchor not found in any window: {anchor}")
    return hits


def find_seed_window(ws: list[W], anchor: str) -> W:
    hits = find_anchor_windows(ws, anchor)
    return hits[0]


def idf(ws: list[W]) -> dict[str, float]:
    n = len(ws)
    df = collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t] += 1
    return {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}


def build_query(seed: str, task: str, base_ws: list[W]) -> list[tuple[str, float]]:
    counts = collections.Counter(
        t for t in toks(seed + " " + task)
        if t not in STOP and len(t) >= 4
    )
    weights = idf(base_ws)
    scored = sorted(
        ((t, c * weights.get(t, 1.0)) for t, c in counts.items()),
        key=lambda z: (-z[1], z[0]),
    )
    return scored[:QUERY_K]


def score(w: W, q: list[tuple[str, float]]) -> float:
    c = collections.Counter(w.words)
    return sum(weight * min(c.get(term, 0), 3) for term, weight in q)


def ranked_candidates(ws: list[W], q: list[tuple[str, float]], seed_w: W | None) -> list[tuple[float, W]]:
    cands: list[tuple[float, W]] = []
    for w in ws:
        if seed_w is not None and w.doc == seed_w.doc and abs(w.start - seed_w.start) < WINDOW:
            continue
        cands.append((score(w, q), w))
    cands.sort(key=lambda z: (-z[0], z[1].doc, z[1].start))
    return cands


def group_rank(ranked: list[tuple[float, W]], group_windows: list[W]) -> tuple[int | None, float | None]:
    keys = {(w.doc, w.start) for w in group_windows}
    for i, (s, w) in enumerate(ranked, 1):
        if (w.doc, w.start) in keys:
            return i, s
    return None, None


def all_groups_in_one_window(ws: list[W], group_anchors: dict[str, str]) -> bool:
    needs = [set(toks(a)) for a in group_anchors.values()]
    for w in ws:
        s = set(w.words)
        if all(n <= s for n in needs):
            return True
    return False


def collective_complete(
    ranked: list[tuple[float, W]],
    group_windows: dict[str, list[W]],
    budget: int,
) -> bool:
    top = {(w.doc, w.start) for _, w in ranked[:budget]}
    for hits in group_windows.values():
        if not any((w.doc, w.start) in top for w in hits):
            return False
    return True


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    raw = {k: fetch(v) for k, v in URLS.items()}
    got = {k: sha(v) for k, v in raw.items()}
    if got != EXPECTED:
        raise RuntimeError(f"source drift: {got}")

    text = {k: raw[k].decode("utf-8", errors="replace") for k in raw}
    boundary = locate_addenda(text["V2"])
    v2_base = text["V2"][:boundary]
    v2_later = text["V2"][boundary:]

    v1_ws = make_windows("V1", text["V1"])
    v2_base_ws = make_windows("V2_BASE", v2_base)
    v2_full_ws = make_windows("V2", text["V2"])
    later_ws = make_windows("V2_LATER", v2_later)

    # Same generic policy, applied to the declared two-volume collection.
    base_ws = v1_ws + v2_base_ws
    full_ws = v1_ws + v2_full_ws

    result = {
        "study": "R3_GENERIC_ACCESS_TRANSFER_V1",
        "protocol_status": "PRE_OUTCOME_FROZEN",
        "source_sha256": got,
        "parameters": {
            "window": WINDOW,
            "stride": STRIDE,
            "query_k": QUERY_K,
            "ranking": "weighted lexical overlap",
            "idf_scope": "V1 + V2 pre-Addenda",
            "full_scope": "V1 + V2 complete",
            "later_scope": "V2 native Addenda",
        },
        "addenda_char_offset_v2": boundary,
        "cases": [],
    }

    for case in CASES:
        seed = seed_span(text["V1"], case["seed_anchor"])
        seed_w = find_seed_window(v1_ws, case["seed_anchor"])
        q = build_query(seed, case["task"], base_ws)
        qterms = {t for t, _ in q}

        seed_terms = set(toks(seed))
        eval_terms = set()
        for a in case["groups"].values():
            eval_terms.update(toks(a))
        leaked = sorted(t for t in qterms if t in eval_terms and t not in seed_terms)
        if leaked:
            raise RuntimeError(f"{case['id']} INVALID_LEAKAGE: {leaked}")

        full_ranked = ranked_candidates(full_ws, q, seed_w)
        later_ranked = ranked_candidates(later_ws, q, None)

        # Evaluation anchors are resolved independently inside each scope.
        full_group_windows = {
            gid: find_anchor_windows(full_ws, anchor)
            for gid, anchor in case["groups"].items()
        }
        later_group_windows = {
            gid: find_anchor_windows(later_ws, anchor)
            for gid, anchor in case["groups"].items()
        }

        c = {
            "inquiry_id": case["id"],
            "task": case["task"],
            "seed_anchor": case["seed_anchor"],
            "seed_sha256": hashlib.sha256(seed.encode("utf-8")).hexdigest(),
            "query_terms": [t for t, _ in q],
            "leakage_overlap": [],
            "scopes": {},
        }

        for name, ranked, gws, ws in [
            ("GSA_FULL_OBJECT", full_ranked, full_group_windows, full_ws),
            ("GSA_LATER_LAYER", later_ranked, later_group_windows, later_ws),
        ]:
            groups = {}
            for gid, hits in gws.items():
                rank, sc = group_rank(ranked, hits)
                groups[gid] = {
                    "target_window_count": len(hits),
                    "rank": rank,
                    "score": sc,
                    "rr": 0.0 if rank is None else 1.0 / rank,
                    "H10": int(rank is not None and rank <= 10),
                    "H20": int(rank is not None and rank <= 20),
                    "H50": int(rank is not None and rank <= 50),
                }

            c["scopes"][name] = {
                "candidate_count": len(ranked),
                "groups": groups,
                "single_window_complete": all_groups_in_one_window(ws, case["groups"]),
                "collective_H10_complete": collective_complete(ranked, gws, 10),
                "collective_H20_complete": collective_complete(ranked, gws, 20),
                "collective_H50_complete": collective_complete(ranked, gws, 50),
            }

        result["cases"].append(c)

    out = Path("experiments/deepening_v1/results")
    out.mkdir(parents=True, exist_ok=True)
    target = out / "r3_generic_access_transfer_v1.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("R3_GENERIC_ACCESS_TRANSFER_V1")
    print("source_sha256_V1=" + got["V1"])
    print("source_sha256_V2=" + got["V2"])
    for c in result["cases"]:
        print("CASE," + c["inquiry_id"] + ",query=" + "|".join(c["query_terms"]))
        for scope_name, s in c["scopes"].items():
            group_bits = []
            for gid, g in s["groups"].items():
                group_bits.append(f"{gid}:r{g['rank']}")
            print(",".join([
                "RESULT",
                c["inquiry_id"],
                scope_name,
                f"candidates={s['candidate_count']}",
                "groups=" + ";".join(group_bits),
                f"single={int(s['single_window_complete'])}",
                f"H10all={int(s['collective_H10_complete'])}",
                f"H20all={int(s['collective_H20_complete'])}",
                f"H50all={int(s['collective_H50_complete'])}",
            ]))


if __name__ == "__main__":
    main()
