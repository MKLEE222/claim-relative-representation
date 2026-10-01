# Portable object/claim contract v1 — ISO datetime portability amendment

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-AMP-OPENING AMENDMENT.

## 1. Trigger and scientific legitimacy

During project-level, pre-content screening of Auden-Musulin-Papers/amp-data, the project-specific
schema was inspected without opening any edition XML.

That schema requires TEI temporal ISO attributes such as:

    notBefore-iso="2023-10-12T00:00:00+01:00"
    notAfter-iso="2023-10-12T23:59:59+01:00"

The current portable engine already admits the TEI attribute names:
- when-iso;
- notBefore-iso;
- notAfter-iso;
- from-iso;
- to-iso;

but its inherited parser accepts only date-granularity lexical values such as YYYY-MM-DD.

This is a contract/implementation portability defect discovered before candidate episode
opening. It must be repaired before any AMP edition XML is consumed.

This amendment is generic TEI temporal syntax support. It is not an AMP outcome-dependent rule.

## 2. Scope

Historical Modules I/J/K are not modified or reinterpreted.

The portable Module-L engine is extended for future work.

No object grammar, eligibility rule, warrant rule, event rule, comparator budget, or obligation
definition is changed.

Only the lexical parsing of already-admitted *-iso temporal attributes is extended.

## 3. Accepted ISO datetime lexical forms

In addition to all previously accepted temporal forms, the portable engine shall accept:

    YYYY-MM-DDTHH:MM:SSZ

and:

    YYYY-MM-DDTHH:MM:SS+HH:MM
    YYYY-MM-DDTHH:MM:SS-HH:MM

Optional fractional seconds are permitted only on the datetime portion and do not alter the
day-granularity interpretation.

Malformed calendar dates/times/offsets remain non-machine-readable rather than being repaired.

## 4. Day-granularity semantics

The registered scholarly dating task operates at calendar-day granularity.

For an accepted ISO datetime, the temporal interval is therefore the date component encoded in
that datetime's own local offset:

    2023-10-12T23:30:00-05:00
    -> [2023-10-12, 2023-10-12]

Do not convert the instant to UTC before taking the date.

Rationale:
the claim represented in the edition is the encoded local/document calendar date, not an
instant-ordering task.

Timezone/clock information remains in raw_attrs and therefore remains auditable even though the
registered warrant interval is day-granular.

## 5. Range semantics

For:

    notBefore-iso = datetime A
    notAfter-iso  = datetime B

the lower bound is the local encoded calendar date of A and the upper bound is the local encoded
calendar date of B.

Existing open-bound behavior remains unchanged when only one side is present.

Existing date-only and partial-date behavior must remain byte-for-byte semantically unchanged.

## 6. Claim identity

Raw source attributes are preserved exactly.

Therefore claim identity continues to bind:
- the canonical day-level interval;
- the original raw temporal attributes;
- role/ordinal;
- source locator;
- object/applicability/source context.

Two lexically distinct temporal source claims may share a day-level interval without becoming
the same claim.

## 7. Independent implementations

Runtime and oracle must implement ISO-datetime parsing independently.

They may use different parsing strategies but must agree on:
- accepted/rejected lexical forms;
- day-level bounds;
- claim keys under the shared public claim contract.

No shared helper module may contain the scientific parsing decision.

## 8. Mandatory new pre-fresh controls

F31 ISO_DATETIME_EXACT_LOCAL_DAY

A when-iso offset datetime must map to its encoded local calendar day.

F32 ISO_DATETIME_Z_EXACT_LOCAL_DAY

A Z datetime must map to its encoded UTC calendar day.

F33 ISO_DATETIME_BOUNDED_RANGE

notBefore-iso / notAfter-iso offset datetimes spanning different dates must produce the exact
inclusive day interval.

F34 ISO_DATETIME_RAW_ATTRS_PRESERVED

Raw datetime strings must survive unchanged in claim raw_attrs and contribute to claim identity.

F35 ISO_DATETIME_INVALID_REJECTED

Malformed datetime input must not be silently repaired into a machine temporal interval.

F36 LEGACY_DATE_SEMANTICS_UNCHANGED

The pre-existing date-only synthetic trajectory must retain the same oracle/runtime interval,
eligibility and end-to-end result.

## 9. Mandatory regression gate

Before any AMP edition XML may be opened:

1. F1-F30 must still pass;
2. F31-F36 must pass;
3. inherited I/J scientific obligations on portable L must pass;
4. Berlin/Paul/StaBi exposed regression must complete;
5. any change in object/discovery/full-trajectory counts must be attributed and retained;
6. Module M comparator and Module N obligation synthetic gates must still pass.

Only after this gate closes may an AMP one-shot holdout protocol be frozen/launched.

## 10. Claim ceiling

Successful hardening establishes only parser portability for an already-declared TEI temporal
syntax.

It is not evidence that AMP contains eligible trajectories and it is not a positive scientific
result.
