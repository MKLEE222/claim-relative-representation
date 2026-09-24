# External Validation X2C - Whitman printed-locus task audit

Date frozen: 2026-09-24
Status: TASK-FACING NATIVE AUDIT

## Purpose

Move beyond the schema-level observation that @cert exists.

The native task is reconstructed at the printed-locus level:

> For a printed 1855 Leaves of Grass locus, which manuscript/notebook loci are linked to it, and with what editorial certainty?

The task uses the Archive's native relation semantics.

## External source

Repository:
whitmanarchive/whitman-LG_1855_variorum

Pinned commit:
25a00b7ebbdbc5246fce65a333bc761a5c22dad4

File:
source/authority/anc.02134.xml

## Task unit

The first token of each link @target is the printed-locus identifier.
The enclosing linkGrp @corresp identifies the manuscript/notebook file.
The second target token identifies the manuscript/notebook locus.
The link @cert is the Archive's encoded certainty.

For every unique printed locus, construct the native task output:

\[
Y(p)=\{(manuscript,\ locus,\ cert)\}
\]

and a link-only projection:

\[
Y^{-cert}(p)=\{(manuscript,\ locus)\}.
\]

## Metrics

- number of unique printed loci;
- loci linked to more than one manuscript/notebook passage;
- loci with both high and low certainty among their links;
- maximum number of linked manuscript passages for a single printed locus;
- endpoint equality before/after certainty removal.

## Interpretation

If mixed-certainty printed loci exist, certainty is not a single global property of "having a relation."

The link-only projection may preserve endpoint recovery while failing to preserve the Archive's editorially encoded relation status.

This remains an archive-state recovery task, not an independent genetic judgment by a scholar.
