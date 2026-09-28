from __future__ import annotations

import calendar
import copy
import hashlib
import json
import re
from datetime import date

from lxml import etree as LET

UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
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

CONTROL_NULL_EVENT = {
    "event_key": "CONTROL_NULL_V1",
    "event_id": "CONTROL_NULL_V1",
    "event_class": "NON_TEMPORAL_MAINTENANCE",
    "operation": "REFRESH_NON_TEMPORAL_METADATA_INDEX",
    "temporal_targets": [],
    "payload": {"index_family": "presentation-metadata", "revision": "v1"},
    "when": None,
    "who": "CONTROL",
    "text": "Controlled non-temporal presentation metadata index refresh.",
    "attrs": {},
}

INTERFACES = (
    "I_NATIVE",
    "I_RSTAR",
    "I_NO_ALTERNATIVES",
    "I_NO_BINDING",
    "I_NO_HISTORY",
)


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm_text(s: str) -> str:
    return " ".join((s or "").split())


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def month_bounds(y: int, m: int):
    return date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])


def parse_atom(v: str):
    v = (v or "").strip()
    m = re.fullmatch(r"(\d{4})", v)
    if m:
        y = int(m.group(1))
        return date(y, 1, 1), date(y, 12, 31)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", v)
    if m:
        y, mo = map(int, m.groups())
        if 1 <= mo <= 12:
            return month_bounds(y, mo)
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


def parse_temporal(v: str):
    v = (v or "").strip()
    if not v:
        return None
    m = re.fullmatch(r"(\d{4})/(\d{4})", v)
    if m:
        a, b = map(int, m.groups())
        return date(a, 1, 1), date(b, 12, 31)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})/(\d{1,2})", v)
    if m:
        y, a, b = map(int, m.groups())
        if 1 <= a <= 12 and 1 <= b <= 12:
            return month_bounds(y, a)[0], month_bounds(y, b)[1]
        return None
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})/(\d{1,2})", v)
    if m:
        y, mo, a, b = map(int, m.groups())
        try:
            return date(y, mo, a), date(y, mo, b)
        except ValueError:
            return None
    return parse_atom(v)


def date_attrs(el):
    return {k: el.attrib[k] for k in DATE_ATTRS if k in el.attrib}


def bounds_from_attrs(attrs):
    exact = attrs.get("when-iso") or attrs.get("when")
    if exact:
        return parse_temporal(exact)
    lo_s = (
        attrs.get("notBefore-iso") or attrs.get("notBefore")
        or attrs.get("from-iso") or attrs.get("from")
    )
    hi_s = (
        attrs.get("notAfter-iso") or attrs.get("notAfter")
        or attrs.get("to-iso") or attrs.get("to")
    )
    lo = parse_temporal(lo_s) if lo_s else None
    hi = parse_temporal(hi_s) if hi_s else None
    if not lo and not hi:
        return None
    return lo[0] if lo else date.min, hi[1] if hi else date.max


def interval_json(bounds):
    if not bounds:
        return None
    lo, hi = bounds
    return [
        None if lo == date.min else lo.isoformat(),
        None if hi == date.max else hi.isoformat(),
    ]


def interval_kind(bounds):
    if not bounds:
        return "UNPARSED"
    lo, hi = bounds
    if lo == date.min or hi == date.max:
        return "OPEN"
    if lo == hi:
        return "POINT"
    return "BOUNDED"


def is_disjoint(a, b):
    return bool(a and b and (a[1] < b[0] or b[1] < a[0]))


def overlaps_but_diff(a, b):
    return bool(a and b and not is_disjoint(a, b) and a != b)


def intersection(bounds):
    xs = [x for x in bounds if x]
    if not xs:
        return None
    lo = max(x[0] for x in xs)
    hi = min(x[1] for x in xs)
    return None if lo > hi else (lo, hi)


