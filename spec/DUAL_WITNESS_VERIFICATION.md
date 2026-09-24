# Dual-Witness Verification Contract v1

Date frozen: 2026-09-24
Status: PRE-OUTCOME SOURCE CONTRACT

## Problem

A digital-representation experiment can become confused if the same object is asked to do two jobs:

1. establish the historical/editorial event; and
2. serve as the live computational task object.

The project therefore uses a dual-witness gate.

## H - Historical witness gate

Purpose:
verify that the relevant edition layer/event is historically attested and that the direction of the editorial transition is source-grounded.

Acceptable evidence:
- printed page image;
- scan tied to printed page;
- page-verified transcription.

H does **not** need to be the object consumed by the computational task.

## D - Digital task witness gate

Purpose:
freeze the exact digital representation actually exposed to the retrieval/recovery workflow.

Required:
- object identity and URL/file ID;
- hash where available;
- exact seed/target anchors;
- task-entry boundary;
- target-only evaluation information isolated from live input.

## Exact-transcription rule

Character-for-character scan transcription is mandatory only when a scientific claim depends on exact print wording or exact typographic/documentary form.

For a computational task run on a native digital object, it is sufficient that:

- H verifies the historical event/layer/direction; and
- D freezes the exact digital task object.

This prevents a false requirement that the digital task text must be manually retyped from the scan while preserving the source hierarchy.

## Promotion rule

A transition episode may enter a retrieval/access experiment when:

\[
H=PASS \land D=PASS.
\]

A downstream quotation or print-form claim may require a stronger H-exact-transcription gate.

## Claim boundary

Passing H+D does not establish historical truth.

It establishes:
- source identity;
- edition/layer identity;
- event direction;
- exact computational task witness.
