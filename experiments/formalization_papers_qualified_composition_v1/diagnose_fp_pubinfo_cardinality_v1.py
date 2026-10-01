from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import Dataset

NP_HAS_PUBINFO = "http://www.nanopub.org/nschema#hasPublicationInfo"
DCT_CREATOR = "http://purl.org/dc/terms/creator"
DCT_CREATED = "http://purl.org/dc/terms/created"


def v(x):
    return str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    root = Path(args.source_root)
    files = sorted(
        p for p in (root / "nanopubs").rglob("*") if p.is_file()
    )

    by_graph = defaultdict(set)
    all_triples = set()
    for path in files:
        ds = Dataset()
        ds.parse(
            data=path.read_text(encoding="utf-8"),
            format="trig",
        )
        for s, p, o, g in ds.quads((None, None, None, None)):
            gn = v(g.identifier if hasattr(g, "identifier") else g)
            row = (v(s), v(p), v(o))
            by_graph[gn].add(row)
            all_triples.add(row)

    pubinfo = {}
    for s, p, o in all_triples:
        if p == NP_HAS_PUBINFO:
            pubinfo[s] = o

    rows = []
    creator_hist = Counter()
    created_hist = Counter()
    for np, pg in sorted(pubinfo.items()):
        triples = by_graph.get(pg, set())
        creators = sorted({
            o for s, p, o in triples
            if s == np and p == DCT_CREATOR
        })
        created = sorted({
            o for s, p, o in triples
            if s == np and p == DCT_CREATED
        })
        creator_hist[len(creators)] += 1
        created_hist[len(created)] += 1
        if len(creators) != 1 or len(created) != 1:
            rows.append({
                "nanopub": np,
                "creator_count": len(creators),
                "creators": creators,
                "created_count": len(created),
                "created": created,
            })

    result = {
        "study": "FORMALIZATION_PAPERS_POSTFRESH_PUBINFO_CARDINALITY_AUDIT_V1",
        "file_count": len(files),
        "nanopub_count": len(pubinfo),
        "creator_cardinality_histogram": dict(
            sorted(creator_hist.items())
        ),
        "created_cardinality_histogram": dict(
            sorted(created_hist.items())
        ),
        "non_singleton_pubinfo_count": len(rows),
        "non_singleton_rows": rows,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "study": result["study"],
        "file_count": result["file_count"],
        "nanopub_count": result["nanopub_count"],
        "creator_cardinality_histogram": (
            result["creator_cardinality_histogram"]
        ),
        "created_cardinality_histogram": (
            result["created_cardinality_histogram"]
        ),
        "non_singleton_pubinfo_count": len(rows),
        "non_singleton_first20": rows[:20],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
