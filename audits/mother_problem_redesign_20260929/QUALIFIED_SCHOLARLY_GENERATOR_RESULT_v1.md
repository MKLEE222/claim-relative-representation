# Qualified scholarly generator repair result v1

Date: 2026-09-29
Status: QUALIFIED_GENERATOR_REPAIR_PASS.

## 1. Problem

The prior Module-R representation supplied the operation label externally:

    REPLACE
    ADD_ALTERNATIVE
    REVISE_STATUS
    RESOLVE

A frozen structural audit then showed:

    generator recovery from S,e:
        unique          0/10
        underidentified 10/10

and even with the complete observed post-state:

    unique          3/10
    underidentified 7/10

Therefore the previous operation vocabulary could not be interpreted as endogenous first-order
scholarly generators.

## 2. Repair principle

The repair removes operation from the input.

It uses:
- current scholarly state S;
- source-grounded earlier/later evidence relation rho;
- evidence/proposal e;
- inherited object/target/source/applicability bindings.

The qualification object is:

    Q(S,rho,e,g)

and:

    Gamma(S,rho,e) = { g : Q(S,rho,e,g) }

The evidence-relation vocabulary was not invented after the generator failure.

It comes from the already frozen R3 contrast protocol:

    CONTRADICTS_PRIOR
    REPLACES_PRIOR
    NARROWS_PRIOR
    ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT
    CORROBORATES_PRIOR
    NO_VERIFIED_CONTRAST

R3_UPDATE_CONTRAST_AMENDMENT_v4 explicitly requires these labels to be grounded in earlier-vs-
later source comparison.

## 3. First-class generators

The repaired vocabulary is:

    RECORD_EVIDENCE
    REPLACE
    ADD_ALTERNATIVE
    REVISE_STATUS
    RESOLVE

RECORD_EVIDENCE is first-class.

It is:

    identity under Psi(current assertions)

but:

    non-identity under Xi(evidence/history)

so unchanged current assertions no longer imply that no scholarly action occurred.

## 4. Independent implementations

Two independently coded engines were used:

    qualified_oracle_v1
    qualified_runtime_v1

They do not call each other's qualification implementation.

They agree exactly on all registered scientific surfaces.

## 5. Frozen workflow

Workflow:

    qualified-scholarly-generator-repair-v1

Final successful run:

    36564265592

Head:

    a821e78e243b361b8243b50c10b215c36923c5c4

Artifact:

    11031286196

Artifact ZIP SHA-256:

    093d6b574b84f1c754ecc77a18b71865e4926a8c895f809a22c570ce55331079

The workflow first verifies frozen Git blobs for:
- the R3 contrast amendment;
- the R3 relation ontology;
- the historical source-audit CSV;
- the qualified-generator contract;
- both qualified engines;
- the closure runner.

It then:
1. reruns the existing Module-R synthetic contract;
2. reproduces the old exogenous-operation problem;
3. runs the repair gate.

## 6. Recovery result

### Historical

Source-grounded historical recovery:

    5/5

No historical operation label is supplied to the qualified engines.

Results:

    YC1920E-0022
    CONTRADICTS_PRIOR
    -> REVISE_STATUS

    YC1920E-0023
    ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT
    -> RECORD_EVIDENCE

    YC1920E-0024
    CONTRADICTS_PRIOR
    -> ADD_ALTERNATIVE

    YC1920E-0030
    CORROBORATES_PRIOR
    -> RECORD_EVIDENCE

    YC1920E-0049
    ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT
    + unresolved prior state
    -> RESOLVE

The two historical null cases are intentionally repaired away from the old generic REPLACE label.

They are now:

    assertion identity
    + history nonidentity

rather than pseudo-mutations whose only purpose is to record evidence.

### Synthetic

Synthetic recovery:

    5/5

    REPLACES_PRIOR
    -> REPLACE

    CONTRADICTS_PRIOR
    -> ADD_ALTERNATIVE

    NARROWS_PRIOR
    -> REVISE_STATUS

    CORROBORATES_PRIOR
    -> RECORD_EVIDENCE

    CORROBORATES_PRIOR
    -> RECORD_EVIDENCE

## 7. Preservation of prior empirical state results

For all 10 audited cases:

    operation absent from qualified input = 10/10

and:

    repaired Psi(S1) == old frozen Psi(S1) = 10/10

Thus the repair changes how the scholarly action is identified, not the previously established
current-state outcomes.

## 8. Oracle/runtime agreement

Exact agreement:

    10/10

