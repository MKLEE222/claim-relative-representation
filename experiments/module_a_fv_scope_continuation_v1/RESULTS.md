# Module A: Frankenstein C18 inherited-scope continuation results

Date: 2026-09-28
Status: EXECUTED SOURCE-GROUNDED DEVELOPMENT PILOT. NOT CONFIRMATORY TRANSFER OR MOTHER-PROBLEM CLOSURE.
Upstream: FrankensteinVariorum/collationWorkspace at 5a208f869ff1213defa000e3181d5315a072a15f.
Source materialization: Actions run 36371210016; artifact 10949441122; ZIP SHA-256 f8e080c1cb9af513db28115b0ddc98d0ed34f7a55af691d884eee47054a8f918.

## 1. What actually ran

A full scan of the pinned C18 published apparatus and raw manuscript source, construction of local research checkpoints, comparison of current and follow-up outputs, restoration with inherited scope or ordinary pinned source locators, matched wrong-locator controls, an independently implemented interval check, and bounded source-native branch traces.

No LLM calls, new historical gold labels, fabricated retractions, or new corpus holdouts were used. The pilot did not rerun the full CollateX pipeline; it used the published apparatus and replayed its encoded manuscript scope structure. Earlier R2 alignment reproduction retains its separate authority.

## 2. Population and source verification

- Published apparatus units: 493.
- Units containing nonempty manuscript text: 469.
- No-text units: 24, retained as explicit controls.
- Encoded addition spans: 112.
- Spans with start and end markers in different apparatus units: 53.
- Checkpoints entered while an addition was still open: 64.
- Start/end unit distance distribution: 0 -> 59; 1 -> 46; 2 -> 5; 3 -> 1; 5 -> 1.

For all 112 additions, the source and apparatus agree on identifiers, start attributes and enclosed character sequences after whitespace removal. No mismatch was observed.

An independent scanner reconstructs global character intervals and checks full text-segment containment without using the primary parser's active-scope stack. Both coarse membership and detailed place/hand profiles agree at all 493 checkpoints. This is implementation-level documentary verification, not independent historical judgement.

## 3. Natural collisions in the complete local view

Three collision classes, comprising six checkpoints, have identical full local apparatus payloads but different encoded insertion-scope status. No alternative source history was fabricated. The controlled operation is exporting a local apparatus unit without its global ordinal, source position, surrounding units or inherited state.

All indices below are 1-based app ordinals in the pinned file.

| Identical local reading | App pair | First member | Second member |
|---|---|---|---|
| to | 33 / 399 | inside encoded superlinear addition | outside encoded addition |
| that | 35 / 249 | inside encoded superlinear addition | outside encoded addition |
| or | 324 / 328 | outside encoded addition | inside encoded superlinear addition |

For each pair, all five witness readings, native normalized group descriptors, witness ordering, app/group/reading attributes and raw local strings agree. The serialized full app XML is also byte-identical, not merely a matching keyword.

Serialized local XML SHA-256 values:

- app 33 = app 399: 5eb2aa7cebd3da33947cf022f3eb05b823d3361caff9fbdbf0dec292062e7b21
- app 35 = app 249: 4c24634d50490854224c9e00f64585873e46cb76b827276be1d85269ba9bd2ae
- app 324 = app 328: 2dcaf76d9ba85fd732c7d02a879ed0987f98dd0e7913d562346a56267d0bec31

The current question is the published normalized comparison; it has the same answer in each pair. The follow-up asks whether the selected manuscript text falls inside an encoded addition and which scope can be inspected. That answer differs.

This proves a bounded local-interface ambiguity. Safe abstention, reporting alternatives, or asking for provenance remains possible. The entire source document is not identical, and a retained global locator distinguishes the cases.

The 'to' and 'that' cases share the same source addition. The three classes are NOT three independent corpora or three independent historical mechanisms.

## 4. Concrete source witnesses

Apps 33 and 35 lie inside:

    sga-add sID=c57-0015__main__d4e3200
    xml:id=c57-0015.05
    place=superlinear

Its enclosed source text is 'it proper to pursue that'. The start marker is in app 31 and the end marker in app 36. App 33 ('to') and app 35 ('that') do not repeat those boundary markers locally.

App 328 lies inside:

    sga-add sID=c57-0020__main__d4e4257
    place=superlinear

Its source content includes an internally cancelled 'or', followed by 'brother or son'. The selected local 'or' is within the addition. Start and end markers occur in apps 327 and 329.

OUTSIDE_ENCODED_ADDITION is a claim about these encoded scopes only. It does not establish that a historical inscription was never revised. Missing hand attributes are NOT_ENCODED; no author's hand is inferred.

