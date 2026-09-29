from __future__ import annotations

import json
from pathlib import Path

import run_vgw_fresh_confirmatory_v1 as base

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "vgw_corrected_reproduction_v1"
CACHE = HERE / "results" / "vgw_corrected_source_cache_v1"

EXPECTED_SOURCE_HASHES = {
    "de_la_faille_1970": "88ae395103d86b5b40afb40465d7d093d88412f16841c936bfa22e68502548e3",
    "works_after_1970": "eed8cd78f3ec811b5302555abb5cad14cc86679ebc23e9132f46943803dac810",
    "van_gogh_museum": "8985296d791366910ae01a954d0ade65f196f461cd78328ce21602e2ed279e43",
    "krollermuller_museum": "78c48e3f7cb1699548e3d7f2e604ce363a663deca1b3747343fb22c013c788b2",
    "rkd_collections": "85ec7afd25c3cd4cf99924d65a7b9954c50254715467231a0a1f56fe1e5d7f03",
}


def corrected_marker(anchor_rows):
    marker = {
        "study": "MODULE_R_VGW_CORRECTED_REPRODUCTION_V1",
        "event": "CORRECTED_REPRO_OPEN_EVENT",
        "scientific_status": "POSTFRESH_CORRECTED_REPRODUCTION_ONLY",
        "authoritative_fresh_run": 36553853190,
        "original_fresh_disposition": "INVALID",
        "repairs": [
            "NTRIPLES_BLANK_NODE_TERMINATOR_LEXER",
            "NTRIPLES_LANGTAG_TERMINATOR_LEXER",
            "INVALID_RECORD_BLANK_NODE_COMPARISON_NORMALIZATION"
        ],
        "source_urls": {
            slug: anchor_rows[slug]["content_url"]
            for slug in base.EXPECTED_SLUGS
        },
        "git_context": base.git_context(),
    }
    base.write_json(RESULTS / "CORRECTED_REPRO_OPEN_EVENT_v1.json", marker)
    print(json.dumps(marker, ensure_ascii=False))


def main():
    base.RESULTS = RESULTS
    base.CACHE = CACHE
    base.write_data_open_marker = corrected_marker
    base.main()

    manifest_path = RESULTS / "distribution_manifest_v1.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    observed = {
        x["slug"]: x["sha256"] for x in manifest["distributions"]
    }
    exact = observed == EXPECTED_SOURCE_HASHES
    check = {
        "study": "VGW_CORRECTED_REPRO_SOURCE_IDENTITY_V1",
        "authoritative_fresh_run": 36553853190,
        "same_source_bytes_as_first_open": exact,
        "expected": EXPECTED_SOURCE_HASHES,
        "observed": observed,
    }
    base.write_json(RESULTS / "source_identity_check_v1.json", check)
    print(json.dumps(check, ensure_ascii=False, indent=2))
    if not exact:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
