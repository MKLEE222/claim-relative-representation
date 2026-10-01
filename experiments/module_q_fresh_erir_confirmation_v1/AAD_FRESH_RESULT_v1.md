# Module Q — AAD fresh confirmatory result v1

Date: 2026-09-29
Status: BOUNDED_PARTIAL — authoritative one-shot fresh result.

## 1. Freshness and run identity

Fresh trigger commit:

    ebf58ed57b643ce9fe969bf67789e351ea4001e5

Authoritative workflow:

    module-q-aad-fresh-v1

Authoritative run:

    36526317608

Artifact:

    module-q-aad-fresh-v1
    artifact id = 11014393375
    artifact ZIP SHA-256 = 79081353b3712d725ec8f20f77e2b9b3c306463e71ab35e96457ea559bb08f4d

Pinned upstream:

    auden-in-austria-digital/aad-data
    34c3958686ab03614dedd8d979ffe94b6c0f2a28
    data/xml/editions/

Upstream archive SHA-256:

    73412badf8eca6dbffe9e7a17278db28949209179b5babc9a379f7b1a8fe3b40

AAD is exposed after this run and cannot be reused as fresh confirmation.

## 2. Population accounting

Frozen expected population:

    148 XML

Observed:

    parsed documents = 148
    parse errors = 0
    complete accounting = TRUE
    oracle/runtime contract unresolved = 0

Object contract:

    SINGLE_PRIMARY_DOCUMENT_OBJECT = 139
    NO_PRIMARY_DOCUMENT_OBJECT     = 9

Thus the run is not INVALID.

## 3. ERIR dispositions

Across all 148 documents:

    ERIR_ELIGIBLE          = 69
    ADMISSIBLE_NULL_EVENT  = 70
    INELIGIBLE             = 9

The 70 nulls are retained as nulls rather than folded into a positive denominator.

The 9 object-ineligible documents remain in the corpus accounting.

## 4. Transition-class distribution among 69 eligible episodes

    P-U1 CONFLICT_FORMATION              = 16
    P-U2 RESOLUTION_OR_ACQUISITION       = 30
    P-U3 NARROWING_OR_QUALIFICATION      = 23
    P-U4 ALTERNATIVE_REVISION            = 0
    OTHER                                = 0

This is a natural cross-project replication of three registered temporal update classes.

## 5. Activation-regime separation

For all 69 ERIR-eligible episodes:

    old Module-I D1/D2 eligible = 0
    old Module-I D1/D2 not eligible = 69

Thus every natural Module-Q episode in this corpus belongs to the evidence-release regime rather
than the earlier ambiguity-triggered regime.

Licensed interpretation:

    visible initial ambiguity
    !=
    later evidence capable of revising a scholarly state

This is a task/regime separation, not a prevalence claim beyond the frozen AAD population.

## 6. Reference interface

For all 69 eligible episodes:

    P1 CURRENT_STATE_BEFORE      69/69
    P2 EVENT_APPLICABILITY       69/69
    P3 POST_EVENT_RESULT         69/69
    P4 SELECTIVE_UPDATE          69/69
    P5 PROVENANCE                69/69
    P6 TRANSITION_ATTRIBUTION    69/69
    P7 DELAYED_HISTORY           69/69

Reference end-to-end:

    69/69

Therefore the primary retained-interface execution itself did not cause the bounded-partial
result.

## 7. Strong comparators

### RSTAR

    current state                    69/69
    current provenance               69/69
    exact state delta                69/69
    transition attribution           69/69
    delayed history                  69/69

### B_CURRENT_REOPEN

    current state                    69/69
    current provenance               69/69
    exact state delta                 0/69
    transition attribution            0/69
    delayed history                   0/69

### B_ORDERED_SNAPSHOTS

    current state                    69/69
    current provenance               69/69
    exact state delta                69/69
    transition attribution            0/69
    delayed history                   0/69

This fresh result reproduces the distinction:

    current state recovery
    !=
    exact state-delta recovery
    !=
    evidence-bound transition attribution
    !=
    delayed scholarly-history audit

