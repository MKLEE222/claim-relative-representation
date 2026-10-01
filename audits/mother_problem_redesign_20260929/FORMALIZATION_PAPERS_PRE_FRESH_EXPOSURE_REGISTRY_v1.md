# Formalization Papers pre-fresh exposure registry v1

Date frozen: 2026-09-29
Status: RECORD-LEVEL OUTCOME UNOPENED / CANDIDATE-SCOPE PROSPECTIVE.

## 1. Candidate

Project:

    Nanopublication-Based Semantic Publishing and Reviewing:
    A Field Study with Formalization Papers

Public repositories:

    LaraHack/formalization_papers_supplemental
    LaraHack/fpsi_analytics

Selected under:

    PROSPECTIVE_QUALIFIED_COMPOSITION_CANDIDATE_DISCOVERY_PROTOCOL_v1.md

Screening result:

    SCREEN_PASS_C1_C8

## 2. Inspected before this registry

Allowed documentation-level material inspected:

### Published/project-level documentation
- published field-study article and abstract-level workflow description;
- generic nanopublication architecture/documentation;
- generic nanopublication update/retraction semantics.

### formalization_papers_supplemental
- repository root directory tree;
- README.md;
- GitHub release metadata for v1.0;
- tag/branch comparison metadata.

Frozen release anchor:

    tag = v1.0
    commit = 2f68d8498aeeb724e3438deda13e74ae7fb076d8
    release published = 2022-03-25

### fpsi_analytics
- repository root directory tree;
- README.md;
- generic SPARQL extraction query scripts:
  - get-sp-response-to-review.rq
  - get-response-to-updated.rq
  - get-decision-to-updated.rq
  - get-updated.rq
  - get-sp-reviews.rq

Documentation snapshot inspected:

    commit = b6aef0049b3b2f02fc67030c080218617d71ab41

These generic scripts establish the project-native relation surface without exposing concrete
record outcomes.

## 3. Known but NOT opened

The published nanopublication index URI is known from project documentation:

    http://purl.org/np/RAkLJW7vIsnKKJDf1iswdgtFPQSo3lEG_z8DhHfD7dofE

It has NOT been dereferenced.

The following directories/content have NOT been opened:

    formalization_papers_supplemental/nanopubs/*
    fpsi_analytics/nanopubs/*
    fpsi_analytics/sparql-results/*

Also not opened:
- any individual submission/formalization nanopublication;
- any review nanopublication;
- any author-response nanopublication;
- any updated-formalization nanopublication;
- any decision nanopublication;
- any retraction nanopublication;
- any concrete nanopublication Trusty URI from the population;
- any candidate trajectory ID;
- any graph visualization whose node labels/outcomes reveal episode content.

## 4. No record-level discovery

Before this registry:

- no repository-wide code search was used against candidate record files;
- no search query by record/object/nanopublication ID was made;
- no SPARQL endpoint query returning project records was made;
- no raw nanopublication distribution/index was downloaded;
- no candidate positive/negative trajectory was inspected;
- no favorable case was selected.

The expected existence of approximately 15 formalization submissions comes from the published
field-study description and is not a record-derived denominator.

## 5. Documentation-level native relations already visible

The following are allowed pre-record because they are defined in generic project query scripts:

### Review target

    ReviewComment
    lf:refersTo
    submitted formalization

### Response target

    response
    lf:isResponseTo
    review nanopublication

and:

    response
    lf:refersTo
    updated formalization

### Update target

    updated formalization nanopublication
    lf:isUpdateOf
    submitted formalization

### Decision target/status

    updated formalization
    pso:withStatus
    decision status

where the decision assertion is carried by a decision nanopublication.

### Version/retraction relations

    npx:supersedes
    npx:retracts

These are project-native relation predicates, not post-outcome labels.

## 6. Freshness boundary

Strict candidate freshness is defined at record-level content.

Current status:

    RECORD_LEVEL_UNOPENED

Freshness is consumed at the first operation that:
- opens any candidate nanopublication record;
- dereferences the published nanopublication index;
- opens a populated SPARQL result file;
- executes a query returning candidate record assertions;
- opens a repository file under the candidate nanopubs directories.

Before that event, failures limited to:
- dependency installation;
- compilation;
- synthetic fixtures;
- schema/ontology/generic-query inspection;
- source metadata/commit verification

are:

    PRE_DATA_ABORT

and are recoverable without consuming candidate record freshness.

## 7. Stop rules

Before the candidate-specific scientific contract, adapter, denominator, independent
implementations and synthetic gate are frozen:

DO NOT:
- list file names inside nanopubs directories if those names encode candidate IDs;
- fetch nanopub files;
- fetch populated SPARQL results;
- dereference the published nanopub index;
- use graph visualizations to identify positive trajectories;
- use repository search over candidate data directories.

Any accidental record-level exposure must be logged immediately and the affected freshness claim
downgraded.

## 8. Claim ceiling

This registry supports only:

> The Formalization Papers candidate remained record-level outcome-unopened through the
> documentation-screening and pre-fresh registry stage.

It does not establish:
- existence of any complete qualified-composition trajectory;
- prevalence;
- any generator result;
- any prospective confirmation outcome.
