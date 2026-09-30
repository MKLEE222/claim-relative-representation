# Formalization Papers corrected reproduction protocol v1

Date: 2026-09-30
Status: POST-FRESH / EXPOSED CORRECTED REPRODUCTION / FRESH RESULT IMMUTABLE.

## 1. Immutable authoritative fresh result

Authoritative prospective run:

    36657856767

remains permanently:

    INVALID

Freshness was consumed at:

    2026-09-30T02:01:23.587128+00:00

Primary invalidation:

    PARSER_OR_REGISTERED_SURFACE_FAILURE

The corrected reproduction does not replace or relabel that result.

## 2. Exact source constraint

Corrected reproduction must use the byte-identical first-opening source archive:

    LaraHack/formalization_papers_supplemental
    commit 2f68d8498aeeb724e3438deda13e74ae7fb076d8

Archive SHA-256:

    c2349aa34350dc5f02f3ad7ccfc1ff6f879e88950fee948b0d5ffa206d4ca9e3

No published-index fallback, extra record, filtered subset or alternate release is allowed.

## 3. Frozen implementation correction

Only the registered dct:created canonicalization defined in:

    FORMALIZATION_PAPERS_POSTFRESH_DATETIME_CORRECTION_v1.md

is allowed.

Observed mismatch class:

    RDFLib    .526000+02:00
    pyoxigraph .526+02:00

and analogous fractional-second precision differences.

All other registered components were exact over all 10 files before correction:

    roots
    reviews
    updates
    responses
    decisions
    supersedes
    retracts
    creators

## 4. Scientific code invariants

The following scientific logic remains unchanged from DATA_OPEN:

- fp_constants.py
- fp_population.py
- run_fp_fresh_population_v1.py
- fp_documentary_audit_v1.py
- fp_finalize_v1.py
- T0-T9 taxonomy;
- denominator;
- connected-chain enumeration;
- chronology rule;
- qualification;
- P1-P7 counterfactuals;
- documentary audit criteria.

Only fp_oracle.py and fp_runtime.py change in their dct:created lexical canonicalizer.

## 5. Required gates before real corrected analysis

1. datetime canonicalization regression PASS;
2. original parser/qualification synthetic gate PASS;
3. population taxonomy synthetic gate PASS;
4. authoritative-stack synthetic closure PASS;
5. exact first-opening archive SHA verified;
6. component-level real-source diagnostic returns:
   - 10/10 files exact;
   - zero mismatching registered components.

Failure at any gate stops the corrected reproduction.

## 6. Corrected full-population analysis

If all gates pass, rerun unchanged:

    raw archive
    -> independent parser surfaces
    -> complete T0-T9 population accounting
    -> all eligible connected T0/T1 chains
    -> P1-P7
    -> independent documentary audit
    -> unchanged scientific finalizer

All roots and all eligible chains remain in the denominator.

## 7. Corrected disposition labels

The corrected wrapper reports one of:

    POST_FRESH_CORRECTED_REPRODUCTION_PASS
    POST_FRESH_CORRECTED_REPRODUCTION_BOUNDED_PARTIAL
    POST_FRESH_CORRECTED_REPRODUCTION_NULL_APPLICABILITY
    POST_FRESH_CORRECTED_REPRODUCTION_INVALID

Even if the unchanged scientific finalizer returns PASS, the user-facing corrected result must
remain prefixed POST_FRESH_CORRECTED_REPRODUCTION.

## 8. Interpretation ceiling

If corrected reproduction passes, licensed statement:

> On the exact Formalization Papers bytes first opened under the prospective protocol, the frozen
> qualified-composition analysis becomes fully executable after a parser-output correction limited
> to semantically equivalent xsd:dateTime fractional-second serialization.

Not licensed:
- literal prospective fresh PASS;
- freshness restoration;
- prevalence beyond the frozen v1.0 population;
- any taxonomy or relation change inferred from exposed outcomes.
