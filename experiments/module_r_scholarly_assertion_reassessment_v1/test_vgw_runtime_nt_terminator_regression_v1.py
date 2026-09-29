from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import vgw_runtime


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    raw = (
        b"<https://example.org/s> <https://example.org/p> "
        b"_:support_00e26e7d-2e2a-4290-b87b-efe316b63ae6-d-87bc1c.\n"
    )
    triples = vgw_runtime.parse_nt(raw)
    require(len(triples) == 1, triples)
    s, p, o = triples[0]
    require(s == ("I", "https://example.org/s"), s)
    require(p == "https://example.org/p", p)
    require(
        o == (
            "B",
            "_:support_00e26e7d-2e2a-4290-b87b-efe316b63ae6-d-87bc1c",
        ),
        o,
    )

    raw_internal_dot = (
        b"<https://example.org/s> <https://example.org/p> "
        b"_:support.segment-1 .\n"
    )
    triples2 = vgw_runtime.parse_nt(raw_internal_dot)
    require(triples2[0][2] == ("B", "_:support.segment-1"), triples2)

    print(json.dumps({
        "study": "VGW_RUNTIME_NTRIPLES_TERMINATOR_REGRESSION_V1",
        "terminal_dot_without_whitespace": "PASS",
        "internal_blank_node_dot_preserved": "PASS",
        "overall": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
