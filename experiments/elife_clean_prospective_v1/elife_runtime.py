from __future__ import annotations

import copy
import re
from pathlib import Path
from xml.parsers import expat

import elife_constants as C


def _local(name: str) -> str:
    return name.split("|")[-1]


def _attr(attrs: dict, wanted: str):
    for key, value in attrs.items():
        if _local(key) == wanted:
            return value
    return None


def _preprint_version(raw):
    if raw is None:
        return None
    m = re.fullmatch(r"1\.(\d+)", str(raw).strip())
    return int(m.group(1)) if m else None


def parse_xml(path: str, raw: bytes) -> dict:
    name = Path(path).name
    fm = C.FILENAME_RE.fullmatch(name)
    filename_msid = fm.group(1) if fm else None
    filename_version = int(fm.group(2)) if fm else None

    stack = []
    attr_stack = []
    text_stack = []

    publisher_ids = []
    version_dois = []
    preprint_version_raw = None
    publication_state = None

    assessments = []
    reviews = []
    responses = []
    unknown = []
    current_sub = None

    current_event = None
    prior_events = []

    parser = expat.ParserCreate(namespace_separator="|")

    def start(name_raw, attrs):
        nonlocal current_sub, current_event
        lname = _local(name_raw)
        stack.append(lname)
        attr_stack.append(dict(attrs))
        text_stack.append([])

        if lname == "sub-article" and current_sub is None:
            current_sub = {
                "type": _attr(attrs, "article-type"),
                "doi": None,
            }

        if (
            lname == "event"
            and "pub-history" in stack[:-1]
            and current_event is None
        ):
            current_event = {
                "uris": [],
                "dates": [],
            }

    def chars(data):
        if text_stack:
            text_stack[-1].append(data)

    def end(name_raw):
        nonlocal current_sub, current_event
        lname = _local(name_raw)
        attrs = attr_stack[-1]
        text_value = "".join(text_stack[-1]).strip()
        parent = stack[-2] if len(stack) >= 2 else None
        in_sub = "sub-article" in stack
        in_event = current_event is not None and "event" in stack

        if lname == "article-id":
            if in_sub and current_sub is not None:
                if (
                    parent == "front-stub"
                    and _attr(attrs, "pub-id-type") == "doi"
                ):
                    current_sub["doi"] = C.canonical_doi(text_value)
            elif parent == "article-meta":
                if _attr(attrs, "pub-id-type") == "publisher-id":
                    publisher_ids.append(text_value)
                elif (
                    _attr(attrs, "pub-id-type") == "doi"
                    and _attr(attrs, "specific-use") == "version"
                ):
                    version_dois.append(C.canonical_doi(text_value))

        elif lname == "article-version":
            kind = _attr(attrs, "article-version-type")
            if kind == "preprint-version":
                nonlocal_set["preprint_version_raw"] = text_value
            elif kind == "publication-state":
                nonlocal_set["publication_state"] = text_value

        elif lname == "self-uri" and in_event and current_event is not None:
            current_event["uris"].append({
                "content_type": _attr(attrs, "content-type"),
                "doi": C.canonical_doi(_attr(attrs, "href")),
                "label": text_value,
            })

        elif lname == "date" and in_event and current_event is not None:
            current_event["dates"].append({
                "date_type": _attr(attrs, "date-type"),
                "iso": _attr(attrs, "iso-8601-date"),
            })

        elif lname == "event" and current_event is not None:
            rps = sorted(
                x["doi"] for x in current_event["uris"]
                if x["content_type"] == "reviewed-preprint" and x["doi"]
            )
            if rps:
                prior_events.append({
                    "reviewed_preprint_dois": rps,
                    "assessment_dois": sorted(
                        x["doi"] for x in current_event["uris"]
                        if x["content_type"] == "editor-report" and x["doi"]
                    ),
                    "review_dois": sorted(
                        x["doi"] for x in current_event["uris"]
                        if x["content_type"] == "referee-report" and x["doi"]
                    ),
                    "response_dois": sorted(
                        x["doi"] for x in current_event["uris"]
                        if x["content_type"] == "author-comment" and x["doi"]
                    ),
                    "dates": sorted(
                        current_event["dates"],
                        key=lambda x: (
                            str(x.get("date_type")),
                            str(x.get("iso")),
                        ),
                    ),
                })
            current_event = None

        elif lname == "sub-article" and current_sub is not None:
            row = {
                "type": current_sub.get("type"),
                "doi": current_sub.get("doi"),
            }
            typ = row["type"]
            if typ == "editor-report":
                assessments.append(row)
            elif typ == "referee-report":
                reviews.append(row)
            elif typ == "author-comment":
                responses.append(row)
            else:
                unknown.append(row)
            current_sub = None

        stack.pop()
        attr_stack.pop()
        text_stack.pop()

    nonlocal_set = {
        "preprint_version_raw": None,
        "publication_state": None,
    }

    parser.StartElementHandler = start
    parser.CharacterDataHandler = chars
    parser.EndElementHandler = end
    parser.Parse(raw, True)

    preprint_version_raw = nonlocal_set["preprint_version_raw"]
    publication_state = nonlocal_set["publication_state"]
    preprint_version = _preprint_version(preprint_version_raw)

    version_doi = version_dois[0] if len(version_dois) == 1 else None
    vm = C.VERSION_DOI_RE.fullmatch(version_doi or "")
    xml_msid = vm.group(1) if vm else None
    xml_version = int(vm.group(2)) if vm else None

    traces = {"PARSE_OK"}
    if filename_version == 1:
        traces.add("VERSION_V1")
    elif filename_version is not None and filename_version > 1:
        traces.add("VERSION_REVISED")

    ac = len(assessments)
    traces.add(
        "ASSESSMENT_MISSING" if ac == 0
        else "ASSESSMENT_ONE" if ac == 1
        else "ASSESSMENT_MULTIPLE"
    )
    rc = len(reviews)
    traces.add(
        "REVIEW_MISSING" if rc == 0
        else "REVIEW_ONE" if rc == 1
        else "REVIEW_MULTIPLE"
    )
    xc = len(responses)
    traces.add(
        "AUTHOR_RESPONSE_ABSENT" if xc == 0
        else "AUTHOR_RESPONSE_PRESENT" if xc == 1
        else "AUTHOR_RESPONSE_MULTIPLE"
    )
    traces.add(
        "PRIOR_HISTORY_PRESENT" if prior_events else "PRIOR_HISTORY_NONE"
    )
    traces.add(
        "UNKNOWN_SUBARTICLE_PRESENT"
        if unknown else "UNKNOWN_SUBARTICLE_ABSENT"
    )

    prior_events.sort(key=lambda x: x["reviewed_preprint_dois"])

    return {
        "path": path,
        "filename_msid": filename_msid,
        "filename_rp_version": filename_version,
        "publisher_ids": sorted(publisher_ids),
        "version_dois": sorted(x for x in version_dois if x),
        "version_doi": version_doi,
        "xml_msid": xml_msid,
        "xml_rp_version": xml_version,
        "preprint_version_raw": preprint_version_raw,
        "preprint_version": preprint_version,
        "publication_state": publication_state,
        "assessments": sorted(assessments, key=lambda x: str(x["doi"])),
        "reviews": sorted(reviews, key=lambda x: str(x["doi"])),
        "responses": sorted(responses, key=lambda x: str(x["doi"])),
        "unknown_subarticles": sorted(
            unknown, key=lambda x: (str(x["type"]), str(x["doi"]))
        ),
        "prior_events": prior_events,
        "traces": sorted(traces),
    }


