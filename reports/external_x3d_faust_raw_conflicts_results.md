# Faust X3D results - raw source-qualified conflict ecology

Date: 2026-09-24
Authoritative CI run: 35958443136
External source commit: 502eca65120dd6189ceaf41d4e5017775e6e4677

## Source universe

The pinned faust-xml repository tarball produced:

- 20 XML files containing usable temp-pre relations;
- 1089 temp-pre relation records;
- 1959 adjacent directed precedence constraints;
- 641 distinct witness/item nodes;
- 18 distinct scholarly source URIs.

## Raw conflict structure

The source-qualified raw assertion graph contains:

- 38 direct reciprocal edge pairs;
- 20 nontrivial strongly connected components;
- 118 nodes participating in those SCCs;
- 612 directed edges internal to conflict SCCs;
- 7 source URIs represented inside conflict SCCs.

Therefore:

\[
RAW\ ASSERTION\ GRAPH\ ACYCLIC = 0.
\]

## Interpretation

The raw scholarly assertion ecology cannot be represented as one acyclic precedence order without discarding, reinterpreting, or otherwise resolving at least some constraints.

This is an empirical property of the pinned source XML, not a hypothetical graph example.

It supports the need to distinguish:

\[
assertion\ presence
\]

from

\[
assertion\ status\ in\ an\ executable\ chronology.
\]

## Important boundary

X3D does not reproduce the Digital Faust Edition's published feedback-edge-set solution.

It does not identify which specific edge the edition should delete or ignore.

It does not assign historical error to any cited source.

The published documentation separately states that contradictory assertions are handled to obtain an acyclic graph; X3D supplies the raw-data-side witness that contradictions/cycles are genuinely present in the source assertion ecology.

## X3C status

The separately preregistered published-GEXF audit remains BLOCKED_TRANSPORT.

No ignore/delete counts from the published graph are claimed.
