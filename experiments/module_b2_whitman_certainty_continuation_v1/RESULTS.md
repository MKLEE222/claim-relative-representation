# Module B2 results — Whitman certainty-to-evidence continuation

Date: 2026-09-28
Status: EXECUTED DEVELOPMENT PRESSURE TEST ON AN ALREADY-EXPOSED RELATION INVENTORY. NOT INDEPENDENT TRANSFER.

Authoritative main execution:
- GitHub Actions run 36375605387
- artifact: module-b2-whitman-certainty-continuation-v1
- artifact ID: 10950183907
- artifact ZIP SHA-256: 58033e7bd1fb9ae99852299c544e680a313a0c1b85d4d9937d6db0c76c8d9662
- results SHA-256: a5b7eb30d1bdb7ead03c7ad309a77daebedd954f6c6523b2b487656bc32d60d3
- scientific payload SHA-256: 64aa4ae115d230d1a688fd20d0727e3348cbcb863ec4bd38ddc2f860585a7c8e

Authoritative contemporaneous source-route repair:
- GitHub Actions run 36375714615
- artifact: module-b2-whitman-source-route-v2
- artifact ID: 10950298784
- artifact ZIP SHA-256: 0d31f4cc60dfa3f1b319d35c0e7ed68630cb99ba027738b23ad3049741c018bb
- route-v2 results SHA-256: c2a6b382129eb8946e9f75366709b488c829f732844ee8fcab94befbe923a47f

## 1. Question

The prior X2B/X2C result already established:

    endpoint recoverability != certainty recoverability

Module B2 asks a stronger continuation question:

> If the current printed-locus -> manuscript endpoint answer and even the locus-level amount of uncertainty are preserved, is that sufficient to determine which concrete manuscript evidence should be inspected next?

The continuation rule is frozen:
- low-certainty links identify endpoints selected for additional source inspection;
- mixed-certainty loci license comparison between the high and low endpoint partitions.

This is a source-selection rule over the Archive's encoded certainty state. It is not an independent genetic judgement.

## 2. Population

Pinned relation object:
- 1,444 valid links
- 764 unique printed loci
- 508 high-certainty links
- 936 low-certainty links
- 251 high-only loci
- 393 low-only loci
- 120 mixed high/low loci

## 3. Current task remains identical

For every printed locus, Q0 is the complete set of:

    (manuscript_file, manuscript_local_locus)

All compared representations preserve Q0 at all 764 loci:

- native: 764/764
- endpoint-only: 764/764
- locus-status-only: 764/764
- explicit endpoint-cert ledger: 764/764
- native relation-file reopening: 764/764

Therefore the continuation comparison is not driven by current endpoint failure.

## 4. Continuation target

Under the frozen rule:
- 513 loci contain at least one low-certainty relation;
- they expose 936 low-certainty endpoint targets for source review;
- 120 loci are mixed-certainty;
- the mixed loci contain 449 endpoint targets whose high/low partition is part of the continuation state.

Native per-link certainty determines the continuation exactly at 764/764 loci.

Endpoint-only representation cannot determine certainty-sensitive continuation.

The stronger locus-status representation retains:
- all endpoints;
- high-link count;
- low-link count;
- HIGH_ONLY / LOW_ONLY / MIXED state.

It is exact on:
- all 251 high-only loci;
- all 393 low-only loci.

It remains binding-underdetermined on exactly:
- 120/120 mixed loci.

Thus:

    current endpoints + locus-level uncertainty profile
    != endpoint-specific uncertainty binding

and, under the frozen continuation rule:

    current endpoints + locus-level uncertainty profile
    != which concrete evidence should be inspected next.

## 5. Controlled mixed-locus separation

For every mixed locus:
1. choose the lexically first distinct high endpoint and low endpoint;
2. swap only their certainty labels.

Across all 120 mixed loci:

- endpoint set unchanged: 120/120
- high/low counts unchanged: 120/120
- MIXED status unchanged: 120/120
- complete R_LOCUS_STATUS_ONLY unchanged: 120/120
- endpoint-specific continuation target changed: 120/120

These are controlled certainty-binding twins, not naturally observed alternative editorial histories.

