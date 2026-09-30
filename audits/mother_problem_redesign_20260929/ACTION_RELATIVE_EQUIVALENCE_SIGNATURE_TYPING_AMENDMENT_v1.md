# Action-relative equivalence signature typing amendment v1

Date frozen: 2026-09-30
Status: PRE-IMPLEMENTATION FORMAL TYPING CLARIFICATION.

## 1. Trigger

Before implementing the frozen action-relative state-equivalence audit, the registered empirical
signature dimensions were inspected by type.

The label:

    TARGET_IDENTITY

is not solely a coordinate of scholarly state S.

The exact target is supplied by the source-grounded event/relation binding e, while the state
determines whether that bound target is live/current and whether its required history is retained.

Therefore TARGET_IDENTITY and TARGET_LIVE_OR_CURRENT must not be treated as interchangeable
state coordinates.

## 2. Typed signature

For each generator g define:

    Sigma(g) = (Beta(g), Kappa(g))

where:

### Beta(g) — event/relation binding signature

Predicates inspected on the source-grounded event/relation:

- exact object/root binding;
- exact target identity;
- source/version binding;
- relation kind;
- evidence/event identity when registered.

### Kappa(g) — state qualification signature

Predicates inspected on the current state/history:

- target live/current status;
- version/retraction validity;
- retained target-entry transition history;
- current proposition/status state when registered.

## 3. Corrected action-relative state equivalence

State equivalence is defined only on Kappa(g):

    S ~_g S'
    iff
    P_{Kappa(g)}(S) = P_{Kappa(g)}(S')

for the fixed admissible event/relation binding e.

Qualification invariance becomes:

    if S ~_g S'
    then Q_g(S,e) = Q_g(S',e)

within the registered model.

## 4. Binding counterexamples

Dimensions in Beta(g) are not tested by pretending they are state ablations.

They require event-side perturbation:

    e -> e'

while holding S fixed.

A Beta dimension is REQUIRED only if a registered perturbation of that binding changes
qualification as expected.

Examples:
- wrong formalization/review/update target;
- wrong scholarly claim target;
- wrong root/object binding.

## 5. State counterexamples

Dimensions in Kappa(g) are tested with e fixed and state pairs changed only in the registered
state condition.

Examples:
- exact target remains named by e but is no longer current/live;
- update is explicitly retracted;
- current target projection is held fixed while required transition history is erased.

## 6. Sequence closure typing

For a sequence:

    g_t -> g_(t+1)

closure distinguishes:

### Binding production

g_t may create an entity that later appears as target(e_(t+1)).

### State qualification production

g_t may make that target live/current or create the retained transition history inspected by
Kappa(g_(t+1)).

Thus sequence closure is:

    writes(g_t)
    covers
    bindings/conditions read by (Beta(g_(t+1)), Kappa(g_(t+1)))

not merely field overlap in one untyped state vector.

## 7. Scientific invariants

This amendment changes no:
- empirical signature label;
- generator;
- source relation;
- denominator;
- natural action result;
- Formalization Papers chain result;
- Yule-Cordier result.

It only types previously observed requirements so the equivalence theorem is well-formed.

## 8. Pass rule effect

The frozen closure protocol remains in force with this interpretation:

- REQUIRED TARGET_IDENTITY -> event-side binding witness;
- REQUIRED LIVE/CURRENT, VALIDITY, HISTORY -> state-side witness;
- NOT_REQUIRED HISTORY -> state-side invariance witness.

A dimension may not be counted twice using one confounded perturbation when a cleaner typed
witness is available.
