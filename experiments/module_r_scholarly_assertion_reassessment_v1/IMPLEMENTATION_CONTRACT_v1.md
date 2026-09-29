# Module R implementation contract v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-RESULT.

## 1. Abstract development representation

Module R synthetic hardening uses an encoding-neutral assertion state.

A live assertion record contains:

- claim_id;
- object_id;
- target_property;
- value;
- status;
- applicability_class;
- source_repository;
- source_version;
- source_id;
- source_locator;
- responsible_agent.

The scientific state projection Psi removes claim_id and storage ordering but preserves:

- object_id;
- target_property;
- value;
- status.

For an alternative set, Psi preserves the canonical sorted set of projected assertions.

## 2. Event

A reassessment event contains:

- event_id;
- event_class;
- object_id;
- target_property;
- source_repository;
- source_version;
- evidence_id;
- evidence_locator;
- responsible_agent;
- applicability_class;
- operation;
- proposed value;
- proposed status.

Registered operations:

- REPLACE;
- ADD_ALTERNATIVE;
- REVISE_STATUS;
- RESOLVE.

## 3. Admission rule

Before mutation, an event is applicable only if all are true:

- event object_id == state object_id;
- event target_property exists in the registered task contract;
- source repository/version match state source context;
- applicability_class == ASSERTION_LEVEL_ADMISSIBLE;
- evidence_id and evidence_locator are nonempty.

A rejected event must not mutate Psi(state).

## 4. Transition semantics

### REPLACE

Replace the live assertion set for the target with one new assertion.

### ADD_ALTERNATIVE

Add a new assertion as a live alternative without deleting the existing assertion(s).

### REVISE_STATUS

Replace status for the same literal value while preserving the target/value identity.

### RESOLVE

Replace UNRESOLVED or an alternative set with one new qualified assertion.

## 5. Null discipline

An admitted event is a substantive reassessment only if:

    Psi(S0) != Psi(S1)

A new claim_id, changed responsible_agent or storage-only metadata is not substantive unless the
declared task includes that attribute.

R-F13 and R-F14 enforce this.

## 6. Provenance and transition history

The retained runtime stores:

- evidence ledger;
- event ledger;
- transition ledger.

Each transition stores:
- event id/class;
- object;
- target property;
- evidence id;
- before Psi/state;
- after Psi/state;
- changed targets;
- collateral targets.

Delayed history is computed only from these ledgers.

## 7. Strong comparator budgets

### B_CURRENT_REOPEN_R

Visible:
- final assertion state;
- current live assertion provenance.

Hidden:
- S0;
- event;
- evidence-to-event transition record.

### B_ORDERED_SNAPSHOTS_R

Visible:
- complete S0 and S1;
- exact state delta;
- current live assertion provenance.

Hidden:
- event semantics;
- evidence-to-event authorization.

### B_CHANGE_LOG_NO_JUSTIFICATION_R

Visible:
- event/change id;
- event time/order;
- object;
- target property;
- exact old/new diff.

Hidden:
- evidence_id;
- evidence_locator;
- justification/source relation;
- evidence applicability proof.

This comparator is intentionally stronger than snapshots for event identity and target, but weaker
than the retained transition record for scholarly justification.

## 8. Oracle/runtime separation

oracle_r.py and runtime_r.py must independently implement:
- Psi;
- event applicability;
- transition semantics;
- transition classification.

They may share only plain fixture data and canonical serialization helpers.

The evaluator compares runtime outcomes against oracle outcomes.

## 9. Synthetic fixture set

### F1 Attribution replacement

S0:
    target=author-attribution, A, ACCEPTED

E:
    evidence supports B, operation=REPLACE

S1:
    B, ACCEPTED

### F2 Alternative formation

S0:
    A, ACCEPTED

E:
    competing evidence supports B, operation=ADD_ALTERNATIVE

S1:
    {A, B}

### F3 Evidential-status revision

S0:
    value=A, status=DIRECT

E:
    reassessment of source transmission, operation=REVISE_STATUS

S1:
    value=A, status=MEDIATED

### F4-F7 binding failures

Wrong object / wrong target / wrong source version / missing applicability.

### F8 provenance-surface removal

Execution remains valid, but current provenance is removed from the scholar-visible result.

### F9 collateral mutation

A valid event also mutates unrelated target_property.

### F10 history drop

Execution/post-state remains correct; transition ledger removed before delayed audit.

### F11 snapshot non-identifiability

Two different evidence/assessment histories produce identical S0/S1.

### F12 change-log no justification

The comparator knows exact target and diff but no evidence source/reason.

### F13 basis-only null

Only claim_id/responsibility/storage identity changes.

### F14 admitted null reassessment

Event proposes same task-relevant value/status as current state.

## 10. Evaluation tasks

R1 PRE_STATE_EXACT
R2 TARGET_DETERMINACY
R3 EVENT_APPLICABILITY
R4 POST_EVENT_RESULT
R5 SELECTIVE_UPDATE
R6 PROVENANCE
R7 TRANSITION_ATTRIBUTION
R8 DELAYED_HISTORY

No scalar score.

## 11. Gate

Synthetic Module R passes only if:

- positive F1-F3 pass R1-R8;
- F4-F7 reject without Psi mutation;
- F8 isolates provenance loss;
- F9 isolates selectivity failure while transition record remains available;
- F10 preserves result/selectivity but fails delayed history;
- F11 establishes snapshot observational equivalence;
- F12 shows target/diff change log does not determine evidence justification;
- F13/F14 remain outside substantive reassessment denominator.

No natural/fresh data is opened before this gate.
