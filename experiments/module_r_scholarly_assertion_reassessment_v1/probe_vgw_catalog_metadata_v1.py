from __future__ import annotations

import hashlib
import json
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

DATASETS = [
    "de_la_faille_1970",
    "works_after_1970",
    "van_gogh_museum",
    "krollermuller_museum",
    "rkd_collections",
]

BASE = "https://data.spinque.com/ld/data/vangoghworldwide/"


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._current = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        d = dict(attrs)
        href = d.get("href")
        if href:
            self._current = {"href": href, "text": "", "attrs": d}

    def handle_data(self, data):
        if self._current is not None:
            self._current["text"] += data

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._current is not None:
            self.links.append(self._current)
            self._current = None


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def candidate_distribution_links(base_url: str, html: str):
    parser = LinkCollector()
    parser.feed(html)
    out = []
    for row in parser.links:
        text = " ".join(row["text"].split()).lower()
        href = row["href"]
        attrs = {str(k).lower(): str(v) for k, v in row["attrs"].items()}
        signal = " ".join([text, href.lower(), json.dumps(attrs, sort_keys=True)])
        if (
            "n-triple" in signal
            or "application/n-triples" in signal
            or href.lower().endswith(".nt")
            or "download" in href.lower()
            or "distribution" in href.lower()
        ):
            out.append({
                "href": urljoin(base_url, href),
                "text": " ".join(row["text"].split()),
                "type": attrs.get("type"),
                "rel": attrs.get("rel"),
            })
    return out


def fetch_metadata(slug: str):
    url = BASE + slug + "/"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CRR-Module-R-VGW-metadata-probe/1.0",
            "Accept": "text/html,application/xhtml+xml;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
        headers = {k.lower(): v for k, v in resp.headers.items()}
        content_type = headers.get("content-type", "")
        final_url = resp.geturl()
        status = getattr(resp, "status", None)

    if "html" not in content_type.lower():
        raise RuntimeError(
            f"METADATA_BOUNDARY_VIOLATION_OR_UNEXPECTED_CONTENT: {slug}: {content_type}"
        )

    html = raw.decode("utf-8", errors="replace")
    return {
        "slug": slug,
        "landing_url": url,
        "final_url": final_url,
        "http_status": status,
        "content_type": content_type,
        "content_length_header": headers.get("content-length"),
        "etag": headers.get("etag"),
        "last_modified_header": headers.get("last-modified"),
        "landing_page_bytes": len(raw),
        "landing_page_sha256": sha256(raw),
        "distribution_link_candidates": candidate_distribution_links(final_url, html),
    }


def main():
    results = [fetch_metadata(slug) for slug in DATASETS]

    report = {
        "study": "MODULE_R_VGW_METADATA_ONLY_PROBE_V1",
        "freshness_boundary": {
            "provider_distribution_opened": False,
            "provider_ntriples_followed": False,
            "landing_pages_only": True,
        },
        "dataset_slugs": DATASETS,
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
