# Module G v1 — Confirmatory transfer on published Codex Zacynthius corrigenda

Date frozen: 2026-09-28
Status: PRE-SOURCE-INSPECTION CONFIRMATORY TRANSFER PROTOCOL.

## 0. Confirmatory status

Module G is the first correction corpus in this project chosen specifically to test the dynamic-sufficiency mechanism after Modules E/F had already fixed the mechanism:

    current state
    + correction event
    + lawful source access
    -> selective warranted update

Codex Zacynthius did not participate in:
- the original R3 mechanism discovery;
- Whitman Modules B2-C-D-E;
- Urumtsi Module F;
- the design of the state/event/access decomposition.

Before this protocol was committed, the following were inspected:
- the public Codex Zacynthius corrigenda page;
- public metadata for the project and data deposits;
- repository commit history and tree/blob metadata.

The XML file bodies at the frozen parent commit were NOT inspected before protocol freeze.

No correction event may be removed after source inspection because it is awkward, absent, already integrated, non-executable, or null.

## 1. Published scholarly source ecology

### Digital edition

The Codex Zacynthius digital edition was produced by the AHRC-funded Codex Zacynthius project and launched through Cambridge Digital Library in 2020.

The project released TEI P5 XML transcriptions under CC BY 4.0.

### Published corrigenda

Public corrigenda:
https://sites.google.com/site/haghoughton/publications/zacynthius-corrigenda

The page states that errors and oversights reported after publication are listed separately and may be integrated into online resources later.

The confirmatory event population is the COMPLETE set currently listed under:

    DIGITAL EDITION: UNDERTEXT (and TRANSLATION)

The "DIGITAL EDITION: OVERTEXT" section is not part of the positive correction population because it states that no corrections have yet been reported.

## 2. Frozen parent source state

Repository:
itsee-birmingham/codex-zacynthius-xml

Parent commit:
2bc9ef70a5d3635e98b5a6b327833c57a5b0a67f

Commit date:
2020-07-31T10:44:51Z

Commit message:
initial commit of all xml transcriptions

This is the first XML commit in the public repository.
All later commits in the repository history observed before protocol freeze affect only README/.gitignore metadata.

Frozen parent blobs:

- L299-lectionary.xml
  SHA-1 blob: 2ecebd8b2b1068c4d9999b17dbed9ed0e5858eaf
  bytes: 3,392,970

- Zacynthius-catena-translation.xml
  SHA-1 blob: 97e51cffa117b6a0e18c9879b5ecf3e489f26a0b
  bytes: 919,481

- Zacynthius-catena.xml
  SHA-1 blob: 45116ec9174e692bf0aff7b6e5ca6d6536c47d3a
  bytes: 1,165,268

- Zacynthius-gospel-translation.xml
  SHA-1 blob: 0e90aabadfe1143df0bc84abbaf5226cf3ee010e
  bytes: 235,723

- Zacynthius-gospel.xml
  SHA-1 blob: bd0bac8cd394df94e385c007241e6c00c27194ba
  bytes: 328,075

No file is excluded before inspection.

## 3. Complete correction-event population

All four undertext/translation corrigenda are retained.

### CZ-C1 — fol. IIIr — insertion

Published correction:
before the rubricated "ευαγγελιον" in the middle of fol. IIIr, add/recognize the section numbers alpha and beta with overlines in black ink.

Operation class:
INSERT / ADD OMITTED SOURCE CONTENT

### CZ-C2 — fol. XIIIv, Extract 060-1 — Greek text + translation replacement

Published correction:
replace the previously published Greek reading associated with "the Saviour of the world" with the corrected Greek reading associated with "the common Saviour".

Operation class:
REPLACE SOURCE TRANSCRIPTION + LINKED TRANSLATION

The evaluator preserves the exact Unicode strings from the public corrigenda record mechanically; no normalized substitute is hand-authored after XML inspection.

### CZ-C3 — fol. XVr, Extract 072-2 — source/title reference replacement

Published correction:
replace the published "On Numbers" identification with "Sermon 115", together with the corresponding Greek abbreviated form.

Operation class:
REPLACE TEXTUAL IDENTIFICATION / REFERENCE

### CZ-C4 — fol. XVIIIv, Extract 081-2 — translation + CPG reference revision

Published correction:
- revise the English translation of "εν υπακοη" to "in a Hymn";
- change CPG 7058 to CPG 7072.

Operation class:
LINKED MULTI-FIELD REVISION

No event is selected by whether the parent XML contains the expected old value.

## 4. Parent-state arms

### S_TEI