on:
- binding disposition;
- source-grounded relation;
- selected generator;
- before/after Psi;
- before/after Xi;
- assertion-identity flag;
- history-nonidentity flag;
- final state;
- retained evidence/history.

## 9. False-positive generator availability controls

All controls reject before scholarly-state mutation:

    wrong object             PASS
    wrong target             PASS
    wrong source version     PASS
    missing applicability    PASS
    unregistered relation    PASS
    no verified contrast     PASS

Total:

    6/6

For every rejection:

    Psi unchanged
    Xi unchanged
    generator = none

This supplies an explicit action-availability interpretation for the earlier object/binding
discipline:

    invalid binding
    -> no qualified generator

rather than:

    invalid binding
    -> mutate and repair afterward.

## 10. Generator factorization

The repair explicitly tests whether the selected generator is merely a renamed evidence relation.

It is not.

### Relation sensitivity

Hold fixed:
- scholarly state;
- object;
- target;
- evidence identity;
- proposed value/status.

Change only source-grounded relation:

    CONTRADICTS_PRIOR -> ADD_ALTERNATIVE
    REPLACES_PRIOR    -> REPLACE

Therefore:

    generator != relation label.

### State sensitivity

Hold fixed:

    relation = REPLACES_PRIOR

At a singleton state:

    generator = REPLACE

After a competing alternative exists:

    generator = RESOLVE

Therefore:

    generator != relation-only lookup.

The observed form is genuinely joint:

    g = Q(S,rho,e)

## 11. Composition

Registered two-step probe:

Initial:

    S0 = accepted A

Evidence e1:

    CONTRADICTS_PRIOR
    proposes competing B

Forward qualification:

    S0
    --ADD_ALTERNATIVE-->
    S1 = {A,B}

Then evidence e2:

    REPLACES_PRIOR
    proposes accepted B

At S1:

    e2 -> RESOLVE

Forward generator sequence:

    ADD_ALTERNATIVE ; RESOLVE

Reverse order:

At S0:

    e2 -> REPLACE

Then the contradiction evidence sees B already live with a different proposed status:

    e1 -> REVISE_STATUS

Reverse generator sequence:

    REPLACE ; REVISE_STATUS

Therefore:

    generator sequences differ         true
    final Psi states differ             true
    final full scholarly states differ  true
    composition non-commutative         true

This is not merely an ordering effect on event labels.

The first action changes the qualification of the second action.

## 12. Null repair

Four audited former nulls become:

    RECORD_EVIDENCE

For all 4:

    Psi(S0) = Psi(S1)

and:

    Xi(S0) != Xi(S1)

Therefore the appropriate distinction is:

    assertion-state identity
    !=
    full scholarly-state identity

The older term ADMISSIBLE_NULL_EVENT remains valid for the old assertion-state task but is not
used as a claim that the action is an identity element for future scholarly structure.

## 13. What is now resolved

Within the audited relation vocabulary and state forms:

### Exogenous operation problem

Resolved.

The operation field is not an input.

### Generator nonidentifiability caused by redundant mutation semantics

Resolved for the registered cases.

The qualification layer selects one generator before execution.

### Null/action conflation

Resolved.

Evidence registration is a first-order generator even when the assertion projection is unchanged.

### State-dependent composition

Established in the registered two-step probe.

The same evidence relation selects different generators under different states.

### Generator-as-renamed-relation concern

Rejected by the factorization probe.

Both state and source-grounded relation are necessary.

## 14. What is not yet claimed

The repair does not establish:
- universal completeness of the five-generator vocabulary;
- automatic extraction of contrast relations from arbitrary natural language;
- real-world prevalence of non-commutative multi-step trajectories;
- a universal category/algebra of scholarly revision;
- that every corroborative evidence event changes the immediately available generator set.

These are validation/generalization questions, not the original exogenous-operation defect.

## 15. Revised theoretical object

The dynamic mother problem can now be written more strongly as:

> What representational distinctions must be preserved so that, from a scholarly state S and
> source-grounded evidence relation rho, the legitimate scholarly action g is qualified, its
> justification remains auditable, and executing g produces the correct next-state action
> structure?

The minimal formal layer is:

    Gamma(S,rho,e) = {g : Q(S,rho,e,g)}

with transitions:

    S_(t+1) = g_t(S_t)

and composition governed by the state-dependent qualification of later generators.

This makes the previously identified representation obligations conditions on lawful scholarly
action availability, not merely a metadata checklist.