def _identity(surface):
    msid = surface.get("filename_msid")
    version = surface.get("filename_rp_version")
    if msid is None or version is None:
        return False
    expected = C.expected_version_doi(msid, version)
    return (
        surface.get("publisher_ids") == [msid]
        and surface.get("version_dois") == [expected]
        and surface.get("xml_msid") == msid
        and surface.get("xml_rp_version") == version
    )


def _current_evaluations(surface):
    base = (surface.get("version_doi") or "") + ".sa"
    all_rows = []
    all_rows.extend(surface.get("assessments", []))
    all_rows.extend(surface.get("reviews", []))
    all_rows.extend(surface.get("responses", []))
    prefixes = all(
        row.get("doi") is not None
        and str(row["doi"]).startswith(base)
        for row in all_rows
    )
    cardinality = (
        len(surface.get("assessments", [])) == 1
        and len(surface.get("reviews", [])) >= 1
        and len(surface.get("responses", [])) <= 1
    )
    return cardinality, prefixes


def _history(surface):
    msid = surface.get("filename_msid")
    version = surface.get("filename_rp_version")
    events = surface.get("prior_events", [])
    if not msid or not version:
        return {
            "count_ok": False,
            "version_set_ok": False,
            "assessment_ok": False,
            "review_ok": False,
            "prefix_ok": False,
        }

    if version == 1:
        empty = len(events) == 0
        return {
            "count_ok": empty,
            "version_set_ok": empty,
            "assessment_ok": True,
            "review_ok": True,
            "prefix_ok": True,
        }

    seen = []
    ass_ok = True
    rev_ok = True
    prefix_ok = True
    for ev in events:
        roots = ev.get("reviewed_preprint_dois", [])
        if len(roots) != 1:
            prefix_ok = False
            root = None
        else:
            root = roots[0]
            seen.append(root)

        if len(ev.get("assessment_dois", [])) != 1:
            ass_ok = False
        if not ev.get("review_dois"):
            rev_ok = False

        if root is not None:
            for d in (
                ev.get("assessment_dois", [])
                + ev.get("review_dois", [])
                + ev.get("response_dois", [])
            ):
                if not str(d).startswith(root + ".sa"):
                    prefix_ok = False

    wanted = {
        C.expected_version_doi(msid, i)
        for i in range(1, version)
    }
    return {
        "count_ok": len(events) == version - 1,
        "version_set_ok": set(seen) == wanted,
        "assessment_ok": ass_ok,
        "review_ok": rev_ok,
        "prefix_ok": prefix_ok,
    }


