# Ecological Anchor E1D - Retrieval-policy sensitivity diagnostic

Date frozen: 2026-09-24
Status: EXPLORATORY DIAGNOSTIC AFTER E1

## Why this diagnostic exists

E1 established:

- PM03 is unavailable under a Volume-I-only search scope;
- PM03 is available but ranked 5835/6033 under the frozen seed-similarity policy over the two-volume collection.

E1D does not alter or rescue E1. It asks a new question:

> Is the poor collection-level retrieval result specific to the retrieval policy?

## Native inputs

The same live Project Gutenberg Volume I and Volume II/addenda texts and the same frozen PM02 seed / PM03 evaluation anchors are used.

Their SHA-256 values are re-reported.

## Policies

### PI_NAMED_SOURCE_CHAIN

Extract the surname following "Dr." in the PM02 source window.

Expected extraction rule is generic; the expected extracted value is not hard-coded into ranking logic.

Search both volumes for 180-word windows containing that extracted surname, excluding the known PM02 seed neighborhood.

### PI_NAMED_SOURCE_DOMAIN_FILTER

From the same PM02 seed window, derive a frozen domain lexicon by retaining seed tokens from:

mulberry, mulberry-trees, bark, broussonetia, papyrifera, bank-notes, money

Only terms actually present in the seed may be activated.

Filter named-source hits to windows that also contain at least one activated domain term after hyphen normalization.

## Target leakage

The target-only name LAUFER is forbidden from query/filter construction.

PM03 target anchors are used only after candidate generation to calculate target inclusion and ordinal.

## Outcomes

For each policy:

- extracted source name;
- activated domain terms;
- candidate-set size;
- whether PM03 is in the candidate set;
- target ordinal among candidates;
- inspection burden represented by candidate-set size/ordinal.

## Interpretation

If a seed-derived chaining policy surfaces PM03 with a small candidate set, E1's failure is retrieval-policy-sensitive.

If it does not, the access problem persists even under source chaining.

This remains a retrievability diagnostic, not a human discoverability result.
