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


def parse(line: str):
    triples = vgw_runtime.parse_nt((line + "\n").encode("utf-8"))
    require(len(triples) == 1, triples)
    return triples[0]


def main():
    cases = {
        "nl_no_space": (
            '<https://example.org/s> <https://example.org/p> "Milano"@nl.',
            "Milano",
        ),
        "en_no_space": (
            '<https://example.org/s> <https://example.org/p> "Vienna (city)"@en.',
            "Vienna (city)",
        ),
        "nl_space_before_dot": (
            '<https://example.org/s> <https://example.org/p> "Amsterdam"@nl .',
            "Amsterdam",
        ),
        "regional_langtag": (
            '<https://example.org/s> <https://example.org/p> "colour"@en-GB.',
            "colour",
        ),
    }

    observed = {}
    for name, (line, literal) in cases.items():
        triple = parse(line)
        require(triple[2] == ("L", literal), {
            "case": name,
            "triple": triple,
        })
        observed[name] = "PASS"

    print(json.dumps({
        "study": "VGW_RUNTIME_NTRIPLES_LANGTAG_TERMINATOR_REGRESSION_V1",
        "cases": observed,
        "overall": "PASS",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
