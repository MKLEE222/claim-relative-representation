from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANCHORS = HERE / "VGW_LANDING_METADATA_ANCHORS_v1.json"


def head_probe(row):
    req = urllib.request.Request(
        row["landing_url"],
        headers={
            "User-Agent": "CRR-Module-R-VGW-head-only/1.0",
            "Accept": "application/n-triples",
        },
        method="HEAD",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            # Critical freshness guarantee: read zero bytes.
            body = resp.read(0)
            if body not in (b"", None):
                raise RuntimeError("HEAD_ZERO_BODY_GUARD_FAILED")
            return {
                "slug": row["slug"],
                "request_method": "HEAD",
                "request_accept": "application/n-triples",
                "status": getattr(resp, "status", None),
                "final_url": resp.geturl(),
                "content_type": headers.get("content-type"),
                "content_length": headers.get("content-length"),
                "etag": headers.get("etag"),
                "last_modified": headers.get("last-modified"),
                "content_disposition": headers.get("content-disposition"),
                "location": headers.get("location"),
                "body_bytes_read": 0,
            }
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()}
        return {
            "slug": row["slug"],
            "request_method": "HEAD",
            "request_accept": "application/n-triples",
            "status": e.code,
            "final_url": e.geturl(),
            "content_type": headers.get("content-type"),
            "content_length": headers.get("content-length"),
            "etag": headers.get("etag"),
            "last_modified": headers.get("last-modified"),
            "content_disposition": headers.get("content-disposition"),
            "location": headers.get("location"),
            "body_bytes_read": 0,
            "http_error": str(e),
        }


def main():
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    results = [head_probe(row) for row in anchors["datasets"]]

    report = {
        "study": "MODULE_R_VGW_HEAD_ONLY_DISTRIBUTION_PROBE_V1",
        "freshness_boundary": {
            "request_method": "HEAD",
            "accept": "application/n-triples",
            "response_body_bytes_read": 0,
            "provider_distribution_content_opened": False,
            "rdf_statements_inspected": False,
            "guessed_distribution_url_used": False,
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
