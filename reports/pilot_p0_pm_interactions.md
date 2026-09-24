# Pilot P0 results - paper-money interaction dry run

Date: 2026-09-24
GitHub Actions run: 35951414662
Commit: b12064c16eebe435350cb9047917062e8f0359ed

## Result

All three paper-money interaction probes failed to exhaust the alternative carrier family.

- I01 temporal order: R11 remained R/D1/B_LEXICAL_CUE.
- I02 claim binding: R11 remained R/D1/B_LEXICAL_CUE.
- I03 evidence relation: R11 remained R/D1/B_LEXICAL_CUE.

The construction/validation suite remained green.

## Immediate interpretation

The current TA_SPAN condition is too weak to create a carrier-exhaustion interaction for TAU_PM_CROSSLAYER because the task-defining spans themselves preserve strong lexical cues.

The main-effect pattern is therefore:

structured explicit -> lexical recovery

rather than:

structured explicit -> unavailable.

This is consistent with Experiment 1A and is a second independent design-level warning against binary "metadata loss = evidence loss" claims.

## More important design finding

The pilot reveals a task/transformation mismatch.

TAU_PM_CROSSLAYER receives PM01, PM02, and PM03 as frozen task inputs. Once all three relation endpoints are already supplied, an access transformation that merely removes surrounding object context cannot test the full scholarly access problem. It can only test whether extra context is needed after discovery has already succeeded.

Therefore access transformations should be paired primarily with tasks whose scientific object is access/discovery/sequence reconstruction, for example:

- tau_locate: starting from a claim/referent or one seed passage, can the relevant later/earlier witness be found?
- tau_sequence: can the version relation be established from the allowed representation horizon?

By contrast, fixed-endpoint tau_relation is better suited to TD/TR transformations, because the relevant passages are already present.

## Consequence

Do not strengthen TA_SPAN post hoc merely to force an interaction.

Instead, revise the factorial architecture:

1. **Access block** - TA transformations x locate/sequence tasks.
2. **Relation block** - TD/TR transformations x fixed-endpoint attribution/binding/relation tasks.
3. **Workflow block** - only after both are validated, compose access output into relation/adjudication tasks.

This preserves task identity and avoids using context truncation as disguised evidence deletion.

## Status of I01-I03

The preregistered blocks remain in the ledger.

Pilot status:

- I01: MECHANISM_NOT_SUPPORTED_ON_CURRENT_TASK_PACKET
- I02: MECHANISM_NOT_SUPPORTED_ON_CURRENT_TASK_PACKET
- I03: MECHANISM_NOT_SUPPORTED_ON_CURRENT_TASK_PACKET

They should not be promoted to a human confirmatory interaction test without a new pre-outcome rationale.

## Boundary

This pilot used a deterministic lexical-cue probe. It is not evidence about human recovery accuracy or humanities claim-state effects.
