# Module B v2 results — source-triggered branching on Frankenstein C18

Date: 2026-09-28
Status: EXECUTED DEVELOPMENT REANALYSIS AFTER PREDECLARED EVALUATOR REPAIR. NOT INDEPENDENT TRANSFER.

Authoritative execution:
- GitHub Actions run 36375362424
- artifact: module-b-fv-source-branching-v2
- artifact ID: 10950304992
- artifact ZIP SHA-256: f585ec7dd2edf0723cd0b2cdd6bf5399a3626518a9ea0ef3b306b4e2bf66b061
- results SHA-256: a05099d4e7b4443c2a7ec083d22095179b61385e690a2a834c2ce69983f3c5f0
- scientific payload SHA-256: dbfe3cd1221b2d1cd63d3dd44bf5d8f96796a76f9b03a4b4075bc8391d577824

## 1. Evaluator history

Module B v1 executed once but contained a regex-escaping implementation defect that made the B_INTERNAL_CANCELLATION detector incapable of matching del/mdel elements.

The defect was identified because v1 returned zero cancellation branches while Module A had already established, before Module B, the source witness:

- sga-add sID c57-0020__main__d4e4257;
- internal <mdel>or</mdel>.

EVALUATOR_REPAIR_v2.md froze the repair before v2 execution. No branch type, source, population, interface, denominator or success rule changed.

The v1 raw output is retained. Metrics depending on cancellation detection are not authoritative.

## 2. Population

All 493 C18 apparatus units were evaluated.

Source-scope state:
- NO_TEXT: 24
- OUTSIDE encoded addition: 376
- MIXED inside/outside within one app: 64
- INSIDE encoded addition: 29

Pinned raw manuscript source contains 112 encoded addition spans.

## 3. Source-triggered branch distribution

Under the frozen branch grammar:

- B_SCOPE_ONLY: 82 checkpoints; 103 unique source scopes
- B_PREDECESSOR: 6 checkpoints; 5 unique source scopes
- B_INTERNAL_CANCELLATION: 5 checkpoints; 4 unique source scopes

The branch grammar therefore produces multiple nondegenerate continuation states across the source.

Checkpoint counts are not treated as independent historical replications. Several checkpoints can share one source addition.

## 4. Current-answer equivalence versus continuation state

Three byte-identical local-app equivalence classes, containing six checkpoints total, preserve the same current normalized collation answer while corresponding to different source-grounded continuation states.

This reproduces the bounded Module A local-interface separation at the richer branch/state level.

The local checkpoint excludes:
- global app ordinal;
- neighboring apparatus units;
- inherited open-scope state;
- original-object handle;
- lawful source reopening.

The whole source object is not claimed to be ambiguous.

## 5. Interface comparison

### I_SOURCE_LINKED

Pinned source locator plus lawful reopening:

- exact continuation state: 493 / 493
- Q0 alignment preserved: 493 / 493

Implemented cold-source footprint:
- apparatus file: 235,462 bytes
- raw manuscript source: 47,854 bytes
- all serialized version-bound locator payloads: 69,021 bytes

These are implementation costs, not minimum information bounds.

### I_SCOPE_STATE

Local app plus inherited open-scope state, with source relation lookup by discovered scope identity:

- exact continuation state: 493 / 493
- Q0 alignment preserved: 493 / 493
- inherited-state payload across 493 checkpoints: 7,135 canonical JSON bytes
- construction requires a prior full-stream scan

This is an explicit retained-state representation, not free decoder knowledge or a global minimal carrier.

### I_LOCAL_ONLY

Conservative local policy:
- exact full continuation state: 24 / 493
- branch true positives: 3
- branch false positives: 0
- branch false negatives: 90
- precision: 1.0
- recall: 0.03225806451612903

The policy emits an internal-cancellation branch only when the cancellation is directly visible locally and never infers OUTSIDE merely because inherited state is absent.

The 24 exact states are not interpreted as evidence that the other 469 local states are wrong; the local policy safely leaves most continuation fields unresolved.

## 6. Matched locator controls

Across every member of the three byte-identical / continuation-different classes:

- tested: 6
- correct fixed-width locator exact: 6 / 6
- equal-byte wrong locator fails: 6 / 6
- current Q0 answers remain the same: 6 / 6
- locator byte length is matched

Thus the successful source-linked route depends on the correct binding, not merely on the presence of a locator-shaped field.

## 7. Selective research-state refinement

The initialized continuation state contains:
- insertion_scope = UNRESOLVED
- predecessor_relation = NOT_ASSESSED
- internal_cancellation = NOT_ASSESSED

After lawful source inspection:
- insertion_scope is resolved at all 493 checkpoints;
- predecessor status is assessed at 93 checkpoints where encoded addition scope is present;
- cancellation status is assessed at the same 93 checkpoints;
- Q0 alignment is unchanged at all 493 checkpoints.

This supports selective state refinement under the declared source contract.

It does NOT establish selective belief revision. No previously warranted substantive historical conclusion was reversed. UNRESOLVED/NOT_ASSESSED becoming resolved is refinement, not a belief-change result.

## 8. Scientific disposition

MODULE_B_BRANCHING_OBSERVED = YES

LOCAL_CURRENT_EQUIVALENCE_CONTINUATION_SEPARATION = YES

SOURCE_LINKED_BRANCH_RECOVERY = 493/493

SCOPE_STATE_BRANCH_RECOVERY = 493/493

LOCAL_ONLY_EXACT_CONTINUATION = 24/493

SELECTIVE_STATE_UPDATE = YES, AS STATE REFINEMENT

AUTONOMOUS_QUESTION_DISCOVERY = NOT TESTED

SELECTIVE_BELIEF_REVISION = NOT ESTABLISHED

INDEPENDENT_TRANSFER = NOT TESTED

## 9. Interpretation

The development result supports the following bounded statement:

> A representation that is complete for the current local collation comparison can fail to expose which source-grounded follow-up inquiry is licensed at that checkpoint. Retained inherited state or ordinary provenance-linked source reopening restores the continuation state exactly on this finite C18 population.

The result does not establish:
- failure of the Frankenstein Variorum infrastructure;
- a repair advantage over ordinary source navigation;
- autonomous scholarly question generation;
- a new theory of truth maintenance;
- long-horizon sustained discovery;
- independent cross-corpus replication.

The important null remains positive for the upstream system: ordinary source-linked recovery fully solves this Module B task.

## 10. Next obligation

The next experiment should not repeat scope recovery.

It should move to a distinct continuation trigger where the current task remains equivalent but epistemic/status information changes which evidence should be inspected next. A suitable development pressure test is the already-exposed Whitman relation inventory, where endpoint recovery can remain unchanged while encoded certainty differs.

That next study remains development unless a genuinely unexposed source group is identified and frozen.
