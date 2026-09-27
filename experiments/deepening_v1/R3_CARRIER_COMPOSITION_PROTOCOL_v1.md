# R3 carrier-composition transfer protocol v1

Date frozen: 2026-09-27
Status: PRE-OUTCOME for the selected B03 pair.

## Motivation

R3-F/G v1 produced a post-outcome development clue: one later target shared its native page pointer with another entry, while body lexical evidence ranked the correct target first.

This protocol tests carrier composition prospectively on the first untouched duplicate-pointer group after the already opened material.

## Frozen target group

Source-order duplicate-pointer group:
- chapter XXXVII, page 191;
- YC1920E-0045: later correction concerning the claim that Fa-hien followed the directer route;
- YC1920E-0047: later discussion challenging/qualifying identifications of Pein/Pimo.

Neither entry has had an R3 representation/retrieval outcome opened.

## Historical-start seeds

Both seeds come only from the earlier 1903 Volume I object and are frozen before later ranking.

CASE C01 -> YC1920E-0045:
`This directer route between Khotan and China must have been followed by Fa-hian on his way to India`

CASE C02 -> YC1920E-0047:
`Pein, then, was identical with PIMA`

Each seed is a fixed ±900-character window around the first whitespace/punctuation-robust match.

## Frozen routes

### POINTER_ONLY
Match chapter XXXVII + page 191 against refined 1920 entry heads.

Expected structural property, known before lexical outcomes:
the pointer returns more than one candidate.

### LEXICAL_GLOBAL
Hide all heads and rank all 223 entry bodies using the same frozen TF-IDF rule as R3-F/G v1.

### POINTER_THEN_LEXICAL
Take the POINTER_ONLY candidate set, then rank only those candidates with the same seed-side TF-IDF scorer.

No target-derived term is added.

## Primary question

Does composition of a coarse documentary pointer with textual discrimination uniquely recover the correct later intervention when either carrier alone is not guaranteed to do so?

## Primary metrics

For each case:
- pointer candidate count;
- global lexical rank;
- rank within pointer candidate set;
- whether the composed route places target at rank 1;
- whether the non-target sibling remains a plausible lexical competitor.

## Interpretation

Prospective support for carrier complementarity requires the target to be non-unique under POINTER_ONLY and uniquely rank first under POINTER_THEN_LEXICAL.

A global lexical rank of 1 is allowed and does not invalidate the result; it means text is independently sufficient under this policy.

If the composed route fails, retain the failure. Do not change the page group, seed, or scoring rule.

## Claim ceiling

A positive result supports composition for this duplicate-pointer group.

It does not establish that composition is universally superior, that the pointer is minimal, or that human researchers use TF-IDF.