# Ecological Anchor E1 results - paper-money access/discovery

Date: 2026-09-24
GitHub Actions run: 35954991944
Commit: 45f30461bdd7fda0e625691cb0eff0b27f6c9efe

## Provenance check

The live Project Gutenberg texts fetched by the CI run produced:

- Volume I SHA-256: 7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5
- Volume II SHA-256: c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

These exactly match the hashes already frozen in the source registry before E1 was run.

This is a strong provenance check: E1 operated on the same native Gutenberg objects used during source discovery, not on a rewritten experiment-only text.

## Frozen seed-derived query

The query terms generated from PM02 using Volume-I-only TF x IDF were:

liang | silver | mulberry-trees | bank-notes | exchange | amount | tree | broussonetia | kwei | moraceae | rents | same

The target-only name LAUFER did not enter the query.

## Results

### W_CURRENT_OBJECT

PM03 was outside the searchable scope.

- target_in_scope: 0
- candidates: 3007
- target rank: NA
- Hit@20: 0

This is an access-horizon result, not a retrieval-quality result.

### W_DECLARED_COLLECTION

PM03 was inside the searchable scope, but the frozen seed-derived retrieval policy ranked its target window 5835 of 6033 candidates.

- reciprocal rank: 0.000171
- Hit@1: 0
- Hit@5: 0
- Hit@10: 0
- Hit@20: 0

## Interpretation

The ecological access hypothesis is **not supported in the strong form** that broader collection scope by itself makes the later corrective witness practically discoverable.

The run separates two failure modes:

1. **scope exclusion** - under current-object-only access, PM03 cannot enter the candidate set at all;
2. **retrieval failure** - under collection access, PM03 enters the candidate set but is not surfaced by the frozen seed-similarity policy.

Therefore discoverability cannot be attributed to representation/access scope alone.

## Design consequence

The next access design must explicitly factor retrieval policy from representation scope.

A suitable model is:

Disc(tau, R, K, pi)

where pi is a frozen retrieval/navigation policy.

Representation scope determines what can be retrieved; retrieval policy determines what is surfaced from that scope.

The project must not interpret a poor rank under one retrieval policy as evidence that the representation itself made PM03 unavailable.

## Status

E1 is closed as a valid negative ecological pilot.

- native/workflow provenance: PASS
- target leakage check: PASS
- current-object scope exclusion: OBSERVED
- collection-scope target availability: OBSERVED
- practical retrieval under frozen seed-TFIDF: FAIL
- ecological Tier-3 mechanism claim: NOT ESTABLISHED

No query tuning is allowed retroactively inside E1.
