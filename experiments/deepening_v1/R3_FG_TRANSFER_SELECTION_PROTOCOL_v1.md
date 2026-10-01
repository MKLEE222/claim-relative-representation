# R3-F/G transfer selection protocol v1

Date frozen: 2026-09-27
Status: selection rule frozen before B02-B12 representation outcomes.

## Development material

Paper money, Kinsay, coal, Sarai, and B01 are development material because their relation mechanisms and/or representation behavior have already been inspected.

They may be used to debug carrier maps and recovery-profile instrumentation but not as untouched transfer evidence.

## Transfer population

Candidate entries come from R3 coding batches B02-B12 after Stage-0 frame validation and act segmentation.

Selection is based on historical relation family and source-verification feasibility, not on representation success/failure.

## Strata

Attempt to select the first entry in source order satisfying each stratum:
- FACTUAL_CORRECTION;
- IDENTIFICATION_UPDATE;
- ATTRIBUTION_UPDATE;
- QUALIFICATION with explicit source modality where available;
- ADDITIVE_EVIDENCE without explicit criticism/correction.

If a stratum has no eligible entry, report STRATUM_UNAVAILABLE rather than substituting a different effect-friendly case.

## Eligibility

An entry is eligible when:
- target locus is at least provisionally identifiable;
- proposition actor/mediator can be separated or explicitly marked unresolved;
- the act has at least one recorded lawful source basis;
- required source text is reproducibly available;
- no representation outcome for this act has been inspected.

Page-image verification is required before the selected case becomes manuscript-load-bearing, but selection itself may occur from the reproducible transcription.

## Frozen tests

For each selected act:
1. RELATION_KNOWN entry state;
2. HISTORICAL_START entry state;
3. enumerate native lawful basis family;
4. remove one basis at a time while preserving text where feasible;
5. test basis substitution before basis exhaustion;
6. record recoverability profile rather than only pass/fail;
7. if a separation is supported, test correct source-bound repair versus matched wrong repair;
8. preserve source-explicit uncertainty/contest status separately from analyst unresolved state.

## No selection by drama

Selection may not use:
- size of retrieval gain;
- whether a representation fails;
- whether the case produces a reversal;
- whether the case supports the manuscript's expected conclusion.

Null and fully resilient cases remain valid transfer outcomes.