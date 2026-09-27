# R3-AW1 locator repair memo

Date: 2026-09-27
Status: IMPLEMENTATION REPAIR BEFORE OPENING RESULTS FOR THREE STOPPED CASES

R3-AW1 v1 opened valid results for Urumtsi and Tun-o-Kain, but Pashai, Arbre Sec, and Great Desert stopped before query construction because the seed locator selected the first global occurrence of the first anchor (often a table-of-contents or earlier mention) and then failed to find the second anchor locally.

This is an implementation failure, not a scientific null.

The repair does not change:
- inquiry;
- seed anchor strings;
- task wording;
- target anchors;
- forbidden target-only terms;
- 180-word window;
- 90-word stride;
- top-K=12;
- IDF source;
- ranker;
- later-layer rule;
- metrics.

Only the locator is repaired:

1. enumerate all occurrences of the unchanged seed anchor A;
2. enumerate all occurrences of unchanged seed anchor B;
3. choose the pair with minimum character distance;
4. require distance <= 12,000 characters;
5. construct the same local seed span around that pair.

Only the three previously stopped cases are rerun. Urumtsi and Tun-o-Kain v1 outputs remain the opened authoritative v1 results and are not rerun in this repair.
