# Module J object-boundary contract v2 amendment

Date: 2026-09-28
Status: EXPOSED-DEVELOPMENT REPAIR BEFORE ANY NEW FRESH HOLDOUT.

## 1. Why v1 is insufficient

Module J v1 correctly rejects the exposed StaBi aggregate objects, but exposed Berlin reaudit showed a severe false-negative:

- 190 Berlin XML documents parsed;
- v1 classified 184 as NO_PRIMARY_DOCUMENT_OBJECT;
- only 2 as SINGLE_PRIMARY_DOCUMENT_OBJECT;
- previously source-audited Berlin letters such as Brief007 encode the letter directly inside one div type="transcription" and do not wrap it in div type="letter".

Therefore v1 confounds one TEI serialization pattern with scholarly object identity.

This is a development-set repair, not a post-holdout rescue.
Berlin, Paul and StaBi are already exposed.
No new fresh corpus has been opened under Module J.

## 2. Revised primary-object selection

Within the first body:

### Route A — explicit letter object

1. locate transcription containers;
2. within the first transcription, enumerate direct child div type="letter" not inside annex;
3. if exactly one exists, select it;
4. if more than one exists, classify MULTIPLE_PRIMARY_DOCUMENT_OBJECTS;
5. if zero, enumerate descendant non-annex div type="letter";
6. if exactly one exists, select it;
7. if more than one exists, classify MULTIPLE_PRIMARY_DOCUMENT_OBJECTS.

### Route B — transcription-as-letter object

If Route A finds zero letter divs, the transcription container itself may be the primary scholarly object only if ALL hold:

1. exactly one div type="transcription" exists in the first body;
2. it contains no eligible non-annex div type="letter";
3. exactly one correspDesc exists in the document;
4. at least one correspAction type="sent" exists;
5. the transcription contains substantive source text/content rather than being empty metadata scaffolding.

If these conditions hold:

    object_boundary_kind = TRANSCRIPTION_AS_LETTER

and the boundary signature is computed over that transcription container.

Otherwise:

    NO_PRIMARY_DOCUMENT_OBJECT.

## 3. Multiple transcription containers

If more than one transcription container exists and no unique explicit letter object can be established without choosing among them:

    MULTIPLE_PRIMARY_DOCUMENT_OBJECTS.

Do not select the first transcription merely by document order.

## 4. Metadata applicability

File-level docDate, sent-date metadata and origin evidence may bind to the selected object only after either Route A or Route B establishes one unique primary object.

The object_id remains:

    H(source file, source version, boundary kind, primary boundary signature)

Boundary kind is included so an explicit letter object and a whole-transcription object with identical text do not silently alias.

## 5. Required exposed-development checks

Berlin:
- previously audited direct-transcription letters must be restored as single objects when Route B conditions hold;
- known D1/D2 development episodes should not disappear merely because they lack div type="letter".

Paul:
- explicit primary letters continue to use Route A;
- annex dates remain excluded.

StaBi:
- all seven Module I aggregate candidates remain non-eligible;
- absence of a transcription container cannot be repaired by file-level sent dates.

## 6. Added tests

F13 / positive contract control:
- one transcription with direct letter content, one correspDesc and sent action, and no nested letter div must be admitted as TRANSCRIPTION_AS_LETTER.

F14:
- two transcription containers without a unique explicit letter must be rejected as MULTIPLE_PRIMARY_DOCUMENT_OBJECTS.

The previous F1-F12 tests remain mandatory.

## 7. Anti-flexibility rule

This amendment is frozen from exposed Berlin/Paul/StaBi only.

A future fresh holdout may not add another object-boundary serialization route after source inspection.

If a fresh corpus uses a third representation not covered by Route A/B, it fails this contract rather than being retrofitted.
