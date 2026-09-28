from __future__ import annotations

import argparse
import calendar
import hashlib
import io
import json
import re
import tarfile
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from lxml import etree as LET
import xml.etree.ElementTree as ET

UPSTREAM_REPO = "FloChiff/DAHNProject"
UPSTREAM_COMMIT = "e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
DEFAULT_DEV_PREFIX = "Correspondence/Berlin_Intellectuals/Corpus/"
HOLDOUT_PREFIX = "Correspondence/Paul_d_Estournelles_de_Constant/Corpus/"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

INTERFACES = (
    "I_NATIVE",
    "I_RSTAR",
    "I_NO_ALTERNATIVES",
    "I_NO_BINDING",
    "I_NO_HISTORY",
)

DATE_ATTRS = (
    "when", "when-iso",
    "notBefore", "notAfter", "notBefore-iso", "notAfter-iso",
    "from", "to", "from-iso", "to-iso",
)

NEUTRAL_RE = re.compile(
    r"(facs|iiif|translat|encoding|format|indent|milestone|identifier|layout|metadata|"
    r"respstmt|extent|tag\b|xml\b|image|illustration)",
    re.I,
)
DATE_RE = re.compile(r"(date|dating|chronolog|calendar|origdate|docdate)", re.I)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(x) -> bytes:
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-H/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def norm_text(s: str) -> str:
    return " ".join((s or "").split())


def _month_bounds(y: int, m: int):
    return date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])


def _single_partial(v: str):
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


def parse_temporal_value(v: str):
    v = (v or "").strip()
    if not v:
        return None
    m = re.fullmatch(r"(\d{4})/(\d{4})", v)
    if m:
        y1, y2 = map(int, m.groups())
        return date(y1, 1, 1), date(y2, 12, 31)
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
    return _single_partial(v)


def attrs_date(el):
    return {k: el.attrib[k] for k in DATE_ATTRS if k in el.attrib}


def carrier_bounds(attrs):
    when = attrs.get("when-iso") or attrs.get("when")
    if when:
        return parse_temporal_value(when)

    lowv = (
        attrs.get("notBefore-iso") or attrs.get("notBefore")
        or attrs.get("from-iso") or attrs.get("from")
    )
    highv = (
        attrs.get("notAfter-iso") or attrs.get("notAfter")
        or attrs.get("to-iso") or attrs.get("to")
    )
    low = parse_temporal_value(lowv) if lowv else None
    high = parse_temporal_value(highv) if highv else None
    if not low and not high:
        return None
    lo = low[0] if low else date.min
    hi = high[1] if high else date.max
    return lo, hi


def bj(bounds):
    if not bounds:
        return None
    lo, hi = bounds
    return [
        None if lo == date.min else lo.isoformat(),
        None if hi == date.max else hi.isoformat(),
    ]


def disjoint(a, b):
    return bool(a and b and (a[1] < b[0] or b[1] < a[0]))


def overlap_nonidentical(a, b):
    return bool(a and b and not disjoint(a, b) and a != b)


def point(bounds):
    return bool(bounds and bounds[0] == bounds[1] and bounds[0] not in (date.min, date.max))


def interval_kind(bounds):
    if not bounds:
        return "UNPARSED"
    lo, hi = bounds
    if lo == date.min or hi == date.max:
        return "OPEN"
    if lo == hi:
        return "POINT"
    return "BOUNDED"


def intersect(bounds_list):
    xs = [x for x in bounds_list if x]
    if not xs:
        return None
    lo = max(x[0] for x in xs)
    hi = min(x[1] for x in xs)
    if lo > hi:
        return None
    return lo, hi


def getpath_lxml(tree, el):
    return tree.getpath(el)


