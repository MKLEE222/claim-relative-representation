# Final Warrant Result Analysis Contract v1

Date frozen: 2026-09-26
Status: FROZEN BEFORE FINAL JUDGE OUTPUTS

## Input

Exactly 15 output records from one fresh/stateless or model-separated judge:
- 5 anonymous packet families;
- canonical, reverse-order, ID-relabel variants.

## Stage 1 — schema and completeness

All 15 call IDs must be present exactly once.
Only frozen E_* labels and RETAIN/DEFER/WITHHOLD are admissible.

## Stage 2 — stability before unblinding

For each anonymous packet, warrant state must be identical across:
- canonical;
- reverse order;
- ID relabel.

If any packet fails this condition:
`FINAL_WARRANT_STATUS=MODEL_SENSITIVE`

No selective-restoration claim is evaluated.

Relation-set agreement is descriptive and reported by pairwise Jaccard.
Warrant-state invariance is the hard gate.

## Stage 3 — unblinding

Only after every packet passes Stage 2 is the audit mapping applied.

## Stage 4 — frozen contrasts

Report:
- GENERIC_BASE vs GUIDED_BASE;
- GENERIC_BASE vs GENERIC_RESCUE_PM03;
- GENERIC_BASE vs GENERIC_SHAM;
- GUIDED_BASE vs GUIDED_REMOVE_PM03.

## Strong selective-restoration criterion

PASS iff:
1. GENERIC_RESCUE_PM03 differs from GENERIC_BASE;
2. GENERIC_SHAM equals GENERIC_BASE;
3. GUIDED_REMOVE_PM03 differs from GUIDED_BASE.

The base generic/guided difference is reported separately and is not sufficient for selective closure.

## No ordinal forcing

RETAIN, DEFER, and WITHHOLD are not converted into a numeric score.
The analysis tests equality/difference of frozen warrant states.

## Null retention

Any failure of the three selective criteria is retained as a partial/null result.
No prompt, packet, donor, evidence budget, or state vocabulary is changed after observing final outputs.