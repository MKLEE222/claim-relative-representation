# Task Contract v1

Date frozen: 2026-09-24

## Purpose

A representation is not evaluated in the abstract. It is evaluated relative to a **frozen scholarly task**.

The project therefore separates:

[
T_j:Sightarrow R_j
]

from:

[
A_	au:R_jightarrow X_{	au,j}
]

where (T_j) is a task-independent representation transformation and (A_	au) exposes the parts of that representation that a declared scholarly task is allowed to use.

This prevents answer-shaped ablations: the transformation is not redesigned for the task after outcomes are known.

## Task contract

A task contract is:

[
	au=(Q,I,D,O,H,S)
]

where:

- **Q — question**: the scholarly operation to be performed, stated without encoding the expected answer;
- **I — input scope**: the frozen source objects or representation objects presented to the task;
- **D — required distinctions**: the representational distinctions that may be needed for the task;
- **O — admissible outputs**: the allowed answer space, including unresolved;
- **H — background-knowledge state**: what non-representational knowledge the evaluator may use;
- **S — success rule**: what counts as successful execution, defined before intervention outcomes.

## Background-knowledge states

### H0 — representation-internal only
Only information present in the supplied representation and its explicitly exposed metadata may be used.

### H1 — general bibliographic/domain conventions
General scholarly conventions may be used, but not case-specific Yule-Cordier scholarship or the frozen author ledger.

### H2 — case-specific scholarly knowledge
Case-specific external scholarship may be consulted. H2 is not the primary experimental condition; it is reserved for sensitivity analysis.

The main recovery experiment uses **H0** unless a protocol explicitly states otherwise.

## Core task family

### tau_locate
Locate the source span(s) relevant to a frozen referent or question.

Permitted outputs:
- located
- multiple candidates
- not found

### tau_attribute
Identify the speaking/authorial/source role for a supplied span.

Permitted outputs:
- narrator/travel account
- editor
- cited scholar
- textual witness
- digital assembler
- unresolved

### tau_sequence
Establish the relative documentary/version order among supplied spans.

Permitted outputs:
- earlier/later relation
- same layer
- unresolved

### tau_bind
Determine whether supplied spans bear on the same frozen referent/claim object.

Permitted outputs:
- direct
- indirect
- unrelated
- unresolved

### tau_relation
Classify the source-grounded relation between supplied spans or between a span and a frozen claim object.

Permitted primitive outputs:
- ASSERTS_CONTENT
- ATTRIBUTES_SOURCE
- SUPPORTS
- CHALLENGES
- QUALIFIES_AUTHORITY
- DISTINGUISHES_WITNESSES
- UPDATES_IDENTIFICATION
- ACCRETES_INTERPRETATION
- LINKS_PRIOR
- DIGITAL_ASSEMBLES
- unresolved

Derived labels such as rehabilitation are **not** admissible task outputs at this stage.

### tau_adjudicate
Assign a humanistic claim state only after the upstream task contract has been satisfied.

Permitted outputs:
- retain
- revise
- defer
- withhold

This task remains sealed until the pre-outcome gates are passed.

## Task-adapted state

For a representation (R), task (	au), and recovery contract (K), define:

[
sigma_	au(Rmid K)={(q,z,d,a,u,c):qin D_	au}
]

where:

- (q): required distinction;
- (z): recoverability class;
- (d): minimum recovery depth;
- (a): assumption burden;
- (u): residual uncertainty;
- (c): operational cost.

The task-adapted state is the object compared across representation transformations.

## Non-leakage rule

A task contract must not contain:

- the expected primitive relation label;
- the expected retain/revise/defer/withhold state;
- language that presupposes a rehabilitation, correction, qualification, or accretion result;
- a task-specific transformation chosen because the expected answer is already known.

## Task preservation

A transformation (T_j) is task-preserving for (	au) when:

[
sigma_	au(T_j(R)mid K)
]

is equivalent to:

[
sigma_	au(Rmid K)
]

under the task's predeclared tolerance.

Two representations are task-equivalent when they yield the same task-adapted state under the same task and recovery contract.

## Scientific implication

The target is not a global ranking of representations.

The target is to identify which transformations preserve or alter the representational distinctions required by which scholarly tasks, under a fixed recovery contract.