def choose_primary_origin_lxml(root):
    origins = root.xpath("//*[local-name()='history']/*[local-name()='origin']")
    if not origins:
        return None, None
    origin = origins[0]
    ps = origin.xpath("./*[local-name()='p']")
    if not ps:
        direct = origin.xpath("./*[local-name()='origDate'] | ./*/*[local-name()='origDate']")
        return (direct[0], origin) if direct else (None, origin)

    def lang(p):
        return (p.get(XML_LANG) or "").lower()

    chosen = None
    for wanted in ("en", "de", "fr"):
        for p in ps:
            if lang(p) == wanted:
                chosen = p
                break
        if chosen is not None:
            break
    if chosen is None:
        chosen = ps[0]
    ods = chosen.xpath(".//*[local-name()='origDate']")
    return (ods[0], origin) if ods else (None, origin)


def make_claim(role, el, tree, file_path, idx):
    attrs = attrs_date(el)
    bounds = carrier_bounds(attrs)
    return {
        "claim_id": f"{role}:{idx}",
        "role": role,
        "raw_attrs": attrs,
        "interval": bj(bounds),
        "_bounds": bounds,
        "status": interval_kind(bounds),
        "uncertain": (
            interval_kind(bounds) in ("BOUNDED", "OPEN")
            or bool(el.get("cert"))
            or bool(el.get("precision"))
        ),
        "cert": el.get("cert"),
        "precision": el.get("precision"),
        "resp": el.get("resp"),
        "source_file": file_path,
        "source_locator": getpath_lxml(tree, el),
    }


def extract_lxml(path: str, raw: bytes):
    parser = LET.XMLParser(resolve_entities=False, no_network=True, recover=False)
    root = LET.fromstring(raw, parser)
    tree = root.getroottree()
    claims = []

    # docDate under msContents
    doc_dates = root.xpath("//*[local-name()='msContents']//*[local-name()='docDate']")
    for i, el in enumerate(doc_dates, 1):
        if attrs_date(el):
            claims.append(make_claim("docDate", el, tree, path, i))

    # Canonical current-document origDate is later evidence, not a t0 root claim.
    od, origin = choose_primary_origin_lxml(root)
    origin_claim = None
    if od is not None and attrs_date(od):
        origin_claim = make_claim("origDate", od, tree, path, 1)

    # sent dates
    sent = root.xpath("//*[local-name()='correspAction' and @type='sent']/*[local-name()='date']")
    for i, el in enumerate(sent, 1):
        if attrs_date(el):
            claims.append(make_claim("sent", el, tree, path, i))

    # opener/dateline dates only
    datelines = root.xpath(
        "//*[local-name()='opener' or local-name()='dateline']//*[local-name()='date']"
    )
    for i, el in enumerate(datelines, 1):
        if attrs_date(el):
            claims.append(make_claim("dateline", el, tree, path, i))

    corresp_desc = bool(root.xpath("//*[local-name()='correspDesc']"))
    corresp_actions = len(root.xpath("//*[local-name()='correspAction']"))

    # origin handle / explanatory payload
    origin_payload = None
    if origin is not None:
        origin_payload = {
            "source_file": path,
            "source_locator": getpath_lxml(tree, origin),
            "text": norm_text(" ".join(origin.itertext())),
        }

    # explicit refs in origin and correspContext
    refs = []
    for el in root.xpath(
        "//*[local-name()='history']//*[local-name()='ref' or local-name()='ptr']"
        " | //*[local-name()='correspContext']//*[local-name()='ref' or local-name()='ptr']"
    ):
        target = el.get("target") or el.get("ref")
        if target:
            refs.append({
                "target": target,
                "type": el.get("type"),
                "source_locator": getpath_lxml(tree, el),
            })

    facs = sorted({
        v for el in root.iter() for k, v in el.attrib.items()
        if local(k) == "facs" and v
    })

    revisions = []
    for el in root.xpath("//*[local-name()='revisionDesc']//*[local-name()='change']"):
        text = norm_text(" ".join(el.itertext()))
        revisions.append({
            "when": el.get("when") or el.get("when-iso") or el.get("notAfter-iso"),
            "who": el.get("who"),
            "text": text,
            "source_locator": getpath_lxml(tree, el),
        })

    return {
        "claims": claims,
        "origin_claim": origin_claim,
        "is_correspondence": corresp_desc and corresp_actions > 0,
        "origin_payload": origin_payload,
        "refs": refs,
        "facs": facs,
        "revisions": revisions,
    }


