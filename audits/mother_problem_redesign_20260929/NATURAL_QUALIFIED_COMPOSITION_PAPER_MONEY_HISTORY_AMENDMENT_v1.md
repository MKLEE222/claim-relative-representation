# Paper Money natural composition history-binding amendment v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-OUTCOME AMENDMENT.

## 1. Reason

The base natural-composition protocol preserves relation_target_claim_id.

A stronger test is available from the same already verified source sequence.

The fact that PM02 is a prior criticism should not be encoded redundantly in the current assertion
status if the experiment is intended to test whether retained transition history matters for
future action qualification.

Therefore the normalized current-assertion projection is made relation-neutral.

## 2. PM02 normalized assertion status

Replace the protocol-only PM02 status:

    EDITORIAL_CRITICISM_ASSERTED

with:

    ASSERTED

The source-grounded fact that PM02 is a criticism of PM01 remains preserved in the transition
history created by e1:

    evidence_relation = CONTRADICTS_PRIOR
    relation_target_claim_id = PM01
    generated_claim_id = PM02

This amendment does not alter the source interpretation.

It changes only where that relation is represented.

## 3. Target-history qualification for CORRECTION_OF_PRIOR_CRITICISM

PM03 is qualified only if all of the following hold:

1. relation_target_claim_id = PM02 is live;
2. retained transition history contains a transition that generated PM02;
3. that transition has:
       evidence_relation = CONTRADICTS_PRIOR
   and:
       relation_target_claim_id = PM01
4. PM03 proposes the value of another live alternative, PM01.

Then:

    generator = RESOLVE

If PM02 is live but the required relation history is missing:

    Gamma = empty
    reason = RELATION_TARGET_HISTORY_UNRESOLVED

## 4. History-ablation test

Construct:

    S1_full

after PM02 with complete evidence/event/transition history.

Construct:

    S1_psi_only

with exactly the same current assertions as S1_full but empty evidence/event/transition ledgers.

Required:

    Psi(S1_full) = Psi(S1_psi_only)

and:

    Q(S1_full, PM03) = RESOLVE

while:

    Q(S1_psi_only, PM03) = empty
    reason = RELATION_TARGET_HISTORY_UNRESOLVED

Therefore:

    identical current assertion state
    !=
    identical future generator availability

when transition history required to interpret a source-grounded later relation has been lost.

## 5. Scientific role

If passed, this directly resolves the earlier future-qualification blind spot for one natural
source-grounded sequence.

It supports the bounded proposition:

> Retained scholarly history can be causally required for determining which later action is
> licensed, even when the currently visible assertions are identical.

It does not establish that every scholarly relation requires historical transition memory.
