# Documentary Reference-State Protocol v1

Date frozen: 2026-09-25
Status: PRE-ADJUDICATION

## Principle

A reference state is not "the author's answer" and is not historical truth.

For Stage A, the reference object is a source-verified set of documentary constraints:

\[
R_D=\{r_1,\ldots,r_n\}
\]

where every \(r_i\) has:
- a documentary relation type;
- subject/object;
- source witness;
- page/span anchor;
- verification state;
- admissible alternatives, if any.

## Construction order

1. Build the reference from the richest source hierarchy available before any representation ablation.
2. Verify against printed page image where available.
3. Freeze admissible alternatives and ambiguity.
4. Only then apply representation/access transformations.
5. Never repair a transformed output by consulting the reference during live recovery.

## Set-valued answers

When the source permits more than one materially compatible documentary assignment, the reference stores an admissible set rather than forcing one point label.

Scoring categories:

- EXACT_SUPPORTED
  recovered answer matches a verified reference assignment.

- COMPATIBLE_INCOMPLETE
  recovered answer is source-compatible but omits a distinction needed for full resolution.

- UNSUPPORTED_OVERCOMMITMENT
  recovered answer asserts a documentary distinction not licensed by the visible/source basis.

- CONTRADICTION
  recovered answer conflicts with the frozen source-verified constraint set.

- UNRESOLVED_VALID
  the task contract permits unresolved and the visible evidence genuinely leaves materially different assignments.

## Independence

Reference construction is independent of:
- transformation outcome;
- retrieval rank;
- provisional humanistic claim state.

No retain/revise/defer/withhold field is part of Stage-A reference data.

## Verification labels

- PAGE_VERIFIED
- OBJECT_VERIFIED
- PROVISIONAL_DIGITAL_ONLY
- BLOCKED

Only PAGE_VERIFIED / OBJECT_VERIFIED entries may anchor confirmatory Stage-A evaluation.

## Current scope

The paper-money PM01-PM03 documentary reference is confirmatory-ready because the relevant excerpts and page anchors are page-image verified.

Kinsay/coal reference promotion must follow the alignment file's stricter verification ledger; conflicting metadata elsewhere in the repository does not silently upgrade them.
