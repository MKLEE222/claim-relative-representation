# Oxford MMOL Add_A parent-continuation development results v2

Date: 2026-09-28
Status: DEVELOPMENT ONLY. Auct_B remained unopened through this analysis.
GitHub Actions run: 36373707087
Artifact: oxford-mmol-parent-continuation-add-a-dev-v2
Artifact ID: 10949694183
Artifact ZIP SHA-256: ad196dc53052fad304968a1728e261f0dbbc52b7e3b9af476e2129a6a743d957
results SHA-256: 496f800f1d8e27e6a4fa0d3aff90d227ccdce1dd95c373b8630161924209ae01

## 1. Evaluator repair retained

Development v1 incorrectly equated the upstream XPath

`count(preceding::tei:msItem) + 1`

with simple document-order ordinal.

Because the XPath `preceding::` axis excludes ancestors, nested `msItem` elements can receive duplicated/gapped upstream item UIDs.

Development v2:
- reproduces upstream UID semantics exactly;
- aligns source items to rows without using parent identity or nest level;
- uses unique source-local item IDs first;
- otherwise uses a parent/depth-free fingerprint of already-published current-row fields;
- uses actual published within-file row order plus exported nest level for the FILE_TABLE decoder.

The first development run is not interpreted scientifically.

## 2. Population

Frozen development selector:
first 20 Add_A XML files in lexicographic path order.

Observed:
- native `msItem` elements: 49;
- native nested `msItem` elements: 8;
- source items uniquely aligned to published rows: 46 / 49;
- all eight nested source items were uniquely aligned;
- source versus published nest level: 46 / 46 exact among aligned items.

All eight nested items occur in `MS_Add_A_166.xml`.

## 3. Upstream UID diagnostic

In `MS_Add_A_166.xml`, both source-reproduced and published table UIDs contain exactly three duplicated UID classes:

- `MS_Add_A_166_item_1`: 2 rows;
- `MS_Add_A_166_item_6`: 2 rows;
- `MS_Add_A_166_item_7`: 2 rows.

Thus the configuration's nominal item UID is not globally unique within this nested source file.

This is a development carrier diagnostic, not by itself a claim that the published table is unusable.

## 4. Parent-continuation results

All eight native nested items remain in the denominator.

### SINGLE_ROW

- exact: 0 / 8;
- UNKNOWN: 8 / 8;
- informative wrong: 0.

The upstream row exposes nest level, but no explicit immediate-parent row key. The safe decoder abstains.

### SOURCE_LINKED

- exact: 8 / 8;
- UNKNOWN: 0;
- wrong: 0.

Pinned source reopening directly recovers the TEI ancestor relation.

### FILE_TABLE

- exact: 5 / 8;
- UNKNOWN: 3 / 8;
- wrong: 0.

The full-table stack using only published row order + nest level identifies a parent row for the nested items. Five parent rows can be independently aligned to the native parent source item and pass exactly.

For three children:
- source-msItem-7;
- source-msItem-8;
- source-msItem-11;

the source parent is source-msItem-6. The predicted parent row cannot be independently aligned to that source item under the frozen parent/depth-free alignment rule, so these are retained as UNKNOWN rather than silently repaired with source order.

The stack itself reported no malformed-depth problem.

## 5. Development interpretation

Two distinct carrier facts coexist:

1. Local row exposure is insufficient for this parent continuation under the safe decoder.
2. The full published table distributes hierarchy information across row order and nest-level columns and restores 5 / 8 source-verified parent relations without source reopening.
3. Ordinary pinned-source reopening restores 8 / 8.

Therefore the development result does **not** support a binary “tabularization destroys hierarchy” claim.

It supports testing the more precise transfer hypothesis:

[
local row exposure
<
global distributed table carriers
le
source	ext{-}linked recovery
]

where the first inequality concerns the observed development capability, not a universal scalar ranking.

The full-table UNKNOWN cases also show why evaluation must separate:
- representation insufficiency;
- source-row identity ambiguity;
- safe abstention.

## 6. Transfer consequence

The prospective Auct_B protocol will freeze this exact decoder family before opening Auct_B:

- source-row alignment without parent/depth;
- SINGLE_ROW safe abstention;
- FILE_TABLE row-order + nest-level stack;
- SOURCE_LINKED direct source ancestry;
- no use of UID suffix as source order;
- all nested source items retained;
- alignment ambiguity reported separately;
- UID duplication retained as diagnostic.

No transfer criterion is changed to target a favorable outcome.
