# VGW runtime N-Triples blank-node terminator correction v1

Date: 2026-09-29
Status: POST-FRESH IMPLEMENTATION CORRECTION / SCIENTIFIC CONTRACT UNCHANGED.

## Trigger

Authoritative fresh run 36553853190 exposed a lexical parser failure on a valid N-Triples line
whose object is a blank-node label immediately followed by the statement terminator:

    _:blank-node-label.

The independent RDFLib oracle parses this form successfully.

## Frozen correction

The runtime blank-node lexical reader may no longer consume an end-of-statement dot as part of a
blank-node label.

For a blank-node token read to the end of a stripped N-Triples line:

- if the scanned token ends in '.';
- treat exactly the final dot as the statement terminator;
- return the blank-node token without that final dot;
- leave parser position pointing at that dot.

Dots internal to a blank-node label are not removed.

No other tokenization rule changes.

## Scientific invariants

The correction does NOT change:
- URI constants;
- F-number extraction;
- baseline/current provider cardinality;
- Production cardinality;
- direct Van Gogh attribution;
- previous_attribution E13 recognition;
- stable-addressability rejection;
- natural-null definition;
- status vocabulary;
- Module-R transition semantics;
- R1-R8;
- strong comparator budgets;
- outcome thresholds.

## Required regression

Before corrected reproduction:
1. the original VGW synthetic gate must still pass;
2. a dedicated lexical regression must parse a blank-node object with no whitespace before the
   terminal dot;
3. oracle/runtime extraction must agree on that fixture.

Any further natural-data parser discrepancy is preserved rather than silently repaired in the
same corrected reproduction.
