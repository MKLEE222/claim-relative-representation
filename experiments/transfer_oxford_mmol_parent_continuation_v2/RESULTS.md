# Oxford MMOL structurally selected prospective transfer v2 — results

Date: 2026-09-28
Status: EXECUTED PROSPECTIVE CROSS-OBJECT TRANSFER
GitHub Actions run: 36374060262
Artifact: oxford-mmol-structural-transfer-v2
Artifact ID: 10949957742
Artifact ZIP SHA-256: d6bc01a38ba4ded5d3e9acc493502e99c430e4db8641efbb42f5e3a48610f8fd
Selection-manifest payload SHA-256: 3d81058b93888e4ef983ccbf49eab70674d4a4e99c3dc6a6ac12532a30d94bb9
Transfer results SHA-256: 0e7d12b19ed52c610c9c24d7a7a6f5c32bdf7ffa66e4a880a4e582b6cc0373ed

## 1. Selection integrity

The v2 selector was frozen after the Auct_B zero-eligible support stop and before scanning any collection after Auct_B.

The selector could inspect only native TEI structure:
- file path/blob/size;
- number of msItem elements;
- whether each msItem has an ancestor msItem.

It could not inspect titles, loci, item IDs, table rows, exported nest levels, UID duplication, or parent-recovery outcomes.

Candidate collections were scanned lexicographically after Auct_B.

The first candidate, Auct_D, reached the frozen support threshold after the 25th scanned XML file:
- 85 msItems inspected at selection time;
- 22 nested msItems;
- nested items in 2 files.

The selector stopped immediately.

The complete Auct_D collection, not merely the 25 selection files, then became the transfer denominator:

- 118 XML files.

No later collection was inspected for outcome selection.

## 2. Complete transfer population

Across all 118 frozen Auct_D files:

- native msItems: 469;
- native nested msItems: 210;
- source items uniquely aligned to published rows without using parent/depth: 399 / 469;
- nested source items so aligned: 165 / 210;
- nested items with unresolved child-row alignment: 45 / 210.

Nested items occur in 26 of the 118 source files, so the effect is not confined to the two files that caused structural selection eligibility.

No native nested item is removed from the denominator because alignment or an interface later fails.

## 3. Continuation-trigger transfer

For uniquely aligned source items:

Native trigger:
`has direct parent msItem`.

Published-row trigger:
`metadata: nest level > 1`.

Observed:

- true positive: 165;
- true negative: 234;
- false positive: 0;
- false negative: 0;
- invalid nest-level trigger: 0.

Thus the local published row can expose that parent-context continuation is needed for all 165 aligned nested cases.

It does not thereby identify the parent target.

## 4. Parent resolution by interface

### SINGLE_ROW

For all 165 aligned nested cases:

- continuation trigger exposed: 165 / 165;
- parent target resolved: 0 / 165;
- safe `PARENT_UNRESOLVED`: 165 / 165;
- informative wrong parent: 0.

The local row is therefore not treated as if a unique row identifier secretly indexed a parent oracle.

### FILE_TABLE

Input:
all published 05_contents rows for the same `metadata: file URL`, in the actual published order.

Decoder:
published row order + exported nest-level stack only.

Results among 165 aligned nested cases:

- EXACT: 152 / 165;
- UNKNOWN: 13 / 165;
- WRONG: 0 / 165.

Conditional exact recovery among aligned nested cases:

[
152 / 165 = 92.12\%
]

The full-table decoder itself reported zero malformed-depth / missing-parent-depth stack problems.

The 13 UNKNOWN cases occur in only two source files:

- `MS_Auct_D_5_5.xml`: 8;
- `MS_Auct_D_inf_2_11.xml`: 5.

In all 13, the depth-stack identifies a parent *row*, but that predicted parent row cannot be mapped back to a unique native parent source item under the frozen parent/depth-free alignment registry.

Therefore these 13 cases are retained as identity-support uncertainty rather than converted into either EXACT or WRONG.

### SOURCE_LINKED

For every aligned nested child:

- EXACT: 165 / 165;
- UNKNOWN: 0;
- WRONG: 0.

Pinned TEI source reopening therefore restores every parent relation that has a uniquely aligned child row.

This ordinary provenance/source route receives full credit.

## 5. Alignment-support boundary

The remaining 45 / 210 native nested items have unresolved child-row alignment under the frozen evaluator.

Concentration:

- `MS_Auct_D_5_5.xml`: 23;
- `MS_Auct_D_inf_2_11.xml`: 10;
- `MS_Auct_D_4_7.xml`: 4;
- `MS_Auct_D_3_6.xml`: 3;
- `MS_Auct_D_2_16.xml`: 2;
- `MS_Auct_D_4_13.xml`: 2;
- `MS_Auct_D_5_10.xml`: 1.

