# Module Q — AAD exposed audit result v1

Date: 2026-09-29
Status: EXPOSED AUDIT AFTER INVALID FRESH ATTEMPT.

## 1. Fresh-attempt status

The frozen AAD fresh workflow:

    36531128233

was INVALID because the moved runner could not import oracle_p.

The failure occurred before archive acquisition.

Nevertheless the trigger marker had explicitly declared AAD freshness consumed, and that decision
is not reversed post hoc.

AAD is therefore permanently excluded from future fresh-confirmatory use in this project.

## 2. Corrected exposed population audit

Authoritative exposed audit:

    36531278014

Pinned upstream:

    auden-in-austria-digital/aad-data
    34c3958686ab03614dedd8d979ffe94b6c0f2a28

Population:

    expected XML              148
    parsed                    148
    parse errors                0
    complete accounting       yes

Object contract:

    SINGLE_PRIMARY_DOCUMENT_OBJECT  139
    NO_PRIMARY_DOCUMENT_OBJECT        9

Module-P disposition:

    ERIR_ELIGIBLE              69
    ADMISSIBLE_NULL_EVENT      70
    INELIGIBLE                  9

Transition classes among eligible:

    P-U1 CONFLICT_FORMATION                16
    P-U2 RESOLUTION_OR_ACQUISITION         30
    P-U3 NARROWING_OR_QUALIFICATION        23

Oracle/runtime unresolved:

    0

Result JSON SHA-256:

    d6a248b0d227a8878587e865a945af7feec608ac18441a9f9181a5ea1b9484cd

## 3. Reference capability result

All 69 ERIR-eligible exposed episodes pass:

    P1 CURRENT_STATE_BEFORE          69/69
    P2 EVENT_APPLICABILITY           69/69
    P3 POST_EVENT_RESULT             69/69
    P4 SELECTIVE_UPDATE              69/69
    P5 PROVENANCE                    69/69
    P6 TRANSITION_ATTRIBUTION        69/69
    P7 DELAYED_HISTORY               69/69
    reference end-to-end             69/69

This is exposed execution evidence only.

## 4. Strong comparator separation

RSTAR:

    current state                     69/69
    current provenance                69/69
    state delta                       69/69
    transition attribution            69/69
    delayed history                   69/69

B_CURRENT_REOPEN:

    current state                     69/69
    current provenance                69/69
    state delta                        0/69
    transition attribution             0/69
    delayed history                    0/69

B_ORDERED_SNAPSHOTS:

    current state                     69/69
    current provenance                69/69
    state delta                       69/69
    transition attribution             0/69
    delayed history                    0/69

Thus the exposed AAD result preserves the already observed separation:

    current state
    !=
    exact state delta
    !=
    evidence-grounded transition/history.

## 5. Failure interventions

Wrong-object, wrong-source-version and missing-applicability interventions:

    rejected 69/69
    root unchanged 69/69

No-history intervention:

    post result          69/69
    selectivity          69/69
    provenance           69/69
    transition binding   69/69
    delayed history       0/69

Collateral-mutation intervention:

    event applicable     69/69
    collateral detected  39/69
    selectivity passes   30/69

The last result is not interpreted as a 30/69 weakness of the reference interface.
The injected collateral fault only produces a detectable task-external temporal mutation in the
39 episodes for which the fixture exposes such an additional temporal path.

## 6. Documentary carrier audit

Post-exposure documentary audit workflow:

    36531414488

The population result reproduced exactly before the source audit.

Eligible manifest:

    69

Audited:

    69

Independent audit PASS:

    46

Not independently classified by this audit:

    23

The 46 independently classified episodes are exactly:

    16 x P-U1 CONFLICT_FORMATION
    30 x P-U2 RESOLUTION_OR_ACQUISITION

The remaining 23 are exactly the P-U3 NARROWING_OR_QUALIFICATION cases.

## 7. Why the documentary audit did not pass 69/69

The documentary audit was adapted from the earlier AMP audit.

Its independent classifier contains explicit carrier-level rules only for:

### P-U1

One active root carrier plus one machine origin carrier whose intervals are disjoint.

### P-U2

No active root carrier plus one machine origin carrier.

For every other expected class it deliberately returns:

    OTHER_NOT_INDEPENDENTLY_CLASSIFIED

Therefore all 23 P-U3 cases fail only:

    transition_class_exact

because P-U3 has no independent audit rule in the frozen audit instrument.

This is an audit-instrument coverage gap.

It is not evidence that the 23 documents lack the recorded carriers.

## 8. Scientific interpretation

The strongest currently licensed AAD statement is:

> In an exposed second project using a closely related digital-edition framework, the frozen
> portable object/claim engine finds 69 task-level temporal evidence-release transitions among
> 148 documents, with 70 admissible nulls and 9 object-ineligible documents. All 69 executable
> transitions satisfy the retained P1-P7 capability contract. An independent post-exposure
> carrier audit directly verifies the 16 conflict-formation and 30 acquisition/resolution cases;
> the 23 narrowing/qualification cases remain outside that audit instrument's registered
> classification coverage.

This is stronger than the AMP-only development result but weaker than fresh independent
confirmation.

## 9. What is not licensed

Do not claim:
- AAD is fresh confirmation;
- AAD is an independent encoding ecology;
- 69/69 are independently source-audited;
- the 23 P-U3 cases failed scientifically;
- the 69/148 fraction is prevalence beyond this closed AAD population.

## 10. Consequence for Module Q

Module Q fresh-confirmatory burden remains:

    OPEN

The next candidate should prioritize:
1. independent project/schema ecology;
2. project-level proof of distinct current-state and later-evidence carriers;
3. stable object identity;
4. deterministic closed population;
5. synthetic compatibility before opening;
6. full population one-shot with no post-opening rescue.

AAD now functions only as exposed design/development evidence.
