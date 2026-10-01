# Module Q — post-hoc Q4 intervention-support diagnostic v1

Date: 2026-09-29
Status: POST-HOC DIAGNOSTIC ONLY. DOES NOT CHANGE THE FRESH DISPOSITION.

## 1. Authoritative source

Fresh run:

    36526317608

Artifact:

    module-q-aad-fresh-v1
    artifact id = 11014393375

Fresh final disposition remains:

    BOUNDED_PARTIAL

This diagnostic uses only the frozen result artifact.
No AAD rerun is performed.

## 2. Question

Why did the predeclared Q4 collateral-mutation intervention produce:

    collateral detected = 39/69
    selectivity pass     = 30/69

despite the valid reference execution passing P4 selectivity for all 69 natural episodes?

## 3. Exact transition-class cross-tab

### P-U1 CONFLICT_FORMATION

N = 16

Frozen Phi(before):

    EXACT = 16/16

Q4:

    event applicable       16/16
    collateral path exists 16/16
    selectivity fails       16/16
    transition attribution 16/16

### P-U2 RESOLUTION_OR_ACQUISITION

N = 30

Frozen Phi(before):

    UNRESOLVED = 30/30

Q4:

    event applicable       30/30
    collateral path exists  0/30
    selectivity remains pass 30/30
    transition attribution 30/30

### P-U3 NARROWING_OR_QUALIFICATION

N = 23

Frozen Phi(before):

    OPEN_INTERVAL = 20
    EXACT         = 2
    INTERVAL      = 1

Q4:

    event applicable       23/23
    collateral path exists 23/23
    selectivity fails       23/23
    transition attribution 23/23

Therefore:

    16 + 23 = 39

exactly equals the number of successful collateral-fault instantiations.

No non-U2 episode retained selectivity under Q4.

No U2 episode produced a collateral path under Q4.

## 4. Mechanism

The frozen collateral fault mutates an unrelated pre-existing root temporal state.

For P-U1 and P-U3, a task-relevant root state already exists and the fault has a target.

For P-U2:

    Phi(before) = UNRESOLVED

because no machine root temporal carrier supplies such a target.

Therefore the fault request is admitted as an event-level test but has no pre-existing collateral
root claim to mutate.

The observed result is:

    no injected collateral mutation
    -> no collateral path
    -> selectivity correctly remains PASS

rather than:

    collateral mutation occurred but the evaluator failed to detect it.

## 5. Scientific meaning

The fresh result demonstrates two different statements.

### Natural valid execution

For all 69 eligible episodes:

    P4 SELECTIVE_UPDATE = PASS

There is no observed natural collateral mutation.

### Stress-test support

The specific frozen Q4 fault operator is supported on:

    39/69 episodes

and unsupported on:

    30/69 P-U2 episodes

Thus the Q4 failure is an intervention-support problem.

It is not evidence that:
- P-U2 updates are non-selective;
- the source audit failed;
- the reference state is wrong;
- the object/evidence binding is wrong.

## 6. Why the authoritative result stays BOUNDED_PARTIAL

The fresh protocol required the Q4 intervention across all eligible episodes.

That rule was fixed before AAD opening.

After seeing the result, it would be outcome-driven to redefine Q4 as class-conditional and then
relabel the same fresh run PASS.

Therefore:

    authoritative fresh disposition = BOUNDED_PARTIAL

remains unchanged.

## 7. Future design implication

For any future independent temporal confirmation, failure injection should be frozen with an
explicit support predicate.

Example:

    Q4a ROOT_COLLATERAL_MUTATION
        applicable only when a non-target root claim exists

and, for unresolved-to-warranted episodes:

    Q4b FOREIGN_TARGET_CREATION
        inject an unauthorized unrelated claim into an otherwise unresolved pre-state

The second intervention would test selectivity for P-U2 without presupposing an existing root
claim.

This design change is prospective only.
It may not be retroactively applied to AAD.

## 8. Relation to near-neighbor design

The result reinforces the broader distinction developed from provenance/versioning neighbors:

    event applicability
    !=
    intervention support
    !=
    natural selectivity
    !=
    delayed transition audit

Stress tests themselves require a declared domain of applicability.

## 9. Claim ceiling

This diagnostic may explain the bounded-partial result.

It may not upgrade it.
