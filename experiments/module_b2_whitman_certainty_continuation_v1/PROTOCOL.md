# Module B2 v1 — Whitman certainty-to-evidence continuation

Date frozen: 2026-09-28
Status: DEVELOPMENT PRESSURE TEST ON AN ALREADY-EXPOSED RELATION INVENTORY. NOT AN INDEPENDENT HOLDOUT.

## Purpose

Test whether preserving the current endpoint answer and even a locus-level uncertainty summary is sufficient to preserve which source endpoints should be inspected next.

The experiment moves beyond the prior X2B/X2C question "is certainty still present?" by making certainty control a concrete source-following continuation target.

## Pinned sources

### Variorum relation and printed text repository

Repository:
whitmanarchive/whitman-LG_1855_variorum

Commit:
25a00b7ebbdbc5246fce65a333bc761a5c22dad4

Relation file:
source/authority/anc.02134.xml

Expected relation blob:
11d6f7508c8bfd120d390d31c49d2399e38b5337

Printed source:
source/tei/ppp.01880.xml

Expected printed blob:
676c84cb48cdb2edaa6f72f68ae9d489a2beff22

### Manuscript repository

Repository:
whitmanarchive/whitman-manuscripts

Commit:
249bc14594fa1c0428e7ca39f52753de21ce604b

This is the latest commit returned at or before 2019-06-05, immediately after the relation file's recorded 2019-06-04 creation date.

Pinned tree:
1871715fbcef5f9721e80f385471a86ad52ef463

The experiment validates manuscript files against this tree. A missing file or missing xml:id is retained as unresolved source-route accessibility; it is not silently repaired with a later repository state.

## Population

All valid two-target relation links in anc.02134.xml.

Unit for the current scholarly task:
one unique printed locus.

Previously known descriptive counts are development knowledge and not a new outcome:
- 764 unique printed loci;
- 120 mixed high/low loci;
- 251 high-only loci;
- 393 low-only loci.

## Current task Q0_ENDPOINTS

For each printed locus p, recover the complete set:

    {(manuscript_file, manuscript_local_locus)}

Per-link certainty is not part of Q0.

## Continuation grammar

### B_LOW_CERTAINTY_REVIEW

Eligible iff at least one native relation at p has cert="low".

Continuation target:
the exact set of manuscript endpoints whose relation is low-certainty.

Interpretation:
these are the source endpoints selected for additional inspection under this frozen uncertainty-review rule.

This does not assert that the relation is historically false or that a human scholar must reject it.

### B_MIXED_CERTAINTY_COMPARISON

Eligible iff p has at least one high-certainty and at least one low-certainty relation.

Continuation target:
the partition of all endpoints into high and low sets.

Interpretation:
the representation supports a source comparison in which differently qualified relation claims at the same printed locus remain distinguishable.

### HIGH_ONLY_CONTROL

If every relation at p is high-certainty, no low-certainty review branch is licensed under this grammar.

This does not mean no other scholarly question exists.

## Representations

### R_NATIVE

Per-link endpoint plus per-link cert.

### R_ENDPOINT_ONLY

All Q0 endpoints retained; cert removed.

### R_LOCUS_STATUS_ONLY

For each printed locus retain:
- complete endpoint set;
- number of high links;
- number of low links;
- high-only / low-only / mixed status.

Remove:
- the binding from certainty value to endpoint.

This is deliberately stronger than R_ENDPOINT_ONLY.

### R_ENDPOINT_CERT_LEDGER

R_LOCUS_STATUS_ONLY plus an explicit endpoint -> cert binding ledger.

The ledger is charged input, not free decoder knowledge.

### R_SOURCE_LINKED

Printed-locus identifier plus lawful reopening of the pinned relation file.

## Controlled mixed-locus twin

For every mixed locus:
- choose the first high endpoint and first low endpoint under frozen lexical ordering;
- swap only their cert values.

Then:
- endpoint set is identical;
- number of high and low links is identical;
- mixed status is identical;
- R_LOCUS_STATUS_ONLY is identical;
- B_LOW_CERTAINTY_REVIEW target set changes;
- B_MIXED_CERTAINTY_COMPARISON partition changes.

This is a controlled relation-binding witness, not a naturally observed alternative editorial judgement.

## Repair / wrong-binding control

Correct endpoint-cert ledger must reconstruct the exact native continuation target.

Wrong ledger:
apply the frozen high/low swap for each mixed locus.

Requirements:
- Q0_ENDPOINTS remains exact;
- locus-level high/low counts remain exact;
- correct ledger restores the continuation partition;
- wrong binding fails the native continuation target on every mixed locus where endpoints are distinct.

No new cert value is invented.

## Source-route execution

The experiment must resolve:
1. printed target IDs against pinned ppp.01880.xml;
2. manuscript file names against the pinned 2019 manuscript tree;
3. manuscript local IDs against the corresponding pinned manuscript TEI.

Report separately:
- relation links whose printed locus resolves;
- manuscript file resolves;
- manuscript local locus resolves;
- complete two-sided source route resolves.

Do not treat a missing 2019 source route as evidence that the editorial relation itself is false.

## Metrics

- Q0 exactness under every representation;
- continuation exactness;
- mixed-locus controlled separations;
- correct/wrong ledger results;
- low-review target counts;
- mixed-comparison target counts;
- source-route resolution by certainty level;
- source bytes and locator/ledger payload bytes;
- unresolved routes retained.

No model or human accuracy score is part of this experiment.

## Dispositions

CURRENT_ENDPOINT_EQUIVALENCE = all representations preserve Q0.

LOCUS_STATUS_CONTINUATION_SEPARATION = controlled mixed-locus twins exist under identical R_LOCUS_STATUS_ONLY.

CORRECT_BINDING_RESTORES_CONTINUATION = correct ledger exact.

WRONG_BINDING_FAILS = swapped ledger changes the selected follow-up evidence on mixed loci.

SOURCE_ROUTE_EXECUTABLE = report exact rate; no success assumed.

AUTONOMOUS_QUESTION_GENERATION = NOT TESTED.

HISTORICAL_GENETIC_TRUTH = NOT TESTED.

INDEPENDENT_TRANSFER = NOT TESTED.

## Claim ceiling

A positive result can support only:

> For this exposed Whitman relation inventory, current endpoint recovery and locus-level uncertainty summaries can be insufficient to determine which manuscript evidence is selected by a certainty-sensitive continuation rule; per-link status binding or lawful source reopening restores that target.

It cannot establish that low-certainty relations are wrong, that certainty must be stored in one specific field, or that this mechanism generalizes beyond the tested source ecology.
