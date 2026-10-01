# Module D2 results — natural combined epistemic and relation revision in Whitman history

Date: 2026-09-28
Status: EXECUTED PRE-DIFF-FROZEN DEVELOPMENT PRESSURE TEST. DISTINCT FROM D1; NOT INDEPENDENT TRANSFER.

Authoritative execution:
- GitHub Actions run 36378861851
- artifact: module-d2-whitman-combined-revision-v1
- artifact ID: 10951868316
- artifact ZIP SHA-256: 574f832def80d2617f4cd25b7c8243ac839109e7e96231eb036a5433bb5e3bb1
- results SHA-256: d47a0040dd255c94d9c5c7874563502d1e2ec6684b65e9927a128d85a642de36

## 1. Natural event

Parent:
fe63fcfbeca16f85583a29355c2d3a44e09b280f

Child:
8c6aba338bd3b8a52ec74d014ec1afc8137cc4a9

Child message:
adjusted certainty and some relations

The pair was frozen before the file delta was opened.

## 2. Complete delta

Parent relation records:
1,436

Child relation records:
1,435

Natural delta:
- certainty changed: 141
- relations added: 7
- relations removed: 8
- unchanged: 1,287
- affected printed targets: 113
- affected source files: 30

All 141 certainty changes are:

    low -> high

The event therefore combines broad epistemic-status revision with localized relation-topology change.

## 3. Current endpoint task

Unlike D1, endpoint topology changes.

Parent printed targets:
761

Child printed targets:
761

But:
- 3 printed targets newly appear;
- 3 printed targets disappear;
- 13 printed targets change endpoint set.

Therefore:

    Q0_endpoint(parent) != Q0_endpoint(child)

The correct continuation must revise both relation presence and epistemic status selectively.

## 4. Full relation-state update

R_FULL_RELATION_STATE:
- changed certainties correct: YES
- added relations correct: YES
- removed relations correct: YES
- every unaffected relation stable: YES
- collateral changes: 0
- complete child state exact: YES

Thus the natural patch reproduces:

    141 status changes
    + 7 additions
    + 8 removals
    + 1,287 unaffected relations

without global collateral revision.

SELECTIVE_COMBINED_REVISION = YES.

## 5. Endpoint-only state

The identity-rich natural patch exposes status for changed/added records and endpoint topology for added/removed records.

It therefore knows 148 child status items from the event itself.

However, 1,287 unchanged relation-status items remain unavailable from an endpoint-only parent state without lawful reopening or retained epistemic state.

Complete child epistemic state:
NOT EXACT.

## 6. Coarse locus-status state

R_CERT_ONLY_STATE retains at each printed target:
- full parent endpoint set;
- number of high relations;
- number of low relations;
- HIGH_ONLY / LOW_ONLY / MIXED status;
- no endpoint-specific certainty binding.

For every affected locus, the evaluator enumerates all parent endpoint-specific certainty assignments compatible with those aggregate counts, then applies the exact natural identity-rich patch.

Affected loci:
113

Of these:
- certainty-only revision loci: 100
- topology-changing loci: 13

Result:
- uniquely exact child state: 113 / 113
- ambiguous affected loci: 0 / 113
- no-compatible-state loci: 0 / 113

Therefore:

COARSE_STATE_NONDETERMINING_ON_AFFECTED_LOCUS = NO

COARSE_STATE_SUFFICIENT_ON_ALL_AFFECTED_LOCI = YES

This is not because endpoint-specific certainty binding is generally redundant. It follows from the information jointly available in:
- the coarse parent state;
- the identity-rich natural patch;
- the exact add/remove identities.

D2 independently reinforces the D1 null against a state-only necessity claim.

## 7. Why the coarse state succeeds here

The event channel itself supplies:
- which relation identity changed;
- its old certainty;
- its new certainty;
- exact identities of added relations;
- exact identities of removed relations.

Across the affected loci, this information plus parent aggregate counts is sufficient to determine the exact child binding.

Hence dynamic determinacy cannot be assigned to the retained state in isolation.

The experimental object is the coupled system:

    retained research state
    + revision event channel
    + lawful source access
    + continuation task

## 8. Source reopening

Independent reconstruction from the pinned child relation source is exact.

R_SOURCE_REOPEN:
complete child state exact = YES

Child source bytes:
121,447

Ordinary source reopening remains a valid strong baseline.

## 9. Wrong-binding control

All 141 certainty changes are low -> high.

Therefore permuting the new certainty labels among changed identities produces no nontrivial alternative new-cert assignment.

The frozen matched certainty-permutation control is:

WRONG_CERT_BINDING_CONTROL_NOT_IDENTIFIABLE

No artificial high->low event was introduced.

## 10. Costs

Natural delta packet:
17,528 canonical JSON bytes

Full parent relation state:
149,387 canonical JSON bytes

Parent source:
121,563 bytes

Child source:
121,447 bytes

These are descriptive implementation encodings, not optimal information bounds.

## 11. Scientific disposition

NATURAL_COMBINED_REVISION_OBSERVED = YES

SELECTIVE_COMBINED_REVISION = YES

COLLATERAL_CHANGES = 0

COARSE_STATE_NONDETERMINING_ON_AFFECTED_LOCUS = NO

COARSE_STATE_SUFFICIENT_ON_ALL_AFFECTED_LOCI = YES

SOURCE_REOPEN_EXACT = YES

INDEPENDENT_TRANSFER = NO

## 12. Joint interpretation with D1

D1:
one real high -> low status revision; no endpoint change.

D2:
141 real low -> high status revisions plus 7 adds and 8 removals.

Both exhibit exact selective revision with no collateral updates.

But both also show that a weaker retained parent representation can be sufficient when the natural revision event carries strong identity-specific information.

Therefore the stronger dynamic claim:

    "retained state must itself preserve every future-needed binding"

is not supported.

The evidence instead motivates:

    DynamicSufficiency(state, event_channel, access_contract, task)

rather than:

    DynamicSufficiency(state alone)

## 13. Next experimental obligation

The next test should manipulate or find variation in the revision-event channel while keeping the natural revision target fixed.

For the same real revision, compare channels such as:
- identity-rich delta;
- target locator without old state;
- aggregate revision notice without relation identity;
- lawful child-source reopening;
- no revision channel.

This would identify which obligations may be distributed between retained state and incoming evidence rather than pre-stored redundantly.

Such a test must remain explicit that channel ablations are controlled experiments around a natural event.
