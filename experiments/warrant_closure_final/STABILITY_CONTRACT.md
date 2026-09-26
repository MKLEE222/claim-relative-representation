# Final LLM Stability and Selective-Restoration Contract v1

Date frozen: 2026-09-26
Status: FROZEN BEFORE FINAL LLM EXECUTION

## Packet family

Five anonymous canonical packets are adjudicated:
- GENERIC_BASE
- GUIDED_BASE
- GENERIC_RESCUE_PM03
- GENERIC_SHAM
- GUIDED_REMOVE_PM03

Policy/condition names are sealed separately from judge-visible packet IDs.

## Per-packet perturbations

Each packet has:
- canonical order;
- reverse evidence-unit order;
- ID-relabel-only variant.

Text and source metadata remain identical.

## Stable packet state

A packet's warrant state is stable only if canonical, reverse-order, and ID-relabel variants receive the same warrant state.

Relation-set variation is reported separately using exact set agreement and Jaccard.

## Primary selective-restoration contrast

Strong pattern:
- GENERIC_RESCUE_PM03 differs from GENERIC_BASE;
- GENERIC_SHAM equals GENERIC_BASE;
- GUIDED_REMOVE_PM03 differs from GUIDED_BASE.

All three comparisons are evaluated only after packet-level stability.

## Nulls

Any null is retained.
If perturbations change warrant state, the packet is MODEL_SENSITIVE and cannot support the final consequence claim.

## Replication

J0 is excluded from confirmatory counts.
The final confirmatory judge must be fresh/stateless or model-separated from the design conversation.

If more than one fresh model is used, no majority vote is treated as truth. Agreement/disagreement is reported as instrument stability.