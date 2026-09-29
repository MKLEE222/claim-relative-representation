# Qualified scholarly generator contract v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / EXPOSED-AND-SYNTHETIC-ONLY.

## 1. Problem resolved by this contract

The previous Module-R event surface supplied one of:

    REPLACE
    ADD_ALTERNATIVE
    REVISE_STATUS
    RESOLVE

as an input.

The generator de-exogenization audit established that this operation is not generally recoverable
from the represented pre-state/evidence surface and, for 7/10 audited episodes, is not even
recoverable from the complete before/after state pair.

This contract removes operation from the input.

## 2. Independent evidence-relation basis

The qualification layer uses the already frozen R3 earlier-vs-later contrast ontology:

    CONTRADICTS_PRIOR
    REPLACES_PRIOR
    NARROWS_PRIOR
    ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT
    CORROBORATES_PRIOR
    NO_VERIFIED_CONTRAST

These relations predate Module-R representation outcomes.

R3_UPDATE_CONTRAST_AMENDMENT_v4 requires them to be established from explicit earlier-layer
contrast. It specifically forbids treating a later statement as an update merely because the
later statement exists.

Therefore these relation labels are not renamed Module-R operations.

## 3. Full scholarly state and projections

A scholarly state S contains at least:

    assertions
    evidence_ledger
    event_ledger
    transition_ledger

Define:

    Psi(S)

as the current assertion projection inherited from Module R.

Define:

    Xi(S)

as the retained evidence/history projection:

    evidence_ledger
    event_ledger
    transition_ledger

Two states may satisfy:

    Psi(S0) = Psi(S1)

while:

    Xi(S0) != Xi(S1)

Such a transition is an assertion-state identity, not a full scholarly-state identity.

## 4. Operation-free evidence input

A qualified evidence input contains:

    event_id
    event_class
    object_id
    target_property
    source_repository
    source_version
    evidence_id
    evidence_locator
    responsible_agent
    applicability_class
    evidence_relation
    new_claim_id
    value
    status

It contains no operation field.

## 5. Generator vocabulary

The qualified generator vocabulary is:

    RECORD_EVIDENCE
    REPLACE
    ADD_ALTERNATIVE
    REVISE_STATUS
    RESOLVE

RECORD_EVIDENCE is first-class.

It records an admissible evidence intervention and its justification/history without changing
the current assertion projection.

## 6. Binding gate

If any of the following fails, Gamma(S,e) is empty:

- object identity;
- registered target;
- source repository;
- source version;
- ASSERTION_LEVEL_ADMISSIBLE;
- nonempty evidence id;
- nonempty evidence locator;
- registered evidence relation.

This preserves the existing object/applicability/source obligations.

## 7. State predicates

For the target assertion set A(S,target), define:

    SAME_PAIR
        proposed value and proposed status already occur together.

    SAME_VALUE
        proposed value occurs, regardless of status.

    SINGLE_UNRESOLVED
        exactly one live assertion exists and either:
        - status = UNRESOLVED; or
        - value = NO_EXPLICIT_ASSIGNMENT.

    ALTERNATIVE_STATE
        more than one live assertion exists.

## 8. Qualification relation Q(S,e,g)

Qualification must return exactly zero or one generator.

### 8.1 CORROBORATES_PRIOR

If SAME_PAIR:

    RECORD_EVIDENCE

Otherwise:

    relation-state mismatch / no generator.

### 8.2 CONTRADICTS_PRIOR

If SAME_VALUE and proposed status differs from the live status:

    REVISE_STATUS

Else if proposed value is different from every live value and target is not SINGLE_UNRESOLVED:

    ADD_ALTERNATIVE

Otherwise:

    relation-state mismatch / no generator.

This distinguishes contradiction of the status of the same proposition from introduction of a
competing proposition.

### 8.3 REPLACES_PRIOR

If ALTERNATIVE_STATE and the proposed value matches exactly one live alternative:

    RESOLVE

Else if at least one live assertion exists:

    REPLACE

Otherwise:

    relation-state mismatch / no generator.

Thus the same evidence relation can select a different generator after the state changes.

### 8.4 NARROWS_PRIOR

If SAME_VALUE and the proposed status differs from the live status:

    REVISE_STATUS

Else if at least one live assertion exists:

    REPLACE

Otherwise:

    relation-state mismatch / no generator.

The source-grounded NARROWS_PRIOR relation supplies the semantic fact that the proposed value is
a refinement; the representation engine does not infer semantic subset relations from arbitrary
literal strings.

### 8.5 ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT

If SINGLE_UNRESOLVED:

    RESOLVE

Else if SAME_PAIR:

    RECORD_EVIDENCE

Otherwise:

    relation-state mismatch / no generator.

### 8.6 NO_VERIFIED_CONTRAST

No state-changing generator is authorized.

It is not silently promoted to RECORD_EVIDENCE because even the earlier/later relation is not
verified.

## 9. Generator execution

### RECORD_EVIDENCE

