# Oxford MMOL transfer selection / exposure freeze v1

Date frozen: 2026-09-28
Status: PRE-OUTCOME COLLECTION-LEVEL TRANSFER SELECTION

## External infrastructure

Repository:
`Digital-Scholarship-Oxford/enabling-digital-research`

Pinned commit:
`7763fe63b51fd20ddb29a546e8af960641785ed1`

The upstream project converts TEI manuscript-catalogue data into configurable tabular outputs for cross-comparison and accessibility. This project has not previously been used in claim-relative-representation experiments.

## Selection rule

Selection uses repository paths and file metadata only.

- DEVELOPMENT collection: lexicographically first collection directory observed in the pinned tree with XML files: `collections/Add_A`.
- PROSPECTIVE TRANSFER collection: lexicographically next distinct collection directory observed in the pinned tree with XML files: `collections/Auct_B`.

The transfer collection is fixed before its XML contents or its corresponding tabular rows are inspected.

## Frozen transfer files

`collections/Auct_B` contains exactly three XML files in the pinned directory listing:

1. `MS_Auct_B_subtus_4.xml`
   - blob `0299f8e0cfc774cb01ae4fa11b8ecee832e31c36`
   - 18,397 bytes

2. `MS_Auct_B_subtus_5.xml`
   - blob `e9add37740d2c24885e7179bff82e52186bb26a9`
   - 18,473 bytes

3. `MS_Auct_B_subtus_6.xml`
   - blob `827c24bc1b659ac726be2c00c167236c14d8816c`
   - 18,483 bytes

All three remain in the denominator after opening.

## Exposure ledger at freeze

Already inspected before this freeze:

- external repository README;
- processor configuration documentation;
- filenames, blobs and file sizes in the collection tree;
- names/blobs/sizes of the eleven collection CSV configuration files;
- names/blobs/sizes of the generated collection CSV outputs;
- contents of `tabular_data/config/collection/05_contents.csv`, `08_origins.csv`, and portions of `00_overview.csv`;
- relevant processor/helper implementation, including collection sorting.

Not inspected before this freeze:

- XML content of any `collections/Auct_B/*.xml` file;
- any `05_contents.csv` row identified as belonging to Auct_B;
- Auct_B nested-`msItem` counts or hierarchy outcomes;
- Auct_B parent-recovery results under any interface.

Development collection `Add_A` may now be opened and used to debug/choose the precise decoder within the already declared mechanism family.

## Mechanism family fixed before transfer opening

Candidate continuation task:

Given a content/item record that is adequate for the current tabular cross-comparison task, recover the item's immediate parent `msItem` relation when the source TEI encodes nested `msItem` structure.

The purpose is to test:

[
full/native hierarchy preservation
quad vs quad
consumer-facing row exposure
]

with strong baselines:
- full generated contents table;
- single generated contents row;
- version-pinned source reopening.

The development phase must determine whether the full table can reconstruct parenthood from retained order/UID/nest-level carriers. A successful full-table reconstruction is a valid null against a stronger loss claim.

## Eligibility

After transfer opening, an Auct_B source item is eligible only if:
- it is a TEI `msItem`;
- it has an immediate ancestor `msItem`.

Eligibility depends only on native source structure, not on whether any tested interface succeeds.

If zero eligible items exist, the transfer outcome is `SUPPORT_STOP_ZERO_ELIGIBLE_NESTED_ITEMS`; no replacement collection may be selected under this freeze.

## Anti-tuning

After Auct_B contents are opened:
- no file may be dropped;
- the parent relation may not be replaced with an easier relation;
- a new column may not be added to the upstream table;
- source reopening remains a fully credited comparator;
- null, exact reconstruction, ambiguity and malformed/missing rows are all retained.

Development findings from Add_A do not count as independent transfer evidence.
