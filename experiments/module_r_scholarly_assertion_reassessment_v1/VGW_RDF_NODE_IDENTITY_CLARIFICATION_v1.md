# Module R / VGW pre-fresh RDF node-identity clarification v1

Date: 2026-09-29
Status: PRE-FRESH CLARIFICATION AFTER SYNTHETIC-GATE FAILURE.

## 1. Trigger

The first VGW-shaped synthetic gate failed before any real provider distribution was opened.

The two extractors agreed on:
- all F-number joins;
- all disposition classes;
- the substantive previous-attribution case;
- all ambiguity/ineligibility cases.

The only mismatch was the evidence identifier for a synthetic current-direct null whose
Production node was deliberately encoded as an RDF blank node.

RDFLib renamed the blank node during parsing.
The lexical runtime preserved the source-local "_:" label.

These labels are not stable RDF identities and therefore must not be used as scholarly evidence
identifiers.

## 2. Scientific clarification

### Current-direct null

For a current direct Van Gogh attribution, the stable evidence anchor is:

    the current provider HumanMadeObject URI

The selected Production relation remains part of the extraction contract, but its blank-node label
is not the evidence identity.

Thus:

    evidence_id = current artwork URI

and:

    evidence_locator = provider slug + artwork URI + registered production relation

This does not change the task state or null/substantive classification.

### Previous-attribution reassessment

The reassessment event itself is the crm:E13_Attribute_Assignment.

For a substantive Module-R event, the assignment must have a stable IRI.

If the qualifying AttributeAssignment is an RDF blank node:

    NON_ADDRESSABLE_REASSESSMENT_EVENT

The object remains accounted for but is not eligible for the R1-R8 substantive denominator.

Reason:
a parser-local blank-node label cannot support stable event identity, provenance or delayed
history across independent implementations.

This is a representational requirement, not a parser convenience.

## 3. What does not change

No change to:
- F-number join;
- De la Faille 1970 baseline semantics;
- current-direct null semantics;
- previous-attribution status semantics;
- Psi;
- R-U3 classification;
- comparator budgets;
- any natural outcome.

No VGW provider N-Triples distribution had been opened when this clarification was frozen.
