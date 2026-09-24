# Retrieval Contract v1

Date frozen: 2026-09-24
Status: PRE-EXPERIMENT CONTRACT

## Motivation

Ecological Anchor E1 showed that putting PM03 inside the searchable collection did not make it practically retrievable under the frozen seed-TFIDF policy.

Therefore the access layer must distinguish:

1. representation/access scope;
2. retrieval/navigation policy;
3. later human relevance recognition.

The project must not attribute a retrieval-policy failure to representation alone.

## Access decomposition

For task tau under representation R and recovery contract K:

### Availability

Avail(tau,R,K)=1 when the relevant evidence object lies inside the allowed evidence universe.

### Retrievability

Retr(tau,R,K,pi,B)=1 when retrieval policy pi surfaces the relevant object within budget B.

### Discoverability

Disc(tau,R,K,pi,B,human)=1 when the surfaced object is recognized as relevant by the evaluator.

The first two can be studied computationally. The third requires a human-facing or independently adjudicated relevance stage.

## Retrieval policy

A retrieval policy pi specifies:

- query construction rule;
- searchable fields/text;
- candidate unit;
- ranking/filtering rule;
- navigation rule;
- stopping/budget rule.

Changing pi defines a different access experiment.

## Frozen policy family

### PI_SEED_SIMILARITY

Mechanically derive weighted query terms from the known seed passage only and rank windows by lexical similarity.

This is the policy used in E1.

### PI_NAMED_SOURCE_CHAIN

If the seed explicitly names a cited source/scholar, search the declared collection for that name.

This corresponds to source/citation chaining rather than generic semantic similarity.

No name absent from the seed may be introduced.

### PI_NAMED_SOURCE_DOMAIN_FILTER

Start from PI_NAMED_SOURCE_CHAIN and retain only hits that also contain at least one domain term derived from the seed passage.

This tests whether a scholar-name chain plus topical filtering reduces inspection burden.

### PI_POINTER_FOLLOW

Follow an explicit bibliographic/page/cross-reference pointer already present in the seed or current object.

No inferred pointer may be invented.

Held for later use where the source contains a suitable pointer.

## Policy comparison rule

Policy sensitivity is not evidence that one representation is globally better.

For fixed R and task entry state, report:

- candidate-set size;
- target-in-candidate-set;
- target rank/ordinal where defined;
- inspection budget required;
- whether query terms were seed-derived or externally supplied.

## Leakage rule

Target-only information may be used only for evaluation.

For paper-money E1D:
- BRETSCHNEIDER is allowed because it is explicit in PM02.
- LAUFER is forbidden in query construction because it is target-only with respect to PM02.

## Claim ceiling

A computational retrieval replay can support claims about availability and retrievability under the declared policy.

It cannot establish human discoverability or final claim-warrant consequences.
