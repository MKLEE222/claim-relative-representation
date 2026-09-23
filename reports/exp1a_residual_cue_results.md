# Experiment 1A results - residual-cue leakage

Date: 2026-09-23
GitHub Actions run: 35882450291
Commit: 90e30a1b8b6ff7865a1fbd9bc9a0c0051bef5785

## Result

The metadata-only one-coordinate intervention family does **not** generally make the targeted relation unavailable.

Residual lexical cues remained after explicit-coordinate removal in:

- attribution: 7/10 events
- temporal order: 5/10 events
- evidence relation: 7/10 events
- claim binding: 7/10 events

The CI run completed successfully and the intervention invariant tests remained green.

## Interpretation

This is a negative result for the naive main-effect design.

For many Yule-Cordier events, historically important relations are **text-entangled**: actor names, source-reporting constructions, challenge language, cross-references, and subject terms are present in the words themselves. Nulling a structured field while holding substantive text fixed therefore often produces:

`explicit -> recoverable`

rather than:

`explicit -> unavailable`.

PM03 is the clearest carrier: attribution, temporal relation, evidential direction, and claim binding all remain lexically cued even after their structured coordinates are removed.

## Scientific consequence

The project should not use metadata-only ablation as if it created information loss.

The representational object now needs at least three separable states:

1. **explicit** - typed relation available directly;
2. **recoverable** - relation absent structurally but recoverable from retained local or cross-layer cues;
3. **unavailable** - required relation cannot be recovered from the representation without supplementation.

A fourth state, **unresolved**, remains necessary when retained cues license more than one material relation assignment.

## Redesign trigger

Experiment 1A activates the preregistered redesign condition.

The next intervention study should target **reconstruction burden / recovery depth** rather than assume binary preservation versus loss.

A candidate recovery-depth scale is:

- D0: explicit structured relation;
- D1: recoverable from the local span itself;
- D2: requires local note/chapter context;
- D3: requires cross-layer/page/edition traversal within the digital object;
- D4: requires external witness or source registry;
- U: unavailable from the representation.

This scale must be frozen and independently coded before claim-state outcomes are opened.

## Boundary

The detector is lexical and conservative. Its positive result proves that a direct textual cue survives; its negative result does not prove semantic unavailability. The 7/10 and 5/10 counts are mechanism diagnostics for the current ten-event carrier, not population frequencies.
