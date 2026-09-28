# Module D2 v1 — Natural combined epistemic and relation revision in Whitman history

Date frozen: 2026-09-28
Status: PRE-DIFF DEVELOPMENT PRESSURE TEST. DISTINCT FROM D1; NOT A RESCUE OR REPLACEMENT.

## Natural revision event

Repository:
whitmanarchive/whitman-LG_1855_variorum

Relation file:
source/authority/anc.02134.xml

Parent commit:
fe63fcfbeca16f85583a29355c2d3a44e09b280f

Child commit:
8c6aba338bd3b8a52ec74d014ec1afc8137cc4a9

Child commit date:
2020-05-13T17:20:49Z

Child commit message:
adjusted certainty and some relations

The commit message and parent identity were inspected. The file diff and changed relation identities were NOT opened before this protocol was frozen.

## Purpose

D1 established a real one-link certainty revision but also showed that a homogeneous locus-level status plus an identity-rich patch was sufficient for that event.

D2 tests a harder natural regime chosen independently by its commit message:

> When an editorial revision may alter certainty and relation presence/identity together, can a research state reproduce the exact revised relation graph while preserving all unaffected relation claims?

D1 remains authoritative for its event regardless of D2 outcome.

## Population

All valid relation links in anc.02134.xml at the parent and child commits.

## Logical relation identity

Primary identity:

    (print_target, manuscript_file, manuscript_local_target)

Multiplicity is retained.

Certainty is an epistemic attribute on the logical relation.

## Delta classes

Across the complete parent/child pair report:

- CERT_CHANGED: same identity, certainty differs;
- ADDED_RELATION: identity newly present;
- REMOVED_RELATION: identity removed;
- UNCHANGED: identity and certainty unchanged.

If the same logical identity occurs multiple times, use multiset semantics and report ambiguity.

## Current task Q0

For each printed target:

    endpoint multiset = {(manuscript_file, manuscript_local_target)}

Report whether Q0 changes.

Unlike D1, D2 does not assume endpoint identity is invariant.

## Dynamic research state

The complete state consists of:
- relation identity/presence;
- endpoint binding;
- per-relation certainty.

A correct update must produce the exact child state.

## Representation arms

### R_FULL_RELATION_STATE

Retains the complete parent relation identity -> certainty multiset.

Receives only the natural relation-level delta.

### R_CERT_ONLY_STATE

Retains the multiset of certainty labels per printed locus and the complete endpoint set, but not endpoint -> certainty binding.

### R_ENDPOINT_ONLY

Retains only relation identities/endpoints.

### R_SOURCE_REOPEN

Reopens the exact child relation source and reconstructs the complete child relation state.

## Selective revision criteria

### Delta correctness

Every changed certainty, added relation, and removed relation matches the child source.

### Unaffected stability

Every relation outside the natural delta retains its parent identity and certainty.

### No collateral revision

No unaffected relation is modified.

### Complete child graph exactness

Final relation presence + endpoint identity + certainty multiset equals the child state.

### Event-local determinacy

For each affected printed target, enumerate all endpoint-specific parent certainty assignments compatible with R_CERT_ONLY_STATE.

Apply the natural identity-rich patch.

Report whether the child state is uniquely determined.

This allows the experiment to discover that a coarse state is sufficient for some affected loci and insufficient for others.

## Matched wrong-delta control

If at least two delta records of a compatible type exist:

- for CERT_CHANGED records, permute new certainty assignments among changed identities while preserving old/new certainty multisets;
- for ADDED/REMOVED relation records, only construct a wrong control if an interface/cardinality-matched reassignment can be made without changing the number of add/remove operations.

Do not force a control if no nontrivial matched permutation exists.

## Metrics

- parent/child relation counts;
- delta-class counts;
- affected printed targets;
- affected source files;
- Q0 endpoint changes;
- R_FULL_RELATION_STATE exactness;
- unaffected stability and collateral change count;
- R_CERT_ONLY_STATE event-local exact/ambiguous affected loci;
- R_ENDPOINT_ONLY unresolved epistemic items;
- source reopen exactness;
- delta packet bytes;
- parent full-state bytes;
- dependency-aware counts.

## Dispositions

NATURAL_COMBINED_REVISION_OBSERVED:
at least one CERT_CHANGED and at least one ADDED_RELATION or REMOVED_RELATION.

SELECTIVE_COMBINED_REVISION:
full retained state plus natural patch reaches exact child state with zero collateral changes.

COARSE_STATE_NONDETERMINING_ON_AFFECTED_LOCUS:
at least one affected locus has multiple child states compatible with the coarse parent state plus natural patch.

SOURCE_REOPEN_EXACT:
exact child reconstruction from pinned source.

## Claim ceiling

A positive result can support only:

> A real editorial revision selectively changes relation statuses and/or relation topology while leaving unrelated relation claims stable; exact continuation depends jointly on retained state, the information carried by the revision event, and lawful source access.

It cannot establish:
- that the child editorial state is historically truer;
- universal necessity of full relation graphs;
- independent transfer;
- human consensus;
- that all editorial changes are well represented by Git commits.

## Stop rule

Do not substitute another commit after opening D2 because its delta is smaller, larger, cleaner, or less favorable than expected.

Preserve every natural delta class.
