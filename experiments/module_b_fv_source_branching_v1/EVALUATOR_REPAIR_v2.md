# Module B evaluator repair v2

Date: 2026-09-28
Status: POST-v1 IMPLEMENTATION REPAIR ON EXPOSED DEVELOPMENT DATA; NOT A FRESH CONFIRMATORY RUN.

## Trigger

Module B v1 executed successfully but reported zero B_INTERNAL_CANCELLATION checkpoints.

This conflicts with a pre-existing Module A source witness established before Module B v1:
- enclosing addition sID c57-0020__main__d4e4257;
- source contains <mdel>or</mdel> between that addition's start and end milestones.

Direct inspection of run.py showed the v1 cancellation regular expression was serialized as a Python raw string containing literal double backslashes:

    r"<(del|mdel)\\b[^>]*>(.*?)</\\1\\s*>"

That pattern searches for literal backslash sequences rather than the intended word boundary, backreference and whitespace operator. It therefore cannot validate the frozen B_INTERNAL_CANCELLATION branch.

## Repair

Evaluator v2 changes only the cancellation parser to:

    r"<(del|mdel)\b[^>]*>(.*?)</\1\s*>"

No source, population, branch grammar, interface, control, denominator, or disposition is changed.

Before evaluating the full population, v2 must assert that the pre-existing Module A witness c57-0020__main__d4e4257 contains an mdel whose normalized text is "or".

## Authority

- v1 raw output is preserved.
- Any v1 metric depending on cancellation detection is invalidated by this implementation defect.
- Metrics independent of cancellation parsing may be compared descriptively, but v2 is the authoritative development reanalysis for Module B.
- Because the v1 outcome has already been observed, v2 is not a blind replication and cannot upgrade the study to confirmatory evidence.

## Anti-tuning

No further branch type may be added in v2.
The repair must be applied to all 112 source addition spans and all 493 apparatus units.
