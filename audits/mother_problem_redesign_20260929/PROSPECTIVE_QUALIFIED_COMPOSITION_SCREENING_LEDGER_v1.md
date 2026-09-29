# Prospective qualified-composition screening ledger v1

Date: 2026-09-29
Status: DOCUMENTATION-ONLY SCREENING CLOSED AFTER FIRST C1-C8 PASS.

## 1. Governing protocol

    PROSPECTIVE_QUALIFIED_COMPOSITION_CANDIDATE_DISCOVERY_PROTOCOL_v1.md

No candidate record content was opened during this screening stage.

## 2. Candidate A — OpenReview

Project:
    OpenReview / openreview-py

Documentation inspected:
- openreview-py README;
- API model documentation / generic Note fields;
- generic venue stage code for Review, Rebuttal, Comment, MetaReview, Decision and custom reply targets.

Record content exposed:
    none

Documentation findings:
- Note objects have stable IDs;
- forum and replyto bind replies to prior Notes;
- signatures and cdate/tcdate/tmdate retain actor/time provenance;
- Invitations type workflow acts such as Official_Review, Rebuttal, Meta_Review and Decision;
- generic custom stages can explicitly reply to reviews, metareviews or rebuttals.

C1 independent ecology:
    PASS

C2 stable scholarly object/proposition target:
    BOUNDED_PASS
    stable Note targets exist, but the default unit is a workflow note rather than a claim-level
    proposition.

C3 source-native intervention relation:
    PASS
    workflow stage and reply relations are native.

C4 connected multi-step possibility:
    PASS
    generic review/rebuttal/comment chains are structurally supported.

C5 relation-target binding:
    PASS
    replyto/forum preserve target identity.

C6 provenance/history retention:
    PASS

C7 deterministic source scope:
    BOUNDED_PASS
    a venue/invitation/time-cutoff query can be frozen, but a project-level immutable snapshot was
    not yet identified.

C8 pre-record adapter feasibility:
    PASS

Screening disposition:

    SCREEN_HOLD_NOT_SELECTED

Reason:
    Structurally strong, but the most natural multi-step chains are scholarly-workflow replies.
    They risk collapsing the qualified-generator test into repeated RECORD_EVIDENCE rather than
    testing substantive state-dependent generator changes. A stronger candidate was found before
    any record opening.

## 3. Candidate B — generic nanopublication infrastructure

Documentation inspected:
- Nanopublication Guidelines;
- published nanopublication service architecture;
- documentation of Trusty URIs, assertion/provenance/publication-info graphs;
- npx:supersedes and npx:retracts update semantics;
- index nanopublications and latest-version traversal.

Record content exposed:
    none for candidate selection purposes.

C1 independent ecology:
    PASS

C2 stable scholarly object/proposition target:
    PASS
    Trusty URIs identify immutable assertion packages.

C3 source-native intervention relation:
    PASS
    npx:supersedes / npx:retracts.

C4 connected multi-step possibility:
    PASS
    superseding chains are structurally supported.

C5 relation-target binding:
    PASS

C6 provenance/history retention:
    PASS

C7 deterministic source scope:
    PASS IN PRINCIPLE
    index nanopublications can freeze versioned sets.

C8 pre-record adapter feasibility:
    PASS

Screening disposition:

    SCREEN_HOLD_INFRASTRUCTURE_ONLY

Reason:
    Infrastructure capability alone is not an empirical scholarly ecology.

## 4. Candidate C — Wen Fu / ancient Chinese commentary nanopublication reconstruction

Documentation inspected:
- published chapter "Combining ontology and nanopublication models to reconstruct digital
  commentaries on ancient Chinese books";
- published abstract/model description of ancient-book commentary knowledge representation.

Record content exposed:
    no machine-readable candidate record set opened.

Documentation findings:
- humanities/cultural-heritage setting;
- commentary knowledge represented with ontology + nanopublication;
- interpretation, citation, provenance and alignment units;
- traceability and responsible-entity provenance are design goals;
- multiple historical commentary works are represented.

C1:
    PASS

