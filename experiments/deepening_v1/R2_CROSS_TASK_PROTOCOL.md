# R2 cross-task locator-preservation protocol v1

Date frozen: 2026-09-26
Status: prospective within-project controlled-twin transfer.
Development chunks already opened: C01-C05 and C16-C18.
Target selector does not inspect target XML content.

## Question

Can a representation be exact for the collation task while being insufficient for a different scholarly task that requires source-documentary coordinates?

The upstream Frankenstein workflow deliberately distinguishes raw token content t from normalized token content n. Its complete apparatus retains raw rdg content as well as normalized rdgGrp descriptors. This experiment does not claim the upstream project loses source location. It tests what is lost if one compresses the output to the normalized collation state alone.

## Target selector

At the pinned upstream commit, enumerate chunks by filename existence only.

Exclude C01-C05 and C16-C18 because their outcomes have already been inspected in this project.

Select the next five eligible chunks in lexical order. Eligibility is the same as R2_TRANSFER_PROTOCOL: five standard input witnesses plus a complete output file must exist.

No target apparatus content may be parsed before the selected list is frozen by the script.

## Registered tasks

### Q_GROUP

Recover, for every apparatus unit:
- the witness partition;
- the native normalized rdgGrp descriptor sequence.

### Q_LOCATOR

For a selected source witness, recover the exact registered documentary locator value changed by the controlled twin.

Eligible locator elements:
- pb;
- lb;
- milestone;
- anchor.

Eligible changed attributes, in priority order:
- xml:id;
- n;
- sID;
- eID.

The twin changes exactly one attribute value on the first eligible locator found by the frozen witness/file order. Text, element type, ordering, and every other source coordinate remain unchanged.

## Representations

FULL_NATIVE:
the upstream complete apparatus including raw rdg content plus normalized descriptors.

NORM_COLLATION:
for every app, only witness partition plus rdgGrp@n descriptors; raw rdg content and source-locator attributes are removed.

LOCATOR_LEDGER:
an explicitly charged source-side binding containing chunk, witness, locator ordinal, element type, attribute name, and original value.

## Controlled twin test

For each selected chunk:

1. Replay the unmodified native pipeline and require exact Q_GROUP agreement with the pinned complete target before interpreting the twin.
2. Construct the one-attribute locator twin.
3. Replay the complete native pipeline on the twin.
4. Compare NORM_COLLATION signatures between original and twin.
5. Confirm that Q_LOCATOR differs.
6. Confirm that FULL_NATIVE raw output differs at the changed locator when the changed marker survives into raw rdg content. If the marker is not carried into the apparatus raw reading, report FULL_NATIVE_LOCATOR_NOT_EXPOSED rather than forcing a success.

The decisive projection-separation pattern is:
NORM_COLLATION(original) = NORM_COLLATION(twin)
and
Q_LOCATOR(original) != Q_LOCATOR(twin).

This is a controlled source-completion witness, not a naturally observed editorial error.

## Repair test

For NORM_COLLATION, attach the correct LOCATOR_LEDGER and recover Q_LOCATOR.

Wrong-binding control:
replace the ledger value with the twin value while keeping the ledger schema and key identical.

Required:
- correct ledger recovers original Q_LOCATOR;
- wrong ledger does not;
- Q_GROUP remains unchanged in both repair arms.

Report canonical JSON bytes for the locator ledger and bytes for the full native complete apparatus. These are descriptive information costs, not universal coding bounds.

## Interpretation

A positive result supports a task-relative preservation claim:
a normalized state may be sufficient for the registered collation grouping task yet fail a source-coordinate task unless an additional source-bound relation is retained.

It does not imply:
- the upstream Frankenstein Variorum is deficient;
- all normalization loses location;
- the locator ledger is globally minimal;
- the controlled twin is a natural historical alternative.

The upstream complete apparatus retaining both raw and normalized content is a strong baseline and must receive full credit.
