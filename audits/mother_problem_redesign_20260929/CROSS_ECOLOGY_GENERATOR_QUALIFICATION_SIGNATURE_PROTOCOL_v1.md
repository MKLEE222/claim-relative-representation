# Cross-ecology generator qualification signature audit v1

Date: 2026-09-30
Status: POST-FRESH / EXPOSED CROSS-ECOLOGY CONDITIONAL-MINIMALITY AUDIT.

## 1. Goal

Test whether generator-relative qualification signatures are a local property of the Formalization
Papers workflow or recur across distinct scholarly action ecologies.

Compare:

### Formalization Papers
- RECORD_REVIEW
- REPLACE_FORMALIZATION
- RECORD_RESPONSE
- REVISE_PUBLICATION_STATUS

### Yule-Cordier target-bound natural composition
- ADD_ALTERNATIVE
- RESOLVE
- RECORD_EVIDENCE

The goal is not to force identical field vocabularies across corpora.

The goal is to identify whether:

    retained-history dependence

and:

    live/target dependence

vary by generator rather than acting as universal requirements.

## 2. Evidence status

Formalization Papers:
- exposed corrected reproduction;
- closed 15-root population;
- 52 connected T0 chains;
- generator-signature audit already frozen.

Yule-Cordier:
- pre-existing exposed page-verified natural sequences;
- Paper Money;
- Arbre Sec;
- shared case-independent target-bound v2 engine.

No fresh evidence claim is made.

## 3. Shared signature dimensions

Cross-ecology comparison uses only dimensions that have a meaningful analogue in both systems:

### TARGET_IDENTITY
The act is bound to a specific prior scholarly object/claim/update rather than relation type alone.

### TARGET_LIVE_OR_CURRENT
The target must be present in the action-relevant current state.

### RETAINED_TRANSITION_HISTORY
Qualification needs retained history showing how the target entered the state.

### VERSION_OR_VALIDITY_STATE
Where the action family exposes this dimension, a superseded/retracted/invalid target is not
treated as live.

Use:

    REQUIRED
    NOT_REQUIRED_IN_REGISTERED_TASK
    ROOT_ACTION_NO_PRIOR_HISTORY
    NOT_APPLICABLE

Do not infer a universal signature from missing probes.

## 4. Yule-Cordier natural action denominators

### Y_ADD_ALTERNATIVE

Two page-verified acts:
- Paper Money PM02 CONTRADICTS_PRIOR targeting PM01;
- Arbre Sec ARBR-ID-HS COMPETING_IDENTIFICATION targeting ARBR-ID-1903.

For each:

Valid:
- exact live target qualifies as ADD_ALTERNATIVE.

Target ablation:
- replace relation_target_claim_id with a nonexistent/foreign claim id.
- require RELATION_TARGET_NOT_LIVE.

History ablation:
- the start state already has no transition history.
- valid action must still qualify.

Signature:

    TARGET_IDENTITY = REQUIRED
    TARGET_LIVE_OR_CURRENT = REQUIRED
    RETAINED_TRANSITION_HISTORY = NOT_REQUIRED_IN_REGISTERED_TASK

### Y_RESOLVE

One page-verified act:
- Paper Money PM03 CORRECTION_OF_PRIOR_CRITICISM targeting PM02.

Construct S1 through the frozen PM02 ADD_ALTERNATIVE transition.

Valid:
- PM03 qualifies as RESOLVE.

History ablation:
- preserve exact live assertions {PM01,PM02};
- remove evidence/event/transition ledgers;
- require RELATION_TARGET_HISTORY_UNRESOLVED.

Target substitution:
- point PM03 to PM01 while keeping current assertions unchanged.
- require rejection.

Signature:

    TARGET_IDENTITY = REQUIRED
    TARGET_LIVE_OR_CURRENT = REQUIRED
    RETAINED_TRANSITION_HISTORY = REQUIRED

### Y_RECORD_EVIDENCE

One page-verified act:
- Arbre Sec bibliographic reply targeting ARBR-ID-HS.

Construct S1 through the frozen competing-identification ADD_ALTERNATIVE transition.

Valid:
- reply qualifies as RECORD_EVIDENCE.

History ablation:
- preserve live assertions and exact target ARBR-ID-HS;
- erase evidence/event/transition ledgers;
- require the reply still qualifies as RECORD_EVIDENCE.

Target ablation:
- attempt reply before ARBR-ID-HS exists;
- require RELATION_TARGET_NOT_LIVE.

Signature:

    TARGET_IDENTITY = REQUIRED
    TARGET_LIVE_OR_CURRENT = REQUIRED
    RETAINED_TRANSITION_HISTORY = NOT_REQUIRED_IN_REGISTERED_TASK

## 5. Formalization Papers input

Do not redefine the already frozen Formalization signatures.

Use the result established by:

    FORMALIZATION_PAPERS_GENERATOR_QUALIFICATION_SIGNATURE_RESULT_v1.md

and, in machine execution, reproduce the same action-level audit from the byte-identical corrected
population.

Expected history signatures:

    RECORD_REVIEW
        ROOT_ACTION_NO_PRIOR_HISTORY

    REPLACE_FORMALIZATION
        NOT_REQUIRED_IN_REGISTERED_TASK

    RECORD_RESPONSE
        REQUIRED

    REVISE_PUBLICATION_STATUS
        NOT_REQUIRED_IN_REGISTERED_TASK

## 6. Cross-ecology decision rule

PASS only if:

1. all Formalization action-level signature probes remain PASS;
2. both Yule ADD_ALTERNATIVE acts satisfy the registered signature;
3. Yule RESOLVE satisfies history-required signature;
4. Yule RECORD_EVIDENCE satisfies history-not-required signature;
5. oracle/runtime agreement is exact for every Yule probe;
6. at least one history-required and one history-not-required generator exists in each ecology.

Desired cross-ecology structure:

    Formalization:
        RECORD_RESPONSE -> history REQUIRED
        update/decision -> history NOT REQUIRED

    Yule-Cordier:
        RESOLVE -> history REQUIRED
        ADD_ALTERNATIVE / RECORD_EVIDENCE -> history NOT REQUIRED

## 7. Scientific interpretation

If PASS:

> Qualification is generator-relative across two different scholarly ecologies. Retained
> transition history is load-bearing for some later acts, but making it a universal prerequisite
> would incorrectly overconstrain other legitimate acts.

This supports:

    Sigma(g)

as the appropriate theoretical object.

## 8. Claim ceiling

This audit does not establish:
- globally minimal signatures;
- that untested history never matters;
- completeness of the generator vocabularies;
- a universal scholarly action algebra;
- literal fresh confirmation.

It establishes conditional heterogeneity over the registered natural action families only.
