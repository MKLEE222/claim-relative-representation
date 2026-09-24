# EP_KS_01D - Native referent-bridge diagnostic

Date frozen: 2026-09-24
Status: EXPLORATORY MECHANISM DIAGNOSTIC AFTER v1 FAILURE

## Question

Can an explicit seed-side identity note in the native 1903 representation bridge the lexical shift from Kinsay to later terminology without using target-only text?

## Baseline

Generic Seed-Task Access Policy v1 remains unchanged and is not retroactively rescued.

## Additional carrier

Chapter LXXVI Note 1 is attached to the Kinsay chapter and explicitly identifies the place under multiple names.

The diagnostic extracts alias forms mechanically from the first identity sentence of that note.

## Extraction rule

1. locate "NOTE 1.—KINSAY" after the frozen seed;
2. take only the first sentence;
3. extract:
   - all-uppercase alphabetic/hyphenated name tokens;
   - mixed-case hyphenated name tokens;
4. normalize hyphens into whole-form and component tokens;
5. add these tokens to the frozen v1 query signature with the median weight of the original v1 query terms.

No target is inspected during alias extraction.

## Forbidden target-only terms

Tanner | sea wall | native poet | visited

These remain forbidden.

"Hang-chau" is not target-only in this diagnostic because its provenance is the native 1903 seed-side Note 1.

## Conditions

Run only on the later-layer scope, because v1 already established the full-object and later-layer baselines.

Report:
- extracted aliases;
- target rank/score;
- Hit@10/20/50;
- comparison with frozen v1 later-layer result.

## Claim ceiling

A positive result would identify a carrier mechanism for Kinsay.

It would not validate a general alias-expansion method because the mechanism was discovered after v1.