The snapshot baseline remains strong for exact before/after state change.

## 8. Binding failure interventions

### Q1 wrong object

    rejected = 69/69
    root unchanged = 69/69

### Q2 wrong source version

    rejected = 69/69
    root unchanged = 69/69

### Q3 missing applicability

    rejected = 69/69
    root unchanged = 69/69

### Q5 no history

    post result preserved       69/69
    selectivity preserved       69/69
    provenance preserved        69/69
    transition attribution      69/69
    delayed history              0/69

These controls behave exactly as frozen.

## 9. Q4 collateral-mutation control and bounded-partial cause

The only failed aggregate confirmatory gate is Q4.

Observed:

    event applicable          = 69/69
    transition attribution    = 69/69
    collateral detected       = 39/69
    selectivity pass          = 30/69

The frozen confirmatory runner required every eligible episode to support a collateral-mutation
fault injection.

Post-run diagnostic, using the frozen artifact only and without rerunning AAD, shows exact
class separation:

    P-U1: 16/16
      Phi(before) = EXACT
      collateral mutation instantiated = yes
      collateral detected = yes
      selectivity failed = yes

    P-U2: 30/30
      Phi(before) = UNRESOLVED
      collateral mutation instantiated = no
      collateral detected = no
      selectivity remained pass = yes

    P-U3: 23/23
      Phi(before) = EXACT / INTERVAL / OPEN_INTERVAL
      collateral mutation instantiated = yes
      collateral detected = yes
      selectivity failed = yes

Hence:

    16 + 23 = 39

exactly accounts for all successful Q4 injections, while the 30 P-U2 episodes have no
pre-existing root state for the frozen collateral-root mutation to alter.

Scientific disposition:

    Q4 is a failure-injection applicability gap on P-U2,
    not a failure of the valid reference transition,
    not a source-audit failure,
    and not evidence that selectivity failed naturally.

Because the Q4 all-episode gate was frozen before opening AAD, the authoritative fresh result
remains BOUNDED_PARTIAL. It is not retrospectively upgraded to PASS.

## 10. Independent documentary audit

Frozen independent audit:

    audit_aad_fresh_sources.py

It reconstructs from raw XML, independently of Module-P warrant/eligibility helpers:
- object selection;
- root carriers;
- origin carrier;
- Phi(before);
- Phi(after);
- transition class;
- source file/version/provenance binding.

Observed:

    eligible manifest = 69
    audited = 69
    PASS = 69
    FAIL = 0
    missing = 0

Audit SHA-256:

    8ce64125b90429f9301b63dca61c85af7be55db1946ce131cdf1038ea1e87d2a

Thus the source-level natural interpretation of all 69 eligible transitions is independently
reconstructed under the frozen audit.

## 11. Authoritative final disposition

    BOUNDED_PARTIAL

Reason:

    all primary/reference/source-audit evidence passes,
    but one predeclared stress-test intervention is undefined/uninstantiable for the P-U2
    unresolved-root subclass under the frozen fault implementation.

This is materially stronger than a null, but it is not a clean confirmatory PASS under the
predeclared gate.

## 12. Licensed claim

At the AAD same-framework fresh-replication ceiling:

> In a second, prospectively opened digital-edition project, 69 source-audited document/evidence
> pairs instantiated evidence-release-induced scholarly revision under the frozen object and
> evidence contract. The retained interface recovered current state, applicability, post-event
> result, provenance, transition attribution and delayed history for all 69. Current reopening
> and ordered snapshots retained strong state-level capabilities but did not determine the
> evidence-bound transition history. The study remains bounded-partial because the predeclared
> collateral-mutation stress test was not applicable to the 30 unresolved-to-warranted cases.

## 13. Ceiling

Do not claim:
- cross-encoding confirmation;
- independent infrastructure confirmation;
- universal representational necessity;
- population prevalence outside the frozen AAD corpus;
- full confirmatory PASS;
- that current/latest or snapshots are generally poor representations.

AAD and AMP use closely related editorial/TEI frameworks.

The non-temporal Module-R line remains necessary for event-family generality.
