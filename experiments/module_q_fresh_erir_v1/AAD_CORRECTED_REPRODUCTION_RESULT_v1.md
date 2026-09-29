# AAD corrected reproduction result v1

Date: 2026-09-29
Status: COMPLETED CORRECTED REPRODUCTION AFTER EXPOSURE.

## 1. Scope

This run repairs only the original execution-layer import-path failure.

Scientific logic was unchanged:
- same upstream repository;
- same pinned commit;
- same 148-file population;
- same object grammar;
- same Module-P eligibility;
- same Phi projection;
- same transition classes;
- same P1-P7 evaluator;
- same strong comparators;
- same failure interventions.

The only original execution repair was adding:

    experiments/module_p_evidence_release_revision_v1

to sys.path so oracle_p/runtime_p/evaluator_p can be imported from the Module-Q runner.

Because AAD had already been opened in a later exposed audit, this run is not labeled fresh
confirmation.

## 2. Successful corrected workflow

Workflow:

    module-q-aad-corrected-reproduction-v1

Successful run:

    36540147897

Head:

    60ca1a3fad8a7a46e68ad947a36462f84a765f64

Artifact:

    ID 11020635013
    module-q-aad-corrected-reproduction-v1

Artifact ZIP SHA-256:

    608017d71f13a8e1e92a3c450368df16faf78ee50bbf533471a439944ed2145d

Corrected result JSON SHA-256:

    1722d78e33559eae26cfe41cb8ff7d0233f475adaeebaae5c6d2c4bcaf4bb869

## 3. Corrected population result

Expected XML:

    148

Parsed:

    148

Parse errors:

    0

Complete accounting:

    true

Object status:

    SINGLE_PRIMARY_DOCUMENT_OBJECT = 139
    NO_PRIMARY_DOCUMENT_OBJECT = 9

Module-P disposition:

    ERIR_ELIGIBLE = 69
    ADMISSIBLE_NULL_EVENT = 70
    INELIGIBLE = 9

Transition classes:

    P-U1 CONFLICT_FORMATION = 16
    P-U2 RESOLUTION_OR_ACQUISITION = 30
    P-U3 NARROWING_OR_QUALIFICATION = 23

Oracle/runtime contract unresolved:

    0

## 4. Regime separation

Among all 69 ERIR-eligible episodes:

    old D1/D2 eligible = 0
    old D1/D2 not eligible = 69

Thus the corrected execution preserves the intended empirical distinction between:

    ambiguity-triggered inquiry

and:

    evidence-release-induced revision.

## 5. Reference capability result

All 69 eligible episodes pass:

    P1 CURRENT_STATE_BEFORE = 69/69
    P2 EVENT_APPLICABILITY = 69/69
    P3 POST_EVENT_RESULT = 69/69
    P4 SELECTIVE_UPDATE = 69/69
    P5 PROVENANCE = 69/69
    P6 TRANSITION_ATTRIBUTION = 69/69
    P7 DELAYED_HISTORY = 69/69

Reference end-to-end:

    69/69

## 6. Strong comparator result

RSTAR:

    T1 = 69/69
    T2 = 69/69
    T3 = 69/69
    T4 = 69/69
    T5 = 69/69

B_CURRENT_REOPEN:

    T1 = 69/69
    T2 = 69/69
    T3 = 0/69
    T4 = 0/69
    T5 = 0/69

B_ORDERED_SNAPSHOTS:

    T1 = 69/69
    T2 = 69/69
    T3 = 69/69
    T4 = 0/69
    T5 = 0/69

## 7. Failure interventions

Wrong object:

    rejected 69/69
    root unchanged 69/69

Wrong source version:

    rejected 69/69
    root unchanged 69/69

Missing applicability:

    rejected 69/69
    root unchanged 69/69

No history:

    post result 69/69
    selectivity 69/69
    provenance 69/69
    transition attribution 69/69
    delayed history 0/69

Collateral mutation:

    event applicable 69/69
    transition attribution 69/69
    collateral detected 39/69
    selectivity pass 30/69

The collateral denominator remains intervention-applicability-limited as already documented.

## 8. Reproduction consistency

The corrected reproduction was rerun in the same workflow with the already successful exposed
reference analysis.

Machine comparison result:

    all_scientific_outputs_match = true

Exact matches:
- upstream snapshot;
- population accounting;
- regime separation;
- P1-P7 aggregate capabilities;
- strong comparator capabilities;
- failure-intervention outcomes;
- eligible per-episode scientific manifest;
- null-event manifest;
- parse errors;
- unresolved-contract manifest.

The only initially observed per-episode difference was an opaque claim-key hash inside one fault
trace path.

That hash intentionally includes source-context population_scope, which differs between:
- the original frozen population context;
- the later exposed-audit context.

After normalizing only this context-bound opaque identifier, the mutation semantics remained
exactly identical:

    claims/<context-bound-key>:CHANGED

No scientific value, transition class, capability or fault outcome was normalized.

Final comparison:

    eligible_manifest_first_diff = null

## 9. Interpretation

The original AAD failure was therefore an execution-layer import failure.

After correcting that execution error, the originally frozen scientific analysis reproduces the
same scientific outcomes obtained by the later exposed audit.

This supports the conclusion that:
- the import failure did not indicate a scientific/mechanism failure;
- the Module-P/AAD results are stable to the corrected execution;
- the loss of fresh-confirmatory status is procedural/history-related, not due to a changed
  scientific result.

## 10. Claim ceiling

This run remains:

    CORRECTED_REPRODUCTION_AFTER_EXPOSURE

It does not retroactively restore AAD as a fresh confirmatory corpus.

It does establish that the engineering repair reproduces the intended frozen analysis without
scientific redesign.
