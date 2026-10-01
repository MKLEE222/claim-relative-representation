# R3-A frame refinement protocol v1

Date frozen: 2026-09-27
Status: structural frame repair before relation coding.

## Problem

The first regex enumerator intentionally over-generated. Manual inspection of the candidate heads revealed a small class of lines that match the Roman-numeral/page syntax but are not Yule-Cordier Addenda entry heads. They are citations or sub-items embedded inside a preceding entry.

If left untreated, such false heads split one historical entry into multiple artificial units.

## Content-independent exclusion rules

A candidate head is excluded from the entry-head frame when its head syntax itself identifies another source structure:

F1 EXTERNAL_PERIODICAL_ISSUE
- Roman volume/number immediately followed by a month or four-digit year before the page reference.
- Example form: "VII., 1878, pp. ..."

F2 LETTERED_SOURCE_SUBITEM
- single capital letter followed by "Chap." before its page reference.
- Example form: "C. Chap. 8, p. ..."

F3 CLOSING_PAREN_CITATION_CONTINUATION
- page reference is immediately closed by ")" before continuing the sentence.
- This marks a parenthetical external citation continuation rather than an Addenda head.

F4 EXPLICIT_NAMED_PAPER_PAGE
- the putative head explicitly states that its page number is "in ... paper", so the page belongs to the named external paper rather than to the Yule edition.

These rules inspect head syntax only. They do not inspect whether an entry is a criticism/correction or whether it would help the representation hypothesis.

## Merge rule

An excluded false head and its text are merged back into the immediately preceding structurally accepted entry, because the false head was produced by splitting the source stream at that line.

If an excluded false head occurs before any accepted entry in the frame, it remains an excluded orphan and is not silently attached to a later entry.

## Authority

This refinement is still a structural candidate frame, not final historical coding.

All structurally accepted rows must still receive Stage-0 human frame review. Further false positives found by review remain in an exclusion ledger with explicit reason; no candidate is silently deleted.

## Output

- structural entry frame with merged text;
- exclusion ledger with F1-F4 reasons;
- counts by source section;
- no relation labels.
