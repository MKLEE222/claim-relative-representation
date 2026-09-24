# External Validation X3B - Faust source-locator projection preflight

Date frozen: 2026-09-24
Status: CONTROLLED EXTERNAL PROJECTION

## Motivation

X3A shows that every frozen temporal assertion is source-qualified and that the source element carries both:

- work-level source URI;
- per-relation page/locator text.

These must not be collapsed into one coordinate.

## Transformations

### X3B-L
Remove only source locator text while preserving:
- source URI;
- relation name;
- ordered item sequence.

### X3B-S
Remove the source element entirely while preserving:
- relation name;
- ordered item sequence.

## Task contracts

### FA-TEMPORAL
Recover the native ordered item relation.

### FA-SOURCE-WORK
Recover the cited source work.

### FA-SOURCE-LOCATOR
Recover the per-relation source locator/page.

## Hypotheses

For X3B-L:
- FA-TEMPORAL structurally preserved;
- FA-SOURCE-WORK structurally preserved;
- FA-SOURCE-LOCATOR explicit state removed.

For X3B-S:
- FA-TEMPORAL structurally preserved;
- relation-local FA-SOURCE-WORK and FA-SOURCE-LOCATOR removed;
- contextual recovery of source work from the file path remains a separate carrier hypothesis and is not labeled unavailable here.

## Claim ceiling

This is a carrier-separation audit.

It does not evaluate conflict resolution, graph ordering, or historical truth.
