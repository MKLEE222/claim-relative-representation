# R2 Frankenstein native-pipeline reproduction result

Date: 2026-09-26
Authority: retrospective reproduction on the pinned upstream project.
Authoritative run: GitHub Actions 36251010043.
Artifact: deepening-r2-result, artifact id 10909710121, archive SHA-256 05f298b85dfdbc121d4c244af4598d40b79badf4b2b4bd6c6e35d9a724256b26.

## Reproduction

Pinned upstream commit: 5a208f869ff1213defa000e3181d5315a072a15f.

The historical project pipeline was replayed from the five C18 witness inputs:
- preprocessing stage 1;
- preprocessing stage 2;
- vendored CollateX;
- native post-processing.

A compatibility shim changes only modern ClusterShell iteration syntax to its documented integer iterator while preserving the historical integer-position semantics.

Results:
- regenerated preprocessing inputs structurally match all pinned inputs;
- published apparatus entries: 493;
- replay apparatus entries: 493;
- witness-partition mismatches: 0;
- native descriptor mismatches: 0;
- full structural digest equality: yes.

## Consequence

The actual native normalization/alignment/post-processing contract reproduces C18 exactly. Therefore the old 166 whitespace-only serialized-string mismatches are evidence against that weak decoder, not against the upstream pipeline.

The supported comparison is now:
- raw serialized equality is weak;
- generic normalization removes many false distinctions but can introduce false merges;
- the native pipeline recovers the published C18 target exactly.

This credits the upstream project rather than manufacturing a weak baseline.

## Remaining R2 task

R2_FV_TASKS remains open. It must test cross-task preservation without feeding target-group attributes back to the predictor:
- grouping recovery;
- source/read-location recovery;
- controlled normalization variants;
- source-bound repair where a normalized representation lacks a required relation.

C16-C18 remain development material. Any broader chunk transfer requires an outcome-agnostic selector frozen before target inspection.
