# External Validation X1B - Frankenstein C17 sealed holdout

Date frozen: 2026-09-24
Status: SEALED HOLDOUT BEFORE OUTPUT INSPECTION

## Purpose

Test the task-relative representation claim on an untouched Frankenstein Variorum collation chunk.

C16 was used to develop the external mapping. C17 is the holdout.

At freeze time:
- C17 input/output contents have not been opened by this study;
- only file/directory metadata and blob identifiers for the five input files are known;
- the external repository commit is pinned.

## External source

Repository:
FrankensteinVariorum/collationWorkspace

Pinned commit:
5a208f869ff1213defa000e3181d5315a072a15f

Chunk:
C17

Expected witness set:
- f1818
- f1823
- f1831
- fThomas
- fMS

## Frozen task contracts

### FV-ALIGN

Question:
Does the task-facing collation representation explicitly expose cross-witness alignment units and witness membership?

Success state:
- at least one app unit exists;
- all five expected witnesses occur in rdg @wit;
- app-level witness coverage is measurable without reopening the five source files.

This task evaluates alignment exposure, not literary interpretation.

### FV-SOURCE-STRUCTURE

Question:
Can the task-facing collation representation exactly reconstruct the selected native documentary-structure count vector for each witness?

Frozen documentary marker set:

surface | zone | lb | pb | p | head | mod | del | sga-add | milestone | anchor

For each witness:
1. count these elements in the external project's C17 input;
2. count literal source-marker occurrences carried inside that witness's collation readings;
3. compare the vectors exactly.

Success state:
all selected marker counts match for all five witnesses.

Failure state:
at least one selected marker count differs for at least one witness.

A failure means only:
the collation representation is not structurally equivalent to the source inputs for this declared reconstruction task.

It does **not** mean the collation representation is defective.

## Frozen hypothesis

The development mapping predicts:

- FV-ALIGN: task-facing state exposed;
- FV-SOURCE-STRUCTURE: exact equivalence is not assumed.

The holdout is considered informative under either result.

## Anti-tuning rule

After C17 output is opened:
- marker set cannot change;
- witness set cannot change;
- no marker may be dropped because it behaves inconveniently;
- no new normalization rule may be introduced into X1B.

Any later refinement becomes X1C and cannot rewrite X1B.

## Claim ceiling

A concordant result would support:

\[
Adequacy(R,\tau)
\]

with the same representation being alignment-enabling while not necessarily substituting for source-documentary reconstruction.

No global claim about flattening, TEI, or edition quality is licensed.
