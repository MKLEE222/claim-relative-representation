# Module R — Yule-Cordier exposed historical reassessment result v1

Date: 2026-09-29
Status: COMPLETED SOURCE-GROUNDED EXPOSED DEVELOPMENT EVIDENCE.

## 1. Scientific status

This study uses:
- source-verified historical episodes;
- a pre-Module-R contrast audit;
- controlled assertion-state execution.

It is not:
- automatic extraction from historical prose;
- independent historian adjudication;
- fresh confirmation.

FRUS remained unopened.

## 2. Frozen denominator

Source contrast audit:

    experiments/deepening_v1/r3_B02_B03_contrast_audit_v1.csv

Panel:

    experiments/module_r_scholarly_assertion_reassessment_v1/
    HISTORICAL_REASSESSMENT_PANEL_v1.json

All five rows of the pre-existing source contrast audit were retained.

Source grounding:

    5/5 exact row matches
    evidence_authority = OBJECT_VERIFIED for all five

## 3. First run and preserved partial

Initial historical workflow:

    36523435267

Result:

    EXPOSED_DEVELOPMENT_PARTIAL

The source grounding and historical transition classifications were already correct:

- YC1920E-0022 -> R-U3 EVIDENTIAL_STATUS_REVISION
- YC1920E-0023 -> ADMISSIBLE_NULL_EVENT
- YC1920E-0024 -> R-U2 ALTERNATIVE_FORMATION
- YC1920E-0030 -> ADMISSIBLE_NULL_EVENT
- YC1920E-0049 -> R-U4 RESOLUTION

Only YC1920E-0024 failed exact state/capability equality.

Cause:
oracle/runtime serialized the unordered Plane/Cypress alternative set in different deterministic
orders.

The frozen v1 implementation contract said only:

    canonical sorted set

without specifying the ordering function.

The original partial result remains part of the audit trail.

## 4. Pre-fresh canonicalization clarification

Frozen amendment:

    IMPLEMENTATION_CONTRACT_v1_ALTERNATIVE_CANONICALIZATION_AMENDMENT.md

The amendment defines one serialization-only order:
canonical JSON of projected assertion fields.

It does not change:
- assertion value/status;
- event applicability;
- transition class;
- substantive/null classification;
- historical mapping;
- comparator budgets.

A first implementation attempt missed the runtime json import and was blocked by the synthetic
gate before historical execution.

After the import bug was fixed, the full synthetic gate was rerun successfully.

## 5. Final development workflow

Successful workflow:

    36523589259

Synthetic R-F1-R-F14:

    PASS

Historical exposed study:

    EXPOSED_DEVELOPMENT_PASS

Historical result JSON SHA-256:

    90f16a24ce8ae6897a082a0b9f33add33f47bc1aae920948dc94fe05e84cf5b2

## 6. Historical denominator

Total:

    5

Substantive reassessments:

    3

Admissible null events:

    2

Transition classes:

    R-U3 EVIDENTIAL_STATUS_REVISION = 1
    R-U2 ALTERNATIVE_FORMATION      = 1
    R-U4 RESOLUTION                 = 1

## 7. Source-grounded cases

### YC1920E-0022 — Sykes route position

Frozen historical contrast:

    CONTRADICTS_PRIOR
    FACTUAL_CORRECTION|CRITICISM

Observed Module-R class:

    R-U3 EVIDENTIAL_STATUS_REVISION

Interpretation:
the source licenses that Sykes's earlier adoption/support has since been altered; the study does
not invent a specific new route position absent from the frozen contrast.

### YC1920E-0023 — Tutia

Frozen historical relation:

    ADDITIVE_EVIDENCE|CORROBORATION

Observed:

    ADMISSIBLE_NULL_EVENT

New comparative evidence/provenance does not automatically become a task-level identification
replacement.

### YC1920E-0024 — Arbre Sec

Earlier:

    Chinar / Oriental Plane

Later source-grounded proposal:

    Cypress of Zoroaster
    responsible actor = Houtum-Schindler

Observed:

    R-U2 ALTERNATIVE_FORMATION

The earlier identification remains live.
Cordier is not encoded as adopting the Cypress proposal.

### YC1920E-0030 — Pashai

Frozen correction audit had already withdrawn ATTRIBUTION_UPDATE.

Observed:

    ADMISSIBLE_NULL_EVENT

Stein's later statement corroborates/sharpens the registered non-eyewitness/hearsay attribution
without creating a new task-level attribution state.

### YC1920E-0049 — Great Desert

Earlier:

    no explicit local-on-the-spot source-derivation assignment

Later:

    explicit local-folklore source assignment

Observed:

    R-U4 RESOLUTION

## 8. Development finding

The same Module-R representation distinguishes, on a real source-verified DH panel:

- revision of a scholar's prior position;
- formation of a competing identification;
- acquisition/resolution of a previously unstated source assignment;
- corroborative/additive evidence that should remain non-substantive.

Thus the development contribution is not merely:

    different values can be stored.

It is:

    scholarly interventions that look superficially similar in a later editorial layer can have
    different diachronic status, and the representation must retain enough target, responsibility,
    result-state, provenance and history structure to avoid collapsing them.

## 9. Near-neighbor significance

The result is consistent with the experimental distinction motivated by:
- TEI change targeting;
- E13-style assertion assignment activities;
- CRMinf-style evidence / assessment / adopted belief separation.

Those neighboring models informed the task design but did not determine the historical labels.

## 10. Claim ceiling

Licensed at development level:

> A source-grounded historical contrast panel containing position revision, competing
> identification, attribution acquisition and corroborative nulls can be represented under one
> proposition-targeted reassessment contract without promoting every later intervention to a
> substantive change.

Not licensed:
- automatic historical interpretation;
- independent historian agreement;
- fresh cross-project generalization;
- prevalence;
- universal representational necessity.

The next Module-R burden remains fresh confirmation under a separately frozen natural ecology.

FRUS remains reserved and unopened.