def choose_primary_letter(root):
    trans = root.xpath(
        "//*[local-name()='body']//*[local-name()='div' and @type='transcription']"
    )
    if not trans:
        return None
    t = trans[0]
    direct = t.xpath("./*[local-name()='div' and @type='letter']")
    if direct:
        return direct[0]
    desc = t.xpath(
        ".//*[local-name()='div' and @type='letter' and "
        "not(ancestor::*[local-name()='div' and @type='annex'])]"
    )
    return desc[0] if desc else None


def boundary_signature(el):
    if el is None:
        return None
    return sha256(norm_text(" ".join(el.itertext())).encode("utf-8"))


def contract_locator(role: str, idx: int, extra: str = "") -> str:
    return f"{role}:{idx}" + (f":{extra}" if extra else "")


def claim_key(path, role, idx, interval, attrs, locator):
    payload = {
        "document": path,
        "role": role,
        "ordinal": idx,
        "interval": interval,
        "attrs": sorted(attrs.items()),
        "locator": locator,
    }
    return sha256(canonical(payload))


def make_claim(path, role, idx, el, tree, locator):
    attrs = date_attrs(el)
    b = bounds_from_attrs(attrs)
    iv = interval_json(b)
    return {
        "claim_key": claim_key(path, role, idx, iv, attrs, locator),
        "role": role,
        "ordinal": idx,
        "raw_attrs": attrs,
        "interval": iv,
        "_bounds": b,
        "status": interval_kind(b),
        "uncertain": (
            interval_kind(b) in ("BOUNDED", "OPEN")
            or bool(el.get("cert"))
            or bool(el.get("precision"))
        ),
        "cert": el.get("cert"),
        "precision": el.get("precision"),
        "resp": el.get("resp"),
        "source_file": path,
        "source_locator_contract": locator,
        "source_locator_xpath": tree.getpath(el),
        "source_text": norm_text(" ".join(el.itertext()))[:500],
    }


def choose_origin(root):
    origins = root.xpath("//*[local-name()='history']/*[local-name()='origin']")
    if not origins:
        return [], ""
    origin = origins[0]
    ps = origin.xpath("./*[local-name()='p']")
    if ps:
        chosen = None
        lang = ""
        for wanted in ("en", "de", "fr"):
            for p in ps:
                if (p.get(XML_LANG) or "").lower() == wanted:
                    chosen = p
                    lang = wanted
                    break
            if chosen is not None:
                break
        if chosen is None:
            chosen = ps[0]
            lang = (chosen.get(XML_LANG) or "").lower()
        ods = [x for x in chosen.xpath(".//*[local-name()='origDate']") if date_attrs(x)]
        return ods, lang

    ods = [x for x in origin.xpath(".//*[local-name()='origDate']") if date_attrs(x)]
    return ods, ""


def parse_revisions(root):
    rows = []
    changes = root.xpath(
        "//*[local-name()='revisionDesc']//*[local-name()='change']"
    )
    for x in changes:
        rows.append({
            "when": x.get("when") or x.get("when-iso"),
            "who": x.get("who"),
            "text": norm_text(" ".join(x.itertext())),
            "attrs": dict(x.attrib),
        })
    return rows


def choose_neutral_runtime(revisions):
    rows = []
    for r in revisions:
        blob = " ".join(f"{k}={v}" for k, v in sorted(r["attrs"].items()))
        if not r["text"] or not MAINT_RE.search(r["text"]):
            continue
        if TEMPORAL_RE.search(r["text"]) or TEMPORAL_RE.search(blob):
            continue
        key = sha256(canonical({
            "when": r["when"],
            "who": r["who"],
            "text": r["text"],
            "attrs": sorted(r["attrs"].items()),
        }))
        rows.append({**r, "event_key": key, "event_class": "NON_TEMPORAL_MAINTENANCE"})
    rows.sort(key=lambda r: ((r["when"] or ""), r["text"], r["event_key"]))
    return rows[0] if rows else None


