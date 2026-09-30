# Formalization Papers authoritative fresh attempt INVALID v1

Date: 2026-09-30
Status: AUTHORITATIVE FRESH OUTCOME / INVALID / FRESHNESS CONSUMED.

## 1. Frozen prospective run

Workflow:

    formalization-papers-fresh-qualified-composition-v1

Run:

    36657856767

Trigger/head:

    af8be87c21bdbc9734b8913466299d5ecb516514

The workflow completed technically, but the scientific disposition is:

    INVALID

This label is permanent for the authoritative fresh attempt.

## 2. DATA_OPEN event

DATA_OPEN_EVENT was emitted before any record archive was downloaded.

UTC:

    2026-09-30T02:01:23.587128+00:00

Frozen source:

    LaraHack/formalization_papers_supplemental
    tag v1.0
    commit 2f68d8498aeeb724e3438deda13e74ae7fb076d8

Published nanopublication index used:

    false

The frozen source archive was then downloaded.

Therefore candidate record-level freshness is consumed and is not restorable.

## 3. Frozen source archive

Archive SHA-256:

    c2349aa34350dc5f02f3ad7ccfc1ff6f879e88950fee948b0d5ffa206d4ca9e3

Record files under nanopubs/:

    10

The authoritative runner retained each relative path, byte size and SHA-256.

## 4. Primary invalidation

For all 10 record files:

    parser_exact = false

between the frozen:
- RDFLib oracle;
- pyoxigraph runtime.

The main runner therefore stopped before population classification under the frozen rule:

    PARSER_OR_REGISTERED_SURFACE_FAILURE

No T0-T9 population result was produced.

No root or eligible chain was selected after seeing the disagreement.

## 5. Documentary audit consequence

The independent raw-TriG documentary auditor did derive a non-empty root set.

Because the authoritative main runner had already aborted before producing a population root set:

    root_set_exact = false

and documentary audit overall:

    FAIL

with:

    DOCUMENTARY_ROOT_SET_MISMATCH

This is downstream of the primary parser-surface invalidation and is not interpreted as an
independent substantive negative result.

## 6. Final authoritative disposition

Final:

    INVALID

Reasons:

    PARSER_OR_REGISTERED_SURFACE_FAILURE
    DOCUMENTARY_ROOT_SET_MISMATCH

This result does not establish:
- absence of T0/T1 trajectories;
- failure of qualified composition;
- NULL_APPLICABILITY;
- BOUNDED_PARTIAL;
- a negative empirical claim about Formalization Papers.

The population scientific question was never reached because the registered extraction gate did
not close.

## 7. Scientific engine identities at DATA_OPEN

Git blob identities:

    fp_constants.py
    69d96f700dc90bf2cd1fc2a83f60e06e07cbee3d

    fp_oracle.py
    10069272597e183f8e0f857d9693691730b82d2f

    fp_runtime.py
    d3991f0d2c3827a19ac67a02f7526f5fbd7693aa

    fp_population.py
    21257498e78b11fe5996f00c398bd70ab39bc3a4

    run_fp_fresh_population_v1.py
    21800a8eb456892efff609013c32505d46c7b134

    fp_documentary_audit_v1.py
    7e7f77377e7c2402b8c700ae2fb36420247b2ec2

    fp_finalize_v1.py
    3bd10046534291b3a01f34861a66d5c0c267e83f

## 8. Result artifact

Artifact:

    11072718112

Artifact ZIP SHA-256:

    3e5ebb0fd12abfd77fa0028dd7766c1dc820e0fca6cc7ba9e33fc9ee8d062e15

Result hashes:

    fp_fresh_main_v1.json
    65763dd6250d138820c4efd794ac1a4ded28b4a6a3d7028f04d4bae99dd8a0c3

    fp_fresh_documentary_audit_v1.json
    8147eaf208f37826efa24a25c1a01e311b92f2de459b90a209fcc548a678c31d

    fp_data_open_event_v1.json
    6e851ec12a6d6ab9c1e76c3440eb2e56b4f02dd1ce96d8e5d79332c994ec1b03

## 9. Authorized post-fresh work

Now that records are exposed, the next work is diagnostic/corrected reproduction only.

Authorized:
1. use the exact frozen source archive/commit;
2. compare the two extractors component by component;
3. identify the first and complete mismatch classes;
4. distinguish semantics-preserving RDF term serialization differences from registered scientific
   relation disagreement;
5. freeze any implementation-only correction before corrected reproduction;
6. rerun on byte-identical source;
7. independently documentary-audit the corrected result.

Not authorized:
- relabel the first attempt as fresh PASS;
- restore freshness;
- change T0-T9 after observing the population;
- subset the record files;
- use the published index to rescue the result;
- change the relation vocabulary to fit observed cases.

Any corrected reproduction is:

    POST-FRESH / EXPOSED CORRECTED REPRODUCTION

not fresh confirmation.
