# Module R — scholarly assertion reassessment charter v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-FRESH-DATA CHARTER.

## 1. Purpose

Modules I/P establish two temporal activation regimes:
- ambiguity-triggered inquiry;
- evidence-release-induced revision.

A strong Digital Humanities contribution must show that the same researchability obligations are
not artifacts of dating.

Module R defines a second, non-temporal event family:

    source-grounded scholarly assertion reassessment

Examples include:
- attribution revision;
- source-status revision;
- identification revision;
- responsibility revision;
- direct-vs-mediated evidence reclassification;
- qualified acceptance / alternative formation.

The task is derived from neighboring scholarly provenance models, but the present experiment does
not require adopting any one ontology.

## 2. Near-neighbor design basis

The event model is informed by three established neighboring ideas.

### A. TEI change targeting

TEI change records can identify a change activity and point to the element(s) affected by that
change.

Design consequence:
a revision event must have an explicit scholarly target; an unbound change log entry is
insufficient for proposition-level reassessment.

### B. CIDOC CRM E13 Attribute Assignment

E13 treats making an assertion about a property/relation as an activity, making it possible to
document how an assignment came about and whose opinion it was.

Design consequence:
the old/new assertion values alone are insufficient for the strongest history task; the
assignment/reassessment activity is itself a scholarly object of record.

### C. CRMinf argumentation / belief adoption / provenance assessment

CRMinf distinguishes evidence sources, adopted beliefs, provenance beliefs/assessments and
argumentation activities.

Design consequence:
Module R explicitly distinguishes:

    evidence object
    -> assessment/adoption activity
    -> proposition/assertion state

rather than reducing revision to:

    old value -> new value.

These neighboring models motivate the task but do not pre-establish the empirical necessity of
the present obligation set.

## 3. Scholarly state

For one declared scholarly object O and one declared proposition/property target P:

    S0 = current scholarly assertion state about P(O)

A state can be:
- SINGLE_ASSERTION(value, status);
- ALTERNATIVE_SET(values/statuses);
- UNRESOLVED;
- QUALIFIED_ASSERTION(value, modality/status).

Each live assertion may carry:
- assertion/claim identifier;
- object target;
- proposition/property target;
- value;
- modality/status;
- source/provenance;
- responsible actor/editor where available.

## 4. Reassessment event

A later evidence/assessment event E contains or authorizes:

- event_id;
- event_class;
- target object O;
- target proposition/property P;
- evidence source(s);
- evidence/source locator(s);
- assessing/adopting agent or responsibility record where available;
- asserted/reassessed value;
- assertion status/modality;
- source/context/version binding;
- optional justification/inference type.

The event may:
- replace a previously warranted assertion;
- qualify it;
- create an alternative set;
- resolve an unresolved state;
- reject a previously admitted assertion;
- change evidential status without changing the literal value.

## 5. Core distinction

A substantive reassessment is not merely a changed serialization or identifier.

Define a claim-key-insensitive assertion-state projection Psi(S).

Psi preserves:
- object target;
- proposition/property target;
- value(s);
- status/modality;
- alternative structure.

Psi removes:
- claim identifier;
- storage identifier;
- ordering not declared semantically significant.

An event is substantively state-changing only if:

    Psi(S0) != Psi(S1)

or if the literal value remains the same but the registered evidential/provenance status changes
in a way declared task-relevant before evaluation.

## 6. Registered transition classes

### R-U1 ATTRIBUTION_REPLACEMENT

Example:

    attributed_to(A)
    -> evidence reassessment
    -> attributed_to(B)

### R-U2 ALTERNATIVE_FORMATION

Example:

    attributed_to(A)
    -> competing evidence
    -> {A, B} as live alternatives

### R-U3 EVIDENTIAL_STATUS_REVISION

Example:

    DIRECT_SOURCE
    -> reassessment
    -> MEDIATED_SOURCE

or:
    accepted provenance
    -> disputed provenance

The literal proposition/value may remain unchanged while its warrant status changes.

### R-U4 RESOLUTION

Example:

    UNRESOLVED / ALTERNATIVE_SET
    -> assessment
    -> one qualified or accepted assertion

### R-U5 QUALIFICATION

Example:

    ACCEPTED
    -> PROBABLE / POSSIBLE / CONDITIONAL

### OTHER

Any substantive transition not matched above is retained but does not silently enter a named
primary class.

## 7. Researchability obligations under test

Module R reuses the existing obligations rather than inventing event-specific metadata.

Mandatory:
- O1 ObjectIdentity;
- O2 ClaimApplicability;
- O3 TargetDeterminacy;
- O4 ResultDeterminacy;
- O5 Selectivity;
- O6 ProvenancePreservation;
- O7 TransitionCompatibility;
- O8 HistoryRetention.

O3 becomes load-bearing in this family because the event must be bound to the exact proposition /
property being reassessed.

## 8. Required retained-interface capabilities

R1 PRE_STATE
- recover the registered pre-event assertion state.

R2 TARGET_DETERMINACY
- identify the exact proposition/property target.

R3 EVENT_APPLICABILITY
- authorize/reject the evidence/reassessment event before mutation.

R4 POST_EVENT_RESULT
- preserve exact resulting assertion/alternative/modality state.

R5 SELECTIVE_UPDATE
- unrelated assertions remain unchanged.

