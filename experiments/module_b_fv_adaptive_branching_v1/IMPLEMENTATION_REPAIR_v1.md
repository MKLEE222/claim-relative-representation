# Module B implementation support repair v1

Date: 2026-09-28
Status: PRE-OUTCOME IMPLEMENTATION REPAIR AFTER SUPPORT STOP
Failed run: GitHub Actions 36372539414

## Stop

The first Module-B execution stopped before producing a results artifact or printing any branch/collision outcome.

The failure occurred while attempting to parse every `sga-add` start-to-end slice as a standalone XML fragment.

Traceback:

`XMLSyntaxError: Opening and ending tag mismatch: fragment ... and longToken`

This reveals a support-feasibility problem in the original `LOCAL_SCOPE_XML` implementation premise: source-native `sga-add` milestones can begin or end while another XML element is already open. A raw milestone-bounded slice is therefore not guaranteed to be a standalone well-formed XML subtree.

No branch counts, natural-collision counts, interface scores, or selective-update outcomes were observed before this stop.

## Repair

The source, population, current documentary answer, three branch families, SOURCE_LINKED baseline, collision criteria, controlled `@next` event, and success/failure rules remain unchanged.

The implementation is repaired as follows:

1. The reference model is reconstructed by one full-document event traversal.
   - active `sga-add` scopes are tracked across element boundaries;
   - text is assigned to every currently active scope;
   - active `del` / `mdel` context is tracked independently;
   - cancellation records are assigned when cancelled text actually overlaps an active addition scope.

2. The infeasible name `LOCAL_SCOPE_XML` is superseded by `LOCAL_SCOPE_SERIALIZATION`.
   - it is the literal source substring from the opening `sga-add` milestone through its matching closing milestone;
   - it may be structurally unbalanced as standalone XML;
   - it does not receive hidden parent/ancestor context.

3. Consequently, `LOCAL_SCOPE_SERIALIZATION` no longer claims exact negative or complete B-CANCEL determination.
   - visible local `del` / `mdel` markers may license a cancellation-inspection trigger;
   - the complete B-CANCEL structured answer remains UNKNOWN without sufficient inherited context or source reopening.

4. START_ATTRS_PLUS_TEXT behavior and SOURCE_LINKED exact behavior are unchanged.

5. Natural collision auditing still uses byte equality of the complete retained interface.
   The raw local serialization is compared byte-for-byte; no normalization is introduced.

This is a support repair, not a favorable-outcome adjustment.

## Claim effect

The repair weakens, rather than strengthens, the local-interface assumption.

If successful execution later shows source-linked recovery, that baseline receives full credit.

The failed run is retained in the execution record and is not counted as a negative scientific outcome.
