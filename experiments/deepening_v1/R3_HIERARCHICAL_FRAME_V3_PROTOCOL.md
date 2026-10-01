# R3 Hierarchical Frame v3 — Source-Form Distinction Protocol

Date frozen: 2026-09-27
Status: PRE-OUTCOME REPAIRED STRUCTURAL FRAME

## Evidence motivating v3

v2 fixed publication-section boundaries but left two structural discrepancies:

1. Roman heading candidates still included five false heads already covered by the earlier structural exclusion taxonomy.
2. Case-insensitive P./PP. matching conflated source-authored page-addressed subnote headings with line-wrapped lowercase bibliographic/page citations.

Artifact inspection established the source-form distinction before v3 execution.

### Roman candidates

Applying the pre-existing F1-F4 false-head rules to v2 Roman candidates gives:
- KEEP: 225
- F1 external periodical issue: 2
- F2 lettered source subitem: 2
- F3 citation continuation: 1
- F4 named-paper page: 0

These rules predate v3 and are restored unchanged.

### Bare page-pointer candidates in Addenda body

v2 emitted 17.
Sixteen begin with lowercase `p.` / `pp.` and are citation continuations after source line wrapping.
One begins with uppercase `P.`:
- `P. 201, Line 12. Read ... founded instead of found.`

v3 therefore treats source-authored explicit target headings as case-sensitive uppercase `P.` / `Pp.`.

### Temple Supplementary Note

v2 emitted 13 line-initial page references.
Three false positives are lowercase citation continuations:
- `p. 250). ...`
- `pp. 255-284.`
- `p. 51, but ...`

The remaining ten are uppercase source-addressed subnotes, matching the independent frame-scope audit.

## v3 rules

- L2 Introduction headings: 8 source candidates if reproduced.
- L2 Roman headings: case-insensitive page typography but pre-existing F1-F4 false-head exclusions applied.
- L4 Addenda bare page target: uppercase P./Pp. only.
- L3 Temple contribution: one signed responsibility wrapper.
- L4 Temple subnotes: uppercase P./Pp. only and nested under L3.
- L5/L6 remain unauthorized for automatic counting.

## Sanity gates

v3 is structurally valid only if:
- Introduction p.6 detected;
- Urumtsi P.201 detected;
- indented Ceylon XIV p.313 detected;
- Temple uppercase page-subnote count = 10;
- all five legacy false Roman heads are excluded by frozen F1-F3 rules;
- no replacement denominator is authorized.

## Expected interpretation if gates pass

The hierarchical frame may explain the earlier 244 provisional spans as distinct structural levels rather than a homogeneous N.

It still does not authorize 244 as an intervention denominator.