C2:
    PASS IN PRINCIPLE

C3:
    DOCUMENTATION_INSUFFICIENT
    the inspected documentation does not establish a registered update/supersession/reply target
    vocabulary for sequential scholarly acts.

C4:
    DOCUMENTATION_INSUFFICIENT
    cross-commentary relations exist, but a connected act1 -> act2 revision trajectory is not
    established prospectively.

C5:
    BOUNDED

C6:
    PASS

C7:
    FAIL AT SCREENING
    no closed public machine-readable distribution/index suitable for one-shot confirmation was
    identified.

C8:
    BOUNDED

Screening disposition:

    SCREEN_FAIL_DOCUMENTATION_INSUFFICIENT

## 5. Candidate D — Formalization Papers semantic publishing/reviewing field study

Project:
    "Nanopublication-based semantic publishing and reviewing: a field study with formalization papers"

Public data:
    LaraHack/formalization_papers_supplemental
    LaraHack/fpsi_analytics

Documentation inspected only:
- published field-study article;
- supplemental repository root tree + README;
- GitHub v1.0 release metadata;
- analytics repository root tree + README;
- generic SPARQL extraction query scripts;
- generic nanopublication update/retraction documentation.

Not opened:
- formalization_papers_supplemental/nanopubs/*
- fpsi_analytics/nanopubs/*
- fpsi_analytics/sparql-results/*
- nanopublication index contents
- any individual formalization/review/response/update/decision nanopublication
- any candidate episode identifier/content.

Frozen public scope anchor:

    supplemental release tag: v1.0
    tag commit: 2f68d8498aeeb724e3438deda13e74ae7fb076d8
    release publication date: 2022-03-25

Generic analytics documentation anchor:

    LaraHack/fpsi_analytics
    inspected commit: b6aef0049b3b2f02fc67030c080218617d71ab41

Published collection/index URI is known from documentation but has NOT been dereferenced:

    http://purl.org/np/RAkLJW7vIsnKKJDf1iswdgtFPQSo3lEG_z8DhHfD7dofE

Documentation-level structure:
- formalization/submission nanopublications;
- semantic ReviewComment nodes;
- author response nanopublications;
- updated formalizations;
- final decision nanopublications;
- superseding version links;
- provenance/creator information.

Generic project query scripts register:
- ReviewComment lf:refersTo submitted formalization;
- response lf:isResponseTo review nanopublication;
- response lf:refersTo updated formalization;
- update lf:isUpdateOf submitted formalization;
- decision assigns pso:withStatus to an updated formalization;
- npx:supersedes for new versions;
- npx:retracts for retractions.

C1 independent ecology:
    PASS
    independent from Yule-Cordier, AAD and VGW.

C2 stable scholarly object/proposition target:
    PASS
    immutable nanopublication URIs + semantic targets.

C3 source-native intervention relation:
    PASS
    Linkflows / PSO / NPX relations are native project semantics.

C4 connected multi-step possibility:
    PASS
    review -> response/update -> decision and update/supersession chains are explicitly described
    at documentation level.

C5 relation-target binding:
    PASS
    project queries explicitly bind review, response, update and decision targets.

C6 provenance/history retention:
    PASS
    nanopublication provenance/publication-info + creator + immutable URI/version links.

C7 deterministic source scope:
    PASS
    published v1.0 supplemental release + published nanopublication index.

C8 pre-record adapter feasibility:
    PASS
    relation graph and extraction logic are available in generic query scripts before record
    opening.

Screening disposition:

    SCREEN_PASS_C1_C8
    SELECTED_FOR_CANDIDATE_SPECIFIC_FREEZE

## 6. Stop rule

Broad candidate discovery stops here.

Next authorized work:
- freeze candidate exposure registry;
- freeze exact relation/target adapter;
- freeze denominator and trajectory grammar;
- build independent synthetic oracle/runtime;
- freeze PRE_DATA/DATA_OPEN boundary;
- only then open the published index / nanopub records once.

No additional broad candidate search is authorized before this candidate is either:
- prospectively executed, or
- invalidated by a pre-data feasibility failure.
