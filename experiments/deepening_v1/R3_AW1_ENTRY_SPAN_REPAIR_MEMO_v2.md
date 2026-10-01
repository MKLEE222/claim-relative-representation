# R3-AW1 entry-span evaluator repair memo v2

Date: 2026-09-27
Status: EVALUATION-PLUMBING REPAIR BEFORE OPENING PASH/Great-Desert RESULTS

## Why a second repair is necessary

The first locator-only repair fixed the seed-side global-first-occurrence bug. It then revealed two remaining evaluator problems:

- Pashai: the frozen later entry could not be identified by requiring "Stein" and "Kafiristan" to occur inside one 180-word evaluation window.
- Great Desert: the 1903 chapter heading "Great Desert" and the already-frozen "evil spirits" seed passage are separated by more than the implementation's arbitrary 12,000-character proximity cap.

Neither is a scientific null.

## Repair discipline

No scientific policy changes.

Unchanged:
- task wording;
- frozen 1903 historical starting object;
- top-K = 12;
- IDF source;
- tokenizer;
- 180-word window;
- 90-word stride;
- ranker;
- full-object and native later-layer conditions;
- target identities;
- success metrics;
- no-retuning rule.

## Seed evaluation repair

The seed is a native paragraph at the already-frozen 1903 locus.

For Pashai:
- keep the unchanged anchors Pashai and Chitral;
- choose their closest occurrence pair;
- take the enclosing native paragraph.

For Great Desert:
- keep the unchanged anchors Great Desert and evil spirits;
- identify the evil-spirits occurrence nearest a Great-Desert occurrence;
- take the enclosing native paragraph around that source passage.
- the former 12,000-character cap is removed because it was an implementation assumption, not part of Generic Seed-Task Access Policy v1.

No 1920 target text is used in seed construction.

## Gold-target evaluator repair

The later gold targets are not redefined from target keywords.

They use entry identities frozen before R3-AW1:
- Pashai -> YC1920E-0030, page-verified at 1920 pp.34-35;
- Great Desert -> YC1920E-0049, page-verified at 1920 pp.48-49.

The evaluator reconstructs the same structural entry frame used by the existing R3 frame code, obtains each frozen entry's source character span, and scores a retrieval window as a target hit when that window overlaps the frozen entry span.

This changes only how the already-fixed gold target is recognized.

## Outcome rule

Only Pashai and Great Desert are run in v2.
Arbre Sec, Urumtsi and Tun-o-Kain retain their already-opened authoritative AW1 outcomes.