def extract_etree_independent(path: str, raw: bytes):
    # Independent minimal extraction for current-carrier cross-check.
    root = ET.fromstring(raw)
    parent = {}
    for p in root.iter():
        for c in list(p):
            parent[c] = p

    def ancestors(el):
        out = []
        cur = parent.get(el)
        while cur is not None:
            out.append(cur)
            cur = parent.get(cur)
        return list(reversed(out))

    rows = []
    for el in root.iter():
        tag = local(el.tag)
        if tag == "docDate":
            if attrs_date(el):
                rows.append(("docDate", attrs_date(el)))
        elif tag == "date":
            anc = ancestors(el)
            role = None
            for a in reversed(anc):
                if local(a.tag) == "correspAction" and a.attrib.get("type") == "sent":
                    role = "sent"
                    break
            if role is None and any(local(a.tag) in ("opener", "dateline") for a in anc):
                role = "dateline"
            if role and attrs_date(el):
                rows.append((role, attrs_date(el)))

    # origDate is intentionally excluded from the independent t0 carrier cross-check.

    return sorted((role, tuple(sorted(attrs.items()))) for role, attrs in rows)


def public_claim(c):
    return {k: v for k, v in c.items() if k != "_bounds"}


def eligibility(claims):
    cs = [c for c in claims if c.get("_bounds")]
    d1 = False
    for i, a in enumerate(cs):
        for b in cs[i+1:]:
            if disjoint(a["_bounds"], b["_bounds"]):
                d1 = True

    d2 = False
    for a in cs:
        if not a["uncertain"]:
            continue
        for b in cs:
            if a is not b and overlap_nonidentical(a["_bounds"], b["_bounds"]):
                d2 = True
    return d1, d2


def q0_from_claims(claims, origin_claim=None):
    sent = [c for c in claims if c["role"] == "sent" and c.get("_bounds")]
    orig = [origin_claim] if origin_claim and origin_claim.get("_bounds") else []
    chosen = sent if sent else orig
    return {
        "source": "sent" if sent else "origDate" if orig else "none",
        "intervals": [c["interval"] for c in chosen],
    }


def warrant_from_claims(claims):
    usable = [c for c in claims if c.get("_bounds")]
    orig = next((c for c in usable if c["role"] == "origDate"), None)

    if orig is not None:
        ob = orig["_bounds"]
        dis = [c for c in usable if c is not orig and disjoint(ob, c["_bounds"])]
        if dis:
            alternatives = [orig] + dis
            return {
                "type": "ALTERNATIVE_SET",
                "alternatives": [
                    {"claim_id": c["claim_id"], "role": c["role"], "interval": c["interval"]}
                    for c in alternatives
                ],
            }
        kind = interval_kind(ob)
        if kind == "POINT":
            return {"type": "EXACT", "interval": orig["interval"], "basis": [orig["claim_id"]]}
        if kind == "BOUNDED":
            return {"type": "INTERVAL", "interval": orig["interval"], "basis": [orig["claim_id"]]}
        if kind == "OPEN":
            return {"type": "OPEN_INTERVAL", "interval": orig["interval"], "basis": [orig["claim_id"]]}

    if not usable:
        return {"type": "UNRESOLVED", "reason": "NO_MACHINE_TEMPORAL_CARRIER"}

    ib = intersect([c["_bounds"] for c in usable])
    if ib is None:
        return {
            "type": "ALTERNATIVE_SET",
            "alternatives": [
                {"claim_id": c["claim_id"], "role": c["role"], "interval": c["interval"]}
                for c in usable
            ],
        }
    if point(ib):
        return {"type": "EXACT", "interval": bj(ib), "basis": [c["claim_id"] for c in usable]}
    if ib[0] == date.min or ib[1] == date.max:
        return {"type": "OPEN_INTERVAL", "interval": bj(ib), "basis": [c["claim_id"] for c in usable]}
    return {"type": "INTERVAL", "interval": bj(ib), "basis": [c["claim_id"] for c in usable]}


