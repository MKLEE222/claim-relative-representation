# Module R — Van Gogh Worldwide fresh attribution-status reassessment protocol v1

Date frozen: 2026-09-29
Status: FROZEN BEFORE OPENING ANY OF THE FIVE PROVIDER N-TRIPLES DISTRIBUTIONS.

## 1. Purpose

Module R has:
- synthetic hardening;
- source-grounded exposed historical development.

The next burden is a prospective, distribution-fresh, independent digital-humanities ecology.

Candidate:

    Van Gogh Worldwide (VGW)

The task is not to identify the true artist of any work.

The task is:

    can a representation preserve a documented scholarly attribution-status transition
    from the De la Faille 1970 catalogue-era Van Gogh attribution state to the current
    provider attribution state, while retaining object identity, event applicability,
    source/responsibility provenance, selectivity and delayed transition history?

## 2. Project-level semantic basis frozen before data opening

Van Gogh Worldwide publicly states:
- its starting scope is the works published in J.-B. de la Faille, The Works of Vincent van Gogh:
  His Paintings and Drawings (1970);
- De la Faille's explicitly "Rejected Works" are not included in VGW;
- some works in De la Faille 1970 are no longer recognized as authentic and are categorized as
  "Previously attributed to Vincent van Gogh";
- if that changed status is not fully recognized, VGW categorizes the work as "questionable";
- basic De la Faille 1970 catalogue information is provided for works in scope;
- provider data are supplied and managed by the participating owners/knowledge institutions.

VGW's frozen Linked Art documentation at:

    vangoghworldwide/linkedart
    9323e453939476640889da932058c73b3f29a286

defines:
- artwork = crm:E22_Human-Made_Object;
- object production = crm:E12_Production;
- current creator through crm:P14_carried_out_by;
- previous/changing creator attribution through crm:E13_Attribute_Assignment;
- the VGW classification:

    https://vangoghworldwide.org/data/concept/previous_attribution

  labelled "Previously attributed to Vincent van Gogh";

- the De la Faille identifier classification:

    https://vangoghworldwide.org/data/concept/f_number

- Van Gogh creator identifiers including:

    http://vocab.getty.edu/ulan/500115588
    https://data.rkd.nl/artists/32439

Linked Art independently documents the general convention:

    carried_out_by = current opinion;
    previous attributions remain represented through attribution/assertion machinery.

## 3. Frozen source population

Five N-Triples distributions were registered before opening:

    de_la_faille_1970
    works_after_1970
    van_gogh_museum
    krollermuller_museum
    rkd_collections

Frozen metadata anchors are in:

    VGW_DISTRIBUTION_METADATA_ANCHORS_v1.json

No distribution content URL had been followed when this protocol was frozen.

### Functional roles

Historical baseline:

    de_la_faille_1970

Explicit post-1970 no-baseline collection:

    works_after_1970

Current provider collections:

    van_gogh_museum
    krollermuller_museum
    rkd_collections

All five distributions are downloaded and accounted for in the authoritative run.

The reassessment denominator is not selected by observed outcome.

## 4. Pre-open source-integrity gate

Before any N-Triples distribution content is downloaded, the runner must re-fetch only the
registered dataset metadata surface and verify, for each slug:

- catalog metadata body hash;
- ETag where supplied;
- Last-Modified where supplied;
- encoding format;
- content URL;
- content size metadata.

If any frozen metadata anchor has changed:

    INVALID_SOURCE_ANCHOR

and the runner must stop before distribution opening.

Once an anchor gate passes and distribution bytes are acquired:
- record full distribution SHA-256;
- bind every extracted object/assertion/event to that distribution SHA-256;
- never substitute a later download in the same confirmatory run.

## 5. Object identity

The only cross-dataset join key is the project-native De la Faille F-number.

A candidate object key exists only when:
- a HumanMadeObject has exactly one Identifier;
- that Identifier is classified exactly as:

    https://vangoghworldwide.org/data/concept/f_number

- the Identifier has exactly one symbolic content literal.

The literal is used exactly as supplied.

No:
- fuzzy title matching;
- owner/title matching;
- punctuation rescue;
- case repair;
- numeric normalization;
- accession-number substitution

is allowed after opening.

### Baseline cardinality

For an F-number:
- exactly one baseline object in de_la_faille_1970 is required for reassessment eligibility;
- zero => NO_1970_BASELINE;
- >1 => AMBIGUOUS_1970_BASELINE.

### Current-provider cardinality

Across:

    van_gogh_museum
    krollermuller_museum
    rkd_collections

for an F-number:
- exactly one current provider object is required;
- zero => NO_CURRENT_PROVIDER_OBJECT;
- >1 => MULTIPLE_CURRENT_PROVIDER_OBJECTS.

