# Typed Transformation Taxonomy v1

Date frozen: 2026-09-24

## Principle

The previous intervention table mixed operations on different representational layers. This taxonomy separates them.

A transformation is defined independently of the downstream task. Applicability to a task is handled by the task contract, not by redesigning the transformation.

## TD — Documentary transformations

Operate on documentary/digital-object structure inherited from the source representation.

Examples:
- remove responsibility metadata;
- remove revision-history metadata;
- regularize/normalize variant forms;
- merge or serialize edition layers;
- body-only export.

Current operators:
- **TD_ATTRIBUTION** — remove explicit responsibility metadata while preserving substantive text.
- **TD_TEMPORAL** — remove explicit revision/version ordering while preserving substantive text and remaining metadata.
- **TD_NORMALIZE** — collapse declared documentary distinctions through a deterministic normalizer.

## TR — Relational-interface transformations

Operate on the constructed scholarly relation interface, not on the historical source itself.

Examples:
- omit typed CEDL relation edges;
- omit explicit claim/referent pointers;
- expose endpoint passages without the relation graph.

Current operators:
- **TR_EVIDENCE** — remove typed relation edges while retaining endpoint evidence objects.
- **TR_BINDING** — remove explicit claim/referent binding while retaining evidence objects.

These operators must never be described as if the printed Yule-Cordier witness originally contained a native SUPPORTS or CHALLENGES field.

## TA — Access/context transformations

Operate on what context is available to the downstream task.

Examples:
- current span only;
- span + note;
- chapter window;
- whole digital volume;
- cross-edition access;
- external-witness access.

Current access states:
- **TA_SPAN** — only the focal span plus minimal bibliographic identity;
- **TA_LOCAL** — focal span plus local note/heading/neighboring context;
- **TA_OBJECT** — full declared digital object, including internal cross-layer traversal;
- **TA_EXTERNAL** — declared external witnesses are available.

TA changes operational availability rather than asserting documentary deletion.

## Invalid comparisons

The following are not treated as equivalent operations:

- TD_ATTRIBUTION vs TR_EVIDENCE;
- TR_BINDING vs TA_SPAN;
- TD_NORMALIZE vs TA_LOCAL.

They act on different layers and therefore enter different factorial blocks.

## Realism requirement

Every TD/TR/TA level used in an experiment must satisfy:

1. documented analogue or reproducible workflow;
2. deterministic constructor;
3. declared invariants;
4. no undeclared changes to substantive claim content;
5. applicability mask relative to the downstream task.

## Task-relative applicability

A transformation may be irrelevant to a task.

Irrelevant transformation-task cells are marked **N/A**, not counted as negative results.

This prevents artificial denominator inflation and avoids treating a task that never needed a coordinate as evidence that removing that coordinate is harmless in general.
