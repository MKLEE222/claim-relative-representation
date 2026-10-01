# Module C: Frankenstein native-pipeline continuation retention results v1

Date: 2026-09-28
Status: EXECUTED DEVELOPMENT RESULT ON ALREADY-EXPOSED C18. NOT INDEPENDENT TRANSFER.
GitHub Actions run: 36373059187
Artifact: module-c-fv-native-pipeline-continuation-v1
Artifact ID: 10950071329
Artifact ZIP SHA-256: 3b2835110162bb77129c0aeb09ad38e2c67a530dc7d1774b4cd446afd3a5ad2c
results.json SHA-256: acb0ebec46c3f8bc70c824b4b7f36881f461261a5954e34655dd69259cf2e291

## 1. Purpose

Modules A/B found continuation-context losses under constructed local interfaces.

Module C tested whether the actual pinned Frankenstein collation pipeline loses those same continuation obligations in its full serialized stages.

The registered continuation families remained:
- B-INCOMING;
- B-OUTGOING;
- B-CANCEL.

RAW_SOURCE was the reference.

## 2. Frozen native stages

1. RAW_SOURCE
   - collationChunks/C18/msColl_C18.xml
   - blob 8e537331ebf46dd4f013da9afcbe38c14092b6fd

2. INPUT_PRE
   - collationChunks/C18/input-pre/msColl_C18.xml
   - blob 8e537331ebf46dd4f013da9afcbe38c14092b6fd

3. INPUT
   - collationChunks/C18/input/msColl_C18.xml
   - blob 5bd2088e072805be05f1238dc3312764c8de0417

4. PARTWAY_APPARATUS
   - collationChunks/C18/output/Collation_C18-partway.xml
   - blob 008910e1a253e2ac2e6245e533f4b5de14ca3708

5. COMPLETE_APPARATUS
   - collationChunks/C18/output/Collation_C18-complete.xml
   - blob bca0548912ab1d7b2676360d33a6468290296d7e

The output-stage manuscript stream was reconstructed only from native fMS readings in document/app order. No evaluator source text was spliced into the output.

## 3. Main result

Every stage passed the continuation scanner with zero structural support errors.

| Stage | Scope inventory | Branch decisions | Positive branches | Current scope output |
|---|---:|---:|---:|---:|
| RAW_SOURCE | 112 / 112 | 336 / 336 | 9 / 9 | 112 / 112 |
| INPUT_PRE | 112 / 112 | 336 / 336 | 9 / 9 | 112 / 112 |
| INPUT | 112 / 112 | 336 / 336 | 9 / 9 | 112 / 112 |
| PARTWAY_APPARATUS | 112 / 112 | 336 / 336 | 9 / 9 | 112 / 112 |
| COMPLETE_APPARATUS | 112 / 112 | 336 / 336 | 9 / 9 | 112 / 112 |

No registered positive continuation instance is first lost at any native stage.

`FIRST_LOSS_DISTRIBUTION = {"NEVER_LOST_IN_REGISTERED_PIPELINE": 9}`

No missing/extra `sga-add` scope and no branch-ledger mismatch was observed.

## 4. Interpretation

This is a natural native-workflow null for the loss hypothesis.

The pinned Frankenstein collation workflow does **not** reproduce the continuation-context losses observed under Module A/B reduced local interfaces.

The full workflow preserves, through the complete published apparatus stream:

- all registered insertion identities;
- the two incoming `@next` obligations;
- the two outgoing `@next` obligations;
- the five registered cancellation-context obligations;
- the current source-scope text/place/hand output for all 112 scopes.

R2 separately established that the actual native pipeline reproduces the published C18 collation target exactly. Module C therefore adds a different result:

> task optimization and normalization in this mature native pipeline are compatible with preservation of the registered continuation state at full-stream scope.

This directly rejects a simplistic interpretation that the earlier local-interface result is caused by the upstream collation transformation itself.

## 5. Relation to Modules A/B

Module B immediate positive continuation-trigger exposure:

- CURRENT_SUMMARY: 0 / 9;
- START_ATTRS_PLUS_TEXT: 2 / 9;
- LOCAL_SCOPE_SERIALIZATION: 5 / 9;
- SOURCE_LINKED: 9 / 9.

Module C full native stages:

- RAW_SOURCE: 9 / 9;
- INPUT_PRE: 9 / 9;
- INPUT: 9 / 9;
- PARTWAY_APPARATUS: 9 / 9;
- COMPLETE_APPARATUS: 9 / 9.

Therefore the observed continuation boundary is presently located at the consumer-facing projection/interface layer, not at the registered native pipeline layer.

In particular, the two deletion-wrapped additions that are not self-describing in a milestone-bounded local serialization remain correctly contextualized when the complete manuscript stream is retained.

## 6. Scientific consequence

The stronger development pattern is now:

[
native transformation preservation

eq
consumer	ext{-}interface continuation exposure
]

A system can preserve the relevant relation globally while a local task-facing projection fails to expose it without inherited context or source navigation.

This matters because it prevents two invalid stories:

1. “normalization/collation destroyed the research relation” — not observed here;
2. “if the complete digital object contains the relation, every downstream research interface preserves equivalent researchability” — contradicted by Modules A/B under their declared local interfaces.

The natural native null is part of the result, not an inconvenience.

## 7. Claim boundary

Supported only for the nine registered continuation instances and 112 C18 insertion scopes.

Not established:

- arbitrary future scholarly tasks;
- local website/API behavior not represented by the tested interfaces;
- human discovery;
- superiority over ordinary provenance/navigation;
- cross-object replication;
- prevalence across Frankenstein;
- long-horizon sustained discovery;
- a universal preservation theorem.

C18 remains development material.

## 8. Next evidentiary obligation

The mechanism is now sufficiently differentiated for a genuine transfer test:

- do not merely repeat “is a field present?”;
- freeze a new source family or outcome-uninspected episode set before continuation outcomes;
- preserve native full-source/full-graph baselines;
- compare full native state to realistic consumer-facing projections;
- retain nulls where the full workflow or ordinary source navigation already preserves continuation.

The transfer must test the interface-level distinction, not seek a pipeline-loss positive result.