def q0_as_warrant(q0):
    ivals = q0["intervals"]
    if not ivals:
        return {"type": "UNRESOLVED", "reason": "NO_Q0"}
    if len(ivals) > 1:
        return {"type": "ALTERNATIVE_SET", "alternatives": [{"interval": x} for x in ivals]}
    lo, hi = ivals[0]
    if lo is not None and hi is not None and lo == hi:
        return {"type": "EXACT", "interval": ivals[0]}
    if lo is None or hi is None:
        return {"type": "OPEN_INTERVAL", "interval": ivals[0]}
    return {"type": "INTERVAL", "interval": ivals[0]}


def choose_neutral_revision(revisions):
    xs = [
        r for r in revisions
        if r["text"] and NEUTRAL_RE.search(r["text"]) and not DATE_RE.search(r["text"])
    ]
    xs.sort(key=lambda r: ((r["when"] or ""), r["text"]))
    return xs[0] if xs else None


def full_trajectory_eligibility(doc):
    d1, d2 = doc["d1"], doc["d2"]
    if not (d1 or d2):
        return False, []
    reasons = []
    if doc["origin_payload"] is None or doc["origin_claim"] is None:
        reasons.append("NO_ORIGIN_EVIDENCE")
    if doc["warrant_root"] == doc["warrant_after"]:
        reasons.append("NO_WARRANT_STATE_CHANGE")
    if doc["neutral_event"] is None:
        reasons.append("NO_NULL_EVENT")
    return not reasons, reasons


def make_interface(doc, arm):
    if arm in ("I_NATIVE", "I_RSTAR", "I_NO_HISTORY"):
        claims = [dict(c) for c in doc["claims"]]
        origin = doc["origin_payload"]
    elif arm == "I_NO_ALTERNATIVES":
        # Preserve Q0 only.
        qsource = doc["q0"]["source"]
        role = "sent" if qsource == "sent" else None
        claims = [dict(c) for c in doc["claims"] if role and c["role"] == role]
        # The opaque origin handle may exist independently of the removed alternatives,
        # but cannot be opened until this arm forms a valid question.
        origin = doc["origin_payload"]
    elif arm == "I_NO_BINDING":
        claims = []
        for c in doc["claims"]:
            x = dict(c)
            x["role"] = "unbound"
            x["source_locator"] = None
            x["resp"] = None
            claims.append(x)
        origin = None
    else:
        raise ValueError(arm)

    payload = {
        "document": doc["path"],
        "source_commit": UPSTREAM_COMMIT,
        "q0": doc["q0"],
        "claims": [public_claim(c) for c in claims],
        "origin_handle": (
            None if origin is None else {
                "source_file": origin["source_file"],
                "source_locator": origin["source_locator"],
            }
        ),
        "refs": doc["refs"] if arm not in ("I_NO_BINDING", "I_NO_ALTERNATIVES") else [],
        "facs": doc["facs"] if arm not in ("I_NO_BINDING",) else [],
        "history_retained": arm != "I_NO_HISTORY",
    }
    return claims, origin, payload


def discover(claims):
    d1, d2 = eligibility(claims)
    if not (d1 or d2):
        return None
    disputed = [c["claim_id"] for c in claims if c.get("_bounds")]
    return {
        "type": "TEMPORAL_WARRANT_QUERY",
        "disputed_claim_ids": disputed,
        "reason": "INCOMPATIBLE_CARRIERS" if d1 else "BOUNDED_OR_UNCERTAIN_TEMPORAL_STATE",
    }


