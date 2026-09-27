# R3 coding-state separation amendment v3

Date: 2026-09-27
Status: frozen before full R3-A coding.

## Problem

The prior R3 relation vocabulary allowed UNRESOLVED_RELATION as if it were one more historical relation family.

This risks conflating three different phenomena:
1. source-explicit uncertainty or doubt;
2. historically competing positions among actors;
3. analyst/coder inability to determine the relation from the available evidence.

These must be separated.

## A. Historical relation labels

Historical relation labels describe what one source-bound scholarly act does to another proposition or object:
- ADDITIVE_EVIDENCE
- CORROBORATION
- CRITICISM
- FACTUAL_CORRECTION
- CORRECTION_OF_PRIOR_CRITICISM
- IDENTIFICATION_UPDATE
- ATTRIBUTION_UPDATE
- TEXTUAL_UPDATE
- QUALIFICATION

`UNRESOLVED_RELATION` is removed from this label family for all new coding.

## B. Source modality

Record source-explicit modality separately:
- SOURCE_MODALITY_NOT_MARKED
- SOURCE_UNCERTAIN
- SOURCE_DOUBTFUL
- SOURCE_PROBABLE_OR_CONJECTURAL

The field records explicit source wording only. It does not express the coder's confidence.

## C. Coding status

Record analyst status separately:
- CODED
- TARGET_UNRESOLVED
- RESPONSIBILITY_UNRESOLVED
- RELATION_UNRESOLVED
- EVIDENCE_INSUFFICIENT

These are measurement states, not historical relations.

## D. Controversy state

After act segmentation, an entry/trajectory may be characterized as:
- SINGLE_POSITION
- MULTIVOICE_COMPATIBLE
- MULTIVOICE_CONTESTED
- SOURCE_LEAVES_OPEN

This state is derived from verified acts and source modality. It is not assigned from topic similarity.

## Why this matters

A representation that drops an explicit doubt marker or collapses multiple competing actors into one settled proposition has lost a historical scholarly state even if all textual endpoints remain present.

By contrast, a coder who cannot identify the target has not discovered historical uncertainty; the measurement is unresolved.

## Effect on B01

B01 contains no final prevalence output and may be migrated without changing historical evidence spans.

Rows currently using QUALIFICATION remain valid where the later act explicitly narrows or limits an earlier proposition.

No B01 row is reclassified solely to create a representation effect.