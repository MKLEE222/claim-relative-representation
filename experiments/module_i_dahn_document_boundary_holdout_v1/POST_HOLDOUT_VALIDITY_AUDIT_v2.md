# Module I post-holdout semantic validity audit v2

Date: 2026-09-28
Status: POST-HOLDOUT VALIDITY AUDIT. NO RERUN AUTHORIZED.

## 1. Frozen execution

One-time prospective StaBi holdout:
- workflow run 36417611131
- workflow commit 439422bf48e49a45ca53ccf1fbf3a8b84f67a0bb
- frozen evaluator hashes verified successfully before source access
- 465 documents parsed
- 0 parse errors
- 7 oracle primary-discovery candidates
- 0 full trajectories
- Module I mother-problem gate: FALSE
- result SHA-256: f504c021c74918147df87f6e50a2f9ae7100e4869a50ab377a39f39c4d3df1dd
- source-audit SHA-256: 37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570
- artifact ID: 10967212367
- artifact ZIP digest: 5c76d822759b0ff7b91214e37c0af21e7a55d5d058128eeeeb4e1aac7e5a0b10

The holdout is not rerun after this audit.

## 2. Immediate frozen result

All seven primary candidates failed FULL_TRAJECTORY before any R* episode was executed because:
- NO_ORIGIN_EVIDENCE: 7/7
- NO_WARRANT_STATE_CHANGE: 7/7

Therefore:
- I_RSTAR evaluated full episodes: 0
- I_NATIVE evaluated full episodes: 0
- end-to-end confirmation: NOT ESTABLISHED
- mother-problem Module I gate: FAILED.

This is already a strict negative result, not a positive result to rescue.

## 3. Post-holdout source-object audit of all seven primary candidates

Every one of the seven source files was opened after the frozen execution.

Files:
- AuszugeBriefwechselBoeckhundseinemBruderFriedrich.xml
- BriefabschriftenKarlFriedrichHermannanBoeckh.xml
- BriefabschriftenKarlJosephHieronymusWindischmannanBoeckh.xml
- BriefausschnitteAugustBoeckhanDavidSchulz.xml
- BriefauszugeBoeckhanOscarvonSarwey.xml
- BriefauszugeCarlRichardLepsiusanBoeckh.xml
- BriefauszugeHermannKochlyanBoeckh.xml

Common structure in all 7:
- no transcription div;
- no div type=letter;
- no selected primary letter body;
- one correspDesc;
- one sent correspAction containing two different dates separated by years/decades;
- file titles identify extracts/copies/cuttings or correspondence bundles rather than a single letter.

Examples:
- Boeckh/Friedrich: sent dates 1832-01-01 and 1849-01-01;
- Hermann/Boeckh: 1836-01-01 and 1857-01-01;
- Windischmann/Boeckh: 1808-01-01 and 1834-01-01;
- Boeckh/Schulz: 1806-01-01 and 1841-01-01;
- Boeckh/Sarwey: 1854-01-01 and 1866-01-01;
- Lepsius/Boeckh: 1837-01-01 and 1863-01-01;
- Kochly/Boeckh: 1852-01-01 and 1863-01-01.

## 4. Validity finding

The frozen oracle treated multiple sent dates inside one file-level correspAction as multiple current-document temporal claims.

For these seven files, the source object is not an individually selected primary letter.

Therefore the D1 relation:

    sent_date_1 != sent_date_2

cannot be interpreted as a validated contradiction among carriers of one scholarly document.

It is compatible with an aggregate archival object spanning multiple letters/extracts.

Thus:

    STABI_PRIMARY_DISCOVERY_CANDIDATES = COMPUTATIONALLY_IDENTIFIED

but:

    SINGLE-DOCUMENT_DISCOVERY_VALIDITY = NOT ESTABLISHED.

The count 7 must NOT be used as positive evidence for endogenous question emergence.

## 5. Scientific disposition

MODULE_I_FROZEN_EXECUTION = COMPLETE

MODULE_I_FULL_TRAJECTORY_POOL = 0

MODULE_I_MOTHER_PROBLEM_GATE = FAILED

STABI_DISCOVERY_POSITIVE_CLAIM = NOT AUTHORIZED

POST_HOLDOUT_SOURCE_OBJECT_VALIDITY = FAILED FOR 7/7 PRIMARY CANDIDATES

CONFIRMATORY_END_TO_END_EVIDENCE = NONE

This does not falsify R* because R* was never evaluated on an eligible full trajectory.

It shows the chosen StaBi source ecology does not instantiate the frozen end-to-end contract in a valid single-document form.

## 6. New object-boundary obligation exposed by the null

Document identity has at least two separable boundaries:

1. body/text boundary
   - primary letter versus annex/embedded document;

2. correspondence-metadata boundary
   - one scholarly correspondence object versus an aggregate archive/bundle represented by a file-level correspDesc.

A future discovery holdout must establish both before temporal carriers may be compared.

Multiple dates in one correspAction are not automatically competing claims about one letter.

## 7. No rescue

Do not:
- reinterpret the two sent dates as alternatives after seeing the holdout;
- add an aggregate-range decoder and rerun StaBi;
- select a favorable subset of the 465 files;
- rerun with repaired single-document eligibility and call it confirmatory;
- count the 7 primary candidates as positive discovery evidence.

StaBi is now exposed and may be used only for development of the next source-object contract.

## 8. Consequence

The mother problem remains empirically unresolved at the end-to-end discovery level.

A subsequent fresh holdout requires a pre-source-inspection gate that proves:
- a single primary scholarly document object exists;
- all compared t0 temporal claims are bound to that same object;
- aggregate correspondence records are either excluded or explicitly modeled under a separately frozen semantics.

That rule must be validated on exposed Berlin, Paul and now StaBi before another fresh corpus is opened.