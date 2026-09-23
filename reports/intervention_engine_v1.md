# Intervention engine validation v1

Date: 2026-09-23

## Result

The controlled representation operator layer is now executable and CI-tested.

GitHub Actions run 19 completed successfully after adding intervention invariant tests.

The test suite verifies, on the ten-event canonical representation fixture:

1. each intervention changes exactly one declared representation field;
2. the textual-content key is invariant under every intervention;
3. restoring the removed coordinate reconstructs the baseline record exactly;
4. every matched negative-control pair remains structurally disjoint from the intervention coordinate that defines its target treatment.

This is a **construction-validity result**, not a claim-state outcome.

## Gate T update

The intervention family now has documented analogues in TEI:

- responsibility metadata for attribution;
- revision history for temporal ordering;
- link/linkGrp structures for stand-off relations;
- target/corresp pointers for binding;
- orig/reg/choice for normalization and distinction collapse.

The native Project Gutenberg object is retained as a negative witness against an overly simple flattening story. Its UTF-8 text still exposes edition chronology, editorial attribution, note structure, and cross-layer pointers.

Therefore Gate T is now:

**DESIGN PASS / EMPIRICAL TRANSFORMATION WITNESS PENDING**

The operators are realistic as controlled abstractions and satisfy one-coordinate invariance, but we have not yet shown that a particular external corpus pipeline applies exactly these operators to this historical object.

## What remains unopened

No retain/revise/defer/withhold outcome has been computed from an intervention.

No second independent relation coder has been scored.

No restoration result is counted as empirical merely because the operator can mechanically restore a field.

The next admissible empirical step is independent relation coding, followed by source-grounded claim adjudication under the frozen intervention family.
