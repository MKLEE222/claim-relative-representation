# Natural qualified composition protocol v1 — Paper Money

Date frozen: 2026-09-29
Status: PRE-EXECUTION / EXISTING EXPOSED SOURCE EVIDENCE ONLY.

## 1. Purpose

Test qualified multi-step scholarly composition on a naturally occurring three-layer historical
sequence already preserved in the repository:

    PM01 base narrative
    PM02 1903 editorial criticism
    PM03 1920 correction of the prior critic + endorsement of the original material claim

No fresh source is opened.

The experiment is not allowed to redesign the historical relations after observing generator
outcomes.

## 2. Frozen source assets

Git blobs:

    data/yule_cordier_claim_events.csv
    807e2aeef5054553e59de1cd017a216dfa46283d

    data/paper_money_archival_stance_traces_v1.csv
    7a032f814536911fa27001dbbb93660cd0f67221

    experiments/deepening_v1/R3_RELATION_ONTOLOGY_AMENDMENT_v2.md
    54b859edc59cf3ae008a76cf7dff7053d151280d

The claim-event rows are page-image verified.

The stance traces are PAGE_VERIFIED.

No new historical reading is introduced by this protocol.

## 3. Frozen natural sequence

### PM01 — base assertion

Historical layer:

    base narrative

Normalized scholarly claim:

    claim_id = PM01
    target = paper-money-material-identification
    value = MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE
    status = NARRATIVE_ASSERTED

This normalization refers only to the material-identification proposition needed for the dynamic
test. It does not assert universal historical truth beyond the inspected source.

### PM02 — 1903 criticism

Source event:

    actor = Emil Bretschneider as transmitted by Henri Cordier
    cue = "He seems to be mistaken."
    target = Marco Polo material identification

Frozen relation:

    CONTRADICTS_PRIOR

Relation target:

    PM01

Normalized proposal:

    claim_id = PM02
    value = MULBERRY_BARK_IDENTIFICATION_MISTAKEN
    status = EDITORIAL_CRITICISM_ASSERTED

### PM03 — 1920 correction of prior critic

Source event:

    actor = Berthold Laufer as transmitted by Henri Cordier

Verified cues:

    "This is a singular error of Bretschneider."
    "Marco Polo is perfectly correct."

The first cue targets Bretschneider's prior statement.

The second endorses the original Marco Polo material identification.

Frozen source relation:

    CORRECTION_OF_PRIOR_CRITICISM

Relation target:

    PM02

Normalized proposal:

    claim_id = PM03
    value = MULBERRY_BARK_PAPER_MONEY_PLAUSIBLE
    status = RESTORED_AS_CORRECT

## 4. Why relation-target identity is required

A relation type alone is insufficient.

PM03 does not license a generic replacement of any current paper-money assertion.

It specifically corrects PM02.

Therefore the qualified evidence input is extended with:

    relation_target_claim_id

A state-changing relation that names a prior claim is qualified only if that claim is live in the
current target assertion set.

If the relation target is absent:

    Gamma = empty
    reason = RELATION_TARGET_NOT_LIVE

No evidence/history ledger mutation is allowed on this rejected action.

## 5. Target-bound relation vocabulary

This experiment adds no new historical relation ontology.

It uses:

    CONTRADICTS_PRIOR
    CORRECTION_OF_PRIOR_CRITICISM

The second relation already exists in R3_RELATION_ONTOLOGY_AMENDMENT_v2.

For target-bound qualification:

### CONTRADICTS_PRIOR

Require:

    relation_target_claim_id is live.

If proposed value differs from the target claim's value and the state is not unresolved:

    ADD_ALTERNATIVE

If proposed value is the same and status differs:

    REVISE_STATUS

### CORRECTION_OF_PRIOR_CRITICISM

Require:

    relation_target_claim_id is live.

Require the relation target to be a live competing/critical assertion.

If:
- more than one live assertion exists; and
- the proposed value matches exactly one other live assertion;

