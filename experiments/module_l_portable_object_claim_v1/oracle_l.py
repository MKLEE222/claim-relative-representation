from __future__ import annotations

import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
I_DIR = HERE.parent / "module_i_dahn_document_boundary_holdout_v1"
if str(I_DIR) not in sys.path:
    sys.path.insert(0, str(I_DIR))

import oracle_v2 as base

ALLOWED_ACTIVE_APPLICABILITY = {
    "FILE_LEVEL_UNIQUE_OBJECT",
    "INSIDE_SELECTED_OBJECT_BOUNDARY",
}


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _boundary_signature(el) -> str:
    """Independent structural signature for the selected ElementTree boundary."""
    def emit(node):
        attrs = sorted((_local(k), v) for k, v in node.attrib.items())
        parts = [["tag", _local(node.tag)], ["attrs", attrs]]
        text = _norm(node.text or "")
        if text:
            parts.append(["text", text])
        for child in list(node):
            parts.append(["child", emit(child)])
            tail = _norm(child.tail or "")
            if tail:
                parts.append(["tail", tail])
        return parts
    return _sha(
        json.dumps(emit(el), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def _norm(s: str) -> str:
    return " ".join((s or "").split())


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _freeze_source_context(source_context: dict) -> dict:
    required = ("source_repository", "source_version", "population_scope")
    out = {k: str(source_context.get(k) or "").strip() for k in required}
    if not all(out.values()):
        raise ValueError(f"incomplete source context: {out}")
    return out


def _parents(root):
    out = {}
    for p in root.iter():
        for c in list(p):
            out[c] = p
    return out


def _ancestors(el, pmap):
    out = []
    cur = pmap.get(el)
    while cur is not None:
        out.append(cur)
        cur = pmap.get(cur)
    return list(reversed(out))


def _inside_annex(el, pmap, stop=None) -> bool:
    cur = pmap.get(el)
    while cur is not None and cur is not stop:
        if _local(cur.tag) == "div" and cur.attrib.get("type") == "annex":
            return True
        cur = pmap.get(cur)
    return False


def _object_selection(root, pmap):
    bodies = [x for x in root.iter() if _local(x.tag) == "body"]
    if not bodies:
        return {
            "status": "NO_PRIMARY_DOCUMENT_OBJECT",
            "candidates": [],
            "boundary_kind": None,
            "reason": "NO_BODY",
        }

    body = bodies[0]

    explicit = []
    for x in body.iter():
        if x is body or _local(x.tag) != "div" or x.attrib.get("type") != "letter":
            continue
        if not _inside_annex(x, pmap, stop=body):
            explicit.append(x)

    if len(explicit) == 1:
        return {
            "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
            "candidates": explicit,
            "boundary_kind": "EXPLICIT_LETTER_DIV",
            "reason": None,
        }
    if len(explicit) > 1:
        return {
            "status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
            "candidates": explicit,
            "boundary_kind": None,
            "reason": "MULTIPLE_EXPLICIT_LETTERS",
        }

    trans = [
        x for x in body.iter()
        if x is not body and _local(x.tag) == "div" and x.attrib.get("type") == "transcription"
    ]
    if len(trans) > 1:
        return {
            "status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
            "candidates": trans,
            "boundary_kind": None,
            "reason": "MULTIPLE_TRANSCRIPTIONS_WITHOUT_EXPLICIT_LETTER",
        }

    corresp_desc = [x for x in root.iter() if _local(x.tag) == "correspDesc"]
    sent_actions = [
        x for x in root.iter()
        if _local(x.tag) == "correspAction" and (x.attrib.get("type") or "").lower() == "sent"
    ]

    if len(trans) == 1:
        candidate = trans[0]
        substantive = bool(_norm(" ".join(candidate.itertext())))
        if len(corresp_desc) == 1 and sent_actions and substantive:
            return {
                "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
                "candidates": [candidate],
                "boundary_kind": "TRANSCRIPTION_AS_LETTER",
                "reason": None,
            }
        return {
            "status": "NO_PRIMARY_DOCUMENT_OBJECT",
            "candidates": [],
            "boundary_kind": None,
            "reason": "TRANSCRIPTION_ROUTE_B_REQUIREMENTS_FAILED",
        }

    direct_divs = [
        x for x in list(body)
        if _local(x.tag) == "div"
    ]
    if len(direct_divs) == 1:
        candidate = direct_divs[0]
        markers = {
            _local(x.tag)
            for x in candidate.iter()
            if _local(x.tag) in {"opener", "closer", "salute", "signed", "dateline"}
        }
        substantive = bool(_norm(" ".join(candidate.itertext())))
        if (
            candidate.attrib.get("type") is None
            and len(corresp_desc) == 1
            and sent_actions
            and markers
            and substantive
        ):
            return {
                "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
                "candidates": [candidate],
                "boundary_kind": "UNTYPED_BODY_LETTER",
                "reason": None,
            }

    return {
        "status": "NO_PRIMARY_DOCUMENT_OBJECT",
        "candidates": [],
        "boundary_kind": None,
        "reason": "NO_FROZEN_A_B_C_OBJECT",
    }


def _object_contract(path: str, raw: bytes, source_context: dict):
    root = ET.fromstring(raw)
    pmap = _parents(root)
    sel = _object_selection(root, pmap)
    candidates = sel["candidates"]

    if sel["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        return root, pmap, None, {
            "status": sel["status"],
            "object_id": None,
            "candidate_count": len(candidates),
            "boundary_signature": None,
            "boundary_kind": sel["boundary_kind"],
            "reason": sel.get("reason"),
            "source_repository": source_context["source_repository"],
            "source_version": source_context["source_version"],
        }

    candidate = candidates[0]
    sig = _boundary_signature(candidate)
    payload = {
        "source_repository": source_context["source_repository"],
        "source_version": source_context["source_version"],
        "population_scope": source_context["population_scope"],
        "source_file": path,
        "boundary_kind": sel["boundary_kind"],
        "primary_boundary_signature": sig,
    }
    oid = _sha(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return root, pmap, candidate, {
        "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        "object_id": oid,
        "candidate_count": 1,
        "boundary_signature": sig,
        "boundary_kind": sel["boundary_kind"],
        "reason": None,
        "source_repository": source_context["source_repository"],
        "source_version": source_context["source_version"],
    }


def _rekey_claim(c, object_id: str, boundary_signature: str, applicability_class: str, source_context: dict):
    if applicability_class not in ALLOWED_ACTIVE_APPLICABILITY:
        raise ValueError(f"inadmissible active applicability class: {applicability_class}")
    x = dict(c)
    x["object_id"] = object_id
    x["object_boundary_signature"] = boundary_signature
    x["applicability_class"] = applicability_class
    x["source_repository"] = source_context["source_repository"]
    x["source_version"] = source_context["source_version"]
    x["population_scope"] = source_context["population_scope"]
    payload = {
        "object_id": object_id,
        "object_boundary_signature": boundary_signature,
        "applicability_class": applicability_class,
        "source_repository": source_context["source_repository"],
        "source_version": source_context["source_version"],
        "population_scope": source_context["population_scope"],
        "role": x.get("role"),
        "interval": x.get("interval"),
        "source_file": x.get("source_file"),
        "source_locator_contract": x.get("source_locator_contract"),
        "raw_attrs": sorted((x.get("raw_attrs") or {}).items()),
        "ordinal": x.get("ordinal"),
    }
    x["claim_key"] = _sha(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return x


def _selected_dateline_elements(candidate, pmap):
    if candidate is None:
        return []
    out = []
    for x in candidate.iter():
        if _local(x.tag) != "date" or not base._attrs(x):
            continue
        if _inside_annex(x, pmap, stop=candidate):
            continue
        anc = _ancestors(x, pmap)
        inside_marker = False
        for a in reversed(anc):
            if a is candidate:
                break
            if _local(a.tag) in ("opener", "dateline"):
                inside_marker = True
        if inside_marker:
            out.append(x)
    return out


def _excluded_body_dates(root, pmap, candidate):
    if candidate is None:
        return []
    body = next(x for x in root.iter() if _local(x.tag) == "body")
    candidate_nodes = set(candidate.iter())
    rows = []
    for x in body.iter():
        if _local(x.tag) != "date":
            continue
        attrs = base._attrs(x)
        if not attrs:
            continue
        if _inside_annex(x, pmap, stop=body):
            cls = "EXCLUDED_ANNEX"
        elif x in candidate_nodes:
            continue
        else:
            cls = "EXCLUDED_OUTSIDE_SELECTED_OBJECT"
        rows.append({
            "applicability_class": cls,
            "raw_attrs": attrs,
            "source_text": _norm(" ".join(x.itertext()))[:500],
        })
    return rows


def parse_document(path: str, raw: bytes, source_context: dict):
    ctx = _freeze_source_context(source_context)
    root, pmap, candidate, obj = _object_contract(path, raw, ctx)
    d0 = base.parse_document(path, raw)

    if obj["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        d0["source_context"] = ctx
        d0["object_contract"] = obj
        d0["object_id"] = None
        d0["primary_boundary_signature"] = None
        d0["claims"] = []
        d0["_claims_private"] = []
        d0["origin_claim"] = None
        d0["_origin_private"] = None
        d0["eligibility"] = {
            "eligible": False,
            "trigger": None,
            "live_claim_keys": [],
            "d1_pairs": [],
            "d2_pairs": [],
        }
        d0["expected_question"] = None
        d0["q0"] = {"source": "none", "intervals": []}
        d0["warrant_root"] = {"type": "UNRESOLVED", "reason": obj["status"]}
        d0["warrant_after"] = d0["warrant_root"]
        d0["required_live_claim_keys_after"] = []
        d0["full_trajectory_eligible"] = False
        d0["full_trajectory_exclusion_reasons"] = [obj["status"]]
        d0["audit_packet"] = None
        d0["excluded_temporal_claims"] = []
        return d0

    oid = obj["object_id"]
    sig = obj["boundary_signature"]

    private = []
    for c in d0.get("_claims_private", []):
        if c.get("role") in ("docDate", "sent"):
            private.append(_rekey_claim(
                c, oid, sig, "FILE_LEVEL_UNIQUE_OBJECT", ctx
            ))

    for i, x in enumerate(_selected_dateline_elements(candidate, pmap), 1):
        c = base._claim(
            path,
            "dateline",
            i,
            x,
            base._locator_token("selected_object_dateline_date", i),
        )
        private.append(_rekey_claim(
            c, oid, sig, "INSIDE_SELECTED_OBJECT_BOUNDARY", ctx
        ))

    origin = None
    if d0.get("_origin_private") is not None:
        origin = _rekey_claim(
            d0["_origin_private"],
            oid,
            sig,
            "FILE_LEVEL_UNIQUE_OBJECT",
            ctx,
        )

    eligibility = base._eligibility(private)
    root_warrant = base._warrant(private)
    post_warrant = base._warrant(private, origin) if origin else root_warrant
    required_live = base._required_live_after(private, origin, post_warrant)
    sent_claims = [c for c in private if c.get("role") == "sent"]
    q0 = base._q0(sent_claims, origin)

    expected_question = None
    if eligibility["eligible"]:
        expected_question = {
            "type": "TEMPORAL_WARRANT_QUERY",
            "trigger": eligibility["trigger"],
            "disputed_claim_keys": eligibility["live_claim_keys"],
            "object_id": oid,
        }

    reasons = []
    if not d0.get("is_correspondence") or not eligibility["eligible"]:
        reasons.append("NOT_PRIMARY_ELIGIBLE")
    if d0.get("origin_contract_status") == "NO_ORIGIN_EVIDENCE":
        reasons.append("NO_ORIGIN_EVIDENCE")
    elif d0.get("origin_contract_status") == "COMPOSITE_ORIGIN_UNRESOLVED":
        reasons.append("COMPOSITE_ORIGIN_UNRESOLVED")
    if root_warrant == post_warrant:
        reasons.append("NO_WARRANT_STATE_CHANGE")

    audit_packet = None
    if origin is not None:
        audit_packet = {
            "document": path,
            "object_id": oid,
            "object_boundary_signature": sig,
            "source_context": ctx,
            "current_warrant": post_warrant,
            "origin_event_id": f"OPEN_ORIGIN::{path}",
            "origin_evidence_key": origin["claim_key"],
            "required_live_claim_keys_after": required_live,
            "neutral_event_key": (d0.get("neutral_event") or {}).get("event_key"),
            "before_warrant": root_warrant,
            "after_warrant": post_warrant,
        }

    d0["source_context"] = ctx
    d0["object_contract"] = obj
    d0["object_id"] = oid
    d0["primary_boundary_signature"] = sig
    d0["_claims_private"] = private
    d0["claims"] = [base._strip_private_claim(c) for c in private]
    d0["_origin_private"] = origin
    d0["origin_claim"] = base._strip_private_claim(origin) if origin else None
    d0["eligibility"] = eligibility
    d0["expected_question"] = expected_question
    d0["q0"] = q0
    d0["warrant_root"] = root_warrant
    d0["warrant_after"] = post_warrant
    d0["required_live_claim_keys_after"] = required_live
    d0["full_trajectory_eligible"] = not reasons
    d0["full_trajectory_exclusion_reasons"] = reasons
    d0["audit_packet"] = audit_packet
    d0["excluded_temporal_claims"] = _excluded_body_dates(root, pmap, candidate)
    return d0
