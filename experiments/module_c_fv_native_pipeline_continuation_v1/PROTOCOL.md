# Module C: Frankenstein native-pipeline continuation retention v1

Date frozen: 2026-09-28
Status: DEVELOPMENT PROTOCOL ON ALREADY-EXPOSED C18; PRE-OUTCOME FOR THIS STAGE-RETENTION ANALYSIS.
Parents:
- experiments/deepening_v1/R2_NATIVE_REPLAY_RESULTS.md
- experiments/module_a_fv_scope_continuation_v1/
- experiments/module_b_fv_adaptive_branching_v1/

## 1. Question

Module A/B found continuation-context losses under constructed local interfaces.

Module C asks whether those losses occur in the actual pinned Frankenstein collation workflow itself, or only after a downstream consumer projects the workflow output into a smaller local interface.

The registered continuation obligations are the same three Module-B source-native families:

- B-INCOMING: incoming `sga-add@next` relations;
- B-OUTGOING: outgoing `sga-add@next` relation and resolution;
- B-CANCEL: cancellation context overlapping an `sga-add` scope.

No branch family is added after stage outcomes are opened.

## 2. Native stages

Pinned upstream commit:

`5a208f869ff1213defa000e3181d5315a072a15f`

Stages and frozen Git blobs:

1. RAW_SOURCE
   - `collationChunks/C18/msColl_C18.xml`
   - blob `8e537331ebf46dd4f013da9afcbe38c14092b6fd`

2. INPUT_PRE
   - `collationChunks/C18/input-pre/msColl_C18.xml`
   - blob `8e537331ebf46dd4f013da9afcbe38c14092b6fd`

3. INPUT
   - `collationChunks/C18/input/msColl_C18.xml`
   - blob `5bd2088e072805be05f1238dc3312764c8de0417`

4. PARTWAY_APPARATUS
   - `collationChunks/C18/output/Collation_C18-partway.xml`
   - blob `008910e1a253e2ac2e6245e533f4b5de14ca3708`

5. COMPLETE_APPARATUS
   - `collationChunks/C18/output/Collation_C18-complete.xml`
   - blob `bca0548912ab1d7b2676360d33a6468290296d7e`

R2 already established that the actual native preprocessing/alignment/post-processing pipeline reproduces the published C18 complete apparatus exactly at the registered collation target. Module C does not rerun or redefine that collation success criterion.

## 3. Stage stream construction

For RAW_SOURCE, INPUT_PRE and INPUT:
- scan the pinned manuscript XML serialization in source order.

For PARTWAY_APPARATUS and COMPLETE_APPARATUS:
- parse the apparatus XML;
- collect every `rdg[@wit="fMS"]` in document/app order;
- decode its XML text content;
- concatenate those manuscript-reading strings in order into a manuscript stage stream.

The reconstruction must report:
- apparatus unit count;
- number of fMS readings;
- any app containing more than one fMS reading;
- stage-stream bytes.

No evaluator-only source text may be spliced into an apparatus stream.

## 4. Common continuation scanner

Use one lexical/event scanner for every stage stream.

It tracks:
- `sga-add@sID` / `@eID` open scopes;
- opening attributes, including `xml:id`, `place`, `hand`, `next`;
- `del` / `mdel` context crossing arbitrary scope or app boundaries;
- normalized text accumulated while each insertion is open.

The scanner must stop or mark a stage unsupported if:
- an insertion marker is duplicated or unbalanced;
- the source reference scope cannot be identified;
- a stage contains ambiguous duplicate `xml:id` targets needed for a registered link.

This stage scanner is independent of Module B's full-XML recursive traversal implementation.

## 5. Reference and comparisons

RAW_SOURCE is the reference branch ledger.

For each later stage, compare:

### Scope inventory
- exact set of 112 reference `sga-add` IDs;
- extra/missing IDs.

### Current documentary scope output
For every shared scope:
- normalized enclosed text;
- place;
- hand.

This is diagnostic. R2's separately registered collation task remains the authoritative current-task native baseline.

### Continuation ledger
For every shared scope:
- B-INCOMING;
- B-OUTGOING;
- B-CANCEL.

Report:
- exact branch-family decisions out of 336;
- changed coordinates;
- positive branch instances retained out of the 9 Module-B source positives;
- newly introduced positive branch instances, if any.

Do not convert a missing/unsupported stage parse into FALSE.

## 6. Delayed-dependence analysis

For each RAW_SOURCE positive branch instance, record the first native stage at which its exact registered continuation output ceases to be recoverable.

Allowed labels:

- RAW_SOURCE
- INPUT_PRE
- INPUT
- PARTWAY_APPARATUS
- COMPLETE_APPARATUS
- NEVER_LOST_IN_REGISTERED_PIPELINE

This is descriptive across the pinned pipeline.

It is not a proof about every export, UI, API or downstream chunking policy.

## 7. Local-interface contrast

Module B remains the authority for constructed reduced interfaces:

- CURRENT_SUMMARY: 0 / 9 immediate positive branch triggers;
- START_ATTRS_PLUS_TEXT: 2 / 9;
- LOCAL_SCOPE_SERIALIZATION: 5 / 9;
- SOURCE_LINKED: 9 / 9.

Module C must not silently attribute those local-interface losses to the native pipeline.

If the full native COMPLETE_APPARATUS stream preserves all 9, the scientific result is a null for native workflow loss and a positive separation between full-stream preservation and downstream local-interface exposure.

If the native workflow loses any registered branch instance, report the exact first stage and source relation; do not generalize beyond C18.

## 8. Controls

1. Frozen source blobs are verified before analysis.
2. The source and apparatus scanners share the same branch semantics but not the Module-B reference traversal implementation.
3. All 112 source scopes remain in the denominator.
4. Module-B nulls and controlled `@next` twins are not reused as native-workflow outcomes.
5. No LLM or manual target repair is used.
6. All malformed, missing, extra and unresolved stage states are retained.

## 9. Claim ceiling

Possible supported result:

> A real task-optimizing collation workflow can preserve continuation-relevant documentary relations in its full serialized output even when later local projections of that output expose only a subset of those relations.

or, if losses occur:

> The pinned native workflow first ceases to preserve specified continuation obligations at identified transformation stages.

Not licensed:

- all Frankenstein interfaces preserve continuation;
- all collation systems behave similarly;
- full output is sufficient for arbitrary future scholarship;
- human users discover every preserved relation;
- long-horizon sustained discovery is solved;
- independent transfer.
