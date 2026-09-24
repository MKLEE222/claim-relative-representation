# Generic Access Workflow v1

Date frozen: 2026-09-24
Status: TRANSFER RULE FREEZE

This workflow is distilled from the paper-money development case but is defined without paper-money-specific tokens.

## Input

A tuple:

\[
(seed,\ task,\ native\_object,\ horizon)
\]

The hidden target is not an input.

## Step A - determine historical direction

From task wording only:

- later-treatment task -> later documentary horizon;
- earlier-source task -> earlier documentary horizon;
- no direction -> no horizon restriction.

## Step B - extract seed/task signature

Build a signature from terms actually present in:

- seed passage;
- task wording;
- seed-exposed native metadata.

Feature classes:

1. explicit cited-source/person names;
2. referent/place/person names;
3. rare seed content terms;
4. document-local identifiers if natively exposed.

## Step C - choose applicable retrieval primitive

Priority is rule-based:

1. if explicit cited-source/person name exists -> source-chain primitive is applicable;
2. always compute a seed/task signature retrieval primitive;
3. domain filter is allowed only from seed/task terms;
4. pointer follow is allowed only if an explicit native pointer exists.

Do not substitute a target-derived name when source chaining is unavailable.

## Step D - apply native horizon

Use only native section/edition boundaries.

No reference-reconstruction boundary may be injected into the live workflow unless the same boundary is visible in the native object.

## Step E - return ranked/filtered candidate set

Record:
- candidate count;
- candidate ordering;
- inspection budget;
- which workflow primitives were applicable.

## Step F - evaluate after retrieval

Use the sealed source-verified target only now.

## No retuning rule

For NEAR_HOLDOUT and EXTERNAL_HOLDOUT:

- no new stopword list;
- no new target-specific domain dictionary;
- no new target-specific section locator;
- no parameter tuning after seeing target rank.

Any necessary change creates a new workflow version and invalidates the current holdout for confirmatory transfer.