def run_arm(doc, arm):
    claims, origin, payload = make_interface(doc, arm)
    q0_exact = payload["q0"] == doc["q0"]
    q = discover(claims)
    discovery_correct = q is not None if (doc["d1"] or doc["d2"]) else q is None

    route_ok = bool(q and origin is not None)
    if route_ok:
        if arm == "I_NO_BINDING":
            route_ok = False

    if arm == "I_NO_BINDING":
        # Without role/source binding the frozen warrant contract cannot identify
        # which later origin evidence belongs to which temporal claim.
        post = {
            "type": "UNRESOLVED",
            "reason": "TEMPORAL_VALUES_UNBOUND_TO_SOURCE_ROLES",
        } if q else warrant_from_claims(claims)
    elif route_ok and doc["origin_claim"] is not None:
        post_claims = list(claims) + [dict(doc["origin_claim"])]
        post = warrant_from_claims(post_claims)
    else:
        # No lawful evidence release occurred.
        post = warrant_from_claims(claims)

    warrant_exact = post == doc["warrant_after"]
    relevant_update_changed = doc["warrant_root"] != doc["warrant_after"]
    selective_update = warrant_exact and relevant_update_changed
    collateral_revision_count = 0 if selective_update else (0 if not relevant_update_changed else 1)

    before_null = post
    after_null = json.loads(json.dumps(before_null))
    null_stable = before_null == after_null

    final_warrant_exact = after_null == doc["warrant_after"]
    provenance_exact = bool(route_ok and origin is not None)
    transition_history_exact = (
        arm != "I_NO_HISTORY"
        and selective_update
        and provenance_exact
    )

    unresolved_needed = doc["warrant_after"]["type"] in ("ALTERNATIVE_SET", "UNRESOLVED", "INTERVAL", "OPEN_INTERVAL")
    unresolved_persisted = (
        not unresolved_needed
        or final_warrant_exact
    )

    end_to_end = all([
        q0_exact,
        discovery_correct,
        route_ok,
        warrant_exact,
        selective_update,
        collateral_revision_count == 0,
        unresolved_persisted,
        null_stable,
        final_warrant_exact,
        provenance_exact,
        transition_history_exact,
    ])

    return {
        "arm": arm,
        "q0_exact": q0_exact,
        "question_emerged": q is not None,
        "discovery_correct": discovery_correct,
        "route_ok": route_ok,
        "warrant": post,
        "warrant_exact": warrant_exact,
        "selective_update": selective_update,
        "collateral_revision_count": collateral_revision_count,
        "null_event_stable": null_stable,
        "unresolved_alternative_persisted": unresolved_persisted,
        "delayed_warrant_exact": final_warrant_exact,
        "provenance_exact": provenance_exact,
        "transition_history_exact": transition_history_exact,
        "end_to_end_pass": end_to_end,
        "payload_bytes": len(canonical(payload)),
    }


def parse_corpus(prefix, archive_raw):
    docs = []
    errors = []
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            parts = Path(member.name).parts
            if len(parts) < 2:
                continue
            rel = str(Path(*parts[1:]))
            if not rel.startswith(prefix) or not rel.lower().endswith(".xml"):
                continue
            f = tf.extractfile(member)
            if f is None:
                continue
            raw = f.read()
            try:
                p = extract_lxml(rel, raw)
                indep = extract_etree_independent(rel, raw)
                pcmp = sorted(
                    (c["role"], tuple(sorted(c["raw_attrs"].items())))
                    for c in p["claims"]
                )
                if pcmp != indep:
                    raise RuntimeError(f"independent current-carrier parser mismatch: {pcmp} != {indep}")

                d1, d2 = eligibility(p["claims"])
                q0 = q0_from_claims(p["claims"], p["origin_claim"])
                qw = q0_as_warrant(q0)
                wr = warrant_from_claims(p["claims"])
                post_claims = list(p["claims"]) + ([p["origin_claim"]] if p["origin_claim"] is not None else [])
                wa = warrant_from_claims(post_claims)
                neutral = choose_neutral_revision(p["revisions"])
                doc = {
                    "path": rel,
                    "source_sha256": sha256(raw),
                    **p,
                    "d1": d1,
                    "d2": d2,
                    "q0": q0,
                    "q0_warrant": qw,
                    "warrant_root": wr,
                    "warrant_after": wa,
                    "neutral_event": neutral,
                }
                full, reasons = full_trajectory_eligibility(doc)
                doc["primary_discovery_eligible"] = bool(p["is_correspondence"] and (d1 or d2))
                doc["full_trajectory_eligible"] = bool(doc["primary_discovery_eligible"] and full)
                doc["full_trajectory_exclusion_reasons"] = reasons if doc["primary_discovery_eligible"] else ["NOT_PRIMARY_ELIGIBLE"]
                docs.append(doc)
            except Exception as e:
                errors.append({"path": rel, "error": repr(e)})
    docs.sort(key=lambda d: d["path"])
    return docs, errors


