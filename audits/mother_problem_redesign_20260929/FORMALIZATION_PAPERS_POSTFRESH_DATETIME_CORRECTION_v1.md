# Formalization Papers post-fresh datetime canonicalization correction v1

Date: 2026-09-30
Status: POST-FRESH IMPLEMENTATION-ONLY CORRECTION / AUTHORITATIVE FRESH RESULT REMAINS INVALID.

## 1. Diagnostic basis

Authoritative fresh run:

    36657856767

remains permanently:

    INVALID

Post-fresh component diagnostic:

    formalization-papers-postfresh-parser-diagnostic-v1
    run 36658251785

Exact frozen source archive:

    c2349aa34350dc5f02f3ad7ccfc1ff6f879e88950fee948b0d5ffa206d4ca9e3

Observed over all 10 record files:

    roots        exact 10/10
    reviews      exact 10/10
    updates      exact 10/10
    responses    exact 10/10
    decisions    exact 10/10
    supersedes   exact 10/10
    retracts     exact 10/10
    creators     exact 10/10
    created      mismatch 10/10

Thus the registered relation/object surface agrees completely except for dct:created lexical
serialization.

## 2. Exact mismatch class

Examples:

    RDFLib:
    2021-10-25T16:22:30.526000+02:00

    pyoxigraph:
    2021-10-25T16:22:30.526+02:00

and:

    RDFLib:
    2021-10-07T02:12:24.840000+03:00

    pyoxigraph:
    2021-10-07T02:12:24.84+03:00

The represented xsd:dateTime value is unchanged.

RDFLib renders the parsed fractional second at six-digit microsecond precision.
Pyoxigraph retains the shorter lexical fractional precision.

No relation, object, target, creator, status, version or chronology disagreement was observed.

## 3. Frozen correction

For values admitted to the registered dct:created surface only:

1. parse an ISO-8601/xsd:dateTime lexical value;
2. preserve its represented date, clock time and UTC offset;
3. render fractional seconds at exactly six microsecond digits;
4. render UTC as +00:00.

Examples:

    2021-10-25T16:22:30.526+02:00
    ->
    2021-10-25T16:22:30.526000+02:00

    2021-10-07T02:12:24.84+03:00
    ->
    2021-10-07T02:12:24.840000+03:00

    2021-01-01T00:00:00Z
    ->
    2021-01-01T00:00:00.000000+00:00

The correction is applied independently in both parser implementations.

If a created value cannot be parsed as ISO-8601/xsd:dateTime, it is retained unchanged; no
inference or repair is attempted.

## 4. Scientific invariants

This correction does NOT alter:
- root extraction;
- review targets;
- update targets;
- response review/update targets;
- decision target/status;
- supersession/retraction;
- creator identity;
- object/version identity;
- T0-T9 definitions;
- population denominator;
- connected-chain enumeration;
- chronology ordering semantics;
- qualification;
- counterfactuals;
- history ablation;
- documentary audit criteria.

It changes only a comparison/storage serialization of a timestamp value already parsed by both
engines.

## 5. Required regression before corrected reproduction

Synthetic regression must prove:

### Equivalent precision

    2021-10-25T16:22:30.526000+02:00
    2021-10-25T16:22:30.526+02:00

canonicalize equal.

### Equivalent shorter fraction

    2021-10-07T02:12:24.840000+03:00
    2021-10-07T02:12:24.84+03:00

canonicalize equal.

### Different time remains different

    2021-10-25T16:22:30.526+02:00
    2021-10-25T16:22:31.526+02:00

must remain unequal.

### Different offset lexical values are not silently rewritten into one wall-time value

The canonicalizer preserves the represented offset and does not invent or drop timezone
information.

## 6. Corrected reproduction status

Any run after this correction is:

    POST-FRESH / EXPOSED CORRECTED REPRODUCTION

It can test whether the exact first-opening bytes become fully executable and whether the
prospective scientific structure survives the implementation correction.

It cannot become or replace a literal fresh PASS.
