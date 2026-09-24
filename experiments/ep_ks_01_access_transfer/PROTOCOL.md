# EP_KS_01 - Kinsay design-aware near-holdout access transfer

Date frozen: 2026-09-24
Status: PRE-OUTCOME TRANSFER TEST

## Scientific question

Starting from the 1903 Kinsay passage that says the Queen's written statement was later witnessed by Marco Polo with his own eyes, can a generic seed/task retrieval policy surface later editorial treatment bearing on that eyewitness status?

## Task wording

"Find later editorial material in the same declared edition that bears on whether Marco Polo personally observed the Kinsay description."

This wording is frozen before retrieval.

## Source gates

H:
- 1903 vol. 2 p.185 seed layer page-image verified in the source registry;
- 1920 Addenda p.97 Tanner layer page-image verified in the source registry.

D:
- live task object is Project Gutenberg eBook #12410;
- expected SHA-256 is frozen;
- exact seed and target anchors are frozen;
- target-only evaluation text is excluded from query construction.

## Conditions

1. GSA_FULL_OBJECT
2. GSA_LATER_LAYER

Both use Generic Seed-Task Access Policy v1 unchanged.

## Target evaluation anchors

Evaluation only:
- "Mr. P. von Tanner"
- "never visited Hang Chau"

No relation label or claim state is opened.

## Status language

This is a design-aware near-holdout, not a blind holdout.

The Tanner event was known during design; the retrieval outcome under this frozen policy was not.
