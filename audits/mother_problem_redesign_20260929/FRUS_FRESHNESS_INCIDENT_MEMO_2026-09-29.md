# FRUS freshness incident memo — 2026-09-29

Status: STRICT FRESH CANDIDATE DISQUALIFIED.

## 1. Prior rule

The Module-R planning record had reserved:

    HistoryAtState/frus

as a possible fresh corpus under the explicit restriction:

    do not open volumes/*.xml

Allowed pre-fresh inputs were limited to:
- repository metadata;
- README;
- schema/frus.odd;
- generic schema/shared taxonomy/transformation files.

## 2. Incident

While auditing project-level encoding of sender/recipient roles, a GitHub repository code-search
query was issued for:

    persName type from head

The search was intended to locate schema/guideline occurrences.

One returned search result was from:

    volumes/frus1977-80v09.xml

The returned snippet exposed only non-target volume-level material:
- a General Editor byline;
- a nearby history.state.gov / Government Printing Office URL fragment.

No FRUS document episode was intentionally opened.
No document-level head/date/@ana reassessment case was surfaced.
No candidate outcome, event count or favorable episode was inspected.

The volume file itself was not fetched/opened.

## 3. Scientific disposition

Despite the minimal and non-target nature of the snippet, the literal pre-fresh restriction was:

    no volumes/*.xml exposure

That restriction is now violated.

Therefore, under the stricter interpretation required by this project:

    FRUS_STRICT_FRESHNESS = LOST

FRUS must not be used as the untouched confirmatory corpus for Module R.

This is a conservative scientific disposition.
It does not imply that the snippet biased any substantive Module-R result; no Module-R FRUS result
exists.

## 4. Retained uses

FRUS may still be used for:
- near-neighbor design;
- schema/taxonomy analysis;
- exposed development;
- sensitivity / transfer analysis;
- candidate-family discovery.

It may not be described as:
- untouched;
- pristine;
- fresh one-shot confirmation.

## 5. Consequence

The next fresh non-temporal Module-R corpus must be a different project/corpus whose episode-level
content has not been surfaced.

The replacement screening protocol should prevent this class of incident by:
1. using exact project-level file fetches only;
2. avoiding repository-wide code search after a corpus is reserved as fresh;
3. maintaining an explicit allowlist of pre-fresh paths;
4. treating any returned episode/data path outside that allowlist as immediate exposure.