No first-provider fallback is allowed.

## 6. works_after_1970 discipline

Every object whose only project role is:

    works_after_1970

is counted in full population accounting but is not eligible for the registered 1970->current
reassessment task.

Disposition:

    NO_1970_BASELINE_BY_DATASET_ROLE

This is not a failure and is not removed from reporting.

## 7. Registered proposition

For each eligible F-number:

    target_property = van-gogh-creator-attribution-status

The literal attribution value is fixed:

    VINCENT_VAN_GOGH

The task-relevant status vocabulary is frozen to:

    ATTRIBUTED
    PREVIOUSLY_ATTRIBUTED

No additional natural status is admitted after opening.

In particular:

    QUESTIONABLE

is known at project-policy level but its machine representation was not established from the
allowed pre-open Linked Art documentation.

Therefore any record whose attribution status cannot be uniquely classified under the two
registered machine patterns is:

    UNREGISTERED_CURRENT_ATTRIBUTION_STATUS

and is excluded from the substantive/null reassessment denominator while remaining fully counted.

## 8. S0 — catalogue-era attribution state

For each F-number with exactly one object in de_la_faille_1970:

    value  = VINCENT_VAN_GOGH
    status = ATTRIBUTED

This is a project-relative catalogue-era state, not an assertion of universal art-historical
consensus.

The interpretation is licensed only because the project documentation states that:
- VGW's 1970 starting scope is the works published as Van Gogh's works in De la Faille 1970;
- De la Faille's own Rejected Works are not included;
- current non-authentic cases from that 1970 set are explicitly represented as previously
  attributed/questionable.

## 9. S1-A — current direct Van Gogh attribution

A current provider object is classified:

    CURRENT_DIRECT_VAN_GOGH

only if:
- exactly one selected Production is linked from the object under the project Linked Art
  production pattern;
- that Production directly has crm:P14_carried_out_by one of the two frozen Van Gogh identifiers;
- no qualifying previous_attribution AttributeAssignment for Van Gogh is attached to the selected
  Production.

Task state:

    value  = VINCENT_VAN_GOGH
    status = ATTRIBUTED

Relative to S0:

    Psi(S0) == Psi(S1)

Disposition:

    ADMISSIBLE_NULL_EVENT

This natural null is mandatory evidence against promoting every later provider record into a
scholarly reassessment.

## 10. S1-B — previous attribution

A current provider object is classified:

    CURRENT_PREVIOUS_ATTRIBUTION

only if all are true:
- exactly one selected Production belongs to the object;
- exactly one crm:E13_Attribute_Assignment is connected through the frozen assigned_by pattern;
- the assignment is classified exactly as:

    https://vangoghworldwide.org/data/concept/previous_attribution

- its assigned Production identifies Van Gogh under crm:P14_carried_out_by using one of the two
  frozen Van Gogh identifiers.

Task state:

    value  = VINCENT_VAN_GOGH
    status = PREVIOUSLY_ATTRIBUTED

Relative to S0:

    ATTRIBUTED
    ->
    PREVIOUSLY_ATTRIBUTED

Expected Module-R class:

    R-U3_EVIDENTIAL_STATUS_REVISION

No claim about the replacement/true artist is made.

## 11. Ambiguity and rejection rules

The following are never repaired after opening:

- multiple F-number identifiers;
- duplicate baseline objects;
- multiple current provider objects;
- multiple incompatible Productions;
- direct current Van Gogh attribution plus a qualifying previous-attribution assignment;
- multiple qualifying previous-attribution assignments;
- previous-attribution assignment not uniquely bound to Van Gogh;
- unknown/questionable attribution encoding;
- missing target/status binding;
- source-anchor mismatch.

These receive explicit ineligible/unresolved dispositions.

## 12. Natural reassessment event

For CURRENT_PREVIOUS_ATTRIBUTION:

    event_id

is derived from the exact AttributeAssignment node.

    evidence_id

is the exact current provider assignment/source node plus provider distribution identity.

    evidence_locator

contains the provider slug and assignment node identifier.

    responsible_agent

is the exact crm:P14_carried_out_by actor of the AttributeAssignment when uniquely present;
otherwise it is retained as missing and must not be invented.

The assignment node is the documentary source that records the current scholarly reassessment.

This study does not claim that the machine record preserves the full underlying art-historical
argument that originally caused the reassessment.

## 13. Natural null event

For CURRENT_DIRECT_VAN_GOGH:

- the current provider production assertion is treated as the later source event;
- operation is a same-value/same-status reassessment;
- provenance changes from catalogue baseline to current provider source;
- Psi does not change.

Expected:

    ADMISSIBLE_NULL_EVENT

