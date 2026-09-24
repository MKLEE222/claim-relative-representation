# Ecological Validity Contract v1

Date frozen: 2026-09-24
Status: PRE-EXPERIMENT DESIGN CONTRACT

## Reviewer-facing problem

A controlled representation study can become scientifically circular if it compares a researcher-built "ideal" representation against deliberately degraded variants and then concludes that the ideal is better.

This project therefore separates three different objects that must never be conflated:

1. **native representations** that actually exist;
2. **source-aligned reference reconstructions** used for adjudication;
3. **controlled projections** used for causal identification.

The reference reconstruction is not treated as a deployed system, a historically natural object, or a globally optimal representation.

## Representation classes

### N - Native representation

An object that exists independently of this experiment.

Examples in the current carrier:
- printed page-image witnesses;
- scan-tied OCR;
- Project Gutenberg HTML/plain text;
- historical edition layers as published.

Claims about ecological behavior may be made directly from N objects.

### W - Workflow replay

A deterministic transformation that reproduces a documented or common digital workflow on a native object.

Examples:
- body-only export;
- metadata stripping;
- chunk extraction;
- pointer/link omission;
- normalization using a declared rule.

A W object is experiment-generated, but its operation is independently grounded and reproducible.

### C - Controlled projection

A deliberately isolated representation used to identify the effect of one declared coordinate.

Examples:
- remove only structured attribution while preserving the source span;
- remove only a typed CEDL edge;
- restrict only the allowed context horizon.

C objects are valid for mechanism identification, not for claims about how often real-world systems instantiate that exact state.

### R - Source-aligned reference reconstruction

A research scaffold assembled from verified witnesses to record the richest currently recoverable documentary relation state.

R is used to:
- freeze claim/event identity;
- verify source relations;
- define restoration targets;
- adjudicate whether a native or replayed object exposes a relation.

R is **not**:
- a gold historical truth;
- an ideal user-facing edition;
- evidence that all systems should encode every field it contains.

## Anti-idealization rule

The project must not formulate the main comparison as:

"full/ideal representation versus degraded representation."

Instead, claims are tiered.

### Claim Tier 1 - Native descriptive claim

Example form:

> In native representation N1, relation q is explicit; in native representation N2, q is only recoverable through cross-layer traversal.

Requires only native-object evidence.

### Claim Tier 2 - Mechanism claim

Example form:

> Removing carrier b1 under controlled projection C shifts recovery to carrier b2 while other declared coordinates remain invariant.

Requires controlled intervention plus invariant checks.

### Claim Tier 3 - Ecological mechanism claim

Example form:

> The mechanism identified in C is also instantiated by at least one native object or independently documented workflow replay W.

Requires convergence between controlled and ecological evidence.

### Claim Tier 4 - Generalized design claim

Example form:

> A class of representation transformations systematically changes task-adapted recoverability across cases/workflows.

Requires replication across more than one carrier family or workflow. Current Yule-Cordier experiments alone cannot establish this tier.

## Natural-anchor requirement

Every transformation family used in a confirmatory claim must have one of:

- a native representation contrast showing the relevant coordinate differs naturally; or
- a documented workflow replay that produces the relevant contrast from a native source.

A TEI feature analogue is sufficient for design plausibility, but **not by itself** sufficient for an ecological-effect claim.

## Concordance requirement

A controlled result is strengthened when the same mechanism appears in an independently existing representation contrast.

Concordance is evaluated mechanistically, not by requiring identical numerical effect size.

Examples:
- structured chronology absent but lexical chronology recoverable;
- explicit note binding absent but local contextual rebinding possible;
- separate-edition access makes a later corrective witness harder to discover than a merged searchable object.

Discordance is retained and reported.

## Task-entry realism

Access/discovery tasks must begin from a realistic research entry state rather than from a curated packet that already contains all relevant evidence.

Permitted entry states include:
- a chapter/passage already under study;
- a bibliographic citation;
- a research question plus access to a real digital object;
- a seed passage plus the navigation/search affordances of the declared object.

For relation tasks, curated endpoints are permitted because discovery is intentionally held fixed.

The paper must state which stage is being experimentally supplied.

## Strong-claim prohibition

The following are prohibited unless directly supported:

- "the full representation is better";
- "plain text loses provenance";
- "metadata removal destroys evidence";
- "the reference reconstruction is the ideal scholarly edition";
- "the controlled projection represents the prevalence of real digital editions."

## Integration with Gate T

Gate T is split into three subconditions:

### T1 - operation realism
The transformation corresponds to a documented operation or defensible digital workflow.

### T2 - representation provenance
The input object is classified as N, W, C, or R and its provenance is explicit.

### T3 - ecological anchoring
Any ecological-effect claim is tied to at least one native contrast or workflow replay.

A controlled mechanism experiment may proceed with T1+T2 while T3 remains pending, but its claim tier is capped at Tier 2.
