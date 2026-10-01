# R3 Hierarchical Historical Frame Contract v1

Date frozen: 2026-09-27
Status: FRAME DESIGN FROZEN; POPULATION COUNT NOT YET AUTHORIZED

## Purpose

Replace the invalid assumption that the legacy 223 intervals form a complete homogeneous population of retrospective interventions.

This contract defines the units that must be distinguished before any denominator-bearing humanities result is reported.

## Hierarchy

### L0 Publication object
The 1920 Notes and Addenda as a publication object.

### L1 Publication section
Examples include:
- Addenda body;
- bibliography;
- supplementary note/contribution;
- index;
- modern electronic wrapper/paratext.

L1 sections are not pooled automatically.

### L2 Top-level editorial entry
A source-authored entry or heading that functions as a primary Addenda unit.

### L3 Contribution
A named, signed, or otherwise responsibility-distinct contribution embedded within the publication, such as the Temple supplementary contribution.

A contribution can contain several interventions.

### L4 Page-addressed subnote or explicit target unit
A distinct source unit that points to a particular earlier page, chapter, note, or locus.

### L5 Embedded quotation / transmitted source passage
Quoted or transmitted scholarly material whose responsibility differs from the surrounding editor.

### L6 Proposition-level intervention act
The smallest analytical act for which target proposition, responsible actor/source, relation, modality, and evidence basis can be separately assigned.

## Counting rules

1. A denominator must name its level.
2. Nested L3-L6 units may not be added to L2 counts as if all were independent equivalent entries.
3. One L2 entry may contain multiple L6 acts.
4. One L6 act may address more than one proposition only if the source licenses the same relation and modality; otherwise split.
5. Quoted statements retain quoted-source responsibility unless the surrounding editor explicitly adopts or rejects them.
6. Bibliography/index/electronic wrapper material is never silently merged into a preceding L2 unit.
7. Unheaded acts remain eligible for L6 coding and therefore prevent a heading-only count from being treated as a complete intervention denominator without recall audit.

## Legacy 223 status

The 223 intervals are:
LEGACY_FROZEN_RETRIEVAL_UNIVERSE.

They are not:
- the L2 population;
- the L6 intervention population;
- a whole-book prevalence denominator.

No replacement N is frozen by this contract.

## Minimum frame review before a denominator is authorized

For every candidate boundary:
- section assignment;
- top-level versus nested status;
- responsibility boundary;
- quotation boundary;
- target-locus status;
- inclusion/exclusion reason;
- source offsets;
- verification authority.

A recall audit must cover more than one heading syntax class and explicitly inspect unheaded/nested structures.

## Output requirement

The next inventory must expose separate IDs:
publication_id, section_id, entry_id, contribution_id, subnote_id, quotation_id, act_id, proposition_id.

Null/NA values are allowed when a level is absent.

## Claim rule

Until this hierarchy has been reviewed across the declared source scope, only purposive or bounded historical findings are admissible. No whole-book intervention prevalence claim is authorized.