- Psi unchanged;
- evidence ledger gains the evidence;
- event ledger gains the qualified event;
- transition ledger records:
  - generator = RECORD_EVIDENCE;
  - assertion_identity = true;
  - history_nonidentity = true;
  - evidence relation and binding.

### REPLACE / ADD_ALTERNATIVE / REVISE_STATUS / RESOLVE

Execution follows the existing Module-R mutation semantics, but the chosen operation is produced
internally by Q rather than supplied by the event.

Every transition ledger entry records:
- qualified generator;
- evidence relation;
- before Psi;
- after Psi;
- evidence id;
- object/target/source bindings.

## 10. Historical recovery gate

Use the five already source-audited Yule-Cordier rows.

The engine receives:
- historical pre-state;
- later evidence proposal;
- contrast_type from r3_B02_B03_contrast_audit_v1.csv.

It does NOT receive:
- frozen Module-R operation;
- expected transition class.

Required qualified generators:

    YC1920E-0022 -> REVISE_STATUS
    YC1920E-0023 -> RECORD_EVIDENCE
    YC1920E-0024 -> ADD_ALTERNATIVE
    YC1920E-0030 -> RECORD_EVIDENCE
    YC1920E-0049 -> RESOLVE

The old operation label is held out and used only for retrospective comparison.

For the two old null cases, disagreement with old REPLACE is expected and scientifically
intentional: RECORD_EVIDENCE is the repaired first-order generator.

## 11. Synthetic recovery gate

Synthetic evidence relations are declared independently of operation:

    replacement case        -> REPLACES_PRIOR
    alternative case        -> CONTRADICTS_PRIOR
    status revision case    -> NARROWS_PRIOR
    basis-only null         -> CORROBORATES_PRIOR
    status-null             -> CORROBORATES_PRIOR

Required generators:

    REPLACE
    ADD_ALTERNATIVE
    REVISE_STATUS
    RECORD_EVIDENCE
    RECORD_EVIDENCE

## 12. False-positive gate

For every otherwise valid evidence input:

- wrong object;
- wrong target;
- wrong source version;
- missing applicability;
- unregistered evidence relation;

must produce:

    Gamma(S,e) = empty

and leave both Psi and Xi unchanged except for an explicit rejected diagnostic if the test harness
chooses to retain one outside the scholarly state.

No rejected event is admitted to evidence/history ledgers.

## 13. Composition gate

Initial state:

    S0 = accepted A

Evidence e1:

    relation = CONTRADICTS_PRIOR
    proposed = competing B

Qualification:

    Q(S0,e1) = ADD_ALTERNATIVE

yielding:

    S1 = {A,B}

Evidence e2:

    relation = REPLACES_PRIOR
    proposed = accepted B

At S0:

    Q(S0,e2) = REPLACE

At S1:

    Q(S1,e2) = RESOLVE

Therefore generator identity is state-dependent.

Required composition result:

    e1 ; e2

and:

    e2 ; e1

must both be executable when individually qualified, but must produce different qualified
generator sequences and different final full scholarly states.

This establishes non-commutative composition under state-dependent qualification.

## 14. Null/history gate

For RECORD_EVIDENCE:

    Psi(S0) = Psi(S1)

must hold.

Also:

    Xi(S0) != Xi(S1)

must hold.

Therefore the old binary term ADMISSIBLE_NULL_EVENT is refined into:

    ASSERTION_IDENTITY_HISTORY_NONIDENTITY

for qualified-generator theory.

This does not assert that every corroborative evidence item changes the immediately available
generator set.

It removes the incorrect inference that unchanged current assertions imply no scholarly action
occurred.

## 15. Independent implementations

Implement two independently coded qualification engines:

    qualified_oracle_v1
    qualified_runtime_v1

They may share only:
- frozen string constants;
- test fixtures.

They must not call each other's qualification function.

Agreement is required on:
- binding disposition;
- evidence relation;
- selected generator;
- before/after Psi;
- assertion-identity/history-nonidentity flags;
- final assertion state;
- retained evidence/history fields.

## 16. Decision rule

QUALIFIED_GENERATOR_REPAIR_PASS only if:

- historical generator recovery = 5/5;
- synthetic generator recovery = 5/5;
- oracle/runtime exact on all registered scientific surfaces;
- false-positive controls all reject before mutation;
- RECORD_EVIDENCE passes Psi-identity/Xi-nonidentity checks;
- state-dependent generator selection appears in the composition probe;
- the two sequence orders produce different qualified generator sequences and different final
  full scholarly states.

Otherwise the repair remains incomplete.

## 17. Claim ceiling

If passed, this licenses:

> For the audited evidence-relation vocabulary, scholarly transition generators can be selected
> from source-grounded earlier/later relations and current scholarly state without supplying the
> operation label itself; generator selection is state-dependent and sequential composition is
> non-commutative in the registered probe.

It does not license:
- universal completeness of the generator vocabulary;
- automatic natural-language extraction of evidence relations;
- general prevalence claims;
- a universal algebra for all scholarly revision.