A new provider/source record alone is not substantive reassessment.

## 14. Module-R capabilities

For each substantive R-U3 episode, the retained interface is evaluated on:

    R1 PRE_STATE_EXACT
    R2 TARGET_DETERMINACY
    R3 EVENT_APPLICABILITY
    R4 POST_EVENT_RESULT
    R5 SELECTIVE_UPDATE
    R6 PROVENANCE
    R7 TRANSITION_ATTRIBUTION
    R8 DELAYED_HISTORY

No scalar score.

## 15. Strong comparators

Reuse unchanged:

    B_CURRENT_REOPEN_R
    B_ORDERED_SNAPSHOTS_R
    B_CHANGE_LOG_NO_JUSTIFICATION_R

The comparator budgets are not altered for VGW.

## 16. Fresh synthetic gate

Before distribution opening, a VGW-shaped synthetic N-Triples gate must prove:

1. exact F-number join works;
2. current-direct Van Gogh -> ADMISSIBLE_NULL_EVENT;
3. previous_attribution E13 pattern -> R-U3 status revision;
4. works_after_1970-only object -> no baseline;
5. duplicate current provider object -> ambiguity/ineligible;
6. multiple F-number -> ambiguity/ineligible;
7. direct-current plus previous-attribution conflict -> ambiguity/ineligible;
8. unregistered attribution encoding -> ineligible;
9. wrong object/source version/applicability interventions reject;
10. provenance removal, collateral mutation and history drop remain separable;
11. B_CURRENT_REOPEN_R / B_ORDERED_SNAPSHOTS_R / B_CHANGE_LOG_NO_JUSTIFICATION_R retain their
    frozen positive and negative capabilities.

No provider N-Triples bytes may be used in that synthetic fixture.

## 17. Independent extraction requirement

The fresh implementation must not use one shared pattern detector as both oracle and runtime.

At minimum:
- one implementation uses an RDF graph parser;
- the other independently reconstructs the relevant N-Triples relation graph from lexical triples.

They may share only frozen URI constants and fixture bytes.

Any disagreement on a natural object is:

    ORACLE_RUNTIME_UNRESOLVED

and cannot be outcome-specifically repaired.

## 18. Documentary audit

For every substantive candidate, an independent raw-triple audit verifies:

- F-number baseline/current binding;
- baseline dataset identity;
- current provider identity;
- Production target;
- E13 AttributeAssignment identity;
- previous_attribution classification;
- assigned Van Gogh production relation;
- assignment responsibility where present;
- source distribution SHA-256.

The audit does not redefine the transition.

## 19. Outcome categories

### INVALID

Use if:
- source anchors fail before opening;
- population accounting is incomplete;
- oracle/runtime disagreement remains unresolved;
- the run violates this frozen protocol.

### NULL_APPLICABILITY

Use if:
- the population is valid;
- zero objects satisfy the strict baseline/current/status contract.

### NULL_REASSESSMENT

Use if:
- admissible matched objects exist;
- all are current-direct nulls;
- zero substantive R-U3 reassessments occur.

### BOUNDED_PARTIAL

Use if:
- at least one substantive R-U3 reassessment occurs;
- but a bounded capability/source-audit issue remains.

### PASS

Use only if:
- source anchors match;
- all five distributions are completely accounted for;
- at least one R-U3 episode exists;
- every substantive episode passes R1-R8;
- registered natural nulls remain null;
- strong comparator behavior matches the frozen contract;
- documentary audit verifies every substantive episode.

## 20. Freshness boundary

The authoritative opening occurs only after this protocol and the synthetic gate are committed and
green.

At the first distribution-content fetch:
- all five distributions become exposed forever for this project;
- any later rerun is audit/reproduction only.

Pre-data infrastructure failure is recoverable only if:
- zero distribution content bytes were acquired;
- zero episode/object outcome was observed;
- scientific engine hashes remain unchanged.

## 21. Claim ceiling

Even PASS licenses only:

> In the Van Gogh Worldwide linked-open-data ecology, a prospectively frozen representation can
> distinguish unchanged current Van Gogh attributions from source-documented transitions to
> previous-attribution status while preserving the registered target, provenance, transition and
> delayed-history capabilities.

It does not establish:
- the true authorship of any artwork;
- prevalence outside the closed VGW population;
- that every scholarly reassessment has this encoding;
- universal representational necessity;
- completeness of the underlying art-historical justification.

## 22. References used before opening

Project-level only:
- Van Gogh Worldwide About / FAQ;
- vangoghworldwide/linkedart at 9323e453939476640889da932058c73b3f29a286;
- Linked Art production / changing-attribution documentation;
- frozen Dataset Registry metadata anchors.

No provider N-Triples distribution was opened in producing this protocol.
