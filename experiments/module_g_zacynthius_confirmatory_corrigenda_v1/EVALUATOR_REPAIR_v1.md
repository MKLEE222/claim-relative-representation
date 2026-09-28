# Module G evaluator repair note v1

Date: 2026-09-28
Status: PRE-OUTCOME IMPLEMENTATION REPAIR.

First CI run:
36382187686

The run terminated during source-contract verification before any of the 48 matrix cells were evaluated.

Failure:
CZ-C1's structural target is encoded as:

    <w><hi rend="rubric">ευαγγελιον</hi></w>

The generic record builder stores direct <hi> text in the record's plain-text key.
Its word-stream key is empty because the <hi> element itself does not contain a descendant <w>.

The first implementation incorrectly tested the rubric record's word_base field and therefore returned zero locator groups even though the frozen schema audit had already established the target.

Repair:
- for rubric target matching only, compare the published anchor against the record's plain_base field;
- update the matching source-contract assertion accordingly.

No source, parent commit, correction event, normalization rule, matrix arm, metric, denominator, hypothesis, or claim rule changes.

The failed run is preserved and is not an experimental outcome.
