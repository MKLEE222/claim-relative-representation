from __future__ import annotations

import calendar
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from datetime import date

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

DATE_ATTRS = (
    "when", "when-iso",
    "notBefore", "notAfter", "notBefore-iso", "notAfter-iso",
    "from", "to", "from-iso", "to-iso",
)

MAINT_RE = re.compile(
    r"(facs|iiif|translat|encoding|format|indent|milestone|identifier|layout|metadata|"
    r"respstmt|extent|tag\b|xml\b|image|illustration)",
    re.I,
)
TEMPORAL_RE = re.compile(
    r"(date|dating|chronolog|calendar|origdate|docdate|notbefore|notafter|when-iso)",
    re.I,
)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _norm_text(s: str) -> str:
    return " ".join((s or "").split())


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _month_bounds(y: int, m: int):
    return date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])


def _partial(v: str):
    v = (v or "").strip()
    m = re.fullmatch(r"(\d{4})", v)
    if m:
        y = int(m.group(1))
        return date(y, 1, 1), date(y, 12, 31)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", v)
    if m:
        y, mo = map(int, m.groups())
        if 1 <= mo <= 12:
            return _month_bounds(y, mo)
        return None
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", v)
    if m:
        y, mo, d = map(int, m.groups())
        try:
            x = date(y, mo, d)
            return x, x
        except ValueError:
            return None
    return None


def _parse_value(v: str):
    v = (v or "").strip()
    if not v:
        return None
    m = re.fullmatch(r"(\d{4})/(\d{4})", v)
    if m:
        a, b = map(int, m.groups())
        return date(a, 1, 1), date(b, 12, 31)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})/(\d{1,2})", v)
    if m:
        y, m1, m2 = map(int, m.groups())
        if 1 <= m1 <= 12 and 1 <= m2 <= 12:
            return _month_bounds(y, m1)[0], _month_bounds(y, m2)[1]
        return None
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})/(\d{1,2})", v)
    if m:
        y, mo, d1, d2 = map(int, m.groups())
        try:
            return date(y, mo, d1), date(y, mo, d2)
        except ValueError:
            return None
    return _partial(v)


def _attrs(el):
    return {k: el.attrib[k] for k in DATE_ATTRS if k in el.attrib}


def _bounds(attrs):
    val = attrs.get("when-iso") or attrs.get("when")
    if val:
        return _parse_value(val)
    lo_v = (
        attrs.get("notBefore-iso") or attrs.get("notBefore")
        or attrs.get("from-iso") or attrs.get("from")
    )
    hi_v = (
        attrs.get("notAfter-iso") or attrs.get("notAfter")
        or attrs.get("to-iso") or attrs.get("to")
    )
    lo = _parse_value(lo_v) if lo_v else None
    hi = _parse_value(hi_v) if hi_v else None
    if not lo and not hi:
        return None
    return lo[0] if lo else date.min, hi[1] if hi else date.max


def _jiv(bounds):
    if not bounds:
        return None
    lo, hi = bounds
    return [
        None if lo == date.min else lo.isoformat(),
        None if hi == date.max else hi.isoformat(),
    ]


def _kind(bounds):
    if not bounds:
        return "UNPARSED"
    lo, hi = bounds
    if lo == date.min or hi == date.max:
        return "OPEN"
    if lo == hi:
        return "POINT"
    return "BOUNDED"


def _disjoint(a, b):
    return bool(a and b and (a[1] < b[0] or b[1] < a[0]))


def _overlap_nonidentical(a, b):
    return bool(a and b and not _disjoint(a, b) and a != b)


def _intersection(items):
    xs = [x for x in items if x]
    if not xs:
        return None
    lo = max(x[0] for x in xs)
    hi = min(x[1] for x in xs)
    return None if lo > hi else (lo, hi)


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


def _first_desc(el, tag):
    for x in el.iter():
        if _local(x.tag) == tag:
            return x
    return None


