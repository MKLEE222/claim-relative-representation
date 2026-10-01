# R1 executable recovery and source-bound repair results

Date: 2026-09-26
Authority: retrospective native recovery plus explicitly controlled repair tests on already inspected corpora.
Authoritative run: GitHub Actions 36250962451.
Artifact: deepening-r1-results, artifact id 10909700096, archive SHA-256 2cd43d6eeb8380b55a44c558fa3ffa38b12515049c7d67c68e3d33d0b0c08fbf.

## Whitman

Pinned relation object:
- 1,444 valid relation records.
- Native whole-document consumer exactly reconstructs the registered printed-locus to manuscript endpoint-set output.

Natural record-local projection collisions:
- MS_LOCUS only: 91 ambiguous keys / 1,096 records.
- PRINT_LOCUS + MS_LOCUS: 25 ambiguous keys / 52 records.
- PRINT_LOCUS + MS_LOCUS + CERTAINTY: 20 ambiguous keys / 41 records.
- Adding LINK_INDEX still leaves 7 ambiguous keys / 15 records.

Whole-document controlled twin:
- link/group structure, loci, certainty and order fixed;
- two manuscript-file bindings swapped;
- registered endpoint output changes at 6 printed loci.

Prospectively frozen repair:
- correct group_id -> manuscript_file registry recovers the full endpoint output exactly;
- same-domain wrong-binding registry fails exact recovery;
- repair registry size: 6,384 canonical JSON bytes;
- the unaffected task remains exact.

## Faust

Pinned population:
- 22 relevant XML files;
- 1,089 eligible temp-pre assertions;
- zero missing source bundles;
- 53 multi-source assertions;
- 1,959 edge occurrences / 1,015 unique directed edges;
- 20 nontrivial SCCs;
- 612 internal edge occurrences / 207 unique internal edges.

The new consumer reads every source element and locator.

Assertion-level source-bundle ambiguity:
- FILE: 13 ambiguous keys;
- FILE + ORDERED_ITEMS: 44;
- FILE + ORDERED_ITEMS + SOURCE_COUNT: 39;
- FILE + ORDERED_ITEMS + SOURCE_LOCATORS: 0 on this frozen population.

Prospectively frozen repair candidates:
1. LOCATOR -> source URI set: nonfunctional, 28 conflicting keys;
2. FILE + LOCATOR -> source URI set: functional and exact;
3. FILE + ITEMS + LOCATOR -> source URI set: also functional and exact but not selected because candidate 2 already passes.

Selected repair:
- FILE + LOCATOR registry;
- 352 keys;
- 62,025 canonical JSON bytes;
- 0 failed assertions under the correct registry;
- 18 failed assertions after a same-interface wrong-binding swap;
- temporal structure remains unchanged.

Twenty natural FILE + ORDERED_ITEMS collision trials also give 20/20 exact correct-source repairs and 0/20 exact wrong-source repairs.

## Cross-corpus interpretation

Both corpora now instantiate the same auditable pattern:
1. execute a full-input native consumer;
2. declare the reduced consumer-visible projection;
3. emit concrete collision witnesses where present;
4. add an explicitly charged source-side repair;
5. compare correct versus equally shaped wrong binding;
6. keep an unaffected task invariant.

This supersedes the earlier field-membership minimality story. It supports a source-bound recovery/separation/repair method at the declared interfaces, not universal minimal carrier claims.
