# Module M — genuine DH comparator exposed result v1

Date: 2026-09-29
Status: COMPLETED EXPOSED DEVELOPMENT STUDY. RESULT = EXPOSED_HISTORY_SEPARATION.

## 1. Scientific purpose

Module M tests a Digital Humanities distinction:

    current-state recoverability
    !=
    scholarly-history recoverability

It does not test a generic representation leaderboard and it does not provide fresh
independent confirmation.

The preregistered comparators are deliberately strong positive baselines:

- B_CURRENT_REOPEN:
  lawfully reopen the current/latest source and reconstruct the terminal warranted state.

- B_ORDERED_SNAPSHOTS:
  retain ordered complete temporal state snapshots and exact adjacent-state diffs, but no
  explicit transition semantics or event-to-evidence authorization record.

The comparator contract was frozen before implementation/results in:

    868a9363294ed9322e3d3166f8263828c66bdc79

## 2. Transparent implementation correction

The first Module-M workflow run:

    36510203486
    head 141c4bfd6fc485b548ddf0c5825c15d7504241c0

failed the synthetic positive gate.

Cause:
the implementation of T2 provenance exactness additionally required parser-specific
source_locator_xpath equality.

The frozen comparator contract did not require XPath equality. T2 had been frozen as:
- claim key;
- source file;
- source locator contract;
- object identity / applicability proof.

The extra XPath equality therefore made the baseline stricter than preregistered.

The correction removed only that extra implementation requirement:
- comparator information budgets were unchanged;
- T1-T5 definitions were unchanged;
- transition/history information was not added to either comparator;
- no exposed comparator result had been produced because the gate failed before the exposed job.

Correction commits:

    29ebd57cb077b4c941d4a9da97eeb3aa6eb0bf12
    f7ad4fcee05bd28b72cc5c0ac62041e229af1c9e

## 3. Successful preregistered workflow

Workflow:

    module-m-dh-comparators-v1

Successful run:

    36510243720

Comparator-result head:

    f7ad4fcee05bd28b72cc5c0ac62041e229af1c9e

Artifact:

    ID 11008213501
    module-m-dh-comparators-v1

Artifact ZIP digest:

    sha256:7bd5f821f79da7926a285fc191f0faefa906939930def7962f2362a4abe95b42

The workflow first reran:
- portable F17-F30 controls;
- inherited I/J obligations on the portable engine;
- the Module-M synthetic positive/indistinguishability gate.

All passed before the exposed corpus study was executed.

## 4. Synthetic non-strawman gate

### B_CURRENT_REOPEN

Passed:
- T1 CURRENT_STATE;
- T2 CURRENT_PROVENANCE.

Did not determine:
- T3 STATE_DELTA;
- T4 TRANSITION_ATTRIBUTION;
- T5 DELAYED_HISTORY_AUDIT.

This is the registered capability boundary.

### B_ORDERED_SNAPSHOTS

Passed:
- T1 CURRENT_STATE;
- T2 CURRENT_PROVENANCE;
- T3 STATE_DELTA.

Did not determine:
- T4 TRANSITION_ATTRIBUTION;
- T5 DELAYED_HISTORY_AUDIT.

This is the registered capability boundary.

### RSTAR

Passed T1-T5 on the synthetic positive control.

### Indistinguishability witness

The preregistered histories H_A and H_B differ in event semantics, but:
- CURRENT_REOPEN information projection is identical;
- ORDERED_SNAPSHOTS information projection is identical.

Thus the T4/T5 separation is not created solely by an evaluator refusing to credit a visible
state difference. Distinct registered histories are observationally equivalent under the
comparator information regimes.

## 5. Exposed Berlin result

Eligible full trajectories:

    N = 29

RSTAR:

    T1 = 29/29
    T2 = 29/29
    T3 = 29/29
    T4 = 29/29
    T5 = 29/29

B_CURRENT_REOPEN:

    T1 = 29/29
    T2 = 29/29
    T3 = 0/29
    T4 = 0/29
    T5 = 0/29

B_ORDERED_SNAPSHOTS:

    T1 = 29/29
    T2 = 29/29
    T3 = 29/29
    T4 = 0/29
    T5 = 0/29

Disposition:

    EXPOSED_HISTORY_SEPARATION

## 6. Exposed Paul result

Eligible full trajectories:

    N = 33

RSTAR:

    T1 = 33/33
    T2 = 33/33
    T3 = 33/33
    T4 = 33/33
    T5 = 33/33

B_CURRENT_REOPEN:

    T1 = 33/33
    T2 = 33/33
    T3 = 0/33
    T4 = 0/33
    T5 = 0/33

B_ORDERED_SNAPSHOTS:

    T1 = 33/33
    T2 = 33/33
    T3 = 33/33
    T4 = 0/33
    T5 = 0/33

Disposition:

    EXPOSED_HISTORY_SEPARATION

## 7. StaBi

Eligible full trajectories:

    N = 0

Disposition:

    NO_ELIGIBLE_EXPOSED_EPISODES

StaBi is not included in any performance denominator.

## 8. Combined exposed capability pattern

Across Berlin + Paul:

    N = 62

RSTAR:

    T1 = 62/62
    T2 = 62/62
    T3 = 62/62
    T4 = 62/62
    T5 = 62/62

B_CURRENT_REOPEN:

    T1 = 62/62
    T2 = 62/62
    T3 = 0/62
    T4 = 0/62
    T5 = 0/62

B_ORDERED_SNAPSHOTS:

    T1 = 62/62
    T2 = 62/62
    T3 = 62/62
    T4 = 0/62
    T5 = 0/62

The strong result is not that the comparators are generally weak.

They recover exactly the capabilities they were granted:
- current/latest-source reopening recovers current state and provenance;
- ordered snapshots additionally recover exact state differences.

The observed separation begins only when the registered task asks for:
- authorized transition attribution;
- delayed scholarly-history audit.

## 9. DH interpretation

The exposed result supports the bounded distinction:

    knowing what the current scholarly state is
    !=
    knowing how that state became warranted

and, more strongly:

    knowing the complete ordered states and their exact differences
    !=
    determining the scholarly transition semantics that licensed the change.

For the registered task, a state diff identifies what changed.
It does not by itself determine whether the change was:
- an authorized evidence release;
- an import;
- a repair;
- a migration;
- another operation yielding the same adjacent states.

That historical distinction requires information not present in the frozen snapshot comparator.

## 10. Claim ceiling

Module M is exposed development evidence.

It licenses:
- a non-strawman comparator result on Berlin/Paul;
- an information-regime non-identifiability witness;
- development support for separating current-state/state-delta recoverability from
  transition-history recoverability.

It does not license:
- unseen-corpus superiority;
- universal necessity of a transition ledger for every scholarly task;
- a claim that ordinary version control cannot contain useful semantic history;
- a fresh independent dynamic confirmation.

The next empirical burden remains:
1. obligation-level non-substitutability (Module N);
2. fresh independent eligible trajectory;
3. a second non-temporal DH event family.
