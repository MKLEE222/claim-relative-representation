from __future__ import annotations

from copy import deepcopy

COORDINATE_FIELD = {
    "attribution": "attribution",
    "temporal_order": "temporal_order",
    "evidence_relation": "evidence_relation",
    "claim_binding": "claim_binding",
    "distinction_collapse": "distinction",
}

def intervene(record: dict, coordinate: str) -> dict:
    if coordinate not in COORDINATE_FIELD:
        raise KeyError(coordinate)
    out = deepcopy(record)
    field = COORDINATE_FIELD[coordinate]
    if coordinate == "distinction_collapse":
        out[field] = "generic_annotation"
    else:
        out[field] = None
    return out

def restore(intervened: dict, baseline: dict, coordinate: str) -> dict:
    if coordinate not in COORDINATE_FIELD:
        raise KeyError(coordinate)
    out = deepcopy(intervened)
    field = COORDINATE_FIELD[coordinate]
    out[field] = baseline[field]
    return out

def changed_fields(before: dict, after: dict) -> set[str]:
    keys = set(before) | set(after)
    return {k for k in keys if before.get(k) != after.get(k)}
