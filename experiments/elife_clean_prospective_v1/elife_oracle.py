from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

from lxml import etree

import elife_constants as C


def _lname(tag: Any) -> str:
    if not isinstance(tag, str):
        return ""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def _children(node, name: str):
    return [x for x in node if _lname(x.tag) == name]


def _first_child(node, name: str):
    xs = _children(node, name)
    return xs[0] if xs else None


def _text(node) -> str:
    return "".join(node.itertext()).strip() if node is not None else ""


def _main_article_meta(root):
    front = _first_child(root, "front")
    if front is None:
        return None
    return _first_child(front, "article-meta")


def _article_ids(article_meta):
    out = []
    if article_meta is None:
        return out
    for el in _children(article_meta, "article-id"):
        out.append({
            "pub_id_type": el.get("pub-id-type"),
            "specific_use": el.get("specific-use"),
            "value": _text(el),
        })
    return out


def _version_alternatives(article_meta):
    result = {"preprint_version_raw": None, "publication_state": None}
    if article_meta is None:
        return result
    ava = _first_child(article_meta, "article-version-alternatives")
    if ava is None:
        return result
    for el in _children(ava, "article-version"):
        kind = el.get("article-version-type")
        if kind == "preprint-version":
            result["preprint_version_raw"] = _text(el)
        elif kind == "publication-state":
            result["publication_state"] = _text(el)
    return result


def _subarticle_surface(root):
    assessments = []
    reviews = []
    responses = []
    unknown = []
    for sub in _children(root, "sub-article"):
        typ = sub.get("article-type")
        front_stub = _first_child(sub, "front-stub")
        doi = None
        if front_stub is not None:
            for aid in _children(front_stub, "article-id"):
                if aid.get("pub-id-type") == "doi":
                    doi = C.canonical_doi(_text(aid))
                    break
        row = {"type": typ, "doi": doi}
        if typ == "editor-report":
            assessments.append(row)
        elif typ == "referee-report":
            reviews.append(row)
        elif typ == "author-comment":
            responses.append(row)
        else:
            unknown.append(row)
    return {
        "assessments": assessments,
        "reviews": reviews,
        "responses": responses,
        "unknown_subarticles": unknown,
    }


def _history_surface(article_meta):
    events = []
    if article_meta is None:
        return events
    ph = _first_child(article_meta, "pub-history")
    if ph is None:
        return events
    for event in _children(ph, "event"):
        uris = []
        for u in _children(event, "self-uri"):
            href = (
                u.get(C.XLINK_HREF)
                or u.get("href")
                or u.get("{http://www.w3.org/1999/xlink}href")
            )
            uris.append({
                "content_type": u.get("content-type"),
                "doi": C.canonical_doi(href),
                "label": _text(u),
            })
        rp = [x["doi"] for x in uris if x["content_type"] == "reviewed-preprint"]
        if not rp:
            continue
        dates = []
        for d in _children(event, "date"):
            dates.append({
                "date_type": d.get("date-type"),
                "iso": d.get("iso-8601-date"),
            })
        events.append({
            "reviewed_preprint_dois": sorted(x for x in rp if x),
            "assessment_dois": sorted(
                x["doi"] for x in uris
                if x["content_type"] == "editor-report" and x["doi"]
            ),
            "review_dois": sorted(
                x["doi"] for x in uris
                if x["content_type"] == "referee-report" and x["doi"]
            ),
            "response_dois": sorted(
                x["doi"] for x in uris
                if x["content_type"] == "author-comment" and x["doi"]
            ),
            "dates": sorted(
                dates,
                key=lambda x: (str(x.get("date_type")), str(x.get("iso"))),
            ),
        })
    events.sort(key=lambda x: x["reviewed_preprint_dois"])
    return events


def _preprint_version(raw: str | None):
    if raw is None:
        return None
    m = re.fullmatch(r"1\.(\d+)", raw.strip())
    return int(m.group(1)) if m else None


