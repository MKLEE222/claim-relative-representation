from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANDING = HERE / "VGW_LANDING_METADATA_ANCHORS_v1.json"
HEADS = HERE / "VGW_HEAD_METADATA_ANCHORS_v1.json"
DIST = HERE / "VGW_DISTRIBUTION_METADATA_ANCHORS_v1.json"

MAX_BYTES = 10000


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def headers_dict(resp):
    return {k.lower(): v for k, v in resp.headers.items()}


def local_key(key: str) -> str:
    s = str(key)
    for sep in ("#", "/", ":"):
        if sep in s:
            s = s.rsplit(sep, 1)[-1]
    return s.lower()


def walk_key_values(node, wanted):
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            if local_key(k) == wanted:
                out.append(v)
            out.extend(walk_key_values(v, wanted))
    elif isinstance(node, list):
        for x in node:
            out.extend(walk_key_values(x, wanted))
    return out


def scalar_values(items):
    out = []
    for x in items:
        if isinstance(x, (str, int, float, bool)) or x is None:
            out.append(x)
        elif isinstance(x, dict):
            if "@value" in x:
                out.append(x["@value"])
            elif "value" in x:
                out.append(x["value"])
            elif "@id" in x:
                out.append(x["@id"])
        elif isinstance(x, list):
            out.extend(scalar_values(x))
    return out


def head_now(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CRR-Module-R-VGW-source-anchor/1.0",
            "Accept": "application/n-triples",
        },
        method="HEAD",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        h = headers_dict(resp)
        resp.read(0)
        return {
            "status": getattr(resp, "status", None),
            "content_type": h.get("content-type"),
            "content_length": h.get("content-length"),
            "etag": h.get("etag"),
            "last_modified": h.get("last-modified"),
        }


def catalog_now(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CRR-Module-R-VGW-source-anchor/1.0",
            "Accept": "application/ld+json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        h = headers_dict(resp)
        ctype = h.get("content-type", "")
        clen = int(h.get("content-length") or 0)
        if "application/ld+json" not in ctype.lower():
            raise RuntimeError("CATALOG_CONTENT_TYPE_BOUNDARY")
        if clen <= 0 or clen > MAX_BYTES:
            raise RuntimeError("CATALOG_CONTENT_LENGTH_BOUNDARY")
        raw = resp.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise RuntimeError("CATALOG_BODY_BOUNDARY")
    text = raw.decode("utf-8")
    for forbidden in (
        '"HumanMadeObject"',
        '"AttributeAssignment"',
        '"assigned_by"',
        '"produced_by"',
        "crm:P108_has_produced",
    ):
        if forbidden in text:
            raise RuntimeError("CATALOG_RECORD_LEVEL_RDF_BOUNDARY")
    return {
        "raw": raw,
        "headers": h,
        "obj": json.loads(text),
    }


def one(row, head_expected, dist_expected):
    observed_head = head_now(row["landing_url"])
    expected_head = {
        "status": head_expected["status"],
        "content_type": head_expected["content_type"],
        "content_length": head_expected["content_length"],
        "etag": head_expected["etag"],
        "last_modified": head_expected["last_modified"],
    }
    if observed_head != expected_head:
        return {
            "slug": row["slug"],
            "ok": False,
            "stage": "HEAD",
            "expected": expected_head,
            "observed": observed_head,
        }

    cat = catalog_now(row["landing_url"])
    raw = cat["raw"]
    h = cat["headers"]
    obj = cat["obj"]

    enc = scalar_values(walk_key_values(obj, "encodingformat"))
    urls = scalar_values(walk_key_values(obj, "contenturl"))
    sizes = scalar_values(walk_key_values(obj, "contentsize"))

    observed = {
        "catalog_body_sha256": sha256(raw),
        "etag": h.get("etag"),
        "last_modified": h.get("last-modified"),
        "encoding_format_values": sorted(str(x) for x in enc),
        "content_url_values": sorted(str(x) for x in urls),
        "content_size_values": sorted(str(x) for x in sizes),
    }

    expected = {
        "catalog_body_sha256": dist_expected["catalog_body_sha256"],
        "etag": dist_expected["etag"],
        "last_modified": dist_expected["last_modified"],
        "encoding_format": dist_expected["encoding_format"],
        "content_url": dist_expected["content_url"],
        "content_size": str(dist_expected["content_size"]),
    }

    ok = all([
        observed["catalog_body_sha256"] == expected["catalog_body_sha256"],
        observed["etag"] == expected["etag"],
        observed["last_modified"] == expected["last_modified"],
        expected["encoding_format"] in observed["encoding_format_values"],
        expected["content_url"] in observed["content_url_values"],
        expected["content_size"] in observed["content_size_values"],
    ])

    return {
        "slug": row["slug"],
        "ok": ok,
        "stage": "CATALOG",
        "expected": expected,
        "observed": observed,
    }


def main():
    landing = json.loads(LANDING.read_text(encoding="utf-8"))
    heads = json.loads(HEADS.read_text(encoding="utf-8"))
    dist = json.loads(DIST.read_text(encoding="utf-8"))

    hmap = {x["slug"]: x for x in heads["datasets"]}
    dmap = {x["slug"]: x for x in dist["datasets"]}

    results = [
        one(row, hmap[row["slug"]], dmap[row["slug"]])
        for row in landing["datasets"]
    ]

    report = {
        "study": "MODULE_R_VGW_PREOPEN_SOURCE_ANCHOR_GATE_V1",
        "provider_distribution_content_opened": False,
        "rdf_statements_inspected": False,
        "results": results,
        "all_anchors_match": all(x["ok"] for x in results),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not report["all_anchors_match"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