def parse_document(path: str, raw: bytes, fault: str | None = None):
    parser = LET.XMLParser(resolve_entities=False, no_network=True, recover=False)
    root = LET.fromstring(raw, parser)
    tree = root.getroottree()

    primary = choose_primary_letter(root)
    primary_sig = boundary_signature(primary)

    claims = []
    docs = root.xpath("//*[local-name()='msContents']//*[local-name()='docDate']")
    docs = [x for x in docs if date_attrs(x)]
    for i, x in enumerate(docs, 1):
        claims.append(
            make_claim(path, "docDate", i, x, tree, contract_locator("msContents_docDate", i))
        )

    sent = root.xpath(
        "//*[local-name()='correspAction' and @type='sent']//*[local-name()='date']"
    )
    sent = [x for x in sent if date_attrs(x)]
    for i, x in enumerate(sent, 1):
        claims.append(
            make_claim(path, "sent", i, x, tree, contract_locator("correspAction_sent_date", i))
        )

    datelines = []
    if primary is not None:
        datelines = primary.xpath(
            ".//*[local-name()='opener' or local-name()='dateline']"
            "//*[local-name()='date' and not(ancestor::*[local-name()='div' and @type='annex'])]"
        )
        datelines = [x for x in datelines if date_attrs(x)]
    for i, x in enumerate(datelines, 1):
        claims.append(
            make_claim(
                path, "dateline", i, x, tree,
                contract_locator("primary_letter_dateline_date", i)
            )
        )

    annex_claims = []
    annex_dates = root.xpath(
        "//*[local-name()='div' and @type='annex']//*[local-name()='date']"
    )
    annex_dates = [x for x in annex_dates if date_attrs(x)]
    for i, x in enumerate(annex_dates, 1):
        annex_claims.append(
            make_claim(path, "annex_date", i, x, tree, contract_locator("annex_date", i))
        )

    if fault == "annex_contamination" and annex_claims:
        claims.append(copy.deepcopy(annex_claims[0]))

    origin_els, lang = choose_origin(root)
    origin_claim = None
    origin_handle = None
    origin_contract_status = "NO_ORIGIN_EVIDENCE"
    origin_element_count = len(origin_els)
    if origin_element_count == 1:
        od = origin_els[0]
        origin_claim = make_claim(
            path, "origDate", 1, od, tree,
            contract_locator("history_origin_origDate", 1, lang or "none")
        )
        handle_material = {
            "document": path,
            "source_commit": UPSTREAM_COMMIT,
            "locator_contract": origin_claim["source_locator_contract"],
            "xpath": origin_claim["source_locator_xpath"],
        }
        origin_handle = {
            "handle_id": sha256(canonical(handle_material)),
            "target_document": path,
            "source_commit": UPSTREAM_COMMIT,
            "source_file": path,
            "source_locator_contract": origin_claim["source_locator_contract"],
            "source_locator_xpath": origin_claim["source_locator_xpath"],
        }
        origin_contract_status = "SINGLE_ORIGIN_ADMISSIBLE"
    elif origin_element_count > 1:
        origin_contract_status = "COMPOSITE_ORIGIN_UNRESOLVED"

    revisions = parse_revisions(root)
    natural_neutral_diagnostic = choose_neutral_runtime(revisions)
    neutral = copy.deepcopy(CONTROL_NULL_EVENT)

    is_correspondence = bool(
        root.xpath("//*[local-name()='correspDesc']")
        and root.xpath("//*[local-name()='correspAction']")
    )

    refs = sorted(set(
        x for x in root.xpath("//@target | //@ref | //@corresp")
        if isinstance(x, str)
    ))
    facs = sorted(set(x for x in root.xpath("//@facs") if isinstance(x, str)))

    has_annex = bool(root.xpath("//*[local-name()='div' and @type='annex']"))

    if fault == "wrong_boundary":
        wrong = root.xpath(
            "//*[local-name()='div' and @type='annex']"
            "//*[local-name()='div' and @type='letter']"
        )
        if wrong:
            primary_sig = boundary_signature(wrong[0])
        elif has_annex:
            primary_sig = sha256(b"forced-wrong-boundary")
        else:
            primary_sig = sha256((primary_sig or "none").encode("utf-8") + b"-wrong")

    return {
        "path": path,
        "source_sha256": sha256(raw),
        "is_correspondence": is_correspondence,
        "primary_boundary_signature": primary_sig,
        "claims": claims,
        "annex_claims": annex_claims,
        "origin_claim": origin_claim,
        "origin_handle": origin_handle,
        "origin_contract_status": origin_contract_status,
        "origin_element_count": origin_element_count,
        "neutral_event": neutral,
        "natural_neutral_revision_diagnostic": natural_neutral_diagnostic,
        "refs": refs,
        "facs": facs,
        "has_annex": has_annex,
    }


