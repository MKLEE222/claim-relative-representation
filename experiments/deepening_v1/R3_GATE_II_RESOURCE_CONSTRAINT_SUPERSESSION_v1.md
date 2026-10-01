# R3 Gate-II Resource-Constraint Supersession v1

Date: 2026-09-27
Status: ACTIVE FOR TRACK A; HUMAN REVIEW MATERIALS PRESERVED BUT NO LONGER MANDATORY

## Reason

The project is being executed by one human researcher.

A second independent human historical reviewer is not available within the study's actual research configuration.

Treating an unavailable second person as a mandatory scientific closure condition would convert a staffing constraint into an implicit validity criterion and would make the Track-A claim formally uncloseable regardless of the evidence already accumulated.

## What is superseded

The following earlier state is superseded **as a mandatory Track-A requirement**:

INDEPENDENT_SECOND_PASS = PENDING

where "independent second pass" meant a qualifying second human reader.

The sealed human-review design, packet, source bundle, answer seal and atomic adjudication plan are not deleted or rewritten.

They remain valid as an optional future external-human validation layer.

## Replacement gate

Track-A Gate II now requires:

BLINDED_MODEL_SEPARATED_HISTORICAL_ADJUDICATION

under:

R3_BLINDED_THREE_MODEL_HISTORICAL_ADJUDICATION_PROTOCOL_v1.md

The frozen design uses:

- qwen2.5:7b
- gemma3:12b
- llama3.1:8b

across:

- five load-bearing historical cases;
- three semantically equivalent prompt/order perturbations;
- 45 stateless source-only calls;
- 21 predeclared atomic historical components.

The runner does not load the registered answer panel.

The post-run analyzer opens the sealed normalized answer key only after all outputs have been frozen.

## Why this is not described as human validation

The replacement test can establish reproducibility across heterogeneous, answer-blinded computational adjudicators.

It cannot establish:

- independent human validation;
- historian consensus;
- human inter-rater reliability;
- expert-community acceptance.

The manuscript must state this limitation directly.

## Why the prior LLM negative does not invalidate this gate

The earlier 45-call warrant experiment tested whether local models could implement a frozen abstract defeasible-warrant instrument.

That experiment was model-sensitive / non-selective and remains a negative result.

The new Gate-II task is materially narrower:

- source-grounded historical extraction;
- actor/proposition assignment;
- evidence-to-proposition assignment;
- modality/uncertainty extraction;
- textual correction;
- controversy-state extraction.

The new experiment therefore does not reinterpret or rescue the old warrant result.

It tests a different measurement function.

## Disposition rule

If all 21 components receive stable two-of-three model consensus matching the sealed historical reading:

GATE_II = SOURCE_GROUNDED_BLINDED_MODEL_REPLICATION_PASS

If no stable consensus contradicts the sealed reading but some components lack consensus:

GATE_II = BOUNDED_PARTIAL

and only the affected claims are downgraded.

If any stable ensemble consensus contradicts a sealed load-bearing component:

GATE_II = HISTORICAL_READING_REOPENED

and the affected historical claim is reopened without prompt retuning.

## Human packet status

The human-review artifact remains preserved:

r3-independent-second-pass-review-bundle-v1

Artifact ID:
10929598975

It is now:

OPTIONAL_EXTERNAL_HUMAN_VALIDATION

not:

TRACK_A_REQUIRED_GATE.
