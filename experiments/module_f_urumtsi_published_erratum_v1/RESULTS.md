# Module F results — published-erratum transfer: Urumtsi 1903 -> 1920

Date: 2026-09-28  
Status: EXECUTED HETEROGENEOUS REVISION-ECOLOGY PRESSURE TEST ON ALREADY-EXPOSED YULE-CORDIER SOURCES. NOT INDEPENDENT HISTORICAL VALIDATION.

Authoritative execution:
- first implementation-only failed run: 36380927078
- authoritative repaired run: 36381023412
- artifact: module-f-urumtsi-published-erratum-v1
- artifact ID: 10952955859
- artifact ZIP SHA-256: b4f8c27fe2696187f41367b36dedb84d3d0fc8139654d073b22e7ad73f128684
- results SHA-256: fff17d4d2bf909cb781a362e487b3556ab51ed91a97c330393967a59cc56bb44

The first run terminated before the matrix because PDF text extraction collapsed "of found" into "offound". EVALUATOR_REPAIR_v1.md froze the verifier-only repair before rerun. No source, corpus, arm, metric, or hypothesis changed.

## 1. Why the correction is represented as an overlay

The experiment does not rewrite the 1903 source.

The 1903 witness remains an immutable historical source object containing:

    The Chinese Governor of Urumtsi found ...

The 1920 addenda/errata layer supplies the later correction:

    P. 201, Line 12.
    Read the Governor of Urumtsi founded instead of found.

The updated research state is represented as a provenance-bearing correction overlay:

    base witness
    + correction target
    + old reading
    + corrected reading
    + correction witness

This follows established scholarly-editing practice rather than inventing destructive source mutation as the update mechanism.

Relevant published/standard precedents used before protocol freeze:
- TEI P5 apparent-error representation: original and corrected readings can both be retained;
- TEI revisionDesc/change: correction history can be recorded separately;
- Broyles 2020 on Piers Plowman Electronic Archive versioning: published editions require legible, citable change histories;
- Codex Zacynthius corrigenda: location-specific "for X, read Y", replacement and deletion notices can remain separately published pending integration;
- Fyfe 2012 on electronic errata and scholarly correction.

See PROTOCOL.md for exact references.

## 2. Frozen source corpus

The 1903 corpus is not hand-expanded after observing the correction.

It is exactly the six 1903 pages frozen earlier for the independent second-pass review bundle:

- printed p.113
- p.128
- p.164
- p.165
- p.201
- p.202

Source PDF SHA-256:

    6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7

The 1920 correction page is printed p.50 / PDF index 63.

Source PDF SHA-256:

    dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941

## 3. Natural collateral structure

Across the six frozen 1903 pages, exact token scanning finds two occurrences of:

    found

### p.113

Sykes:

    I found that there was a route which exactly fitted Marco's conditions ...

### p.201

Urumtsi:

    The Chinese Governor of Urumtsi found some years ago ...

Thus the old/new pair:

    found -> founded

does not uniquely determine a correction target in the already-frozen source corpus.

This gives a natural collateral control that was not added after Module F outcome.

## 4. Parent proposition and natural correction

The source-verified p.201 proposition retains:

- actor: Chinese Governor of Urumtsi
- time: some years ago
- relative location: north-west of the Lob-nor
- river location: banks of the Tarim
- distance relation: within five days of Charkalyk
- object: a town bearing the same name
- site distinction: not on the same site as the Lop of Marco Polo
- action in 1903 witness: found

The 1920 correction changes only the action reading:

    found -> founded

Module F makes no independent claim that "founded" is historical truth about the Governor's real action. It is the published corrected editorial reading.

## 5. Matrix

Two parent-state arms:

- S_CORPUS: six page texts; no pre-bound Urumtsi.action target
- S_TARGET_BOUND: same corpus plus explicit Urumtsi.action -> p.201 "found" binding

Three correction-event channels:

- E_NATIVE_FULL: page/context + old/new
- E_CONTEXT_NEW: page/context + corrected reading; old reading omitted
- E_PAIR_ONLY: old/new pair only; locator/context removed

Two access arms:

- A_NONE
- A_ERRATUM_REOPEN

Total:

    2 x 3 x 2 = 12 cells

All event channels retain the same correction-witness provenance envelope.

## 6. Native and contextual correction channels

With S_CORPUS and no source reopening:

### E_NATIVE_FULL

Candidate targets:
1

Result:
- current action: EXACT
- transition audit: EXACT
- collateral p.113 reading stable: YES
- 1903 witness preserved: YES

### E_CONTEXT_NEW

Candidate targets:
1

Even without the explicit old reading, the retained parent page supplies:

    found

and the context/page binding identifies the Urumtsi action.

Result:
- current action: EXACT
- transition audit: EXACT
- collateral stable: YES
- witness preserved: YES

Thus an incoming correction need not redundantly carry every old-state value if the retained source state lawfully supplies it.

## 7. Old/new pair without scope is non-determining

The critical transfer result is:

    S_CORPUS
    + E_PAIR_ONLY
    + A_NONE

The delivered event says only:

    found -> founded

The frozen corpus contains two admissible exact old-token targets:

    1903 p.113
    1903 p.201

Therefore:

- candidate targets: 2
- current Urumtsi action: AMBIGUOUS
- transition audit: AMBIGUOUS
- collateral stability: NOT GUARANTEED

The two compatible research states include:

1. correct Urumtsi overlay:
       p.201 found -> founded
       p.113 remains found

2. wrong Sykes overlay:
       p.113 found -> founded
       p.201 remains found

Hence:

    correct old/new lexical pair
    !=
    correctly scoped published correction

when target binding is absent from state, event, and access.

## 8. State binding can substitute for event binding

For:

    S_TARGET_BOUND
    + E_PAIR_ONLY
    + A_NONE

the event remains only:

    found -> founded

but the retained state already contains:

    Urumtsi.action -> p.201 old token "found"

Result:
- candidate targets: 1
- current action: EXACT
- transition audit: EXACT
- collateral stable: YES
- witness preserved: YES

Thus the same target-binding obligation may be supplied by the retained research state rather than repeated in the correction message.

## 9. Source access can substitute for delivered event detail

For:

    S_CORPUS
    + E_PAIR_ONLY
    + A_ERRATUM_REOPEN

the delivered pair-only channel is initially ambiguous.

Lawful reopening of the exact pinned 1920 erratum supplies:

- p.201
- Governor of Urumtsi context
- found -> founded

Result:
- candidate targets: 1
- current action: EXACT
- transition audit: EXACT
- collateral stable: YES
- witness preserved: YES

Therefore the target-binding obligation may also be delegated to lawful correction-source access.

## 10. Destructive global replacement fails selectivity

A deliberately invalid control applies:

    found -> founded

to every exact old-token occurrence in the six-page 1903 corpus.

Result:
- replacements: 2
- changed printed pages: 113 and 201
- Urumtsi new word becomes correct: YES
- Sykes p.113 is corrupted: YES
- historical source witness is mutated: YES

The resulting p.113 reading becomes:

    I founded that there was a route ...

This control shows why "the target word is now correct" is an insufficient update criterion.

A warranted correction must also preserve correction scope and unaffected evidence.

## 11. Local proposition stability

Every exact valid overlay changes only:

    action

The following fields remain unchanged:

- actor
- time
- relative location
- river location
- distance relation
- object
- site distinction

Observed non-action field changes:

    0

This is selective proposition revision rather than full-record replacement.

## 12. Witness preservation

Every valid matrix update leaves the 1903 extracted source text invariant.

The corrected current reading is computed from:

    immutable base witness
    + correction overlay

Therefore:

    current scholarly reading = founded

can coexist with:

    1903 historical witness reading = found

This distinction is methodologically aligned with textual-editing practices that preserve source readings and correction history.

## 13. Information footprint

Canonical implementation payloads:

### Parent state

S_CORPUS:
29,174 bytes

S_TARGET_BOUND:
29,628 bytes

### Delivered event

E_NATIVE_FULL:
283 bytes

E_CONTEXT_NEW:
251 bytes

E_PAIR_ONLY:
215 bytes

### Correction page reopening

Extracted p.50 text:
2,565 bytes

These are implementation encodings, not minimum information bounds.

## 14. Scientific dispositions

ERRATUM_SCOPE_BINDING_SEPARATION = YES

PROVENANCE_PRESERVING_CORRECTION = YES

COLLATERAL_CONTROL_PASS = YES

GLOBAL_REPLACEMENT_FAILS_SELECTIVITY = YES

ACCESS_REPAIRS_EVENT_ABLATION = YES

All were frozen before the successful matrix execution.

## 15. Cross-ecology interpretation

Whitman Module E established in a digital-edition relation ecology:

    aggregate revision information
    !=
    identity-bound selective revision

Module F establishes the analogous bounded mechanism in a historical print-corrigendum ecology:

    old/new correction pair
    !=
    source-scoped correction

In both cases the missing distinction can be supplied through different lawful carriers:

    retained state
    OR event binding
    OR source access

The two experiments differ materially in revision mechanism:

Whitman:
- relation identities;
- certainty status;
- add/remove topology;
- Git-versioned digital source.

Urumtsi:
- lexical/action reading;
- printed page/line correction;
- earlier witness + later erratum;
- provenance-preserving overlay.

This supports heterogeneous mechanism transfer more strongly than repeating the same digital relation task.

It is still not independent historical replication because Urumtsi was already used to develop R3.

## 16. Revised bounded claim

Supported:

> For a source-grounded scholarly correction, knowing the replacement values is not enough when multiple source loci are compatible with those values. Exact selective revision requires the correction-to-target distinction to be available at decision time from retained state, the correction event, lawful source access, or a declared composition. A provenance-preserving overlay can update the current reading while preserving the earlier witness and unrelated occurrences.

Not supported:
- universal necessity of page/line locators;
- one globally minimal correction schema;
- independent truth of the corrected factual proposition;
- whole-book prevalence;
- historian consensus;
- independent cross-domain replication.

## 17. Consequence for the mother problem

Module F strengthens the dynamic formulation:

    DynamicResearchability(S_t, E_t, A_t, T)

The relevant sufficiency question is not:

    Did the representation store the new word?

It is:

    Does the available information interface preserve enough target,
    provenance, and revision scope to make the warranted update selective
    and auditable without corrupting unaffected evidence?

This is the cross-ecology obligation carried forward from Module E.
