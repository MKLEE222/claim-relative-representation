# Holdout Construction Protocol v1

Date frozen: 2026-09-24
Status: PRE-HOLDOUT CONSTRUCTION CONTRACT

## Goal

Build holdout carriers without turning them into paper-money lookalikes and without tuning the retrieval workflow to known target passages.

The unit is not a random text row. It is a **scholarly transition episode**:

\[
E=(s,\tau,h,t,N,W,R)
\]

where:

- **s**: a realistic research seed state;
- **tau**: a frozen scholarly task;
- **h**: the native historical/version horizon in which a later treatment could occur;
- **t**: the hidden evaluation target, if one exists;
- **N**: native representation(s);
- **W**: workflow replay(s);
- **R**: source-aligned reference used only for target verification/evaluation.

## Construction principle

The development case may teach us which *operations* are plausible.

It may not teach us the lexical content of the holdout query.

Therefore workflow transfer is defined at the rule level, not by copying paper-money terms.

## Episode roles

### DEV
Used for mechanism discovery, debugging, policy design, and failure analysis.

Current:
- paper money (PM01-PM04)

No DEV result is treated as an independent replication.

### NEAR_HOLDOUT
Same documentary ecology, different humanistic mechanism.

Current:
- Kinsay/Hangzhou

Purpose:
- test whether the frozen workflow family transfers within Yule-Cordier without retuning.

### BOUNDARY
Same documentary ecology, deliberately different evidential structure.

Current:
- coal/editorial accretion

Purpose:
- test whether the framework correctly predicts that some tasks are locally recoverable and do not require the same cross-layer access workflow.

A null or weaker effect is scientifically valuable.

### EXTERNAL_HOLDOUT
Different historical object and, preferably, different editorial tradition.

Purpose:
- test cross-object transport.

Selection occurs by predeclared eligibility criteria before retrieval outcomes are inspected.

## Holdout eligibility criteria

A candidate external carrier is eligible only if all are true:

1. historical/public-domain scholarly object;
2. at least two independently identifiable documentary/editorial states;
3. at least one source-facing later treatment that can plausibly bear on an earlier proposition, attribution, identification, or authority claim;
4. native digital representations are publicly accessible;
5. the later target can be source-verified independently of the retrieval experiment;
6. the seed can be stated without naming the later target;
7. the object supplies a realistic navigation/search horizon;
8. the case is not selected because a pilot search already succeeded.

## Holdout sealing

Before execution, freeze:

- seed passage/object;
- task wording;
- native object IDs/hashes where possible;
- historical horizon rule;
- workflow policy family;
- retrieval budget;
- target-evaluation anchor in a sealed/evaluation-only field;
- failure/null retention rule.

The target anchor is never used for query construction.

## Content-agnostic workflow family

The transferred workflow is:

### W1 - Horizon restriction

Use only task-relevant historical direction that is available from the task itself.

Examples:
- "later treatment" permits restriction to documentary layers later than the seed;
- "earlier source" permits restriction to earlier layers.

No target-specific page/section may be supplied.

### W2 - Seed signature extraction

Generate a query signature from:

- the task wording;
- the seed passage;
- native metadata exposed at the seed state.

Allowed features:
- named entities present in the seed;
- rare content tokens present in the seed;
- explicit citation/source names present in the seed;
- place/person/referent terms present in the task wording.

Forbidden:
- target-only names;
- target-only vocabulary;
- target page numbers;
- known relation labels.

### W3 - Native-structure navigation

Use section/edition/addenda boundaries that are native to the digital object.

The workflow may restrict to a later layer when the task itself asks for later treatment.

### W4 - Candidate retrieval

Apply the frozen retrieval policy family without case-specific parameter tuning.

Primary family:
- named-source chaining if the seed contains an explicit source name;
- otherwise seed/task signature retrieval;
- optional seed-domain filtering using only seed/task terms.

### W5 - Evaluation-only target matching

Only after candidate generation:
- identify whether the hidden target was surfaced;
- record ordinal/rank and inspection burden.

## Non-applicability is an outcome

If a workflow primitive is unavailable on the holdout, record N/A.

Examples:
- no named source in seed -> named-source chaining is N/A;
- no distinct later layer -> sequence-guided restriction is N/A.

Do not invent an analogue to make the workflow run.

## Replication interpretation

### TRANSFER
Frozen rule family produces the expected mechanistic reduction in access/recovery burden.

### PARTIAL_TRANSFER
Some primitives transfer, others are N/A or weaker.

### BOUNDARY_CONFIRMED
The holdout is correctly solved by a simpler/local route, showing that the framework is selective rather than universally structure-hungry.

### FAIL_TRANSFER
The frozen rule family does not improve the relevant task or violates task realism.

All four are publishable scientific outcomes.

## Dataset role

The corpus is not framed as a large benchmark.

It is a small, source-verified **transition-episode corpus** designed for causal/mechanistic analysis.

Its strength comes from:
- provenance;
- task realism;
- negative/boundary cases;
- sealed holdouts;
- explicit null retention;
not from row count.