def runtime_eligibility(claims):
    d1_pairs = []
    d2_pairs = []
    usable = [c for c in claims if c.get("_bounds")]
    for i, a in enumerate(usable):
        for j in range(i + 1, len(usable)):
            b = usable[j]
            if is_disjoint(a["_bounds"], b["_bounds"]):
                d1_pairs.append((a.get("claim_key"), b.get("claim_key")))
            elif (
                (a.get("uncertain") or b.get("uncertain"))
                and overlaps_but_diff(a["_bounds"], b["_bounds"])
            ):
                d2_pairs.append((a.get("claim_key"), b.get("claim_key")))
    trigger = "D1" if d1_pairs else "D2" if d2_pairs else None
    pairs = d1_pairs if d1_pairs else d2_pairs
    keys = sorted(set(k for p in pairs for k in p if k))
    return {"trigger": trigger, "live_claim_keys": keys}


def runtime_warrant(claims):
    usable = [c for c in claims if c.get("_bounds")]
    orig = next((c for c in usable if c.get("role") == "origDate"), None)
    roots = [c for c in usable if c is not orig]

    if orig is not None:
        dis = [c for c in roots if is_disjoint(orig["_bounds"], c["_bounds"])]
        if dis:
            alts = [orig] + dis
            return {
                "type": "ALTERNATIVE_SET",
                "alternatives": [
                    {
                        "claim_key": c.get("claim_key"),
                        "role": c.get("role"),
                        "interval": c.get("interval"),
                    }
                    for c in alts
                ],
            }
        k = interval_kind(orig["_bounds"])
        if k == "POINT":
            return {"type": "EXACT", "interval": orig["interval"], "basis": [orig.get("claim_key")]}
        if k == "BOUNDED":
            return {"type": "INTERVAL", "interval": orig["interval"], "basis": [orig.get("claim_key")]}
        if k == "OPEN":
            return {"type": "OPEN_INTERVAL", "interval": orig["interval"], "basis": [orig.get("claim_key")]}

    if not usable:
        return {"type": "UNRESOLVED", "reason": "NO_MACHINE_TEMPORAL_CARRIER"}

    ib = intersection([c["_bounds"] for c in usable])
    if ib is None:
        return {
            "type": "ALTERNATIVE_SET",
            "alternatives": [
                {
                    "claim_key": c.get("claim_key"),
                    "role": c.get("role"),
                    "interval": c.get("interval"),
                }
                for c in usable
            ],
        }
    if ib[0] == ib[1] and ib[0] not in (date.min, date.max):
        return {
            "type": "EXACT",
            "interval": interval_json(ib),
            "basis": [c.get("claim_key") for c in usable],
        }
    if ib[0] == date.min or ib[1] == date.max:
        return {
            "type": "OPEN_INTERVAL",
            "interval": interval_json(ib),
            "basis": [c.get("claim_key") for c in usable],
        }
    return {
        "type": "INTERVAL",
        "interval": interval_json(ib),
        "basis": [c.get("claim_key") for c in usable],
    }


def runtime_q0(doc):
    sent = [c for c in doc["claims"] if c.get("role") == "sent" and c.get("_bounds")]
    if sent:
        return {"source": "sent", "intervals": [c["interval"] for c in sent]}
    if doc.get("origin_claim") and doc["origin_claim"].get("_bounds"):
        return {"source": "origDate", "intervals": [doc["origin_claim"]["interval"]]}
    return {"source": "none", "intervals": []}


