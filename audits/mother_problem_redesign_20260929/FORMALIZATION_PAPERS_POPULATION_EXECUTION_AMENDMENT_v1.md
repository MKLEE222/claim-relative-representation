# Formalization Papers population and execution amendment v1

Date: 2026-09-30
Status: PRE_DATA / PRE_RECORD / FROZEN BEFORE AUTHORITATIVE POPULATION OPENING.

## 1. Purpose

This amendment closes implementation choices that must not be decided after the Formalization
Papers record population is opened.

It does not change the scientific question or T0-T9 taxonomy.

## 2. Authoritative data source

The sole authoritative fresh source for the first one-shot execution is:

    LaraHack/formalization_papers_supplemental
    commit 2f68d8498aeeb724e3438deda13e74ae7fb076d8
    release tag v1.0

The workflow will download the immutable GitHub source archive for that commit only after the
DATA_OPEN_EVENT has been emitted.

Primary record directory:

    nanopubs/

The published nanopublication index is NOT a fallback during the authoritative fresh run.

If the frozen v1.0 snapshot is incomplete or cannot support complete population accounting, the
fresh outcome is INVALID_SOURCE_SCOPE / INVALID rather than an index-assisted rescue.

The index may be used only later as exposed diagnostic material.

## 3. Record-file inclusion rule

After DATA_OPEN, recursively enumerate every regular file under the frozen snapshot's nanopubs/
directory.

Do not select by filename or candidate ID.

Every regular file is attempted as TriG by both registered RDF engines.

If any file cannot be parsed by either engine, preserve the failure and classify the run INVALID.

No malformed file is silently skipped.

## 4. Surface aggregation

Each file is independently parsed by:

    RDFLib oracle
    pyoxigraph runtime

The per-file registered surfaces are unioned setwise over:
- roots;
- reviews;
- updates;
- responses;
- decisions;
- supersedes;
- retracts;
- creators;
- created timestamps.

Exact equality of the aggregate registered surface is mandatory.

Parser-local graph ordering is irrelevant.

## 5. Live nanopublication canonicalization

Version/retraction maintenance is resolved before trajectory construction.

For a nanopublication package n:

- if a non-retracted live package directly or transitively supersedes n, n is retained in history
  but is not the live act version;
- if n is retracted, n is retained in history but is not live;
- a unique terminal non-retracted superseding version is the live version.

The following are T8/invalid-for-trajectory ambiguities for any affected root:
- supersession cycle;
- more than one incomparable live terminal superseder for the same act;
- retraction/supersession target needed by a trajectory cannot be resolved.

No older version is revived merely because the latest version is inconvenient.

## 6. Root denominator

Population roots are all unique submitted-formalization objects discovered by the frozen R1 root
grammar in the full record scope.

The graph-derived denominator is authoritative.

The documented expectation of approximately 15 submissions is reported only as a consistency
check.

Every graph-derived root receives exactly one T0-T9 disposition.

## 7. Connected trajectory enumeration

For each root, enumerate ALL live connected chains.

A T1 chain is the exact tuple:

    (root, review_np, update_np, response_np)

such that:
- the live review has exactly one target and that target is root;
- the live update has exactly one isUpdateOf target and that target is root;
- the live response has exactly one isResponseTo target equal to review_np;
- the live response has exactly one refersTo target equal to update_np.

A T0 chain extends a T1 chain with every live decision nanopublication whose exact status target is
update_np.

Do not choose one favorable chain when multiple connected chains exist.

Primary tests execute on every enumerated T0/T1 chain in every T0/T1 root.

## 8. Chronology rule

Relation-target edges encode prerequisite existence.

Therefore the required partial order is:

    review  < response
    update  < response
    update  < decision

A direct chronological order between review and update is not required unless the source encodes
one, because both can independently precede the response.

If retained timestamps exist for both endpoints of a required dependency and contradict the
dependency, classify the affected root T8.

