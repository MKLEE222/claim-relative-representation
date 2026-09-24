# External Validation X2A - Whitman native relation-certainty audit

Date frozen: 2026-09-24
Status: EXTERNAL STATIC AUDIT

## External source

Repository:
whitmanarchive/whitman-LG_1855_variorum

Pinned commit:
25a00b7ebbdbc5246fce65a333bc761a5c22dad4

File:
source/authority/anc.02134.xml

Native title:
1855 Leaves of Grass Relations List

## Native semantics

The file itself states that its certainty levels correspond to the editors' level of certainty that the described manuscript or notebook line is a version of the printed line.

Relations are represented with:
- linkGrp type="relation";
- corresp identifying a manuscript/notebook file;
- link @target binding a printed locus to a manuscript locus;
- link @cert carrying native high/low certainty.

The project therefore supplies an independent case in which:
- an explicit relation exists;
- relation endpoints are explicit;
- epistemic/editorial commitment varies.

## Questions

X2A-Q1.
Does the native relation list contain both high- and low-certainty explicit links?

X2A-Q2.
Can a single manuscript/notebook group contain links at more than one certainty level?

X2A-Q3.
Would collapsing @cert while retaining targets preserve relation availability but alter the editorial commitment exposed by the representation?

X2A-Q3 is a construction hypothesis for a later controlled audit; X2A itself only characterizes the native object.

## Metrics

- number of relation groups;
- number of links;
- high/low/other certainty counts;
- number of manuscript groups with mixed certainty levels;
- target-shape counts;
- whether all links retain explicit target endpoints.

## Claim ceiling

X2A may support:
- native descriptive claims about relation/certainty representation;
- design of a later certainty-projection intervention.

It does not support a literary/genetic conclusion about Whitman's manuscripts.