def public_claim(c):
    return {k: v for k, v in c.items() if k != "_bounds"}


def live_keys_from_warrant(w):
    if w.get("type") == "ALTERNATIVE_SET":
        return sorted(
            x.get("claim_key")
            for x in w.get("alternatives", [])
            if x.get("claim_key")
        )
    return sorted(k for k in w.get("basis", []) if k)


def discover(claims):
    e = runtime_eligibility(claims)
    if not e["trigger"]:
        return None
    return {
        "type": "TEMPORAL_WARRANT_QUERY",
        "trigger": e["trigger"],
        "disputed_claim_keys": e["live_claim_keys"],
    }


def make_interface(doc, arm):
    q0 = runtime_q0(doc)

    if arm in ("I_NATIVE", "I_RSTAR", "I_NO_HISTORY"):
        claims = copy.deepcopy(doc["claims"])
        origin_handle = copy.deepcopy(doc["origin_handle"])
    elif arm == "I_NO_ALTERNATIVES":
        qsource = q0["source"]
        if qsource == "sent":
            claims = [copy.deepcopy(c) for c in doc["claims"] if c.get("role") == "sent"]
        else:
            claims = []
        origin_handle = copy.deepcopy(doc["origin_handle"])
    elif arm == "I_NO_BINDING":
        claims = []
        for c in doc["claims"]:
            x = copy.deepcopy(c)
            x["role"] = "unbound"
            x["source_file"] = None
            x["source_locator_contract"] = None
            x["source_locator_xpath"] = None
            x["claim_key"] = None
            claims.append(x)
        origin_handle = None
    else:
        raise ValueError(arm)

    root_warrant = runtime_warrant(claims)
    state = {
        "document": doc["path"],
        "source_commit": UPSTREAM_COMMIT,
        "q0": q0,
        "claims": {c.get("claim_key") or f"unbound:{i}": c for i, c in enumerate(claims, 1)},
        "current_warrant": root_warrant,
        "live_claim_keys": live_keys_from_warrant(root_warrant),
        "evidence_ledger": [],
        "event_ledger": [],
        "transition_ledger": [],
        "origin_handle": origin_handle,
        "history_retained": arm != "I_NO_HISTORY",
        "interface_arm": arm,
    }
    payload = {
        "document": doc["path"],
        "source_commit": UPSTREAM_COMMIT,
        "q0": q0,
        "claims": [public_claim(c) for c in claims],
        "origin_handle": (
            None if origin_handle is None else {
                "handle_id": origin_handle["handle_id"],
                "target_document": origin_handle["target_document"],
                "source_commit": origin_handle["source_commit"],
                "source_file": origin_handle["source_file"],
                "source_locator_contract": origin_handle["source_locator_contract"],
            }
        ),
        "history_retained": state["history_retained"],
    }
    return state, payload


def temporal_state_view(state):
    claims = {}
    for key, c in state["claims"].items():
        claims[key] = {
            "claim_key": c.get("claim_key"),
            "role": c.get("role"),
            "interval": c.get("interval"),
            "status": c.get("status"),
            "uncertain": c.get("uncertain"),
            "source_file": c.get("source_file"),
            "source_locator_contract": c.get("source_locator_contract"),
            "cert": c.get("cert"),
            "precision": c.get("precision"),
            "resp": c.get("resp"),
        }
    return {
        "document": state["document"],
        "source_commit": state["source_commit"],
        "q0": state["q0"],
        "claims": claims,
        "current_warrant": state["current_warrant"],
        "live_claim_keys": state["live_claim_keys"],
    }


def temporal_digest(state):
    return sha256(canonical(temporal_state_view(state)))