The result is a binding determinacy witness stronger than deleting certainty entirely: even preserving the amount and existence of uncertainty is insufficient when the task requires knowing which source relation carries it.

## 6. Binding repair and matched wrong control

The complete native endpoint -> cert mapping is functional on this frozen population; no endpoint carries conflicting cert values at the same printed locus.

Correct explicit binding ledger:
- exact continuation recovery: 764/764 loci
- canonical JSON bytes: 111,703

Wrong binding:
- on every mixed locus, use the same frozen high/low swap as the controlled twin;
- current endpoint output remains unchanged;
- locus-level high/low counts remain unchanged;
- serialized wrong ledger bytes: 111,703, exactly matching the correct ledger.

Result:
- wrong binding tested: 120 mixed loci
- wrong binding fails native continuation target: 120/120

Therefore the recovery is binding-specific rather than a benefit of merely adding a cert-shaped payload.

No global minimality claim follows.

## 7. Source-route audit and contract repair

Main v1 source-route execution initially sent every @corresp file to the contemporaneous manuscripts repository and obtained:
- 628 / 1,444 complete routes
- 816 unresolved

That contract was incomplete because the relation inventory includes manuscript OR notebook sources.

SOURCE_ROUTE_REPAIR_v2 froze a two-repository routing rule before the repaired audit:

### 2019 manuscript snapshot
- commit 249bc14594fa1c0428e7ca39f52753de21ce604b
- tree 1871715fbcef5f9721e80f385471a86ad52ef463

### 2019 notebook snapshot
- commit 682c04c0998739b8edfd75e0e7496592777e2898
- tree 90ce5a76b2358d3350e889b6988af8e26bcdd835

Among 151 distinct relation @corresp files:
- 130 route to manuscripts
- 12 route to notebooks
- 0 appear in both
- 9 appear in neither pinned tree

Under the repaired source contract:
- complete two-sided routes: 772 / 1,444
- unresolved routes: 672 / 1,444

By certainty:

Low:
- printed endpoint resolves: 927 / 936
- source file resolves: 916 / 936
- local manuscript/notebook ID resolves: 482 / 936
- complete two-sided route: 479 / 936

High:
- printed endpoint resolves: 506 / 508
- source file resolves: 507 / 508
- local manuscript/notebook ID resolves: 295 / 508
- complete two-sided route: 293 / 508

The remaining failures are dominated by local-ID mismatch/absence in the pinned 2019 source snapshots, not by relation-file endpoint loss.

This is a versioned source-route accessibility finding, not evidence that the Archive's encoded relation is historically false.

## 8. Scientific disposition

CURRENT_ENDPOINT_EQUIVALENCE = YES, 764/764

LOCUS_STATUS_CONTINUATION_SEPARATION = YES, 120/120 mixed loci

CORRECT_BINDING_RESTORES_CONTINUATION = YES, 764/764

WRONG_BINDING_FAILS = YES, 120/120 mixed loci

CONTEMPORANEOUS_SOURCE_ROUTE_EXECUTABLE_ALL_LINKS = NO, 772/1444 complete

AUTONOMOUS_QUESTION_GENERATION = NOT TESTED

HISTORICAL_GENETIC_TRUTH = NOT TESTED

INDEPENDENT_TRANSFER = NOT TESTED

## 9. Claim ceiling

Supported as development evidence:

> A representation can preserve the complete current endpoint answer and the locus-level amount of uncertainty while failing to determine which concrete evidence should be inspected next under an uncertainty-sensitive continuation rule. Endpoint-specific status binding or lawful reopening of the native relation object restores that target.

Not supported:
- low-certainty relations are false;
- every researcher should inspect low-certainty endpoints first;
- one specific cert field is universally necessary;
- this is an independent transfer;
- source-route incompleteness implies archive failure.

## 10. Relation to Module A/B

Frankenstein Module B showed:

    same current local comparison
    != same source-triggered continuation state

Whitman B2 shows a different mechanism:

    same current endpoints + same global uncertainty profile
    != same endpoint-specific evidence-selection continuation

Both are solved by richer lawful source/provenance access in their native ecology. Neither establishes that the upstream infrastructure is deficient.
