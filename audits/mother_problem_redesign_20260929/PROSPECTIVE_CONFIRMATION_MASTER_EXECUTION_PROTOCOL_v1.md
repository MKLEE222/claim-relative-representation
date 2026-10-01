# Prospective confirmation master execution protocol v1

Date frozen: 2026-09-30
Status: REUSABLE PRE-DATA EXECUTION CONTRACT / NO NEW CANDIDATE DATA OPENED.

## 1. Purpose

Previous prospective assets repeatedly failed at the execution layer after the irreversible
DATA_OPEN boundary:
- AAD: import-path failure before source acquisition, later followed by exposed execution;
- VGW: natural N-Triples lexical cases not exercised by the pre-fresh synthetic path;
- Formalization Papers: natural RDF term/surface cases not exercised by the pre-fresh synthetic
  path.

The scientific contracts survived corrected reproduction, but literal fresh-positive status was
lost.

This protocol removes the infrastructure asymmetry that allowed those failures.

## 2. Core rule

A future candidate may cross DATA_OPEN only if the exact authoritative execution stack has already
completed once on a closed synthetic source package.

"Exact stack" means the same:
- source-loader interface after bytes are supplied;
- parser/oracle implementation;
- parser/runtime implementation;
- population accounting;
- denominator construction;
- qualification;
- counterfactual execution;
- action-relative equivalence probes;
- documentary audit;
- finalizer;
- result serialization;
- artifact manifest generation.

A separate lightweight synthetic test that bypasses any authoritative stage is insufficient.

## 3. Candidate package interface

Every candidate-specific package must provide:

    source_manifest_v1.json
    scientific_manifest_v1.json
    synthetic_source/
    run_authoritative_v1.py
    run_documentary_audit_v1.py
    finalize_v1.py

The authoritative runner must accept exactly:

    --source <path-or-frozen-source-handle>
    --output-dir <path>
    --mode synthetic|authoritative

The mode may alter only:
- the source loader;
- output labels identifying synthetic versus authoritative execution.

It may not select a different parser, population classifier, qualification engine, evaluator,
counterfactual set, or finalizer.

## 4. Scientific manifest

Before DATA_OPEN, freeze:
- candidate protocol blob;
- source schema/documentation anchors;
- relation vocabulary;
- Beta(g) binding predicates;
- Kappa(g) state/history predicates;
- population denominator rule;
- generator vocabulary;
- history-required generators;
- history-not-required generators;
- connected sequence grammar;
- action-relative equivalence perturbations;
- independent parser/oracle file hashes;
- independent parser/runtime file hashes;
- documentary auditor hash;
- finalizer hash.

All files are checked by Git blob/hash immediately before opening.

## 5. Synthetic-source completeness

The synthetic source is not merely a positive toy example.

It must exercise every registered parser/data-model surface that documentation/schema establishes
as admissible for the candidate scope.

At minimum, where applicable:
- scalar and multi-valued properties;
- optional and required properties;
- all registered RDF/XML/JSON literal datatypes;
- timezone/date lexical variants admitted by the source specification;
- URI and stable-node identities;
- blank/non-addressable nodes if the source format permits them;
- multiple creators/agents;
- relation-target multiplicity;
- supersession/retraction/version cases;
- every registered trajectory class;
- every registered rejection class;
- history-present and history-ablated states;
- at least one history-required and one history-not-required generator.

The candidate package must contain a coverage manifest mapping every registered parser/model surface
to at least one synthetic fixture.

Any uncovered registered surface blocks DATA_OPEN.

## 6. Exact-path PRE_DATA rehearsal

Before DATA_OPEN, the workflow must run:

### A. Environment closure
- install every dependency used after DATA_OPEN;
- import every authoritative module;
- compile every script;
- print dependency versions;
- verify no dependency installation remains after the DATA_OPEN marker.

### B. Scientific blob closure
- verify all frozen scientific and protocol hashes.

### C. Full synthetic authoritative run
Run:

    run_authoritative_v1.py
        --source synthetic_source/
        --mode synthetic

This must produce the same artifact classes expected after real opening:
- source manifest;
- parser/oracle result;
- parser/runtime result;
- population accounting;
- every disposition;
- every connected sequence;
- every forward generator sequence;
- every registered counterfactual;
- action-relative equivalence result;
- run summary.

### D. Exact documentary audit
Run the actual:

    run_documentary_audit_v1.py

against the synthetic source and synthetic authoritative result.

The documentary auditor may not import either primary extractor.

### E. Exact finalizer
Run the actual:

    finalize_v1.py

and require the synthetic final scientific disposition to equal the preregistered synthetic
expectation.

### F. Artifact round-trip
Package the complete synthetic result artifact exactly as the authoritative artifact will be
packaged.

