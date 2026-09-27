# R3 Independent Second-Pass Source Bundle Protocol v1

Date frozen: 2026-09-27
Status: REVIEWER-MATERIAL PACKAGING ONLY; NO ADJUDICATION

## Purpose

Materialize the already-sealed independent review packet into a single blinded source bundle that a qualifying reviewer can inspect without browsing the research repository.

This operation does not score, interpret or adjudicate any historical answer.

## Frozen review design

Question/answer separation is governed by:

- R3_SECOND_PASS_REVIEW_PROTOCOL_v1.md
- R3_SECOND_PASS_REVIEW_PACKET_v1.md
- R3_SECOND_PASS_REVIEW_MANIFEST_v1.csv
- R3_SECOND_PASS_REVIEW_SEAL_v1.md

The registered-answer source remains excluded.

## Source objects

1903 Volume I scan copy:
https://archive.org/download/bookofsermarcopo001polo/bookofsermarcopo001polo.pdf

Frozen SHA-256:
6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7

1920 Notes and Addenda:
https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf

Frozen SHA-256:
dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941

## Required pages

1903 PDF indices:
408, 425, 461, 462, 500, 501.

1920 PDF indices:
38, 39, 40, 41, 42, 43, 44, 47, 48, 61, 62, 63.

These are exactly the pages referenced by the sealed five-case review manifest.

## Bundle contents

Allowed:
- blinded reviewer instructions;
- blank reviewer response form;
- case/page manifest;
- rendered page PNGs;
- extracted text from those exact pages for accessibility/search;
- source hashes;
- bundle checksum manifest.

Forbidden:
- data/r3_verified_proposition_panel_v1.csv;
- required_output;
- required_bindings;
- controlled separation/repair outcomes;
- AW1/AW2 ranks;
- claim-state labels;
- comparison-to-registered-answer results.

## Rendering and verification

Each source page is rendered directly from the frozen PDF at 2x PDF point resolution with no OCR or rewriting.

The page image is authoritative; extracted PDF text is navigation/accessibility support only.

The builder verifies:
- both PDF hashes;
- all requested page indices exist;
- every render is non-trivially sized;
- the text bundle contains no declared answer-side leakage tokens;
- every generated file receives a SHA-256 entry.

## Gate consequence

Successful bundle generation means:

REVIEW_MATERIAL_ENGINEERING = COMPLETE

It does not mean:

INDEPENDENT_SECOND_PASS = COMPLETE

Gate II remains pending until a qualifying reviewer returns the sealed response.
