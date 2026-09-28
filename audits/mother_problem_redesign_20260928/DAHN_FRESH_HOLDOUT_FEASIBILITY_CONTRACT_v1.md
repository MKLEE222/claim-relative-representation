# Fresh holdout candidate audit v1 — DAHN Berlin Intellectuals correspondence

Date frozen: 2026-09-28
Status: PRE-SCAN HOLDOUT FEASIBILITY CONTRACT. NOT AN EXPERIMENTAL RESULT.

## 1. Purpose

This audit asks whether the DAHN Berlin Intellectuals correspondence can support the final missing empirical burden for the mother problem:

    discovery
    + multi-event sustained inquiry
    + substantive warrant
    + delayed reuse under one unchanged candidate interface

The project is a fresh ecology for this research program. It did not participate in Modules A-G or in the design of DynamicResearchability.

## 2. Frozen source

Repository:
FloChiff/DAHNProject

Branch/head:
master at
e7d4a81d42ea10a3d672e5c0869f033a8c2c8149

Primary scope for the feasibility scan:

    Correspondence/Berlin_Intellectuals/Corpus/*.xml

Indexes, guidelines, correction scripts and other correspondence collections may be used only as generic schema/context documentation during this feasibility stage. They are not eligible episode files unless a later protocol explicitly freezes them.

## 3. Why this project is a plausible discovery holdout

The public encoding guidelines distinguish:
- docDate: date actually written on the manuscript;
- origDate: editor's asserted actual origin date, which may be a supposition;
- correspondence metadata;
- responsibility-bearing editorial notes;
- revision history.

Therefore a letter can in principle expose a live scholarly distinction such as:

    written/visible date
    !=
    warranted chronology / origin date

without the evaluator supplying a follow-up question.

This is only a source-feasibility hypothesis until the corpus scan is executed.

## 4. Root research task

The root task is fixed before scanning:

> Construct a source-grounded chronological account of the correspondence while preserving any letter whose temporal placement is not uniquely warranted by the currently available evidence.

The system is NOT supplied with a list of letters having date conflicts and is NOT asked a per-letter question such as "is this date wrong?"

A discovery event occurs only if the available research state itself exposes an eligible temporal distinction under section 5.

## 5. Eligible live-distinction grammar

A corpus document is discovery-eligible if, in the frozen source, at least one of the following holds.

### D1 — explicit date disagreement

Two independently encoded date carriers attached to the same document disagree after ISO normalization, for example:
- docDate versus origDate;
- docDate versus correspAction/sent date;
- origDate versus correspAction/sent date;
- explicit source/postmark date versus one of the above.

### D2 — bounded uncertainty

A date carrier is explicitly encoded as uncertain, approximate, ranged, notBefore/notAfter, or otherwise non-singleton, while another source-grounded carrier supplies a competing or narrowing temporal constraint.

### D3 — explicit contradiction/commentary

A responsibility-bearing note/history statement explicitly says that a written date, postmark, archival date or other date signal is incorrect, contradictory, inferred, or otherwise requires adjudication.

### D4 — cross-document temporal constraint

A letter has a source-grounded relation to another document/event whose dated relation creates a temporal incompatibility or narrowing constraint that is encoded in the corpus rather than invented by the evaluator.

D4 is used only if the relation is explicit and machine-addressable.

## 6. Ineligible triggers

The following do NOT by themselves create a discovery episode:
- two duplicated encodings of the same date;
- formatting differences only;
- revisionDesc maintenance timestamps;
- file creation/modification dates;
- inferred date conflict based only on filename numbering;
- language translation differences;
- an evaluator-supplied historical guess.

## 7. Feasibility scan outputs

The scan must report the complete Berlin_Intellectuals/Corpus population and classify every XML document as:

- ELIGIBLE_D1
- ELIGIBLE_D2
- ELIGIBLE_D3
- ELIGIBLE_D4
- MULTI_TRIGGER
- NO_LIVE_TEMPORAL_DISTINCTION
- PARSE_ERROR / CONTRACT_UNRESOLVED

For every eligible document report:
- path;
- all machine-readable date carriers and source locations;
- whether carriers agree/disagree;
- uncertainty attributes;
- responsibility-bearing notes relevant to the date;
- source handles/facsimile availability if encoded;
- related document identifiers if applicable;
- revisionDesc separately, never treated as historical evidence.

No favorable subset is selected at this stage.

## 8. Evidence-release feasibility

For each eligible episode, the scan should determine whether the source supports at least two independent evidence layers that could be revealed lawfully in sequence, for example:

    surface/doc date
    -> manuscript/history metadata
    -> correspondence relation / explicit note / source image handle

This stage does NOT hide evidence or run a policy. It only determines whether a later prospective protocol could freeze a nontrivial source-release schedule.

## 9. Multi-event feasibility

A candidate episode is especially valuable if the frozen source also contains:
- one later evidence item that changes the warranted temporal state;
- one encoded item that is irrelevant to the temporal conclusion;
- at least one unresolved alternative or bounded interval that should survive an intermediate step;
- a later query requiring reuse of earlier provenance/evidence.

These are descriptive feasibility flags, not selection weights.

## 10. Freshness and anti-cherry-picking rule

The final holdout protocol, if DAHN passes feasibility, must be based on:
- all eligible episodes under a prospectively frozen sampling rule; or
- a predeclared random/deterministic subset rule based only on source identity, not observed outcome.

Do not select episodes because a particular representation fails.

## 11. Pass criteria for DAHN as final holdout candidate

DAHN remains a viable candidate only if the scan finds:

1. at least 5 source-grounded eligible temporal-conflict/uncertainty episodes;
2. at least 3 episodes with two or more independent evidence layers;
3. at least 1 episode capable of carrying an unresolved alternative across a delayed step;
4. at least 1 episode with a plausible irrelevant/null event;
5. source/provenance handles sufficient for independent documentary evaluation.

These thresholds are feasibility thresholds, not paper success thresholds.

If DAHN fails them, reject it as the final end-to-end holdout and audit another fresh project without changing these criteria post hoc.

## 12. No claim yet

This document establishes only the pre-scan selection contract.

It does not claim:
- that DAHN contains date conflicts;
- that any encoded origDate is historically correct;
- autonomous discovery;
- a successful sustained trajectory;
- sufficiency of any representation.

