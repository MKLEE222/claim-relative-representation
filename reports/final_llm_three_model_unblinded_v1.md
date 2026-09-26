# Paper-Money Unblinded Three-Model LLM Outcome v1

Date: 2026-09-26

## Frozen mapping

- K4N = GENERIC_BASE
- R8Q = GUIDED_BASE
- M3V = GENERIC_RESCUE_PM03
- H7C = GENERIC_SHAM
- T2P = GUIDED_REMOVE_PM03

## Qwen2.5 7B

- GENERIC_BASE: RETAIN / RETAIN / RETAIN
- GUIDED_BASE: RETAIN / RETAIN / RETAIN
- GENERIC_RESCUE_PM03: RETAIN / RETAIN / RETAIN
- GENERIC_SHAM: WITHHOLD / RETAIN / WITHHOLD
- GUIDED_REMOVE_PM03: RETAIN / RETAIN / RETAIN

Disposition:
`MODEL_SENSITIVE` due to the sham packet.

Even ignoring the failed stability gate, the canonical non-sham conditions do not show the selective-restoration pattern.

## Gemma3 12B

All five conditions:
`RETAIN / RETAIN / RETAIN`.

Disposition:
`STABLE_NO_PACKET_CONTRAST`.

## Llama3.1 8B

All five conditions:
`RETAIN / RETAIN / RETAIN`.

Disposition:
`STABLE_NO_PACKET_CONTRAST`.

## Final frozen-LLM conclusion

`SELECTIVE_RESTORATION_NOT_SUPPORTED`.

The result is preserved as a negative measurement result.

## Diagnostic observation

The two stable judges commonly treat PM01's direct assertion as sufficient for RETAIN and treat PM02's explicit botanical objection as a qualification that does not defeat admissibility.

This is exactly the relation-collapse failure that the representation framework warns against:

`statement presence != successful use of attack / counter-attack structure`.