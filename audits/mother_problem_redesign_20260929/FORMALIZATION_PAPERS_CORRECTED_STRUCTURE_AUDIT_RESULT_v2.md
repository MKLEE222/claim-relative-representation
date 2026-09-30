# Formalization Papers corrected structure audit result v2

Date: 2026-09-30
Status: POST-FRESH EXPOSED STRUCTURE AUDIT / CORRECTED RESULT UNCHANGED.

Workflow:

    formalization-papers-corrected-structure-audit-v2

Run:

    36659541817

Artifact:

    11074305301

Artifact ZIP SHA-256:

    6900ef817d97c722d0a07d5bcd427f147d173aefafb65cd12f5f479567e51641

## 1. Population

Graph-derived roots:

    15

Disposition:

    T0_COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION = 8
    T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET         = 7

Eligible connected chains:

    52

All 52 belong to the eight T0 roots.

Per-root chain counts:

    2, 4, 6, 6, 7, 8, 8, 11

No favorable chain was selected; all connected chains in the frozen T0 denominator are retained.

## 2. Generator sequence

All 52 chains execute the same project-native action structure:

    RECORD_REVIEW
    -> REPLACE_FORMALIZATION
    -> RECORD_RESPONSE
    -> REVISE_PUBLICATION_STATUS

Count:

    52/52

This is not supplied as a provider operation label.
The generators are selected by the frozen target/state qualification rules.

## 3. Counterfactual decomposition

Every registered control is actually executable for every eligible chain.

### P2 response before review

    PASS_REJECT = 52/52

### P3 response before update

    PASS_REJECT = 52/52

### P4 same-current-state history ablation

    PASS_REJECT = 52/52

Current formalization/update projection held equal:

    52/52

Rejection reason after history removal:

    RESPONSE_TARGET_HISTORY_UNRESOLVED = 52/52

Thus the central result is not an aggregate artifact:

    Psi(current full history)
    =
    Psi(current history-ablated)

while:

    Gamma_response(full history)
    !=
    Gamma_response(history-ablated)

for every eligible connected chain.

### P5 decision before update

    PASS_REJECT = 52/52

### P6 wrong review target

    PASS_REJECT = 52/52

Structurally unavailable:

    0

### P6 wrong update target

    PASS_REJECT = 52/52

Structurally unavailable:

    0

### P7 live-version discipline

    PASS = 52/52

Thus no primary control success rate is inflated by unavailable counterfactuals.

## 4. Natural negative/ambiguous side

The seven T8 roots are retained in the closed root population.

Observed ambiguity instances:

    RESPONSE_UPDATE_TARGET_NOT_LIVE = 47
    RESPONSE_NONFUNCTIONAL_TARGET   = 1

These are ambiguity instances, not root counts; one root can contain multiple affected response
relations.

The dominant T8 mechanism is therefore not generic parsing failure.

It is exactly a relation-target/version condition:

> a response edge can exist in the data while the update nanopublication it refers to is not the
> unique live update act under the frozen supersession/retraction discipline.

This is a natural negative side of the mother problem:

    relation presence
    !=
    lawful current action availability

and supports retaining target/version status as part of qualification rather than treating every
edge as executable.

## 5. Scientific interpretation

The Formalization Papers corrected result supplies both sides needed by the qualified-composition
claim.

Positive side:

    52/52 connected T0 chains

show that retained target/history supports the registered future actions.

Negative/ambiguous side:

    7/15 roots -> T8

shows that relation edges alone are insufficient when exact target/live-version requirements do
not close.

The cross-ecology distinction is therefore:

    edge/material presence
    !=
    target live-ness
    !=
    history-qualified action availability
    !=
    lawful composition

This is structurally homologous to earlier object/applicability false-positive findings but occurs
at a later, composition-level boundary.

## 6. Evidentiary ceiling

This audit is post-fresh/exposed and does not alter:

    authoritative fresh = INVALID

or:

    corrected reproduction = PASS

It adds decomposition and interpretation only.