def evaluate_surface(surface: dict) -> dict:
    traces = set(surface.get("traces", []))

    id_ok = _identity(surface)
    traces.add("IDENTITY_OK" if id_ok else "IDENTITY_BAD")

    pv = surface.get("preprint_version")
    rv = surface.get("filename_rp_version")
    pv_ok = pv is not None and rv is not None and rv <= pv
    traces.add("PREPRINT_VERSION_OK" if pv_ok else "PREPRINT_VERSION_BAD")

    current_cardinality, current_prefix = _current_evaluations(surface)
    traces.add(
        "CURRENT_EVAL_PREFIX_OK"
        if current_prefix else "CURRENT_EVAL_PREFIX_BAD"
    )
    current_ok = current_cardinality and current_prefix

    h = _history(surface)
    traces.add(
        "PRIOR_HISTORY_COUNT_OK"
        if h["count_ok"] else "PRIOR_HISTORY_COUNT_BAD"
    )
    traces.add(
        "PRIOR_VERSION_SET_OK"
        if h["version_set_ok"] else "PRIOR_VERSION_SET_BAD"
    )
    traces.add(
        "PRIOR_EVENT_ASSESSMENT_OK"
        if h["assessment_ok"] else "PRIOR_EVENT_ASSESSMENT_BAD"
    )
    traces.add(
        "PRIOR_EVENT_REVIEW_OK"
        if h["review_ok"] else "PRIOR_EVENT_REVIEW_BAD"
    )
    traces.add(
        "PRIOR_EVENT_PREFIX_OK"
        if h["prefix_ok"] else "PRIOR_EVENT_PREFIX_BAD"
    )
    history_ok = (
        h["count_ok"]
        and h["version_set_ok"]
        and h["assessment_ok"]
        and h["review_ok"]
        and h["prefix_ok"]
    )

    if not id_ok or not pv_ok:
        disp = "INVALID_IDENTITY"
    elif not current_ok:
        disp = "INVALID_CURRENT_EVALUATION_BINDING"
    elif not history_ok:
        disp = "INVALID_PRIOR_HISTORY"
    elif rv == 1:
        disp = "COMPLETE_V1"
    else:
        disp = "COMPLETE_REVISED"

    return {
        "disposition": disp,
        "identity_ok": id_ok,
        "preprint_version_ok": pv_ok,
        "current_evaluation_ok": current_ok,
        "prior_history": h,
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
            row["doi"] for row in surface.get("assessments", [])
            if row.get("doi")
        ]
        state["current_review_dois"] = [
            row["doi"] for row in surface.get("reviews", [])
            if row.get("doi")
        ]
        state["current_response_dois"] = [
            row["doi"] for row in surface.get("responses", [])
            if row.get("doi")
        ]
    return state


