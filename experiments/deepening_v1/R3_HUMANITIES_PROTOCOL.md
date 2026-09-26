# R3 humanities-first editorial-history protocol v1

Date frozen: 2026-09-26
Status: prospective candidate inventory and source-verification study.
Primary corpus: Yule-Cordier 1903 edition + Cordier 1920 Notes and Addenda.

## Humanistic question

How does a major scholarly edition accumulate, contest, correct, qualify, and reattribute knowledge across editorial generations, and which documentary relations must remain recoverable if a later reader is to reconstruct that history rather than merely retrieve the same words?

The object is not "retrieval performance" in the abstract. The object is the editorial history of claims: who asserted what, who challenged it, what later evidence was invoked, whether an earlier note was corrected or merely supplemented, and how that responsibility is attached across editions.

## Why this corpus is suitable

The 1903 Yule-Cordier edition contains a dense commentary apparatus. Cordier's 1920 Notes and Addenda explicitly revisits the earlier edition using newer research and discoveries. This creates a naturally diachronic scholarly object in which later notes often point back to earlier chapters/pages and named scholars.

The paper-money chain is one close-read example, not the sampling frame.

## Source hierarchy

1. printed/page-image witness for final historical claims;
2. Project Gutenberg transcription for candidate enumeration and reproducible search;
3. derived CSV/graph only after source verification.

A candidate found in OCR/Gutenberg is not automatically a verified historical relation.

## Universe and denominator

Define the 1920 Addenda region from its explicit title heading through the end of the addenda text before bibliography/index material.

Enumerate every structurally explicit retrospective entry matching an edition locator such as:
- Roman chapter/section identifier + page/pages reference;
- explicit "Regarding ... p." / "Referring to ..." pointer;
- other unambiguous backward pointer to the 1903 edition.

Do not select by whether the entry contains a correction, disagreement, dramatic reversal, or a known target name.

The inventory records every candidate, including routine additions and entries whose relation type remains unresolved.

## Registered humanistic relation families

Classification occurs only after source inspection.

- ASSERTION_CONTEXT: earlier narrative/editorial proposition being revisited.
- ADDITIVE_EVIDENCE: later material extends context without contradicting the earlier proposition.
- CORROBORATION: later evidence explicitly confirms/upholds an earlier proposition.
- CRITICISM: later material explicitly challenges an earlier proposition or identification.
- CORRECTION_OF_PRIOR_CRITICISM: later material explicitly rejects an earlier objection and restores or changes the earlier assessment.
- IDENTIFICATION_UPDATE: place/person/material/textual identification changes.
- ATTRIBUTION_UPDATE: responsibility, eyewitness status, source derivation, or who knew/observed what changes.
- TEXTUAL_UPDATE: reading/translation/textual witness changes without necessarily changing historical truth.
- QUALIFICATION: scope, certainty, chronology, or authority is narrowed without straightforward reversal.
- UNRESOLVED_RELATION: source linkage is clear but the above relation cannot be assigned without over-interpretation.

Multiple labels are allowed when the source explicitly licenses them.

## Three registered scholarly tasks

### H1 — editorial responsibility recovery

Given a later note, recover:
- the earlier locus it addresses;
- the earlier actor/source;
- the later actor/source;
- the relation between them.

Success requires source-bound attribution, not just topical similarity.

### H2 — controversy trajectory recovery

For episodes containing criticism/correction/qualification, recover the ordered sequence of scholarly acts without collapsing:
- base narrative;
- editor note;
- cited scholar;
- later addendum;
- later cited scholar.

The task output is a provenance-bearing trajectory, not a final truth label.

### H3 — historiographic change characterization

Across the complete verified candidate inventory, estimate the distribution of later interventions:
- additive;
- corroborative;
- critical;
- corrective;
- identification/attribution/textual update;
- qualification;
- unresolved.

This is the main denominator-bearing humanistic result. It asks what kind of knowledge work the later editorial layer performs.

## Representation experiment attached to the humanistic tasks

For verified episodes, compare three representations under the same task:

1. FULL_LAYERED:
   explicit edition layer + pointer + attribution + source text.

2. LINEAR_TEXT:
   textual content in chronological concatenation but no explicit cross-layer attachment edge.

3. TOPIC_BAG:
   same episode texts grouped by topic but without temporal/editorial responsibility relations.

A representation is not declared inadequate because one retriever fails. For H1/H2, inadequacy requires either:
- a same-visible-input / different-required-answer collision;
- or a controlled twin preserving visible text while changing the source-bound attachment/actor relation.

FULL_LAYERED is the strong native/reference upper bound, not a straw baseline.

## Close reading requirement

At least four qualitatively different verified episodes will receive source-level close readings:
- one correction/reinstatement episode if available;
- one attribution/eyewitness episode if available;
- one additive/accretion episode;
- one unresolved or non-reversal episode.

Paper money may occupy the first role only if it survives the inventory unchanged.

The close readings must explain why the relation matters to a substantive historical question, not merely why it changes a computational label.

## Negative and null retention

Retain:
- later notes that only add context;
- pointers whose target cannot be verified;
- cases with no explicit stance change;
- cases where LINEAR_TEXT is sufficient;
- cases where the computational distinction has no meaningful humanistic consequence.

These cases define the scope of the method.

## Claim ceiling

Permitted if supported:
> The editorial history of a scholarly edition contains source-bound relations of criticism, correction, attribution, qualification and accretion that are not reducible to textual co-presence; preserving or reconstructing those relations matters for specific historical research tasks.

Not permitted without further evidence:
> every editorial layer change alters historical warrant;
> richer metadata is always better;
> the formal relation labels exhaust the editors' historical reasoning;
> readers or historians necessarily change belief when a relation is exposed.
