# R3 Great Desert Exact-Start Generic-Access Replication Protocol v1

Date frozen: 2026-09-27
Status: PRE-OUTCOME ENTRY-STATE FIDELITY REPLICATION

## Reason for this replication

R3_GENERIC_ACCESS_TRANSFER_v1 successfully executed the previously frozen Generic Seed-Task Access Policy v1 across five R3 inquiries. After opening that run, the Great Desert seed was audited against the already-frozen inquiry contract.

The inquiry contract had always specified:

- inquiry: R3Q-DES-EVIDENCE;
- historical entry state: HISTORICAL_START_FROM_1903_GREAT_DESERT_NOTE;
- admissible earlier source: 1903 I:202.

The v1 seed phrase was drawn from a broader Great Desert chapter context and is therefore not accepted as an exact implementation of the frozen p.202 entry state.

This replication repairs **entry-state fidelity**, not the retrieval policy or success criterion. The v1 result is retained as a broader-start workflow result and is not overwritten.

## Exact historical start

Registered 1903 source locus: Volume I, p.202, Note 2.

Seed anchor:

`The waste and desert places of the Earth`

This is the opening phrase of the p.202 note used in the historical source audit.

## Frozen access task

`Find later editorial treatment bearing on the Great Desert folklore source interpretation and the distance or marches described in the earlier note.`

## Evaluation-only carrier groups

FOLKLORE_SOURCE:
`faithful reflex of old folklore beliefs he must have heard on the spot`

MEASUREMENT:
`plane-table survey checked by cyclometer readings`

These anchors are evaluation-only and may not enter query construction unless independently present in the 1903 seed.

## Workflow parameters — unchanged

Inherited without modification from Generic Seed-Task Access Policy v1 and R3_GENERIC_ACCESS_TRANSFER_v1:

- native objects: registered Gutenberg V1 + V2;
- candidate windows: 180 words;
- stride: 90 words;
- query size: top K=12;
- query weighting: TF x IDF;
- ranking: weighted lexical overlap;
- IDF corpus: V1 + V2 pre-Addenda;
- FULL_OBJECT scope: both complete volumes;
- LATER_LAYER scope: native 1920 Addenda;
- target-only terms forbidden;
- no query tuning after outcome.

## Outcomes

For each scope report:

- candidate count;
- query terms;
- rank of FOLKLORE_SOURCE;
- rank of MEASUREMENT;
- Hit@10/20/50 for each;
- collective completeness at 10/20/50;
- whether one 180-word window contains both carrier groups.

## Interpretation rule

A poor rank is a discoverability/access result, not proof that the underlying source representation deletes a binding.

A multi-window requirement is a carrier-exposure/profile result, not proof of source-level information loss.

The proposition-binding controlled separation remains a separate Tier-2 mechanism result.

## Comparison with v1

The exact-start result will be compared descriptively with the already-opened broader-start Great Desert result:

- FULL_OBJECT: folklore rank 77; measurement rank 146;
- LATER_LAYER: folklore rank 15; measurement rank 31;
- later-layer collective completeness first reached at H50.

No parameter may be changed to make the exact-start result resemble or improve on v1.

## Disposition

If exact-start remains difficult, the project gains an entry-state-faithful ecological burden result.

If exact-start improves materially, retain that result: the broader-start burden was partly an entry-state effect.

If exact-start fully resolves the inquiry at a small budget, retain the null for strong workflow impairment.
