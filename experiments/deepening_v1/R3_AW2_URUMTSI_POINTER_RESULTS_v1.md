# R3-AW2 Urumtsi Native Page-Pointer Repair Results v1

Date: 2026-09-27
Status: EXECUTED SELECTIVE ECOLOGICAL REPAIR
Primary run: GitHub Actions 36311166597
Evaluator-only repair: GitHub Actions 36311209881

## Background

R3-AW1 tested the five frozen R3 inquiries under Generic Seed-Task Access Policy v1.

For Urumtsi:
- native later-layer candidate universe: 482 windows;
- lexical target rank: 65;
- Hit@10 = 0;
- Hit@20 = 0;
- Hit@50 = 0.

Direct source inspection nevertheless established that the erratum is present and determinate in the natural plain-text object.

AW2 therefore tests an alternative source-native carrier route rather than retuning AW1.

## Pre-existing carrier rule

The tested route was already admissible before the Urumtsi AW1 outcome.

Generic Access Workflow v1 and Source-Grounded Mediation Contract v1 were frozen on 2026-09-24 and permit:
- document-local identifiers available from the seed/task state;
- native explicit page/cross-reference pointers.

The R3 inquiry panel freezes the Urumtsi historical start as 1903 p.201.

No answer-bearing lexical term is needed to construct the bridge.

## Conditions

Correct document-local identifier:
- 201

Pre-frozen adjacent sham identifiers:
- 200
- 202

All three use the same extraction and matching code over native page-pointer units in the 1920 Addenda layer.

## Result

After the evaluator-only repair for Gutenberg underscore emphasis markup:

### Correct identifier — page 201

Matched native pointer units: 1

Matched unit:
> P. 201, Line 12. Read the Governor of Urumtsi _founded_ instead of _found_.

Frozen erratum target in returned set: YES.

### Sham page 200

Matched native pointer units: 0

Frozen erratum target in returned set: NO.

### Sham page 202

Matched native pointer units: 1

Matched head:
> pp. 202.

This is a different source unit.

Frozen erratum target in returned set: NO.

## Selective repair

[
CORRECT_RECOVERS_TARGET = 1
]

[
SHAM_{200} = 0,qquad SHAM_{202} = 0
]

[
SELECTIVE_REPAIR_PASS = 1
]

The candidate burden changes from:
- 482 later-layer windows under AW1 lexical access;
- target at rank 65;

to:
- 1 native pointer unit under the page-201 route;
- target recovered exactly.

## Scientific interpretation

The result establishes a natural carrier-specific repair of research access.

The same Project Gutenberg plain-text object supports two different lawful research routes from the same historical episode:

1. generic lexical retrieval:
   target remains outside B50;

2. source-native page-pointer mediation:
   exact target is isolated as one candidate.

Thus the relevant object is not merely whether information is present in a representation.

It is whether the representation exposes a carrier system that can be composed with the researcher's entry state.

A natural representation may be weak under one route and highly effective under another.

## Relation to proposition-level binding results

AW2 repairs discovery/access, not a controlled proposition-binding deletion.

Once the erratum passage is supplied, its proposition-level answer is already determinate:
`found -> founded`.

Therefore this result must not be used to claim that a natural pointer restores a lost stance-to-target, commitment, or evidence edge.

Instead the evidence layers are:

- controlled R3 separation: proposition-binding determinacy;
- natural plain-text check: relation remains textually recoverable;
- AW1: workflow-specific discoverability burden;
- AW2: source-native carrier-specific discovery repair.

Together these establish a multi-stage researchability mechanism without pretending that all stages are the same kind of loss.

## Claim ceiling

Supported:
> a recoverable historical relation that is poorly surfaced under a frozen generic lexical workflow can be selectively restored to practical discoverability by a source-native documentary identifier available from the historical entry state.

Not supported:
- global minimality;
- all page pointers being sufficient;
- all lexical retrieval being inadequate;
- natural proposition-binding deletion;
- whole-book prevalence;
- human search behavior.

## Implementation note

The first AW2 target checker returned a false negative because Gutenberg emphasis underscores prevented a word-boundary regex from matching `_founded_` / `_found_`.

Candidate generation in that run was already correct and exposed the exact target under page 201.

The repair stripped underscore emphasis only for evaluation and changed no candidate, identifier, workflow rule, or sham condition.
