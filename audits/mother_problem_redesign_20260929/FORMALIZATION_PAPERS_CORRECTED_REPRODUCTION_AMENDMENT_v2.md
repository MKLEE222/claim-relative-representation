# Formalization Papers corrected reproduction amendment v2 — creator relation cardinality

Date: 2026-09-30
Status: POST-FRESH IMPLEMENTATION-CARDINALITY CORRECTION.

## 1. Trigger

Corrected reproduction attempt 1:

    run 36658658912

stopped before population because real-source parser exactness was:

    9/10

Residual mismatch:

    nanopubs/sp-responses.trig
    component = creators

## 2. Raw-source diagnosis

Source examples explicitly encode:

    dct:creator creator_A, creator_B

for a single nanopublication.

Independent full-archive pubinfo audit on the exact first-opening bytes found:

    nanopublications = 404

    creator cardinality:
        1 creator = 379
        2 creators = 25

    created timestamp cardinality:
        1 timestamp = 404

Thus creator is demonstrably multi-valued in the frozen source ecology.

## 3. Defect

Both registered extractors used a scalar map:

    creators[np] = creator

When two creator triples existed, set iteration order selected whichever value happened to be
visited last.

The two RDF engines therefore sometimes retained different valid creator URIs for the same
nanopublication.

This is an extractor cardinality defect.

It is not a disagreement in:
- RDF parsing;
- review/update/response/decision relations;
- target identity;
- supersession/retraction;
- chronology;
- generator qualification.

## 4. Frozen correction

Represent the registered creator surface as the RDF relation itself:

    creators = set of (nanopublication_uri, creator_uri) pairs

For every dct:creator triple in the nanopublication's publication-info graph:

    add (np, creator)

No creator is selected as primary.
No creator ordering is inferred.
No duplicate relation is counted twice.

Output is a lexicographically sorted list of unique pairs for deterministic comparison.

## 5. Scope

The correction changes only:
- fp_oracle creator extraction;
- fp_runtime creator extraction.

It does NOT change:
- created timestamp extraction;
- population classification;
- T0-T9;
- eligible chains;
- event qualification;
- generator semantics;
- chronology;
- P1-P7;
- documentary audit success criteria.

Creator identity is retained for provenance reporting but is not an input to the registered
population or qualified-composition decision rules.

## 6. Required regression

Before corrected reproduction v2:

1. a synthetic nanopublication with two dct:creator triples returns both creator pairs in both
   extractors;
2. single-creator nanopublications remain unchanged;
3. no artificial primary creator is introduced;
4. original synthetic parser/qualification gate PASS;
5. population synthetic gate PASS;
6. authoritative-stack synthetic gate PASS;
7. exact real-source diagnostic returns 10/10 exact files and zero mismatching components.

Only after all seven gates pass may corrected population analysis run.

## 7. Evidentiary status

The authoritative fresh run remains:

    INVALID

Corrected attempt 1 remains:

    BLOCKED_BEFORE_POPULATION

Any successful v2 run remains:

    POST_FRESH_CORRECTED_REPRODUCTION

and cannot restore freshness.
