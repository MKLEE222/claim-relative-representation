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

UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"


def _local(tag):
    return tag.rsplit("}", 1)[-1]


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


def _norm(s):
    return " ".join((s or "").split())


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _object_selection(root):
    pmap = _parents(root)
    bodies = [x for x in root.iter() if _local(x.tag) == "body"]
    if not bodies:
        return {"status": "NO_PRIMARY_DOCUMENT_OBJECT", "candidates": [], "boundary_kind": None}

    first_body = bodies[0]
    transcriptions = [
        x for x in first_body.iter()
        if _local(x.tag) == "div" and x.attrib.get("type") == "transcription"
    ]
    if not transcriptions:
        return {"status": "NO_PRIMARY_DOCUMENT_OBJECT", "candidates": [], "boundary_kind": None}

    t = transcriptions[0]
    direct = [
        x for x in list(t)
        if _local(x.tag) == "div" and x.attrib.get("type") == "letter"
    ]
    if len(direct) == 1:
        return {"status": "SINGLE_PRIMARY_DOCUMENT_OBJECT", "candidates": direct, "boundary_kind": "EXPLICIT_LETTER_DIV"}
    if len(direct) > 1:
        return {"status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS", "candidates": direct, "boundary_kind": None}

    desc = []
    for x in t.iter():
        if x is t or _local(x.tag) != "div" or x.attrib.get("type") != "letter":
            continue
        anc = _ancestors(x, pmap)
        if any(_local(a.tag) == "div" and a.attrib.get("type") == "annex" for a in anc):
            continue
        desc.append(x)
    if len(desc) == 1:
        return {"status": "SINGLE_PRIMARY_DOCUMENT_OBJECT", "candidates": desc, "boundary_kind": "EXPLICIT_LETTER_DIV"}
    if len(desc) > 1:
        return {"status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS", "candidates": desc, "boundary_kind": None}

    # Route B: the sole transcription container is itself one scholarly letter.
    if len(transcriptions) != 1:
        return {
            "status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
            "candidates": transcriptions,
            "boundary_kind": None,
        }

    corresp_desc = [x for x in root.iter() if _local(x.tag) == "correspDesc"]
    sent_actions = [
        x for x in root.iter()
        if _local(x.tag) == "correspAction" and (x.attrib.get("type") or "").lower() == "sent"
    ]
    substantive = bool(_norm(" ".join(t.itertext())))
    if len(corresp_desc) == 1 and sent_actions and substantive:
        return {
            "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
            "candidates": [t],
            "boundary_kind": "TRANSCRIPTION_AS_LETTER",
        }

    return {"status": "NO_PRIMARY_DOCUMENT_OBJECT", "candidates": [], "boundary_kind": None}


