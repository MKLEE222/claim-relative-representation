# R3 carrier-composition replication protocol v2

Date frozen: 2026-09-27
Status: PRE-OUTCOME.

## Selection

Use the next untouched duplicate-pointer group in source order after XXXVII p.191:
- chapter LII, page 254;
- YC1920E-0071;
- YC1920E-0072.

Selection is based only on duplicate native pointer structure, not lexical outcome.

## Historical-start seeds

C03 -> YC1920E-0071:
`They live on the milk and meat which their herds supply`

C04 -> YC1920E-0072:
`the custom of turning the door to the south`

Both phrases occur in the earlier 1903 object and are frozen before later ranking.

## Routes

Use exactly the v1 scoring/representation rules:
- POINTER_ONLY: chapter LII + page 254;
- LEXICAL_GLOBAL: pointer-hidden bodies across all 223 entries;
- POINTER_THEN_LEXICAL: same scorer restricted to pointer candidates.

No tuning, target-only term, or new stopword list is permitted.

## Primary support pattern

Composition support requires:
- POINTER_ONLY non-unique;
- POINTER_THEN_LEXICAL target rank 1.

Global lexical rank is reported but is not required to fail.

## Scope

This is an within-corpus replication on a different editorial topic pair, not an independent infrastructure replication.