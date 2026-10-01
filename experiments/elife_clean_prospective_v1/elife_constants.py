from __future__ import annotations

import re

SOURCE_REPOSITORY = "elifesciences/elife-article-xml"
SOURCE_COMMIT = "ec0fbc8e81cfae472260f96a03ba078b57007612"
SOURCE_TREE = "d6bba934b495f7e4272f370de53817c0fc28af84"

EXPECTED_MANUSCRIPTS = 297
EXPECTED_XML_FILES = 568
EXPECTED_TOTAL_BYTES = 96584062

FILENAME_RE = re.compile(r"^elife-preprint-(\d+)-v(\d+)\.xml$")
VERSION_DOI_RE = re.compile(r"^10\.7554/eLife\.(\d+)\.(\d+)$")
SUBARTICLE_DOI_RE = re.compile(
    r"^10\.7554/eLife\.(\d+)\.(\d+)\.sa(\d+)$"
)

XLINK_NS = "http://www.w3.org/1999/xlink"
XLINK_HREF = f"{{{XLINK_NS}}}href"

REGISTERED_SUBARTICLE_TYPES = {
    "editor-report",
    "referee-report",
    "author-comment",
}

REGISTERED_GENERATORS = {
    "REGISTER_PUBLIC_REVIEW",
    "REGISTER_ASSESSMENT",
    "REGISTER_AUTHOR_RESPONSE",
    "PUBLISH_REVIEWED_PREPRINT",
    "PUBLISH_REVISED_REVIEWED_PREPRINT",
}

TOP_DISPOSITIONS = {
    "COMPLETE_V1",
    "COMPLETE_REVISED",
    "INVALID_IDENTITY",
    "INVALID_CURRENT_EVALUATION_BINDING",
    "INVALID_PRIOR_HISTORY",
    "PARSE_ERROR",
    "ORACLE_RUNTIME_UNRESOLVED",
}

TRACE_REGISTRY = {
    "PARSE_OK",
    "PARSE_ERROR",
    "VERSION_V1",
    "VERSION_REVISED",
    "ASSESSMENT_MISSING",
    "ASSESSMENT_ONE",
    "ASSESSMENT_MULTIPLE",
    "REVIEW_MISSING",
    "REVIEW_ONE",
    "REVIEW_MULTIPLE",
    "AUTHOR_RESPONSE_ABSENT",
    "AUTHOR_RESPONSE_PRESENT",
    "AUTHOR_RESPONSE_MULTIPLE",
    "PRIOR_HISTORY_NONE",
    "PRIOR_HISTORY_PRESENT",
    "UNKNOWN_SUBARTICLE_ABSENT",
    "UNKNOWN_SUBARTICLE_PRESENT",
    "CURRENT_EVAL_PREFIX_OK",
    "CURRENT_EVAL_PREFIX_BAD",
    "IDENTITY_OK",
    "IDENTITY_BAD",
    "PREPRINT_VERSION_OK",
    "PREPRINT_VERSION_BAD",
    "PRIOR_HISTORY_COUNT_OK",
    "PRIOR_HISTORY_COUNT_BAD",
    "PRIOR_VERSION_SET_OK",
    "PRIOR_VERSION_SET_BAD",
    "PRIOR_EVENT_ASSESSMENT_OK",
    "PRIOR_EVENT_ASSESSMENT_BAD",
    "PRIOR_EVENT_REVIEW_OK",
    "PRIOR_EVENT_REVIEW_BAD",
    "PRIOR_EVENT_PREFIX_OK",
    "PRIOR_EVENT_PREFIX_BAD",
    "QUALIFY_REGISTER_PUBLIC_REVIEW",
    "QUALIFY_REGISTER_ASSESSMENT",
    "QUALIFY_REGISTER_AUTHOR_RESPONSE",
    "QUALIFY_PUBLISH_V1",
    "QUALIFY_PUBLISH_REVISED",
    "REJECT_WRONG_TARGET",
    "REJECT_WRONG_EVALUATION_BINDING",
    "REJECT_MISSING_CURRENT_ASSESSMENT",
    "REJECT_MISSING_CURRENT_REVIEWS",
    "REJECT_MISSING_PRIOR_HISTORY",
    "REJECT_BAD_PRIOR_HISTORY",
    "HISTORY_ABLATION_REGISTRATION_INVARIANT",
    "HISTORY_ABLATION_REVISED_PUBLICATION_REJECTED",
    "SEQUENCE_CLOSURE_PASS",
}


def canonical_doi(value: str | None) -> str | None:
    if value is None:
        return None
    s = value.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/"):
        if s.startswith(prefix):
            return s[len(prefix):]
    return s


def expected_version_doi(manuscript_id: str, rp_version: int) -> str:
    return f"10.7554/eLife.{manuscript_id}.{rp_version}"


def in_scope(manuscript_id: str) -> bool:
    return int(manuscript_id) % 16 == 0
