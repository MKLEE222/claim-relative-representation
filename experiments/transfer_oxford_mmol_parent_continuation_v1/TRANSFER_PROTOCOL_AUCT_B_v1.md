# Oxford MMOL Auct_B prospective parent-continuation transfer protocol v1

Date frozen: 2026-09-28
Status: PRE-OUTCOME TRANSFER PROTOCOL; Auct_B CONTENT STILL UNOPENED AT FREEZE.

Parent documents:
- SELECTION_FREEZE.md
- DEVELOPMENT_PROTOCOL.md
- DEVELOPMENT_EVALUATOR_REPAIR_v1.md
- DEVELOPMENT_RESULTS_v2.md

## 1. Transfer question

Does a second, previously unused scholarly infrastructure reproduce the Frankenstein development distinction between:

- a consumer unit that can expose a continuation need;
- globally distributed carriers that may or may not resolve it;
- ordinary source/provenance reopening that may restore the relation?

The external infrastructure is the Oxford MMOL TEI-to-tabular processor.

The registered relation is the immediate parent relation among nested TEI `msItem` elements.

This relation was fixed from Add_A development before any Auct_B XML or corresponding Auct_B output row was opened.

## 2. Pinned external state

Repository:
`Digital-Scholarship-Oxford/enabling-digital-research`

Commit:
`7763fe63b51fd20ddb29a546e8af960641785ed1`

Published consumer table:
`tabular_data/output/collection/csv/05_contents.csv`

Blob:
`3b67d46018404f84b9f1440e126d1a17dd6c466d`

Prospective transfer collection:
`collections/Auct_B`

Frozen files:

1. `MS_Auct_B_subtus_4.xml`
   - blob `0299f8e0cfc774cb01ae4fa11b8ecee832e31c36`

2. `MS_Auct_B_subtus_5.xml`
   - blob `e9add37740d2c24885e7179bff82e52186bb26a9`

3. `MS_Auct_B_subtus_6.xml`
   - blob `827c24bc1b659ac726be2c00c167236c14d8816c`

All three remain in the denominator.

## 3. Native reference population

For every source file:

1. enumerate every TEI `msItem` in document order;
2. record source-local identity:
   `{TEI root xml:id}::source-msItem-{1-based document-order ordinal}`;
3. record direct parent source identity, if the immediate ancestor is `msItem`;
4. record native nesting depth;
5. reproduce the upstream nominal item UID exactly using:
   `count(preceding::tei:msItem) + 1`.

Every source item with a direct parent `msItem` is a nested-item continuation case.

No nested item is removed because an interface later fails.

If the three frozen files contain zero nested items:

`TRANSFER_SUPPORT_STOP_ZERO_ELIGIBLE_NESTED_ITEMS`

and no replacement collection is selected under v1.

## 4. Source-row alignment

Alignment is evaluation/support infrastructure and may not use:
- parent identity;
- native nesting depth;
- the FILE_TABLE predicted parent.

Frozen alignment order:

### A. ITEM_ID
Use `file URL + item ID` only when:
- source `msItem/@xml:id` is nonempty;
- the value uniquely identifies one source item in the file;
- the corresponding published row value uniquely identifies one row.

### B. CURRENT_ROW_FINGERPRINT
For still-unmapped source items, use the exact tuple:

- upstream nominal item UID;
- item n;
- direct title text;
- direct locus text;
- direct locus @from;
- direct locus @to.

The tuple must be unique among remaining source items and remaining published rows.

Otherwise:
`ALIGNMENT_UNRESOLVED`.

No source-order assumption is used to align rows.

## 5. Continuation trigger

For every aligned source item, compare:

Native trigger:
[
TRIGGER_{source}=1
]
iff the item has a direct parent `msItem`.

Published-row trigger:
[
TRIGGER_{row}=1
]
iff exported `metadata: nest level > 1`.

Report:
- true positive;
- true negative;
- false positive;
- false negative;
- invalid/missing nest level.

This tests whether the local row exposes the *need* for parent-context continuation.

It does not yet resolve the parent.

## 6. Parent-resolution interfaces

Primary resolution population:
all native nested items.

Each case retains an alignment/support status.

### SINGLE_ROW

Input:
one published contents row.

If its row trigger is positive:
- output `PARENT_UNRESOLVED`.

No lookup table from row identity to registered parent is permitted.

This interface measures trigger without target resolution.

