# Natural qualified composition result v1 — Paper Money

Date: 2026-09-29
Status: NATURAL_COMPOSITION_PASS / EVENT-LEVEL NATURAL DEVELOPMENT.

## 1. Workflow

Workflow:

    natural-qualified-composition-paper-money-v1

Run:

    36568697213

Artifact:

    11033530207

Artifact ZIP SHA-256:

    96c7b73a95898a2389d03f0c87e68ebd6596935cdd30f368513384ed15ed1ffe

## 2. Frozen source sequence

All source rows pre-existed the qualified-composition experiment.

Claim events:
- PM01 base narrative;
- PM02 1903 criticism;
- PM03 1920 correction/rehabilitation.

Stance traces:
- PMT01: Bretschneider/Cordier criticism of the Marco Polo material identification;
- PMT02: Laufer/Cordier correction of Bretschneider's prior statement;
- PMT03: Laufer/Cordier endorsement of the Marco Polo material identification.

The claim-event rows are page-image verified.

The stance traces are PAGE_VERIFIED.

The relation ontology already contains:

    CORRECTION_OF_PRIOR_CRITICISM

## 3. Target-bound natural forward sequence

Initial:

    S0 = {PM01}

PM02:

    relation = CONTRADICTS_PRIOR
    relation target = PM01

Qualified generator:

    ADD_ALTERNATIVE

After PM02:

    S1 = {PM01, PM02}

PM03:

    relation = CORRECTION_OF_PRIOR_CRITICISM
    relation target = PM02

Qualified generator:

    RESOLVE

Final current claim:

    {PM03}

Registered forward generator sequence:

    ADD_ALTERNATIVE ; RESOLVE

Oracle/runtime agreement:

    exact

## 4. Reverse-order test

Attempt PM03 at S0.

PM03 names PM02 as its historical relation target.

But PM02 is not yet live.

Result:

    qualified = false
    reason = RELATION_TARGET_NOT_LIVE

and:

    Psi unchanged
    Xi unchanged

Thus the later action is not generically available from the earlier state.

The natural sequence exhibits target-bound partial non-commutativity:

    PM02 ; PM03 is defined

while:

    PM03 first is not defined.

## 5. History ablation

Construct:
- S1_full with PM01 and PM02 plus complete transition/evidence history;
- S1_psi_only with exactly the same current assertions and no retained ledgers.

Observed:

    Psi(S1_full) = Psi(S1_psi_only)

while:

    Xi(S1_full) != Xi(S1_psi_only)

PM03 qualification:

With full history:

    RESOLVE

With identical current assertions but erased history:

    qualified = false
    reason = RELATION_TARGET_HISTORY_UNRESOLVED

Therefore:

> identical current assertion state does not imply identical future scholarly-action availability.

For this natural sequence, retained transition history is required to determine that PM02 is the
prior criticism that PM03 corrects.

This directly supplies a natural source-grounded positive result for the earlier
FUTURE_QUALIFICATION_BLIND_SPOT.

## 6. v1 relation-type-only diagnostic

The earlier qualified-generator v1 does not bind a relation to a specific prior claim.

Projecting:

    CORRECTION_OF_PRIOR_CRITICISM
    -> REPLACES_PRIOR

and applying the PM03 proposal directly at S0 yields:

    qualified = true
    generator = REPLACE

This is false generator availability relative to the source-grounded PM03 relation because the
criticized PM02 claim does not yet exist.

Therefore:

    state shape + relation type

is still insufficient.

The required object is more precise:

    Q(S, rho, target(rho), e, g)

where the relation target and, for some relations, its retained transition history are part of
qualification.

## 7. Scientific implication

The result strengthens the dynamic mother problem:

    current state values
    + relation type

are not enough.

A representation may need to preserve:
- which prior claim the relation targets;
- how that prior claim entered the scholarly state;
- the evidence/provenance binding of that earlier transition.

Otherwise it can permit a later scholarly action before the historical object that licenses that
action exists.

This gives a unified reading of prior false positives as false action availability.

## 8. Important act-granularity ceiling

The event-level PM03 row combines two analytically distinct page-verified Laufer acts:

1. correction of Bretschneider's prior criticism;
2. positive corroboration/rehabilitation of Polo.

The later R3 act-segmentation protocol explicitly requires these to be distinguished.

Therefore this result is licensed as:

    page-verified event-level natural composition development

not as final act-level ecological closure.

The next replication should use already segmented proposition/act records so that composition is
tested without collapsing multiple scholarly acts into one event.

## 9. Claim ceiling

Supported:

> In the page-verified Paper Money sequence, the availability of the 1920 correction depends on
> the existence and retained transition history of the 1903 criticism it targets, even when the
> current assertion projection is held fixed.

Not supported:
- prevalence;
- universal history dependence;
- universal algebra;
- act-level closure of the Paper Money entry itself.
