# R3 Hierarchical Frame Execution Protocol v1

Date frozen: 2026-09-27
Status: PRE-OUTCOME STRUCTURAL FRAME EXECUTION

## Purpose

Instantiate R3_HIERARCHICAL_FRAME_CONTRACT_v1 as a reproducible structural skeleton without converting machine-detectable headings into historical prevalence claims.

The execution addresses known legacy-frame defects:
- omitted Introduction page-pointer headings;
- missed bare P./PP. target units such as the Urumtsi erratum;
- missed indented Roman headings such as the Ceylon passage;
- bibliography/index contamination;
- nested page-addressed units inside the Temple Supplementary Note.

## Source

Project Gutenberg pg12410.txt
Expected SHA-256:
c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

## Structural levels emitted

### L1 — publication section

Detect source-native section boundaries after the Notes and Addenda title:
- ADDENDA_BODY
- BIBLIOGRAPHY
- SUPPLEMENTARY_NOTE
- INDEX
- POST_END_WRAPPER when present

Section matching is line-anchored and whitespace-tolerant.

### L2 — top-level heading candidate

Within ADDENDA_BODY:
- Introduction p./pp. headings;
- Roman/chapter page headings, including indented forms.

These are structural candidates, not automatically validated historical interventions.

### L3 — responsibility-distinct contribution

Within SUPPLEMENTARY_NOTE:
- register the signed/named Temple contribution as one L3 contribution when Richard C. Temple is source-explicit.

The contribution is not counted as ten contributors because it contains multiple page-addressed subnotes.

### L4 — explicit target-unit candidate

Capture line-initial P./PP. page-pointer headings:
- in ADDENDA_BODY, as explicit-target units requiring review of whether they are independent L2-level entries or nested L4 units;
- in SUPPLEMENTARY_NOTE, as L4 subnotes nested under the L3 contribution.

This deliberately captures the Urumtsi `P. 201, Line 12...` form.

## Not automatically closed

### L5 — embedded quotation / transmitted source passage

Quotation boundaries are not inferred from punctuation alone.

### L6 — proposition-level intervention act

No proposition-level act count is produced by this structural run.

## Parent assignment

For ADDENDA_BODY L4 units:
- provisional parent = nearest preceding L2 candidate;
- parent relation is marked REVIEW_REQUIRED and may be rejected.

For SUPPLEMENTARY_NOTE L4 units:
- parent = the L3 Temple contribution.

## Output

- hierarchical_frame_candidates_v1.csv
- hierarchical_frame_meta_v1.json
- section boundaries and counts in stdout

## Claim ceiling

The run may support:
- structural coverage;
- section separation;
- detection of known missed heading classes;
- a reviewable hierarchy.

It may not support:
- a new whole-book denominator;
- prevalence of intervention types;
- independence of nested units;
- historical correctness of every candidate boundary.
