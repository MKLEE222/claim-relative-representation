# Module P — AMP exposed development protocol v1

Date frozen: 2026-09-29
Status: PRE-RUN EXPOSED DEVELOPMENT PROTOCOL.

## 1. Data status

AMP is already exposed through authoritative Module O and the subsequent trigger diagnostic.

Therefore this study provides development evidence only.

It must never be described as fresh, holdout, confirmatory or prevalence evidence.

Frozen AMP source:

    Auden-Musulin-Papers/amp-data
    commit 289a52de61aef0b6354e3c8298173bf1f889feb2
    population data/editions/*.xml
    expected N = 73

## 2. Purpose

Test whether the independently hardened Module-P evidence-release-induced revision mechanism
matches the already exposed AMP ecology.

Primary questions:

1. Do oracle/runtime independently agree on ERIR eligibility and transition class?
2. How many AMP objects are:
   - INELIGIBLE;
   - ADMISSIBLE_NULL_EVENT;
   - ERIR_ELIGIBLE?
3. Which P-U1/P-U2/P-U3/P-U4/OTHER transition classes occur?
4. Do retained P1-P7 capabilities hold on every ERIR-eligible AMP episode?
5. Do strong Module-M comparators retain their positive current-state/state-delta capabilities?
6. Do preregistered failure interventions produce the expected capability separations?

## 3. Population accounting

All 73 XML files are included.

For every file record:
- path;
- parse success/error;
- object status;
- source context;
- oracle/runtime P disposition;
- oracle/runtime transition class;
- oracle/runtime Phi before/after agreement.

Required accounting:

    parsed + parse_errors = 73

No subset may be selected by outcome.

## 4. Primary development denominator

The primary Module-P mechanism denominator is:

    all files where oracle and runtime agree:
        p_disposition == ERIR_ELIGIBLE

Any oracle/runtime P-contract mismatch is reported separately and invalidates mechanism
interpretation for that episode.

ADMISSIBLE_NULL_EVENT is a scientific null category, not a failure.

INELIGIBLE is an applicability category, not a failure.

## 5. Primary capability gate

For every contract-resolved ERIR-eligible episode, retained execution is evaluated on:

    P1 CURRENT_STATE_BEFORE
    P2 EVENT_APPLICABILITY
    P3 POST_EVENT_RESULT
    P4 SELECTIVE_UPDATE
    P5 PROVENANCE
    P6 TRANSITION_ATTRIBUTION
    P7 DELAYED_HISTORY

Report each capability separately and the count satisfying all P1-P7.

No scalar representation score is computed.

## 6. Regime-separation check

For every ERIR-eligible AMP episode, report the inherited Module-I/L D1/D2 eligibility flag.

The strongest evidence that Module P adds a distinct task is:

    ERIR eligible
    AND
    old D1/D2 not eligible

Do not require this pattern by construction; report what is observed.

## 7. Strong comparator evaluation

Reuse frozen Module-M comparators unchanged.

For every ERIR-eligible episode:

B_CURRENT_REOPEN:
- T1 current state;
- T2 current provenance.

B_ORDERED_SNAPSHOTS:
- T1 current state;
- T2 current provenance;
- T3 exact state delta.

Also record T4/T5 exactly as observed.

RSTAR/retained Module-P execution is projected onto the same T1-T5 surface.

If a comparator unexpectedly recovers T4/T5, retain the result and weaken the history claim.

## 8. Registered failure interventions

On every ERIR-eligible episode, run:

### Q1 WRONG_OBJECT
Expected:
- event rejected;
- post-event warrant remains root warrant.

### Q2 WRONG_SOURCE_VERSION
Expected:
- event rejected;
- post-event warrant remains root warrant.

### Q3 MISSING_APPLICABILITY
Expected:
- event rejected;
- post-event warrant remains root warrant.

### Q4 COLLATERAL_MUTATION
Expected:
- event accepted;
- P4 SELECTIVE_UPDATE fails;
- transition attribution remains available.

### Q5 NO_HISTORY
Expected:
- P3 POST_EVENT_RESULT remains correct;
- P4 SELECTIVE_UPDATE remains correct;
- P5 PROVENANCE remains available;
- P6 TRANSITION_ATTRIBUTION remains available in immediate trace;
- P7 DELAYED_HISTORY fails.

The study reports these as capability patterns, not overall scores.

## 9. Transition-class counts

Report separately:

    P-U1 CONFLICT_FORMATION
    P-U2 RESOLUTION_OR_ACQUISITION
    P-U3 NARROWING_OR_QUALIFICATION
    P-U4 ALTERNATIVE_REVISION
    OTHER
    ADMISSIBLE_NULL_EVENT
    INELIGIBLE

Unexpected OTHER transitions are retained and described; the contract is not changed post hoc.

## 10. Documentary source audit

Because AMP is exposed development data, audit all ERIR-eligible episodes rather than sampling.

The audit must independently inspect the raw XML and record:

- one valid selected scholarly object under the frozen object grammar;
- root carrier(s) actually present in the declared source locations;
- one later origDate carrier in the declared origin/history location;
- raw temporal attributes;
- whether root vs later evidence is substantively:
  - disjoint/conflict-forming;
  - unresolved-to-warranted;
  - another registered class;
- absence of envelope/enclosure/embedded contamination in active claims;
- source/object/applicability binding consistency.

The audit may invalidate individual development episodes.
It cannot change Module O or make Module P fresh.

## 11. Development interpretation ceiling

A successful exposed AMP result supports:

- naturalistic development evidence that Regime B exists in a real independent DH edition;
- transfer of the frozen object/applicability/provenance/history mechanism to a second activation
  regime.

It does not support:
- prospective generalization;
- event-family generality beyond temporal dating;
- prevalence;
- universal necessity.

Fresh Regime-B confirmation remains required afterward.