def parse_xml(path: str, raw: bytes) -> dict:
    traces = {"PARSE_OK"}
    name = Path(path).name
    fm = C.FILENAME_RE.fullmatch(name)
    filename_msid = fm.group(1) if fm else None
    filename_version = int(fm.group(2)) if fm else None

    root = etree.fromstring(raw)
    meta = _main_article_meta(root)
    ids = _article_ids(meta)
    publisher_ids = [
        x["value"] for x in ids if x["pub_id_type"] == "publisher-id"
    ]
    version_dois = [
        C.canonical_doi(x["value"])
        for x in ids
        if x["pub_id_type"] == "doi" and x["specific_use"] == "version"
    ]
    va = _version_alternatives(meta)
    preprint_version = _preprint_version(va["preprint_version_raw"])
    subs = _subarticle_surface(root)
    history = _history_surface(meta)

    version_doi = version_dois[0] if len(version_dois) == 1 else None
    vm = C.VERSION_DOI_RE.fullmatch(version_doi or "")
    xml_msid = vm.group(1) if vm else None
    xml_version = int(vm.group(2)) if vm else None

    rp_version = filename_version
    if rp_version == 1:
        traces.add("VERSION_V1")
    elif rp_version is not None and rp_version > 1:
        traces.add("VERSION_REVISED")

    ac = len(subs["assessments"])
    traces.add(
        "ASSESSMENT_MISSING" if ac == 0
        else "ASSESSMENT_ONE" if ac == 1
        else "ASSESSMENT_MULTIPLE"
    )
    rc = len(subs["reviews"])
    traces.add(
        "REVIEW_MISSING" if rc == 0
        else "REVIEW_ONE" if rc == 1
        else "REVIEW_MULTIPLE"
    )
    xc = len(subs["responses"])
    traces.add(
        "AUTHOR_RESPONSE_ABSENT" if xc == 0
        else "AUTHOR_RESPONSE_PRESENT" if xc == 1
        else "AUTHOR_RESPONSE_MULTIPLE"
    )
    traces.add("PRIOR_HISTORY_PRESENT" if history else "PRIOR_HISTORY_NONE")
    traces.add(
        "UNKNOWN_SUBARTICLE_PRESENT"
        if subs["unknown_subarticles"]
        else "UNKNOWN_SUBARTICLE_ABSENT"
    )

    surface = {
        "path": path,
        "filename_msid": filename_msid,
        "filename_rp_version": filename_version,
        "publisher_ids": sorted(publisher_ids),
        "version_dois": sorted(x for x in version_dois if x),
        "version_doi": version_doi,
        "xml_msid": xml_msid,
        "xml_rp_version": xml_version,
        "preprint_version_raw": va["preprint_version_raw"],
        "preprint_version": preprint_version,
        "publication_state": va["publication_state"],
        "assessments": sorted(subs["assessments"], key=lambda x: str(x["doi"])),
        "reviews": sorted(subs["reviews"], key=lambda x: str(x["doi"])),
        "responses": sorted(subs["responses"], key=lambda x: str(x["doi"])),
        "unknown_subarticles": sorted(
            subs["unknown_subarticles"],
            key=lambda x: (str(x["type"]), str(x["doi"])),
        ),
        "prior_events": history,
        "traces": sorted(traces),
    }
    return surface


def _current_prefix_ok(surface):
    prefix = (surface.get("version_doi") or "") + ".sa"
    rows = (
        surface.get("assessments", [])
        + surface.get("reviews", [])
        + surface.get("responses", [])
    )
    return all(x.get("doi") and x["doi"].startswith(prefix) for x in rows)


def _identity_ok(surface):
    msid = surface.get("filename_msid")
    ver = surface.get("filename_rp_version")
    return all([
        msid is not None,
        ver is not None,
        surface.get("publisher_ids") == [msid],
        surface.get("version_dois") == [C.expected_version_doi(msid, ver)],
        surface.get("xml_msid") == msid,
        surface.get("xml_rp_version") == ver,
    ])


def _prior_history_check(surface):
    msid = surface.get("filename_msid")
    ver = surface.get("filename_rp_version")
    events = surface.get("prior_events", [])
    if not msid or not ver:
        return {
            "count_ok": False,
            "version_set_ok": False,
            "assessment_ok": False,
            "review_ok": False,
            "prefix_ok": False,
        }
    if ver == 1:
        return {
            "count_ok": len(events) == 0,
            "version_set_ok": len(events) == 0,
            "assessment_ok": True,
            "review_ok": True,
            "prefix_ok": True,
        }

    expected = {
        C.expected_version_doi(msid, x) for x in range(1, ver)
    }
    observed = set()
    assessment_ok = True
    review_ok = True
    prefix_ok = True
    for e in events:
        if len(e["reviewed_preprint_dois"]) == 1:
            base = e["reviewed_preprint_dois"][0]
            observed.add(base)
        else:
            base = ""
            prefix_ok = False
        if len(e["assessment_dois"]) != 1:
            assessment_ok = False
        if len(e["review_dois"]) < 1:
            review_ok = False
        for d in (
            e["assessment_dois"]
            + e["review_dois"]
            + e["response_dois"]
        ):
            if not base or not d.startswith(base + ".sa"):
                prefix_ok = False

    return {
        "count_ok": len(events) == ver - 1,
        "version_set_ok": observed == expected,
        "assessment_ok": assessment_ok,
        "review_ok": review_ok,
        "prefix_ok": prefix_ok,
    }


