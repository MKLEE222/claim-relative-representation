# Generic Seed-Task Access Policy v1

Date frozen: 2026-09-24
Status: CONTENT-AGNOSTIC TRANSFER POLICY

## Purpose

Test whether the task-adaptation mechanism discovered in paper money transfers to a different Yule-Cordier episode without copying paper-money-specific source names or topic terms.

## Inputs

Only:
- exact seed text;
- answer-neutral task wording;
- native digital object;
- native historical-layer boundary when licensed by the task.

The hidden target is not an input.

## Query construction

1. tokenize seed + task wording;
2. lowercase and normalize hyphenation;
3. remove a frozen general-English stoplist;
4. compute IDF from the pre-Addenda/base portion of the same native object;
5. score seed/task terms by TF x IDF;
6. select top K=12 terms.

No case-specific domain dictionary is allowed.

## Candidate representation

- 180-word windows;
- 90-word stride;
- lexical weighted-overlap ranking;
- identical ranking policy in all scope conditions.

## Scope conditions

### GSA_FULL_OBJECT

Search the declared digital object.

### GSA_LATER_LAYER

When and only when the task explicitly asks for later treatment, restrict the same candidate/ranking procedure to the native later editorial layer identified by its own heading.

No target-specific subsection/page may be supplied.

## Metrics

- target in scope;
- candidate count;
- target rank;
- reciprocal rank;
- Hit@10/20/50;
- query terms;
- source hash.

## Leakage rule

Terms used only to identify the hidden target are forbidden from query construction.

For EP_KS_01 the evaluation-only terms are:

Tanner | sea wall | native poet | never visited Hang Chau

The target locator is used only after candidate generation.

## Falsification

A transfer claim is weakened if GSA_LATER_LAYER does not materially reduce inspection burden relative to GSA_FULL_OBJECT under the frozen policy.

No post-outcome query tuning is permitted inside v1.