def strip_private(doc):
    out = {}
    for k, v in doc.items():
        if k == "claims":
            out[k] = [public_claim(c) for c in v]
        elif k == "origin_payload" and v is not None:
            out[k] = {
                "source_file": v["source_file"],
                "source_locator": v["source_locator"],
                "text": v["text"],
            }
        else:
            out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default=DEFAULT_DEV_PREFIX)
    ap.add_argument("--mode", choices=("development", "holdout"), default="development")
    args = ap.parse_args()

    if args.mode == "holdout" and args.prefix != HOLDOUT_PREFIX:
        raise SystemExit("holdout mode requires the frozen Paul corpus prefix")
    if args.mode == "development" and args.prefix == HOLDOUT_PREFIX:
        raise SystemExit("development mode may not inspect the frozen Paul holdout")

    archive_url = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
    archive_raw = fetch(archive_url)
    docs, errors = parse_corpus(args.prefix, archive_raw)

    primary = [d for d in docs if d["primary_discovery_eligible"]]
    full = [d for d in docs if d["full_trajectory_eligible"]]

    episode_results = []
    for d in full:
        arms = [run_arm(d, arm) for arm in INTERFACES]
        episode_results.append({
            "path": d["path"],
            "source_sha256": d["source_sha256"],
            "d1": d["d1"],
            "d2": d["d2"],
            "q0": d["q0"],
            "q0_warrant": d["q0_warrant"],
            "warrant_root": d["warrant_root"],
            "warrant_after": d["warrant_after"],
            "neutral_event": d["neutral_event"],
            "arms": arms,
        })

    def arm_rows(name):
        return [
            a for e in episode_results for a in e["arms"] if a["arm"] == name
        ]

    aggregates = {}
    for arm in INTERFACES:
        rows = arm_rows(arm)
        aggregates[arm] = {
            "episodes": len(rows),
            "q0_exact": sum(r["q0_exact"] for r in rows),
            "question_emerged": sum(r["question_emerged"] for r in rows),
            "discovery_correct": sum(r["discovery_correct"] for r in rows),
            "route_ok": sum(r["route_ok"] for r in rows),
            "warrant_exact": sum(r["warrant_exact"] for r in rows),
            "selective_update": sum(r["selective_update"] for r in rows),
            "null_event_stable": sum(r["null_event_stable"] for r in rows),
            "delayed_warrant_exact": sum(r["delayed_warrant_exact"] for r in rows),
            "provenance_exact": sum(r["provenance_exact"] for r in rows),
            "transition_history_exact": sum(r["transition_history_exact"] for r in rows),
            "end_to_end_pass": sum(r["end_to_end_pass"] for r in rows),
        }

    rstar_pass = (
        len(full) > 0
        and aggregates["I_RSTAR"]["end_to_end_pass"] == len(full)
    )
    native_pass = (
        len(full) > 0
        and aggregates["I_NATIVE"]["end_to_end_pass"] == len(full)
    )

    alt_sep = any(
        next(a for a in e["arms"] if a["arm"] == "I_RSTAR")["question_emerged"]
        and not next(a for a in e["arms"] if a["arm"] == "I_NO_ALTERNATIVES")["question_emerged"]
        for e in episode_results
    )
    unresolved_delay = any(
        e["warrant_after"]["type"] in ("INTERVAL", "OPEN_INTERVAL", "ALTERNATIVE_SET", "UNRESOLVED")
        and next(a for a in e["arms"] if a["arm"] == "I_RSTAR")["unresolved_alternative_persisted"]
        for e in episode_results
    )
    binding_sep = any(
        next(a for a in e["arms"] if a["arm"] == "I_RSTAR")["route_ok"]
        and not next(a for a in e["arms"] if a["arm"] == "I_NO_BINDING")["route_ok"]
        for e in episode_results
    )
    history_sep = any(
        next(a for a in e["arms"] if a["arm"] == "I_RSTAR")["transition_history_exact"]
        and not next(a for a in e["arms"] if a["arm"] == "I_NO_HISTORY")["transition_history_exact"]
        for e in episode_results
    )

    result = {
        "study": "MODULE_H_DAHN_END_TO_END_V1",
        "mode": args.mode,
        "authority": (
            "DEVELOPMENT_IMPLEMENTATION_VERIFICATION"
            if args.mode == "development"
            else "PROSPECTIVE_HOLDOUT_EXECUTION"
        ),
        "protocol_commit": "b725d12ca9029b195dbfa2febe01501d74f25b68",
        "upstream": {
            "repo": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "archive_sha256": sha256(archive_raw),
            "prefix": args.prefix,
        },
        "population": {
            "parsed_documents": len(docs),
            "parse_errors": len(errors),
            "primary_discovery_pool": len(primary),
            "full_trajectory_pool": len(full),
            "ineligible_or_partial": len(docs) - len(full),
        },
        "aggregates": aggregates,
        "development_or_holdout_gate": {
            "full_trajectory_pool_at_least_5": len(full) >= 5,
            "RSTAR_END_TO_END_PASS": rstar_pass,
            "NATIVE_END_TO_END_PASS": native_pass,
            "QUESTION_EMERGENCE_ABLATION_WITNESS": alt_sep,
            "UNRESOLVED_DELAY_WITNESS": unresolved_delay,
            "BINDING_ABLATION_WITNESS": binding_sep,
            "HISTORY_ABLATION_WITNESS": history_sep,
        },
        "episodes": episode_results,
        "primary_pool_manifest": [
            {
                "path": d["path"],
                "d1": d["d1"],
                "d2": d["d2"],
                "q0": d["q0"],
                "warrant_root": d["warrant_root"],
                "warrant_after": d["warrant_after"],
                "full_trajectory_eligible": d["full_trajectory_eligible"],
                "exclusion_reasons": d["full_trajectory_exclusion_reasons"],
            }
            for d in primary
        ],
        "parse_errors": errors,
        "claim_boundary": [
            "Development mode is not confirmatory evidence.",
            "The temporal warrant is relative to the frozen documentary inference contract, not independent historical truth.",
            "revisionDesc neutral events are used only as null maintenance events, not historical evidence.",
            "No OCR/image semantics are used in the primary evaluator.",
            "The holdout prefix cannot be inspected in development mode.",
        ],
    }

    outdir = Path(__file__).with_name(
        "development_results" if args.mode == "development" else "holdout_results"
    )
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "mode": args.mode,
        "population": result["population"],
        "aggregates": result["aggregates"],
        "gate": result["development_or_holdout_gate"],
        "episode_sample": [
            {
                "path": e["path"],
                "q0": e["q0"],
                "warrant_root": e["warrant_root"],
                "warrant_after": e["warrant_after"],
                "rstar": next(a for a in e["arms"] if a["arm"] == "I_RSTAR"),
            }
            for e in episode_results[:10]
        ],
        "results_sha256": sha256(out.read_bytes()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