def evaluate_surface(surface: dict) -> dict:
    traces = set(surface.get("traces", []))
    identity_ok = _identity_ok(surface)
    traces.add("IDENTITY_OK" if identity_ok else "IDENTITY_BAD")

    pv_ok = (
        surface.get("preprint_version") is not None
        and surface.get("filename_rp_version") is not None
        and surface["filename_rp_version"] <= surface["preprint_version"]
    )
    traces.add("PREPRINT_VERSION_OK" if pv_ok else "PREPRINT_VERSION_BAD")

    prefix_ok = _current_prefix_ok(surface)
    traces.add("CURRENT_EVAL_PREFIX_OK" if prefix_ok else "CURRENT_EVAL_PREFIX_BAD")

    current_ok = all([
        len(surface.get("assessments", [])) == 1,
        len(surface.get("reviews", [])) >= 1,
        len(surface.get("responses", [])) <= 1,
        prefix_ok,
    ])

    ph = _prior_history_check(surface)
    traces.add("PRIOR_HISTORY_COUNT_OK" if ph["count_ok"] else "PRIOR_HISTORY_COUNT_BAD")
    traces.add("PRIOR_VERSION_SET_OK" if ph["version_set_ok"] else "PRIOR_VERSION_SET_BAD")
    traces.add("PRIOR_EVENT_ASSESSMENT_OK" if ph["assessment_ok"] else "PRIOR_EVENT_ASSESSMENT_BAD")
    traces.add("PRIOR_EVENT_REVIEW_OK" if ph["review_ok"] else "PRIOR_EVENT_REVIEW_BAD")
    traces.add("PRIOR_EVENT_PREFIX_OK" if ph["prefix_ok"] else "PRIOR_EVENT_PREFIX_BAD")
    history_ok = all(ph.values())

    if not identity_ok or not pv_ok:
        disposition = "INVALID_IDENTITY"
    elif not current_ok:
        disposition = "INVALID_CURRENT_EVALUATION_BINDING"
    elif not history_ok:
        disposition = "INVALID_PRIOR_HISTORY"
    elif surface["filename_rp_version"] == 1:
        disposition = "COMPLETE_V1"
    else:
        disposition = "COMPLETE_REVISED"

    return {
        "disposition": disposition,
        "identity_ok": identity_ok,
        "preprint_version_ok": pv_ok,
        "current_evaluation_ok": current_ok,
        "prior_history": ph,
        "prior_history_ok": history_ok,
        "traces": sorted(traces),
    }


def initial_state(surface: dict, include_current: bool = False) -> dict:
    state = {
        "manuscript_id": surface.get("filename_msid"),
        "rp_version": surface.get("filename_rp_version"),
        "version_doi": surface.get("version_doi"),
        "preprint_version": surface.get("preprint_version"),
        "publication_state": surface.get("publication_state"),
        "current_assessment_dois": [],
        "current_review_dois": [],
        "current_response_dois": [],
        "prior_events": copy.deepcopy(surface.get("prior_events", [])),
        "published": False,
    }
    if include_current:
        state["current_assessment_dois"] = [
            x["doi"] for x in surface.get("assessments", []) if x.get("doi")
        ]
        state["current_review_dois"] = [
            x["doi"] for x in surface.get("reviews", []) if x.get("doi")
        ]
        state["current_response_dois"] = [
            x["doi"] for x in surface.get("responses", []) if x.get("doi")
        ]
    return state


def actions_for_surface(surface: dict) -> list[dict]:
    version_doi = surface.get("version_doi")
    actions = []
    for x in surface.get("assessments", []):
        actions.append({
            "generator": "REGISTER_ASSESSMENT",
            "target_version_doi": version_doi,
            "evaluation_doi": x.get("doi"),
            "evaluation_type": "editor-report",
        })
    for x in surface.get("reviews", []):
        actions.append({
            "generator": "REGISTER_PUBLIC_REVIEW",
            "target_version_doi": version_doi,
            "evaluation_doi": x.get("doi"),
            "evaluation_type": "referee-report",
        })
    for x in surface.get("responses", []):
        actions.append({
            "generator": "REGISTER_AUTHOR_RESPONSE",
            "target_version_doi": version_doi,
            "evaluation_doi": x.get("doi"),
            "evaluation_type": "author-comment",
        })
    actions.append({
        "generator": (
            "PUBLISH_REVIEWED_PREPRINT"
            if surface.get("filename_rp_version") == 1
            else "PUBLISH_REVISED_REVIEWED_PREPRINT"
        ),
        "target_version_doi": version_doi,
    })
    return actions


