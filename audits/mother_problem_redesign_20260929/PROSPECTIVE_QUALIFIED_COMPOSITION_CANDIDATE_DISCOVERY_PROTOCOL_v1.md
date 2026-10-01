# Prospective independent qualified-composition candidate discovery protocol v1

Date frozen: 2026-09-29
Status: PRE-DISCOVERY / PRE-CANDIDATE-OUTCOME.

## 1. Goal

Identify a genuinely independent scholarly ecology for prospective confirmation of target-bound,
history-sensitive qualified composition.

The target phenomenon is not another one-step reassessment.

The project must make it prospectively plausible that:

    S0 --g1--> S1 --g2--> S2

where:
- g1 and g2 are qualified from source-native relations rather than supplied as operations;
- the first act can change whether/how the second act is qualified;
- relation-target identity is representable;
- retained transition/provenance history is available.

## 2. Freshness rule

Candidate discovery is documentation-only.

Allowed before a candidate-specific scientific contract is frozen:
- project landing pages;
- public project documentation;
- published papers describing the data model;
- repository root/directory trees;
- README files;
- ODD / RNG / XSD / SHACL / ontology/schema files;
- generic templates and generic transforms;
- API/schema documentation that contains no episode/result records;
- distribution metadata only.

Disallowed before candidate-specific contract freeze:
- episode XML/JSON/RDF/CSV records;
- object pages containing candidate target outcomes;
- repository-wide code search that returns record snippets;
- search-engine queries by object/record ID;
- SPARQL/API queries that return record assertions;
- raw data distributions;
- sample records whose substantive relation outcome is visible;
- issue/commit history that exposes target record contents.

Any disallowed exposure is logged and removes strict freshness for the exposed candidate scope.

## 3. Hard scientific gates

A candidate passes documentation screening only if project-level evidence establishes all of:

### C1 Independent ecology

Not the Yule-Cordier corpus and not an AAD/VGW reuse framed as fresh confirmation.

### C2 Stable scholarly object/proposition target

The model exposes stable IDs/URIs/anchors for the scholarly object and for the assertion,
assignment, reading, attribution, identification, or editorial proposition that later acts target.

### C3 Source-native intervention relation

The model contains a native way to express a relation such as:
- correction of;
- supersedes;
- challenges;
- corroborates;
- previous attribution;
- reassignment;
- reply/response;
- acceptance/rejection;
- version-to-version replacement;
- explicit change target.

The relation must not be invented from the desired generator outcome.

### C4 Connected multi-step possibility

Project documentation must make at least one two-step connected trajectory structurally possible:

    act2 targets either:
    - the assertion produced by act1; or
    - a transition/reassessment event produced by act1.

A mere ordered list of snapshots is insufficient.

### C5 Relation-target binding

The data model must preserve which prior assertion/event is targeted, not only a relation type.

### C6 Provenance/history retention

The model must retain enough actor/source/time/version history to reconstruct why the target
assertion/event entered the state.

### C7 Deterministic source scope

A bounded population/distribution/version can be frozen before records are opened.

### C8 Pre-record adapter feasibility

The object/relation/history adapter can be specified from schema/docs alone.

## 4. Preferred evidence

Higher-value candidates have:
- explicit event/assignment/revision entities;
- typed relation target edges;
- version/provenance entities;
- multiple independent source providers or editorial layers;
- machine-readable schema;
- closed distribution snapshot;
- natural null / history-only actions.

## 5. Screening outputs

For each candidate record only:
- project name;
- public project URL;
- repository URL if public;
- documentation sources inspected;
- whether any record content was exposed;
- C1-C8 disposition;
- candidate relation family;
- likely object/proposition identity;
- likely transition-history identity;
- deterministic-population feasibility;
- scientific risks;
- freshness status.

Do not record candidate episode IDs before the candidate-specific contract is frozen.

## 6. Stop rule

Do not open candidate data merely to see whether positive trajectories exist.

If project-level documentation cannot establish C1-C8, mark:

    SCREEN_FAIL_DOCUMENTATION_INSUFFICIENT

and move on.

If one candidate passes all C1-C8, stop broad discovery and freeze:
- candidate exposure registry;
- data-model adapter;
- relation vocabulary;
- target binding;
- denominator;
- synthetic controls;
- independent oracle/runtime;
- PRE_DATA/DATA_OPEN execution boundary

before any record is opened.

## 7. Claim ceiling

Documentation screening establishes structural feasibility only.

It does not establish:
- that any qualifying natural trajectory exists;
- prevalence;
- generator success;
- prospective confirmation.

Those remain outcome-blind until the one-shot opening.
