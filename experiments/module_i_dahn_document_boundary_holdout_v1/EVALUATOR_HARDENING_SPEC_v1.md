# Module I evaluator hardening specification v1

Date: 2026-09-28
Status: PRE-HOLDOUT IMPLEMENTATION REBUILD. THE STABI HOLDOUT REMAINS UNOPENED.

## 0. Reason for rebuild

The first Module I implementation fixed Module H's document-boundary failure, but post-implementation audit found several evaluation paths that could make positive results partially definitional:

1. policy discovery and discovery gold reused the same eligibility function;
2. policy warrant and warrant gold reused the same warrant function;
3. neutral-event stability was implemented as state copy rather than an executed event;
4. collateral revision count was assigned from success state rather than measured from a full state diff;
5. unresolved-alternative persistence was inferred from final warrant equality rather than source-bound claim identity;
6. delayed transition audit was assigned from interface type rather than reconstructed from a retained ledger.

No StaBi holdout XML body has been opened.
Therefore Module I remains eligible for a clean pre-holdout implementation rebuild.

## 1. Architectural separation

The rebuilt evaluator must contain two independent implementations.

### Runtime/policy implementation

Responsibilities:
- parse the interface-visible source state;
- build R* and ablations;
- detect a live question;
- execute OPEN_ORIGIN;
- apply origin evidence to a mutable research state;
- apply a neutral maintenance event;
- retain/discard history according to interface arm;
- answer delayed query from the resulting state and ledger.

The runtime may not call oracle eligibility/warrant/update functions.

### Oracle implementation

Responsibilities:
- independently parse the raw XML with a different XML library/traversal;
- independently identify the primary document boundary;
- independently extract t0 carriers and the canonical primary origDate;
- independently determine D1/D2 eligibility;
- independently compute contracted root/post-origin warrant;
- independently compute the expected source-bound alternatives that must remain live;
- independently derive the expected origin transition and neutral-event non-effect.

The oracle may not import runtime parsing, eligibility, warrant, state-transition, or audit functions.

Only normalized serialized outputs are compared.

## 2. Discovery evaluation

Runtime discovery output must contain:
- query type;
- trigger class: D1 or D2;
- source-bound disputed claim keys.

Oracle independently outputs the expected trigger class and expected live claim keys.

Discovery is exact only if:
- query presence/absence matches oracle eligibility;
- trigger class matches;
- all disputed runtime claim keys belong to the current primary document;
- the runtime set covers the oracle's live conflicting/narrowing carriers required by the trigger.

Do not score discovery by asking the same predicate that produced the runtime query.

## 3. Independent warrant evaluation

The runtime computes its warrant from interface state.

The oracle computes root and post-origin warrant independently from raw source.

`warrant_exact` is true only when normalized runtime warrant equals independently computed oracle warrant.

No shared warrant helper is permitted across the implementations.

## 4. Executed state transitions

Represent the runtime research state explicitly:

    {
      document identity,
      source/version,
      active source-bound claims,
      current warrant,
      unresolved/live claim identities,
      evidence ledger,
      event ledger,
      transition ledger,
      Q0
    }

### OPEN_ORIGIN

OPEN_ORIGIN is a real event with:
- event identity;
- source locator/handle;
- applicability precondition;
- target document identity;
- released origin claim;
- before-state digest;
- after-state digest.

The update must be performed by the runtime transition operator.

### Neutral maintenance event

The frozen revisionDesc event is also executed through the transition operator.

Its declared target class is non-temporal maintenance.

It must:
- append an event record;
- leave temporal claims unchanged;
- leave temporal warrant unchanged;
- leave live alternatives unchanged.

`null_event_stable` is evaluated from the actual before/after temporal-state diff, not by copying the state.

## 5. Full-state diff and selectivity

For every event compute a structural state diff.

For OPEN_ORIGIN, permitted temporal changes are limited to:
- insertion/revelation of the declared origin claim;
- warrant value/state;
- live-alternative set if lawfully narrowed by origin evidence;
- provenance/evidence/transition ledgers.

Every pre-existing root temporal claim must retain:
- claim identity;
- role;
- interval;
- source file;
- source locator;
- status/uncertainty attributes.

A collateral temporal revision is any change to a pre-existing root temporal claim outside the declared event target.

`collateral_revision_count` is measured from this diff.

## 6. Source-bound alternative persistence

The oracle independently computes `required_live_claim_keys_after`.

