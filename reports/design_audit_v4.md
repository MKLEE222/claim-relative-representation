# Design audit v4 - task adaptation, carrier substitution, and typed T

Date: 2026-09-24

## Main corrections before experiment

The design audit identified four places where the previous protocol was still too coarse.

### 1. Candidate distinctions are not assumed necessities

Task Contract v1 called coordinates "required distinctions". This would make a later finding that a task survives their removal look contradictory or force the study toward its own dependency assumptions.

v2 freezes a candidate distinction universe and stores expected dependencies separately as falsifiable hypotheses.

### 2. Recovery depth needs a carrier basis

Experiment 1A showed that removing structured attribution often leaves lexical attribution. Therefore the same distinction can migrate between carriers.

The recoverability profile is expanded from:

`(class, depth, assumptions, uncertainty, cost)`

to:

`(class, depth, basis, assumptions, uncertainty, cost)`.

This distinguishes carrier loss from carrier substitution.

### 3. T needs class-specific invariants

A single "one-coordinate invariance" rule is insufficient.

- TD operators act on documentary metadata/text.
- TR operators act on the constructed relation interface.
- TA operators act on context availability.

Each now has its own invariant contract.

TD_NORMALIZE is removed from the first main-effect block because lexical identity is not invariant by definition. It requires a separate semantic-preservation audit before use.

### 4. Task output equivalence and burden equivalence are different

A transformation may increase recovery depth/cost while preserving the task output.

The study therefore separates:

- output equivalence;
- profile equivalence;
- task executability;
- later humanistic claim-state equivalence.

## Revised target

The immediate scientific target is now:

> For a frozen scholarly task and recovery contract, which representational distinctions remain executable through which carriers after a typed transformation, and at what recovery burden?

Only after that object is stable will the project ask whether task-output changes propagate to retain/revise/defer/withhold claim states.

## Experiment hold

No replacement for Exp1B is launched in this commit. The next experiment requires a final audit of:

1. task realism;
2. transformation-task applicability blocks;
3. basis-aware recovery coding;
4. class-specific invariants.