def _history_valid_for_state(state: dict) -> bool:
    msid = state.get("manuscript_id")
    ver = state.get("rp_version")
    events = state.get("prior_events", [])
    if not msid or not ver:
        return False
    if ver == 1:
        return len(events) == 0
    if len(events) != ver - 1:
        return False
    expected = {
        C.expected_version_doi(msid, x) for x in range(1, ver)
    }
    observed = set()
    for e in events:
        if len(e.get("reviewed_preprint_dois", [])) != 1:
            return False
        base = e["reviewed_preprint_dois"][0]
        observed.add(base)
        if len(e.get("assessment_dois", [])) != 1:
            return False
        if len(e.get("review_dois", [])) < 1:
            return False
        for d in (
            e.get("assessment_dois", [])
            + e.get("review_dois", [])
            + e.get("response_dois", [])
        ):
            if not d.startswith(base + ".sa"):
                return False
    return observed == expected


def qualify_action(state: dict, action: dict) -> dict:
    generator = action.get("generator")
    target = action.get("target_version_doi")
    if target != state.get("version_doi"):
        return {"qualified": False, "generator": None, "reason": "WRONG_TARGET"}

    if generator in {
        "REGISTER_PUBLIC_REVIEW",
        "REGISTER_ASSESSMENT",
        "REGISTER_AUTHOR_RESPONSE",
    }:
        doi = action.get("evaluation_doi")
        expected_type = {
            "REGISTER_PUBLIC_REVIEW": "referee-report",
            "REGISTER_ASSESSMENT": "editor-report",
            "REGISTER_AUTHOR_RESPONSE": "author-comment",
        }[generator]
        if action.get("evaluation_type") != expected_type:
            return {"qualified": False, "generator": None, "reason": "WRONG_EVALUATION_TYPE"}
        if not doi or not doi.startswith(state["version_doi"] + ".sa"):
            return {"qualified": False, "generator": None, "reason": "WRONG_EVALUATION_BINDING"}
        return {"qualified": True, "generator": generator, "reason": None}

    current_ok = (
        len(state.get("current_assessment_dois", [])) == 1
        and len(state.get("current_review_dois", [])) >= 1
    )
    if not current_ok:
        return {"qualified": False, "generator": None, "reason": "MISSING_CURRENT_EVALUATION"}

    if generator == "PUBLISH_REVIEWED_PREPRINT":
        if state.get("rp_version") != 1:
            return {"qualified": False, "generator": None, "reason": "WRONG_VERSION_CLASS"}
        return {"qualified": True, "generator": generator, "reason": None}

    if generator == "PUBLISH_REVISED_REVIEWED_PREPRINT":
        if not state.get("rp_version") or state["rp_version"] <= 1:
            return {"qualified": False, "generator": None, "reason": "WRONG_VERSION_CLASS"}
        if not _history_valid_for_state(state):
            return {"qualified": False, "generator": None, "reason": "MISSING_OR_INVALID_PRIOR_HISTORY"}
        return {"qualified": True, "generator": generator, "reason": None}

    return {"qualified": False, "generator": None, "reason": "UNREGISTERED_GENERATOR"}


def apply_action(state: dict, action: dict) -> dict:
    q = qualify_action(state, action)
    out = copy.deepcopy(state)
    if not q["qualified"]:
        return {"qualification": q, "state": out}

    g = q["generator"]
    doi = action.get("evaluation_doi")
    if g == "REGISTER_ASSESSMENT":
        out["current_assessment_dois"].append(doi)
    elif g == "REGISTER_PUBLIC_REVIEW":
        out["current_review_dois"].append(doi)
    elif g == "REGISTER_AUTHOR_RESPONSE":
        out["current_response_dois"].append(doi)
    elif g in {
        "PUBLISH_REVIEWED_PREPRINT",
        "PUBLISH_REVISED_REVIEWED_PREPRINT",
    }:
        out["published"] = True
    return {"qualification": q, "state": out}
