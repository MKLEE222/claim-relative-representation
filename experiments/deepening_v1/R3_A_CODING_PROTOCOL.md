# R3-A inventory adjudication protocol v1

Date frozen: 2026-09-27
Status: active humanities coding protocol after the 229-candidate structural enumeration.

## Purpose

Turn the reproducible 229-candidate frame into a defensible editorial-intervention inventory without letting lexical cues determine the historical relation.

The unit of analysis is a retrospective editorial entry in Cordier's 1920 Notes and Addenda that points back to, quotes, or otherwise explicitly revisits the Yule-Cordier edition.

## Stage 0 — frame validity

For every candidate, first decide whether the regex head is actually an Addenda entry head rather than:
- a bibliographic citation inside an entry;
- a numbered sub-item in a quoted source;
- a chapter/page reference belonging to an external work;
- a continuation line accidentally matching the head pattern.

A candidate excluded at Stage 0 remains in the denominator ledger with a reason.

No relation-family coding occurs until Stage 0 = VALID_ENTRY.

## Stage 1 — backward target

For each valid entry, record:
- volume/book/chapter where recoverable;
- 1903 page reference exactly as printed in the Addenda head;
- quoted earlier wording if present;
- whether the target locus can be matched in the 1903 Gutenberg/page witness.

Target status:
- TARGET_VERIFIED;
- TARGET_PROVISIONAL;
- TARGET_UNRESOLVED.

## Stage 2 — responsibility

Record distinct roles rather than collapsing names:
- base narrator / Marco Polo when the quoted narrative is his;
- Yule as translator/commentator where applicable;
- Cordier as 1903 reviser/editor;
- Cordier as 1920 addenda editor;
- cited later scholar(s);
- cited earlier scholar(s).

Do not infer authorship of an evaluative sentence from proximity alone.

## Stage 3 — relation family

Assign one or more labels only where the wording licenses them:

ADDITIVE_EVIDENCE
CORROBORATION
CRITICISM
CORRECTION_OF_PRIOR_CRITICISM
IDENTIFICATION_UPDATE
ATTRIBUTION_UPDATE
TEXTUAL_UPDATE
QUALIFICATION
UNRESOLVED_RELATION

Every non-UNRESOLVED label must include a short evidence span from the 1920 entry.

## Stage 4 — humanistic consequence

Record whether the intervention changes any of the following research-relevant objects:
- geographical/onomastic identification;
- route reconstruction;
- textual reading/translation;
- source attribution;
- eyewitness/hearsay status;
- chronology;
- material culture identification;
- political/institutional interpretation;
- natural-history identification;
- economic/quantitative interpretation;
- no substantive change / additive context only;
- other, with note.

This field is descriptive and may be multi-valued.

## Stage 5 — verification authority

Coding authority levels:
- TRANSCRIPTION_ONLY: reproducible Gutenberg source only;
- PAGE_VERIFIED_1920: 1920 printed/page image checked;
- PAGE_VERIFIED_BOTH: both 1920 entry and earlier target checked in printed/page images.

Only PAGE_VERIFIED_BOTH episodes may carry the strongest historical claim in close reading.

## Coding discipline

- Cue flags generated during enumeration are hidden during relation coding.
- Do not force every entry into a change relation.
- ADDITIVE_EVIDENCE is a substantive category, not a residual failure.
- Multiple labels are allowed.
- Unresolved cases remain unresolved.
- Exact historical truth is not adjudicated by this coding layer.

## Reliability

The first pass may be model-assisted/manual but every coded row must retain its evidence span and source offsets.

Before manuscript counts are final:
- all rows classified as criticism/correction/identification/attribution must receive a second independent review;
- all five close-reading episodes require page-image verification;
- disagreements are retained in an adjudication ledger rather than silently overwritten.

## Outputs

1. complete frame ledger, 229 rows;
2. valid-entry denominator and exclusion reasons;
3. intervention-family counts with multi-label reporting;
4. humanistic-consequence counts;
5. verified episode shortlist by relation family;
6. unresolved/disagreement ledger.
