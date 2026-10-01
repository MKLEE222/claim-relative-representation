# Module J v1 — scholarly-object-bound discovery contract

Date frozen: 2026-09-28
Status: PRE-NEW-HOLDOUT CONTRACT. DEVELOPED ONLY FROM EXPOSED BERLIN, PAUL AND STABI FAILURES.

## 1. Motivation

Module H exposed a body-boundary failure: annex dates were incorrectly admitted to the primary letter.

Module I repaired that failure but the one-time StaBi holdout exposed a second boundary:
- 7 computational D1 candidates;
- all 7 had no transcription and no div type=letter;
- each file-level correspAction type=sent carried two dates spanning years/decades;
- the files represented extracts/copies/cuttings or correspondence bundles, not a single primary letter object.

Therefore XML-file identity and correspDesc identity are insufficient proxies for scholarly document identity.

## 2. Scholarly object identity

Before temporal comparison, the parser must identify exactly one primary scholarly letter object.

### Primary-object selection

Within the first body/transcription container:
1. enumerate direct child div type=letter objects not inside an annex;
2. if exactly one exists, select it;
3. if zero direct children, enumerate all descendant div type=letter objects without an annex ancestor;
4. if exactly one descendant exists, select it;
5. if zero, classify NO_PRIMARY_DOCUMENT_OBJECT;
6. if more than one eligible letter exists, classify MULTIPLE_PRIMARY_DOCUMENT_OBJECTS.

Do not choose the first among multiple eligible letters.

## 3. Object-bound claim identity

For an admissible primary object define:

    object_id = H(source file, source version, primary boundary signature)

Every temporal claim used in the same warrant state must carry this same object_id.

Claim identity includes at least:
- object_id;
- role;
- interval;
- source file;
- source locator contract;
- source/version contract.

## 4. Metadata applicability

File-level metadata is admitted to the primary-object state only when the file contains exactly one admissible primary object.

This applies to:
- msContents/docDate;
- correspAction type=sent dates;
- primary-letter dateline dates;
- canonical origin evidence.

If no unique primary object exists, these values may be reported as archival metadata but may not be compared as competing claims about one letter.

Multiple sent dates in one correspAction are not automatically contradictory.
They become comparable claims only after the single-object applicability gate passes.

## 5. Origin evidence

The Module I single-origDate contract is retained:
- one machine-readable origDate in the chosen canonical paragraph: admissible;
- zero: NO_ORIGIN_EVIDENCE;
- more than one: COMPOSITE_ORIGIN_UNRESOLVED.

The origin claim must share the same object_id as the root temporal claims.

## 6. Discovery eligibility

D1/D2 is evaluated only after:
1. SINGLE_PRIMARY_DOCUMENT_OBJECT;
2. all compared claims have identical non-null object_id;
3. runtime and independent oracle agree on object identity.

Aggregate archival metadata cannot by itself create a discovery episode.

## 7. Exposed-development validation requirements

Before any new fresh holdout:

### Berlin
- previously valid single-letter D1/D2 episodes should remain eligible where a unique object exists.

### Paul
- annex documents must remain excluded;
- primary letter and file-level metadata must bind to one object_id.

### StaBi
- the seven Module I aggregate candidates must be rejected as NO_PRIMARY_DOCUMENT_OBJECT or otherwise object-unresolved;
- they must not produce D1/D2 positive discovery episodes.

## 8. Additional fault tests

F10 aggregate metadata without a primary letter:
- two sent dates + no primary body must not produce discovery.

F11 multiple non-annex letter objects:
- file-level metadata must not be assigned to the first letter;
- object contract must report MULTIPLE_PRIMARY_DOCUMENT_OBJECTS.

F12 cross-object claim injection:
- inserting a claim with another object_id must fail discovery/evaluation or contract agreement.

## 9. Controlled null and state-transition rules

Module I's hardened rules remain:
- independent oracle/runtime implementations;
- controlled null event executed through transition operator;
- measured collateral diff;
- source-bound alternative persistence;
- actual ledger-based delayed audit;
- conservative composite-origin rejection.

## 10. Consequence for the mother problem

This contract makes explicit that representational sufficiency is not only value/binding/provenance relative.

It is also scholarly-object relative:

    the system must know which epistemic claims belong to the same research object

before disagreement, uncertainty, correction or warrant composition is meaningful.

## 11. Anti-rescue rule

StaBi is exposed and cannot be rerun as confirmatory evidence.

A new holdout must be selected without opening its bodies and must use this object contract unchanged.

If a new corpus has insufficient uniquely bounded objects or insufficient full trajectories, the holdout fails.