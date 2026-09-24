# Preflight Experiment - Interaction Representation Construction Audit

Date frozen: 2026-09-24
Status: PRE-OUTCOME CONSTRUCTION AUDIT

## Purpose

Construct and validate the four representation states required by each preregistered first-wave interaction before any human task outcome is collected.

For each interaction (T1,T2):

- R00 = baseline
- R10 = T1(R00)
- R01 = T2(R00)
- R11 = T2(T1(R00))

## This is not an outcome experiment

The audit tests only:

1. constructor determinism;
2. layer-specific invariants;
3. transformation composition;
4. commutation where preregistered;
5. preservation of substantive text identity;
6. exact changed-field accounting.

No claim state, task answer, recoverability class, or recovery depth is opened here.

## Representation wrapper

Each event representation contains:

- the frozen canonical event record;
- an access-scope state.

The access scope is one of:

- object
- local
- span

TA_SPAN changes only the access-scope state. It does not rewrite the focal span.

## Constructor rules

### TD_TEMPORAL
Sets the structured temporal-order field unavailable.
Must not change text, attribution, evidence relation, claim binding, or access scope.

### TR_BINDING
Sets explicit claim binding unavailable.
Must not change endpoint text, attribution, temporal order, evidence relation, or access scope.

### TR_EVIDENCE
Sets the typed evidence-relation field unavailable.
Must not change endpoint text, attribution, temporal order, claim binding, or access scope.

### TA_SPAN
Changes context scope from object/local to span.
Must not change any documentary or relational field.

## Composition

The first-wave interactions are declared commuting because T1 and TA_SPAN act on disjoint layers.

For every registered first-wave block:

T1(TA_SPAN(R)) must equal TA_SPAN(T1(R)).

A failure invalidates the interaction constructor before any empirical task is run.

## Audit disposition

- PASS_CONSTRUCTION: all invariants and composition checks pass.
- FAIL_CONSTRUCTION: any undeclared field changes.
- BLOCKED: a registered interaction lacks a constructor.

A PASS does not imply the interaction will affect recoverability or task executability.
