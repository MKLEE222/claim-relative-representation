# Archival Argument-Reinstatement Protocol v1

Date frozen: 2026-09-26
Status: NEW STUDY AFTER NEGATIVE LLM-JUDGE RESULT

## Motivation

The frozen LLM-judge experiment failed: two stable models collapsed all packet states to RETAIN and one model was perturbation-sensitive.

Rather than tune the judge, this protocol replaces opaque categorical judging with a transparent relation-sensitive consequence.

## Scientific object

Given a frozen active evidence state, construct an abstract argumentation framework:

`AF = (A, ->)`

where arguments are source-bound documentary/evaluative acts and attack edges are admitted only when explicitly licensed by page-verified archival stance traces.

## Paper-money arguments

`A0_PM01_ASSERTION`
Polo/Yule base assertion identifying mulberry bark as the material used for the paper-money.

`A1_PM02_OBJECTION`
Bretschneider objection as transmitted by Cordier: Polo 'seems to be mistaken'; paper is said not to be made from mulberry-trees but Broussonetia papyrifera.

`A2_PM03_CORRECTION`
Laufer correction as transmitted by Cordier: Bretschneider's statement is explicitly called an error and Polo is explicitly called correct.

## Attack edges

`A1_PM02_OBJECTION -> A0_PM01_ASSERTION`

Source basis:
`PMT01 ST_CRITICISM`.

`A2_PM03_CORRECTION -> A1_PM02_OBJECTION`

Source basis:
`PMT02 ST_PRIOR_CRITIC_CORRECTION`.

`PMT03 ST_ENDORSEMENT` is retained as source provenance but is not required to manufacture an additional attack edge.

## Semantics

Use standard grounded semantics on the active attack graph.

Grounded semantics is chosen because it is:
- deterministic;
- skeptical;
- uniquely defined;
- transparent under attack / counter-attack reinstatement.

No numerical confidence score is introduced.

## Claim status

The focal argument is `A0_PM01_ASSERTION`.

Report only:
- `IN_GROUNDED_EXTENSION`;
- `OUT_GROUNDED_EXTENSION`;
- `UNDECIDED` if a future graph structure requires it.

These are formal acceptance statuses under the declared semantics.

They are NOT:
- historical truth;
- human scholarly judgment;
- an LLM opinion.

## Packet activation

PM01 and PM02 are fixed context in every final packet.

PM03 is active only when the frozen audit manifest marks one PM03 evidence unit present.

Therefore the five already frozen packet constructions are reused without modification:
- GENERIC_BASE;
- GUIDED_BASE;
- GENERIC_RESCUE_PM03;
- GENERIC_SHAM;
- GUIDED_REMOVE_PM03.

## Frozen selective-reinstatement prediction

Before execution:

- GENERIC_BASE: A0 expected OUT because A1 is active and undefeated;
- GUIDED_BASE: A0 expected IN because A2 defeats A1;
- GENERIC_RESCUE_PM03: A0 expected IN;
- GENERIC_SHAM: A0 expected OUT;
- GUIDED_REMOVE_PM03: A0 expected OUT.

This prediction follows mechanically from the explicitly frozen attack graph and is therefore a formal consequence test, not a statistical discovery claim.

## Empirical / formal separation

Empirical facts:
- which source acts exist;
- which attack/correction relations are explicit;
- which evidence units are active under each representation/navigation condition.

Formal consequence:
- grounded acceptance status of A0 on each active subgraph.

The paper must keep those layers separate.

## Claim ceiling

Admissible:
> representation/navigation changes can alter the active scholarly argument graph and thereby change claim acceptance under a fixed skeptical argumentation semantics.

Not admissible:
> representation/navigation changes what historians actually believe.