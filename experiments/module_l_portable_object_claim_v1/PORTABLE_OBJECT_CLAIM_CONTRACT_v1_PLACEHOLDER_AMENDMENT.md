# Portable object/claim contract v1 — pre-fresh placeholder-status amendment

Date frozen: 2026-09-28
Status: PRE-FRESH HARDENING AMENDMENT FROM GENERIC PROJECT DOCUMENTATION; NO CANDIDATE EPISODE XML OPENED.

## 1. Reason

The inherited J discipline rejects placeholder material as a scholarly letter object.

Prospective independent-project documentation inspected during Module L screening establishes that a project may keep metadata-complete placeholder TEI files in its correspondence population and mark them generically with:

    revisionDesc status="placeholder"

Such a file can still contain correspondence metadata and may use an otherwise Route-A-compatible body skeleton.

Without an explicit document-status gate, Route A could admit a not-yet-transcribed placeholder merely because its encoding shape looks like a letter.

## 2. Frozen gate

Before Routes A/B/C are evaluated:

    if any revisionDesc has normalized @status == "placeholder":
        object status = NO_PRIMARY_DOCUMENT_OBJECT
        reason = PLACEHOLDER_DOCUMENT

No temporal claims from that file may enter discovery or a full trajectory.

## 3. Scope

This is not a general quality filter and does not exclude arbitrary draft/review states.

Only the explicit status value placeholder is added here because it is prospectively documented before episode opening and corresponds to the already-established J placeholder exclusion principle.

## 4. Mandatory control

Add a direct explicit div type="letter" fixture with valid correspDesc/date/origin structure but revisionDesc status="placeholder".

Both oracle and runtime must reject it before temporal discovery.
