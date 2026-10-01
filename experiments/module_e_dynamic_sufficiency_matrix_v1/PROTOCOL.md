# Module E v1 — Distributed information obligations for warranted selective revision

Date frozen: 2026-09-28
Status: CONTROLLED CHANNEL-ABLATION STUDY AROUND TWO ALREADY-OBSERVED NATURAL WHITMAN REVISION EVENTS. NOT INDEPENDENT TRANSFER.

## Purpose

Modules D1/D2 showed that natural selective editorial revision is real, but also that an identity-rich revision patch can compensate for bindings omitted from the retained pre-state.

Module E asks the causal question:

> How may the information required for exact and auditable selective revision be distributed across retained state, incoming revision evidence, and lawful child-source access?

The natural D1/D2 parent and child states are held fixed. Only the information interface is projected.

## Natural events held fixed

### E_D1
- parent: 7cdf5ddc9d0cfff83289f687613ee3d0510e6520
- child: fe63fcfbeca16f85583a29355c2d3a44e09b280f
- natural delta already observed: 1 certainty change, 0 add, 0 remove.

### E_D2
- parent: fe63fcfbeca16f85583a29355c2d3a44e09b280f
- child: 8c6aba338bd3b8a52ec74d014ec1afc8137cc4a9
- natural delta already observed: 141 certainty changes, 7 add, 8 remove.

These outcomes are development knowledge. Module E is not a blind replication.

## Unit and state domain

Logical relation identity:

    (print_target, manuscript_file, manuscript_local_target)

Certainty domain in the frozen source:

    {high, low}

Primary unit for finite determinacy:

    one printed target (locus)

All exactness claims are also summarized over the complete relation object.

## Retained-state arms

All state arms preserve the current parent endpoint task Q0.

### S_FULL
Retain the complete parent endpoint -> certainty binding.

### S_LOCUS_COUNTS
For every printed target retain:
- complete parent endpoint set;
- number of high relations;
- number of low relations;
- HIGH_ONLY / LOW_ONLY / MIXED status.

Remove endpoint -> certainty binding.

### S_ENDPOINTS
Retain only the complete parent endpoint set.

Remove all parent certainty information.

## Event-channel arms

Each channel is a controlled projection of the same complete natural parent->child delta.

Channels are complete within their declared projection: a locus absent from the event packet is declared unchanged.

### E_LINK_FULL
For every natural delta record retain:
- exact relation identity;
- operation type;
- old certainty when applicable;
- new certainty when applicable.

### E_LINK_NEW
For every natural delta record retain:
- exact relation identity;
- operation type;
- new certainty for CERT_CHANGED and ADDED_RELATION;
- no old certainty.

For REMOVED_RELATION retain exact relation identity but no old certainty.

This channel can prescribe a child update but may not by itself establish the pre-revision epistemic state.

### E_LOCUS_OPERATION_BAG
For each affected printed target retain only the multiset/counts of operation types and certainty transitions:
- number of high->low changes;
- number of low->high changes;
- multiset of certainties of added relations;
- multiset of certainties of removed relations.

Remove the binding from every operation to a relation identity.

The endpoint universe used for exact finite enumeration is conservatively bounded to the union of natural parent and child endpoints at that locus. This gives the weak channel more candidate identity information than a real unlabeled notice would normally provide; ambiguity under this bounded universe is therefore a strong separation witness.

## Access arms

### A_NONE
No child-source reopening.

### A_CHILD_REOPEN
The exact pinned child relation source may be lawfully reopened.

This makes the child state available, but does not automatically reveal the parent endpoint-certainty binding or the exact transition history when retained parent state/event information is insufficient.

## Full factorial

For each natural event execute:

    3 retained-state arms
  x 3 event-channel arms
  x 2 access arms
  = 18 interfaces

Total:

    36 event/interface cells.

No cell may be removed because it is redundant or unfavorable.

## Candidate-state semantics

For every printed locus the evaluator enumerates all parent certainty assignments compatible with the retained-state arm.

It then enumerates all child states and parent->child transition signatures compatible with the selected event-channel arm.

If A_CHILD_REOPEN is enabled, candidate child states are additionally constrained to the exact pinned child source.

