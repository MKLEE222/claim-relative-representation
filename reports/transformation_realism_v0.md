# Transformation realism audit v0

Date: 2026-09-23

## Question

Can the planned representation interventions be justified by simply treating Project Gutenberg plain text as a naturally flattened version of the Yule-Cordier object?

## Result

**No. The naive plaintext-flattening story is rejected.**

The current Project Gutenberg UTF-8 object retains substantial editorial structure:

- its front matter explicitly identifies the object as the complete Yule-Cordier edition and distinguishes the 1903 third edition from the 1920 notes/addenda;
- plain text retains chapter and NOTE headings;
- H. C. signatures remain visible in the text;
- addendum references preserve links back to earlier printed pages;
- the supplied layer-count diagnostic likewise records many note headings, H.C. signatures, and bracket blocks in the Gutenberg files.

Therefore a plain-text export cannot be treated as an attribution-free or chronology-free representation.

## Consequence for design

The intervention family must be reframed as **controlled constructed representations derived from the same source-validated object**, not as a claim that Gutenberg itself has already destroyed all relevant provenance.

Each operator must satisfy two conditions:

1. **one-coordinate invariance**: only its declared representation coordinate changes;
2. **real-use analogue**: the operator must correspond to a documented extraction, chunking, metadata-removal, normalization, or corpus-building practice before Gate T is marked PASS.

## Current intervention dispositions

### T_ATTRIBUTION
Native Gutenberg plaintext is not a valid natural witness for attribution loss because NOTE labels and H.C. signatures survive.

### T_TEMPORAL
Native Gutenberg plaintext is not a valid natural witness for chronology loss because the object explicitly identifies the 1903/1920 assembly and later addenda retain page-targeted references.

### T_EVIDENCE
Typed support/challenge/revision edges are not native fields in the text. This intervention must operate on a constructed CEDL relation representation.

### T_BINDING
Claim bindings are source-grounded derived relations, not native Gutenberg fields. This intervention must operate on the constructed CEDL representation.

### T_NORMALIZE
A deterministic normalizer can be constructed, but its realism remains unverified until bound to an actual documented workflow.

## Scientific implication

This negative audit strengthens the project boundary:

`deletion != relation loss != increased reconstruction cost`.

If a relation remains recoverable from retained textual cues, the result must be coded as recoverability or access-cost change, not information loss.
