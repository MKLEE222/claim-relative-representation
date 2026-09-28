# Portable object/claim contract v1 — embedded text scope amendment

Date frozen: 2026-09-28
Status: PRE-FRESH HARDENING AMENDMENT FROM ALREADY-EXPOSED DAHN OBJECT AUDIT. NO NEW INDEPENDENT EPISODE XML OPENED.

## 1. Empirical trigger

Document-level J-to-L exposed regression identified two Paul files in which literal Route A changed:

    SINGLE_PRIMARY_DOCUMENT_OBJECT -> MULTIPLE_PRIMARY_DOCUMENT_OBJECTS

Source inspection showed that the second `div type="letter"` is not a sibling primary document. It is an embedded text inside the main letter:

    primary letter
      -> floatingText
         -> body
            -> div type="letter"

One source revision log explicitly describes this as a letter inside the letter.

Therefore the current rule 'all descendant div type=letter in the first body compete as primary objects' is too flat.

## 2. Frozen primary-object scope

Let B0 be the first TEI body used as the document-level primary body.

A Route-A explicit letter candidate is primary-eligible only if, on the ancestor path from the candidate to B0, there is no:

    floatingText

and no nested:

    body != B0

Thus an explicit letter inside a floating/nested text island is an EMBEDDED scholarly object, not a competing PRIMARY scholarly object.

The same scope restriction applies to Route-B transcription enumeration.

## 3. Frozen temporal-claim scope

For a selected primary object, a text-internal date is admissible only if it is inside the selected object boundary and not inside an embedded text island below that selected boundary.

Dates inside:

    floatingText

or a nested:

    body

below the selected primary object are not active primary temporal claims.

They must be retained diagnostically as:

    EXCLUDED_EMBEDDED_OBJECT

Annex exclusion has precedence when a date is also under an annex/annexe container.

## 4. Scientific meaning

This amendment distinguishes hierarchical object roles:

    primary scholarly object
    embedded scholarly object
    annex/enclosure object

Temporal composability is licensed only within the role/scope selected by the registered task.

Object identity is therefore not flat set membership in one XML file.

## 5. Scope boundary

This amendment is intentionally narrow.

It does not infer embedded status from arbitrary `quote`, `cit`, `attachment`, `appendix`, or prose semantics.

Only explicit TEI structural islands visible before a task-specific interpretation are covered:

- `floatingText`;
- a nested `body` different from the first primary body.

Any future additional embedding vocabulary requires a separately frozen generic amendment before outcome exposure.

## 6. Mandatory controls

Add a portable control containing:

- one primary Route-A letter;
- one nested `floatingText/body/div type="letter"` with a conflicting machine-readable date.

The engine must:

1. keep exactly one primary object;
2. not count the nested letter as a Route-A competitor;
3. keep the embedded date out of active temporal claims;
4. classify that date as `EXCLUDED_EMBEDDED_OBJECT`;
5. preserve oracle/runtime agreement;
6. preserve end-to-end success of the primary trajectory when otherwise eligible.
