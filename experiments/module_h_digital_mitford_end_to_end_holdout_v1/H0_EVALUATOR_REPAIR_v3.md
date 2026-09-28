# Module H0 evaluator repair note v3

Date: 2026-09-28
Status: PRE-OUTCOME IMPLEMENTATION TYPO REPAIR.

Third failed run:
36384760599

The run terminated before population extraction produced any scientific output.

The frozen Journal blob was inspected only to verify tag syntax and confirms ordinary:

    <persName ref="#...">...</persName>

markup is present.

Failure:
the JavaScript-generated Python source over-escaped raw regular-expression tokens. The committed expressions contained:

    \\b
    \\s

inside Python raw strings and therefore matched literal backslashes rather than regex word/whitespace classes.

Repair:
replace the over-escaped tokens with the intended Python raw-regex forms:

    \b
    \s

for:
- persName fragment matching;
- ref attribute matching;
- XML-comment removal.

No source, checkpoint, gold population, exposure rule, matching rule, uncertainty lexicon, scientific interface, metric, or success criterion changes.

This is a code-generation typo repair before any H0 outcome.
