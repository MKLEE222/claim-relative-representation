# Module P — evidence-release-induced scholarly revision charter v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / POST-AMP DEVELOPMENT CHARTER.

## 1. Motivation

The existing Module-I dynamic task studies one specific regime:

    visible t0 ambiguity/conflict
    -> unsupplied live question
    -> lawful evidence acquisition
    -> warrant update

That regime remains valid and is not reinterpreted.

Authoritative fresh Module O on AMP produced:

    48 valid primary scholarly objects
    0 D1/D2 discovery-eligible objects
    0 full trajectories

Post-hoc development analysis then showed that AMP contains a different real editorial regime:
later admissible origin evidence can materially change a previously determinate or unresolved
state even though no t0 root ambiguity exists.

Module P therefore defines a separate scholarly task rather than patching Module O.

AMP is exposed development data only and can never confirm Module P.

## 2. Humanities task

The task is:

> Maintain a source-grounded scholarly state when new admissible evidence is released after the
> current state has already been formed. Determine whether the evidence applies to the same
> scholarly object and claim, update only the warranted portion of the state, preserve unresolved
> alternatives when required, retain provenance, and preserve enough transition history for a
> later scholar to reconstruct why the state changed.

The research question is not:

    can the system invent a question from current ambiguity?

It is:

    can a scholarly knowledge state remain warranted and historically auditable when a new
    evidence event changes what may responsibly be claimed?

This is a Digital Humanities/editorial-history task.

## 3. Event model

Let:

    S0 = current scholarly state
    E  = a later evidence-release event
    e  = the source-grounded claim carried/revealed by E
    S1 = post-event scholarly state

E is externally released under a declared workflow.
It does not require D1/D2 question discovery.

The event is admissible only if the frozen object/source/claim applicability contract authorizes
e for S0.

No content-based search for favorable evidence is part of the event contract.

## 4. Primary eligibility

A document/event pair is ERIR-eligible only if all are true:

1. one valid scholarly object exists under the frozen portable object grammar;
2. S0 has a well-defined contracted warrant, which may be:
   - EXACT;
   - INTERVAL;
   - OPEN_INTERVAL;
   - ALTERNATIVE_SET;
   - UNRESOLVED;
3. exactly one admissible later evidence claim is available behind the declared evidence-release
   handle;
4. the later evidence is bound to the same source/object applicability contract;
5. adding the evidence produces a substantive warrant-state change.

No minimum number of t0 root claims is required.

## 5. Substantive warrant change

Eligibility must not be created merely because a different claim key becomes the basis of an
otherwise identical warrant.

Define a claim-key-insensitive scholarly warrant projection Phi(W).

For:

    EXACT / INTERVAL / OPEN_INTERVAL

Phi keeps:
- warrant type;
- represented interval.

For:

    ALTERNATIVE_SET

Phi keeps the multiset of:
- claim role/class;
- represented interval;

and removes claim-key identity.

For:

    UNRESOLVED

Phi keeps:
- warrant type;
- registered unresolved reason class.

A later event is substantively state-changing only when:

    Phi(W_root) != Phi(W_post)

This explicitly excludes basis-only replacement.

## 6. Registered transition classes

Development and future holdout results must classify eligible events into one of:

### P-U1 CONFLICT_FORMATION

Example:

    EXACT
    -> ALTERNATIVE_SET

A later source-grounded claim challenges a previously determinate state.

### P-U2 RESOLUTION_OR_ACQUISITION

Example:

    UNRESOLVED
    -> EXACT / INTERVAL / OPEN_INTERVAL

Later evidence makes a previously unwarranted state researchable.

### P-U3 NARROWING_OR_QUALIFICATION

Examples:

    OPEN_INTERVAL -> INTERVAL
    INTERVAL -> narrower INTERVAL
    EXACT -> INTERVAL
    exact/interval -> qualified alternative state

### P-U4 ALTERNATIVE_REVISION

The live alternative set changes without unjustified collapse.

Any unclassified state transition is retained as OTHER and does not silently enter the primary
mechanism denominator until separately interpreted.

## 7. Core scholarly obligations

Module P does not invent a new representation vocabulary.

It reuses the already frozen obligation set:

- O1 ObjectIdentity;
- O2 ClaimApplicability;
- O4 ResultDeterminacy;
- O5 Selectivity;
- O6 ProvenancePreservation;
- O7 TransitionCompatibility;
- O8 HistoryRetention.