Then:
- upload it;
- download it again;
- verify ZIP SHA-256;
- verify required filenames;
- verify each contained result SHA-256;
- rerun a read-only artifact validator on the downloaded copy.

DATA_OPEN is forbidden until the artifact round-trip succeeds.

## 7. Single-environment boundary

The authoritative candidate workflow should use one job whenever feasible.

All of the following happen before DATA_OPEN in the same runner environment:
- dependency installation;
- imports;
- compilation;
- synthetic exact-path rehearsal;
- documentary audit;
- finalizer;
- artifact round-trip verification.

Only then is:

    DATA_OPEN_EVENT_v1.json

written.

No dependency installation, code generation, package upgrade, schema discovery or scientific file
mutation is permitted after DATA_OPEN_EVENT.

This removes environment drift between pre-data and data-open phases.

## 8. DATA_OPEN marker

Immediately before the first candidate-source byte is fetched, write:

    DATA_OPEN_EVENT_v1.json

with:
- repository HEAD SHA;
- workflow run ID and attempt;
- UTC time;
- candidate source handle;
- source version/commit/tag;
- scientific manifest SHA-256;
- synthetic coverage manifest SHA-256;
- every scientific Git blob/hash;
- dependency/version manifest SHA-256;
- pre-data synthetic artifact SHA-256.

The marker is preserved even if subsequent execution fails.

## 9. Authoritative source acquisition

After the marker:
- fetch only the preregistered immutable source handle;
- do not discover alternative URLs;
- do not query provider APIs for rescue records;
- compute source byte hashes before parsing;
- preserve complete source accounting.

If source resolution differs from the preregistered immutable identity:

    INVALID_SOURCE_SCOPE

No fallback source is allowed.

## 10. No first-natural-case code path

After DATA_OPEN, natural data may supply values but may not trigger a code path that was absent
from the synthetic exact-path rehearsal.

Operationally, the authoritative runner must emit a registered execution-surface trace.

Each trace label must occur in the pre-data synthetic coverage manifest.

If natural execution reaches an unregistered trace label:

    INVALID_UNCOVERED_EXECUTION_SURFACE

The run stops.

This does not mean every natural value must have appeared synthetically.

It means every parser/model/qualification branch used by the natural run was rehearsed before
opening.

## 11. Candidate scientific requirements

The next clean prospective ecology must test the already-closed theoretical formulation:

    Sigma(g) = (Beta(g), Kappa(g))

It must preregister:
- at least one connected multi-step scholarly sequence;
- at least one history-required generator;
- at least one history-not-required generator;
- exact target/relation binding;
- live/version state;
- at least one action-relative equivalent-state perturbation;
- REQUIRED-dimension rejection witnesses;
- NOT_REQUIRED-dimension invariance witnesses;
- complete denominator.

A one-step reassessment corpus is insufficient.

## 12. Independent-engine requirement

At least two independent implementations must agree on the registered scientific surface.

They may share:
- frozen constants;
- synthetic fixture bytes;
- final comparison schema.

They may not share:
- parser implementation;
- candidate extraction function;
- qualification implementation when independent qualification is part of the claim.

Documentary audit remains a third path.

## 13. Final dispositions

### INVALID

Any:
- source identity mismatch;
- uncovered natural execution surface;
- parse failure;
- independent-engine disagreement;
- incomplete population accounting;
- denominator mismatch;
- documentary-audit mismatch;
- finalizer inconsistency.

### NULL_APPLICABILITY

No registered connected sequence exists in the complete population.

### BOUNDED_PARTIAL

Connected structure exists but one preregistered scientific criterion is naturally unavailable
without implementation failure.

### PASS

At least one registered connected sequence exists and:
- all registered natural eligible sequences execute;
- all applicable REQUIRED rejection probes behave as frozen;
- all registered NOT_REQUIRED invariance probes behave as frozen;
- action-relative equivalence checks pass;
- sequence write/read closure passes;
- independent engines agree;
- documentary audit passes;
- complete population accounting closes.

No post-open category is invented.

## 14. Freshness discipline

Before DATA_OPEN:

    PRE_DATA_ABORT

is recoverable only if:
- no candidate bytes acquired;
- no candidate record parsed;
- no outcome observed;
- scientific contract unchanged.

After DATA_OPEN:

freshness is consumed permanently.

Implementation repairs may support corrected reproduction but never restore fresh PASS.

## 15. Stop rule

Do not open another candidate until:
1. this master protocol is frozen;
2. the candidate-specific package implements this interface;
3. exact-path synthetic rehearsal passes;
4. coverage manifest has no uncovered registered surface;
5. artifact round-trip passes.

The next fresh ecology has one purpose:

    obtain a clean prospective test of the typed generator-relative theory

not merely add breadth.
