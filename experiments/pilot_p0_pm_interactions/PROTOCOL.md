# Pilot P0 - Paper-money interaction dry run

Date frozen: 2026-09-24
Status: MECHANISM PROBE, NOT CONFIRMATORY EVIDENCE

## Purpose

Run the current task-adapted representation design on one already source-validated carrier before launching any human or claim-state experiment.

The pilot uses TAU_PM_CROSSLAYER and the three preregistered first-wave interactions:

- I01: TD_TEMPORAL x TA_SPAN
- I02: TR_BINDING x TA_SPAN
- I03: TR_EVIDENCE x TA_SPAN

## Important boundary

This pilot does not estimate human performance and does not validate the CEDL ontology.

It is a deterministic mechanism probe asking:

> Given the current source-facing paper-money spans, do the planned joint transformations actually exhaust the preregistered alternative carriers, or do lexical cues still preserve recoverability?

## Task packet semantics

The frozen task input is PM01 + PM02 + PM03.

TA_SPAN means:

- keep all three task-defining spans byte-identical;
- remove surrounding object context and auxiliary context objects;
- do not remove any words inside PM01-PM03.

This avoids changing the task itself while still testing context restriction.

## Recovery probe

For each target distinction, the probe applies the following hierarchy:

1. structured coordinate present -> E / D0 / structured carrier;
2. otherwise, direct lexical cue in task-defining spans -> R / D1 / lexical carrier;
3. otherwise, cue only in auxiliary object context -> R / D3 / cross-layer-context carrier;
4. otherwise -> Q / NA / no sufficient carrier detected.

The probe is intentionally conservative and only recognizes frozen cue families. A negative lexical result is not evidence of true semantic unavailability.

## Expected scientific use

If R11 remains recoverable because lexical cues survive, the corresponding interaction hypothesis is not supported on this carrier and should not be escalated as a confirmatory claim.

If R11 exhausts all frozen carriers, the interaction becomes eligible for later human evaluation.

No retain/revise/defer/withhold outcome is opened.
