# R3 Hierarchical Historical Frame v3 Results

Date: 2026-09-27
Status: STRUCTURAL SANITY PASS / HUMAN FRAME REVIEW PENDING
Authoritative GitHub Actions run: 36311510406
Artifact: r3-hierarchical-frame-v3
Artifact ID: 10929575920
Artifact SHA-256: d87f74a9dc63d522a216d7309dec1073e8509cdd1f78cf482227be4e254693f

## Source integrity

Project Gutenberg pg12410.txt SHA-256:

`c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c`

matches the previously frozen source.

## Publication-section frame

The v3 execution distinguishes:

| L1 section | Source character range |
|---|---:|
| ADDENDA_BODY | 2,023,959–2,301,174 |
| BIBLIOGRAPHY | 2,301,174–2,317,241 |
| SUPPLEMENTARY_NOTE | 2,317,241–2,333,807 |
| INDEX | 2,333,807–2,361,246 |
| POST_END_WRAPPER | 2,361,246–2,380,071 |

This removes the cross-section contamination previously observed in the legacy final intervals.

## Structural candidates

### L2 top-level source-heading candidates

- Introduction page headings: 8
- Roman page headings after pre-existing false-head exclusions: 225

Total L2 candidates:

[
233
]

### L4 explicit target in Addenda body

Case-sensitive uppercase source-addressed bare page targets:

- 1

This is the independently audited Urumtsi erratum heading:

`P. 201, Line 12. Read ... founded instead of found.`

### L3 responsibility-distinct contribution

- Temple Supplementary Note contribution: 1 wrapper

This is a responsibility node, not a peer observation to be pooled with its subnotes.

### L4 Temple nested page-addressed subnotes

- 10

The v2 discrepancy of 13 is resolved by excluding three lowercase line-wrapped citation continuations:
- `p. 250). ...`
- `pp. 255–284.`
- `p. 51, but ...`

The remaining ten match the independent frame-scope audit.

## Restored false-head exclusions

The pre-existing structural exclusion rules remove five Roman-looking false heads:

- F1 external periodical issue: 2
- F2 lettered source subitem: 2
- F3 citation continuation: 1
- F4 named-paper page: 0

## Known-boundary sanity checks

All pass:

- Introduction p.6 -> L2-0001
- Urumtsi P.201 Line 12 -> L4-0001
- indented Ceylon XIV p.313 -> L2-0191

[
STRUCTURAL_SANITY_PASS = 1
]

## Why 244 now makes sense without becoming a denominator

The source-order structural span candidates are:

[
233 L2 + 1 Addenda explicit target L4 + 10 Temple nested L4 = 244
]

The hierarchy additionally contains:

[
1 L3 Temple responsibility wrapper
]

so the structural node count is:

[
245
]

These are not 245 exchangeable historical observations.

The v3 result explains why the earlier audit encountered 244 provisional spans while also showing why 244 cannot be treated as a pooled intervention N:

- 233 are L2 heading candidates;
- 1 is a distinct bare page-addressed target unit;
- 10 are nested within one L3 contribution;
- L5 quotation boundaries are not yet enumerated;
- L6 proposition-level acts are not yet enumerated.

## Authorized and unauthorized uses

Authorized:
- publication-section separation;
- source-boundary candidate review;
- reconstruction of missed heading classes;
- parent/child review for Temple and explicit target units;
- generation of a human frame-review package.

Not authorized:
- whole-book prevalence;
- intervention-type frequencies;
- 244 as a denominator;
- 245 as a denominator;
- proposition-level act prevalence.

Explicit machine state:

[
L5_COUNT_AUTHORIZED = 0
]

[
L6_COUNT_AUTHORIZED = 0
]

[
REPLACEMENT_DENOMINATOR_AUTHORIZED = 0
]

## Gate consequence

The structural part of Gate I has moved from "frame absent" to:

> executable hierarchical frame skeleton established and sanity-checked; intellectual-unit review, L5/L6 review, and denominator authorization remain open.

This is a material closure advance but not historical-object closure.
