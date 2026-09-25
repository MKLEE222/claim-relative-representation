# LLM Judge Contract v1

Date frozen: 2026-09-25
Status: FROZEN BEFORE FIRST JUDGE OUTPUT

## Scientific role

The LLM is a computational adjudication instrument, not a human-subject proxy.

It receives only the frozen claim, fixed PM01/PM02 context, one anonymous 12-candidate evidence packet, and the adjudication rubric.

It does not receive:
- retrieval-policy identity;
- target rank;
- packet mapping;
- author provisional warrant state;
- expected effect direction;
- prior experimental reports.

## Output schema

For one packet, return exactly:

- epistemic_relations: subset of E_SUPPORT | E_UNDERCUT | E_QUALIFY_AUTHORITY | E_REHABILITATE | E_ACCRETION | E_IDENTIFICATION_UPDATE | E_UNRESOLVED
- warrant_state: RETAIN | REVISE | DEFER | WITHHOLD
- decisive_evidence: candidate/span IDs only
- rationale: <= 120 words, source-bounded
- unresolved_dependency: empty unless warrant_state=DEFER

## Evidence discipline

Use only the supplied packet.
Do not use outside historical knowledge.
Do not infer that later-dated evidence is better merely because it is later.
Do not infer that an explicit historical endorsement is automatically correct.
Judge claim entitlement under the supplied editorial record.

## Warrant states

RETAIN: claim remains usable as stated under supplied evidence.
REVISE: supplied evidence licenses a materially narrower/corrected formulation rather than the claim as stated.
DEFER: materially different epistemic assignments remain live and the packet does not license choosing among them.
WITHHOLD: supplied evidence does not license using the claim as stated.

## Relation/state separation

Relation labels do not mechanically determine warrant state.

## Null retention

If both packets receive the same warrant state, retain the null.

## Stability plan

Primary judge run:
- Packet A and Packet B adjudicated independently under the same prompt.

Perturbation audit:
- reverse candidate order;
- relabel candidate IDs without changing text;
- swap packet presentation order.

A warrant consequence is called stable only if the warrant state is invariant to evidence order/ID relabeling for each packet.

## Current-runtime limitation

The first execution in this conversation uses GPT-5.6 Sol after the research design has already been discussed in the same conversation.

Therefore this execution is recorded as:

`J0_SAME_SESSION`

and is not described as an independent blinded replication.

It may close the computational pipeline operationally, but any manuscript wording using the stronger phrase 'blinded independent LLM judge' requires a fresh stateless/model-separated replication.