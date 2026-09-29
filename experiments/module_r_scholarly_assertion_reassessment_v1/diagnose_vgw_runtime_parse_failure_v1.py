from __future__ import annotations

import hashlib
import json
import urllib.request

URL = "https://data.spinque.com/ld/data/vangoghworldwide/de_la_faille_1970/data/export.nt"
EXPECTED_SHA = "88ae395103d86b5b40afb40465d7d093d88412f16841c936bfa22e68502548e3"
TARGET = 31932


def main():
    req = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "CRR-VGW-postfresh-parser-diagnostic/1.0",
            "Accept": "application/n-triples",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read()

    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA:
        raise RuntimeError("SOURCE_SHA_MISMATCH")

    lines = raw.decode("utf-8").splitlines()
    line = lines[TARGET - 1]

    fingerprint = {
        "line_number": TARGET,
        "line_length": len(line),
        "ends_with_dot": line.rstrip().endswith("."),
        "has_language_tag": '"@' in line,
        "language_tag_adjacent_terminal_dot": (
            '"@' in line
            and line.rstrip().endswith(".")
            and not line.rstrip().endswith(" .")
        ),
        "tail_repr": repr(line[-120:]),
        "full_line_repr": repr(line),
        "source_sha256": digest,
    }
    print(json.dumps(fingerprint, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
