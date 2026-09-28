# Module D1 results — natural selective epistemic revision in Whitman relation history

Date: 2026-09-28
Status: EXECUTED PRE-DIFF-FROZEN DEVELOPMENT EVENT. NOT INDEPENDENT TRANSFER.

Authoritative execution:
- GitHub Actions run 36378708507
- artifact: module-d1-whitman-selective-revision-v1
- artifact ID: 10951843165
- artifact ZIP SHA-256: 35a7eac1d25bbcdde7bc9e0de53f3df27c99d03caccc0873bf054c3583fa8711
- results SHA-256: db3ce2a39f185b5166465b86b5139d7a4c4212d6de4f64de291fc8a50038694b

## 1. Natural revision event

Upstream:
whitmanarchive/whitman-LG_1855_variorum

Relation object:
source/authority/anc.02134.xml

Parent:
7cdf5ddc9d0cfff83289f687613ee3d0510e6520

Child:
fe63fcfbeca16f85583a29355c2d3a44e09b280f

Child commit message:
adjusted certainty

The commit pair and evaluation contract were frozen before opening the file delta.

The relation file defines certainty as the editors' level of certainty that the described manuscript or notebook line is a version of the printed line. Therefore this event is treated as an editorial epistemic-status revision, not as independent genetic truth.

## 2. Complete natural delta

Parent relation records:
1,436

Child relation records:
1,436

No duplicate logical relation identities were observed.

Natural relation-state delta:
- CERT_CHANGED: 1
- UNCHANGED: 1,435
- ADDED_RELATION: 0
- REMOVED_RELATION: 0

The only changed relation is:

    printed target: ppp.01880.xml#pr323
    source file:    prc.00127.xml
    source target:  #l09
    certainty:      high -> low

Affected printed targets:
1

Affected source files:
1

This is a genuine highly selective editorial revision.

## 3. Current endpoint task

Ignoring certainty, the complete parent and child endpoint multisets are identical.

Parent printed targets:
761

Child printed targets:
761

Therefore:

    current endpoint answer before revision
    =
    current endpoint answer after revision

The revision changes epistemic status, not relation identity or endpoint presence.

## 4. Full relation-specific binding

R_FULL_BINDING starts from the parent relation identity -> certainty state and receives only the natural relation-level delta.

Result:
- changed target updated correctly: YES
- every unaffected relation retained exactly: YES
- collateral certainty/identity changes: 0
- complete child state exact: YES

Thus:

    1 changed relation + 1,435 stable relations

is reproduced without global rewriting.

This is the first executed project module demonstrating natural selective epistemic revision rather than merely resolving previously unassessed state.

## 5. Endpoint-only representation

R_ENDPOINT_ONLY retains relation identities/endpoints but no prior certainty.

The natural patch explicitly supplies the changed relation's old/new certainty, so it can learn the changed target's new status.

However, the remaining:
1,435
child relation-status items remain unresolved without source reopening or prior epistemic state.

Therefore:
- Q0 endpoint task exact: YES
- changed target learned from event: YES
- complete epistemic child state exact: NO

This distinguishes event-local update information from retained background epistemic state.

## 6. Locus-level aggregate status

R_LOCUS_STATUS retains for each printed target:
- full endpoint set;
- number of high links;
- number of low links;
- HIGH_ONLY / LOW_ONLY / MIXED state;
- no endpoint -> certainty binding.

Globally:
- printed targets with unique child binding: 757 / 761
- printed targets whose endpoint-specific binding remains unresolved: 4 / 761
- complete global child epistemic state exact: NO

However, the naturally affected locus is special.

Before revision, ppp.01880.xml#pr323 has exactly two endpoints:

    prc.00127.xml#l09
    tex.00088.xml#seg05

and its aggregate state is:

    2 high / 0 low / HIGH_ONLY

The identity-rich natural patch states that:

    prc.00127.xml#l09 : high -> low

Given the homogeneous pre-state plus the targeted patch, there is exactly one compatible child assignment:

    prc.00127.xml#l09   -> low
    tex.00088.xml#seg05 -> high

Therefore:

AGGREGATE_STATUS_NONDETERMINING = NO for this event.

AGGREGATE_STATUS_SUFFICIENT_FOR_THIS_EVENT = YES.

This result is retained as a substantive null against an unnecessarily strong universal binding claim.

## 7. Source reopening

An independently implemented parser reconstructs the exact child relation state from the pinned child source.

R_SOURCE_REOPEN:
- complete child state exact: YES
- child source bytes: 121,563

Thus ordinary lawful source reopening remains a strong baseline.

## 8. Wrong-binding control

The frozen protocol permits a matched wrong-binding patch only if at least two CERT_CHANGED relations exist and their new certainty assignments can be nontrivially permuted.

Only one relation changed.

Therefore:

WRONG_BINDING_CONTROL_NOT_IDENTIFIABLE

No artificial second change was introduced.

## 9. Cost record

Natural relation delta packet:
150 canonical JSON bytes

Full retained parent relation state:
149,388 canonical JSON bytes

Parent source:
121,564 bytes

Child source:
121,563 bytes

These are implementation encodings, not optimal information bounds.

## 10. Scientific disposition

NATURAL_EPISTEMIC_REVISION_OBSERVED = YES

SELECTIVE_REVISION_FULL_BINDING = YES

CURRENT_ENDPOINTS_UNCHANGED = YES

COLLATERAL_REVISION = 0

SOURCE_REOPEN_EXACT = YES

AGGREGATE_STATUS_NONDETERMINING_FOR_THIS_EVENT = NO

AGGREGATE_STATUS_SUFFICIENT_FOR_THIS_EVENT = YES

WRONG_BINDING_CONTROL = NOT IDENTIFIABLE

INDEPENDENT_TRANSFER = NO

## 11. Interpretation

The supported positive statement is:

> A real Whitman editorial revision selectively lowers the certainty of one relation while leaving 1,435 other relation states and all relation endpoints unchanged. Relation-specific retained state and lawful source reopening both reproduce the revised state without collateral change.

Equally important, the experiment falsifies a stronger claim:

> This natural revision does not require a complete endpoint-specific certainty binding in the retained pre-state. Because the affected locus is initially homogeneous and the revision event identifies the changed relation, a locus-level aggregate status plus the identity-rich patch is sufficient for the event-local update.

Therefore the relevant sufficiency object is not the stored representation alone.

For dynamic inquiry it is closer to:

    sufficiency = f(retained state, revision/event channel, lawful source access, task)

This event does not by itself establish a universal minimal carrier for selective revision.

## 12. Next obligation

Do not replace or suppress this event because it is small.

A separately frozen natural event may test a harder regime:
- multiple status changes;
- mixed pre-state;
- status and relation-topology changes together;
- or revision evidence that does not itself identify the affected relation.

Such a study is a new pressure test, not a rescue of D1.
