# External Validation X1A - Frankenstein Variorum static representation audit

Date frozen: 2026-09-24
Status: EXTERNAL DEVELOPMENT AUDIT

## Scientific purpose

Test whether the task-relative representation framework maps naturally onto an independently designed DH collation workflow without redefining the external project's task.

This audit uses Frankenstein Variorum Collation Chunk C16 as a **development audit chunk**.

C16 is not an untouched holdout: its output was inspected during source audit and is therefore used only to design/falsify the mapping.

A separate C17 holdout is frozen before opening its collation output.

## External source

Repository:
FrankensteinVariorum/collationWorkspace

Pinned commit:
5a208f869ff1213defa000e3181d5315a072a15f

Native project task:
machine-assisted collation of five Frankenstein witnesses.

The project itself:
- prepares five witness inputs;
- handles structurally heterogeneous manuscript and print material;
- tokenizes/normalizes for collation;
- produces a common CollateX apparatus with app/rdgGrp/rdg structures;
- manually reviews misalignment and modifies source-side tokenization controls rather than editing the output directly.

## C16 files

Inputs:
- 1818_fullFlat_C16.xml
- 1823_fullFlat_C16.xml
- 1831_fullFlat_C16.xml
- Thomas_fullFlat_C16.xml
- msColl_C16.xml

Output:
- Collation_C16-complete.xml

## Questions

X1A-Q1.
Are the input witnesses structurally heterogeneous under the external project's own input representation?

X1A-Q2.
Does the common collation output create an explicit cross-witness alignment apparatus while still carrying witness identity?

X1A-Q3.
Does the audit support the stronger claim that flattening globally preserves or improves all scholarly information?

Expected answer discipline:
Q3 is not inferable from this audit. The external transformation is evaluated only relative to the collation task.

## Metrics

For each input:
- byte size;
- distinct XML element names;
- counts of selected structural/documentary elements.

For the collation output:
- number of app elements;
- number of rdgGrp elements;
- number of rdg elements;
- witness identifiers represented;
- number of app units involving 2, 3, 4, or 5 witnesses;
- occurrences of escaped source-structure markers in reading content.

## Interpretation

The strongest admissible result is:

> an independently designed DH workflow transforms heterogeneous witness structures into a common alignment apparatus that makes cross-witness comparison explicit for the collation task.

This is evidence for task-adaptive representation, not for "more structure is always better" or "flattening is always harmless."

## Holdout discipline

C17 is sealed separately.

No C17 collation output may be read before:
1. X1A mapping is frozen;
2. X1B tasks are frozen;
3. the holdout validator marks C17 SEALED.
