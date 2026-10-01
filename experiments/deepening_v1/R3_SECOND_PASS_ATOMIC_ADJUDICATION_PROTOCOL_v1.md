# R3 Independent Second-Pass Atomic Adjudication Protocol v1

Date frozen: 2026-09-27
Status: SEALED BEFORE REVIEW RETURN

## Purpose

Freeze the atomic comparison dimensions used after a qualifying independent reviewer returns the blinded five-case historical review.

This protocol does not expose or rewrite the registered answers.

## Frozen sources

Inquiry-question blob:
8f0f2bd2ec32e782bff726d1cbdd466d73a4bf55

Registered proposition-panel blob:
f1ffa2aefde17f731fc9d0a19781aed81c94622c

Independent-review seal:
R3_SECOND_PASS_REVIEW_SEAL_v1.md

Atomic component registry:
R3_SECOND_PASS_ATOMIC_COMPONENTS_v1.csv

The component registry points to pre-existing proposition rows but intentionally does not duplicate registered answer text.

## Comparison statuses

Each atomic component must receive exactly one status:

- EXACT_AGREEMENT
- SUBSTANTIVE_AGREEMENT_WITH_WORDING_DIFFERENCE
- REVIEWER_ADDED_DISTINCTION
- SUBSTANTIVE_DISAGREEMENT
- UNRESOLVED

No other status may be invented after the review is returned.

## Comparison procedure

1. Verify reviewer independence declaration.
2. Freeze the returned reviewer file or response with a SHA-256 before comparison.
3. Copy the reviewer’s relevant wording verbatim into an adjudication ledger.
4. Resolve the component’s registered value only from the sealed proposition-panel blob and the row IDs declared in R3_SECOND_PASS_ATOMIC_COMPONENTS_v1.csv.
5. Assign one allowed comparison status.
6. Give a source-based adjudication note.
7. If status is REVIEWER_ADDED_DISTINCTION, SUBSTANTIVE_DISAGREEMENT, or UNRESOLVED, inspect every propagation target registered for that component before manuscript claim freeze.
8. Never change the question, atomic component list, or registered answer source in response to a disagreement.

## Agreement reporting

Primary result:
the full atomic comparison table.

Permitted aggregate:
number/proportion of components in:
- EXACT_AGREEMENT;
- EXACT + SUBSTANTIVE_AGREEMENT_WITH_WORDING_DIFFERENCE.

A single kappa is not the primary result because the components are heterogeneous and not repeated nominal ratings of one common variable.

No disagreement may be hidden by an aggregate.

## Reviewer-added distinctions

A reviewer-added distinction is not automatically an error in either direction.

It must be classified as one of:

- compatible refinement — existing registered answer remains valid but incomplete;
- scope extension — distinction depends on evidence outside the sealed source scope;
- material revision — changes a load-bearing historical reading;
- unresolved interpretive alternative.

Only compatible refinement may leave all existing mechanism experiments untouched without further audit.

## Propagation rule

If a component is materially revised or unresolved:

- historical prose using that component is reopened;
- the controlled separation/repair is rerun or reinterpreted if its required output depends on that component;
- ecological workflow outcomes remain numerically preserved but their historical interpretation is updated if needed;
- claim ledger status is changed before manuscript freeze.

## Gate pass rule

Gate II may be marked HISTORICAL_REVIEW_CLOSED only when:

- reviewer independence qualifies;
- all registered atomic components have one allowed comparison status;
- every disagreement/unresolved component has an adjudication note;
- all required propagation actions are completed or explicitly downgrade the claim;
- the original review return, atomic ledger, and hashes are preserved.

## Stop rule

The adjudication stage may resolve historical disagreement.

It may not be used to redesign computational experiments merely to recover a preferred result.
