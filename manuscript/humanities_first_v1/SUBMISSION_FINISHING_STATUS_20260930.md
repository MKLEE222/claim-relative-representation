# Submission-finishing status — 30 September 2026

**Article:** *After Revision: Corrections, Replies, and Scholarly Continuation in Digital Editions*  
**Authoritative text:** `MANUSCRIPT_v2.md` on branch `audit/cold-start-20260926` of `MKLEE222/claim-relative-representation`  
**Current status:** scholarly argument and present text are in submission finishing; **not yet a DHQ upload package**.

## Completed in this pass

1. Synchronized the local typesetting copy to the current GitHub manuscript before making changes. The prior local PDF belonged to an older, shorter text.
2. Created `EVIDENCE_AND_REPRODUCIBILITY.md` as the first reviewer-facing evidence page. The manuscript now links there, while the detailed research ledger remains available one level deeper.
3. Checked the article's short historical quotations and their immediate contexts against fixed page images: Yule–Cordier 1903, volume I, printed pages 113, 128, 423, 430; Cordier 1920, printed pages 31 and 70–72. In the fixed local scans these correspond to PDF scan pages 405, 420, 723, 732 and 45, 84–86, respectively. Printed and scan pagination are distinguished in the companion.
4. Repaired the Markdown-to-TeX converter: it now derives the full current title from the authoritative Markdown and renders four-level theory headings as headings instead of literal `####` text.
5. Rebuilt the current manuscript with the installed D-drive XeLaTeX in two passes. The result is a 17-page A4 PDF with two current figures and three tables. Every page was reviewed as a rendered image; the final log reports no overfull boxes or LaTeX errors. SHA-256 of the reviewed PDF: `E3B57CB0525075C6BA9CBEAA88F9E4E445698B236059B840F9968B9F96735C77`.
6. Updated the build README to identify the reviewed PDF as a **visual-review copy**. The old 14-page acceptance is superseded for the present text.

The source checks support the article's restrained readings: Laufer's response is transmitted by Cordier and targets Bretschneider's criticism while endorsing Polo's mulberry account; Cordier's Arbre Sec reply addresses his earlier reading/citation of Houtum-Schindler, without establishing adoption of the cypress identification. They are checks of cited passages, not independent historical adjudication.

## Submission gates still open

- **Author's figures:** The author plans to redraw the article's visual system. The current PDF contains the two R-generated review figures; do not freeze it as a final upload until the author approves the final figure set and all figure references/captions are checked again.
- **DHQ file format:** [DHQ's current submission guidelines](https://dhq.digitalhumanities.org/submissions/index.html) accept DHQ XML, TEI XML, RTF, OpenOffice, or Word for the initial article submission; figures should be embedded for review. PDF is useful for review but is not among the listed initial text formats. Prepare and visually verify a compliant file after figure approval.
- **Author metadata and declarations:** Actual author names, affiliations, funding, conflicts, and any required contributor/ethics statements must be supplied by the author. Do not invent them.
- **AI-use review:** [DHQ's AI policy](https://dhq.digitalhumanities.org/submissions/ai_policies.html) places intellectual and ethical responsibility on human authors, restricts AI-generated submission content, and requires acknowledgement of substantive AI use beyond routine grammar checking. The author has stated that the manuscript was directly revised by the research team. Only the author can confirm the final wording, degree of assistance, and accurate disclosure for submission. Do not sanitize the evidence record to imply a different provenance.
- **Source-record reuse:** The fixed Formalization Papers repository has no root license file and GitHub reports no license metadata. The article cites and analyses the source; its raw files are not redistributed in this package. Obtain a rights determination before republishing records or screenshots.
- **Submission action:** No OJS upload, editor contact, or claim of DHQ compliance has been made.

## Scientific boundaries to preserve

The Yule–Cordier readings are authorial and source-bound. The Formalization Papers first prospective execution remains invalid; the repaired run is a corrected reproduction, and later information-view comparisons are post-exposure diagnostics. The 52 connected chains share roots and records. The 47 natural non-live-target cases and 52 controlled history-ablated contexts have different denominators. The controlled removal is a representational test, not an observed loss from a historical digital edition. No independent human historical adjudication or stable blinded-model validation is claimed. Do not reopen the research program or change the frozen experimental definitions during packaging.

## Next mechanical sequence

Author approves final figures and final text → regenerate a DHQ-accepted editable submission file with embedded figures → author confirms metadata, rights, and AI-use statement → check the editable file and a review PDF page by page → submit through DHQ's OJS system only after those gates close.