If timestamps are absent but the exact project-native target relation establishes the dependency,
do not invent an additional date.

If two acts require an order not supplied by target dependency and the order is scientifically
needed for qualification, classify T8 rather than guess.

## 9. Root classification

After ambiguity checks and connected-chain enumeration, apply the already frozen priority:

    T9 > T8 > T0 > T1 > T2 > T5 > T4 > T3 > T7 > T6

Operational definitions:

- T0: at least one complete connected T0 chain;
- T1: no T0 chain, at least one connected T1 chain;
- T2: live review(s) and live update(s), but no connected response chain;
- T5: live decision targeting a live update, but no connected response chain and T2 did not apply;
- T4: live update(s), no live review connected to root;
- T3: live review(s), no live update;
- T7: no scholarly review/update/response/decision trajectory, but supersession/retraction
  maintenance affects the root/acts;
- T6: root only;
- T8: ambiguous/nonfunctional required target/version/chronology;
- T9: safely parsed graph cannot satisfy the frozen contract for that root.

## 10. Primary execution

For each connected T0/T1 chain:

1. initialize the root state;
2. execute REVIEW;
3. execute UPDATE;
4. execute RESPONSE;
5. for T0, execute DECISION.

The registered generator surface remains:

    RECORD_REVIEW
    REPLACE_FORMALIZATION
    RECORD_RESPONSE
    REVISE_PUBLICATION_STATUS

No generator label is read from provider filenames or records.

## 11. Counterfactual execution

For every T0/T1 chain, run all applicable frozen tests:

- response before review;
- response after review but before update;
- same-current-update history ablation;
- wrong-review target using a valid foreign-root review when one exists;
- wrong-update target using a valid foreign-root update when one exists;
- T0 decision before update;
- retraction/supersession discipline.

If the full population contains no valid foreign-root act of the needed type, mark the
corresponding wrong-target injection STRUCTURALLY_UNAVAILABLE rather than fabricate a provider
record.

This alone does not fail PASS if all other registered criteria are testable; it is reported as a
bounded unavailable control.

## 12. Result preservation

The fresh result must retain:
- source archive SHA-256;
- all record relative paths and per-file SHA-256 values;
- total record file count;
- parse-error accounting;
- exact aggregate oracle/runtime surface hash;
- graph-derived root count;
- T0-T9 counts;
- every root disposition;
- every T0/T1 connected chain;
- every forward generator sequence;
- every counterfactual result;
- history-ablation result;
- final PASS/NULL/BOUNDED_PARTIAL/INVALID disposition.

## 13. Documentary audit

After the main result is frozen, a separate audit implementation must re-query raw TriG without
importing the main extractor or population classifier.

For every T0/T1 chain it independently verifies the exact raw relations:
- root special-issue + submitted status;
- review type and review -> root target;
- update -> root target;
- response -> review target;
- response -> update target;
- decision -> update/status for T0;
- creator/time fields when present;
- supersession/retraction status of every chain act.

Any documentary mismatch makes the authoritative run INVALID.

## 14. DATA_OPEN boundary

Immediately before archive download, the workflow writes DATA_OPEN_EVENT.json containing:
- GITHUB_SHA;
- source repository;
- frozen source commit/tag;
- UTC event time;
- SHA-256 hashes of scientific engine/classifier/auditor files;
- protocol/amendment Git blob identities.

Only after that file exists may the source archive be downloaded.

The first archive download consumes candidate record freshness.

## 15. No rescue rule

After DATA_OPEN:
- do not alter T0-T9 definitions;
- do not alter relation adapter;
- do not alter denominator;
- do not add a project-specific relation;
- do not drop negative/ambiguous roots;
- do not switch to the nanopublication index to obtain a better result.

Implementation defects discovered after DATA_OPEN may be corrected only under an explicit
INVALID/corrected-reproduction discipline; they cannot restore literal freshness.