Retain all five frozen TEI XML files exactly.

The evaluator may use:
- element hierarchy;
- attributes;
- XML IDs;
- milestones;
- page/folio labels;
- extract identifiers;
- text-node order.

No correction-derived locator index is manually added.

### S_TEXT_ONLY

Retain:
- source file identity;
- linear text-node sequence and document order.

Drop:
- XML element names;
- attributes;
- xml:id;
- structural hierarchy.

This projection tests whether readable content alone carries the target distinctions exposed by the published corrigenda.

The text-only projection must be generated mechanically from S_TEI before correction matching.

## 5. Event-channel arms

Every event arm remains wrapped in the same immutable provenance envelope identifying:
- the public Codex Zacynthius corrigenda page;
- the specific correction ID CZ-C1...CZ-C4.

Only correction payload is projected.

### E_PUBLISHED_FULL

Retain the complete published correction information relevant to execution:
- folio;
- extract identifier where present;
- operation class;
- old/source-side value where stated;
- corrected/new value;
- linked second field where present.

### E_LOCATOR_RESULT

Retain:
- folio;
- extract identifier where present;
- operation class;
- corrected/new value(s).

Remove:
- explicit old/source-side value(s), when the correction has one.

The parent source must supply the old state.

For CZ-C1, which is an insertion/omission correction, this arm may be identical to E_PUBLISHED_FULL with respect to old-value content. That degeneracy is retained rather than repaired.

### E_TARGETLESS_OPERATION

Retain:
- operation class;
- old/new values when stated;
- corrected insertion/result payload.

Remove:
- folio;
- extract identifier;
- any correction-specific source-location context.

This is a controlled ablation of the published event, not a claim about actual editorial practice.

## 6. Access arms

### A_NONE

Use only retained parent state + delivered correction channel.

### A_CORRIGENDA_REOPEN

Lawfully reopen the exact public corrigenda entry.

This restores the full E_PUBLISHED_FULL event payload for that correction.

No later XML, corrected transcription, manuscript image, secondary commentary, or fuzzy web search may be introduced to rescue execution in Module G v1.

## 7. Full factorial

For each of 4 corrections:

    2 parent-state arms
  x 3 event-channel arms
  x 2 access arms
  = 12 cells

Total:

    48 cells.

All 48 must be executed once.

## 8. Candidate-target semantics

The evaluator does NOT ask whether a human can guess the intended location.

It asks whether the declared information interface uniquely identifies an executable correction target in the frozen parent representation.

### TEI target candidates

Candidate spans may be identified only through:
- exact/normalized old values supplied by the correction;
- structural locators supplied by the correction;
- generic TEI structure already present in S_TEI;
- exact source ordering;
- linked correction fields when explicitly part of the same published event.

No correction-specific hand-coded XML path may be added after source inspection.

### Text-only target candidates

Candidates are spans in the mechanically flattened text projection.

If a published folio/extract locator is not represented in the flattened text, it cannot be treated as free decoder knowledge.

### Unicode normalization

Before matching:
- preserve original source bytes/hashes;
- Unicode matching may use NFC;
- whitespace may be normalized for candidate matching;
- punctuation/diacritics may NOT be silently removed unless the same transformation is declared globally before any correction outcome.

Report every normalization used.

## 9. Correction overlay

Like Module F, the parent XML is immutable.

A successful correction creates an overlay:

    correction_id
    parent source identity
    target span identity
    old state / verified parent state
    corrected state
    correction provenance
    operation type

The overlay must not overwrite the frozen parent XML.

For linked corrections CZ-C2 and CZ-C4, all linked fields explicitly published in the correction must be represented in the same correction transaction.

## 10. Tasks

### T_TARGET

Is the exact correction target, or exact linked target set, uniquely determined?

### T_RESULT

Is the exact corrected result uniquely determined?

### T_TRANSITION

Is the exact parent -> corrected transition uniquely determined, including old/source state where applicable?

### T_SELECTIVITY

Does the correction alter only the published target span(s) and leave all other parent spans unchanged?

### T_WITNESS_PRESERVATION

Are all five parent XML blobs byte-identical before and after applying the overlay?

### T_LINKED_ATOMICITY

For CZ-C2 and CZ-C4:
does the available interface determine the complete linked correction transaction rather than only one of its fields?

## 11. Wrong controls

Wrong controls are generated mechanically and globally, before interpreting any one correction.

### W_GLOBAL_MATCH

Apply the event's old->new replacement or insertion condition to EVERY parent span matching the source-side lexical condition, without the published folio/extract binding.

