# R1 Shared Repair Protocol v1

Date frozen: 2026-09-26
Status: PROSPECTIVE REPAIR TEST AFTER RETROSPECTIVE COLLISION DISCOVERY

## Purpose

The retrospective R1 audits established concrete projection collisions in Whitman and Faust. This protocol asks a different, constructive question:

> Can a small, explicitly source-bound repair restore the registered task output without reopening the entire source object, while an equally shaped wrong repair fails and an unaffected task remains unchanged?

The collision locations are already known. Repair-map candidates, success criteria, controls, and cost accounting below are frozen before repair outputs are computed.

## General rules

1. The base projection and target output are fixed per corpus.
2. Any auxiliary registry used by a decoder is counted as input, not treated as free knowledge.
3. Exact recovery means equality of the full registered output, not point accuracy on selected examples.
4. A wrong-binding control uses the same interface and comparable map size as the correct repair.
5. An unaffected task must remain exactly recoverable under base, correct-repair, and wrong-repair arms.
6. No claim of universal minimality follows from finite-corpus exactness.
7. Reopening the full native source is an upper-bound comparator and its byte cost is reported separately.

## Whitman repair task

Pinned source:
- repository: whitmanarchive/whitman-LG_1855_variorum
- commit: 25a00b7ebbdbc5246fce65a333bc761a5c22dad4
- relation file: source/authority/anc.02134.xml

Registered target output:
- for every printed locus, the exact set of (manuscript file, manuscript local locus, certainty).

Base projection:
- opaque group identifier
- printed locus
- manuscript-local locus
- certainty
- link order within group

Removed relation:
- linkGrp/@corresp manuscript-file identity.

Correct repair:
- explicit group_id -> manuscript_file binding registry derived from the pinned source.

Wrong repair:
- deterministically swap manuscript-file bindings of the first two eligible groups with distinct file identities.
- map cardinality and key domain remain unchanged.

Unaffected task:
- for every printed locus, recover the exact set of (opaque group id, manuscript-local locus, certainty).
- This output does not read manuscript-file identity.

Primary metrics:
- exact registered endpoint-set recovery for BASE / CORRECT_REPAIR / WRONG_REPAIR;
- number of printed loci with omissions or additions;
- registry entry count;
- UTF-8 serialized registry bytes under a canonical JSON encoding;
- source-object bytes;
- unaffected-task exactness in all three arms.

Success pattern for this corpus:
- CORRECT_REPAIR exactly recovers the registered endpoint output;
- WRONG_REPAIR does not;
- UNAFFECTED_TASK remains exact in all arms.

This is a source-bound constructive sufficiency result for the declared interface, not a proof that this registry is globally minimal.

## Faust repair task

Pinned source:
- repository: faustedition/faust-xml
- commit: 502eca65120dd6189ceaf41d4e5017775e6e4677
- population: eligible macrogenesis temp-pre assertions.

Registered target output:
- for every assertion occurrence, the exact set of source URIs.
- Locator text is not part of the target because it remains visible in the base projection.

Base projection:
- file context
- ordered item sequence
- complete locator-text bundle
- source count
- assertion occurrence identity only for aggregation, not as a lookup key.

Removed relation:
- source URI(s).

Candidate repair registries are tested in this frozen order:

1. locator_bundle -> source_uri_set
2. (file, locator_bundle) -> source_uri_set
3. (file, ordered_items, locator_bundle) -> source_uri_set

For each candidate:
- report whether the key is functional on the complete frozen population;
- if functional, execute exact recovery over every assertion;
- report registry entries and canonical serialized bytes.

Selection rule:
- the first candidate in the frozen order that is functional and yields exact recovery is the corpus-relative repair.
- If none succeeds, report NO_REGISTERED_REPAIR; do not add another key after seeing results.

Wrong repair:
- on the selected repair registry, deterministically swap outputs for the first two lexicographically ordered keys with distinct source-URI sets.
- registry key domain and entry count remain unchanged.

Unaffected task:
- reconstruct the complete ordered temporal-edge occurrence multiset (file, ordered items, adjacent directed edges, locator bundle), which does not read source URI.
- It must be identical under BASE / CORRECT_REPAIR / WRONG_REPAIR.

Full-source comparator:
- report compressed pinned archive bytes and extracted source-object population identity separately.
- Cost comparison is descriptive; compressed archive bytes and canonical registry bytes are not interpreted as a universal storage metric.

Success pattern for this corpus:
- at least one preregistered candidate repair is functional and exact;
- the selected correct repair restores all source-URI sets;
- wrong repair fails exact source-URI recovery;
- unaffected temporal structure remains exact.

## Cross-corpus interpretation

A positive result supports only:

> Explicit source-bound relation registries can restore a declared task from projections that otherwise admit collisions, while equally shaped wrong bindings fail and unrelated outputs remain invariant.

It does not establish:
- one universal repair schema;
- global information-theoretic minimality;
- that the repair relation can be inferred from projected content alone;
- population-level prevalence of such failures.

A negative or blocked result is retained.
