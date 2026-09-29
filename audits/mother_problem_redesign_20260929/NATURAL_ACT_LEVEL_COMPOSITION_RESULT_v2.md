# Natural act-level qualified composition result v2

Date: 2026-09-29
Status: NATURAL_ACT_COMPOSITION_REPLICATION_PASS.

## 1. Workflow

Workflow:

    natural-act-level-qualified-composition-v2

Successful run:

    36569809971

Head:

    45bc27858f8a1c1178f661563af19fca038c4f06

Artifact:

    11034225348

Artifact ZIP SHA-256:

    c3dea98b89508f2b1726a623c59664319e0c9292f05dddf10c7371dbff355ffe

The immediately preceding execution stopped before scientific qualification because the runner
used the wrong CSV field name:

    pass1_note

instead of:

    act_note

The frozen source rows, qualification engines, scientific cases and success criteria were
unchanged before the successful run.

## 2. Shared qualified engine

The same independently implemented target-bound engines handle both natural sequences:

    target_bound_oracle_v2
    target_bound_runtime_v2

Registered relation families include:

Contrast/history relations:
- CONTRADICTS_PRIOR;
- CORRECTION_OF_PRIOR_CRITICISM.

Source-native proposition relations:
- COMPETING_IDENTIFICATION;
- BIBLIOGRAPHIC_REPLY.

A static branch scan confirms neither engine contains case-specific strings for:
- Paper Money;
- Arbre Sec;
- PM01/PM02/PM03;
- ARBR proposition IDs.

Thus the replication does not use episode-specific qualification branches.

Oracle/runtime scientific agreement:

    exact

## 3. Paper Money replay under v2

Frozen page-verified sequence:

    PM01
    -> PM02
    -> PM03

Forward qualification:

    PM02:
        CONTRADICTS_PRIOR
        target = PM01
        -> ADD_ALTERNATIVE

    PM03:
        CORRECTION_OF_PRIOR_CRITICISM
        target = PM02
        -> RESOLVE

Generator sequence:

    ADD_ALTERNATIVE ; RESOLVE

After step 1:

    live claims = {PM01, PM02}

Final:

    live claim = {PM03}

Reverse PM03-at-S0:

    rejected
    reason = RELATION_TARGET_NOT_LIVE

History ablation:

    same current assertion projection
    different retained evidence/history projection

With full history:

    PM03 -> RESOLVE

With transition/evidence history removed:

    PM03 rejected
    reason = RELATION_TARGET_HISTORY_UNRESOLVED

Therefore in this natural sequence:

    Psi(S_full) = Psi(S_history_ablated)

does not imply:

    Gamma(S_full, e) = Gamma(S_history_ablated, e)

This is a direct natural demonstration that retained scholarly history can affect future action
availability.

## 4. Arbre Sec act-level replication

Frozen source:

    data/r3_verified_proposition_panel_v1.csv

All three relevant proposition rows are:

    PAGE_VERIFIED_BOTH

Sequence:

### Baseline

    ARBR-ID-1903
    Oriental Plane / Chinar identification

### First later act

    ARBR-ID-HS
    actor = Houtum-Schindler
    mediator = Cordier
    relation = COMPETING_IDENTIFICATION
    target = ARBR-ID-1903

Qualification:

    ADD_ALTERNATIVE

After step 1:

    live claims = {
        ARBR-ID-1903,
        ARBR-ID-HS
    }

### Second later act

    ARBR-REPLY-CORDIER
    actor = Cordier
    relation = BIBLIOGRAPHIC_REPLY
    target = ARBR-ID-HS

The previously frozen historical reading states:
- Cordier points to his earlier reading/citation of Schindler;
- explicit Cordier adoption of the cypress identification is not established.

Qualification:

    RECORD_EVIDENCE

Thus:

    Psi(before reply) = Psi(after reply)

while:

    Xi(before reply) != Xi(after reply)

Generator sequence:

    ADD_ALTERNATIVE ; RECORD_EVIDENCE

The current competing identifications remain live.

The reply changes responsibility/bibliographic history without pretending that Cordier adopted
the cypress identification.

## 5. Arbre Sec reverse-order test

Attempt:

    ARBR-REPLY-CORDIER

at the 1903 start state before:

    ARBR-ID-HS

exists.

Result:

    rejected
    reason = RELATION_TARGET_NOT_LIVE

and:

    Psi unchanged
    Xi unchanged

Therefore the reply action is enabled by the preceding proposal.

This is natural target-bound composition:

    proposal
    -> later reply-to-that-proposal

rather than an unordered bag of editorial statements.

## 6. Cross-relation-family portability

Paper Money uses:

    CONTRADICTS_PRIOR
    CORRECTION_OF_PRIOR_CRITICISM

Arbre Sec uses:

    COMPETING_IDENTIFICATION
    BIBLIOGRAPHIC_REPLY

The same engine implements both without episode-specific branches.

Observed generator structures:

    Paper Money:
        ADD_ALTERNATIVE ; RESOLVE

    Arbre Sec:
        ADD_ALTERNATIVE ; RECORD_EVIDENCE

Therefore qualified composition is not tied to one transition phenotype.

It supports both:
- assertion-changing continuation;
- assertion-identity/history-nonidentity continuation.

## 7. What this adds beyond synthetic composition

The prior synthetic result established:

    state-dependent qualified generators
    + non-commutative two-step composition

The natural results now add:

### Relation-target identity

A later source relation can be unavailable because the specific proposition it targets has not
yet entered the state.

### History-dependent qualification

Paper Money shows a later correction can require retained transition history identifying how its
target entered the state.

### Act-level history-only action

Arbre Sec shows a source-grounded later reply can be a first-class scholarly action even when
current assertion values do not change.

### Relation-family portability

The same target-bound interface works over two pre-existing source relation families.

## 8. Revised formal object

The bounded qualification object should now be written more precisely as:

    Q(S, rho, target(rho), H, e, g)

where:
- S is the current scholarly assertion state;
- rho is a source-grounded relation;
- target(rho) is the specific prior claim/proposition to which the relation attaches;
- H is retained transition/evidence history when needed to interpret that target;
- e is the evidence/proposal;
- g is the qualified generator.

Then:

    Gamma(S,rho,target,H,e)
    =
    { g : Q(S,rho,target,H,e,g) }

and:

    S_(t+1) = g_t(S_t)

with retained history:

    H_(t+1)

feeding later qualification.

## 9. Implication for prior false positives

The earlier false-positive failures can now be organized at a stronger level:

- wrong object;
- wrong proposition;
- wrong source/version;
- absent relation target;
- lost target history;

can all create:

    false generator availability

or:

    false generator unavailability.

Thus researchability requires preserving not just current proposition values but the relational
history that determines which future scholarly acts are meaningful.

## 10. Evidence ceiling

This result is:

    natural
    page-verified
    exposed/development
    two-sequence
    one historical corpus

It is not:
- prospective fresh confirmation;
- cross-corpus composition confirmation;
- prevalence evidence;
- a universal algebra.

Paper Money remains event-level at PM03 because its earlier claim-event row combines two Laufer
acts, although its internal stance traces are separately page-verified.

Arbre Sec supplies the cleaner act-level replication.

## 11. Next empirical burden

The principal remaining composition burden is now:

    prospective / independent ecological qualified-composition confirmation

A high-value next corpus should expose:
- explicit proposition/event targeting;
- at least two connected sequential scholarly acts;
- source-native relations that can be frozen before outcome;
- enough history to test whether the second action depends on the first;
- a deterministic denominator if population-level claims are desired.

Another exposed Yule-Cordier sequence would add robustness but is no longer the highest-value
scientific move.