O3 TargetDeterminacy becomes mandatory when Module P is later generalized to proposition-level
non-temporal revisions.

The task asks whether these obligations survive a different transition regime, not whether more
metadata improves a score.

## 8. Required positive capabilities

For every eligible event, the retained interface must support:

P1 CURRENT_STATE_BEFORE
- recover Phi(W_root).

P2 EVENT_APPLICABILITY
- authorize/reject E before mutation using frozen source/object/claim bindings.

P3 POST_EVENT_RESULT
- recover exact contracted W_post including alternatives/uncertainty.

P4 SELECTIVE_UPDATE
- no unrelated temporal/scholarly state is silently rewritten.

P5 PROVENANCE
- later scholars can recover the evidence item and source locator that licensed the transition.

P6 TRANSITION_ATTRIBUTION
- event, object, evidence and before/after states are bound.

P7 DELAYED_HISTORY
- a later audit can reconstruct why the current state differs from S0.

## 9. Strong comparators

Reuse the Module-M comparator distinction.

### B_CURRENT_REOPEN

May recover the current/latest post-event state and current provenance.

It has no durable pre-event transition record.

### B_ORDERED_SNAPSHOTS

May retain exact ordered S0/S1 snapshots and exact state deltas.

It does not receive transition semantics or event-to-evidence authorization by definition.

These baselines remain strong only if their registered positive capabilities pass.

No scalar winner score is permitted.

## 10. Development controls

Before any new fresh corpus is opened, Module P must pass synthetic controls for at least:

P-F1 VALID_CONFLICT_FORMATION
- one root exact claim + disjoint later evidence -> ALTERNATIVE_SET.

P-F2 VALID_UNRESOLVED_TO_WARRANTED
- no machine root warrant + one admissible later evidence -> warranted state.

P-F3 BASIS_ONLY_NOT_ELIGIBLE
- later evidence with the same substantive warrant projection does not create an ERIR episode.

P-F4 WRONG_OBJECT_REJECTED
- evidence bound to another object cannot mutate the state.

P-F5 WRONG_SOURCE_VERSION_REJECTED
- stale/foreign evidence cannot mutate the state.

P-F6 MISSING_APPLICABILITY_REJECTED
- visible evidence without applicability proof cannot mutate the state.

P-F7 COLLATERAL_MUTATION_DETECTED
- a valid event plus unrelated state mutation fails selectivity.

P-F8 NO_HISTORY_SEPARATION
- final result remains correct while delayed history fails.

P-F9 SNAPSHOT_NONIDENTIFIABILITY
- two different registered event histories yielding identical S0/S1 state sequences are
  indistinguishable to the frozen ordered-snapshot comparator but distinguishable to retained
  transition history.

P-F10 NULL_EVENT
- admissible evidence whose Phi(W) does not change must not be promoted to a substantive revision
  episode.

## 11. AMP role

AMP may be used only for exposed development to:
- test implementation portability;
- classify P-U1/P-U2/P-U3/P-U4 distributions;
- audit whether the event interpretation matches source encoding;
- discover implementation bugs before any future fresh run.

AMP may not be used for:
- prospective confirmation;
- fresh prevalence;
- holdout tuning presented as confirmation.

The authoritative Module-O NULL remains unchanged.

## 12. Fresh confirmation requirement

A future Module-P confirmatory corpus must be independent and unexposed at event level.

Before opening it, project-level documentation must prospectively establish:
- a closed scholarly-object population;
- an initial/current claim layer;
- an independently represented later evidence/revision layer;
- provenance sufficient for source audit.

The future holdout population and event-release rule must be frozen before episode content is
opened.

If N_eligible = 0, report applicability null.

## 13. Relation to the mother problem

Module I asks:

    can representation support inquiry when ambiguity is already visible?

Module P asks:

    can representation support warranted scholarly revision when new evidence changes the state?

Together they test two distinct ways researchability must persist across time:

    ambiguity-driven question emergence

and

    evidence-driven knowledge revision.

Neither task alone is the whole mother problem.

## 14. Claim ceiling

Even if Module P later passes a fresh holdout, it supports only a task-relative claim about
source-grounded scholarly revision.

It does not establish universal necessity for all humanities infrastructures.

A second non-temporal event family remains required before claiming event-family generality.
