# Holdout Promotion Gate v2

Date: 2026-09-26
Status: SUPERSEDES v1

A workflow may be called an untouched holdout only if:
1. source identity/hash is frozen;
2. task entry state is frozen;
3. workflow version is frozen;
4. target-only information is isolated to evaluation;
5. null/failure retention is explicit;
6. case-specific tuning hooks are absent;
7. holdout role is declared before execution;
8. the target/outcome has not been used to design the workflow.

## Current dispositions

- EP_PM_01: DEV. Never promoted to replication.
- EP_KS_01: EXPLORATORY_TRANSFER_AFTER_FAILURE. The generic transfer result is valid, but the successful native-referent bridge was diagnosed after the generic failure and is not an untouched holdout.
- EP_KS_02 / EP_KS_03: SEALED_NEAR_HOLDOUT; blocked from confirmatory promotion until exact scan transcription/reference verification is complete.
- EP_CL_01: EXECUTED_BOUNDARY. Valid for the local-attachment access mechanism; not promoted to confirmatory warrant evidence while exact scan transcription remains pending.
- EP_EXT_01: EXECUTED_EXTERNAL_HOLDOUT for documentary localization/minimal pointer sufficiency.
- Frankenstein C17: SEALED_EXTERNAL_HOLDOUT for selective task adaptation.
- Frankenstein C18: SEALED_EXTERNAL_HOLDOUT for minimal-carrier search.

## Warrant closure

The final paper-money LLM warrant experiment is not labeled a historical holdout.
It is a controlled downstream consequence test on a development primary case with frozen packets and selective rescue/removal controls.

This distinction prevents the paper from laundering development evidence into holdout language.