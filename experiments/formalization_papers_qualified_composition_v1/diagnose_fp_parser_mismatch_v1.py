from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_oracle
import fp_runtime

KEYS = (
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


def is_bnode_string(value):
    if not isinstance(value, str):
        return False
    # RDFLib commonly renders BNode identifiers without "_:", whereas
    # pyoxigraph may expose the source/local blank-node id. This function
    # does not normalize; it only tags common lexical forms for diagnostics.
    return value.startswith("_:")


def tuple_strings(row):
    out = []
    if isinstance(row, (list, tuple)):
        for x in row:
            if isinstance(x, (list, tuple)):
                out.extend(tuple_strings(x))
            else:
                out.append(str(x))
    else:
        out.append(str(row))
    return out


def signature(row):
    values = tuple_strings(row)
    return {
        "values": values,
        "has_explicit_bnode_lexeme": any(
            is_bnode_string(x) for x in values
        ),
        "http_uri_count": sum(
            x.startswith(("http://", "https://")) for x in values
        ),
    }


def compare_component(o_rows, r_rows):
    o_set = {json.dumps(x, ensure_ascii=False, sort_keys=True) for x in o_rows}
    r_set = {json.dumps(x, ensure_ascii=False, sort_keys=True) for x in r_rows}
    only_o_raw = sorted(o_set - r_set)
    only_r_raw = sorted(r_set - o_set)

    only_o = [json.loads(x) for x in only_o_raw]
    only_r = [json.loads(x) for x in only_r_raw]

    return {
        "oracle_count": len(o_rows),
        "runtime_count": len(r_rows),
        "exact": o_set == r_set,
        "only_oracle_count": len(only_o),
        "only_runtime_count": len(only_r),
        "only_oracle_first20": only_o[:20],
        "only_runtime_first20": only_r[:20],
        "only_oracle_signatures_first20": [
            signature(x) for x in only_o[:20]
        ],
        "only_runtime_signatures_first20": [
            signature(x) for x in only_r[:20]
        ],
    }


def string_shape(value):
    s = str(value)
    if s.startswith(("http://", "https://")):
        return "URI"
    if s.startswith("_:"):
        return "EXPLICIT_BNODE"
    if "T" in s and (
        s.endswith("Z")
        or "+" in s[-6:]
        or "-" in s[-6:]
    ):
        return "DATETIME_LIKE"
    return "OTHER"


def mismatch_pair_hints(component):
    o = component["only_oracle_first20"]
    r = component["only_runtime_first20"]
    hints = []
    for a, b in zip(o, r):
        av = tuple_strings(a)
        bv = tuple_strings(b)
        if len(av) != len(bv):
            hints.append({
                "hint": "ARITY_DIFFERENCE",
                "oracle": av,
                "runtime": bv,
            })
            continue
        diffs = []
        for i, (x, y) in enumerate(zip(av, bv)):
            if x != y:
                diffs.append({
                    "position": i,
                    "oracle": x,
                    "runtime": y,
                    "oracle_shape": string_shape(x),
                    "runtime_shape": string_shape(y),
                })
        hints.append({
            "hint": (
                "POSITIONAL_DIFFERENCE"
                if diffs
                else "NO_POSITIONAL_DIFFERENCE"
            ),
            "diffs": diffs,
        })
    return hints


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    source_root = Path(args.source_root)
    files = sorted(
        p for p in (source_root / "nanopubs").rglob("*") if p.is_file()
    )

    file_rows = []
    aggregate_mismatch_keys = Counter()

    for path in files:
        raw = path.read_bytes()
        rel = path.relative_to(source_root).as_posix()

        try:
            oracle = fp_oracle.parse_trig(raw)
            oracle_error = None
        except Exception as exc:
            oracle = None
            oracle_error = f"{type(exc).__name__}: {exc}"

        try:
            runtime = fp_runtime.parse_trig(raw)
            runtime_error = None
        except Exception as exc:
            runtime = None
            runtime_error = f"{type(exc).__name__}: {exc}"

        row = {
            "path": rel,
            "oracle_error": oracle_error,
            "runtime_error": runtime_error,
            "components": {},
        }

        if oracle is not None and runtime is not None:
            for key in KEYS:
                cmp = compare_component(
                    oracle.get(key, []), runtime.get(key, [])
                )
                cmp["mismatch_hints_first20"] = mismatch_pair_hints(cmp)
                row["components"][key] = cmp
                if not cmp["exact"]:
                    aggregate_mismatch_keys[key] += 1
            row["exact"] = all(
                x["exact"] for x in row["components"].values()
            )
        else:
            row["exact"] = False

        file_rows.append(row)

    result = {
        "study": "FORMALIZATION_PAPERS_POSTFRESH_PARSER_DIFF_DIAGNOSTIC_V1",
        "data_status": "POST_FRESH_EXPOSED_DIAGNOSTIC",
        "file_count": len(files),
        "exact_file_count": sum(x["exact"] for x in file_rows),
        "mismatch_component_file_counts": dict(
            sorted(aggregate_mismatch_keys.items())
        ),
        "files": file_rows,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "study": result["study"],
        "file_count": result["file_count"],
        "exact_file_count": result["exact_file_count"],
        "mismatch_component_file_counts": (
            result["mismatch_component_file_counts"]
        ),
        "compact": [
            {
                "path": x["path"],
                "mismatch_keys": [
                    k for k, v in x["components"].items()
                    if not v["exact"]
                ],
            }
            for x in file_rows
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
