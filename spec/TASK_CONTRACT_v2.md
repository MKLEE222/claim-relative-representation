# Task Contract v2 - candidate distinctions, not assumed necessities

Date frozen: 2026-09-24
Status: DESIGN FREEZE BEFORE EXPERIMENT

## Why v2

Task Contract v1 called task-linked coordinates "required distinctions". That language was too strong: Experiment 1A already showed that one carrier can substitute for another. A task may remain executable after an explicit coordinate is removed because the same distinction is recoverable from lexical or contextual evidence.

v2 therefore freezes a **candidate distinction universe** and a separate **dependency hypothesis**. Necessity and sufficiency are experimental results, not task-definition inputs.

## Task contract

[
	au=(Q,I,D^{cand},Y,H,S)
]

where:

- **Q**: answer-neutral scholarly question;
- **I**: frozen input/source objects;
- **D_cand**: candidate representational distinctions plausibly relevant to the task;
- **Y**: admissible task-output space;
- **H**: background-knowledge state;
- **S**: success rule.

A separate preregistered hypothesis (D^{hyp}_	ausubseteq D^{cand}_	au) may predict which distinctions matter. It is not treated as ground truth.

## Candidate distinction vocabulary

- text_presence
- referent_identity
- attribution
- temporal_order
- claim_binding
- evidence_relation
- witness_identity
- editorial_layer
- distinction_class

New distinctions require a protocol revision before outcome inspection.

## Background knowledge

### H0
Representation-internal information only.

### H1
General bibliographic/domain conventions, excluding case-specific Yule-Cordier scholarship.

### H2
Case-specific scholarship.

Primary experiments use H0. H1/H2 are sensitivity conditions, not rescue routes.

## Task family

The main family remains:

- tau_locate
- tau_attribute
- tau_sequence
- tau_bind
- tau_relation
- tau_adjudicate

Only tau_adjudicate may emit retain/revise/defer/withhold, and that stage remains sealed until upstream validation passes.

## Task-adapted state

For each candidate distinction (q):

[
sigma_	au(Rmid K)
=
{ho(q,Rmid K):qin D^{cand}_	au}
]

with recoverability profile:

[
ho=(z,d,b,a,u,c)
]

where (b) is the recovery **basis/carrier**.

## Carrier substitution

A distinction may be supported by more than one carrier:

- structured metadata;
- lexical cue;
- local documentary context;
- explicit pointer/link;
- cross-layer context;
- external witness.

Removing one carrier does not imply removing the distinction.

This is now a central experimental mechanism.

## Executability

A task is executable under ((R,K)) when enough candidate distinctions are recoverable, within the declared uncertainty and budget, to produce an admissible task output under the frozen success rule.

Executability is observed; it is not assumed from the candidate distinction list.

## Output equivalence versus burden equivalence

Two representations can be output-equivalent while differing in recovery burden.

Define:

[
R_1equiv^{out}_{	au,K}R_2
]

when they yield the same admissible output set for the task.

Define:

[
R_1equiv^{profile}_{	au,K}R_2
]

only when their task-adapted recoverability profiles are also equivalent.

The project reports these separately.

## Minimal sufficient distinction families

Let (Y_	au(R,K)) be the admissible output set for task (	au).

A set (Msubseteq D^{cand}_	au) is sufficient when exposing only the information carried by (M) reproduces the reference task output set.

There may be multiple minimal sufficient sets:

[
mathcal M_{	au,K}
=
{M: M	ext{ is sufficient and no strict subset of }M	ext{ is sufficient}}
]

The project therefore does not assume one unique necessary representation.

## Experimental necessity

A coordinate is called necessary only **within the frozen representation family and contract** when removing all admissible carriers of that distinction changes the task output set or makes the task unresolved, and restoration reverses that change.

This is not a universal historical necessity claim.

## Anti-leakage rule

Task wording must not contain the expected relation class or final claim state. The dependency hypothesis is stored separately from task wording and may fail.
