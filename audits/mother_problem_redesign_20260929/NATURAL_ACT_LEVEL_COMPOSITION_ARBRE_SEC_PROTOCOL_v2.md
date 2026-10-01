# Natural act-level qualified composition protocol v2 — Arbre Sec replication

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-OUTCOME / EXISTING EXPOSED SOURCE EVIDENCE ONLY.

## 1. Purpose

Replicate target-bound qualified composition at the intervention-act level using a second
page-verified historical sequence whose relations come from a different pre-existing source-native
relation family.

The sequence is:

    ARBR-ID-1903
    -> ARBR-ID-HS
    -> ARBR-REPLY-CORDIER

No fresh source is opened.

## 2. Frozen source assets

Git blobs:

    data/r3_verified_proposition_panel_v1.csv
    f1ffa2aefde17f731fc9d0a19781aed81c94622c

    experiments/deepening_v1/r3_pass1_B02_entry_labels_v1.csv
    c65e84425e0410f0e70531f09027e3d357d06ed7

    experiments/deepening_v1/R3_ACT_SEGMENTATION_PROTOCOL.md
    00274d41e18506de5e2504e94d07536baf9ab170

The proposition-panel rows used here are PAGE_VERIFIED_BOTH.

The pass-1 entry note predates this composition experiment and states that the Houtum-Schindler
identification is followed by Cordier's response; the acts are to be separated.

## 3. Frozen proposition sequence

### ARBR-ID-1903

Actor:

    EARLIER_EDITORIAL_NOTE

Relation:

    BASE_POSITION

Normalized current claim:

    claim_id = ARBR-ID-1903
    target = arbre-sec-identification
    value = ORIENTAL_PLANE_CHINAR
    status = ASSERTED

### ARBR-ID-HS

Actor:

    HOUTUM_SCHINDLER

Mediator:

    CORDIER

Relation to target:

    COMPETING_IDENTIFICATION

Target proposition:

    ARBR-ID-1903

Normalized proposal:

    claim_id = ARBR-ID-HS
    value = CYPRESS_OF_ZOROASTER
    status = ASSERTED_PROPOSAL

### ARBR-REPLY-CORDIER

Actor:

    CORDIER

Relation to target:

    BIBLIOGRAPHIC_REPLY

Target proposition:

    ARBR-ID-HS

Source interpretation already frozen:

    Cordier replies that he had read the earlier Schindler paper and points back to a genuine
    third-edition citation; explicit adoption of the cypress proposal is not established.

Therefore this act does not mutate the identification assertion set.

It is a first-class:

    RECORD_EVIDENCE

action bound to ARBR-ID-HS.

## 4. Source-native relation extension

The v2 target-bound qualification interface accepts relations that were frozen in either:

A. earlier/later contrast assets; or
B. proposition-to-proposition source-native panel relations.

This replication registers:

    COMPETING_IDENTIFICATION
    BIBLIOGRAPHIC_REPLY

These labels are not derived from generator outcomes.

### COMPETING_IDENTIFICATION

Require:

    relation_target_claim_id is live.

If the proposed value differs from the target claim value:

    ADD_ALTERNATIVE

otherwise:

    relation-state mismatch.

### BIBLIOGRAPHIC_REPLY

Require:

    relation_target_claim_id is live.

Then:

    RECORD_EVIDENCE

No assertion mutation is authorized.

The event must retain:
- relation target;
- evidence/provenance;
- actor/mediator;
- source binding.

## 5. Natural forward composition

Initial:

    S0 = {ARBR-ID-1903}

Step 1:

    e1 = ARBR-ID-HS
    relation = COMPETING_IDENTIFICATION
    target = ARBR-ID-1903

Required:

    Q(S0,e1) = ADD_ALTERNATIVE

yielding:

    S1 = {ARBR-ID-1903, ARBR-ID-HS}

Step 2:

    e2 = ARBR-REPLY-CORDIER
    relation = BIBLIOGRAPHIC_REPLY
    target = ARBR-ID-HS

Required:

    Q(S1,e2) = RECORD_EVIDENCE

and:

    Psi(S1) = Psi(S2)

while:

    Xi(S1) != Xi(S2)

The registered generator sequence is:

    ADD_ALTERNATIVE ; RECORD_EVIDENCE

## 6. Reverse-order qualification

Attempt the Cordier reply at S0 before ARBR-ID-HS exists.

Required:

    qualified = false
    reason = RELATION_TARGET_NOT_LIVE

and:

    Psi unchanged
    Xi unchanged

Thus the reply action is enabled by the existence of the earlier competing-identification act.

## 7. Cross-sequence portability

The v2 target-bound engine must also rerun the Paper Money sequence without changing its frozen
source interpretation:

    PM02 -> ADD_ALTERNATIVE
    PM03 -> RESOLVE

with:
- relation-target binding;
- correction-history binding;
- reverse PM03 rejection;
- history ablation rejection.

The same engine implementation must handle both sequences.

No case-specific branch may inspect:
- event id;
- episode name;
- claim id prefix.

Qualification may inspect only:
- current state;
- registered relation type;
- relation target identity;
- retained transition history;
- evidence/proposal fields.

## 8. Independent implementations

Implement:

    target_bound_oracle_v2
    target_bound_runtime_v2

The two implementations must be independent.

They must agree on:
- qualification;
- generator;
- relation target;
- before/after Psi;
- before/after Xi;
- final state;
- rejection reasons.

## 9. Required result

NATURAL_ACT_COMPOSITION_REPLICATION_PASS only if:

### Paper Money

- forward = ADD_ALTERNATIVE ; RESOLVE;
- reverse PM03 = RELATION_TARGET_NOT_LIVE;
- history-ablated PM03 = RELATION_TARGET_HISTORY_UNRESOLVED.

### Arbre Sec

- forward = ADD_ALTERNATIVE ; RECORD_EVIDENCE;
- reverse Cordier reply = RELATION_TARGET_NOT_LIVE;
- reply preserves Psi;
- reply changes Xi.

### Shared

- operation absent from all event inputs;
- source rows found exactly once;
- source verification authorities match frozen values;
- oracle/runtime exact;
- no event-id or episode-specific branch exists in qualification code.

## 10. Claim ceiling

If passed:

> Target-bound qualified composition replicates at act level in a second page-verified sequence
> and across a second source-native relation family. A competing identification enables a later
> bibliographic reply that is not available before the proposal exists; the reply changes
> retained scholarly history without changing current identification assertions.

Not licensed:
- prevalence;
- automatic relation extraction;
- universal relation vocabulary;
- universal composition algebra.
