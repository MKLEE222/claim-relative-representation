# VGW oracle/runtime invalid blank-node comparison clarification v1

Date: 2026-09-29
Status: POST-FRESH IMPLEMENTATION COMPARISON CLARIFICATION / SCIENTIFIC CONTRACT UNCHANGED.

## 1. Trigger

After the two N-Triples lexical corrections were frozen and the full grammar-coverage audit
returned zero lexical failures, corrected reproduction run:

    36555499619

still returned:

    oracle_runtime_extraction_exact = false

A dedicated post-fresh diff diagnostic on the exact first-opening source SHA-256 values then
showed:

- records_by_slug: exact;
- invalid-disposition counts: exact;
- case key count: 2108 vs 2108;
- case-disposition counts: exact;
- disposition mismatches: 0;
- science-surface mismatches across all cases: 0.

The first full-payload difference was:

    $.invalid_records[0].object_uri

where:
- RDFLib generated one local blank-node label;
- the independent lexical parser preserved another/source-local blank-node label.

Both rows had the same scientific disposition:

    NON_ADDRESSABLE_ARTWORK_OBJECT

## 2. Existing pre-fresh identity rule

Before any provider distribution was opened, the project froze:

    VGW_RDF_NODE_IDENTITY_CLARIFICATION_v1.md

That contract states:
- parser-local RDF blank-node labels are not stable scholarly identities;
- a blank-node artwork object is NON_ADDRESSABLE_ARTWORK_OBJECT;
- a blank-node E13 reassessment event is NON_ADDRESSABLE_REASSESSMENT_EVENT;
- such labels cannot support provenance or delayed-history identity.

Therefore requiring byte-equality of parser-local blank-node labels inside already-ineligible
diagnostic records contradicts the pre-fresh identity contract.

## 3. Frozen normalization

For oracle/runtime extraction equality only:

### 3.1 Invalid-record node identities

Within:

    invalid_records

normalize a node string iff it begins with:

    _:

to:

    <BLANK_NODE>

This applies to:
- invalid-record object_uri;
- invalid-record identifier_nodes entries.

Stable URI strings are never normalized.

### 3.2 What remains exact

The following remain exact and unnormalized:
- invalid-record slug;
- invalid-record disposition;
- f_values;
- number of identifier nodes;
- every stable URI;
- records_by_slug;
- post1970 role exclusions;
- every F-number case;
- case disposition;
- baseline/current object URIs;
- provider slug;
- state;
- event;
- evidence_id;
- evidence_locator;
- responsibility;
- transition class.

No normalization is allowed inside an eligible/admissible case state or event.

## 4. Scientific invariants

This clarification does NOT change:
- RDF parsing;
- any extracted triple;
- F-number extraction;
- baseline/current joining;
- Production cardinality;
- attribution classification;
- previous_attribution recognition;
- eligibility;
- null/substantive status;
- Module-R transition semantics;
- R1-R8;
- comparator budgets;
- documentary audit.

It changes only the equality representation of identities that the pre-fresh contract had already
declared non-addressable.

## 5. Required regression

Before another corrected reproduction:

1. Module-R synthetic controls PASS;
2. VGW-shaped synthetic controls PASS;
3. blank-node terminator regression PASS;
4. LANGTAG terminator regression PASS;
5. grammar-coverage audit remains zero failures;
6. dedicated oracle/runtime diff remains:
   - disposition mismatch count = 0;
   - science-surface mismatch count = 0;
7. a comparison regression proves:
   - two different blank labels in invalid_records normalize equal;
   - a stable URI difference does NOT normalize equal;
   - a case/evidence difference does NOT normalize equal.

The authoritative fresh result remains INVALID and is not changed by this clarification.
