# External DH Materials Contract v1

Date frozen: 2026-09-24
Status: PRE-EXPERIMENT PORTFOLIO FREEZE

## Purpose

The project will use several independently created Digital Humanities resources as external validation materials while retaining the Yule-Cordier transition-episode corpus as the primary humanistic carrier.

The external materials do not form one pooled benchmark. Each is assigned a distinct validation role derived from the scholarly task for which that resource was originally built.

This prevents a common failure mode: selecting unrelated DH datasets only to increase sample count.

## Portfolio roles

### P0 - Primary humanistic carrier

**Yule-Cordier**

Role:
- source-grounded claim/warrant analysis;
- task-contract development;
- access/relation/workflow mechanism discovery;
- transition-episode corpus construction.

This is the only material currently authorized to support the paper's full humanistic claim-state chain.

### P1 - Independent representation/alignment validation

**Frankenstein Variorum**

Original scholarly task:
- collate and navigate five historically distinct versions of Frankenstein;
- compare heterogeneous source encodings;
- support passage-level investigation of textual transformation.

Validation role here:
- test task-relative representation adequacy for alignment and variant recovery;
- examine the project's own documented transition from heterogeneous TEI source structures to comparable flattened XML and a stand-off TEI spine;
- test whether our task-adapted recoverability framework maps naturally to an independently designed collation workflow.

No Yule-Cordier ontology term is required for the human-facing task.

### P2 - Independent uncertainty/relation validation

**Walt Whitman Archive / 1855 Leaves of Grass Variorum**

Original scholarly task:
- connect manuscripts/notebooks to printed lines;
- encode printed variants separately from manuscript relations;
- preserve possible/speculative relations rather than forcing all relations into a stronger genetic apparatus.

Validation role here:
- test the distinction between relation availability, relation type, and epistemic strength;
- test whether stronger/weaker relation representations change task-adapted entitlement;
- externalize the project's distinction between documentary linkage and downstream epistemic adjudication.

The Archive's own editorial uncertainty remains authoritative; this project does not relabel uncertain links as certain.

### P3 - Independent temporal/provenance/conflict validation

**Digital Faust Edition / Macrogenesis**

Original scholarly task:
- aggregate dated and relative chronological assertions about witnesses;
- preserve source attribution;
- represent conflicts and removed/ignored edges;
- produce a chronology compatible with the retained assertion graph.

Validation role here:
- test source-qualified temporal recovery;
- test whether projection of provenance/conflict metadata changes the task state;
- provide an independent graph-based case where chronology is not simply a single canonical order.

The Faustedition's own graph semantics and conflict flags are used as the external object's semantics.

### P4 - Corpus-design reference

**ELTeC**

Role:
- methodological reference for transparent, operationalized corpus selection and task-specific sub-collections;
- not a primary experiment carrier in the current paper.

ELTeC is not counted as an external replication unless a concrete ELTeC task is separately preregistered.

### P5 - Self-constructed historical external holdout

**Scrivener, A Plain Introduction to the Criticism of the New Testament (4th ed.)**

Role:
- researcher-constructed external transition episode using independently existing native digital objects;
- kept distinct from independently curated DH validation materials P1-P3.

It cannot substitute for P1-P3 when arguing that the framework transfers to pre-existing DH scholarly infrastructures.

## Anti-pooling rule

The project will not average Frankenstein, Whitman, Faust, Yule-Cordier, and Scrivener into one global score.

Each material tests a different contract:

- alignment/variant task;
- uncertain relation task;
- source-qualified temporal task;
- historical claim-warrant task;
- external transition-episode task.

Cross-material synthesis is qualitative/mechanistic unless a shared measure has been preregistered and is genuinely commensurable.

## Native-semantics rule

For every external DH material:

1. preserve the project's original task terminology;
2. preserve native relation/variant/chronology semantics;
3. do not retrofit CEDL labels into the source data;
4. map to the project's analytical layer only after native-task outcomes are represented;
5. report N/A when a project concept has no native analogue.

## Representation provenance

Every external experiment must distinguish:

- the project's native source representation;
- any project-authored derived representation;
- any controlled projection introduced by this study.

A representation created by the external DH project is still independent of this study and must not be called our "ideal" representation.

## Outcome hierarchy

External materials may support:

- representation/task mechanism claims;
- recoverability/profile claims;
- transfer/boundary claims.

They do not automatically support Yule-Cordier-specific humanistic claim states.

## Promotion rule

An external material becomes an executed validation block only after:

1. native task and data semantics are documented from the project's own sources;
2. exact data files/endpoints are frozen;
3. a task entry state is frozen;
4. the mapping to our framework is frozen;
5. target/evaluation information is separated from live task input;
6. no result has been inspected under our transformation.