def temporal_diff(before, after):
    b = temporal_state_view(before)
    a = temporal_state_view(after)
    changed = []
    bclaims, aclaims = b["claims"], a["claims"]

    for key in sorted(set(bclaims) | set(aclaims)):
        if key not in bclaims:
            changed.append(f"claims/{key}:ADDED")
        elif key not in aclaims:
            changed.append(f"claims/{key}:REMOVED")
        elif bclaims[key] != aclaims[key]:
            changed.append(f"claims/{key}:CHANGED")

    if b["current_warrant"] != a["current_warrant"]:
        changed.append("current_warrant")
    if b["live_claim_keys"] != a["live_claim_keys"]:
        changed.append("live_claim_keys")
    if b["q0"] != a["q0"]:
        changed.append("q0")
    return changed


def collateral_paths(before, after, allowed_added_key=None):
    b = temporal_state_view(before)
    a = temporal_state_view(after)
    paths = []
    for key, old in b["claims"].items():
        if key not in a["claims"]:
            paths.append(f"claims/{key}:REMOVED")
        elif a["claims"][key] != old:
            paths.append(f"claims/{key}:CHANGED")
    # additions other than the event-declared origin target are collateral.
    for key in a["claims"]:
        if key not in b["claims"] and key != allowed_added_key:
            paths.append(f"claims/{key}:UNDECLARED_ADDITION")
    if b["q0"] != a["q0"]:
        paths.append("q0")
    return paths


def apply_open_origin(state, doc, question, fault=None):
    before = copy.deepcopy(state)
    handle = copy.deepcopy(state.get("origin_handle"))
    origin = copy.deepcopy(doc.get("origin_claim"))
    event_id = f"OPEN_ORIGIN::{state['document']}"

    if fault and fault.get("type") == "wrong_origin_binding" and handle is not None:
        handle["target_document"] = "WRONG_DOCUMENT"

    applicable = bool(
        question
        and handle
        and origin
        and handle.get("target_document") == state["document"]
        and handle.get("source_commit") == state["source_commit"]
        and handle.get("source_file") == state["document"]
        and handle.get("source_locator_contract") == origin.get("source_locator_contract")
    )

    evidence_key = None
    if applicable:
        evidence_key = origin["claim_key"]
        state["claims"][evidence_key] = origin
        state["evidence_ledger"].append({
            "event_id": event_id,
            "evidence_key": evidence_key,
            "source_file": origin["source_file"],
            "source_locator_contract": origin["source_locator_contract"],
            "source_locator_xpath": origin["source_locator_xpath"],
        })
        state["event_ledger"].append({
            "event_id": event_id,
            "event_class": "EVIDENCE_RELEASE",
            "target_document": state["document"],
            "applicable": True,
        })

        if fault and fault.get("type") == "collateral_mutation":
            root_keys = [k for k in before["claims"]]
            if root_keys:
                k = root_keys[0]
                state["claims"][k]["status"] = "FAULT_MUTATED"

        state["current_warrant"] = runtime_warrant(list(state["claims"].values()))
        if fault and fault.get("type") == "wrong_warrant":
            state["current_warrant"] = {
                "type": "UNRESOLVED",
                "reason": "FAULT_INJECTED_WRONG_WARRANT",
            }
        state["live_claim_keys"] = live_keys_from_warrant(state["current_warrant"])

        if fault and fault.get("type") == "drop_live_key":
            key = fault.get("claim_key")
            state["live_claim_keys"] = [x for x in state["live_claim_keys"] if x != key]
    else:
        state["event_ledger"].append({
            "event_id": event_id,
            "event_class": "EVIDENCE_RELEASE",
            "target_document": state["document"],
            "applicable": False,
        })

    changed = temporal_diff(before, state)
    collateral = collateral_paths(before, state, allowed_added_key=evidence_key)
    transition = {
        "event_id": event_id,
        "event_class": "OPEN_ORIGIN",
        "target_document": state["document"],
        "applicable": applicable,
        "evidence_key": evidence_key,
        "before_warrant": before["current_warrant"],
        "after_warrant": state["current_warrant"],
        "before_temporal_digest": temporal_digest(before),
        "after_temporal_digest": temporal_digest(state),
        "changed_paths": changed,
        "collateral_temporal_paths": collateral,
    }
    state["transition_ledger"].append(copy.deepcopy(transition))
    return state, transition


