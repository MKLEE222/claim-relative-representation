from __future__ import annotations

from pathlib import Path

import audit_vgw_fresh_documentary_v1 as base

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "vgw_corrected_reproduction_v1"
CACHE = HERE / "results" / "vgw_corrected_source_cache_v1"


def main():
    base.RESULTS = RESULTS
    base.CACHE = CACHE
    base.AUTH = RESULTS / "authoritative_results_v1.json"
    base.DIST = RESULTS / "distribution_manifest_v1.json"
    base.main()


if __name__ == "__main__":
    main()
