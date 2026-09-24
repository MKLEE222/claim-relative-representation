# Interaction Contract v1

Date frozen: 2026-09-24
Status: PRE-EXPERIMENT FREEZE

## Why interactions are scientifically necessary

Experiment 1A showed carrier substitution: removing one explicit carrier may leave another carrier that preserves task executability.

Therefore a null main effect can be genuine evidence of redundancy rather than evidence that the removed coordinate is irrelevant.

The project permits interaction tests only when a carrier mechanism is frozen before task outcomes are observed.

## Main effects

A main-effect cell applies one typed transformation T_j under a fixed task and recovery contract.

Main effects answer:

> What happens when one declared carrier or access condition changes while the remaining representation contract is held fixed?

Main-effect nulls are retained.

## Interaction definition

For two transformations T_i,T_j, the 2x2 block is:

- R00: baseline
- R10: T_i(R)
- R01: T_j(R)
- R11: T_j(T_i(R))

Composition order must either commute by construction or be frozen explicitly.

The interaction is evaluated on the task-adapted state, not initially on retain/revise/defer/withhold.

## Admissible interaction classes

### I1 - carrier-substitution / carrier-exhaustion interaction

Highest-priority class.

Admissible when:

1. both transformations bear on the same candidate distinction q;
2. T_i removes or hides carrier b1;
3. the preregistered recovery hypothesis predicts substitution to carrier b2;
4. T_j removes or makes b2 inaccessible;
5. the joint condition may therefore exhaust the basis family or increase uncertainty.

Canonical pattern:

b1 --T_i--> b2, then T_j removes or blocks b2.

This class can produce a strong interaction even when both individual main effects preserve task output.

### I2 - dependency-conjunction interaction

Secondary class.

Admissible when the frozen task hypothesis predicts that two distinct candidate distinctions must both be available for the task, and separate transformations target them.

This class is held out of the first interaction wave unless the individual distinctions have already shown stable recoverability coding.

### I3 - generic all-pairs interaction

PROHIBITED.

The project does not run every pair of transformations and search post hoc for non-additivity.

## Layer rule

Primary interactions should normally cross transformation layers:

- TD x TA
- TR x TA
- TD x TR

because these have interpretable mechanisms such as "explicit carrier removed + reconstruction context restricted."

Within-layer interactions require a separate written mechanism and are held out by default.

## First-wave interaction family

The first interaction wave is restricted to I1 carrier-substitution/exhaustion blocks.

Priority examples:

1. TD_TEMPORAL x TA_SPAN or TA_LOCAL for cross-layer tasks.
   - mechanism: structured chronology removed; restricted context may remove the alternative cross-layer recovery route.

2. TR_BINDING x TA_SPAN for relation/binding tasks.
   - mechanism: explicit referent pointer removed; restricted context may remove the contextual basis for rebinding.

3. TR_EVIDENCE x TA_SPAN for cross-layer relation tasks.
   - mechanism: typed relation edge removed; restricted context tests whether lexical/local cues are enough to reconstruct the relation.

TD_ATTRIBUTION interactions enter only where the frozen carrier map predicts that attribution is not already intrinsic to the focal span.

## Interaction outcome

No single scalar interaction coefficient is required in v1.

Report the 2x2 task-adapted states:

sigma_00, sigma_10, sigma_01, sigma_11

and classify the mechanism:

- NO_INTERACTION
- BURDEN_SYNERGY
- UNCERTAINTY_SYNERGY
- BASIS_EXHAUSTION
- TASK_EXECUTABILITY_LOSS

A numeric contrast may be added only for predeclared scalar components such as time or number of traversals.

## Strong interaction witness

The strongest mechanistic witness is:

1. R10 remains task-output equivalent to baseline;
2. R01 remains task-output equivalent to baseline;
3. R11 does not;
4. carrier coding shows that T_i forced recovery onto a carrier removed by T_j;
5. restoration of either carrier reverses the failure.

This is a representation-level interaction, not merely a statistical association.

## Multiple testing / scope discipline

- no exploratory all-pairs matrix in the confirmatory block;
- every interaction has a preregistered target distinction and carrier mechanism;
- failed and null interactions remain in the ledger;
- new interactions suggested by results go to a later exploratory phase;
- claim-state outcomes remain sealed during the first interaction wave.
