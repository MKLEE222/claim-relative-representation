# Module F v1 — Published-erratum transfer: Urumtsi 1903 -> 1920

Date frozen: 2026-09-28
Status: PRE-EXECUTION HETEROGENEOUS REVISION-ECOLOGY PRESSURE TEST ON ALREADY-EXPOSED YULE-CORDIER SOURCES. NOT INDEPENDENT HISTORICAL VALIDATION.

## 0. Why this design is different from Whitman D/E

Whitman D/E uses digital-edition relation-state changes and Git revision events.

Module F uses a historical print erratum:

- a 1903 printed witness contains one reading;
- a 1920 published addenda/errata layer explicitly instructs the reader to correct that reading;
- the earlier witness remains a historical source object and must not be silently rewritten.

The test therefore concerns a correction overlay and its provenance, not destructive mutation of the 1903 witness.

## 1. Published editorial precedents used to constrain the protocol

This protocol was designed after reviewing established scholarly-editing practices, not by inventing a correction ontology from the desired outcome.

### TEI apparent-error representation

TEI P5 distinguishes the source reading from an editorial correction and recommends retaining both when useful for scholarly work:

https://www.tei-c.org/release/doc/tei-p5-doc/en/html/CO.html

TEI revision history separately records changes/corrections:

https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-revisionDesc.html

### Piers Plowman Electronic Archive versioning case

Paul A. Broyles, "Digital Editions and Version Numbering," Digital Humanities Quarterly 14.2 (2020).

https://www.digitalhumanities.org/dhq/vol/14/2/000455/000455.html

The published case documents that scholarly digital editions correct errors over time and argues that content versions and change history must remain intelligible and citable.

### Codex Zacynthius corrigenda

The published corrigenda to the Codex Zacynthius digital/print editions give location-specific corrections such as "for X, read Y", translations to replace, and explicit deletions/replacements, while the correction list can remain separate from the source edition pending integration.

https://sites.google.com/site/haghoughton/publications/zacynthius-corrigenda

### Electronic errata

Paul Fyfe, "Electronic Errata: Digital Publishing, Open Review, and the Futures of Correction," in Debates in the Digital Humanities (2012).

https://dhdebates.gc.cuny.edu/read/untitled-88c11800-9446-469b-a3be-3fdb36bfbd1e/section/4aefa6e6-d668-4acf-bc51-62c8451cce98

This is used only as conceptual prior art that correction history matters to scholarly information systems.

No novelty is claimed for recording an erratum, preserving original/corrected readings, or maintaining a change log.

## 2. Frozen primary sources

### 1903 witness

PDF:
https://archive.org/download/bookofsermarcopo001polo/bookofsermarcopo001polo.pdf

Expected SHA-256:
6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7

The six 1903 PDF pages used here are exactly the six pages frozen earlier for the independent second-pass review bundle:

PDF indices:
- 408
- 425
- 461
- 462
- 500
- 501

They were selected before Module F for five different historical review cases.

Module F does not add another 1903 page after inspecting token distributions.

The Urumtsi source is:
- printed p. 201
- PDF index 500

### 1920 correction witness

PDF:
https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf

Expected SHA-256:
dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941

Correction source:
- printed p. 50
- PDF index 63

The authoritative page image/source reads:

    P. 201, Line 12. Read the Governor of Urumtsi founded instead of found.

The source image remains authoritative; extracted text is an access representation.

## 3. Source-verified parent proposition

The 1903 p.201 sentence is decomposed into a bounded structured record:

- actor: Chinese Governor of Urumtsi
- parent action reading: found
- time: some years ago
- relative location: north-west of the Lob-nor
- river location: banks of the Tarim
- distance relation: within five days of Charkalyk
- object: a town bearing the same name
- site distinction: not on the same site as the Lop of Marco Polo
- base witness: 1903 printed p.201 / PDF index 500

The 1920 event changes only:

    action: found -> founded

No claim is made that the erratum independently proves the historical event itself occurred. It establishes the published editorial correction state.

## 4. Frozen collateral-control corpus

