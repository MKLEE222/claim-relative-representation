# Module I pre-holdout protocol amendment v1 — controlled null event

Date: 2026-09-28
Status: PRE-HOLDOUT AMENDMENT BASED ONLY ON EXPOSED DEVELOPMENT CORPORA.

## 0. Reason

After the hardened oracle/runtime split, both exposed development corpora produced nontrivial discovery pools but zero full trajectories because no episode satisfied the old requirement for a naturally occurring revisionDesc maintenance event under the frozen neutral classifier.

Observed development-only diagnostics:
- Berlin: 190 parsed, 29 primary discovery episodes, 0 full trajectories; all 29 lacked a qualifying natural revisionDesc null event.
- Paul: 1515 parsed, 26 primary discovery episodes, 0 full trajectories for the same reason.

This reveals a design confound: the mother-problem null requirement is about whether an irrelevant event causes gratuitous epistemic revision. It does not require the null event itself to be a naturally occurring scholarly-history record.

No StaBi holdout XML body has been opened.

## 1. Superseded rule

The previous requirement:

    one qualifying natural revisionDesc maintenance event must exist

is removed from FULL_TRAJECTORY eligibility.

revisionDesc remains descriptive source history only and is not used as a gate or historical-evidence carrier in Module I.

## 2. Controlled null event

Every full trajectory receives the same frozen intervention:

    event_id: CONTROL_NULL_V1
    event_class: NON_TEMPORAL_MAINTENANCE
    target_document: current document
    operation: REFRESH_NON_TEMPORAL_METADATA_INDEX
    temporal_targets: []
    payload: {"index_family":"presentation-metadata","revision":"v1"}

The event is a controlled no-op with respect to the temporal research state.

It is executed through the same runtime transition operator as other events.

Success requires an actual before/after state diff showing:
- no temporal claim mutation;
- no warrant mutation;
- no live-alternative mutation;
- no Q0 mutation.

The event may append an event/transition ledger record.

## 3. Independent oracle treatment

The oracle does not infer null stability from runtime output.

It independently declares CONTROL_NULL_V1's temporal target set as empty and expects the temporal state after the event to equal the temporal state before the event.

Runtime mutation under the control must therefore fail evaluation.

## 4. Revised full-trajectory eligibility

A primary discovery episode enters FULL_TRAJECTORY iff:
1. canonical primary origDate exists behind OPEN_ORIGIN;
2. W_root != W_post_origin;
3. delayed audit is defined by the frozen interface contract.

A natural revisionDesc event is no longer required.

## 5. Scientific interpretation

CONTROL_NULL_V1 is a causal stability control, not natural historical evidence.

Claims about naturally occurring editorial revision remain carried by Modules D-G.

Module I uses the controlled null only to test:

    irrelevant maintenance event
    -> no gratuitous change to temporal warrant

## 6. Anti-flexibility rule

CONTROL_NULL_V1 is frozen before holdout execution.

No holdout-specific alternative null event may be substituted.

No revisionDesc wording from the holdout may be used to make an episode eligible.

All other Module I protocol, representation, discovery, warrant, applicability, selectivity and delayed-audit rules remain unchanged.