def _select_primary_letter(root, pmap):
    bodies = [x for x in root.iter() if _local(x.tag) == "body"]
    if not bodies:
        return None
    transcription = None
    for b in bodies:
        for x in b.iter():
            if _local(x.tag) == "div" and x.attrib.get("type") == "transcription":
                transcription = x
                break
        if transcription is not None:
            break
    if transcription is None:
        return None

    direct = [
        x for x in list(transcription)
        if _local(x.tag) == "div" and x.attrib.get("type") == "letter"
    ]
    if direct:
        return direct[0]

    for x in transcription.iter():
        if _local(x.tag) != "div" or x.attrib.get("type") != "letter":
            continue
        anc = _ancestors(x, pmap)
        if any(_local(a.tag) == "div" and a.attrib.get("type") == "annex" for a in anc):
            continue
        return x
    return None


def _boundary_signature(letter):
    if letter is None:
        return None
    txt = _norm_text(" ".join(letter.itertext()))
    return _sha(txt.encode("utf-8"))


def _locator_token(role: str, idx: int, extra: str = "") -> str:
    return f"{role}:{idx}" + (f":{extra}" if extra else "")


def _claim(path, role, idx, el, locator):
    attrs = _attrs(el)
    b = _bounds(attrs)
    iv = _jiv(b)
    key_payload = {
        "document": path,
        "role": role,
        "ordinal": idx,
        "interval": iv,
        "attrs": sorted(attrs.items()),
        "locator": locator,
    }
    key = hashlib.sha256(
        json.dumps(key_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "claim_key": key,
        "role": role,
        "ordinal": idx,
        "raw_attrs": attrs,
        "interval": iv,
        "_bounds": b,
        "status": _kind(b),
        "uncertain": (
            _kind(b) in ("BOUNDED", "OPEN")
            or bool(el.attrib.get("cert"))
            or bool(el.attrib.get("precision"))
        ),
        "cert": el.attrib.get("cert"),
        "precision": el.attrib.get("precision"),
        "resp": el.attrib.get("resp"),
        "source_file": path,
        "source_locator_contract": locator,
        "source_text": _norm_text(" ".join(el.itertext()))[:500],
    }


def _choose_origin(root):
    histories = [x for x in root.iter() if _local(x.tag) == "history"]
    if not histories:
        return None, None, None
    origin = None
    for x in list(histories[0]):
        if _local(x.tag) == "origin":
            origin = x
            break
    if origin is None:
        return None, None, None

    ps = [x for x in list(origin) if _local(x.tag) == "p"]
    chosen = None
    chosen_lang = ""
    if ps:
        for wanted in ("en", "de", "fr"):
            for p in ps:
                if (p.attrib.get(XML_LANG) or "").lower() == wanted:
                    chosen = p
                    chosen_lang = wanted
                    break
            if chosen is not None:
                break
        if chosen is None:
            chosen = ps[0]
            chosen_lang = (chosen.attrib.get(XML_LANG) or "").lower()
        for x in chosen.iter():
            if _local(x.tag) == "origDate":
                return x, origin, chosen_lang
        return None, origin, chosen_lang

    for x in origin.iter():
        if _local(x.tag) == "origDate":
            return x, origin, ""
    return None, origin, ""


def _extract_revisions(root, pmap):
    out = []
    for x in root.iter():
        if _local(x.tag) != "change":
            continue
        anc = _ancestors(x, pmap)
        if not any(_local(a.tag) == "revisionDesc" for a in anc):
            continue
        text = _norm_text(" ".join(x.itertext()))
        attrs = dict(x.attrib)
        out.append({
            "when": attrs.get("when") or attrs.get("when-iso"),
            "who": attrs.get("who"),
            "text": text,
            "attrs": attrs,
        })
    return out


def _neutral_event(revisions):
    candidates = []
    for r in revisions:
        text = r["text"]
        attrs_blob = " ".join(f"{k}={v}" for k, v in sorted(r["attrs"].items()))
        if not text or not MAINT_RE.search(text):
            continue
        if TEMPORAL_RE.search(text) or TEMPORAL_RE.search(attrs_blob):
            continue
        event_key = hashlib.sha256(
            json.dumps(
                {"when": r["when"], "who": r["who"], "text": text, "attrs": sorted(r["attrs"].items())},
                ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        candidates.append({**r, "event_key": event_key, "event_class": "NON_TEMPORAL_MAINTENANCE"})
    candidates.sort(key=lambda r: ((r["when"] or ""), r["text"], r["event_key"]))
    return candidates[0] if candidates else None


def _eligibility(claims):
    d1_pairs = []
    d2_pairs = []
    for i, a in enumerate(claims):
        for j in range(i + 1, len(claims)):
            b = claims[j]
            if _disjoint(a["_bounds"], b["_bounds"]):
                d1_pairs.append((a["claim_key"], b["claim_key"]))
            elif (
                (a["uncertain"] or b["uncertain"])
                and _overlap_nonidentical(a["_bounds"], b["_bounds"])
            ):
                d2_pairs.append((a["claim_key"], b["claim_key"]))
    trigger = "D1" if d1_pairs else "D2" if d2_pairs else None
    live_keys = sorted(set(k for pair in (d1_pairs if d1_pairs else d2_pairs) for k in pair))
    return {
        "eligible": bool(trigger),
        "trigger": trigger,
        "live_claim_keys": live_keys,
        "d1_pairs": d1_pairs,
        "d2_pairs": d2_pairs,
    }


def _warrant(root_claims, origin=None):
    usable = [c for c in root_claims if c.get("_bounds")]
    if origin is not None and origin.get("_bounds"):
        ob = origin["_bounds"]
        dis = [c for c in usable if _disjoint(ob, c["_bounds"])]
        if dis:
            alts = [origin] + dis
            return {
                "type": "ALTERNATIVE_SET",
                "alternatives": [
                    {
                        "claim_key": c["claim_key"],
                        "role": c["role"],
                        "interval": c["interval"],
                    }
                    for c in alts
                ],
            }
        k = _kind(ob)
        if k == "POINT":
            return {"type": "EXACT", "interval": origin["interval"], "basis": [origin["claim_key"]]}
        if k == "BOUNDED":
            return {"type": "INTERVAL", "interval": origin["interval"], "basis": [origin["claim_key"]]}
        if k == "OPEN":
            return {"type": "OPEN_INTERVAL", "interval": origin["interval"], "basis": [origin["claim_key"]]}

    if not usable:
        return {"type": "UNRESOLVED", "reason": "NO_MACHINE_TEMPORAL_CARRIER"}

    ib = _intersection([c["_bounds"] for c in usable])
    if ib is None:
        return {
            "type": "ALTERNATIVE_SET",
            "alternatives": [
                {
                    "claim_key": c["claim_key"],
                    "role": c["role"],
                    "interval": c["interval"],
                }
                for c in usable
            ],
        }
    if ib[0] == ib[1] and ib[0] not in (date.min, date.max):
        return {
            "type": "EXACT",
            "interval": _jiv(ib),
            "basis": [c["claim_key"] for c in usable],
        }
    if ib[0] == date.min or ib[1] == date.max:
        return {
            "type": "OPEN_INTERVAL",
            "interval": _jiv(ib),
            "basis": [c["claim_key"] for c in usable],
        }
    return {
        "type": "INTERVAL",
        "interval": _jiv(ib),
        "basis": [c["claim_key"] for c in usable],
    }


def _q0(sent_claims, origin):
    chosen = sent_claims if sent_claims else ([origin] if origin and origin.get("_bounds") else [])
    return {
        "source": "sent" if sent_claims else "origDate" if chosen else "none",
        "intervals": [c["interval"] for c in chosen],
    }


def _required_live_after(root_claims, origin, post_warrant):
    if origin is None or origin.get("_bounds") is None:
        return []
    if post_warrant.get("type") == "ALTERNATIVE_SET":
        return sorted(
            c["claim_key"] for c in root_claims
            if c.get("_bounds") and _disjoint(origin["_bounds"], c["_bounds"])
        )
    return []


def _strip_private_claim(c):
    return {k: v for k, v in c.items() if k != "_bounds"}


def parse_document(path: str, raw: bytes):
    root = ET.fromstring(raw)
    pmap = _parents(root)
    primary = _select_primary_letter(root, pmap)
    boundary_sig = _boundary_signature(primary)

    has_corresp_desc = any(_local(x.tag) == "correspDesc" for x in root.iter())
    corresp_actions = [x for x in root.iter() if _local(x.tag) == "correspAction"]
    is_correspondence = bool(has_corresp_desc and corresp_actions)

    claims = []

    doc_els = []
    for x in root.iter():
        if _local(x.tag) != "docDate" or not _attrs(x):
            continue
        if any(_local(a.tag) == "msContents" for a in _ancestors(x, pmap)):
            doc_els.append(x)
    for i, x in enumerate(doc_els, 1):
        claims.append(_claim(path, "docDate", i, x, _locator_token("msContents_docDate", i)))

    sent_els = []
    for a in corresp_actions:
        if (a.attrib.get("type") or "").lower() != "sent":
            continue
        for x in a.iter():
            if _local(x.tag) == "date" and _attrs(x):
                sent_els.append(x)
    for i, x in enumerate(sent_els, 1):
        claims.append(_claim(path, "sent", i, x, _locator_token("correspAction_sent_date", i)))

    dateline_els = []
    if primary is not None:
        for x in primary.iter():
            if _local(x.tag) != "date" or not _attrs(x):
                continue
            anc = _ancestors(x, pmap)
            # x must remain inside primary; pmap ancestry also may include document ancestors.
            inside_dateline = any(_local(a.tag) in ("opener", "dateline") for a in anc)
            inside_annex = any(
                _local(a.tag) == "div" and a.attrib.get("type") == "annex"
                for a in anc
            )
            if inside_dateline and not inside_annex:
                dateline_els.append(x)
    for i, x in enumerate(dateline_els, 1):
        claims.append(_claim(path, "dateline", i, x, _locator_token("primary_letter_dateline_date", i)))

    od, origin_el, origin_lang = _choose_origin(root)
    origin_claim = None
    if od is not None and _attrs(od):
        origin_claim = _claim(
            path, "origDate", 1, od,
            _locator_token("history_origin_origDate", 1, origin_lang or "none")
        )

    sent_claims = [c for c in claims if c["role"] == "sent"]
    eligibility = _eligibility(claims)
    root_warrant = _warrant(claims)
    post_warrant = _warrant(claims, origin_claim) if origin_claim else root_warrant
    revisions = _extract_revisions(root, pmap)
    neutral = _neutral_event(revisions)
    q0 = _q0(sent_claims, origin_claim)

    full_reasons = []
    if not is_correspondence or not eligibility["eligible"]:
        full_reasons.append("NOT_PRIMARY_ELIGIBLE")
    if origin_claim is None:
        full_reasons.append("NO_ORIGIN_EVIDENCE")
    if root_warrant == post_warrant:
        full_reasons.append("NO_WARRANT_STATE_CHANGE")
    if neutral is None:
        full_reasons.append("NO_NULL_EVENT")

    required_live = _required_live_after(claims, origin_claim, post_warrant)
    expected_question = None
    if eligibility["eligible"]:
        expected_question = {
            "type": "TEMPORAL_WARRANT_QUERY",
            "trigger": eligibility["trigger"],
            "disputed_claim_keys": eligibility["live_claim_keys"],
        }

    origin_event_id = f"OPEN_ORIGIN::{path}"
    audit_packet = None
    if origin_claim is not None:
        audit_packet = {
            "document": path,
            "current_warrant": post_warrant,
            "origin_event_id": origin_event_id,
            "origin_evidence_key": origin_claim["claim_key"],
            "required_live_claim_keys_after": required_live,
            "neutral_event_key": neutral["event_key"] if neutral else None,
            "before_warrant": root_warrant,
            "after_warrant": post_warrant,
        }

    return {
        "path": path,
        "source_sha256": _sha(raw),
        "is_correspondence": is_correspondence,
        "primary_boundary_signature": boundary_sig,
        "claims": [_strip_private_claim(c) for c in claims],
        "_claims_private": claims,
        "origin_claim": _strip_private_claim(origin_claim) if origin_claim else None,
        "_origin_private": origin_claim,
        "eligibility": eligibility,
        "expected_question": expected_question,
        "q0": q0,
        "warrant_root": root_warrant,
        "warrant_after": post_warrant,
        "required_live_claim_keys_after": required_live,
        "neutral_event": neutral,
        "full_trajectory_eligible": not full_reasons,
        "full_trajectory_exclusion_reasons": full_reasons,
        "audit_packet": audit_packet,
    }
