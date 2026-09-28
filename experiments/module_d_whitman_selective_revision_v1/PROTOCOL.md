# Module D v1 — Natural selective epistemic revision in Whitman relation history

Date frozen: 2026-09-28
Status: PRE-DIFF DEVELOPMENT PROTOCOL. THE EXACT PARENT/CHILD COMMITS ARE FIXED BEFORE OPENING THE FILE DELTA. NOT INDEPENDENT TRANSFER.

## Natural revision event

Repository:
whitmanarchive/whitman-LG_1855_variorum

Relation file:
source/authority/anc.02134.xml

Parent commit:
7cdf5ddc9d0cfff83289f687613ee3d0510e6520

Child commit:
fe63fcfbeca16f85583a29355c2d3a44e09b280f

Child commit date:
2020-05-12T16:32:04Z

Child commit message:
adjusted certainty

The commit message was inspected to select the event. The file diff and changed relation identities were NOT opened before this protocol was frozen.

## Epistemic meaning of cert

The relation file itself states that certainty levels correspond to the editors' level of certainty that the described manuscript or notebook line is a version of the printed line.

Therefore a natural change in per-link cert is treated here as an editorial epistemic-status revision about a relation claim.

It is NOT treated as an independent truth label about Whitman's genetic history.

## Primary question

Can a retained research state absorb a real, localized editorial certainty revision such that:

1. relation claims whose certainty changed are updated to the child value;
2. relation claims not changed by the commit retain their parent value;
3. endpoint identity is preserved;
4. no unrelated relation status is altered;
5. complete child-state recovery remains possible by lawful source reopening.

This is the first project module whose positive target is substantive selective epistemic revision rather than UNRESOLVED -> resolved state refinement.

## Population

All valid relation links in anc.02134.xml at the parent and child commits.

No favorable subset may be used as the main denominator.

## Relation identity

Primary logical relation identity:

    (print_target, manuscript_file, manuscript_local_target)

where:
- print_target is the printed-side target token in @target;
- manuscript_file is linkGrp/@corresp;
- manuscript_local_target is the manuscript/notebook-side target token.

Multiplicity is preserved.

If the same logical identity occurs multiple times, records are treated as a multiset and the ambiguity is reported rather than silently collapsed.

## Natural delta classes

For the complete parent/child pair report:

- CERT_CHANGED: same logical relation identity present in both, certainty differs;
- UNCHANGED: same identity and certainty;
- ADDED_RELATION;
- REMOVED_RELATION;
- NON_CERT_METADATA_ONLY, if the XML changes without a relation-state change.

No assumption is made before execution that the commit is purely certainty-only.

## Current task Q0

For each printed target, recover the complete multiset of relation endpoints while ignoring certainty.

Report whether Q0 is identical parent -> child.

If Q0 changes, the experiment retains that result and separates endpoint revision from certainty revision.

## Research-state representations

### R_FULL_BINDING

Parent state retains each logical relation identity with its certainty.

Input at revision time:
the natural parent->child relation delta only.

Goal:
apply changed/add/remove records while leaving all unaffected records untouched.

### R_ENDPOINT_ONLY

Parent state retains only the relation identities/endpoints, not certainty.

Input at revision time:
the same natural delta.

It may learn certainty for changed records from the delta, but it lacks the unchanged per-link epistemic state unless it reopens a source.

### R_LOCUS_STATUS

For each printed target retain:
- complete endpoint multiset;
- number of high links;
- number of low links;
- HIGH_ONLY / LOW_ONLY / MIXED status.

Do not retain endpoint -> certainty binding.

Input at revision time:
the same natural delta.

### R_SOURCE_REOPEN

Reopen the exact child relation file and reconstruct the complete child state.

This is the strong lawful baseline and receives full credit.

## Natural delta packet

The evaluator derives a relation-level patch from the exact parent and child source states.

The patch contains only records whose logical relation state changed, was added, or was removed.

For CERT_CHANGED it includes:
- relation identity;
- old certainty;
- new certainty.

This patch is evidence supplied by the natural Git revision event, not a hidden answer lookup.

## Selective revision criteria

For a representation arm after applying the natural delta:

### Changed-target correctness

Every CERT_CHANGED relation has the child certainty.

### Unaffected stability

Every UNCHANGED relation retains exactly the parent certainty.

### Endpoint correctness

The final endpoint multiset equals the child endpoint multiset.

### No collateral revision

No relation outside the natural delta changes certainty, identity, presence, or absence.

### Complete epistemic-state exactness

The final relation identity -> certainty multiset equals the child state.

R_ENDPOINT_ONLY and R_LOCUS_STATUS may safely return unresolved endpoint-specific certainty where their retained state is non-determining. Such safe incompleteness is not counted as a false certainty assignment.

## Controlled wrong-binding test

If at least two CERT_CHANGED relations exist, construct a size/interface-matched wrong patch by permuting the new certainty assignments among changed relation identities while preserving:
- the set of changed identities;
- the multiset of old certainty values;
- the multiset of new certainty values;
- patch cardinality.

Apply this only if the permutation yields a different child state.

If no such permutation exists, report WRONG_BINDING_CONTROL_NOT_IDENTIFIABLE rather than inventing one.

## Metrics

- parent relation count;
- child relation count;
- CERT_CHANGED / UNCHANGED / ADDED / REMOVED counts;
- number of printed targets affected;
- Q0 endpoint task parent/child equality;
- changed-target correctness;
- unaffected stability;
- collateral changes;
- complete child-state exactness by representation arm;
- safe unresolved endpoint-specific statuses;
- source-reopen bytes;
- delta packet bytes;
- full-state bytes;
- dependency-aware counts by printed target and manuscript file.

## Dispositions

NATURAL_EPISTEMIC_REVISION_OBSERVED:
at least one natural CERT_CHANGED relation exists.

SELECTIVE_REVISION_FULL_BINDING:
R_FULL_BINDING reaches the exact child state with zero collateral changes.

AGGREGATE_STATUS_NONDETERMINING:
R_LOCUS_STATUS cannot uniquely recover the child endpoint-specific epistemic state for at least one affected locus.

SOURCE_REOPEN_EXACT:
R_SOURCE_REOPEN reconstructs the child state exactly.

WRONG_BINDING_FAILS:
only if an identifiable matched wrong patch exists and fails.

## Claim ceiling

A positive result can support:

> In a real editorial revision of the Whitman relation inventory, per-relation epistemic statuses changed selectively while unaffected relation claims remained stable. A representation retaining relation-specific status binding, or lawful reopening of the revised source object, can reproduce that selective revision; coarser endpoint/status summaries may not.

It cannot establish:
- that the child judgement is historically truer than the parent;
- that every editorial revision is selective;
- human consensus;
- independent transfer beyond the already-exposed Whitman ecology;
- a universally minimal representation.

## Stop rule

Do not choose a different Whitman commit after opening this diff merely because the frozen event is small, null, or awkward.

If the commit contains no relation-certainty revision, report a natural null and move to a separately frozen candidate.