Candidate transition signature records:
- CERT_CHANGED(identity, old, new);
- ADDED_RELATION(identity, new);
- REMOVED_RELATION(identity, old);
- unchanged identities are the complement within the parent/child relation states.

## Tasks

### T_CHILD_LOCAL
For each naturally affected locus:

> Is the exact child endpoint+certainty state uniquely determined?

Report exact / ambiguous / incompatible.

### T_TRANSITION_LOCAL
For each naturally affected locus:

> Is the exact parent->child transition signature uniquely determined?

This is the primary auditability criterion.

A child state can be exact while the transition remains ambiguous.

### T_CHILD_GLOBAL

> Is the exact complete child relation state uniquely determined across every locus?

This penalizes state arms that cannot recover unchanged background certainty, even if the natural event-local update is determined.

### T_UNAFFECTED_STABILITY_AUDIT

> Can the interface uniquely establish that every relation outside the natural delta retained its parent epistemic state?

This is stronger than merely producing the correct child object.

## Primary separation hypotheses

H1 — Event identity can substitute for omitted pre-state binding:

    S_LOCUS_COUNTS + E_LINK_FULL

or E_LINK_NEW may determine affected-locus child states that S_LOCUS_COUNTS alone would not.

H2 — Operation bags are not generally equivalent to identity-bound deltas:

    E_LOCUS_OPERATION_BAG

should be non-determining whenever multiple relation identities can realize the same operation multiset.

H3 — Child reopening and transition audit are distinct:

    A_CHILD_REOPEN

may make T_CHILD exact while T_TRANSITION remains ambiguous under coarse parent/event interfaces.

H4 — Endpoint-only current-task sufficiency is not automatically dynamic sufficiency:

    S_ENDPOINTS

preserves parent Q0 but should leave unchanged epistemic background unresolved unless later information supplies it.

These are testable expectations, not success requirements.

## Strong controls

1. Natural parent/child source states are independently parsed with two implementations.
2. D1/D2 natural delta counts must reproduce their authoritative results before the matrix is evaluated.
3. Every channel projection is generated mechanically from the same natural delta.
4. A locus absent from a complete event packet is forced unchanged; the evaluator may not invent hidden revisions.
5. No post-outcome aliasing, fuzzy matching, extra source, or channel-specific heuristic is permitted.

## Metrics

For every event/interface cell report:
- affected loci child-exact count;
- affected loci child-ambiguous count;
- affected loci transition-exact count;
- affected loci transition-ambiguous count;
- global child exactness;
- unaffected-stability audit exactness;
- maximum and total candidate counts (capped only for display, never for determination);
- canonical retained-state bytes;
- canonical event-channel bytes;
- child-source bytes if reopening is enabled.

Also report minimal successful cells only descriptively under this finite experiment. Do not call them globally minimal representations.

## Dispositions

EVENT_CHANNEL_BINDING_SEPARATION:
at least one event/state/access pair is child- or transition-determining under an identity-bound channel but non-determining under E_LOCUS_OPERATION_BAG.

REOPEN_CHILD_NOT_TRANSITION:
at least one A_CHILD_REOPEN cell has exact child state but ambiguous transition audit.

CURRENT_TASK_NOT_DYNAMIC_SUFFICIENCY:
at least one S_ENDPOINTS cell preserves Q0 but is non-determining for exact dynamic child or transition state.

DISTRIBUTED_SUFFICIENCY_OBSERVED:
multiple distinct combinations of state/event/access information reach the same exact warranted update, showing substitution of information obligations across interface components.

## Claim ceiling

A positive study can support only:

> For these two real Whitman editorial revisions, exact selective update and exact auditability depend on the information jointly available from retained state, the revision channel, and lawful source access. Identity-rich revision evidence can substitute for some omitted pre-state binding, while aggregate operation notices can remain non-determining; reopening a child source can recover the child state without necessarily recovering the transition history.

It cannot establish:
- a universal minimal dynamic representation;
- that Git diffs are the correct event channel for every scholarly system;
- that the child editorial judgement is historically truer;
- independent transfer outside the exposed Whitman ecology;
- general human scholarly behavior.

## Stop rule

Run the complete 36-cell matrix once.

Do not add a fourth event channel or new state arm after seeing the outcome to manufacture a separation.

Any later cross-domain transfer of the dynamic-sufficiency result must be separately frozen.