These are not scored as parent-recovery errors.

They remain denominator-bearing support limitations because the registered alignment deliberately refuses to use parent identity, native depth, or source-order position as an evaluator oracle.

The observed coverage is therefore:

[
165 / 210 = 78.57\%
]

uniquely child-aligned under the frozen support contract.

The transfer claim must distinguish this support coverage from conditional FILE_TABLE accuracy.

## 6. UID carrier diagnostic

The exact upstream item-UID semantics were reproduced using XPath `preceding::tei:msItem`.

Across Auct_D:

- source-reproduced duplicate UID classes: 41;
- published duplicate UID classes: 41;
- excess duplicated rows: 43 in source reproduction and 43 in published output;
- affected files: 26.

The source and published duplicate-class counts agree.

This confirms that nominal item UID is not universally unique under nested msItem structure in this pinned representation.

The transfer decoder therefore correctly did not use UID suffix as a source-order oracle.

This diagnostic helps explain some identity-support ambiguity, but UID duplication alone is not treated as proof of parent-recovery failure.

## 7. File-level distribution

Native nested items occur in 26 source files.

Several large nested files are fully recoverable under FILE_TABLE among aligned cases, for example:

- MS_Auct_D_1_20: 18 / 18;
- MS_Auct_D_2_6: 29 / 29;
- MS_Auct_D_4_4: 16 / 16;
- MS_Auct_D_4_6: 31 / 31.

The two files containing all 13 FILE_TABLE UNKNOWN cases also carry the largest identity-alignment burdens:

- MS_Auct_D_5_5:
  - native nested = 34;
  - child alignment unresolved = 23;
  - aligned nested = 11;
  - FILE_TABLE exact = 3;
  - FILE_TABLE UNKNOWN = 8.

- MS_Auct_D_inf_2_11:
  - native nested = 21;
  - child alignment unresolved = 10;
  - aligned nested = 11;
  - FILE_TABLE exact = 6;
  - FILE_TABLE UNKNOWN = 5.

Thus the partial result is not caused by a stack decoder producing wrong hierarchy.

The limiting factor is source-row identity support under the deliberately strict evaluation contract.

## 8. Frozen disposition

Predeclared disposition:

`V2_TRANSFER_PARTIAL_GLOBAL_PRESERVATION`

The requirements are met:

- structural support threshold met;
- zero trigger false positive / false negative among aligned items;
- FILE_TABLE has both EXACT and UNKNOWN, with zero WRONG;
- SOURCE_LINKED resolves strictly more aligned nested cases than FILE_TABLE;
- SOURCE_LINKED has zero WRONG.

No criterion or decoder was changed after Auct_D outcomes were opened.

## 9. Cross-object scientific interpretation

Together with Frankenstein development, the prospective Oxford transfer now supports a bounded cross-object mechanism:

[
local continuation	ext{-}need exposure

eq
global continuation	ext{-}target recovery

eq
source	ext{-}linked recovery
]

Frankenstein:
- complete native pipeline retains the registered continuation state;
- downstream local projections expose only subsets;
- source/global context restores it.

Oxford:
- local tabular row exposes the need for parent context through nest level;
- the global table recovers 152 / 165 evaluable parents using distributed order+depth carriers;
- source reopening recovers 165 / 165 aligned parents;
- 45 / 210 nested items remain alignment-support unresolved.

This is not a pooled accuracy result and the two infrastructures do not instantiate identical relation semantics.

The shared observation is representational:

> continuation-relevant information may be globally retained or lawfully recoverable while not being self-contained in the consumer unit at which a current scholarly result is presented.

## 10. Claim ceiling

Supported:

- first prospective cross-object transfer of the continuation-carrier mechanism after the Frankenstein development mechanism was frozen;
- local trigger versus global target-recovery separation;
- substantial but partial distributed-carrier parent recovery;
- exact source-linked recovery on every uniquely aligned nested child;
- explicit support/alignment boundary rather than silently scoring unresolved cases as errors.

Not established:

- full global-table preservation;
- arbitrary future-task sufficiency;
- autonomous scholarly question generation;
- selective belief revision under real later evidence;
- long-horizon sustained warranted discovery;
- algorithmic novelty;
- human discovery performance;
- Oxford-wide or DH-wide prevalence;
- superiority to ordinary provenance/navigation.

The next mother-problem obligation is not another parent-recovery replication. It is to test whether representation retains **dependency provenance needed for selective revision when the current value itself is preserved**.
