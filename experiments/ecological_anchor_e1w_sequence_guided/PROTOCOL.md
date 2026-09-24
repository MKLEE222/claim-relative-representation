# Ecological Anchor E1W - Sequence-guided scholarly chaining workflow

Date frozen: 2026-09-24
Status: EXPLORATORY WORKFLOW COMPOSITION AFTER E1/E1D

## Motivation

E1 showed that broader collection scope is insufficient under seed-similarity retrieval.
E1D showed that named-source chaining reduces the candidate set but still leaves substantial inspection burden.

This experiment does not revise either result.

It tests a different, task-grounded workflow:

> when the research question explicitly asks for **later treatment** of a known 1903 objection, use the native edition chronology to restrict navigation to the later 1920 addenda, then perform source-name chaining from the seed.

This composes tau_sequence with tau_locate rather than treating retrieval as context-free search.

## Native chronology cue

Project Gutenberg Volume II identifies itself as containing:
- the second volume of the 1903 edition; and
- the 1920 volume of addenda.

Within the native text, the later section has the heading:
"NOTES AND ADDENDA TO SIR HENRY YULE'S EDITION"
and describes itself as supplementary Addenda and Corrigenda.

The workflow locates that heading mechanically.

## Entry state

Provided:
- PM02 seed objection;
- research request to find later treatment;
- native two-volume edition.

Withheld:
- PM03 locator;
- Laufer's name;
- expected relation label;
- expected claim outcome.

## Policy

### PI_SEQUENCE_GUIDED_SOURCE_CHAIN

1. infer from the task wording that only later editorial material is relevant;
2. locate the native Addenda section using its heading;
3. extract the cited scholar surname from PM02;
4. search only the Addenda section for that surname.

### PI_SEQUENCE_GUIDED_DOMAIN_CHAIN

Apply the same procedure, then require at least one topical term derived from the PM02 seed.

## Why this is not target leakage

The workflow uses:
- the task's word "later";
- chronology/section labels already present in the native edition;
- the source name already explicit in PM02;
- topic terms already present in PM02.

It does not use:
- LAUFER;
- PM03 page number;
- PM03 text;
- the knowledge that PM03 is a correction.

## Outcomes

Report:
- native Addenda boundary location;
- extracted seed source name;
- active seed-derived domain terms;
- candidate count;
- PM03 inclusion;
- PM03 ordinal among candidates.

## Claim ceiling

This can support only a workflow-level retrievability claim:
whether sequence-aware scholarly chaining changes inspection burden relative to E1/E1D.

Human relevance recognition and claim adjudication remain untested.
