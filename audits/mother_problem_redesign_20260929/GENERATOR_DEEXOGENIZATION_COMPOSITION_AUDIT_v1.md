# Generator de-exogenization and composition audit v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / EXPOSED-AND-SYNTHETIC-ONLY.

## 1. Motivation

The current dynamic line establishes object/applicability/provenance/history obligations for
single scholarly transitions.

Module R, however, supplies the transition operation as part of the event:

    REPLACE
    ADD_ALTERNATIVE
    REVISE_STATUS
    RESOLVE

This creates a deeper identification question:

> Is the scholarly operation recoverable from the pre-state and evidence relation, or is it being
> supplied exogenously by the experimental contract?

The audit also tests whether current null events are true identities for future scholarly action,
and whether state-dependent composition already appears under the frozen semantics.

No new fresh data is consumed.

## 2. Objects of study

Primary:
- Module-R synthetic controls R-F1/R-F2/R-F3/R-F13/R-F14;
- the frozen five-row Yule-Cordier historical reassessment panel.

Secondary synthetic composition probes:
- alternative formation followed by resolution;
- basis-only/null evidence followed by a future competing claim.

VGW/AAD are not required for the first audit because the identification issue can be established
or falsified without reopening any external source.

## 3. Operation-free evidence surface

For an existing Module-R event E define:

    e_bar = E without the operation field.

Retain:
- object;
- target property;
- source repository/version;
- evidence id/locator;
- responsibility;
- applicability;
- proposed value;
- proposed status.

The frozen operation is used only as a held-out label for retrospective comparison.

## 4. Registered operation vocabulary

The audit does not invent new operations.

It uses the already frozen Module-R vocabulary:

    Omega = {
        REPLACE,
        ADD_ALTERNATIVE,
        REVISE_STATUS,
        RESOLVE
    }

## 5. Binding qualification independent of operation

An operation-free evidence surface is binding-admissible only if:
- object matches state object;
- target is registered;
- source repository/version match;
- applicability class is ASSERTION_LEVEL_ADMISSIBLE;
- evidence id/locator are nonempty.

These are inherited from Module R and do not use the held-out operation.

## 6. Structural operation qualification

For a binding-admissible (S, e_bar), define a conservative structural candidate set Gamma(S,e).

### REPLACE

Candidate iff:
- the target already has at least one live assertion.

### ADD_ALTERNATIVE

Candidate iff:
- the target has at least one live assertion;
- the target is not currently represented as a single UNRESOLVED assertion;
- the exact proposed (value,status) projection is not already live.

This prevents a duplicate assertion from being treated as a new alternative.

### REVISE_STATUS

Candidate iff:
- at least one live assertion at the target has the same literal value as the proposed value.

The status may remain the same; that produces a null event under the existing contract.

### RESOLVE

Candidate iff:
- the target is a single UNRESOLVED assertion; or
- the target currently contains more than one live alternative.

These rules are derived only from the existing Module-R operation descriptions.
They do not use the observed post-state or the held-out operation label.

## 7. Three identification levels

### G0-A — pre-state generator recovery

Compute:

    Gamma(S,e)

before looking at S1.

Classification:
- EMPTY: no structurally qualified generator;
- UNIQUE: exactly one generator;
- UNDERIDENTIFIED: more than one generator.

The held-out historical/synthetic operation is considered recovered only under UNIQUE.

### G0-B — phenotype-conditioned generator recovery

For each g in Gamma(S,e):
- execute g using the frozen Module-R transition semantics;
- compare Psi(g(S,e)) with the frozen observed Psi(S1).

Define:

    Gamma_match(S,e,S1)

as the candidate generators producing the observed scholarly state.

Classification:
- UNIQUE_PHENOTYPE: exactly one;
- UNDERIDENTIFIED_PHENOTYPE: more than one;
- NO_MATCH: none.

This distinguishes:

    state-transition phenotype

from:

    generator identity.

If two generators produce the same Psi(S1), the generator is not identifiable even from complete
before/after scholarly states.

## 8. Null audit

For each registered null:
- require Psi(S0) == Psi(S1);
- test whether full representation state changed in evidence/event/transition ledgers;
- compare Gamma(S0,e_future) with Gamma(S1,e_future) for a fixed future probe.

Possible outcomes:

### TRUE_ACTION_IDENTITY

Psi unchanged, full representation may record the event, and future candidate set is unchanged.

### STATE_NULL_ACTION_NON_NULL

Psi unchanged but the future candidate generator set changes.

### FUTURE_SENSITIVITY_NOT_REPRESENTED

Psi unchanged and ledgers/provenance change, but the current qualification rules do not consult
that accumulated evidence/history, so Gamma remains unchanged by construction.

The last result does NOT prove that corroborative evidence is irrelevant to future scholarship.
It identifies a limitation of the current one-step qualification model.

## 9. Composition probe

Construct a synthetic state with one accepted assertion A.

Event e1 supports competing assertion B.

Choose the already registered generator:

    ADD_ALTERNATIVE

to obtain:

    S1 = {A,B}

Then examine a second resolution evidence surface e2.

Primary composition checks:

### Enablement

    RESOLVE not in Gamma(S0,e2)

but:

    RESOLVE in Gamma(S1,e2)

### Partial non-commutativity

The sequence:

    ADD_ALTERNATIVE ; RESOLVE

is structurally defined.

The reverse sequence attempts RESOLVE at S0 and is structurally undefined.

This is sufficient to establish that operation availability can be state-dependent under the
existing semantics.

It does not establish a general algebraic theorem.

## 10. False-positive reinterpretation audit

Existing historical failure classes are not relabeled automatically.

The audit records a candidate reinterpretation only:

    representation false positive
    -> generator-availability false positive

Examples for later analysis:
- annex/object contamination;
- aggregate-object false positives;
- evidence applicability failure.

No existing scientific result is overwritten.

## 11. Primary questions

Q1.
Is the held-out Module-R operation uniquely recoverable from S and e?

Q2.
If not, does complete S0/S1 state information make it unique?

Q3.
Do registered nulls preserve only Psi, or also future action availability?

Q4.
Does one scholarly transition change the set of structurally available subsequent operations?

## 12. Decision rule

### NO_DEEPER_PROBLEM

Only if:
- all substantive operations are uniquely recovered from S,e;
- nulls preserve future action sets;
- no state-dependent enablement appears.

### EXOGENOUS_OPERATION_PROBLEM

If any substantive/natural episode has |Gamma(S,e)| > 1.

### GENERATOR_NONIDENTIFIABILITY

If any episode has |Gamma_match(S,e,S1)| > 1.

### COMPOSITION_REQUIRED

If a first transition changes structural availability of a later generator.

### NULL_MODEL_INCOMPLETE

If a Psi-null event changes future generator availability.

### FUTURE_QUALIFICATION_BLIND_SPOT

If Psi-null events change provenance/history but the current generator qualification is
insensitive to that accumulated evidence by construction.

Multiple findings may hold simultaneously.

## 13. Claim ceiling

This is a structural audit of the current dynamic model.

It does not yet establish:
- the correct minimal generator vocabulary;
- a universal scholarly action algebra;
- real multi-step historical composition prevalence;
- that every null should alter future action.

If the audit exposes underidentification/composition dependence, the next scientific task is to
replace exogenous operation labels with state/evidence-dependent qualification and then test
composition prospectively.
