# Dynamic sufficiency memo v3 — applicability after confirmatory corrigenda transfer

Date: 2026-09-28  
Status: THEORY-DESIGN UPDATE FROM MODULE G. NOT A NEW THEOREM.

## 1. New obligation exposed by Module G

Modules D-F emphasized distribution of task-relevant information across:

    retained state S_t
    incoming event E_t
    lawful access A_t

Module G shows that this is not sufficient as a complete update criterion.

A correction can have:
- an exact target;
- an exact desired result;

and still fail to license an exact transition when the event's assumed source-side state is incompatible with the retained parent snapshot.

Observed confirmatory examples:

CZ-C2:
- target exact
- result exact
- parent is partially preintegrated relative to the published correction

CZ-C4:
- target exact
- result exact
- correction assumes CPG7058
- frozen parent carries CPG7039

Thus:

    TargetExact + ResultExact
    !=
    WarrantedTransition

## 2. Event applicability

Introduce a task-relative applicability predicate:

    Applicable(E_t, S_t; K)

where K is the declared source/version contract.

For replacement-style corrections, applicability asks whether the correction's source-side assertions are compatible with the retained parent state under the declared normalization and locator rules.

This is not a claim that every correction must include a literal old string.

It is a requirement that the event have a lawful interpretation as a transition from the state to which it is being applied.

## 3. Revised dynamic researchability interface

Keep:

    I_t(h) = (S_t(h), E_t(h), Obs_A(h))

but separate two conditions.

### Information determinacy

If two admissible histories expose the same available interface, the task output must be the same.

### Transition applicability

The incoming event must be licensed against the declared parent/source state.

A bounded update rule therefore has the form:

    Applicable(E_t, S_t; K)
    AND
    Determinate_T(S_t, E_t, A_t)
    ->
    WarrantedUpdate_T

The implication is task-relative and contract-relative.

## 4. Five-way update decomposition

Module G motivates keeping at least these conditions distinct:

1. TARGET DETERMINACY
   Which source/relation/span is being revised?

2. EVENT APPLICABILITY
   Does the event's source-side/precondition state match the declared parent state?

3. RESULT DETERMINACY
   What state should the target have after the revision?

4. SELECTIVITY
   Are unaffected source relations/spans preserved?

5. PROVENANCE / WITNESS PRESERVATION
   Can the corrected current state coexist with the historical parent witness and correction history?

When historical update history is itself queried, add:

6. TRANSITION AUDITABILITY
   Can the exact old->new path be reconstructed?

These conditions should not be collapsed into one scalar representation score.

## 5. Why source version now matters

C2/C4 show that a correction event is not context-free.

The same published corrigendum may be:
- directly executable against one source state;
- partially redundant against another;
- incompatible with a third.

Therefore identifiers and corrected values alone are not a complete dynamic carrier.

A correction event has an implicit or explicit applicability domain.

For sustained research systems, version/source-state binding is part of warranted update semantics.

## 6. Relation to Module C

Module C showed:

    stable relation strings
    !=
    stable source-route executability over time.

Module G adds:

    stable correction notice
    !=
    executable transition on every source snapshot.

Together:

    source evolution affects both
    access to evidence
    and
    applicability of later update events.

This creates a genuinely temporal representation problem.

## 7. Confirmatory status

Module G was frozen before Codex Zacynthius XML-body inspection and retained the complete four-event digital corrigenda set.

Results:

- 2/4 clean full executions
- 1 target-binding transfer witness
- 2 representation-structure witnesses
- 1 source-access repair witness
- linked atomicity null
- two source-state/version applicability nulls

This is best treated as:

    bounded confirmatory mechanism transfer
    with retained negative evidence.

The confirmatory value comes from preserving the complete correction set and the parent-version mismatch results, not from maximizing a success fraction.

## 8. Revised mother-problem direction

The sustained-discovery question is now less naturally phrased as:

    What static representation is sufficient?

and more naturally as:

> What information interface and transition contract are sufficient for a research system to continue making selective, source-compatible, auditable warranted updates over time?

A compact formal object is:

    DynamicResearchability(S_t, E_t, A_t, T; K)

where K includes the source/version/admissibility contract.

## 9. Current empirical chain

A/B:
current answer != future continuation state

B2:
uncertainty amount != uncertainty-to-evidence binding

C:
stable symbolic relation != time-invariant source executability

D:
natural selective epistemic/topology revision exists

E:
information obligations distribute across state/event/access;
terminal child recovery != transition audit

F:
published lexical replacement pair != source-scoped historical correction

G:
independent-project confirmation of binding/structure/access mechanism;
exact target + exact result != applicable transition under source-version mismatch

This is now a coherent dynamic researchability program rather than a collection of representation-loss cases.

## 10. Next restraint

Do not immediately add another correction corpus.

Before new experiments, the evidence chain should be re-audited at the manuscript-claim level:

- which claims are now independently confirmed;
- which remain development-only;
- which are source-version specific;
- which deserve theorem/formalization versus empirical mechanism language.

The next experiment should be chosen only after that audit.
