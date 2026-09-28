# Oxford MMOL structurally eligible prospective transfer protocol v2

Date frozen: 2026-09-28
Status: PRE-SELECTION / PRE-OUTCOME PROTOCOL.

This protocol is frozen after the Auct_B v1 support stop and before source-structure scanning of any collection after Auct_B.

## 1. Purpose

V1 failed only because the filename-selected Auct_B collection contained zero nested `msItem` cases.

V2 changes only the support-feasibility selector.

The scientific relation, source-row alignment, trigger definition, consumer interfaces and transfer dispositions are inherited from `TRANSFER_PROTOCOL_AUCT_B_v1.md`.

No new representation field or easier relation is introduced.

## 2. Candidate universe

External repository:
`Digital-Scholarship-Oxford/enabling-digital-research`

Pinned commit:
`7763fe63b51fd20ddb29a546e8af960641785ed1`

Candidate collection directories:
all first-level directories under `collections/` containing XML files, ordered lexicographically, strictly after `Auct_B`.

Previously used collections are excluded:
- `Add_A` development;
- `Auct_B` v1 support stop.

## 3. Structural eligibility selector

Candidate collections are inspected in lexicographic order.

During selection, the selector may inspect ONLY:
- pinned XML bytes/blobs;
- TEI element names;
- the number of `msItem` elements;
- whether each `msItem` has an ancestor `msItem`;
- file path/blob/byte size.

It must NOT inspect or record:
- titles;
- loci;
- item IDs;
- item n;
- persons/works;
- parent-recovery outcomes in the tabular table;
- any row from `05_contents.csv`;
- UID duplication outcomes;
- table nest levels.

A collection is eligible iff:
- it contains at least 5 native nested `msItem` elements in total; and
- nested items occur in at least 2 distinct XML files.

Select the first eligible collection and stop scanning later collections.

All XML files in the selected collection form the transfer source denominator, including files with zero nested items.

If no eligible collection exists:
`V2_SUPPORT_STOP_NO_ELIGIBLE_COLLECTION`.

## 4. Selection audit

Before the tabular table is opened for the selected collection, write a selection manifest containing:
- pinned commit;
- ordered candidate collections scanned;
- per candidate: XML file count, files scanned until decision, total msItems inspected, nested msItems, files with nested items;
- selected collection;
- complete selected XML path/blob/size list;
- SHA-256 of the manifest.

Rejected candidate collections remain recorded.

## 5. Reference and alignment

After structural selection is complete, execute the same reference/alignment rules frozen in v1.

Native identity:
`{root xml:id}::source-msItem-{document-order ordinal}`.

Parent relation:
direct ancestor `msItem`.

Source-row alignment may not use parent or depth:

1. unique `file URL + item ID`;
2. otherwise unique tuple:
   - upstream nominal item UID under exact `preceding::msItem` semantics;
   - item n;
   - direct title;
   - direct locus text;
   - direct locus from;
   - direct locus to;
3. otherwise ALIGNMENT_UNRESOLVED.

No source-order assumption is used for alignment.

## 6. Continuation trigger

For every aligned source item:

- native trigger = 1 iff direct parent `msItem` exists;
- row trigger = 1 iff published `metadata: nest level > 1`.

Report TP/TN/FP/FN/invalid.

The local row can therefore expose a continuation *need* without necessarily exposing the parent target.

## 7. Resolution interfaces

### SINGLE_ROW
If the row trigger is positive, parent target remains `PARENT_UNRESOLVED`.
No oracle lookup from row identity is permitted.

### FILE_TABLE
Input:
all published `05_contents` rows with the same `metadata: file URL`, in actual published order.

Frozen decoder:
- parse exported nest level;
- maintain stack by depth;
- predict nearest still-open prior row at depth d-1;
- map predicted row to source identity only through the frozen parent/depth-free alignment registry.

Outcomes: EXACT / WRONG / UNKNOWN.

The nominal UID suffix is not a source-order oracle.

### SOURCE_LINKED
Input:
selected row plus pinned source route.

Align the child row with the same frozen alignment rule, reopen the pinned TEI source, and return the direct parent source identity.

Outcomes: EXACT / WRONG / UNKNOWN.

## 8. Denominators and support

Report separately:
- all selected source files;
- all native msItems;
- all native nested items;
- child-aligned nested items;
- trigger-evaluable items;
- FILE_TABLE exact/wrong/unknown;
- SOURCE_LINKED exact/wrong/unknown;
- alignment-unresolved nested items.

No nested item is removed because an interface fails.

## 9. UID diagnostic

Report duplicate nominal item UID classes in native reproduction and published rows, but do not use those suffixes as ordering keys.

UID duplication is a carrier diagnostic, not the parent-resolution outcome.

## 10. Transfer dispositions

### V2_TRANSFER_GLOBAL_PRESERVATION_LOCAL_EXPOSURE_SEPARATION
- at least 5 native nested items in at least 2 source files;
- zero source-verified trigger FP/FN among aligned items;
- FILE_TABLE has at least one EXACT, zero WRONG, and zero UNKNOWN among child-aligned nested items;
- SOURCE_LINKED EXACT for every child-aligned nested item;
- SINGLE_ROW does not resolve a parent target.

### V2_TRANSFER_PARTIAL_GLOBAL_PRESERVATION
- support threshold met;
- zero trigger FP/FN among aligned items;
- FILE_TABLE has at least one EXACT and at least one UNKNOWN, zero WRONG;
- SOURCE_LINKED resolves strictly more aligned nested cases than FILE_TABLE and has zero WRONG.

### V2_TRANSFER_GLOBAL_REPRESENTATION_FAILURE
Any source-verified trigger FP/FN or any uniquely evaluable FILE_TABLE WRONG parent.

### V2_TRANSFER_SOURCE_LINK_FAILURE
Any uniquely aligned child row receives a WRONG parent under source reopening.

### V2_TRANSFER_SUPPORT_LIMITED
Support threshold met but alignment/evaluation yields no FILE_TABLE exact case, or other frozen conditions prevent the above dispositions without a wrong result.

## 11. Anti-tuning

After the structural selector begins scanning:
- eligibility threshold is fixed;
- candidate order is fixed;
- selected collection cannot be replaced because of table outcome;
- no relation family changes;
- no alignment-field changes;
- no decoder changes;
- no new output column;
- no LLM rescue;
- UNKNOWN remains UNKNOWN;
- source-linked reopening remains fully credited.

An implementation support stop before outcome exposure may be repaired only with an explicit pre-outcome memo and without changing scientific criteria.

## 12. Claim ceiling

A successful v2 transfer would support only a bounded cross-object continuation-carrier phenomenon.

It does not establish:
- arbitrary future-task sufficiency;
- human discovery;
- long-horizon warranted inquiry;
- algorithmic novelty;
- population prevalence;
- superiority to ordinary source/provenance navigation.
