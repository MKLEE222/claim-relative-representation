# Native Referent-Bridge Contract v1

Date: 2026-09-24
Status: POST-EP_KS_01-v1 MECHANISM DEVELOPMENT

## Motivation

EP_KS_01 v1 failed even after later-layer restriction because the seed and later target use different lexical names for the same place.

The digital object itself contains a seed-side editorial identification that bridges those names.

The project therefore distinguishes:

\[
access\ scope
\]

from

\[
referent\ mediation.
\]

## Admissible native referent bridge

A bridge may be used only when all are true:

1. it is present in the native digital object;
2. it is editorially attached to the seed referent or seed locus;
3. it is available without inspecting the hidden target;
4. it explicitly states or encodes an identity/alias/renaming relation;
5. its extraction rule is frozen before the new retrieval run.

Examples of admissible carrier forms:
- name-identification note;
- explicit "X is now Y" statement;
- native authority/identifier link;
- explicit sameAs/corresp identity pointer.

## Forbidden bridge

Not admissible:
- a target-only name learned from the hidden target;
- case-specific external knowledge introduced after inspecting target text;
- manually invented synonyms with no declared source carrier.

## Recovery interpretation

If an alias bridge improves retrieval, the mechanism is not:

"the model knows X and Y are the same."

It is:

\[
B_{native\ identity}
\rightarrow
referent\ expansion
\rightarrow
retrieval.
\]

The carrier and its provenance must be reported.

## Scientific status

The first Kinsay bridge experiment is exploratory because the need for referent mediation was discovered from the v1 failure.

The contract becomes confirmatory only on a later untouched carrier.