All six already-frozen 1903 review pages are scanned for exact lexical occurrences of the old form "found".

Pre-protocol inspection of the frozen bundle established two relevant exact occurrences:

1. Urumtsi p.201:
   "The Chinese Governor of Urumtsi found ... a town ..."

2. p.113:
   Sykes: "I found that there was a route which exactly fitted Marco's conditions ..."

The p.113 occurrence is a natural collateral control.
It must remain "found".

This is not a claim that every "found" occurrence in the whole 1903 book has been enumerated.

## 5. Update representation: provenance-preserving correction overlay

The evaluator never overwrites the 1903 source bytes/text.

A successful update creates an overlay record:

    base_witness
    target_identity
    old_reading
    corrected_reading
    correction_witness
    correction_scope

The current research reading is obtained by applying the overlay at query time.

Thus:

    historical witness preservation
    !=
    current corrected reading.

## 6. Parent-state arms

Both arms retain the same six 1903 page texts and therefore preserve the source corpus.

### S_CORPUS

Retain:
- six page identities;
- six extracted page texts.

Do NOT retain a pre-bound field saying which "found" occurrence is the Urumtsi action slot.

### S_TARGET_BOUND

Retain everything in S_CORPUS plus an explicit source-grounded binding:

    Urumtsi.action
    -> 1903 p.201 Urumtsi sentence / old token "found"

and the seven unaffected structured fields listed in section 3.

This additional binding is charged information.

## 7. Correction-event channel arms

All are controlled projections of the same natural 1920 erratum.

### Provenance envelope held constant

Every event arm is delivered in an immutable envelope identifying the correction witness as:

- 1920 addenda/errata layer;
- printed p.50 / PDF index 63;
- pinned 1920 source hash from section 2.

The ablation changes only the event's correction payload.
It does not erase knowledge of which published correction source delivered the event.

This prevents correction-source provenance from being confounded with correction-to-target binding.

### E_NATIVE_FULL

Retain:
- target page 201;
- printed line 12;
- context/subject: Governor of Urumtsi;
- old reading: found;
- corrected reading: founded.

This is the natural event content.

### E_CONTEXT_NEW

Retain:
- target page 201;
- context/subject: Governor of Urumtsi;
- corrected reading: founded.

Remove:
- explicit old reading.

This tests whether the old state can be supplied by the retained 1903 source.

### E_PAIR_ONLY

Retain only:

    found -> founded

Remove:
- page;
- line;
- subject/context.

This preserves the correction pair but removes correction-to-source binding.

It is a controlled ablation, not a claim that a real editor published such an underspecified erratum.

## 8. Access arms

### A_NONE

No additional correction-source access beyond the projected event channel.

The frozen parent state remains available.

### A_ERRATUM_REOPEN

Lawfully reopen the exact pinned 1920 p.50 erratum.

The full native correction event becomes available.

This tests whether source access can substitute for information projected out of the delivered event channel.

## 9. Matrix

For the one natural correction event:

    2 parent-state arms
  x 3 event-channel arms
  x 2 access arms
  = 12 cells.

Run all 12 once.

## 10. Candidate semantics

### Target binding

A correction overlay is valid only if the available interface uniquely determines one source target in the frozen six-page corpus.

For S_CORPUS + E_PAIR_ONLY + A_NONE:

- every exact token "found" in the six-page corpus is an admissible target candidate;
- no semantic or grammatical heuristic may choose among them.

For S_TARGET_BOUND:

- the retained Urumtsi.action binding may identify the target.

For E_NATIVE_FULL / E_CONTEXT_NEW:

- page/context information may identify the target.

For A_ERRATUM_REOPEN:

- the natural erratum may identify the target.

### Old reading

If an event channel omits the old reading, it may be recovered only from the uniquely identified parent source target.

### Corrected reading

Must be licensed by the event channel or by reopening the exact 1920 erratum.

## 11. Tasks

### T_CURRENT_ACTION

Determine the current corrected Urumtsi action description.

Target:

    founded