def object_contract(path, raw):
    root = ET.fromstring(raw)
    sel = _object_selection(root)
    candidates = sel["candidates"]
    if sel["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        return {
            "status": sel["status"],
            "object_id": None,
            "candidate_count": len(candidates),
            "boundary_signature": None,
            "boundary_kind": sel["boundary_kind"],
        }

    sig = _sha(_norm(" ".join(candidates[0].itertext())).encode("utf-8"))
    payload = {
        "source_file": path,
        "source_version": UPSTREAM_COMMIT,
        "boundary_kind": sel["boundary_kind"],
        "primary_boundary_signature": sig,
    }
    oid = _sha(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return {
        "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        "object_id": oid,
        "candidate_count": 1,
        "boundary_signature": sig,
        "boundary_kind": sel["boundary_kind"],
    }


def _rekey_claim(path, c, object_id):
    x = dict(c)
    x["object_id"] = object_id
    payload = {
        "object_id": object_id,
        "role": x.get("role"),
        "interval": x.get("interval"),
        "source_file": x.get("source_file"),
        "source_locator_contract": x.get("source_locator_contract"),
        "raw_attrs": sorted((x.get("raw_attrs") or {}).items()),
        "ordinal": x.get("ordinal"),
    }
    x["claim_key"] = _sha(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return x


def parse_document(path, raw):
    obj = object_contract(path, raw)
    d = base.parse_document(path, raw)

    # Object gate is prior to temporal disagreement.
    if obj["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        d["object_contract"] = obj
        d["object_id"] = None
        d["claims"] = []
        d["_claims_private"] = []
        d["origin_claim"] = None
        d["_origin_private"] = None
        d["eligibility"] = {
            "eligible": False,
            "trigger": None,
            "live_claim_keys": [],
            "d1_pairs": [],
            "d2_pairs": [],
        }
        d["expected_question"] = None
        d["q0"] = {"source": "none", "intervals": []}
        d["warrant_root"] = {"type": "UNRESOLVED", "reason": obj["status"]}
        d["warrant_after"] = d["warrant_root"]
        d["required_live_claim_keys_after"] = []
        d["full_trajectory_eligible"] = False
        reasons = list(d.get("full_trajectory_exclusion_reasons", []))
        if obj["status"] not in reasons:
            reasons.insert(0, obj["status"])
        d["full_trajectory_exclusion_reasons"] = reasons
        d["audit_packet"] = None
        return d

    oid = obj["object_id"]
    private = []
    for c in d["_claims_private"]:
        private.append(_rekey_claim(path, c, oid))
    origin = _rekey_claim(path, d["_origin_private"], oid) if d.get("_origin_private") else None

    # All file-level metadata are admissible only because there is exactly one primary object.
    d["_claims_private"] = private
    d["claims"] = [base._strip_private_claim(c) for c in private]
    d["_origin_private"] = origin
    d["origin_claim"] = base._strip_private_claim(origin) if origin else None
    d["object_contract"] = obj
    d["object_id"] = oid
    d["primary_boundary_signature"] = obj["boundary_signature"]

    d["eligibility"] = base._eligibility(private)
    d["expected_question"] = None
    if d["eligibility"]["eligible"]:
        d["expected_question"] = {
            "type": "TEMPORAL_WARRANT_QUERY",
            "trigger": d["eligibility"]["trigger"],
            "disputed_claim_keys": d["eligibility"]["live_claim_keys"],
            "object_id": oid,
        }

    d["warrant_root"] = base._warrant(private)
    d["warrant_after"] = base._warrant(private, origin) if origin else d["warrant_root"]
    d["required_live_claim_keys_after"] = base._required_live_after(private, origin, d["warrant_after"])
    sent = [c for c in private if c["role"] == "sent"]
    d["q0"] = base._q0(sent, origin)

    reasons = []
    if not d["eligibility"]["eligible"]:
        reasons.append("NOT_PRIMARY_ELIGIBLE")
    if d.get("origin_contract_status") == "NO_ORIGIN_EVIDENCE":
        reasons.append("NO_ORIGIN_EVIDENCE")
    elif d.get("origin_contract_status") == "COMPOSITE_ORIGIN_UNRESOLVED":
        reasons.append("COMPOSITE_ORIGIN_UNRESOLVED")
    if d["warrant_root"] == d["warrant_after"]:
        reasons.append("NO_WARRANT_STATE_CHANGE")
    d["full_trajectory_exclusion_reasons"] = reasons
    d["full_trajectory_eligible"] = not reasons

    d["audit_packet"] = None
    if origin:
        d["audit_packet"] = {
            "document": path,
            "object_id": oid,
            "current_warrant": d["warrant_after"],
            "origin_event_id": f"OPEN_ORIGIN::{path}",
            "origin_evidence_key": origin["claim_key"],
            "required_live_claim_keys_after": d["required_live_claim_keys_after"],
            "neutral_event_key": d["neutral_event"]["event_key"],
            "before_warrant": d["warrant_root"],
            "after_warrant": d["warrant_after"],
        }
    return d
