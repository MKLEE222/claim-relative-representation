# Module R / VGW corrected reproduction result v1

Date: 2026-09-29
Status: COMPLETED POST-FRESH CORRECTED REPRODUCTION.

## 1. Authoritative fresh status remains unchanged

Authoritative fresh workflow:

    module-r-vgw-fresh-confirmatory-v1
    run 36553853190

Fresh disposition:

    INVALID

Reason:

    RUNTIME_NTRIPLES_LEXER_FAILURE_AFTER_DATA_OPEN

The DATA_OPEN event occurred before the failure, so this result is never relabeled as fresh PASS.

## 2. Post-fresh implementation corrections

Three implementation-only corrections/clarifications were made after exposure:

1. blank-node object immediately followed by terminal dot;
2. language-tagged literal immediately followed by terminal dot;
3. oracle/runtime comparison normalization for parser-local blank-node IDs inside already-invalid
   diagnostic records.

All three are frozen separately.

They do not change:
- RDF relations;
- F-number join;
- baseline/current semantics;
- eligibility;
- attribution-status vocabulary;
- previous_attribution recognition;
- natural-null definition;
- Module-R transition semantics;
- R1-R8;
- comparator budgets.

The third clarification follows the pre-fresh rule that RDF blank-node labels are not stable
scholarly identities.

## 3. Grammar and comparison closure

Before the successful corrected reproduction:

- Module-R synthetic controls PASS;
- VGW-shaped synthetic controls PASS;
- blank-node terminal-dot regression PASS;
- LANGTAG terminal-dot regression PASS;
- full real-source grammar coverage returns zero lexical failure classes after correction;
- oracle/runtime post-fresh diff on the exact first-opening bytes shows:
  - records_by_slug exact;
  - invalid-disposition counts exact;
  - 2108 vs 2108 F-number cases;
  - disposition mismatch count = 0;
  - science-surface mismatch count = 0.

The only raw payload mismatch was parser-local blank-node naming inside already-invalid records.

## 4. Successful corrected reproduction

Workflow:

    module-r-vgw-corrected-reproduction-v1

Successful run:

    36559829867

Head:

    f4ce7241e2eaa958f98aa8706d7e4e11556a6bed

Final disposition:

    CORRECTED_REPRODUCTION_PASS

Artifact:

    ID 11028408412
    module-r-vgw-corrected-reproduction-v1

Artifact ZIP SHA-256:

    67ac95d996fa36ed663c30c7f8e5c827dda1d138fc0ca052f7ef43cde1b1ceae

## 5. Source identity

The corrected reproduction used byte-identical distributions to the first DATA_OPEN event.

Composite source-manifest SHA-256:

    94520fe008f1d2c96fdfa74412ce2801bb13ec0672344b680874312e91e0415d

Per-source SHA-256 values matched the first opening exactly for all five frozen distributions.

## 6. Population accounting

Per dataset:

### de_la_faille_1970

    valid records      2097
    invalid records    2182
    total accounted    4279

### works_after_1970

    valid records         0
    invalid records      71
    total accounted      71

### van_gogh_museum

    valid records       790
    invalid records    3378
    total accounted    4168

### krollermuller_museum

    valid records       600
    invalid records     555
    total accounted    1155

### rkd_collections

    valid records        63
    invalid records     177
    total accounted     240

Cross-dataset unique F-number cases:

    2108

Case dispositions:

    SUBSTANTIVE_CANDIDATE                  36
    ADMISSIBLE_NULL_EVENT                 139
    MULTIPLE_CURRENT_PROVIDER_OBJECTS     189
    NO_1970_BASELINE                       11
    NO_CURRENT_PROVIDER_OBJECT           1004
    INVALID_PRODUCTION_CARDINALITY          1
    UNREGISTERED_CURRENT_ATTRIBUTION_STATUS 728

## 7. Oracle/runtime agreement

After applying only the frozen invalid-record blank-node identity normalization:

    oracle_runtime_extraction_exact = true

No eligible/admissible case identity, event, evidence or state is normalized.

Executed admissible cases:

    175

Execution failures:

    0

Thus:

    36 substantive reassessments
    139 natural nulls

are jointly reproduced by two independent extraction implementations.

## 8. Module-R result

All 36 substantive cases execute as the frozen:

    R-U3 EVIDENTIAL_STATUS_REVISION

under the project-relative task:

    ATTRIBUTED_TO_VAN_GOGH
    ->
    PREVIOUSLY_ATTRIBUTED_TO_VAN_GOGH

All 139 current-direct cases remain:

    ADMISSIBLE_NULL_EVENT

and are not promoted to substantive reassessment.

For every executed admissible case:
- R1 pre-state;
- R2 target determinacy;
- R3 event applicability;
- R4 post-state;
- R5 selectivity;
- R6 provenance;
- R7 transition attribution;
- R8 delayed history

pass under the retained interface.

Strong comparator budgets retain their registered limitations.

## 9. Independent documentary audit

Documentary audit:

    36 substantive candidates
    36 audited
    36 PASS
    0 FAIL

The auditor uses raw N-Triples with RDFLib and does not import the VGW oracle/runtime extractors.

It independently verifies for every substantive case:
- unique baseline F-number object;
- unique current provider F-number object;
- one current Production;
- one addressable E13 AttributeAssignment;
- previous_attribution classification;
- assigned Production;
- Van Gogh identity;
- exact E13 evidence URI;
- provider/source hash;
- responsibility when uniquely encoded.

Documentary audit SHA-256:

    5af488e0bcfae696456f68d1c321c37c8c46481ab94709d90e74ab124d369a1f

## 10. Result hashes

Corrected authoritative-results JSON SHA-256:

    971efa901271fa4306bba6deb8ff7311f98b50510f2af491bd53623c9c818e0d

Documentary audit SHA-256:

    5af488e0bcfae696456f68d1c321c37c8c46481ab94709d90e74ab124d369a1f

Distribution manifest SHA-256:

    27ca9f1a332e0418ad9ad93e0bad5c03e1d463700162c148ed1ff5f26157aacf

## 11. Scientific interpretation

The strongest licensed statement is:

> On the exact provider bytes first opened under the prospective VGW protocol, the frozen
> scholarly-reassessment analysis becomes fully executable after correction of parser-only
> N-Triples grammar gaps. Two independent extraction implementations agree on the scientific case
> surface; 36 source-grounded previous-attribution reassessments satisfy the frozen Module-R
> contract, 139 current-attribution cases remain natural nulls, and an independent raw-triple
> documentary audit verifies all 36 substantive cases.

This is strong independent-ecology post-fresh reproduction evidence.

It is not labeled prospective fresh confirmation because the first DATA_OPEN execution was
INVALID.

## 12. Claim ceiling

Do not claim:
- fresh PASS;
- true authorship adjudication;
- that all previous attributions have the same historical cause;
- prevalence beyond the frozen VGW distributions;
- universal representational necessity.

The result does support:
- non-temporal ecological portability;
- natural substantive/null separation;
- source-grounded attribution-status reassessment;
- the distinction between current state, change record and evidence-grounded transition history.