then:

    RESOLVE

Otherwise:

    relation-state mismatch / no generator.

This rule is frozen specifically from the semantics of correcting a prior criticism.
It is not inferred from the desired output.

## 6. Natural forward composition

Initial:

    S0 = {PM01}

Step 1:

    e1 = PM02
    relation_target_claim_id = PM01

Required:

    Q(S0,e1) = ADD_ALTERNATIVE

yielding:

    S1 = {PM01, PM02}

Step 2:

    e2 = PM03
    relation_target_claim_id = PM02

Required:

    Q(S1,e2) = RESOLVE

yielding a single current material-identification assertion represented by PM03 and retaining the
full history of PM01 -> PM02 -> PM03.

Registered natural generator sequence:

    ADD_ALTERNATIVE ; RESOLVE

## 7. Counterfactual reverse-order test

At S0, attempt PM03 before PM02 exists.

Because:

    relation_target_claim_id = PM02

and PM02 is not live:

    Q(S0,e2) = empty

Required disposition:

    RELATION_TARGET_NOT_LIVE

Therefore the reverse historical order is structurally undefined.

This is partial non-commutativity / history-sensitive enablement:

    e2 o e1 is defined
    e1 o e2 is not defined at the same start state

where composition notation is interpreted in execution order.

The counterfactual is a controlled qualification test, not a claim that historians could actually
observe the reverse chronology.

## 8. Diagnostic against qualified-generator v1

The existing v1 qualified engine has no relation_target_claim_id binding.

For diagnostic purposes only, project:

    CORRECTION_OF_PRIOR_CRITICISM
    -> REPLACES_PRIOR

under the same S0 and PM03 proposal.

If v1 qualifies PM03 at S0, this demonstrates that relation-type + state-shape alone overpermits a
source relation whose historical target does not yet exist.

This diagnostic may expose a false generator availability.

It may not modify v1 results.

## 9. Independent implementations

Build:

    target_bound_oracle_v1
    target_bound_runtime_v1

They may reuse frozen string constants but must independently implement:
- relation-target binding;
- target-bound qualification;
- execution;
- history retention.

They must not call each other's qualification function.

## 10. Required checks

PASS requires:

1. frozen source blob verification;
2. page-verified PM01/PM02/PM03 rows found exactly once;
3. PAGE_VERIFIED PMT01/PMT02/PMT03 rows found exactly once;
4. operation absent from target-bound event input;
5. oracle/runtime exact;
6. forward:
       PM02 -> ADD_ALTERNATIVE
       PM03 -> RESOLVE
7. S1 contains PM01 and PM02 before PM03;
8. PM03 reverse-at-S0 rejected as RELATION_TARGET_NOT_LIVE;
9. rejected reverse leaves Psi and Xi unchanged;
10. final current assertion is PM03;
11. full transition history retains PM01, PM02 and PM03 bindings;
12. v1 diagnostic reports whether generic relation qualification would overpermit PM03 at S0.

## 11. Disposition

NATURAL_COMPOSITION_PASS if all required checks pass.

TARGET_BINDING_REPAIR_INCOMPLETE if:
- target-bound engines disagree;
- relation target can be absent yet action applies;
- forward natural sequence fails;
- final history loses any event binding.

SOURCE_SEQUENCE_UNRESOLVED if frozen source rows do not support the declared sequence.

## 12. Claim ceiling

If passed:

> In the page-verified paper-money sequence, a 1903 criticism becomes a competing scholarly
> assertion and a 1920 correction is qualified as a resolution only because the criticized claim
> is already live. The later action is unavailable from the earlier state when its historical
> relation target is absent. Thus natural scholarly composition depends on relation-target
> identity as well as relation type and current state.

Not licensed:
- prevalence of this pattern;
- universal completeness of target-bound relations;
- a universal scholarly action algebra;
- automatic extraction of historical relation targets from arbitrary prose.
