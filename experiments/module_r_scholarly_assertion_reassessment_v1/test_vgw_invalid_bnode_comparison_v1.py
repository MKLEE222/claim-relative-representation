from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_vgw_fresh_confirmatory_v1 as runner


def require(cond, payload):
    if not cond:
        raise AssertionError(payload)


def base_payload():
    return {
        "engine": "X",
        "records_by_slug": {"provider": 1},
        "invalid_records": [{
            "slug": "provider",
            "object_uri": "_:local-a",
            "disposition": "NON_ADDRESSABLE_ARTWORK_OBJECT",
            "identifier_nodes": ["_:id-a", "https://stable.example/id/1"],
            "f_values": [],
        }],
        "post1970_role_exclusions": [],
        "cases": [{
            "f_number": "F1",
            "disposition": "SUBSTANTIVE_CANDIDATE",
            "baseline_object_uri": "https://stable.example/base/F1",
            "current_object_uri": "https://stable.example/current/F1",
            "current_provider_slug": "provider",
            "state": {
                "object_id": "F1",
                "assertions": {},
            },
            "event": {
                "evidence_id": "https://stable.example/event/F1",
            },
        }],
    }


def main():
    a = base_payload()
    b = copy.deepcopy(a)
    b["engine"] = "Y"
    b["invalid_records"][0]["object_uri"] = "_:other-local-label"
    b["invalid_records"][0]["identifier_nodes"][0] = "_:other-id-label"

    require(
        runner.normalized_extraction(a)
        == runner.normalized_extraction(b),
        {"a": runner.normalized_extraction(a), "b": runner.normalized_extraction(b)},
    )

    stable_uri_change = copy.deepcopy(b)
    stable_uri_change["invalid_records"][0]["identifier_nodes"][1] = (
        "https://stable.example/id/DIFFERENT"
    )
    require(
        runner.normalized_extraction(a)
        != runner.normalized_extraction(stable_uri_change),
        "stable invalid-record URI difference was incorrectly normalized",
    )

    case_change = copy.deepcopy(b)
    case_change["cases"][0]["event"]["evidence_id"] = (
        "https://stable.example/event/DIFFERENT"
    )
    require(
        runner.normalized_extraction(a)
        != runner.normalized_extraction(case_change),
        "eligible/admissible case evidence difference was incorrectly normalized",
    )

    disposition_change = copy.deepcopy(b)
    disposition_change["invalid_records"][0]["disposition"] = (
        "INVALID_F_NUMBER_CARDINALITY"
    )
    require(
        runner.normalized_extraction(a)
        != runner.normalized_extraction(disposition_change),
        "invalid-record disposition difference was incorrectly normalized",
    )

    print(json.dumps({
        "study": "VGW_INVALID_BNODE_COMPARISON_REGRESSION_V1",
        "blank_node_labels_normalize_equal": True,
        "stable_uri_difference_remains_visible": True,
        "case_evidence_difference_remains_visible": True,
        "disposition_difference_remains_visible": True,
        "overall": "PASS",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
