# R3 carrier-composition replication protocol v3

Date frozen: 2026-09-27
Status: PRE-OUTCOME.

## Selection

Use the next untouched duplicate-pointer group in source order after LII p.254:
- chapter LVIII, page 283;
- YC1920E-0082;
- YC1920E-0083.

Selection is structural/source-order only.

## Historical-start seeds

C05 -> YC1920E-0082:
`Among the names of these were Sling, Shirum, Gurun, and Khoza`

C06 -> YC1920E-0083:
`Cunningham also mentions camlets of camel's hair, under the name of Suḳlát`

Orthographic normalization is limited to Unicode/casefold and punctuation/whitespace handling already used by the frozen tokenizer. No later-only form such as sa-ha-la or saghlat is injected into C06.

## Routes

Exactly as v1/v2:
- POINTER_ONLY;
- LEXICAL_GLOBAL over 223 pointer-hidden bodies;
- POINTER_THEN_LEXICAL within the duplicate-pointer candidate set.

## Interpretation categories

STRONG_COMPLEMENTARITY:
pointer non-unique, global lexical target not rank 1, composed target rank 1.

REDUNDANT_WITH_COMPOSITION:
pointer non-unique, global lexical rank 1, composed rank 1.

COMPOSITION_FAILURE:
composed target not rank 1.

These categories are frozen before outcome.

## Claim ceiling

This within-corpus replication characterizes carrier-system heterogeneity. It is not a prevalence estimate.

## Pre-outcome implementation repair

The first execution stopped before ranking because Gutenberg emphasis markup places underscores between anchor words and the C06 source spelling is Suḳlát. No target outcome was observed. The anchor matcher is therefore allowed to treat underscores as punctuation separators, and C06 is corrected to the source-exact orthography. Scientific cases, pointer group, scoring rule, and success categories are unchanged.
