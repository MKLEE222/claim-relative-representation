# Formalization Papers corrected reproduction attempt 1 — blocked v1

Date: 2026-09-30
Status: POST-FRESH CORRECTED ATTEMPT / BLOCKED BEFORE POPULATION.

Workflow:

    formalization-papers-corrected-reproduction-v1

Run:

    36658658912

Head:

    62895e27889b5546f028c0df20f3197ade623610

## Result

All frozen pre-analysis gates passed:
- datetime canonicalization regression;
- parser/qualification synthetic;
- population synthetic;
- authoritative-stack synthetic;
- byte-identical first-opening archive SHA.

Real-source exactness improved from:

    0/10 exact files

to:

    9/10 exact files

after the datetime correction.

The workflow then stopped, by design, before population analysis.

No corrected population disposition was produced.

## Residual mismatch

Only:

    nanopubs/sp-responses.trig

remained non-exact.

Only registered component:

    creators

differed.

All other components, including created timestamps, were exact.

Observed creator mismatch shape:
- same nanopublication URI;
- source contains two dct:creator values;
- RDFLib/scalar extraction retained one;
- pyoxigraph/scalar extraction retained the other.

## Independent pubinfo cardinality audit

Exact first-opening archive:

    404 nanopublications

Creator cardinality:

    379 with 1 creator
    25 with 2 creators

Created timestamp cardinality:

    404 with exactly 1 timestamp

Thus the residual mismatch is not an RDF semantic disagreement.
It exposes that the registered extractor incorrectly collapsed a multi-valued RDF relation into a
scalar dictionary value.

## Disposition

This attempt is not a corrected PASS, PARTIAL or NULL result.

It is:

    POST_FRESH_CORRECTED_ATTEMPT_BLOCKED_BEFORE_POPULATION

The authoritative fresh run remains INVALID.

A new frozen amendment is required before another corrected reproduction.
