# Transformation analogue registry v1

Date: 2026-09-23

## Purpose

The project uses **controlled constructed representations**. A constructed intervention is admissible only when its removed coordinate has a documented analogue in a real scholarly text-encoding or corpus-conversion workflow.

This registry establishes analogue plausibility. It does **not** claim that Project Gutenberg already performed the corresponding loss, and it does not yet mark Gate T as fully empirical-PASS.

## T_ATTRIBUTION — responsibility metadata removal

**CEDL coordinate:** `attribution`

TEI P5 provides explicit mechanisms for responsibility. The global `@resp` attribute identifies the agency responsible for an intervention or interpretation, and `<respStmt>` records intellectual responsibility for a text or edition.

A projection that keeps element text but drops `@resp` / responsibility statements is therefore a realistic representation operation: lexical content can remain while explicit attribution structure disappears.

Sources:
- https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-resp.html
- https://tei-c.org/Vault/P5/current/doc/tei-p5-doc/en/html/ref-respStmt.html

**Disposition:** analogue verified; implementation invariant still required.

## T_TEMPORAL — revision-history removal

**CEDL coordinate:** `temporal_order`

TEI's `<revisionDesc>` is explicitly intended to record revision history and support questions about a file's history. A body-only extraction, corpus chunk, or export that excludes the TEI header can preserve textual passages while dropping this revision-history structure.

Source:
- https://www.tei-c.org/release/doc/tei-p5-doc/en/html/HD.html

**Disposition:** analogue verified; implementation invariant still required.

## T_EVIDENCE — typed relation removal

**CEDL coordinate:** `evidence_relation`

TEI provides `<link>` and `<linkGrp>` for associations and alignment among passages. Those structures can carry relations that are not lexical content of either endpoint. A text projection that retains endpoint passages but removes stand-off link structures is therefore a direct analogue for losing an explicit evidence edge while retaining its textual endpoints.

Sources:
- https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-link.html
- https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-linkGrp.html

**Disposition:** analogue verified; CEDL uses its own relation vocabulary rather than claiming TEI supplies our humanistic semantics.

## T_BINDING — pointer / correspondence removal

**CEDL coordinate:** `claim_binding`

TEI linking uses pointers such as `@target` and correspondence/alignment mechanisms to connect a passage to another element or referent. Removing pointer attributes while retaining passage text is a realistic way to preserve content but lose explicit binding.

Sources:
- https://tei-c.org/Vault/P5/2.0.0/doc/tei-p5-doc/en/html/SA.html
- https://www.tei-c.org/Vault/P5/2.1.0/doc/tei-p5-doc/en/Guidelines.pdf

**Disposition:** analogue verified; empirical operator test required.

## T_NORMALIZE — distinction collapse

**CEDL coordinate:** `distinction_collapse`

TEI explicitly distinguishes original and normalized/regularized readings with `<orig>`, `<reg>`, and `<choice>`. The Guidelines note that regularization may be silent or explicitly marked. Selecting only the regularized reading is therefore a documented example in which a usable text is retained while a source distinction is collapsed.

Source:
- https://www.tei-c.org/Vault/P5/2.9.0/doc/tei-p5-doc/en/Guidelines.pdf (section 3.4.2, Regularization and Normalization)

**Disposition:** analogue verified for normalization as distinction collapse. It is not evidence that Yule-Cordier note-role distinctions are naturally lost by Gutenberg.

## Negative witness retained

Project Gutenberg plain text is **not** accepted as a natural attribution-free or chronology-free witness for this project. It retains NOTE headings, H.C. signatures, edition/addenda language, and page-targeted cross-layer cues.

Therefore:

`plain text != provenance-free representation`

and:

`increased reconstruction cost != relation unavailability`.
