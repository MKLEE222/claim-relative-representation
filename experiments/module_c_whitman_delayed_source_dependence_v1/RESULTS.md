# Module C results — delayed source-route dependence under Whitman repository evolution

Date: 2026-09-28
Status: EXECUTED NATURAL VERSIONED DEVELOPMENT STRESS TEST. NOT INDEPENDENT TRANSFER.

Authoritative execution:
- GitHub Actions run 36375819427
- artifact: module-c-whitman-delayed-source-dependence-v1
- artifact ID: 10950857531
- artifact ZIP SHA-256: 20455f47fb660fb7b70ebdba45269f30563c84b06e946122eb2fe7ad4ba7e8e1
- results SHA-256: 6843141afbce3ff28067019533809bef6eff615ef58993fbea43e0d8d0869a38

## 1. Question

Hold the scholarly relation representation fixed and vary only the source repositories into which its endpoint identifiers must resolve.

Question:

> Can a relation representation preserve exactly the same endpoint strings while its ability to execute later source inspection changes as independently versioned source repositories evolve?

This tests delayed dependence naturally rather than by deleting fields from the relation object.

It is a GitHub-source snapshot audit, not a test of the deployed Whitman Archive service.

## 2. Fixed relation state

The relation inventory is frozen at:

Repository:
whitmanarchive/whitman-LG_1855_variorum

Commit:
25a00b7ebbdbc5246fce65a333bc761a5c22dad4

File:
source/authority/anc.02134.xml

Population:
- 1,444 valid relation links
- current endpoint strings held fixed by construction

Printed-side source is also held fixed at the same variorum commit.

Therefore any route change below occurs in source executability, not in the relation strings themselves.

## 3. Source environments

### E2019

Manuscripts:
- commit 249bc14594fa1c0428e7ca39f52753de21ce604b
- tree 1871715fbcef5f9721e80f385471a86ad52ef463

Notebooks:
- commit 682c04c0998739b8edfd75e0e7496592777e2898
- tree 90ce5a76b2358d3350e889b6988af8e26bcdd835

### ECURRENT

Manuscripts:
- commit 2fe2c934f0b63ce66d4e43f36798767785f2b70c
- tree 6a0372f5d3e111226f6a96bedaa8724ef18c5854

Notebooks:
- commit a7b000f613e4c4fcf38cec4d58aebd6c857ffe37
- tree b1c6b7d631c04fae49939f24cadd66eba697b6cc

No fuzzy ID matching, alias map or later rescue rule was introduced after outcome.

## 4. Natural route trajectories

Across 1,444 fixed links:

- STABLE_RESOLVED: 777
- REPAIRED_OVER_TIME: 660
- STABLE_UNRESOLVED: 7
- BROKEN_OVER_TIME: 0

Reason transitions:

- RESOLVED -> RESOLVED: 777
- MISSING_LOCAL_ID -> RESOLVED: 641
- MISSING_FILE -> RESOLVED: 19
- MISSING_LOCAL_ID -> MISSING_LOCAL_ID: 5
- MISSING_FILE -> MISSING_FILE: 2

Distinct source files participating:
- stable resolved links: 120 files
- repaired-over-time links: 52 files
- stable unresolved links: 2 files

The observed temporal pattern is overwhelmingly improvement, not decay.

## 5. Low-certainty continuation

Module B2's uncertainty-sensitive continuation selects low-certainty endpoints for additional source inspection.

Among 936 low-certainty links:

E2019:
- source route resolves: 482

ECURRENT:
- source route resolves: 930

Trajectory:
- stable resolved: 482
- repaired over time: 448
- broken over time: 0
- stable unresolved: 6

Thus the same fixed uncertainty-sensitive continuation target becomes far more executable in the later source environment without any change to the relation strings.

## 6. High-certainty comparator

Among 508 high-certainty links:

E2019:
- resolved: 295

ECURRENT:
- resolved: 507

Trajectory:
- stable resolved: 295
- repaired over time: 212
- broken over time: 0
- stable unresolved: 1

The effect is therefore not specific to low-certainty links; source-route maturation improves both strata.

## 7. File-level motion

Across 151 referenced source filenames:

- FILE_STABLE_PRESENT: 142
- FILE_ADDED_OR_ROUTED: 8
- FILE_STABLE_UNRESOLVED: 1
- FILE_REMOVED_OR_AMBIGUOUS: 0

The larger link-level improvement is mainly due to local xml:id availability becoming compatible with the fixed relation identifiers, not merely new filenames appearing.

## 8. Scientific interpretation

Observed:

    endpoint strings remain fixed
    while
    source-route executability changes over repository versions

Therefore, for this versioned source ecology:

    stable relation representation
    != stable executable source access

This is the delayed-dependence phenomenon needed by Module C.

However, the direction matters:

    executability improved over time

The result must NOT be narrated as representational decay, link rot, or archival failure.

Instead, it shows that a currently sufficient symbolic reference can have time-varying operational research value because its downstream source environment is independently versioned.

## 9. Scientific disposition

ENDPOINT_STRINGS_STABLE = YES

SOURCE_ROUTE_EXECUTABILITY_CHANGED = YES

LOW_CERTAINTY_CONTINUATION_CHANGED = YES

NATURAL_VERSION_DRIFT_OBSERVED = YES

BROKEN_OVER_TIME = 0

DEPLOYED_ARCHIVE_FAILURE = NOT TESTED / NOT CLAIMED

INDEPENDENT_TRANSFER = NOT TESTED

SELECTIVE_BELIEF_REVISION = NOT TESTED

## 10. Claim ceiling

Supported as development evidence:

> A fixed scholarly relation representation can preserve its endpoint strings while its source-following continuation capacity changes across independently versioned source repositories. In the tested Whitman snapshots, the change is strongly positive: 660 previously unresolved routes become executable and none of the previously executable routes becomes unresolved.

Not supported:
- repository evolution necessarily degrades researchability;
- the deployed archive experienced the same route states;
- fixed endpoint strings are globally insufficient;
- this version trajectory generalizes beyond the tested source ecology.

## 11. Consequence for the mother problem

Module C adds a time-dependent obligation that is absent from one-shot query recovery:

A representation's future research utility depends not only on what identifiers it stores, but also on whether those identifiers remain executable against the source environment available when a later inquiry is performed.

This does not yet solve sustained warranted discovery. It establishes a natural delayed-dependence phenomenon that a stronger sufficiency theory must account for.
