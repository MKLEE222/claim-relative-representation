# Whitman source-route evaluator repair v2

Date: 2026-09-28
Status: POST-v1 SOURCE-CONTRACT REPAIR ON EXPOSED DEVELOPMENT DATA.

## Trigger

Module B2 v1 routed every relation @corresp file through the contemporaneous whitman-manuscripts repository.

The relation inventory, however, explicitly concerns manuscript OR notebook passages. A repository audit after v1 found that among 151 distinct @corresp filenames:

- 130 occur in the pinned 2019 manuscripts tree;
- 12 occur in the pinned 2019 notebooks tree;
- 0 occur in both trees;
- 9 occur in neither pinned tree.

Therefore the v1 source-route metric is not an adequate test of the declared source ecology.

This does not affect:
- current endpoint equivalence;
- 120 mixed-locus controlled certainty-binding separations;
- correct/wrong certainty-ledger results.

It affects only source-route executability.

## Added pinned notebook source

Repository:
whitmanarchive/whitman-notebooks

Commit:
682c04c0998739b8edfd75e0e7496592777e2898

Tree:
90ce5a76b2358d3350e889b6988af8e26bcdd835

This is the latest commit returned at or before 2019-06-05 on the repository's commit history queried for the relation-file creation period.

## Routing rule

For each @corresp filename:

1. if present in the pinned manuscripts tree, route to manuscripts;
2. else if present in the pinned notebooks tree, route to notebooks;
3. if present in both, report AMBIGUOUS_SOURCE_REPOSITORY and do not choose;
4. if present in neither, report SOURCE_FILE_UNRESOLVED.

Then verify the target xml:id in the routed TEI file.

No later repository state is used to repair a 2019 route in the primary v2 metric.

## Authority

v1 source-route results are preserved as manuscript-only diagnostic output.
v2 is authoritative only for the contemporaneous two-repository source-route audit.
This is post-outcome evaluator repair, not confirmatory evidence.
