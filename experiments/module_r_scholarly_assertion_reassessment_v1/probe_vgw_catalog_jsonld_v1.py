from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANDING = HERE / "VGW_LANDING_METADATA_ANCHORS_v1.json"
HEAD_ANCHORS = HERE / "VGW_HEAD_METADATA_ANCHORS_v1.json"

MAX_BYTES = 10000


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def headers_dict(resp):
    return {k.lower(): v for k, v in resp.headers.items()}


def head_now(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CRR-Module-R-VGW-catalog-metadata/1.0",
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


def local_key(key: str) -> str:
    s = str(key)
    for sep in ("#", "/", ":"):
        if sep in s:
            s = s.rsplit(sep, 1)[-1]
    return s.lower()


KEEP_KEYS = {
    "id", "@id", "type", "@type",
    "title", "name", "label",
    "modified", "issued", "publisher", "creator",
    "distribution", "mediatype", "format",
    "accessurl", "downloadurl", "bytesize",
    "contenturl", "encodingformat", "contentsize",
    "license", "rights", "identifier",
}


def sanitize_metadata(node):
    if isinstance(node, list):
        return [sanitize_metadata(x) for x in node]
    if not isinstance(node, dict):
        return node

    out = {}
    for k, v in node.items():
        lk = local_key(k)
        if str(k) in {"@context"}:
            continue
        if lk in KEEP_KEYS or str(k).lower() in KEEP_KEYS:
            out[k] = sanitize_metadata(v)
        elif "distribution" in lk:
            out[k] = sanitize_metadata(v)
        elif any(x in lk for x in (
            "accessurl", "downloadurl", "mediatype", "bytesize",
            "contenturl", "encodingformat", "contentsize",
        )):
            out[k] = sanitize_metadata(v)
    return out


def fetch_catalog(row, head_anchor):
    observed_head = head_now(row["landing_url"])
    expected = {
        "status": head_anchor["status"],
        "content_type": head_anchor["content_type"],
        "content_length": head_anchor["content_length"],
        "etag": head_anchor["etag"],
        "last_modified": head_anchor["last_modified"],
    }
    if observed_head != expected:
        raise RuntimeError(
            "VERSION_DRIFT_BEFORE_CATALOG_GET "
            + json.dumps(
                {"slug": row["slug"], "expected": expected, "observed": observed_head},
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    if "application/ld+json" not in str(observed_head["content_type"]).lower():
        raise RuntimeError(f"UNEXPECTED_HEAD_CONTENT_TYPE {row['slug']}")

    n = int(observed_head["content_length"] or 0)
    if n <= 0 or n > MAX_BYTES:
        raise RuntimeError(f"HEAD_METADATA_SIZE_BOUNDARY {row['slug']} {n}")

    req = urllib.request.Request(
        row["landing_url"],
        headers={
            "User-Agent": "CRR-Module-R-VGW-catalog-metadata/1.0",
            "Accept": "application/ld+json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        h = headers_dict(resp)
        ctype = h.get("content-type", "")
        clen = int(h.get("content-length") or 0)
        if "application/ld+json" not in ctype.lower():
            raise RuntimeError(f"GET_METADATA_CONTENT_TYPE {row['slug']} {ctype}")
        if clen <= 0 or clen > MAX_BYTES:
            raise RuntimeError(f"GET_METADATA_SIZE_HEADER {row['slug']} {clen}")
        raw = resp.read(MAX_BYTES + 1)

    if len(raw) > MAX_BYTES:
        raise RuntimeError(f"GET_METADATA_BODY_BOUNDARY {row['slug']} {len(raw)}")

    text = raw.decode("utf-8")
    forbidden = (
        '"HumanMadeObject"',
        '"AttributeAssignment"',
        '"assigned_by"',
        '"produced_by"',
        "crm:P108_has_produced",
    )
    if any(x in text for x in forbidden):
        raise RuntimeError(f"CATALOG_CONTAINS_RECORD_LEVEL_RDF {row['slug']}")

    obj = json.loads(text)
    return {
        "slug": row["slug"],
        "landing_url": row["landing_url"],
        "body_bytes": len(raw),
        "body_sha256": sha256(raw),
        "content_type": ctype,
        "content_length": str(clen),
        "etag": h.get("etag"),
        "last_modified": h.get("last-modified"),
        "sanitized_catalog_metadata": sanitize_metadata(obj),
    }


def main():
    landing = json.loads(LANDING.read_text(encoding="utf-8"))
    heads = json.loads(HEAD_ANCHORS.read_text(encoding="utf-8"))
    by_slug = {x["slug"]: x for x in heads["datasets"]}

    results = []
    for row in landing["datasets"]:
        results.append(fetch_catalog(row, by_slug[row["slug"]]))

    report = {
        "study": "MODULE_R_VGW_BOUNDED_CATALOG_JSONLD_V1",
        "freshness_boundary": {
            "catalog_metadata_get_only": True,
            "max_bytes_per_response": MAX_BYTES,
            "distribution_url_followed": False,
            "provider_distribution_content_opened": False,
            "artwork_record_rdf_inspected": False,
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
