# Recovery Contract v2 - basis-aware recoverability

Date frozen: 2026-09-24
Status: DESIGN FREEZE BEFORE EXPERIMENT

## Contract

[
K=(Omega,mathcal O,H,B,Gamma)
]

- **Omega**: visible evidence universe;
- **O**: permitted recovery operations;
- **H**: allowed background knowledge;
- **B**: budget;
- **Gamma**: target distinction.

Changing any member defines a new recovery experiment.

## Recoverability profile

[
ho(q,Rmid K)=(z,d,b,a,u,c)
]

### z - recoverability class
- E: explicit
- R: recoverable
- Q: unresolved
- U: unavailable

### d - minimum evidence boundary
- D0: structured explicit
- D1: focal span
- D2: local documentary context
- D3: intra-object traversal
- D4: external witness
- NA: Q/U under the frozen contract

Depth measures evidence boundary, not clicks.

### b - recovery basis/carrier

A set drawn from:

- B_STRUCTURED_METADATA
- B_LEXICAL_CUE
- B_LOCAL_CONTEXT
- B_EXPLICIT_POINTER
- B_CROSS_LAYER_CONTEXT
- B_EXTERNAL_WITNESS

Multiple bases may coexist.

The **minimal basis family** is retained when more than one basis can independently recover the same distinction.

### a - assumption burden
- A0: none beyond explicit representation
- A1: document-internal convention/inference
- A2: general bibliographic/domain knowledge
- A3: case-specific scholarly identification or interpretation

Primary H0 runs permit A0-A1 only.

### u - residual uncertainty
- U0: resolved
- U1: low-impact ambiguity
- U2: materially different assignments remain

U2 normally maps to Q.

### c - operational cost vector

Record separately:
- searches;
- additional spans inspected;
- cross-layer traversals;
- external witnesses;
- elapsed time when measured.

No scalar cost weighting is assumed in v2.

## Basis substitution

The main mechanism exposed by Experiment 1A is basis substitution.

Example:

[
(E,D0,{B_{metadata}})
ightarrow
(R,D1,{B_{lexical}})
]

after removing explicit attribution metadata.

The relation did not disappear; its carrier changed.

## Basis exhaustion

A transformation establishes unavailability only when all carriers permitted by the frozen contract are exhausted:

[
B(q,Rmid K)=arnothing
]

or when remaining carriers leave materially different assignments unresolved.

This rule prevents metadata deletion from being mislabeled as evidence loss.

## Recovery burden

Burden change is represented by changes in (d,a,u,c), even when task output is preserved.

Thus the project distinguishes:

1. carrier loss;
2. carrier substitution;
3. burden increase;
4. unresolved recovery;
5. true unavailability.

## Primary comparison

For fixed ((	au,K)):

[
Deltasigma_{	au,j}
=
sigma_	au(T_j(R)mid K)-sigma_	au(Rmid K)
]

The primary analysis is structured by distinction and carrier, not pooled into a single global score.
