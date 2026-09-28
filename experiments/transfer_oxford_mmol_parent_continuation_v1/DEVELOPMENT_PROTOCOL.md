# Oxford MMOL parent-continuation development protocol v1

Date frozen: 2026-09-28
Status: DEVELOPMENT ON Add_A ONLY. Auct_B remains unopened prospective transfer under SELECTION_FREEZE.md.

## 1. Native object and published consumer representation

External repository:
`Digital-Scholarship-Oxford/enabling-digital-research`

Pinned commit:
`7763fe63b51fd20ddb29a546e8af960641785ed1`

Native source:
TEI manuscript-catalogue XML.

Consumer representation:
the upstream published `tabular_data/output/collection/csv/05_contents.csv`, configured so each row corresponds to one `msItem`.

The upstream configuration explicitly exports:
- item UID;
- item ID;
- file URL;
- manuscript identifiers;
- part ID;
- nest level;
- locus and work/content fields.

It does not define a dedicated parent-msItem column.

## 2. Development selector

Use the first 20 XML paths in lexicographic order under `collections/Add_A` at the pinned tree.

Selection is filename/metadata based, not source-content based.

If none contains a nested `msItem`, the development result is a support stop. Do not enlarge the development set within v1 after observing that outcome.

## 3. Reference parent relation

For every selected source file:
1. enumerate all TEI `msItem` elements in document order;
2. reproduce the upstream item UID:
   `{msID}_item_{1-based document-order msItem ordinal}`;
3. for every item with an immediate ancestor `msItem`, record the parent item UID.

An item is eligible iff it has an immediate parent `msItem`.

No literary interpretation is involved.

## 4. Current task

The registered current output is the upstream published contents row for an item.

A parent-continuation test is interpreted only when:
- the source-derived item UID matches exactly one published contents row;
- the row's exported nest level agrees with the source nesting depth.

Missing/duplicate/mismatched rows remain in the report and are not assigned an artificial zero.

## 5. Continuation task

For an eligible nested content item:

> Which immediate parent content item contains this item?

Required output:
the exact parent item UID.

Diagnostic extension:
after identifying the parent UID, recover the parent row's exported work title when present. Title is not needed for the parent-ID pass/fail criterion.

## 6. Interfaces

### SINGLE_ROW

Input:
only the selected published `05_contents` row.

Decoder:
- if nest level = 1: parent = NONE;
- if nest level > 1: UNKNOWN.

A unique item UID is not treated as an oracle lookup table.

### FILE_TABLE

Input:
all published `05_contents` rows sharing the same `metadata: file URL`.

Decoder:
1. parse the document-order ordinal from `metadata: item UID`;
2. sort rows by that ordinal;
3. parse `metadata: nest level`;
4. use a stack of earlier rows by depth;
5. for depth d>1, return the nearest previous row at depth d-1 that remains open under the stack reconstruction.

No source XML, item title semantics or registered parent answer may be read by this decoder.

### SOURCE_LINKED

Input:
selected row plus the pinned TEI source file identified through the development source registry.

Decoder:
locate the row's source item by the same item UID ordinal and return the direct ancestor `msItem` UID.

This is the strong ordinary provenance/source-reopening baseline.

## 7. Metrics

Report:
- selected source files;
- total native msItems;
- eligible nested msItems;
- exact unique row matches;
- source/table nest-level agreement;
- SINGLE_ROW exact / UNKNOWN / wrong;
- FILE_TABLE exact / UNKNOWN / wrong;
- SOURCE_LINKED exact / UNKNOWN / wrong;
- parent-title recovery after correct parent UID;
- file-table row count and serialized byte count;
- selected-row serialized byte count;
- source-file bytes.

Also report all full-table decoder failure modes:
- malformed item UID ordinal;
- invalid nest level;
- depth jump >1;
- missing predecessor at depth d-1;
- duplicate source-order ordinal.

## 8. Anti-tautology / claim boundary

The experiment does not claim:
- the table is deficient merely because a row is not self-contained;
- parenthood is semantically novel;
- source reopening is a new algorithm;
- parent reconstruction from item UID/nest level is theoretically deep.

The transfer-relevant question is whether a different mature scholarly transformation reproduces the Frankenstein pattern:

[
full/global representation retains continuation carrier
quad	ext{while}quad
local consumer unit exposes less
]

A full-table exact result is a positive preservation result and must receive full credit.

A source-linked exact result weakens any claim of practical irrecoverability.

## 9. Transfer status

Add_A results are development only.

Auct_B remains the prospective transfer population already frozen by path and blobs. Its contents and corresponding rows must not be inspected until a post-development transfer protocol is committed.