### T_TRANSITION_AUDIT

Determine the exact revision:

    found -> founded

and identify:
- parent witness;
- correction witness;
- correction target.

### T_WITNESS_PRESERVATION

Verify that the 1903 page text remains byte/text invariant in the research state.

The corrected reading must be represented as an overlay, not source mutation.

### T_LOCAL_STABILITY

Verify that these Urumtsi proposition fields are unchanged by the correction:
- actor
- time
- relative location
- river location
- distance relation
- object
- site distinction.

### T_COLLATERAL_STABILITY

Verify that the p.113 Sykes occurrence:

    I found that there was a route ...

remains unchanged.

## 12. Global-replacement wrong control

Apply the same lexical pair:

    found -> founded

to every exact old-token occurrence in the frozen six-page corpus.

This control has access to the same old/new strings as E_PAIR_ONLY but no target binding.

Expected evaluation is not frozen as a success requirement.

Report:
- number of replacements;
- whether the Urumtsi current reading becomes correct;
- whether p.113 is corrupted;
- whether the original source witness was destructively changed.

The wrong control is an intentionally invalid update strategy; it is not presented as a plausible editorial method.

## 13. Metrics

For every matrix cell:
- unique target candidate count;
- T_CURRENT_ACTION exact / ambiguous / unsupported;
- T_TRANSITION_AUDIT exact / ambiguous / unsupported;
- parent provenance exact;
- correction provenance exact;
- T_WITNESS_PRESERVATION;
- T_LOCAL_STABILITY: changed field count outside action;
- T_COLLATERAL_STABILITY;
- state payload bytes;
- event payload bytes;
- correction-source reopen bytes if used.

Also report:
- exact "found" token count across the frozen six-page corpus;
- page distribution of those occurrences;
- wrong-control collateral changes.

## 14. Primary hypotheses

H1 — correction-scope binding matters:

    S_CORPUS + E_PAIR_ONLY + A_NONE

can be non-determining even though the old/new lexical pair is correct.

H2 — state/event substitution:

    S_TARGET_BOUND + E_PAIR_ONLY

or

    S_CORPUS + E_CONTEXT_NEW

can restore exact update by carrying target identity on different sides of the interface.

H3 — source access substitution:

    A_ERRATUM_REOPEN

can repair an underspecified delivered event channel.

H4 — corrected state is not source mutation:

a valid interface can yield current action "founded" while preserving the 1903 witness's original "found".

## 15. Dispositions

ERRATUM_SCOPE_BINDING_SEPARATION:
at least one pair-only cell is ambiguous while a target-bound or context-bound cell is exact under the same source corpus.

PROVENANCE_PRESERVING_CORRECTION:
an exact current correction is obtained with the original 1903 witness unchanged.

COLLATERAL_CONTROL_PASS:
valid overlay update leaves p.113 "found" unchanged.

GLOBAL_REPLACEMENT_FAILS_SELECTIVITY:
the wrong control reaches the Urumtsi new word but also changes at least one non-target occurrence or mutates the source witness.

ACCESS_REPAIRS_EVENT_ABLATION:
A_ERRATUM_REOPEN makes an otherwise non-determining pair-only interface exact.

## 16. Claim ceiling

A positive result can support only:

> In a published historical erratum, exact correction requires not just the old/new lexical pair but a lawful binding of the correction to its source target. That binding may be supplied by retained research state, the correction notice itself, or source reopening. A provenance-preserving overlay can update the current scholarly reading without rewriting the earlier witness or collateral occurrences.

It cannot establish:
- that every print erratum has this structure;
- that "founded" is independently historical truth about the Governor's action;
- historian consensus;
- a globally minimal correction representation;
- independent historical replication, because Urumtsi was already used in R3 development.

## 17. Stop rule

Do not add more Yule-Cordier cases after outcome to improve Module F.

Do not expand from the six pre-frozen 1903 review pages to a hand-selected larger corpus after seeing ambiguity.

If Module F is positive, treat it as heterogeneous revision-ecology pressure evidence, not independent transfer.
