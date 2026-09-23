# Recovery Contract and Recoverability Profile v1

Date frozen: 2026-09-24

## Recovery contract

Recoverability is always relative to a declared contract:

[
K=(Omega,mathcal O,H,B,Gamma)
]

where:

- **Omega — evidence scope**: which representational regions are visible;
- **O — permitted operations**: read, search, follow explicit links, compare supplied passages, inspect supplied metadata;
- **H — background knowledge**: H0/H1/H2 from Task Contract v1;
- **B — budget**: permitted traversal, search, and inspection budget;
- **Gamma — target distinction**: the exact relation or representational distinction to be recovered.

Changing any member of (K) defines a new recovery experiment.

## Recoverability classes

For a required distinction (q):

- **E — explicit**: directly encoded or directly queryable;
- **R — recoverable**: not explicit but uniquely reconstructible under the frozen contract;
- **Q — unresolved**: more than one materially different assignment remains compatible;
- **U — unavailable**: the distinction cannot be recovered under the contract.

Higher reconstruction cost alone does not justify U.

## Minimum recovery depth

Depth describes the smallest evidence boundary required for recovery, not the number of mouse clicks.

- **D0 — structured explicit**: the required distinction is directly encoded.
- **D1 — intrinsic span**: the supplied span itself is sufficient.
- **D2 — local documentary context**: heading, note, signature, neighboring passage, or local metadata is required.
- **D3 — intra-object traversal**: another section, page, edition layer, addendum, or linked component within the same declared digital object is required.
- **D4 — external witness**: a printed witness, external edition, source registry, or external scholarly source is required.
- **NA**: no finite depth exists under the contract because the distinction is Q or U.

## Assumption burden

- **A0 — none beyond explicit representation**
- **A1 — document-internal convention/inference**
- **A2 — general bibliographic/domain knowledge**
- **A3 — case-specific scholarly identification or interpretation**

Primary experiments under H0 may use A0-A1 only. A2-A3 require a different contract.

## Residual uncertainty

- **U0 — resolved**
- **U1 — one low-impact ambiguity remains**
- **U2 — multiple materially different relation assignments remain**

U2 normally maps to recoverability class Q.

## Operational cost

Operational cost is recorded separately from depth.

At minimum record:

- number of searches;
- number of additional spans inspected;
- number of cross-layer traversals;
- number of external witnesses consulted;
- elapsed time when a human study is run.

No universal scalar cost function is assumed in v1.

## Recoverability profile

[
ho(q,Rmid K)=(z,d,a,u,c)
]

Depth is therefore one coordinate of the recovery profile, not the whole construct.

## Primary main-effect quantity

For fixed ((	au,K)), a transformation effect is:

[
Delta sigma_{	au,j}
=
sigma_	au(T_j(R)mid K)-sigma_	au(Rmid K)
]

This may be nonzero even when the final humanistic claim state is unchanged.

That separation is intentional.
