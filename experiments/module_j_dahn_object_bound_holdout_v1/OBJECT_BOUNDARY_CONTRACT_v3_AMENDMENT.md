# Module J object-boundary contract v3 amendment

Date: 2026-09-28
Status: EXPOSED-DEVELOPMENT REPAIR BEFORE ANY NEW FRESH HOLDOUT.

## 1. Additional exposed source fact

After v2, Berlin still contained one clear false-negative serialization:

    Brief13vonJAEuleranJHSFormey.xml

It is a single correspondence object with:
- one correspDesc;
- one sent correspAction;
- one direct body div;
- opener/salute and ordinary letter body;
- no div type="transcription";
- no div type="letter".

By contrast, the exposed StaBi aggregate objects also have a direct untyped body div, but contain only placeholder content such as:

    [Transcription to come - See metadata]

and no letter-specific body structure.

Therefore type="transcription" itself is not a necessary scholarly-object marker.

## 2. Route C — untyped body-container letter

If Routes A/B fail, exactly one direct child div of the first body may be selected as the primary scholarly object only if ALL hold:

1. the first body has exactly one direct div child;
2. there is no div type="transcription";
3. there is no eligible non-annex div type="letter";
4. exactly one correspDesc exists;
5. at least one correspAction type="sent" exists;
6. the candidate div contains at least one letter-specific structural marker:
   - opener,
   - closer,
   - salute,
   - signed,
   - dateline.

If these hold:

    object_boundary_kind = UNTYPED_BODY_LETTER

Otherwise the object remains NO_PRIMARY_DOCUMENT_OBJECT.

## 3. Why the marker requirement is load-bearing

The marker requirement prevents file-level correspondence metadata plus a placeholder body from creating a false scholarly object.

Specifically, the exposed StaBi aggregate records with a placeholder transcription div must remain NO_PRIMARY_DOCUMENT_OBJECT even though they contain sent metadata.

## 4. Multiple objects remain rejected

The four exposed Berlin files with 2-3 explicit non-annex div type="letter" objects remain MULTIPLE_PRIMARY_DOCUMENT_OBJECTS.

No first-letter fallback is authorized.

## 5. Additional tests

F15:
- one untyped body div with opener/salute and one correspondence record must be admitted as UNTYPED_BODY_LETTER.

F16:
- one untyped body div containing only placeholder transcription text plus multiple sent dates must remain NO_PRIMARY_DOCUMENT_OBJECT.

F1-F14 remain mandatory.

## 6. Freeze rule

Routes A, B and C now define the complete Module J object grammar.

No new fresh holdout may add Route D after source inspection.