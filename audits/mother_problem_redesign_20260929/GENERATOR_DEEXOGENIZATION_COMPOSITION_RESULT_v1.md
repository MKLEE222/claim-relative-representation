# Generator de-exogenization and composition audit result v1

Date: 2026-09-29
Status: COMPLETED STRUCTURAL AUDIT / SYNTHETIC + PRE-EXISTING EXPOSED ONLY.

## 1. Frozen protocol

Protocol:

    audits/mother_problem_redesign_20260929/
    GENERATOR_DEEXOGENIZATION_COMPOSITION_AUDIT_v1.md

The protocol was frozen before implementation/results.

No new fresh corpus was consumed.

## 2. Workflow

Workflow:

    generator-deexogenization-composition-audit-v1

Successful run:

    36562437618

Artifact:

    11030287909

Artifact ZIP SHA-256:

    cc8b84a373819eabb17cdff0fae5e34be0fccb73769f6e0b7985ff0268ae773c

The workflow first reran the existing Module-R synthetic contract, which passed unchanged.

## 3. Episodes audited

Total:

    10

Synthetic:
- attribution replacement;
- alternative formation;
- evidential-status revision;
- basis-only null;
- status-null reassessment.

Historical:
- YC1920E-0022;
- YC1920E-0023;
- YC1920E-0024;
- YC1920E-0030;
- YC1920E-0049.

The frozen operation label was removed from the evidence surface before generator recovery.

## 4. Pre-state generator recovery

Result:

    unique generator from S,e      0/10
    underidentified               10/10

Thus the current Module-R operation is never uniquely determined by the currently represented:
- scholarly pre-state;
- object/target;
- evidence identity/locator;
- source context;
- proposed value/status;
- applicability proof.

Examples:

### Replacement / alternative ambiguity

For a singleton accepted assertion A and later proposed B:

    Gamma(S,e) = {REPLACE, ADD_ALTERNATIVE}

The current representation does not itself determine whether B replaces A or becomes a competing
live alternative.

### Status-revision ambiguity

For the same literal value with changed status:

    Gamma(S,e) = {
        REPLACE,
        ADD_ALTERNATIVE,
        REVISE_STATUS
    }

The frozen REVISE_STATUS label therefore carries extra transition semantics not recoverable from
the current state/evidence fields alone.

### Resolution ambiguity

For the historical unresolved Great-Desert state:

    Gamma(S,e) = {REPLACE, RESOLVE}

The event/state fields alone do not identify whether the operation is generic replacement or a
resolution of an unresolved scholarly state.

## 5. Generator recovery from observed post-state

Using the complete frozen Psi(S1):

    unique generator phenotype        3/10
    underidentified phenotype         7/10

Using the complete oracle post-state:

    unique generator full state       3/10
    underidentified full state        7/10

Thus the problem is not only uncertainty before execution.

For 7/10 audited episodes, even complete before/after scholarly states fail to identify which
registered generator produced the transition.

Examples:

### REPLACE vs REVISE_STATUS

For same-value status changes:

    REPLACE
    REVISE_STATUS

produce the same scholarly post-state under the current representation.

This occurs in:
- synthetic evidential-status revision;
- synthetic nulls;
- Sykes position revision;
- Tutia null;
- Pashai null.

### REPLACE vs RESOLVE

For the historical unresolved Great-Desert case:

    REPLACE
    RESOLVE

produce the same full post-state.

Therefore the R-U generator identity is not generally a state-transition phenotype.
It is partly an externally supplied transition semantics.

## 6. Natural/synthetic null audit

Registered nulls audited:

    4

- synthetic basis-only null;
- synthetic status null;
- Tutia corroborative/additive null;
- Pashai corroborative null.

For all 4:

    Psi(S0) == Psi(S1)                         true
    full representation changed                true
    evidence/event/transition ledgers changed  true
    future Gamma under current rules changed   false

Classification:

    FUTURE_SENSITIVITY_NOT_REPRESENTED = 4/4

This does NOT establish that corroborative evidence is truly irrelevant to future scholarly
action.

It establishes a limitation of the current one-step model:

> accumulated evidence/provenance/history can change while the present generator qualification
> rules remain blind to those changes.

Thus the current ADMISSIBLE_NULL_EVENT notion is only a Psi-state null.

It is not yet proven to be an identity element for future researchability.

## 7. Composition probe

Synthetic sequence:

    S0 = accepted A

First generator:

    ADD_ALTERNATIVE(B)

produces:

    S1 = {A,B}

Before the first transition:

    Gamma(S0,e_resolution)
    = {REPLACE, ADD_ALTERNATIVE}

After alternative formation:

    Gamma(S1,e_resolution)
    = {
        REPLACE,
        ADD_ALTERNATIVE,
        REVISE_STATUS,
        RESOLVE
    }

Therefore:

    RESOLVE not available at S0
    RESOLVE available at S1

State-dependent enablement:

    PASS

Forward sequence:

    ADD_ALTERNATIVE ; RESOLVE

is structurally defined.

The reverse attempt begins with RESOLVE at S0, where RESOLVE is structurally unavailable.

Partial non-commutativity:

    PASS

This establishes, at the current synthetic semantics, that one scholarly transition can change
the set of subsequent structurally available generators.

It does not yet establish a general composition algebra.

## 8. Audit findings

