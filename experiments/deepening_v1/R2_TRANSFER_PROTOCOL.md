# R2 transfer protocol v1 — Frankenstein native replay and fixed generic decoders

Date frozen: 2026-09-26
Status: prospective within-project transfer after C18 native replay; C16-C18 remain development.

## Source

Repository: FrankensteinVariorum/collationWorkspace
Pinned commit: 5a208f869ff1213defa000e3181d5315a072a15f

## Selector

Without parsing any target apparatus content, enumerate chunk directories C01..C31 at the pinned commit.

A chunk is eligible when all of the following filenames exist:
- five standard witness inputs in collationChunks/<chunk>/input:
  - 1818_fullFlat_<chunk>.xml
  - 1823_fullFlat_<chunk>.xml
  - 1831_fullFlat_<chunk>.xml
  - Thomas_fullFlat_<chunk>.xml
  - msColl_<chunk>.xml
- output/Collation_<chunk>-complete.xml exists.

Exclude C16, C17 and C18 because they were already used in development/audit work.

Select the first five eligible chunks in lexical chunk order. The selector may inspect archive member names and file existence only; it may not parse target XML before selection.

If fewer than five chunks qualify, execute every eligible chunk and report the shortfall.

## Frozen comparators

For each selected chunk:

1. NATIVE_REPLAY
   - regenerate both preprocessing stages from the pinned chunk;
   - run the vendored CollateX pipeline with the same compatibility shim already required by the successful C18 replay;
   - run native post-processing;
   - compare witness partitions and native descriptors to the pinned complete target.

2. SERIALIZED_EQUALITY
   - flatten the target app readings while ignoring their parent rdgGrp membership;
   - group witnesses by exact serialized reading content after whitespace collapse only.

3. STRIP_XML
   - same flattened readings;
   - remove serialized XML tags from reading content and collapse whitespace before equality grouping.

4. STRIP_XML_CASE_AMP
   - STRIP_XML plus Unicode-insensitive case folding and a fixed ampersand-to-"and" replacement.

The three generic decoders are diagnostics, not candidate replacements for the native pipeline.

## Registered grouping output

Per apparatus unit, the target is the witness partition encoded by the native complete apparatus.

The predictor for generic decoders receives:
- the app boundary;
- each flattened reading's witness IDs;
- that reading's own serialized content.

It does not receive parent rdgGrp identity or rdgGrp@n.

## Metrics

For every selected chunk and comparator:
- apparatus-unit count;
- exact partition match count;
- partition mismatch count;
- false-split units;
- false-merge units;
- units exhibiting both;
- examples bounded to ten.

NATIVE_REPLAY additionally reports preprocessing structural equality and descriptor equality.

## Claim ceiling

A successful transfer supports reproducibility of the native pipeline across the selected within-book chunks and quantifies how fixed generic normalization choices differ from it.

It does not:
- make five chunks five independent books;
- prove the native apparatus is historical ground truth;
- prove a generic mismatch is information-theoretic impossibility;
- establish source-location preservation.

A native failure is retained and investigated as environment/pipeline divergence before any scientific interpretation.
