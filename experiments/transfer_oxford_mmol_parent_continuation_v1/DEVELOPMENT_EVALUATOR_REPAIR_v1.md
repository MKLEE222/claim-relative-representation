# Add_A development evaluator repair v1

Date: 2026-09-28
Status: DEVELOPMENT-ONLY MEASUREMENT REPAIR BEFORE Auct_B OPENING

## Trigger

The first Add_A development run completed and revealed:
- 8 native nested msItems;
- only 2 passed the strict row-match + nest-level gate;
- 4 appeared to have non-unique/missing item-UID row matches;
- 2 showed apparent source/table nest-level mismatch.

Inspection of the already-exposed development source `MS_Add_A_166.xml` and the frozen upstream config identified an evaluator error.

The development script incorrectly reproduced the upstream `metadata: item UID` as a simple 1-based document-order ordinal.

The upstream XPath is:

`count($i/preceding::tei:msItem) + 1`

XPath's `preceding::` axis excludes ancestors. Therefore nested `msItem` elements can receive duplicate/gapped numeric suffixes relative to simple document order. The published development table indeed contains duplicate UIDs in the affected file.

The apparent row-match/nest mismatches therefore cannot be interpreted scientifically from development run v1.

## Repair before transfer opening

Auct_B remains unopened.

The parent-continuation task and interfaces remain unchanged in substance.

### Evaluation alignment

Reference source items are aligned to published rows without using parent identity or nest level:

1. Use `file URL + item ID` when the source item has a nonempty `@xml:id` and that pair uniquely identifies one source item and one published row.
2. Otherwise use a source-reproducible fingerprint of already-published current-row fields:
   - upstream item UID using the exact `preceding::msItem` XPath semantics;
   - item n;
   - direct title text;
   - direct locus text/from/to.
3. If the fingerprint is not unique on both sides, mark the item `ALIGNMENT_UNRESOLVED`. Do not force a row assignment.

Parent/depth information is not used in alignment.

### FILE_TABLE decoder

The full-table decoder no longer interprets the UID suffix as source order.

It uses:
- the actual published row order within the same `metadata: file URL`;
- exported `metadata: nest level`;
- a standard stack over observed row order.

This is a consumer-interface test of distributed carriers already present in the published table.

If published row order does not preserve the needed nesting sequence, that is a valid negative result.

### Additional diagnostic

Report:
- duplicate upstream item UID count within each file;
- gaps/nonmonotonicity;
- whether row order + nest level reconstructs the reference parent for aligned eligible items.

No claim is made that UID duplication alone makes the table unusable.

## Authority

The original development result remains archived as an evaluator-development outcome.

It does not count toward transfer evidence.

No Auct_B source, row, nesting outcome or parent relation was inspected before this repair.