### FILE_TABLE

Input:
all published `05_contents` rows sharing the same `metadata: file URL`, in published table order.

Decoder frozen from Add_A development:

1. read exported nest level for each row;
2. maintain a stack of prior rows by depth;
3. for depth (d>1), predict the nearest still-open prior row at (d-1);
4. map the predicted parent row back to a source item only through the parent/depth-free alignment registry defined above.

Outcomes:
- EXACT;
- WRONG;
- UNKNOWN if depth/context is malformed or predicted row has no unique source alignment.

The decoder may not use nominal item-UID numeric suffix as source order.

### SOURCE_LINKED

Input:
selected published row plus its frozen version/source-file route.

1. align the selected row to the source item using the same parent/depth-free alignment rule;
2. reopen the pinned TEI source;
3. return the direct parent `msItem` source identity.

Outcomes:
- EXACT;
- WRONG;
- UNKNOWN if the selected row cannot be uniquely aligned to its source item.

Source reopening is an ordinary provenance baseline and receives full credit.

## 7. Current-row preservation / row identity

For every aligned case retain:
- complete published row;
- row byte cost;
- source file bytes;
- same-file table row count and canonical serialized bytes.

This transfer does not claim that parent recovery is the upstream processor's design goal.

The current cross-comparison representation remains the published row itself.

## 8. Nominal UID diagnostic

Report, but do not use as the primary parent decoder:
- duplicate nominal item UIDs in the native source reproduction;
- duplicate nominal UIDs in the published rows;
- source/published duplicate-class agreement.

Development observed duplicates under nested structure because XPath `preceding::` excludes ancestors.

The transfer keeps both duplication and non-duplication outcomes.

## 9. Predeclared transfer dispositions

### TRANSFER_GLOBAL_PRESERVATION_LOCAL_EXPOSURE_SEPARATION

Requirements:
- at least one native nested item;
- all aligned nested rows expose the correct trigger;
- FILE_TABLE exactly resolves every nested case for which child and predicted parent rows are uniquely aligned;
- FILE_TABLE produces zero informative wrong parent;
- SOURCE_LINKED produces zero informative wrong parent and exactly resolves every nested case whose child row aligns;
- SINGLE_ROW exposes the continuation trigger but does not resolve a parent target.

Alignment-UNRESOLVED cases remain reported and limit coverage.

### TRANSFER_PARTIAL_GLOBAL_PRESERVATION

Requirements:
- at least one native nested item;
- FILE_TABLE yields a mixture of EXACT and UNKNOWN but no WRONG on aligned/evaluable cases;
- SOURCE_LINKED resolves more cases than FILE_TABLE without informative wrong outputs.

### TRANSFER_GLOBAL_REPRESENTATION_FAILURE

Any uniquely evaluable FILE_TABLE parent prediction is WRONG relative to native parenthood, or the row trigger has a source-verified false positive/negative.

This does not imply the source-linked system fails.

### TRANSFER_SOURCE_LINK_FAILURE

A uniquely aligned child row is source-linked to a WRONG parent, or reopening cannot recover a native parent despite successful child alignment.

### TRANSFER_SUPPORT_LIMITED

Nested source items exist but alignment support is too weak to yield any uniquely evaluable parent case.

No disposition implies prevalence outside the frozen Auct_B files.

## 10. Anti-tuning

After Auct_B is opened:

- no source file is dropped;
- no nested item is dropped from the denominator;
- no relation family is substituted;
- alignment fields/order are frozen;
- FILE_TABLE stack decoder is frozen;
- UID suffix may not be reintroduced as an ordering oracle;
- source reopening remains in the comparison;
- UNKNOWN may not be converted to WRONG or EXACT post hoc;
- no extra table column is added;
- no LLM is used to rescue ambiguous cases.

Unexpected source structures are retained and may cause support-limited outcomes.

## 11. Claim ceiling

A positive transfer can support only a bounded cross-object mechanism:

> In two independently designed scholarly infrastructures, complete/global representations can preserve continuation-relevant relations that are not self-contained in a local consumer unit; distributed carriers or lawful source reopening can restore some or all of that continuation context.

It does not establish:
- all tabular interfaces behave this way;
- user-facing discovery performance;
- arbitrary future-task sufficiency;
- long-horizon warranted discovery;
- algorithmic novelty;
- superiority to ordinary provenance/navigation;
- population prevalence across Oxford manuscripts.
