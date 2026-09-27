# R3 Independent Second-Pass Review Bundle Results v1

Date: 2026-09-27
Status: REVIEW MATERIAL ENGINEERING COMPLETE / INDEPENDENT REVIEW NOT YET EXECUTED

Authoritative GitHub Actions run: 36313791906  
Artifact: r3-independent-second-pass-review-bundle-v1  
Artifact ID: 10929598975  
Artifact ZIP SHA-256: c3fa24cd4ef6098e0699be6e3d165664dc7ed00843f7628d78d3c73e66b6599d  
Artifact size: 16,058,306 bytes

## Source integrity

1903 Volume I PDF SHA-256:

6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7

1920 Notes and Addenda PDF SHA-256:

dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941

Both match the source-audit values frozen before the reviewer bundle was built.

## Bundle contents

Generated:

- 18 unique rendered page images;
- 18 corresponding page-text accessibility extracts;
- 19 case-to-page links across the five inquiries;
- blinded reviewer README;
- blank response form;
- case/page manifest;
- source hash manifest;
- file-level SHA-256 checksum manifest.

The repeated 1903 p.128 witness is stored once and referenced by both relevant case mappings.

## Leakage audit

Machine checks report:

- registered_answer_files_included = 0
- answer_side_leakage_check = PASS

The bundle does not include:

- data/r3_verified_proposition_panel_v1.csv;
- required_output;
- required_bindings;
- controlled separation/repair results;
- AW1/AW2 outcome ranks;
- registered-answer comparison labels.

## Artifact integrity and visual QA

The downloaded artifact ZIP was independently re-hashed after build.

Observed SHA-256:

c3fa24cd4ef6098e0699be6e3d165664dc7ed00843f7628d78d3c73e66b6599d

This exactly matches the GitHub Actions artifact digest.

Archive integrity test:
PASS.

Visual spot checks were performed on newly rendered reviewer pages:

- 1903 PDF index 501 / printed p.202;
- 1920 PDF index 61 / printed p.48;
- 1920 PDF index 62 / printed p.49.

The rendered pages are readable, correctly paginated, and expose the intended Great Desert source material. This is packaging QA only, not independent adjudication of the historical question.

## Gate consequence

[
REVIEW_MATERIAL_ENGINEERING = COMPLETE
]

[
INDEPENDENT_SECOND_PASS = PENDING
]

The only remaining action for this gate is a qualifying reviewer completing the sealed response before seeing the registered answers.

No AI self-review or author-side rereading may be substituted for that requirement.
