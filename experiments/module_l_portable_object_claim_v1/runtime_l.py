from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

from lxml import etree as LET

HERE = Path(__file__).resolve().parent
I_DIR = HERE.parent / "module_i_dahn_document_boundary_holdout_v1"
if str(I_DIR) not in sys.path:
    sys.path.insert(0, str(I_DIR))

import runtime_v2 as base

INTERFACES = base.INTERFACES
ALLOWED_ACTIVE_APPLICABILITY = {
    "FILE_LEVEL_UNIQUE_OBJECT",
    "INSIDE_SELECTED_OBJECT_BOUNDARY",
}


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _boundary_signature(el) -> str:
    """Runtime implementation of the parser-neutral structural boundary signature."""
    def emit(node):
        attrs = sorted((_local(k), v) for k, v in node.attrib.items())
        parts = [["tag", _local(node)], ["attrs", attrs]]

        # Canonicalize text between element children. Comments and processing
        # instructions are semantically ignored, but their tails remain part
        # of the surrounding text segment. This makes lxml and ElementTree
        # agree on the same TEI object.
        text_buf = [node.text or ""]
        for child in list(node):
            if isinstance(child.tag, str):
                segment = _norm("".join(text_buf))
                if segment:
                    parts.append(["text", segment])
                parts.append(["child", emit(child)])
                text_buf = [child.tail or ""]
            else:
                text_buf.append(child.tail or "")
        segment = _norm("".join(text_buf))
        if segment:
            parts.append(["text", segment])
        return parts

    return _sha(
        json.dumps(emit(el), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def _norm(s: str) -> str:
    return " ".join((s or "").split())


def _local(el) -> str:
    return LET.QName(el).localname


def _freeze_source_context(source_context: dict) -> dict:
    required = ("source_repository", "source_version", "population_scope")
    out = {k: str(source_context.get(k) or "").strip() for k in required}
    if not all(out.values()):
        raise ValueError(f"incomplete source context: {out}")
    return out


def _inside_annex(el, stop=None) -> bool:
    cur = el.getparent()
    while cur is not None and cur is not stop:
        if (
            _local(cur) == "div"
            and (cur.get("type") or "").strip().lower() in {"annex", "annexe"}
        ):
            return True
        cur = cur.getparent()
    return False


def _object_selection(root):
    if any(
        _local(x) == "revisionDesc"
        and (x.get("status") or "").strip().lower() == "placeholder"
        for x in root.iter()
    ):
        return {
            "status": "NO_PRIMARY_DOCUMENT_OBJECT",
            "candidates": [],
            "boundary_kind": None,
            "reason": "PLACEHOLDER_DOCUMENT",
        }
    bodies = root.xpath("//*[local-name()='body']")
    if not bodies:
        return {
            "status": "NO_PRIMARY_DOCUMENT_OBJECT",
            "candidates": [],
            "boundary_kind": None,
            "reason": "NO_BODY",
        }

    body = bodies[0]

    explicit = []
    for x in body.xpath(".//*[local-name()='div' and @type='letter']"):
        if not _inside_annex(x, stop=body):
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

    trans = body.xpath(".//*[local-name()='div' and @type='transcription']")
    if len(trans) > 1:
        return {
            "status": "MULTIPLE_PRIMARY_DOCUMENT_OBJECTS",
            "candidates": trans,
            "boundary_kind": None,
            "reason": "MULTIPLE_TRANSCRIPTIONS_WITHOUT_EXPLICIT_LETTER",
        }

    corresp_desc = root.xpath("//*[local-name()='correspDesc']")
    sent_actions = root.xpath("//*[local-name()='correspAction' and @type='sent']")

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

    direct_divs = body.xpath("./*[local-name()='div']")
    if len(direct_divs) == 1:
        candidate = direct_divs[0]
        markers = candidate.xpath(
            ".//*[local-name()='opener' or local-name()='closer' or "
            "local-name()='salute' or local-name()='signed' or local-name()='dateline']"
        )
        substantive = bool(_norm(" ".join(candidate.itertext())))
        if (
            candidate.get("type") is None
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
    parser = LET.XMLParser(resolve_entities=False, no_network=True, recover=False)
    root = LET.fromstring(raw, parser)
    sel = _object_selection(root)
    candidates = sel["candidates"]

    if sel["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        return root, None, {
            "status": sel["status"],
            "object_id": None,
            "candidate_count": len(candidates),
            "boundary_signature": None,
            "boundary_kind": sel["boundary_kind"],
            "reason": sel.get("reason"),
            "source_repository": source_context["source_repository"],
            "source_version": source_context["source_version"],
            "population_scope": source_context["population_scope"],
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
    return root, candidate, {
        "status": "SINGLE_PRIMARY_DOCUMENT_OBJECT",
        "object_id": oid,
        "candidate_count": 1,
        "boundary_signature": sig,
        "boundary_kind": sel["boundary_kind"],
        "reason": None,
        "source_repository": source_context["source_repository"],
        "source_version": source_context["source_version"],
        "population_scope": source_context["population_scope"],
    }


def _rekey_claim(c, object_id: str, boundary_signature: str, applicability_class: str, source_context: dict):
    if applicability_class not in ALLOWED_ACTIVE_APPLICABILITY:
        raise ValueError(f"inadmissible active applicability class: {applicability_class}")
    x = copy.deepcopy(c)
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


def _selected_dateline_elements(candidate):
    if candidate is None:
        return []
    out = []
    for x in candidate.xpath(".//*[local-name()='date']"):
        if not base.date_attrs(x):
            continue
        if _inside_annex(x, stop=candidate):
            continue
        ancestors = []
        cur = x.getparent()
        while cur is not None:
            ancestors.append(cur)
            if cur is candidate:
                break
            cur = cur.getparent()
        if any(_local(a) in ("opener", "dateline") for a in ancestors):
            out.append(x)
    return out


def _excluded_body_dates(root, candidate):
    if candidate is None:
        return []
    body = root.xpath("//*[local-name()='body']")[0]
    candidate_nodes = {candidate, *candidate.iterdescendants()}
    tree = root.getroottree()
    rows = []
    for x in body.xpath(".//*[local-name()='date']"):
        attrs = base.date_attrs(x)
        if not attrs:
            continue
        if _inside_annex(x, stop=body):
            cls = "EXCLUDED_ANNEX"
        elif x in candidate_nodes:
            continue
        else:
            cls = "EXCLUDED_OUTSIDE_SELECTED_OBJECT"
        rows.append({
            "applicability_class": cls,
            "raw_attrs": attrs,
            "source_locator_xpath": tree.getpath(x),
            "source_text": _norm(" ".join(x.itertext()))[:500],
        })
    return rows


def parse_document(path: str, raw: bytes, source_context: dict, fault: str | None = None):
    ctx = _freeze_source_context(source_context)
    root, candidate, obj = _object_contract(path, raw, ctx)
    base_doc = base.parse_document(path, raw)

    base_doc["source_context"] = ctx
    base_doc["object_contract"] = obj
    base_doc["object_id"] = obj["object_id"]
    base_doc["primary_boundary_signature"] = obj["boundary_signature"]

    if obj["status"] != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        base_doc["claims"] = []
        base_doc["origin_claim"] = None
        base_doc["origin_handle"] = None
        base_doc["eligibility"] = {
            "eligible": False,
            "trigger": None,
            "live_claim_keys": [],
            "d1_pairs": [],
            "d2_pairs": [],
        }
        base_doc["expected_question"] = None
        base_doc["q0"] = {"source": "none", "intervals": []}
        base_doc["warrant_root"] = {
            "type": "UNRESOLVED",
            "reason": obj["status"],
        }
        base_doc["warrant_after"] = copy.deepcopy(base_doc["warrant_root"])
        base_doc["required_live_claim_keys_after"] = []
        base_doc["full_trajectory_eligible"] = False
        base_doc["full_trajectory_exclusion_reasons"] = [obj["status"]]
        base_doc["excluded_temporal_claims"] = []
        base_doc["neutral_event"] = copy.deepcopy(base.CONTROL_NULL_EVENT)
        return base_doc

    oid = obj["object_id"]
    sig = obj["boundary_signature"]

    claims = []
    for c in base_doc.get("claims", []):
        if c.get("role") in ("docDate", "sent"):
            claims.append(_rekey_claim(
                c, oid, sig, "FILE_LEVEL_UNIQUE_OBJECT", ctx
            ))

    tree = root.getroottree()
    for i, x in enumerate(_selected_dateline_elements(candidate), 1):
        c = base.make_claim(
            path,
            "dateline",
            i,
            x,
            tree,
            base.contract_locator("selected_object_dateline_date", i),
        )
        claims.append(_rekey_claim(
            c, oid, sig, "INSIDE_SELECTED_OBJECT_BOUNDARY", ctx
        ))

    origin = None
    if base_doc.get("origin_claim") is not None:
        origin = _rekey_claim(
            base_doc["origin_claim"],
            oid,
            sig,
            "FILE_LEVEL_UNIQUE_OBJECT",
            ctx,
        )

    if fault == "cross_object_claim" and claims:
        claims[0]["object_id"] = "FOREIGN_OBJECT"

    origin_handle = None
    if origin is not None:
        handle_material = {
            "document": path,
            "source_repository": ctx["source_repository"],
            "source_version": ctx["source_version"],
            "population_scope": ctx["population_scope"],
            "object_id": oid,
            "object_boundary_signature": sig,
            "claim_key": origin["claim_key"],
            "applicability_class": origin["applicability_class"],
            "locator_contract": origin["source_locator_contract"],
            "xpath": origin.get("source_locator_xpath"),
        }
        origin_handle = {
            "handle_id": _sha(
                json.dumps(handle_material, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ),
            "target_document": path,
            "source_repository": ctx["source_repository"],
            "source_commit": ctx["source_version"],
            "source_version": ctx["source_version"],
            "population_scope": ctx["population_scope"],
            "source_file": path,
            "source_locator_contract": origin["source_locator_contract"],
            "source_locator_xpath": origin.get("source_locator_xpath"),
            "object_id": oid,
            "object_boundary_signature": sig,
            "applicability_class": origin["applicability_class"],
            "claim_key": origin["claim_key"],
        }

    is_correspondence = bool(
        root.xpath("//*[local-name()='correspDesc']")
        and root.xpath("//*[local-name()='correspAction']")
    )
    eligibility = base.runtime_eligibility(claims)
    root_warrant = base.runtime_warrant(claims)
    post_claims = claims + ([origin] if origin is not None else [])
    post_warrant = base.runtime_warrant(post_claims) if origin is not None else root_warrant

    sent_claims = [c for c in claims if c.get("role") == "sent" and c.get("_bounds")]
    if sent_claims:
        q0 = {"source": "sent", "intervals": [c["interval"] for c in sent_claims]}
    elif origin is not None and origin.get("_bounds"):
        q0 = {"source": "origDate", "intervals": [origin["interval"]]}
    else:
        q0 = {"source": "none", "intervals": []}

    expected_question = None
    if eligibility.get("trigger"):
        expected_question = {
            "type": "TEMPORAL_WARRANT_QUERY",
            "trigger": eligibility["trigger"],
            "disputed_claim_keys": eligibility["live_claim_keys"],
            "object_id": oid,
        }

    reasons = []
    if not is_correspondence or not eligibility.get("eligible"):
        reasons.append("NOT_PRIMARY_ELIGIBLE")
    if base_doc.get("origin_contract_status") == "NO_ORIGIN_EVIDENCE":
        reasons.append("NO_ORIGIN_EVIDENCE")
    elif base_doc.get("origin_contract_status") == "COMPOSITE_ORIGIN_UNRESOLVED":
        reasons.append("COMPOSITE_ORIGIN_UNRESOLVED")
    if root_warrant == post_warrant:
        reasons.append("NO_WARRANT_STATE_CHANGE")

    base_doc["claims"] = claims
    base_doc["origin_claim"] = origin
    base_doc["origin_handle"] = origin_handle
    base_doc["is_correspondence"] = is_correspondence
    base_doc["eligibility"] = eligibility
    base_doc["expected_question"] = expected_question
    base_doc["q0"] = q0
    base_doc["warrant_root"] = root_warrant
    base_doc["warrant_after"] = post_warrant
    base_doc["required_live_claim_keys_after"] = base.live_keys_from_warrant(post_warrant)
    base_doc["full_trajectory_eligible"] = not reasons
    base_doc["full_trajectory_exclusion_reasons"] = reasons
    base_doc["excluded_temporal_claims"] = _excluded_body_dates(root, candidate)
    return base_doc


def runtime_q0(doc):
    if doc.get("object_contract", {}).get("status") != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        return {"source": "none", "intervals": []}
    return base.runtime_q0(doc)


def discover(claims, expected_object_id=None):
    if not claims:
        return None
    if expected_object_id is None:
        ids = {c.get("object_id") for c in claims}
        if len(ids) != 1 or None in ids:
            return None
        expected_object_id = next(iter(ids))
    if any(
        c.get("object_id") != expected_object_id
        or c.get("applicability_class") not in ALLOWED_ACTIVE_APPLICABILITY
        for c in claims
    ):
        return None
    q = base.discover(claims)
    if q:
        q["object_id"] = expected_object_id
    return q


def make_interface(doc, arm):
    if doc.get("object_contract", {}).get("status") != "SINGLE_PRIMARY_DOCUMENT_OBJECT":
        ctx = doc["source_context"]
        state = {
            "document": doc["path"],
            "object_id": None,
            "source_commit": ctx["source_version"],
            "source_repository": ctx["source_repository"],
            "population_scope": ctx["population_scope"],
            "object_boundary_signature": None,
            "q0": {"source": "none", "intervals": []},
            "claims": {},
            "current_warrant": {"type": "UNRESOLVED", "reason": doc["object_contract"]["status"]},
            "live_claim_keys": [],
            "evidence_ledger": [],
            "event_ledger": [],
            "transition_ledger": [],
            "origin_handle": None,
            "history_retained": arm != "I_NO_HISTORY",
            "interface_arm": arm,
        }
        payload = {
            "document": doc["path"],
            "object_id": None,
            "object_status": doc["object_contract"]["status"],
            "source_commit": ctx["source_version"],
            "source_repository": ctx["source_repository"],
            "population_scope": ctx["population_scope"],
            "object_boundary_signature": None,
            "q0": state["q0"],
            "claims": [],
            "origin_handle": None,
            "history_retained": state["history_retained"],
        }
        return state, payload

    state, payload = base.make_interface(doc, arm)
    ctx = doc["source_context"]
    state["source_commit"] = ctx["source_version"]
    state["source_repository"] = ctx["source_repository"]
    state["population_scope"] = ctx["population_scope"]
    state["object_id"] = doc["object_id"]
    state["object_boundary_signature"] = doc["primary_boundary_signature"]
    payload["source_commit"] = ctx["source_version"]
    payload["source_repository"] = ctx["source_repository"]
    payload["population_scope"] = ctx["population_scope"]
    payload["object_id"] = doc["object_id"]
    payload["object_boundary_signature"] = doc["primary_boundary_signature"]
    payload["object_status"] = doc["object_contract"]["status"]

    if state.get("origin_handle") is not None:
        state["origin_handle"]["source_commit"] = ctx["source_version"]
        state["origin_handle"]["source_repository"] = ctx["source_repository"]
        state["origin_handle"]["source_version"] = ctx["source_version"]
    if payload.get("origin_handle") is not None:
        payload["origin_handle"]["source_commit"] = ctx["source_version"]
        payload["origin_handle"]["source_repository"] = ctx["source_repository"]
        payload["origin_handle"]["source_version"] = ctx["source_version"]
        payload["origin_handle"]["population_scope"] = ctx["population_scope"]
        payload["origin_handle"]["object_id"] = state["origin_handle"].get("object_id")
        payload["origin_handle"]["object_boundary_signature"] = state["origin_handle"].get("object_boundary_signature")
        payload["origin_handle"]["applicability_class"] = state["origin_handle"].get("applicability_class")
        payload["origin_handle"]["claim_key"] = state["origin_handle"].get("claim_key")

    if arm == "I_NO_BINDING":
        state["object_id"] = None
        state["object_boundary_signature"] = None
        payload["object_id"] = None
        payload["object_boundary_signature"] = None
        for c in state["claims"].values():
            c["object_id"] = None
            c["object_boundary_signature"] = None
            c["applicability_class"] = None
        for c in payload.get("claims", []):
            c["object_id"] = None
            c["object_boundary_signature"] = None
            c["applicability_class"] = None

    return state, payload


def _reject_origin_transition(state, reason):
    """Reject an evidence release before any temporal state mutation occurs."""
    before = copy.deepcopy(state)
    event_id = f"OPEN_ORIGIN::{state['document']}"
    state["event_ledger"].append({
        "event_id": event_id,
        "event_class": "EVIDENCE_RELEASE",
        "target_document": state["document"],
        "applicable": False,
        "reason": reason,
    })
    transition = {
        "event_id": event_id,
        "event_class": "OPEN_ORIGIN",
        "target_document": state["document"],
        "object_id": state.get("object_id"),
        "applicable": False,
        "evidence_key": None,
        "before_warrant": before["current_warrant"],
        "after_warrant": state["current_warrant"],
        "before_temporal_digest": base.temporal_digest(before),
        "after_temporal_digest": base.temporal_digest(state),
        "changed_paths": [],
        "collateral_temporal_paths": [reason] if reason else [],
    }
    state["transition_ledger"].append(copy.deepcopy(transition))
    return state, transition


def _origin_binding_ok(state, doc, question):
    handle = state.get("origin_handle")
    origin = doc.get("origin_claim")
    if not question or not handle or not origin:
        return False
    return all([
        question.get("object_id") == state.get("object_id"),
        handle.get("target_document") == state.get("document"),
        handle.get("source_file") == state.get("document"),
        handle.get("source_repository") == state.get("source_repository"),
        handle.get("source_commit") == state.get("source_commit"),
        handle.get("source_version") == state.get("source_commit"),
        handle.get("population_scope") == state.get("population_scope"),
        handle.get("object_id") == state.get("object_id"),
        handle.get("object_boundary_signature") == state.get("object_boundary_signature"),
        handle.get("object_boundary_signature") == origin.get("object_boundary_signature"),
        handle.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT",
        origin.get("applicability_class") == "FILE_LEVEL_UNIQUE_OBJECT",
        handle.get("claim_key") == origin.get("claim_key"),
        handle.get("source_locator_contract") == origin.get("source_locator_contract"),
        handle.get("source_locator_xpath") == origin.get("source_locator_xpath"),
        origin.get("object_id") == state.get("object_id"),
        origin.get("source_repository") == state.get("source_repository"),
        origin.get("source_version") == state.get("source_commit"),
        origin.get("population_scope") == state.get("population_scope"),
    ])


def apply_open_origin(state, doc, question, fault=None):
    if state.get("object_id") is None or doc.get("object_id") is None:
        return _reject_origin_transition(state, "NO_BOUND_OBJECT")

    if any(
        c.get("object_id") != state["object_id"]
        or c.get("object_boundary_signature") != state.get("object_boundary_signature")
        or c.get("applicability_class") not in ALLOWED_ACTIVE_APPLICABILITY
        or c.get("source_repository") != state.get("source_repository")
        or c.get("source_version") != state.get("source_commit")
        or c.get("population_scope") != state.get("population_scope")
        for c in state["claims"].values()
    ):
        return _reject_origin_transition(state, "INVALID_OBJECT_OR_APPLICABILITY_BINDING")

    if fault and fault.get("type") in {
        "source_context_mismatch",
        "object_context_mismatch",
        "claim_context_mismatch",
        "boundary_context_mismatch",
    }:
        state = copy.deepcopy(state)
        handle = state.get("origin_handle")
        if handle is not None:
            if fault.get("type") == "source_context_mismatch":
                handle["source_commit"] = "MISMATCHED_SOURCE_VERSION"
            elif fault.get("type") == "object_context_mismatch":
                handle["object_id"] = "FOREIGN_OBJECT"
            elif fault.get("type") == "claim_context_mismatch":
                handle["claim_key"] = "FOREIGN_CLAIM"
            elif fault.get("type") == "boundary_context_mismatch":
                handle["object_boundary_signature"] = "FOREIGN_BOUNDARY"

    if not _origin_binding_ok(state, doc, question):
        return _reject_origin_transition(state, "ORIGIN_HANDLE_BINDING_MISMATCH")

    state, transition = base.apply_open_origin(state, doc, question, fault=fault)
    transition["object_id"] = state.get("object_id")
    transition["source_repository"] = state.get("source_repository")
    transition["source_version"] = state.get("source_commit")
    transition["population_scope"] = state.get("population_scope")
    transition["object_boundary_signature"] = state.get("object_boundary_signature")
    return state, transition


def execute(doc, arm, fault=None):
    state, payload = make_interface(doc, arm)
    q = discover(list(state["claims"].values()), expected_object_id=state.get("object_id"))

    before_open = copy.deepcopy(state)
    state, origin_transition = apply_open_origin(state, doc, q, fault=fault)

    post_origin_state = copy.deepcopy(state)
    neutral_fault = fault if fault and fault.get("type") == "neutral_mutation" else None
    state, neutral_transition, null_stable = base.apply_neutral_event(
        state, doc.get("neutral_event"), fault=neutral_fault
    )

    if arm == "I_NO_HISTORY" or (fault and fault.get("type") == "drop_history"):
        state["transition_ledger"] = []

    audit = base.delayed_audit(state)
    audit["object_id"] = state.get("object_id")
    audit["source_repository"] = state.get("source_repository")
    audit["source_version"] = state.get("source_commit")

    return {
        "arm": arm,
        "payload": payload,
        "payload_bytes": len(base.canonical(payload)),
        "q0": payload["q0"],
        "question": q,
        "object_id": state.get("object_id"),
        "object_status": doc.get("object_contract", {}).get("status"),
        "source_context": doc.get("source_context"),
        "open_origin_applicable": origin_transition["applicable"],
        "origin_transition": origin_transition,
        "post_origin_warrant": post_origin_state["current_warrant"],
        "post_origin_live_claim_keys": sorted(post_origin_state["live_claim_keys"]),
        "collateral_temporal_paths": origin_transition["collateral_temporal_paths"],
        "null_event_stable": null_stable,
        "neutral_transition": neutral_transition,
        "final_warrant": state["current_warrant"],
        "final_live_claim_keys": sorted(state["live_claim_keys"]),
        "delayed_audit": audit,
        "before_open_temporal_digest": base.temporal_digest(before_open),
        "post_open_temporal_digest": base.temporal_digest(post_origin_state),
        "final_temporal_digest": base.temporal_digest(state),
    }
