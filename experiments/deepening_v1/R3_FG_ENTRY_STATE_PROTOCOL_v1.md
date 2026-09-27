# R3-F/G entry-state and carrier-substitution protocol v1

Date frozen: 2026-09-27
Status: PRE-OUTCOME. No R3-F/G retrieval result for the selected transfer acts has been opened.

## Question

When a scholar starts from an earlier Yule-Cordier locus rather than from a preassembled pair of passages, does the 1920 Addenda remain discoverable through the native backward-pointer carrier, and can retained textual content substitute when that carrier is unavailable?

This is a discoverability/recovery-path experiment, not a historical-truth or human-effort experiment.

## Frozen transfer acts

Use r3_fg_transfer_selection_v2.csv.

Selected historical acts:
- YC1920E-0021 — additive/corroborative Gulf-diet evidence;
- YC1920E-0022 — route-theory correction plus explicit qualification;
- YC1920E-0024 — Arbre Sec identification challenge;
- YC1920E-0049 — source-derivation attribution for the Great Desert folklore account.

The two YC1920E-0022 act strata share one target editorial entry and therefore one discovery target.

## Source objects

1903 Volume I: Project Gutenberg 10636
expected SHA-256: 7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5

1903 Volume II + 1920 Addenda: Project Gutenberg 12410
expected SHA-256: c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

Gutenberg is the digital-object target for this experiment. Page-image verification is a separate historical-authority obligation.

## Research entry state

HISTORICAL_START

The scholar is assumed to have:
- the earlier 1903 locus under study;
- its chapter/page bibliographic coordinate;
- a local seed window from the 1903 text.

The scholar is NOT supplied:
- the 1920 target entry;
- its actor;
- its relation label;
- a later-only name or term.

## Frozen 1903 anchors

S01 / YC1920E-0021:
Their food when in health consists of dates and salt-fish (tunny, to wit) and onions

S02-S03 / YC1920E-0022:
would lead me to suppose that he reached the Province of TUN-O-KAIN about Tabbas

S04 / YC1920E-0024:
There can be no doubt that the tree described is, as Marsden points out, a Chínár or Oriental Plane

S05 / YC1920E-0049:
when he tries to gain his company again he will hear spirits talking, and will suppose them to be his comrades

Each anchor must occur in the 1903 object after Unicode/whitespace normalization. The seed is a fixed ±900-character window around the first match.

## Later-entry population

Reconstruct the same structurally refined 1920 entry frame used by R3-A.

The expected frame is 223 accepted entries after the frozen structural exclusion rules.

Every selected target entry must match its frozen entry SHA-256.

## Condition NATIVE_POINTER

Consumer-visible inputs:
- chapter/page coordinate from HISTORICAL_START;
- native 1920 entry heads.

Operation:
reverse-follow the backward pointer by matching chapter plus page/range.

Report:
- number of candidate entries;
- target membership;
- target ordinal if multiple.

No lexical ranking is used for this condition.

## Condition BODY_LEXICAL

Consumer-visible inputs:
- fixed 1903 seed window;
- 1920 entry bodies;
- entry heads/pointers hidden.

Operation:
deterministic seed-side TF-IDF cosine ranking.

Rules:
- Unicode casefold;
- alphabetic tokens length >= 3;
- fixed English stop-list embedded in code;
- IDF fit on the 223 later-entry bodies plus the seed query;
- no target-only terms;
- no query tuning by case.

Report:
- full target rank / 223;
- cosine score;
- Hit@1/5/10/20;
- top-20 candidate IDs.

## Condition FULL_LEXICAL

Same TF-IDF rule but later entry head text is retained with the body.

This diagnoses whether the native pointer text itself contributes lexical retrieval even when the pointer is not directly followed.

## Primary comparisons

1. native pointer path: chapter/page -> later entry candidate set;
2. pointer-hidden lexical substitution: 1903 seed -> 1920 body ranking;
3. full lexical route: 1903 seed -> head+body ranking.

No scalar representation-quality score is computed.

## Recovery-profile recording

For each target, record scope inclusion, discoverability under each route, active basis, candidate/rank burden, and whether the target output is preserved under budget 20.

Do not infer human time or difficulty from rank.

## Positive carrier-substitution pattern

A strong substitution witness is:
- NATIVE_POINTER directly identifies the target or a small candidate set;
- BODY_LEXICAL also surfaces the same target under the frozen budget after the pointer is hidden.

Interpretation: the relation path is resilient because a second carrier substitutes.

## Burden-increase pattern

If BODY_LEXICAL recovers the target but at a materially larger candidate/rank burden than NATIVE_POINTER, report output preservation with profile non-equivalence.

## Basis-exhaustion pattern

If BODY_LEXICAL fails under the frozen budget after pointer hiding, do NOT immediately call the representation information-theoretically insufficient.

The result establishes failure of the registered alternative route.

A true insufficiency claim still requires a collision/separation witness or exhaustion of every registered lawful carrier.

## Claim ceiling

Permitted:
- native backward-pointer discoverability;
- deterministic lexical carrier substitution;
- output-equivalent/profile-different recovery;
- route-specific nulls.

Not permitted:
- human reading difficulty;
- universal searchability;
- historical truth;
- global superiority of layered representations.