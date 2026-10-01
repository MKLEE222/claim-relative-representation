# Module H0 evaluator repair note v2

Date: 2026-09-28
Status: PRE-OUTCOME SOURCE-PRESERVING IMPLEMENTATION REPAIR.

Second failed run:
36384541374

The run terminated before population extraction produced any scientific output.

Failure:
the frozen Journal blob is not globally well-formed XML at this checkpoint. A strict parser reports:

    Opening and ending tag mismatch: div line 10207 and body, line 10585

The source blob is not repaired, rewritten, or replaced.

## Repair

H0 requires only the pre-registered Journal person-mention interface:
- persName surface text;
- ref attribute when present;
- an exact addressable source location.

For the Journal only, extract complete literal:

    <persName ...> ... </persName>

fragments directly from the immutable UTF-8 source string.

For each fragment retain:
- decoded descendant-readable text after removing markup;
- ref attribute;
- exact raw character start/end offsets;
- document-order ordinal.

The source locator is therefore a raw-span locator rather than an XPath:

    raw_char:[start,end)

This preserves the same scientific information class required by the protocol: an addressable, version-bound source span. It adds no semantic repair, no hidden answer, and no new matching signal.

The Site Index remains strict-parsed XML.

No parser recovery mode is enabled.
No malformed outer Journal structure is inferred.
No source byte is changed.

No checkpoint, blob, exposure exclusion, gold rule, person-matching rule, uncertainty lexicon, denominator, discovery trigger, metric, or success criterion is changed.

The two failed runs are preserved and are not experimental outcomes.
