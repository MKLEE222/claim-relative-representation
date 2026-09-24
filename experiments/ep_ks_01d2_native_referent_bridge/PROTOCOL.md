# EP_KS_01D2 - Native referent-bridge implementation repair

Date frozen: 2026-09-24
Status: REPAIR OF INVALID D1 IMPLEMENTATION

## Why D1 is invalid as a scientific result

EP_KS_01D preregistered an alias extraction rule from the first identity sentence after the seed-side Note 1 attached to Kinsay.

The implementation searched for the first period starting at the heading:
"NOTE 1.—KINSAY"

It therefore terminated at the period in "1." and extracted only the heading prefix rather than the intended first identity sentence.

Observed D1 symptom:
- aliases = empty
- target rank remained identical to baseline v1

This is an implementation failure, not evidence against the referent-bridge mechanism.

## Repair rule

No scientific rule changes.

The repaired parser:

1. locates the same frozen Note 1 heading;
2. starts sentence extraction **after the heading match**;
3. skips whitespace and dash punctuation;
4. takes the first prose sentence ending in a period;
5. applies the original alias-extraction rule unchanged.

## Source-facing rationale

The native Kinsay note explicitly states that Kinsay closely represents "King-sze" and identifies the city as now Hang-chau.

These aliases are available on the seed side of the 1903 representation; they are not imported from the hidden 1920 target.

## Frozen leakage rule

Forbidden target-only terms remain:

Tanner | sea wall | native poet | visited

If any forbidden term enters the query signature, the run fails.

## Outcome discipline

D2 may:
- improve target rank;
- leave rank unchanged;
- worsen rank.

No tuning follows the D2 outcome.

D1 remains in the ledger as INVALID_IMPLEMENTATION, not overwritten.
