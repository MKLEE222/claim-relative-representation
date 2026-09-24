# External Validation X1B - Frankenstein C17 sealed holdout, protocol v2

Date frozen: 2026-09-24
Status: SUPERSEDES X1B v1 BEFORE ANY C17 OUTPUT CONTENT WAS OPENED

## Revision reason

X1B v1 froze a strict whole-vector source-structure reconstruction task.
Before opening C17 output content, v2 decomposes that task into two scholarly subcontracts:

- manuscript source geography;
- print pagination.

This prevents a single all-or-nothing vector from hiding selective preservation.

The marker vocabulary is still frozen from C16 development observations. No C17 outcome was used.

## External source

Repository:
FrankensteinVariorum/collationWorkspace

Pinned commit:
5a208f869ff1213defa000e3181d5315a072a15f

Holdout:
C17

Complete output metadata known before opening:
- path: collationChunks/C17/output/Collation_C17-complete.xml
- blob: 41032625f93e62dcb632f1ff8b35aa04e32df40c
- size: 410333 bytes

No output content had been read at freeze.

## FV-ALIGN

Question:
For a locus in the collation apparatus, which witnesses participate in the comparison unit and what readings are assigned?

Required state:
- app;
- rdgGrp / rdg;
- witness identity.

Success:
- app units exist;
- all five witnesses occur;
- at least one app includes all five witnesses.

## FV-SOURCE-GEOGRAPHY

Question:
From the collation representation alone, can one reconstruct the manuscript documentary geography represented by:

surface | zone | graphic | lb

States per marker:
- EXPLICIT_PRESERVED: output-carried count equals input count;
- PARTIAL: output carries some but not all;
- NOT_EXPLICIT: input count > 0 and output-carried count = 0.

This task is scoped to the collation representation alone. Reopening the manuscript source is a different recovery contract.

## FV-PRINT-PAGINATION

Question:
Does the collation apparatus carry print page-break structure?

Frozen marker:
pb

Evaluate separately for:
f1818 | f1823 | f1831 | fThomas

State definitions are identical to FV-SOURCE-GEOGRAPHY.

## Supplementary source-documentary markers

Report, without changing the primary tasks:

p | head | mod | del | sga-add | milestone | anchor | longToken

These are diagnostic only in X1B.

## Primary holdout hypothesis

C17 will expose FV-ALIGN explicitly while showing selective, not globally identical, carry-through of source-documentary structure.

PASS_SELECTIVE_ADEQUACY requires:
1. FV-ALIGN success; and
2. at least one frozen source-documentary marker with input count > 0 not exactly preserved.

GLOBAL_EQUIVALENCE_NOT_REJECTED occurs if every frozen primary documentary marker is exactly preserved.

## Anti-tuning

After output opening:
- no marker can be dropped;
- no new equivalence normalization can be added to X1B;
- witness set cannot change;
- interpretation categories cannot change.

Any refinement becomes X1C.

## Anti-overclaim

NOT_EXPLICIT means only:
not explicit in this collation representation under this contract.

It does not mean:
- historically destroyed;
- unrecoverable from the source edition;
- bad editorial design.

The collation transformation may be task-enabling for alignment precisely while not substituting for source-documentary reconstruction.