Report:
- number of modified targets;
- whether the intended correction result is reached;
- collateral target count;
- whether parent witness bytes were destructively changed in the simulated wrong strategy.

### W_LOCATOR_SHUFFLE

If at least two corrections expose compatible locator-shaped fields, permute published locators among corrections while preserving:
- correction payload;
- locator field cardinality;
- correction count.

Only execute a shuffle when the permuted locator schema remains syntactically compatible.
If no valid nontrivial shuffle exists, report NOT_IDENTIFIABLE.

Do not hand-pick a wrong locator after observing source matches.

## 12. Outcomes per correction

Every correction receives one of:

- FULL_EXECUTABLE_EXACT
- FULL_EXECUTABLE_AMBIGUOUS
- FULL_TARGET_ABSENT
- FULL_SOURCE_STATE_MISMATCH
- LINKED_PARTIAL_ONLY
- REPRESENTATION_CANNOT_EXPRESS_LOCATOR

No correction is discarded from the denominator.

## 13. Primary metrics

Per correction and matrix cell:
- source files searched;
- target candidate count;
- exact target-set recovery;
- exact result recovery;
- exact transition audit;
- linked-field completeness;
- collateral candidate/changes;
- witness preservation;
- state payload bytes;
- event payload bytes;
- correction-source reopen bytes.

Aggregate:
- 4/4 full-channel executability count;
- exact target count by state arm;
- exact target count by event arm;
- target-binding separation count;
- linked-atomicity count;
- wrong-control collateral failures.

Do NOT treat four corrections as independent statistical samples.
They are a finite published correction set from one editorial project.

## 14. Pre-registered dispositions

### PARENT_SNAPSHOT_COMPATIBLE

All five pinned XML blobs are fetched and parsed at the declared commit.

### FULL_CORRIGENDA_EXECUTABILITY

Report x/4 corrections for which:

    S_TEI + E_PUBLISHED_FULL + A_NONE

is exact for target, result, and transition.

No threshold is required for scientific validity.

### TARGET_BINDING_TRANSFER

At least one correction is exact under E_PUBLISHED_FULL but non-determining under E_TARGETLESS_OPERATION with the same parent state/access.

### STATE_STRUCTURE_CONTRIBUTION

At least one correction is exact under S_TEI but non-determining under S_TEXT_ONLY for the same event/access interface.

### ACCESS_REPAIRS_CHANNEL_ABLATION

At least one targetless or old-value-ablated cell becomes exact when A_CORRIGENDA_REOPEN is enabled.

### LINKED_CORRECTION_ATOMICITY

For CZ-C2 and/or CZ-C4, the full published event uniquely determines the complete linked transaction.

### PROVENANCE_PRESERVING_TRANSFER

At least one exact correction is represented as an overlay while all five parent XML blobs remain unchanged.

### GLOBAL_MATCH_FAILS_SELECTIVITY

At least one W_GLOBAL_MATCH strategy reaches an intended replacement while also modifying one or more non-target spans.

## 15. Confirmatory interpretation rule

Module G counts as a confirmatory mechanism transfer only for claims that were frozen before XML inspection.

Positive transfer can support:

> In a previously unused scholarly edition and its complete published digital corrigenda set, selective correction depends on information jointly available from retained representation, correction-event structure, and lawful correction-source access. Replacement values without correction-to-target binding can be insufficient, and provenance-preserving overlays can update scholarly state without rewriting the parent witness.

A null or partial result must be retained.

If all targetless operations are uniquely executable, TARGET_BINDING_TRANSFER fails.

If the published corrections cannot be mapped to the frozen XML snapshot, report source/version incompatibility rather than changing parent version.

If S_TEXT_ONLY performs as well as S_TEI, STATE_STRUCTURE_CONTRIBUTION fails.

## 16. Claim ceiling

Even a fully positive Module G does NOT establish:
- a universal minimal representation;
- all digital editions require TEI;
- the corrigenda are independent historical truth;
- four corrections are four independent replications;
- the same mechanism holds in every edition ecology;
- human editorial cognition.

It may establish an independent project-level transfer of the bounded dynamic-sufficiency mechanism to a correction corpus that did not participate in mechanism development.

## 17. Stop rule

After this protocol commit:
- do not change the parent commit;
- do not remove a correction;
- do not add correction-specific XML paths;
- do not broaden normalization to rescue misses;
- do not inspect later repository versions to repair absent targets;
- do not replace Codex Zacynthius with another corpus based on outcome.

Any source-contract repair must be documented as an evaluator/source-contract correction and must not change the scientific population or success rules.
