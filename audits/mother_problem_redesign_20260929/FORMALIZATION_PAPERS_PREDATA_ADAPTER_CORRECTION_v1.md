# Formalization Papers pre-data adapter correction v1

Date: 2026-09-29
Status: PRE_DATA_CORRECTION / RECORD-LEVEL CONTENT STILL UNOPENED.

## 1. Trigger

The first dedicated pre-fresh synthetic workflow:

    formalization-papers-prefresh-synthetic-v1
    run 36592663217

reached the synthetic RDF parser comparison and failed before any provider/index/record access.

No candidate nanopublication record, populated result file, or published nanopublication index was
opened.

Freshness status therefore remains:

    RECORD_LEVEL_UNOPENED

## 2. Finding A — special-issue URI typo

The frozen constant had been constructed as:

    https://w3id.org/linkflows/reviews/formalization-papers/DataScienceSpecialIssue

because it was derived by concatenating the Linkflows review namespace.

However the project-generic query scripts frozen in the pre-fresh registry use exactly:

    https://w3id.org/linkflows/formalization-papers/DataScienceSpecialIssue

This is visible in generic, non-record scripts including:
- get-submissions.rq
- get-sp-reviews.rq
- get-updated.rq
- get-sp-response-to-review.rq
- get-response-to-updated.rq
- get-decision-to-updated.rq

Therefore the existing constant is a documentation-inconsistent adapter typo.

Authorized correction:

    SPECIAL_ISSUE =
      "https://w3id.org/linkflows/formalization-papers/DataScienceSpecialIssue"

No record-derived information is used.

## 3. Finding B — equivalent UTC literal serialization

On the same synthetic xsd:dateTime literal:

    2021-01-01T00:00:00Z

RDFLib returns the semantically equivalent lexical form:

    2021-01-01T00:00:00+00:00

while pyoxigraph retains:

    2021-01-01T00:00:00Z

The parser scientific surfaces otherwise matched in the failed fixture.

Authorized correction:

Each independent parser canonicalizes UTC dateTime strings only for comparison/storage by mapping
a terminal:

    +00:00

to:

    Z

No timezone conversion, timestamp inference, ordering rule, or missing-date repair is added.

## 4. Scientific invariants unchanged

This amendment does not alter:
- candidate population;
- root/trajectory denominator;
- relation predicates;
- target binding;
- trajectory classes T0-T9;
- qualification generators;
- history-ablation criterion;
- counterfactuals;
- PASS/NULL/PARTIAL/INVALID rules.

It changes only:
- one documentation-proven URI typo;
- one semantics-preserving UTC lexical canonicalization.

## 5. Required rerun

Before any DATA_OPEN work proceeds:

1. install RDFLib + pyoxigraph;
2. compile both adapters;
3. rerun all synthetic fixtures;
4. require exact oracle/runtime scientific surface;
5. require complete T0 generator chain;
6. require all registered rejection/history/retraction controls;
7. require provider_record_content_opened = false.

If the rerun exposes another mismatch, stop again at PRE_DATA and audit it independently.
