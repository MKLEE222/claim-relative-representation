# R3 Independent Second-Pass Review Seal v1

Date: 2026-09-27
Status: SEALED BEFORE INDEPENDENT REVIEW

## Frozen question source

`experiments/deepening_v1/R3_SCHOLARLY_INQUIRY_PANEL_v1.csv`

Git blob SHA exposed by the repository at sealing time:

`8f0f2bd2ec32e782bff726d1cbdd466d73a4bf55`

The blinded packet copies only:
- inquiry ID;
- question;
- source scope/loci.

It omits:
- required_output;
- required_bindings;
- controlled experimental outcomes.

## Frozen registered-answer source

`data/r3_verified_proposition_panel_v1.csv`

Git blob SHA at sealing time:

`f1ffa2aefde17f731fc9d0a19781aed81c94622c`

This pre-existing blob is the answer-state seal.

It is **not** included in the blinded reviewer packet.

## Historical source-audit basis

`audits/r3_source_round_20260927/RESULTS.md`

Git blob SHA at sealing time:

`4d2b28d989dbb5974bae3696dd1532406914955a`

The source audit records printed loci and registered PDF indices but explicitly states that its AI-assisted historical inspection is not independent human adjudication.

## Comparison rule after review return

Do not alter the inquiry questions or registered proposition panel before comparison.

For each case compare predeclared atomic components:

- target proposition identity;
- responsible actor/source;
- stance/relation direction where applicable;
- evidence-to-proposition assignment;
- modality/uncertainty;
- simple textual correction for Urumtsi.

Report each component as:
- EXACT_AGREEMENT;
- SUBSTANTIVE_AGREEMENT_WITH_WORDING_DIFFERENCE;
- REVIEWER_ADDED_DISTINCTION;
- SUBSTANTIVE_DISAGREEMENT;
- UNRESOLVED.

Do not compress the five heterogeneous tasks into a single kappa as the primary result.

If an aggregate is reported, it may only be the proportion of these predeclared atomic components in agreement after the atomic comparison table has been shown.

## Gate consequence

No review result exists at sealing time.

The repository must continue to state:

`INDEPENDENT_SECOND_PASS_PENDING`

until a qualifying reviewer response is returned and adjudicated.
