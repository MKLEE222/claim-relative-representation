# Module M — genuine DH comparator contract v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-RESULT CONTRACT. EXPOSED DEVELOPMENT DATA ONLY.

## 1. Scientific question

The comparator study tests a Digital Humanities claim, not an algorithmic leaderboard claim:

    current-state recoverability
    !=
    scholarly-history recoverability

The study asks whether two strong and realistic access regimes can substitute for durable,
claim-relative transition history when a later scholar must reconstruct not only the current
warranted state, but how and why that state changed.

No fresh independent episode population is consumed in Module M.
Berlin, Paul and StaBi are exposed development/regression corpora only.

## 2. Reference interface

RSTAR is the portable Module-L retained interface.

It is not treated as superior by definition.
The comparator study must separately score:
- current-state recovery;
- state-delta recovery;
- current provenance;
- transition attribution;
- delayed history audit.

A comparator that fails current-state recovery is not an admissible positive baseline for the
history-separation claim.

## 3. Comparator B_CURRENT_REOPEN

Interpretation:

    A later scholar may lawfully reopen the current/latest source object and recompute the
    current warranted state with the frozen portable parser.

Capabilities intentionally granted:
- full current source access;
- frozen source/object identity;
- all currently visible active temporal claims;
- current claim-level source locators/provenance;
- exact reconstruction of the terminal warrant and live claim set.

Information not retained:
- previous warranted state;
- ordered state snapshots;
- event ledger;
- transition ledger;
- evidence-release event identity;
- durable event-to-evidence binding.

The comparator may not call or inspect an RSTAR transition trace.

Required positive gate:

    CURRENT_STATE_EXACT = 100% of every eligible exposed episode.

If this fails, B_CURRENT_REOPEN is not a valid comparator and Module M is INVALID until the
implementation is corrected without changing the scientific contract.

## 4. Comparator B_ORDERED_SNAPSHOTS

Interpretation:

    A versioned scholarly infrastructure retains ordered complete temporal state snapshots,
    but no explicit transition semantics or event-to-evidence authorization record.

Capabilities intentionally granted:
- S0: complete root temporal state;
- S1: complete temporal state after later evidence is present;
- S2: complete temporal state after the registered null/non-temporal maintenance step;
- source/object/claim provenance contained in each state;
- deterministic exact diff between adjacent snapshots;
- exact recovery of terminal warrant and live claim set.

Information not retained:
- event class;
- event identifier;
- explicit evidence-release authorization;
- target-document/event binding;
- a durable assertion that a newly visible claim caused rather than merely co-occurred with
  a state transition;
- a durable semantic record distinguishing evidence release, state import, repair, migration,
  or another operation that yields the same adjacent states.

The snapshot comparator may identify newly visible claims from a diff.
That is state-difference recovery, not by itself authorized transition attribution.

Required positive gates:

    CURRENT_STATE_EXACT = 100%
    STATE_DELTA_EXACT = 100%

for every eligible exposed episode.

If either gate fails, B_ORDERED_SNAPSHOTS is not an admissible strong comparator.

## 5. DH audit tasks

Module M separates five tasks.

### T1 CURRENT_STATE

Recover:
- terminal warrant;
- terminal live claim set.

### T2 CURRENT_PROVENANCE

For every terminal live claim, recover:
- claim key;
- source file;
- source locator contract;
- object identity / applicability proof.

### T3 STATE_DELTA

Recover the exact change in temporal state between the pre-evidence and post-evidence states:
- added / removed / changed claims;
- warrant change;
- live-key change.

This task does not require causal/event semantics.

### T4 TRANSITION_ATTRIBUTION

Recover the registered scholarly transition as an authorized historical event:
- event class;
- event identity;
- target scholarly object;
- evidence key admitted by the event;
- before warrant;
- after warrant;
- absence/presence of collateral temporal mutation.

### T5 DELAYED_HISTORY_AUDIT

At a later time, reconstruct:
- the evidence-release transition;
- the evidence item bound to it;
- before/after warranted states;
- registered null/non-temporal event identity;
- transition history needed to explain why the current state has its present warrant.

T5 is stronger than T1-T3.

## 6. Indistinguishability control

The study must contain at least one synthetic pair H_A / H_B such that:

- object identity is identical;
- S0, S1 and S2 temporal snapshots are byte-for-byte identical under the comparator's
  canonical snapshot representation;
- terminal current source-visible claims are identical;
- current warrant is identical;
- source locators of visible claims are identical;

but the registered histories differ, for example:

H_A:
    EVIDENCE_RELEASE(origin evidence)
    -> NON_TEMPORAL_MAINTENANCE

H_B:
    STATE_IMPORT / RECONSTRUCTION producing the same S1
    -> a different no-op operation producing the same S2

The ordered-snapshot comparator must emit identical information for H_A and H_B.
The history oracle must distinguish them.

This is the primary non-identifiability witness.
It prevents the history result from being created merely by an evaluator that withholds credit.

## 7. Primary claims and ceilings

Module M may support, on exposed development data:

A. A strong positive capability claim:
   current/latest reopening can recover the terminal warranted state.

B. A stronger positive capability claim:
   ordered full snapshots can recover both terminal state and exact state differences.

C. A bounded history-separation claim:
   current state or state snapshots do not determine transition semantics when distinct
   scholarly histories are observationally equivalent under those access regimes.

Module M does NOT license:
- RSTAR superiority on unseen corpora;
- universal necessity of a transition ledger for every scholarly task;
- a fresh confirmatory claim;
- a claim that ordinary version control never records useful history.

The licensed statement is task-relative:
for the registered delayed scholarly-history audit, the compared information regimes may be
insufficient even when current-state and state-delta recovery are exact.

## 8. Exposed corpus evaluation

Run only on Module-L full-trajectory exposed episodes.

Report separately for each corpus/interface:
- N eligible;
- T1 current state exact;
- T2 current provenance exact;
- T3 state delta exact;
- T4 transition attribution exact;
- T5 delayed history audit exact.

StaBi remains an applicability corpus and may legitimately have N=0.

No score may combine N=0 applicability rows with eligible performance denominators.

## 9. Stop rule

Do not alter comparator information budgets after inspecting exposed results merely to enlarge
the separation.

If a comparator recovers T4/T5 under the frozen information budget, retain that result and
weaken the history-retention claim.

If a comparator fails its required positive gate, repair only implementation bugs that violate
this frozen contract; do not weaken the baseline.
