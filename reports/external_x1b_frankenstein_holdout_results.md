# Frankenstein X1B results - C17 sealed holdout

Date: 2026-09-24
Authoritative CI run: 35957994234
External commit: 5a208f869ff1213defa000e3181d5315a072a15f

## Holdout integrity

The X1B task contract, marker set, witness set, and pass/fail rules were committed before the C17 collation output was opened.

No X1B criterion was changed after output inspection.

## FV-ALIGN

**PASS**

C17 collation output contains:

- 1101 app elements;
- 5453 rdg elements;
- all five expected witnesses.

App witness coverage:

- 1064 app units cover all five witnesses;
- 29 cover four;
- 1 covers three;
- 7 cover two.

The task-facing apparatus therefore exposes cross-witness alignment and witness membership on the untouched holdout.

## FV-SOURCE-STRUCTURE

**FAIL exact equivalence**

For four print-derived witnesses, the frozen selected documentary marker vector is reproduced exactly in the apparatus representation.

For the manuscript witness:

Native C17 input:
- surface: 29
- zone: 67
- lb: 434
- mod: 202
- del: 203
- sga-add: 374
- milestone: 17
- anchor: 31

C17 apparatus reading representation:
- surface: 0
- zone: 0
- lb: 434
- mod: 202
- del: 203
- sga-add: 374
- milestone: 17
- anchor: 31

The only frozen-vector mismatches are:

\[
surface: 29 \rightarrow 0
\]

\[
zone: 67 \rightarrow 0
\]

## Scientific interpretation

The untouched holdout reproduces the task-relative boundary predicted from C16:

\[
FV\text{-}ALIGN = preserved/enabled
\]

while

\[
FV\text{-}SOURCE\text{-}STRUCTURE\ exact\ equivalence = false.
\]

The result is more specific than a generic "flattening loses structure" claim.

Most of the frozen source-documentary markers survive in the task-facing readings, including manuscript line breaks, modifications, deletions, additions, milestones, and anchors.

What does not survive in the frozen vector is the manuscript's surface/zone organization.

Therefore the observed transformation is **selective task adaptation**, not indiscriminate information destruction.

## Claim ceiling

The holdout supports:

> an independently designed DH collation representation can expose cross-witness alignment while not being representation-equivalent to the source manuscript for an explicitly declared surface/zone reconstruction task.

It does not establish:
- that surface/zone information is necessary for collation;
- that the collation representation is inferior;
- that all flattening behaves similarly;
- that source images or linked edition files cannot restore the omitted organization under a broader recovery contract.
