# R3 Historical Object Model v1

Date: 2026-09-27
Status: EXPLORATORY SCIENTIFIC MODEL. Derived from page-verified source audits; not a final ontology or manuscript framework.

## Purpose

The historical object must be fine-grained enough that representation experiments do not manufacture loss by collapsing distinct scholarly acts before transformation.

## Hierarchy

PUBLICATION_SECTION
  -> CONTRIBUTION
     -> ADDRESSABLE_UNIT
        -> PROPOSITION_ACT

These levels are not assumed to be one-to-one.

### PUBLICATION_SECTION
A bibliographically distinct region such as Addenda, Supplementary Note, Bibliography or Index.

### CONTRIBUTION
A contribution with a responsibility boundary, e.g. Cordier's Addenda entry or Temple's signed Supplementary Note.

### ADDRESSABLE_UNIT
A source-native locally addressable unit such as a page-addressed entry/subnote, erratum, or explicitly headed passage.

### PROPOSITION_ACT
The minimum analytical unit for a scholarly-history claim in this project.

Each proposition act records, where source-supported:
- proposition content;
- proposition actor / commitment holder;
- transmitting or mediating editor, if different;
- target proposition or earlier locus;
- relation to target;
- modality / resolution state;
- evidence basis invoked for this proposition;
- edition/publication time and reported opinion/publication time where relevant;
- verification authority.

## Binding principle

Actor, proposition, target, evidence and modality are not independent bags of attributes.

The object includes typed bindings such as:
`ACTOR --COMMITS_TO--> PROPOSITION`
`EDITOR --TRANSMITS--> ACTOR/PROPOSITION`
`PROPOSITION --TARGETS--> EARLIER_PROPOSITION`
`EVIDENCE --SUPPORTS--> PROPOSITION`
`MODALITY --QUALIFIES--> PROPOSITION`.

## Why bindings are required by the inspected history

Pashai: Stein agrees with the earlier source-attribution judgment while challenging a different route proposition.

Arbre Sec: Cordier transmits Houtum-Schindler's cypress proposal and gives a bibliographical reply; transmission does not itself establish Cordier's adoption.

Great Desert: survey measurements support distance/marches while a separate line of reasoning supports a local-folklore source attribution.

Urumtsi: a short erratum changes `found` to `founded`; it is a distinct proposition-level intervention despite minimal length.

## Non-claims

This model is not claimed as a universal ontology of scholarly editing.
It does not imply that every proposition act must be explicitly encoded in a digital edition.
It does not imply that plain text cannot preserve or permit recovery of these bindings.
It is the reference object against which recoverability questions can be posed.