A pre-origin root claim remains required after OPEN_ORIGIN when the warrant contract says the later evidence does not exclude it, especially a source-supported claim disjoint from the origin interval.

Runtime passes alternative persistence only if every required claim remains recoverable by the same source-bound key:
- role;
- interval;
- document identity;
- source locator/structural identity.

For INTERVAL/OPEN_INTERVAL without multiple live alternative claims, the runtime must preserve the explicit unresolved status and origin evidence basis.

Final warrant equality alone is insufficient.

## 7. Transition history and delayed audit

The runtime must append a transition ledger entry for OPEN_ORIGIN containing:
- event ID;
- target document;
- before warrant;
- after warrant;
- released evidence key;
- before/after state digests;
- changed state paths;
- collateral temporal paths.

The neutral maintenance event receives a separate event entry.

At delayed audit time:
- I_NATIVE/I_RSTAR must reconstruct the current warrant, origin evidence path, required live alternatives, and OPEN_ORIGIN transition from retained state/ledger;
- I_NO_HISTORY must discard the transition ledger before the delayed query;
- audit exactness is decided by comparing the reconstructed audit packet with the independent oracle audit packet.

No Boolean may be assigned solely from interface-arm identity.

## 8. Q0 and current-answer equivalence

Q0 remains edition-facing and independent of root research warrant.

Runtime Q0 is compared with an independently extracted oracle Q0.

All ablations must preserve the declared Q0 by construction or explicitly fail Q0.

## 9. Neutral event classifier

Neutral-event selection remains frozen conceptually, but oracle and runtime implementations must independently parse revisionDesc.

A selected neutral event must satisfy:
- maintenance-family positive classification;
- no date/dating/chronology/calendar/origDate/docDate lexical marker;
- no temporal target/reference if one is structurally encoded.

If the two implementations choose different neutral events or disagree on neutrality, the episode is CONTRACT_UNRESOLVED and cannot enter full trajectory.

## 10. Development source audit

Before holdout execution:

1. run rebuilt runtime/oracle on exposed Berlin and Paul corpora;
2. deterministically select at least 10 full-trajectory development episodes by SHA-256(path) order, spanning:
   - D1;
   - D2 where available;
   - exact post-origin warrant;
   - interval/open/alternative post-origin warrant;
   - at least one document with embedded annex in Paul if available;
3. emit for each:
   - root carriers;
   - primary document boundary signature;
   - origin evidence;
   - neutral event;
   - oracle/runtime question;
   - before/after warrant;
   - changed paths;
   - required live alternatives;
   - delayed audit packet.

The audit must be reviewable from source locators/snippets without trusting aggregate pass flags.

## 11. Fault-injection tests

Before holdout execution, development CI must prove the evaluator can detect at least these deliberately introduced failures:

F1 annex contamination: inject an annex date into runtime t0 claims -> oracle discovery mismatch or boundary violation detected.

F2 wrong origin binding: route OPEN_ORIGIN to another document/source locator -> provenance/applicability failure.

F3 wrong warrant: perturb runtime post-origin warrant -> warrant_exact failure.

F4 collateral mutation: modify an unaffected root claim during OPEN_ORIGIN -> collateral diff > 0.

F5 dropped live alternative: remove one oracle-required source-bound alternative -> persistence failure.

F6 fake null stability: make neutral event mutate temporal warrant -> null_event_stable failure.

F7 missing history: drop transition ledger -> delayed audit failure.

F8 wrong document boundary: select annex/second letter as primary -> independent parser boundary mismatch.

The test suite itself must not touch the frozen StaBi holdout.

## 12. Pre-holdout freeze requirements

No holdout execution until all are committed:

- rebuilt runtime file;
- independent oracle file;
- fault-injection test file;
- development source-audit generator;
- Berlin/Paul development outputs;
- hardening validation report;
- exact SHA-256 of runtime/oracle/test files;
- workflow that explicitly runs only exposed development prefixes.

Only after those hashes are frozen may a separate one-time StaBi holdout workflow be added.

## 13. Scientific status

Until the rebuilt evaluator is frozen:

    MODULE I = NOT YET EXECUTED AS CONFIRMATORY HOLDOUT

The existing Berlin/Paul development results are implementation diagnostics only.

Module H remains scientifically invalid for confirmatory use.

No claim about the full mother-problem gate is upgraded by this rebuild itself.