# External Validation X3A - Faust source-qualified temporal relation audit

Date frozen: 2026-09-24
Status: EXTERNAL STATIC AUDIT

## External source

Repository:
faustedition/faust-xml

Pinned commit:
502eca65120dd6189ceaf41d4e5017775e6e4677

File:
xml/macrogenesis/wa/15_2/I.xml

## Native semantics

The Macrogenesis XML records temporal relations as source-qualified scholarly assertions.

Each relation can contain:
- relation type, e.g. temp-pre;
- a source URI plus page/locator text;
- two or more item URIs specifying an ordered sequence.

The external project therefore does not expose chronology as an unqualified date/order table.

It exposes source-bound temporal assertions that can later be combined, conflicted, or filtered by Macrogenesis processing.

## Questions

X3A-Q1.
Are temporal relations explicitly bound to scholarly sources?

X3A-Q2.
Do some relations constrain more than two items, making the native object richer than a simple pairwise date label?

X3A-Q3.
Would removing source attribution while retaining ordered items preserve a temporal edge but alter the provenance available for later conflict/adjudication?

X3A-Q3 is a later intervention hypothesis. X3A only characterizes the native relation object.

## Metrics

- relation count;
- relation-name distribution;
- distinct source URIs;
- distinct source locators;
- item-count distribution;
- distinct document/item URIs;
- relations lacking source or item data.

## Claim ceiling

This audit supports source/provenance-sensitive temporal representation claims.

It does not establish a unique historical chronology and does not treat the Macrogenesis model as historical ground truth.
