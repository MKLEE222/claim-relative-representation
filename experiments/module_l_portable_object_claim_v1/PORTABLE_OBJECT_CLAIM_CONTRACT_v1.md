# Portable object/claim applicability contract v1

Date frozen: 2026-09-28
Status: PRE-FRESH ENGINE CONTRACT. FROZEN BEFORE OPENING ANY NEW INDEPENDENT CANDIDATE EPISODE XML.

## 1. Purpose

This contract defines the next engine version required by the pre-fresh portability audit.

It does not revise the authoritative outcomes of Modules J or K.
It repairs a documented contract/implementation mismatch and makes source/object identity portable across projects before any new independent holdout is opened.

## 2. Frozen scientific invariants retained from J

The following scientific requirements are unchanged:

1. temporal claims may compose only after one scholarly object is established;
2. no first-object fallback is permitted;
3. multiple competing primary letter objects are rejected;
4. annex material cannot create a primary temporal contradiction;
5. file-level metadata is admissible only after one primary object is established;
6. oracle and runtime remain independent implementations;
7. alternatives, binding, provenance and delayed transition history remain separable obligations;
8. no post-opening object route may be added to rescue a fresh corpus.

## 3. Portable source context

Before a source population is opened, freeze:

    source_repository
    source_version
    population_prefix_or_register

Every object_id and evidence handle must bind to the frozen source_repository and source_version.

A source-context mismatch is a contract failure.

## 4. Final A/B/C object grammar

Within the first TEI body:

### Route A — explicit letter object

Enumerate every descendant:

    div type="letter"

that has no ancestor:

    div type="annex"

within the first body.

- exactly one eligible explicit letter -> SINGLE_PRIMARY_DOCUMENT_OBJECT;
- more than one -> MULTIPLE_PRIMARY_DOCUMENT_OBJECTS;
- zero -> continue to Route B/C.

This route applies whether or not a transcription wrapper exists.

Boundary kind:

    EXPLICIT_LETTER_DIV

The selected boundary is exactly the explicit letter div. Dates in sibling continuation/address/note divisions are not silently treated as text-internal claims of the selected boundary.

### Route B — transcription-as-letter

Only if Route A finds zero explicit letters:

- exactly one div type="transcription" in the first body;
- exactly one correspDesc in the TEI document;
- at least one correspAction type="sent";
- the transcription has substantive content.

Then:

    TRANSCRIPTION_AS_LETTER

More than one transcription without a unique Route-A letter is:

    MULTIPLE_PRIMARY_DOCUMENT_OBJECTS

### Route C — strictly untyped direct body letter

Only if Routes A/B find no object and no transcription exists:

- the first body has exactly one direct div child;
- that div has no @type value;
- exactly one correspDesc exists;
- at least one correspAction type="sent" exists;
- the candidate contains at least one of:
  opener, closer, salute, signed, dateline;
- candidate content is substantive.

Then:

    UNTYPED_BODY_LETTER

A typed direct div must never enter Route C.

Otherwise:

    NO_PRIMARY_DOCUMENT_OBJECT

## 5. Claim applicability proof

Every admitted temporal claim must carry:

    object_id
    object_boundary_signature
    applicability_class

Allowed applicability classes:

### FILE_LEVEL_UNIQUE_OBJECT

For file-level metadata admitted because exactly one primary object exists, including:
- msContents/docDate;
- correspAction type=sent/date;
- history/origin/origDate.

### INSIDE_SELECTED_OBJECT_BOUNDARY

For text-internal date carriers that are descendants of the selected object boundary and satisfy the frozen temporal locator grammar, including primary dateline/opener dates.

### EXCLUDED_OUTSIDE_SELECTED_OBJECT

Diagnostic only; never admitted to the active temporal claim set.

### EXCLUDED_ANNEX

Diagnostic only; never admitted to the active temporal claim set.

A claim cannot be rekeyed to object_id without one of the two allowed applicability proofs.

## 6. Selected-boundary temporal extraction

Text-internal temporal claims must be extracted from the actual selected Module-L object boundary, not from the inherited Module-I transcription-only primary selector.

The admitted root claims are:

- file-level docDate claims under FILE_LEVEL_UNIQUE_OBJECT;
- file-level sent-date claims under FILE_LEVEL_UNIQUE_OBJECT;
- date descendants of opener/dateline inside the selected boundary under INSIDE_SELECTED_OBJECT_BOUNDARY.

Date elements in:
- annexes;
- sibling divs outside the selected boundary;
- another explicit letter object

are not admitted as primary text claims.

## 7. Origin evidence

The inherited single-origin contract remains:

- exactly one machine-readable origDate in the chosen origin contract -> SINGLE_ORIGIN_ADMISSIBLE;
- zero -> NO_ORIGIN_EVIDENCE;
- more than one -> COMPOSITE_ORIGIN_UNRESOLVED.

An admitted origin claim must carry:

    FILE_LEVEL_UNIQUE_OBJECT

and the frozen source context.

No project-specific alternative to origDate is introduced in this engine version.

If an independent candidate does not prospectively document origDate, it may support object/discovery transfer but cannot be called a full J-equivalent sustained trajectory under this contract.

## 8. New mandatory pre-fresh controls

The next engine must add and pass at least:

F17 DIRECT_EXPLICIT_LETTER_ACCEPTED
- one body/direct div type=letter;
- no transcription wrapper;
- must be EXPLICIT_LETTER_DIV.

F18 TYPED_DIV_NOT_ROUTE_C
- a sole direct typed non-letter div with letter-like markers;
- must not be UNTYPED_BODY_LETTER.

F19 OUTSIDE_BOUNDARY_DATE_EXCLUDED
- one explicit letter plus a sibling non-letter div containing a date;
- sibling date must not enter active root claims.

F20 SOURCE_CONTEXT_BOUND
- changing frozen source repository/version must change object/evidence binding;
- a mismatched evidence handle must fail applicability.

F21 DIRECT_EXPLICIT_FULL_TRAJECTORY
- a synthetic direct explicit letter with root disagreement and one origDate;
- oracle/runtime must agree and I_RSTAR must pass end to end.

F22 MULTIPLE_DIRECT_EXPLICIT_REJECTED
- two explicit non-annex letters without a transcription wrapper;
- must reject rather than choose first.

F1-F16 remain mandatory regression tests.

## 9. Exposed regression requirement

Before any new independent source is opened, rerun:
- Berlin;
- Paul;
- StaBi;

using their already exposed frozen DAHN source.

Report changes honestly.
The old Module J outcomes remain historical facts and are not overwritten.

A regression change caused by the corrected contract must be explained before a fresh run; it may not be tuned away to reproduce old counts.

## 10. Candidate-screening consequence

A candidate may proceed to a one-time fresh holdout only if generic project documentation establishes before episode opening:

- compatibility with Route A/B/C;
- a closed population rule;
- adequate source provenance;
- the temporal carrier layers required for the specific registered gate.

The next fresh run cannot alter this object/claim engine after seeing candidate episode data.
