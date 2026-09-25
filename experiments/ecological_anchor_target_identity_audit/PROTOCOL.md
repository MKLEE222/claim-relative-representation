# Paper-Money Retrieval Target-Identity Audit v1

Date frozen: 2026-09-25
Status: METRIC REPAIR BEFORE FINAL WARRANT CLOSURE

## Why this audit is required

The original E1/E1D/E1W retrieval evaluations treated a candidate as a target hit when its sliding-window start lay within one stride of a separately located target window.

That rule can mark a neighboring window as a hit even when the candidate itself does not visibly contain the target passage.

This is unacceptable for the later warrant experiment, where "surfaced for inspection" must mean that the candidate itself materially contains the target evidence.

## Frozen strict target rule

A candidate window is a target hit iff the candidate window itself contains both target anchor sets:

- {regarding, bretschneider}
- {laufer}

No proximity-to-target-window heuristic is used.

This rule is frozen before rerunning any E1/E1D/E1W result.

## Policies

No retrieval policy changes.

The audit reuses exactly:

- E1 generic seed-similarity ranking;
- E1D named-source chain;
- E1D named-source + seed-domain filter;
- E1W sequence-guided source chain;
- E1W sequence-guided source + seed-domain chain.

Only target evaluation changes.

## Source identity

The same frozen Gutenberg hashes are required:

V1:
7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5

V2:
c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

## Outcome discipline

The strict audit supersedes the old hit/rank/ordinal numbers for all downstream warrant-closure use.

The original runs remain historical development evidence and are not overwritten.

Possible outcomes:

- same result;
- worse rank/ordinal;
- target absent from candidate set.

Any result is retained.

## Consequence for warrant closure

No Stage-B active-evidence or final LLM packet may use PM03 presence until this strict target audit has completed successfully on the frozen source hashes.
