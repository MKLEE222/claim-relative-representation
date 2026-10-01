from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import vgw_runtime

ANCHORS = HERE / "VGW_DISTRIBUTION_METADATA_ANCHORS_v1.json"

EXPECTED_SHA = {
    "de_la_faille_1970": "88ae395103d86b5b40afb40465d7d093d88412f16841c936bfa22e68502548e3",
    "works_after_1970": "eed8cd78f3ec811b5302555abb5cad14cc86679ebc23e9132f46943803dac810",
    "van_gogh_museum": "8985296d791366910ae01a954d0ade65f196f461cd78328ce21602e2ed279e43",
    "krollermuller_museum": "78c48e3f7cb1699548e3d7f2e604ce363a663deca1b3747343fb22c013c788b2",
    "rkd_collections": "85ec7afd25c3cd4cf99924d65a7b9954c50254715467231a0a1f56fe1e5d7f03",
}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def classify(line: str, exc: Exception):
    s = line.rstrip()
    tail = s[-80:]
    return {
        "error_type": type(exc).__name__,
        "error": str(exc),
        "ends_dot": s.endswith("."),
        "ends_space_dot": s.endswith(" ."),
        "object_blank_node": " _:" in s,
        "literal_lang": '"@' in s,
        "literal_datatype": '"^^<' in s,
        "contains_comment": " #" in s,
        "tail_repr": repr(tail),
    }


def main():
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    rows = {x["slug"]: x for x in anchors["datasets"]}

    report = {}
    total_failures = 0

    for slug, expected_sha in EXPECTED_SHA.items():
        req = urllib.request.Request(
            rows[slug]["content_url"],
            headers={
                "User-Agent": "CRR-VGW-postfresh-grammar-audit/1.0",
                "Accept": "application/n-triples",
                "Accept-Encoding": "identity",
            },
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw = resp.read()

        if sha256(raw) != expected_sha:
            raise RuntimeError(f"SOURCE_SHA_MISMATCH::{slug}")

        failures = []
        classes = Counter()
        lines = raw.decode("utf-8").splitlines()

        for n, line in enumerate(lines, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                vgw_runtime.parse_nt((line + "\n").encode("utf-8"))
            except Exception as exc:
                fp = classify(line, exc)
                key = (
                    fp["error"],
                    fp["object_blank_node"],
                    fp["literal_lang"],
                    fp["literal_datatype"],
                    fp["ends_space_dot"],
                )
                classes[str(key)] += 1
                if len(failures) < 30:
                    failures.append({
                        "line_number": n,
                        **fp,
                        "full_line_repr": repr(line),
                    })

        report[slug] = {
            "line_count": len(lines),
            "failure_count": sum(classes.values()),
            "failure_classes": dict(classes),
            "sample_failures": failures,
            "source_sha256": expected_sha,
        }
        total_failures += sum(classes.values())

    out = {
        "study": "VGW_POSTFRESH_NTRIPLES_GRAMMAR_COVERAGE_V1",
        "scientific_status": "POSTFRESH_PARSER_DIAGNOSTIC_ONLY",
        "total_failures": total_failures,
        "datasets": report,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
