# Module C v1 — Delayed source-route dependence under repository evolution

Date frozen: 2026-09-28
Status: NATURAL VERSIONED DEVELOPMENT STRESS TEST. NOT INDEPENDENT TRANSFER.

## Purpose

Test a delayed-dependence version of the mother problem:

> If a relation inventory remains fixed, does its ability to support later source inspection remain stable when the source repositories it points into evolve independently?

This is not a claim about the deployed Whitman Archive website. It is a versioned GitHub source-route audit.

## Fixed relation object

Repository:
whitmanarchive/whitman-LG_1855_variorum

Commit:
25a00b7ebbdbc5246fce65a333bc761a5c22dad4

Relation file:
source/authority/anc.02134.xml

Printed-side source remains pinned to the same commit:
source/tei/ppp.01880.xml

The current endpoint answer is therefore held fixed across all source environments.

## Source environment E2019

Manuscripts:
- commit 249bc14594fa1c0428e7ca39f52753de21ce604b
- tree 1871715fbcef5f9721e80f385471a86ad52ef463

Notebooks:
- commit 682c04c0998739b8edfd75e0e7496592777e2898
- tree 90ce5a76b2358d3350e889b6988af8e26bcdd835

These are the pinned contemporaneous snapshots used in the Module B2 source-route v2 audit.

## Source environment ECURRENT

Manuscripts:
- commit 2fe2c934f0b63ce66d4e43f36798767785f2b70c
- tree 6a0372f5d3e111226f6a96bedaa8724ef18c5854
- commit date 2026-09-24

Notebooks:
- commit a7b000f613e4c4fcf38cec4d58aebd6c857ffe37
- tree b1c6b7d631c04fae49939f24cadd66eba697b6cc
- commit date 2025-08-11

The commits are pinned before execution.

## Population

All 1,444 valid relation links from the fixed relation inventory.

Primary continuation target:
the exact manuscript/notebook source file and local xml:id named by each relation.

Certainty remains the Archive's encoded status and is used only to stratify source-route trajectories.

## Routing rule

Within each environment:

1. if a source filename appears in exactly one of manuscripts or notebooks, route there;
2. if it appears in both, classify AMBIGUOUS_REPOSITORY;
3. if it appears in neither, classify MISSING_FILE;
4. if the file exists but local xml:id is absent, classify MISSING_LOCAL_ID;
5. otherwise classify RESOLVED.

The printed endpoint is also checked against the fixed printed source, but source-environment comparison concerns the manuscript/notebook side.

No filename alias or ID remapping is learned after outcome.

## Trajectory classes

For every relation link:

- STABLE_RESOLVED: RESOLVED in E2019 and ECURRENT
- REPAIRED_OVER_TIME: unresolved in E2019, RESOLVED in ECURRENT
- BROKEN_OVER_TIME: RESOLVED in E2019, unresolved in ECURRENT
- STABLE_UNRESOLVED: unresolved in both

For unresolved states, preserve the reason in each environment.

## Questions

Q0:
Does the fixed relation inventory still encode the same endpoint strings?
Expected by construction: yes.

Q1:
Does the same endpoint string remain executable as a lawful source route across source-repository versions?

Q2:
For the low-certainty continuation targets from Module B2, how many remain executable, become executable, or stop being executable?

Q3:
Do file-level persistence and local-ID persistence fail independently?

## Metrics

- link trajectory counts;
- trajectory counts by high/low certainty;
- distinct source files per trajectory;
- file present / local ID present separately;
- low-certainty branch-target executability in each environment;
- current endpoint strings unchanged;
- source bytes / files by environment;
- no pooled independence claim over links sharing files.

## Claim ceiling

A positive drift result supports only:

> A fixed scholarly relation representation can preserve its endpoint strings while its executable source-following capacity changes across independently versioned source repositories.

This does not establish:
- that the deployed archive broke;
- that one repository version is historically superior;
- that every digital edition exhibits such drift;
- that source IDs should never change;
- that current GitHub state is the only lawful source route.

## Stop rule

No post-outcome alias map, fuzzy ID matching, or later source is added to rescue unresolved routes in v1.

Any repair/migration study must be separately versioned after this audit.
