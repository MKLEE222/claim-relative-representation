# R3 Hierarchical Frame v1 Implementation Failure and v2 Repair

Date: 2026-09-27

The first executable hierarchical-frame run is INVALID_IMPLEMENTATION.

Observed failure:
- it selected the first line containing "SUPPLEMENTARY NOTE" after the Addenda title;
- that occurrence belongs to the Addenda synopsis of contents, not the actual Temple Supplementary Note;
- ADDENDA_BODY was therefore truncated before the real historical entries;
- only two Roman headings were detected;
- known Introduction p.6 and Ceylon boundaries failed coverage.

No candidate count from v1 is scientifically usable.

## v2 repair frozen before opening v2 output

1. Identify the Addenda publication title.
2. After that title, locate the actual content start at the later source heading:
   `MARCO POLO AND HIS BOOK. / INTRODUCTORY NOTICES.`
3. Locate the actual terminal section markers after the content start:
   - `BIBLIOGRAPHY OF MARCO POLO'S BOOK` (source section title, not synopsis mention);
   - the last line-initial `SUPPLEMENTARY NOTE.` before the final index;
   - the final line-initial `INDEX` preceding index entries.
4. Accept optional Gutenberg emphasis underscores around page numbers.
5. Preserve indentation when matching Roman headings.

No historical relation label, proposition outcome, retrieval result, or denominator is used to choose these markers.

Known sanity checks:
- Introduction p.6 must be structurally detected;
- Urumtsi P.201 Line 12 must be structurally detected;
- indented Ceylon XIV p.313 must be structurally detected;
- Temple supplement should be a distinct L3 contribution containing nested page-addressed units;
- no replacement denominator is authorized by structural success.
