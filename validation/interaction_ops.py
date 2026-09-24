from __future__ import annotations
from copy import deepcopy

DOC_REL_FIELDS = {
    "TD_ATTRIBUTION": "attribution",
    "TD_TEMPORAL": "temporal_order",
    "TR_EVIDENCE": "evidence_relation",
    "TR_BINDING": "claim_binding",
}

ACCESS_LEVELS = {"object", "local", "span"}

def wrap(record: dict) -> dict:
    return {
        "record": deepcopy(record),
        "context_scope": "object",
        "external_access": False,
    }

def apply(state: dict, transformation_id: str) -> dict:
    out = deepcopy(state)

    if transformation_id in DOC_REL_FIELDS:
        field = DOC_REL_FIELDS[transformation_id]
        out["record"][field] = None
        return out

    if transformation_id == "TA_SPAN":
        out["context_scope"] = "span"
        return out

    if transformation_id == "TA_LOCAL":
        out["context_scope"] = "local"
        return out

    if transformation_id == "TA_OBJECT":
        out["context_scope"] = "object"
        return out

    if transformation_id == "TA_EXTERNAL":
        out["external_access"] = True
        return out

    if transformation_id == "TD_NORMALIZE":
        raise RuntimeError("TD_NORMALIZE is held out pending semantic-preservation audit")

    raise KeyError(transformation_id)

def changed_paths(before: dict, after: dict) -> set[str]:
    changed=set()
    for k in set(before["record"]) | set(after["record"]):
        if before["record"].get(k) != after["record"].get(k):
            changed.add(f"record.{k}")
    if before.get("context_scope") != after.get("context_scope"):
        changed.add("context_scope")
    if before.get("external_access") != after.get("external_access"):
        changed.add("external_access")
    return changed
