# Formalization Papers pre-data harness correction v1

Date: 2026-09-29
Status: PRE_DATA_TEST_HARNESS_CORRECTION / RECORD-LEVEL CONTENT STILL UNOPENED.

## Trigger

After the documentation-proven special-issue URI correction and UTC lexical normalization, the
second pre-fresh synthetic workflow reached the qualification chain.

Run:

    36592997203

Failure:

    AttributeError: module 'fp_runtime' has no attribute 'apply'

The independent implementations intentionally expose:

    fp_oracle.apply(state,event)

and:

    fp_runtime.execute(state,event)

The synthetic harness incorrectly assumed both engines used the oracle method name.

## Authorized correction

Add a test-only dispatch helper:

    oracle -> apply
    runtime -> execute

and use it consistently in:
- chain execution;
- counterfactuals;
- retraction checks.

No engine implementation, relation adapter, trajectory grammar, denominator, qualification rule,
or success criterion changes.

## Freshness

No candidate record/index/provider data has been opened.

Status remains:

    RECORD_LEVEL_UNOPENED

The next synthetic rerun must continue to require exact scientific agreement.