Observed:

    EXOGENOUS_OPERATION_PROBLEM       true
    GENERATOR_NONIDENTIFIABILITY      true
    COMPOSITION_REQUIRED              true
    NULL_MODEL_INCOMPLETE             false
    FUTURE_QUALIFICATION_BLIND_SPOT   true
    NO_DEEPER_PROBLEM                 false

NULL_MODEL_INCOMPLETE is false only in the narrow sense that no current audit probe found
Gamma(S0) != Gamma(S1) for a Psi-null event.

Because the current qualification rules do not use accumulated evidence/history, that negative
result cannot establish true future-action identity.

## 9. Scientific interpretation

The existing Module-R result should not be discarded.

It remains valid as evidence that:
- object/target/source/applicability/provenance/history distinctions matter;
- registered transitions can be executed and audited;
- strong state/snapshot/change-log comparators remain insufficient for evidence-grounded history.

What changes is the theoretical level of interpretation.

The current operation vocabulary is not yet identified as a set of endogenous scholarly
generators.

More precisely:

    transition class
    !=
    state/evidence-derived generator identity

and:

    complete before/after state
    !=
    generator identity

for most audited cases.

The next theoretical object should therefore include a qualification relation:

    Q(S,e,g)

or equivalently:

    Gamma(S,e) = {g : Q(S,e,g)}

rather than accepting g as an event input.

## 10. Relation to prior false positives

The audit licenses a new hypothesis, not a retrospective relabeling:

    representation false positive
    may be understood as
    false generator availability.

Examples worth later formalization include:
- annex/object contamination;
- aggregate-object false positives;
- missing applicability/binding.

The unifying question becomes:

> Does the representation preserve which scholarly actions are actually available from the
> current state, rather than merely preserving state values?

## 11. Next authorized scientific step

Do not immediately collect another corpus.

Next:

1. audit Module P separately to distinguish:
   - exogenous evidence-release activation;
   - endogenous warrant-update phenotype;
   - missing multi-event composition;

2. define the minimum additional evidence relation needed to reduce Gamma(S,e):
   - contradiction;
   - corroboration;
   - replacement/supersession;
   - qualification;
   - resolution;
   - source-status revision;

3. test whether those relations are themselves recoverable from source/provenance or merely new
   exogenous labels;

4. construct two-step composition tests under state-dependent qualification;

5. revisit nulls as potential:
   - Psi-null;
   - provenance-non-null;
   - future-action-null or future-action-non-null.

No fresh data is required for these steps.


## 12. Module-P cross-audit

A separate synthetic cross-audit was added after the Module-R generator result.

Workflow:

    generator-deexogenization-composition-audit-v1

Successful cross-audit run:

    36562856755

Artifact:

    11030642414

Artifact ZIP SHA-256:

    342ebad7d9a59ee77195f1f0a98eba6c929b037a708ba76b176f91a2d4c962c3

### P differs structurally from R

Module P does NOT place:

    REPLACE / ADD_ALTERNATIVE / REVISE_STATUS / RESOLVE

inside the event request.

For all three synthetic audit cases:
- conflict formation;
- unresolved -> exact acquisition;
- basis-only null;

the event surface is only:

    EVIDENCE_RELEASE_REVISION
    / EVIDENCE_RELEASE

with no operation field.

The transition class is a pure function of:

    Phi(S0), Phi(S1)

under the frozen classifier.

Thus P-U1/P-U2/P-U3/P-U4 are transition phenotypes rather than externally supplied operation
labels.

### What remains exogenous in P

The release event itself remains externally declared.

The wrapper:
- constructs one OPEN_ORIGIN event;
- opens the already frozen origin handle;
- executes one neutral event;
- returns.

Its public signature is:

    execute(doc, fault=None, drop_history=False)

There is no prior-state or event-sequence input.

Therefore P currently has:

    fixed first-order evidence-admission generator
    + endogenous warrant phenotype

but not:

    endogenous event activation
    or
    multi-generator composition.

### Post-state dependence

P declares substantive ERIR eligibility only after:

    Phi(W_root) != Phi(W_post)

is observed.

Therefore P can identify whether a fixed evidence-admission action changed the scholarly state,
but it does not define a pre-execution qualification rule that distinguishes in advance:

    state-changing action
    from
    admissible state-null action.

### P null

The basis-only synthetic event has:

    Phi(S0) == Phi(S1)

while:
- event applies;
- evidence ledger changes;
- event ledger changes;
- transition ledger changes.

Thus P independently confirms:

    scholarly-state null
    !=
    action/history null.

This matches the deeper concern exposed by the R null audit.

## 13. Integrated diagnosis across P and R

The two modules fail at different layers.

### Module R

Current form:

    state + evidence + externally supplied operation
    -> next state

Problem:

    generator identity is not generally recoverable from state/evidence,
    and often not even from complete before/after state.

### Module P

Current form:

    state + externally released evidence
    -> fixed evidence-admission action
    -> endogenous warrant phenotype

Problem:

    activation is externally supplied;
    state-changing vs null status is known post hoc;
    sequential composition is absent.

Therefore the deeper project-level problem is not simply:

    remove operation labels from R.

It is:

> Define a state- and evidence-dependent qualification relation for scholarly actions, and study
> how executing one qualified action changes the set of actions available next.

A natural formal object is:

    Q(S,e,g)

with:

    Gamma(S,e) = { g : Q(S,e,g) }

and a composition layer where:

    g1 in Gamma(S0,e1)

changes both:

    S1 = g1(S0)

and potentially:

    Gamma(S1, .)

The current evidence now supports treating this as the next mother-problem layer rather than as
an implementation detail.