def apply_neutral_event(state, neutral_event, fault=None):
    before = copy.deepcopy(state)
    if neutral_event is None:
        return state, None, False

    event = {
        "event_id": neutral_event.get("event_id") or f"NEUTRAL::{neutral_event['event_key']}",
        "event_key": neutral_event["event_key"],
        "event_class": "NON_TEMPORAL_MAINTENANCE",
        "target_document": state["document"],
        "text": neutral_event["text"],
        "when": neutral_event["when"],
    }
    state["event_ledger"].append(copy.deepcopy(event))

    if fault and fault.get("type") == "neutral_mutation":
        state["current_warrant"] = {
            "type": "UNRESOLVED",
            "reason": "FAULT_INJECTED_NULL_MUTATION",
        }
        state["live_claim_keys"] = live_keys_from_warrant(state["current_warrant"])

    changed = temporal_diff(before, state)
    transition = {
        "event_id": event["event_id"],
        "event_class": "NON_TEMPORAL_MAINTENANCE",
        "target_document": state["document"],
        "before_warrant": before["current_warrant"],
        "after_warrant": state["current_warrant"],
        "before_temporal_digest": temporal_digest(before),
        "after_temporal_digest": temporal_digest(state),
        "changed_paths": changed,
        "collateral_temporal_paths": collateral_paths(before, state),
    }
    state["transition_ledger"].append(copy.deepcopy(transition))
    null_stable = len(changed) == 0
    return state, transition, null_stable


def delayed_audit(state):
    origin_transition = next(
        (x for x in state["transition_ledger"] if x.get("event_class") == "OPEN_ORIGIN"),
        None,
    )
    evidence = next(
        (x for x in state["evidence_ledger"] if x.get("event_id", "").startswith("OPEN_ORIGIN::")),
        None,
    )
    neutral = next(
        (x for x in state["event_ledger"] if x.get("event_class") == "NON_TEMPORAL_MAINTENANCE"),
        None,
    )
    return {
        "document": state["document"],
        "current_warrant": state["current_warrant"],
        "live_claim_keys": sorted(state["live_claim_keys"]),
        "origin_event_id": origin_transition.get("event_id") if origin_transition else None,
        "origin_evidence_key": evidence.get("evidence_key") if evidence else None,
        "origin_before_warrant": origin_transition.get("before_warrant") if origin_transition else None,
        "origin_after_warrant": origin_transition.get("after_warrant") if origin_transition else None,
        "origin_changed_paths": origin_transition.get("changed_paths") if origin_transition else None,
        "origin_collateral_temporal_paths": origin_transition.get("collateral_temporal_paths") if origin_transition else None,
        "neutral_event_key": neutral.get("event_key") if neutral else None,
    }


def execute(doc, arm, fault=None):
    state, payload = make_interface(doc, arm)
    q = discover(list(state["claims"].values()))
    before_open = copy.deepcopy(state)

    state, origin_transition = apply_open_origin(state, doc, q, fault=fault)
    post_origin_state = copy.deepcopy(state)

    neutral_fault = fault if fault and fault.get("type") == "neutral_mutation" else None
    state, neutral_transition, null_stable = apply_neutral_event(
        state, doc.get("neutral_event"), fault=neutral_fault
    )

    if arm == "I_NO_HISTORY" or (fault and fault.get("type") == "drop_history"):
        state["transition_ledger"] = []

    audit = delayed_audit(state)

    return {
        "arm": arm,
        "payload": payload,
        "payload_bytes": len(canonical(payload)),
        "q0": payload["q0"],
        "question": q,
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
        "before_open_temporal_digest": temporal_digest(before_open),
        "post_open_temporal_digest": temporal_digest(post_origin_state),
        "final_temporal_digest": temporal_digest(state),
    }
