# Module P synthetic gate result v1

Date: 2026-09-29
Status: COMPLETED DEVELOPMENT HARDENING GATE.

## 1. Frozen contracts

Scientific charter:

    c42566c5dde26e354d3794a2183ca62b94033dd6

Implementation contract:

    992ba41708d006965e4252816d813c3e475557d4

The synthetic study did not change either contract after seeing results.

## 2. Transparent implementation debugging

First Module-P run:

    36516199162

The inherited L/M/N gates passed.
The Module-P synthetic gate failed because oracle/runtime Phi(ALTERNATIVE_SET) canonical ordering
did not match.

A second diagnostic run:

    36516259770

showed:
- raw root warrants were identical;
- raw post-event warrants were identical;
- claim keys were identical;
- object/source/event bindings were identical;
- only the oracle Phi alternative ordering differed.

The frozen implementation contract had already specified canonical sorting by:

    role, lower-bound, upper-bound

The oracle implementation had incorrectly sorted by a JSON serialization that prioritized
interval text.

Fix:

    0391a98aa158316843b3e8628e85537baa9e9051

The fix changed only oracle canonical ordering to the already frozen rule.
It did not change eligibility, warrant logic, event semantics, transition classes or test
expectations.

## 3. Successful gate

Workflow:

    module-p-evidence-release-revision-v1

Successful run:

    36516302575

All inherited gates passed:
- portable F17-F36;
- inherited I/J obligations;
- Module-M strong comparator control;
- Module-N non-substitutability crossover control.

Module-P controls:

    P-F1 VALID_CONFLICT_FORMATION               PASS
    P-F2 VALID_UNRESOLVED_TO_WARRANTED          PASS
    P-F3 BASIS_ONLY_NOT_ELIGIBLE                PASS
    P-F4 WRONG_OBJECT_REJECTED                  PASS
    P-F5 WRONG_SOURCE_VERSION_REJECTED          PASS
    P-F6 MISSING_APPLICABILITY_REJECTED         PASS
    P-F7 COLLATERAL_MUTATION_DETECTED           PASS
    P-F8 NO_HISTORY_SEPARATION                  PASS
    P-F9 SNAPSHOT_NONIDENTIFIABILITY            PASS
    P-F10 NULL_EVENT_NOT_PROMOTED               PASS

## 4. Regime separation

The two positive Module-P synthetic cases deliberately do NOT satisfy the old Module-I D1/D2
ambiguity-discovery gate.

Yet they are ERIR-eligible under the independently frozen evidence-release task.

Thus Module P is not a relabeling of ambiguity-triggered inquiry.

### P-F1

Before:

    EXACT(1900-01-01)

Later admissible evidence:

    origDate = 1900-01-02

After:

    ALTERNATIVE_SET(origDate, sent)

Transition class:

    P-U1 CONFLICT_FORMATION

P1-P7:

    all PASS

### P-F2

Before:

    UNRESOLVED(NO_MACHINE_TEMPORAL_CARRIER)

Later admissible evidence:

    origDate = 1900-01-02

After:

    EXACT(1900-01-02)

Transition class:

    P-U2 RESOLUTION_OR_ACQUISITION

P1-P7:

    all PASS

## 5. Null-event discipline

P-F3/P-F10 establish:

    Phi(W_root) == Phi(W_post)

even though the later evidence has a distinct claim identity/basis.

Such an event is:

    ADMISSIBLE_NULL_EVENT

and is not promoted into the substantive revision denominator.

## 6. Failure controls

Wrong object, wrong source version and missing applicability proof are rejected before mutation.

A collateral mutation is detected even when the evidence event itself is valid.

Dropping retained history preserves the correct post-event result/selective update but fails the
delayed-history capability.

## 7. Comparator control

On the Module-P positive synthetic case:

B_CURRENT_REOPEN:
- T1 current state = PASS;
- T2 current provenance = PASS.

B_ORDERED_SNAPSHOTS:
- T1 = PASS;
- T2 = PASS;
- T3 exact state delta = PASS.

The registered history-semantic tasks remain outside those comparator information budgets.

## 8. Claim ceiling

This result establishes only that Regime B is:
- formally distinct from the D1/D2 discovery regime;
- internally executable under the frozen portable binding/action mechanism;
- falsifiable by preregistered controls.

It is not natural-corpus confirmation.

AMP may now be used only as exposed development evidence.