def actions_for_surface(surface: dict) -> list[dict]:
    base = surface.get("version_doi")
    out = []
    out += [
        {
            "generator": "REGISTER_ASSESSMENT",
            "target_version_doi": base,
            "evaluation_doi": x.get("doi"),
            "evaluation_type": "editor-report",
        }
        for x in surface.get("assessments", [])
    ]
    out += [
        {
            "generator": "REGISTER_PUBLIC_REVIEW",
            "target_version_doi": base,
            "evaluation_doi": x.get("doi"),
            "evaluation_type": "referee-report",
        }
        for x in surface.get("reviews", [])
    ]
    out += [
        {
            "generator": "REGISTER_AUTHOR_RESPONSE",
            "target_version_doi": base,
            "evaluation_doi": x.get("doi"),
            "evaluation_type": "author-comment",
        }
        for x in surface.get("responses", [])
    ]
    out.append({
        "generator": (
            "PUBLISH_REVIEWED_PREPRINT"
            if surface.get("filename_rp_version") == 1
            else "PUBLISH_REVISED_REVIEWED_PREPRINT"
        ),
        "target_version_doi": base,
    })
    return out


def _state_history_ok(state):
    msid = state.get("manuscript_id")
    version = state.get("rp_version")
    events = state.get("prior_events", [])
    if not msid or not version:
        return False
    if version == 1:
        return len(events) == 0
    if len(events) != version - 1:
        return False

    seen = set()
    for ev in events:
        roots = ev.get("reviewed_preprint_dois", [])
        if len(roots) != 1:
            return False
        root = roots[0]
        seen.add(root)
        if len(ev.get("assessment_dois", [])) != 1:
            return False
        if len(ev.get("review_dois", [])) < 1:
            return False
        for doi in (
            ev.get("assessment_dois", [])
            + ev.get("review_dois", [])
            + ev.get("response_dois", [])
        ):
            if not str(doi).startswith(root + ".sa"):
                return False
    wanted = {
        C.expected_version_doi(msid, i)
        for i in range(1, version)
    }
    return seen == wanted


def qualify_action(state: dict, action: dict) -> dict:
    target = action.get("target_version_doi")
    generator = action.get("generator")

    if target != state.get("version_doi"):
        return {
            "qualified": False,
            "generator": None,
            "reason": "WRONG_TARGET",
        }

    registration_types = {
        "REGISTER_PUBLIC_REVIEW": "referee-report",
        "REGISTER_ASSESSMENT": "editor-report",
        "REGISTER_AUTHOR_RESPONSE": "author-comment",
    }
    if generator in registration_types:
        if action.get("evaluation_type") != registration_types[generator]:
            return {
                "qualified": False,
                "generator": None,
                "reason": "WRONG_EVALUATION_TYPE",
            }
        doi = action.get("evaluation_doi")
        if doi is None or not str(doi).startswith(str(target) + ".sa"):
            return {
                "qualified": False,
                "generator": None,
                "reason": "WRONG_EVALUATION_BINDING",
            }
        return {
            "qualified": True,
            "generator": generator,
            "reason": None,
        }

    if (
        len(state.get("current_assessment_dois", [])) != 1
        or len(state.get("current_review_dois", [])) < 1
    ):
        return {
            "qualified": False,
            "generator": None,
            "reason": "MISSING_CURRENT_EVALUATION",
        }

    if generator == "PUBLISH_REVIEWED_PREPRINT":
        if state.get("rp_version") != 1:
            return {
                "qualified": False,
                "generator": None,
                "reason": "WRONG_VERSION_CLASS",
            }
        return {"qualified": True, "generator": generator, "reason": None}

    if generator == "PUBLISH_REVISED_REVIEWED_PREPRINT":
        if state.get("rp_version", 0) <= 1:
            return {
                "qualified": False,
                "generator": None,
                "reason": "WRONG_VERSION_CLASS",
            }
        if not _state_history_ok(state):
            return {
                "qualified": False,
                "generator": None,
                "reason": "MISSING_OR_INVALID_PRIOR_HISTORY",
            }
        return {"qualified": True, "generator": generator, "reason": None}

    return {
        "qualified": False,
        "generator": None,
        "reason": "UNREGISTERED_GENERATOR",
    }


def apply_action(state: dict, action: dict) -> dict:
    q = qualify_action(state, action)
    out = copy.deepcopy(state)
    if not q["qualified"]:
        return {"qualification": q, "state": out}

    generator = q["generator"]
    doi = action.get("evaluation_doi")
    if generator == "REGISTER_ASSESSMENT":
        out["current_assessment_dois"].append(doi)
    elif generator == "REGISTER_PUBLIC_REVIEW":
        out["current_review_dois"].append(doi)
    elif generator == "REGISTER_AUTHOR_RESPONSE":
        out["current_response_dois"].append(doi)
    elif generator in {
        "PUBLISH_REVIEWED_PREPRINT",
        "PUBLISH_REVISED_REVIEWED_PREPRINT",
    }:
        out["published"] = True
    return {"qualification": q, "state": out}
