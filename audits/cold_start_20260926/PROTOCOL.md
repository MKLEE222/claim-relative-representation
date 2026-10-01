# Cold-start claim-construction audit

Date: 2026-09-26
Base commit: 3f4f31792a59bdb2d1a2bd57893f417d2d3c6a07
Status: POST-RESULT DIAGNOSTIC; NOT A NEW HOLDOUT OR CONFIRMATORY TEST

## Purpose

Check whether manuscript v0's conclusions are stronger than the operations its existing scripts perform. Preserve every old experiment, protocol, result and negative LLM outcome unchanged.

## A. Frankenstein C18

Use the original pinned complete C18 apparatus, verifying its Git blob SHA before analysis. Recompute native group partitions and the original whitespace-only reading-string comparison. Then report two explicitly post-result diagnostics:

1. remove serialized XML tags from each reading string, collapse whitespace;
2. additionally case-fold and replace ampersand with `and`.

These are illustrative normalization controls, not a reconstruction of the project's full normalizer. They cannot rescue the original holdout or prove that a residual mismatch is irreducible. Report how many mismatches are within-group splitting and how many merge distinct native groups. Record the native `rdgGrp@n` normalization descriptors and a few source-local witnesses. Do not treat descriptors copied from the target groups as independent prediction.

## B. Whitman

Use the original pinned relations file. The old subset script defines sufficiency by checking whether PRINT_LOCUS, MS_FILE and MS_LOCUS were included; it does not reconstruct task outputs for every subset. This diagnostic therefore reports observed mapping ambiguity separately for:

- MS_LOCUS -> MS_FILE;
- (PRINT_LOCUS, MS_LOCUS) -> MS_FILE;
- (PRINT_LOCUS, MS_LOCUS, CERTAINTY) -> MS_FILE.

A repeated local identifier alone does not establish ambiguity after other retained coordinates are considered. Conversely, uniqueness on this one corpus does not provide a permitted decoder or prove general sufficiency. No data-derived lookup table is silently supplied to the consumer. Count malformed links and missing attributes rather than skipping without a denominator.

## C. Faust

Use the original pinned XML archive. Count all source elements, parse failures and temporal assertions. Report source-set variation conditional on FILE_CONTEXT and on (FILE_CONTEXT, ORDERED_ITEMS). Also report the analogous edge-level ambiguity inside nontrivial strongly connected components. A file's multiple sources do not by themselves prove that the larger retained projection (file plus items) fails. No uniqueness finding is called source recoverability without an explicit source-side decoder and its information cost.

## Interpretation ceiling

These checks audit claim validity and identify concrete repairs. No positive count establishes new theory. The native projects own their transformations, normalization and scholarly semantics. The current study must add an auditable task-to-source comparison, not rebrand their existing design principles.

## Output

Machine-readable JSON containing source hashes, all denominators, mismatch/ambiguity counts, bounded examples and explicit limitation statements. A nonzero scientific discrepancy is a result, not a CI failure. Hash or transport failure blocks source conclusions. No LLM calls are authorized by this audit.
