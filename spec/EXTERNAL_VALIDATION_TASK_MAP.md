# External Validation Task Map v1

Date: 2026-09-24

## P1 - Frankenstein Variorum

### Native problem

The project explicitly faced heterogeneous digital structures:

- print editions organized semantically by volume/chapter/paragraph;
- Shelley-Godwin manuscript data organized by page surfaces and documentary lines;
- chapter/paragraph structure in the manuscript represented with milestone elements.

The Variorum project then prepared comparable XML, flattened markup for collation, divided the text into 33 cross-version portions, ran machine-assisted collation, and produced a stand-off TEI spine that stores variant information and pointers back to edition files.

### Proposed external tasks

**FV-T1 ALIGN**
Given a source passage/chunk in one witness, recover the corresponding aligned location(s) in the other witnesses.

**FV-T2 VARIANT**
Given an aligned locus, recover which witnesses differ and which reading belongs to each witness.

**FV-T3 STRUCTURE**
Recover the native structural provenance of an aligned passage: page-surface/documentary-line versus semantic chapter/paragraph organization.

### Framework mapping

- task contract: alignment / witness / structure recovery;
- TD: source-structure projection or flattening already documented by the external project;
- TR: stand-off spine pointers and apparatus relations;
- TA: chunk-level versus edition-level access;
- profile: explicit/recoverable/unresolved + depth/basis/cost.

### Critical boundary

Do not claim that flattening is generally harmful.

The Frankenstein project itself flattened markup because that transformation was useful for its collation task. This material is therefore particularly valuable for showing **positive task adaptation**, not only information loss.

---

## P2 - Walt Whitman Archive

### Native problem

The Archive distinguishes:

- printed variants encoded in TEI critical-apparatus structures;
- manuscript/notebook relations encoded in a separate relation file;
- inclusive possible relations, some of which are explicitly described as speculative or not clear-cut.

The editorial policy explains that a stronger genetically based apparatus was considered inappropriate for these manuscript relations.

### Proposed external tasks

**WW-T1 LINK**
Given a printed line/segment, recover linked manuscript/notebook segments.

**WW-T2 RELATION-STATUS**
Determine what kind of editorial commitment the representation licenses: printed variant apparatus versus possible manuscript relation.

**WW-T3 UNCERTAINTY**
Preserve unresolved/possible relation status rather than coercing the relation into a stronger genealogical claim.

### Framework mapping

- G_D: explicit linkage, target identity, source manuscript identity;
- G_E boundary: editorial entitlement/strength is downstream;
- TR: relation-file availability and pointer structure;
- recovery profile: explicit relation can still carry limited epistemic commitment.

### Critical boundary

Do not invent per-link certainty values if the native data does not encode them.

The external validation target is the distinction between representational forms/editorial commitments, not a fabricated numeric confidence score.

---

## P3 - Digital Faust Edition / Macrogenesis

### Native problem

Macrogenesis aggregates historical/research assertions about:

- witness ordering;
- date constraints;
- sources for those assertions.

The published graph exposes edge attributes including source, ignore/delete status, and weight/trust-related information. Conflicting assertions may be removed or ignored to obtain an acyclic graph compatible with the retained statements.

### Proposed external tasks

**FA-T1 SOURCE**
Recover which scholarly source licenses a temporal edge.

**FA-T2 TEMPORAL**
Recover the relative temporal relation between selected witnesses under the native assertion graph.

**FA-T3 CONFLICT**
Identify whether a temporal assertion is retained, ignored, or removed because of conflict handling.

**FA-T4 ORDER-ENTITLEMENT**
Distinguish a possible graph-compatible order from a claim that the graph reveals the unique historical order.

### Framework mapping

- TD: provenance/temporal metadata;
- TR: graph edge relation;
- carrier basis: source-qualified graph edge;
- unresolved status: non-unique topological order / conflicting assertions;
- task-adapted output: chronology under declared source/conflict policy.

### Critical boundary

The project's computed order is not treated as historical ground truth.

The external edition itself explicitly frames the model as one possible ordering compatible with retained assertions.

---

## P4 - ELTeC

ELTeC is used only to discipline corpus construction:

- transparent selection criteria;
- task-specific sampling/subcollections;
- avoidance of essentializing a literary category through benchmark design.

It is methodological scaffolding, not evidence for the current representation mechanism.

---

## Cross-material synthesis

The external materials deliberately occupy different corners:

- Frankenstein: **task-adaptive restructuring can help**.
- Whitman: **stronger relation representation is not always epistemically appropriate**.
- Faust: **source/provenance/conflict state constrains temporal entitlement**.
- Yule-Cordier: **representation affects whether evidence enters and changes a humanistic warrant chain**.

If these all map coherently onto the same task-relative representation framework without collapsing their native semantics, that is stronger evidence than repeating one engineered ablation across four corpora.