R6 PROVENANCE
- recover the evidence/source/responsibility basis for the reassessment.

R7 TRANSITION_ATTRIBUTION
- bind event, target, evidence, before state and after state.

R8 DELAYED_HISTORY
- reconstruct later why the current scholarly assertion differs from S0.

No scalar representation-quality score is allowed.

## 9. Strong comparators

### B_CURRENT_REOPEN

Receives the current/latest assertion state and current provenance.

Positive capability:
- current result;
- current provenance.

No prior state/event semantics.

### B_ORDERED_SNAPSHOTS

Receives complete ordered S0/S1 snapshots and exact assertion diff.

Positive capability:
- current result;
- current provenance;
- exact state delta.

No event/evidence authorization semantics.

### B_CHANGE_LOG_NO_JUSTIFICATION

New comparator motivated by TEI/version/provenance neighbors.

Receives:
- change/event identifier;
- time/order;
- target object/property;
- exact old/new assertion diff.

Does NOT receive:
- evidence source that licensed the reassessment;
- justification/inference relation;
- evidence-to-event authorization.

Purpose:
test whether recording that an editorial change occurred is sufficient for a later scholarly
audit when the reason/evidence for the change is absent.

This comparator must be frozen before any Module-R natural/fresh evaluation.

## 10. Primary scientific contrasts

### C-A state vs reassessment history

    current assertion recovery
    !=
    reassessment-history recovery

### C-B snapshot diff vs scholarly justification

    exact old/new assertion diff
    !=
    why the reassessment was warranted

### C-C change log vs evidence-grounded transition

    event/target/change record
    !=
    evidence-to-event justification

### C-D provenance vs target determinacy

Knowing the source does not substitute for knowing which proposition/property the source is
evidence for.

### C-E history vs result determinacy

A perfectly retained history does not substitute for preserving unresolved/qualified alternative
states correctly, and vice versa.

## 11. Synthetic hardening requirements

Before any natural fresh candidate is opened, implement at least:

R-F1 VALID_ATTRIBUTION_REPLACEMENT
- A -> B based on admissible evidence.

R-F2 VALID_ALTERNATIVE_FORMATION
- A -> {A,B}, with no unjustified collapse.

R-F3 VALID_EVIDENTIAL_STATUS_REVISION
- same literal proposition/value, but DIRECT -> MEDIATED or ACCEPTED -> DISPUTED.

R-F4 WRONG_OBJECT_REJECTED.

R-F5 WRONG_TARGET_PROPOSITION_REJECTED.

R-F6 WRONG_SOURCE_VERSION_REJECTED.

R-F7 MISSING_APPLICABILITY_REJECTED.

R-F8 PROVENANCE_MISSING_BUT_RESULT_INTACT
- current result remains correct while provenance audit fails.

R-F9 COLLATERAL_ASSERTION_MUTATION_DETECTED.

R-F10 NO_HISTORY_SEPARATION
- current result correct; delayed history fails.

R-F11 SNAPSHOT_NONIDENTIFIABILITY
- identical S0/S1 states compatible with different evidence/assessment histories.

R-F12 CHANGE_LOG_NO_JUSTIFICATION
- target and old/new diff known, but evidence-grounded justification cannot be reconstructed.

R-F13 BASIS_ONLY_NULL
- claim ID/responsibility storage change without Psi change is not promoted.

R-F14 NULL_REASSESSMENT
- admissible event with no task-relevant result/status change remains a null event.

## 12. Development evidence

Do not consume the reserved FRUS corpus for development.

Development must use:
- synthetic controls;
- already exposed historical/controlled assets;
- already exposed projects/cases where appropriate.

A natural exposed development set may be added only from already non-fresh sources.

## 13. Reserved fresh candidate: FRUS

HistoryAtState/frus is currently preserved as a possible fresh Module-R candidate.

Only:
- repository metadata;
- README;
- schema/frus.odd

have been inspected.

No volumes/*.xml file has been opened.

The generic ODD prospectively establishes:
- stable document object identifiers;
- source-visible document dates;
- editorially inferred/corrected normalized dates;
- explicit date/@ana evidence categories;
- editorialDecl/correction;
- revisionDesc/change;
- document source/provenance notes.

This resembles an editorial assessment/assignment ecology.

FRUS must remain unopened until:
1. Module-R synthetic controls are frozen and pass;
2. an FRUS-specific object/assertion adapter is frozen from ODD only;
3. the event/evidence release rule is frozen;
4. the full population rule and denominator are frozen;
5. source-audit rules are frozen.

## 14. Relation to Module Q

Module Q remains the fresh confirmation route for temporal ERIR under the Module-P family.

Module R is not a replacement for Q.

The two open burdens are therefore separate:

    Q = fresh independent confirmation of evidence-release-induced temporal revision

    R = second, non-temporal scholarly assertion/reassessment family

A positive result in one cannot silently substitute for the other.

## 15. Claim ceiling

Even a future fresh Module-R PASS would license only a task-relative result for one scholarly
assertion-reassessment ecology.

It would not establish universal necessity or prevalence.

The strongest intended synthesis is narrower:

    across distinct scholarly tasks and activation regimes, the same core representational
    distinctions can be tested for whether they preserve warranted, selective and historically
    auditable research action.
