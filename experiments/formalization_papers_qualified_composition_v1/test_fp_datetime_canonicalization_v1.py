from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fp_oracle
import fp_runtime


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def main():
    pairs = [
        (
            "2021-10-25T16:22:30.526000+02:00",
            "2021-10-25T16:22:30.526+02:00",
            "2021-10-25T16:22:30.526000+02:00",
        ),
        (
            "2021-10-07T02:12:24.840000+03:00",
            "2021-10-07T02:12:24.84+03:00",
            "2021-10-07T02:12:24.840000+03:00",
        ),
        (
            "2021-01-01T00:00:00+00:00",
            "2021-01-01T00:00:00Z",
            "2021-01-01T00:00:00.000000+00:00",
        ),
    ]

    rows = []
    for a, b, expected in pairs:
        oa = fp_oracle._canon_time(a)
        ob = fp_oracle._canon_time(b)
        ra = fp_runtime._canon_time(a)
        rb = fp_runtime._canon_time(b)
        require(oa == ob == ra == rb == expected, {
            "a": a, "b": b, "oracle_a": oa, "oracle_b": ob,
            "runtime_a": ra, "runtime_b": rb, "expected": expected,
        })
        rows.append({
            "a": a,
            "b": b,
            "canonical": expected,
            "equal": True,
        })

    different_a = "2021-10-25T16:22:30.526+02:00"
    different_b = "2021-10-25T16:22:31.526+02:00"
    require(
        fp_oracle._canon_time(different_a)
        != fp_oracle._canon_time(different_b),
        "oracle collapsed different times",
    )
    require(
        fp_runtime._canon_time(different_a)
        != fp_runtime._canon_time(different_b),
        "runtime collapsed different times",
    )

    offset_value = "2021-07-25T20:31:26.159-04:00"
    expected_offset = "2021-07-25T20:31:26.159000-04:00"
    require(
        fp_oracle._canon_time(offset_value) == expected_offset,
        fp_oracle._canon_time(offset_value),
    )
    require(
        fp_runtime._canon_time(offset_value) == expected_offset,
        fp_runtime._canon_time(offset_value),
    )

    malformed = "not-a-date"
    require(fp_oracle._canon_time(malformed) == malformed, malformed)
    require(fp_runtime._canon_time(malformed) == malformed, malformed)

    result = {
        "study": "FORMALIZATION_PAPERS_DATETIME_CANONICALIZATION_REGRESSION_V1",
        "equivalent_precision_cases": rows,
        "different_time_remains_different": True,
        "nonzero_offset_preserved": True,
        "malformed_value_not_inferred": True,
        "overall": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