## 5. Executed comparators and controls

| Interface / route | Current comparison | Follow-up result |
|---|---|---|
| Entire native encoded stream | preserved | all 469 text-bearing units resolved; 24 no-text controls retained |
| Complete local app only, without provenance or inherited context | all 493 comparisons preserved | at least the six exhibited checkpoints cannot be uniquely disambiguated from their local payload |
| Ordinary pinned source path + ordinal + source reopening | all 493 comparisons preserved | 469/469 text-bearing units match full-stream scope profiles; 24 controls match |
| Local app + source-derived open-scope state | all 493 comparisons preserved | 469/469 text-bearing units match full-stream scope profiles; 24 controls match |
| Correct versus wrong fixed-width source locator | current comparison unchanged for all six tested checkpoints | correct 6/6; wrong 0/6; locator bytes and source reopening cost matched |

The equal-size source locators are 139 canonical JSON bytes each. They differ only in the supplied version-bound ordinal. Correct and wrong pointers reopen the same file. The wrong route is not secretly corrected using the evaluator's intended target.

A separate wrong-scope swap also fails for all six cases, but it is only interface-matched: empty and nonempty scope states have different byte counts. It is NOT presented as a size-matched repair control.

## 6. Costs and the important null

Published apparatus source: 235462 bytes.

The simple linked baseline reads this full file once on a cold episode; a batch can cache it once. This is the implemented route, not a claim that every native system requires a whole-file transfer or that this is a minimum cost.

The list of source-derived open-scope states for all 493 checkpoints occupies 7135 canonical JSON bytes, with 2-140 bytes per checkpoint under this encoding. Construction required a full source-stream pass. This is extra information, not free knowledge or a global compression bound.

**Ordinary source-linked recovery already solves the tested continuation.** Therefore the pilot does NOT establish insufficiency of the original Frankenstein infrastructure and does NOT establish a novel repair advantage over ordinary provenance/navigation methods.

The supported distinction is narrower: a correct and complete local comparison view need not carry its inherited documentary scope; provenance plus lawful reopening or an explicit inherited-state summary can restore that scope.

## 7. Bounded source-native branch feasibility

The trace script reads the raw source rather than copying the pilot's reference excerpts.

For apps 33 and 35, inspecting the containing addition exposes xml:id=c57-0015.05. An earlier addition has next="#c57-0015.05". Following that actual source relation reconstructs:

    hereafter consider it proper to pursue that

For app 328, inspecting the containing addition exposes an internal mdel containing 'or'. A source-supported next operation can inspect which characters were cancelled inside the addition.

These traces establish source feasibility for a branching episode: different scope findings expose different native questions/operations. They do NOT measure autonomous question generation, adaptive scientific discovery, or successful selective belief revision. The outside-scope members produce no positive insertion-specific branch under this limited rule; other research questions are not ruled out.

## 8. Reproducibility and artifacts

Local pilot source SHA-256:
724beaf78b86abedb24ac23fbb1b62b5aa7822bf8b1c32445b8552edcc013fa8

Local final results.json SHA-256:
4fb4edba6e715b0f0863f74212997b37700818efe5e14ca3dfae6608567d80e4

Environment-independent scientific payload SHA-256 (canonical results excluding execution metadata):
5d25cd1bd505d6d916aeb602407337f89608a729ddddb77a76b59470171ae3fb

Native branch trace SHA-256:
5b974012d1002e08908bd4de8742ba688a4774c5e4c79ca9c5b56ba35ae2efe6

Commands:

    python pilot.py --download-sources
    python trace_native_branches.py

When source files are already present, omit --download-sources. Requires lxml. Source blob mismatches stop execution. The CI workflow replays the completed development experiment and checks the already-recorded substantive payload; it is not a fresh confirmatory study.

## 9. Scientific disposition

MODULE_A_SOURCE_GROUNDED_LOCAL_COLLISION = OBSERVED

NATIVE_OR_ORDINARY_SOURCE_LINKED_FAILURE = NOT_OBSERVED

SOURCE_NATIVE_BRANCH_FEASIBILITY = OBSERVED_UNDER_DECLARED_RULES

AUTONOMOUS_QUESTION_GENERATION = NOT_TESTED

SELECTIVE_BELIEF_REVISION = NOT_TESTED

LONG_HORIZON_MODULE_C = NOT_TESTED

INDEPENDENT_TRANSFER = NOT_TESTED

The next evidentiary obligation is an adaptive branching/revision test on a separately fixed episode set, with these ordinary recovery routes as strong baselines. The mother's problem is not declared closed, and no old result or Gate-II outcome is altered.
