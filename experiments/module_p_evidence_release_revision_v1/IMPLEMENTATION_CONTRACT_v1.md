# Module P implementation contract v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-RESULT.

This file operationalizes CHARTER_v1 without changing its scientific meaning.

## 1. Parser inheritance

Module P does not create a new TEI parser.

It consumes the already frozen portable Module-L parsed document objects.

Thus object selection, temporal-carrier extraction, source binding, claim applicability,
origin-handle construction and raw temporal normalization are inherited unchanged.

New scientific decisions introduced by Module P are implemented independently in oracle_p.py
and runtime_p.py:
- scholarly warrant projection Phi;
- ERIR eligibility;
- transition-class assignment.

No shared helper may encode those three decisions.

## 2. Exact Phi definition

### EXACT / INTERVAL / OPEN_INTERVAL

Phi(W) is:

    {
      "type": W.type,
      "interval": W.interval
    }

Claim-key basis identity is removed.

### ALTERNATIVE_SET

Each alternative is projected to:

    {
      "role": alternative.role,
      "interval": alternative.interval
    }

The projected alternatives are sorted canonically by:

    role, lower-bound, upper-bound

Phi(W) is:

    {
      "type": "ALTERNATIVE_SET",
      "alternatives": sorted projected alternatives
    }

Claim keys are removed.

### UNRESOLVED

Phi(W) is:

    {
      "type": "UNRESOLVED",
      "reason_class": normalized unresolved reason
    }

Reason normalization is intentionally conservative:
- no-machine/root-empty reasons -> NO_MACHINE_TEMPORAL_CARRIER;
- object-contract reasons remain their existing object-status class;
- every other nonempty reason is retained literally.

### Unknown warrant type

Phi returns the type and all non-claim-key public value fields.
Such an episode is transition-class OTHER unless a registered class applies.

## 3. ERIR eligibility

ERIR_ELIGIBLE is true only if all are true:

E1.
    object_contract.status == SINGLE_PRIMARY_DOCUMENT_OBJECT

E2.
    exactly one admissible later origin claim exists:
    origin_contract_status == SINGLE_ORIGIN_ADMISSIBLE

E3.
    origin claim has:
    - object_id equal to selected object;
    - object_boundary_signature equal to selected boundary;
    - applicability_class == FILE_LEVEL_UNIQUE_OBJECT;
    - source repository/version/population equal to document source context.

E4.
    Phi(W_root) != Phi(W_post)

No D1/D2 trigger is required.

A document satisfying E1-E3 but not E4 is:

    ADMISSIBLE_NULL_EVENT

and is excluded from the substantive-revision denominator rather than counted as a failure.

## 4. Event request

The runtime receives a declared external event request:

    {
      "type": "EVIDENCE_RELEASE_REVISION",
      "event_class": "EVIDENCE_RELEASE",
      "object_id": selected object id,
      "target_document": path
    }

This request is not discovered from root ambiguity.

It authorizes only an attempt to open the already frozen origin handle.
The existing Module-L binding checks remain authoritative.

## 5. Transition class

Classes are determined from Phi(W_root) and Phi(W_post).

### P-U1 CONFLICT_FORMATION

Any transition where:
- pre type is EXACT / INTERVAL / OPEN_INTERVAL;
- post type is ALTERNATIVE_SET;
- at least one post alternative is not substantively represented in the pre state.

### P-U2 RESOLUTION_OR_ACQUISITION

Pre:
    UNRESOLVED

Post:
    EXACT / INTERVAL / OPEN_INTERVAL / ALTERNATIVE_SET

### P-U3 NARROWING_OR_QUALIFICATION

Non-unresolved, non-alternative transitions with different Phi values, including:
- OPEN_INTERVAL -> INTERVAL / EXACT;
- INTERVAL -> narrower INTERVAL / EXACT;
- EXACT -> INTERVAL / OPEN_INTERVAL.

No assumption is made that every P-U3 transition is epistemically "better"; the label only
denotes changed qualification/resolution structure.

### P-U4 ALTERNATIVE_REVISION

Pre:
    ALTERNATIVE_SET

Post:
    ALTERNATIVE_SET

and projected alternative multisets differ.

### OTHER

Every substantive Phi change not matched above.

OTHER is retained in descriptive counts but is not silently treated as one of P-U1-P-U4.

## 6. Runtime execution

For an ERIR-eligible or admissible-null document:

1. construct I_RSTAR portable state;
2. do NOT call ambiguity discovery;
3. construct the external event request;
4. call the existing portable apply_open_origin binding/action implementation;
5. execute the frozen neutral event;
6. retain/drop history according to intervention;
7. return before/post/final state and audit.

Module P therefore changes activation semantics, not evidence-binding semantics.

## 7. Required evaluator

P1 CURRENT_STATE_BEFORE
    runtime Phi(root) == oracle Phi(root).

P2 EVENT_APPLICABILITY
    valid event is accepted; registered wrong-object/source/applicability controls rejected.

P3 POST_EVENT_RESULT
    exact post warrant and Phi(post) equal oracle.

P4 SELECTIVE_UPDATE
    zero collateral paths for valid retained execution.

P5 PROVENANCE
    admitted evidence key/source locator/object/source context exactly bound.

P6 TRANSITION_ATTRIBUTION
    event class/id, target object/document, evidence key, before/after warrant exact.

P7 DELAYED_HISTORY
    later audit reconstructs event/evidence and before/after states.

No scalar score is computed.

## 8. Synthetic fixtures

P-F1:
    one sent exact 1900-01-01;
    origin exact 1900-01-02;
    no second root temporal carrier.

P-F2:
    no machine-readable root temporal claim;
    origin exact 1900-01-02.

P-F3/P-F10:
    one sent exact 1900-01-01;
    origin exact 1900-01-01;
    Phi unchanged.

P-F4:
    mutate external event/object binding only.

P-F5:
    mutate source version only.

P-F6:
    remove origin applicability proof only.

P-F7:
    valid event plus collateral root mutation.

P-F8:
    retained post result with transition ledger dropped before delayed audit.

P-F9:
    same S0/S1 snapshots paired with two distinct event-semantic histories.

## 9. Exposed AMP development run

Only after P-F1-P-F10 pass.

Freeze AMP source context exactly as Module O:
- Auden-Musulin-Papers/amp-data;
- commit 289a52de61aef0b6354e3c8298173bf1f889feb2;
- data/editions/;
- 73 XML.

Report:
- valid objects;
- admissible later evidence;
- admissible-null events;
- substantive ERIR eligible events;
- P-U1/P-U2/P-U3/P-U4/OTHER counts;
- P1-P7 retained-interface results;
- Module-M comparator capability vectors;
- selected obligation interventions.

AMP results are explicitly exposed development evidence.

## 10. No result-driven amendments

If AMP reveals an unexpected transition class or source structure:
- record it;
- classify as OTHER/unresolved;
- do not modify this contract to make it pass.

Any new interpretation belongs to a later version.
