# MC_FA_01 - Faust raw-conflict carrier search

Date frozen: 2026-09-24
Status: MECHANISM SEARCH ON ALREADY-INSPECTED RAW ASSERTION ECOLOGY

## Task A - FA-CONFLICT-STRUCTURE

From the raw temp-pre assertions, recover the directed precedence graph used to detect reciprocal edges and nontrivial strongly connected components.

Candidate carriers:
- ORDERED_ITEMS
- SOURCE_URI
- SOURCE_LOCATOR
- FILE_CONTEXT

Reference output:
directed adjacent constraints and resulting conflict SCC membership.

Hypothesis:
ORDERED_ITEMS alone is sufficient for structural conflict detection.

## Task B - FA-CONFLICT-SOURCE

For each directed precedence edge inside a conflict SCC, recover the scholarly source-work identity attached to the native assertion(s) that generated the edge.

Candidate source carriers:
- SOURCE_URI
- FILE_CONTEXT

The search tests whether native file context functionally substitutes for explicit SOURCE_URI across the pinned raw corpus.

Important:
functional substitution is accepted only if every source-bearing XML file used in the task maps to exactly one source URI and no file-context key maps ambiguously.

If that condition fails, FILE_CONTEXT is not called source-work equivalent.

SOURCE_LOCATOR is reported separately and is not required for source-work identity.

## Claim ceiling

This experiment can identify carrier sufficiency for:
- graph conflict structure;
- source-work auditability.

It cannot identify which historical source is correct or reproduce the published feedback-edge-set solution.
