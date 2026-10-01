# Near-neighbor design audit for fresh ERIR confirmation v1

Date: 2026-09-29
Status: PRE-HOLDOUT DESIGN AUDIT. NO NEW EPISODE CONTENT WAS OPENED FOR THIS AUDIT.

## 1. Purpose

Module P has source-audited exposed development evidence for evidence-release-induced scholarly
revision (ERIR). Module Q must now seek prospective confirmation without reducing the task to one
specific TEI date pattern.

This audit reviews nearby Digital Humanities / cultural-heritage provenance traditions only to
improve experimental design.

It does not treat neighboring standards or systems as prior confirmation of the present claims.

## 2. Neighbor A — TEI revision/change history

Relevant TEI constructs:
- revisionDesc;
- listChange;
- change;
- change/@target;
- creation/listChange;
- recordHist.

TEI distinguishes at least two conceptually different uses:
- changes made during the evolution/creation of a source text;
- changes made during the evolution of the encoded representation.

The change element can point to one or more affected targets.

Design consequence:

A future fresh candidate may satisfy the later-event layer through a project-native TEI revision
history only if project-level documentation prospectively establishes that the relevant change is
a scholarly/editorial claim event rather than merely a technical XML/file maintenance action.

Required distinction:

    representation edit
    !=
    scholarly evidence/revision event

A candidate with revisionDesc alone does not pass the ERIR later-evidence gate.

Useful fields for a strong event contract:
- event/change identifier;
- target;
- who/responsibility;
- when;
- source/evidence link;
- change status/type.

## 3. Neighbor B — digital-edition versioning

Digital-edition versioning literature emphasizes:
- stable identification of edition states;
- separating informational content from interface/presentation versioning;
- keeping revision histories intelligible and citable;
- associating version identifiers with actual content changes.

Design consequence:

Module Q should freeze and evaluate source/content states, not rendered interface states.

The current/latest-resource comparator and ordered-snapshot comparator remain legitimate strong
baselines because versioned states are themselves meaningful scholarly infrastructure.

But version identity and state difference are not automatically equivalent to:
- why the change was made;
- which evidence licensed it;
- which scholarly proposition was revised.

This is exactly the distinction tested by Module M/P and should remain explicit in the fresh
holdout.

## 4. Neighbor C — provenance and change tracking in cultural-heritage RDF

Recent DH provenance work separates provenance dimensions including:
- object;
- attribution;
- process;
- versioning;
- justification;
- entailment.

It also distinguishes snapshot-oriented provenance from an explicit record of the operation that
produced the next snapshot.

A particularly useful neighboring pattern is:

    snapshot_i
    + explicit update operation
    -> snapshot_i+1

Design consequence:

Module Q may accept a non-TEI candidate if project-level documentation establishes:
- stable scholarly assertions/states;
- an explicit update/change operation or event layer;
- source/agent/justification provenance;
- a deterministic object/claim target.

A pure snapshot history still belongs to the strong comparator family.
An explicit update operation is closer to the retained transition semantics.

## 5. Neighbor D — CIDOC CRM E13 Attribute Assignment

E13 models an assertion-making activity rather than only the resulting property value.

Conceptually relevant distinctions include:
- the thing/proposition being assigned an attribute;
- the assigned value/relation;
- the activity by which the assignment was made;
- whose opinion/assignment it was;
- the possibility of contradictory assignments.

Design consequence:

For ERIR and especially the future non-temporal event family, a candidate can be stronger than a
date-correction corpus if it represents scholarly assignment/reassignment events explicitly.

Candidate examples include:
- attribution changes;
- source-status changes;
- identification changes;
- classification changes;
- condition/assessment changes.

The event must still be tied to a source/evidence basis; merely storing successive values is not
enough.

## 6. Neighbor E — CRMinf argumentation / belief adoption / provenance assessment

CRMinf explicitly models:
- argumentation/inference activities;
- adopted beliefs;
- evidence sources;
- provenance beliefs/assessments;
- conclusions derived/adopted through scholarly activity.

This is the closest conceptual neighbor to the mother problem.

Design consequence:

A stronger future event contract should, where the source ecology permits, distinguish:

    evidence object
    -> scholarly argument/assessment/adoption event
    -> proposition/belief state

rather than representing only:

    old value -> new value.

For the next fresh temporal ERIR holdout, this richer structure is desirable but not mandatory.

For the second non-temporal family, it should become a priority because attribution and
evidential-status revisions are naturally assertion/provenance events rather than simple scalar
value changes.

## 7. Neighbor F — Versioning Machine / witness comparison

Version-comparison systems show that multiple states/witnesses can be preserved and compared
side-by-side while retaining annotations and editorial material.

Design consequence:

State coexistence and comparability are valuable positive capabilities.

They should not be treated as weak baselines.

However side-by-side state comparison does not by itself establish:
- event authorization;
- evidence-to-transition binding;
- why one scholarly state superseded, qualified or challenged another.

This supports keeping Module-M strong snapshot comparators in the fresh study.

## 8. Revised conceptual design space

The next fresh candidate need not instantiate exactly:

    sent date + origDate.

It may instantiate any prospectively documented pattern of:

    S0 scholarly assertion/state
    +
    E independent evidence/change event
    +
    target/object binding
    +
    source/provenance/justification
    ->
    S1 scholarly assertion/state

Acceptable candidate event ecologies now include three broad families.

### Q-A Layered evidence

Example:
- current correspondence/document date;
- independent editorial/origin evidence.

This is the AMP-like pattern.

### Q-B Explicit editorial change event

Example:
- TEI change/listChange/recordHist;
- target points to a scholarly assertion/object;
- documentation establishes scholarly rather than technical change semantics.

### Q-C Assertion/provenance reassignment

Example:
- explicit attribution/identification/source-status assignment event;
- evidence and responsibility are represented;
- old and new assertions can coexist or be historically ordered.

Q-C is especially valuable because it begins bridging toward the required non-temporal event
family.

## 9. Fresh-candidate hard gates after neighbor audit

The existing Module-Q gates remain unchanged and are not weakened.

A candidate must still prospectively establish:
1. independent/unexposed ecology;
2. closed deterministic population;
3. stable scholarly object;
4. current/pre-event claim layer;
5. independent later evidence/event layer;
6. object/claim target relation;
7. provenance/source-audit feasibility;
8. portable execution without outcome-specific rescue.

Additional semantic check:

9. the later layer must document a scholarly change/evidence activity, not merely a technical file
   change or second serialization of the same value.

## 10. Fresh holdout endpoint

The fresh study should report capability vectors, not a single score.

Primary retained-interface tasks:
- pre-state recovery;
- event applicability;
- post-event result;
- selective update;
- provenance;
- transition attribution;
- delayed history.

Strong comparators:
- current/latest reopening;
- ordered snapshots / exact state diff.

If a neighboring project supplies explicit change operations, add a third comparator only if its
information budget is frozen before episode opening:

    operation log without claim/evidence justification.

This would test whether recording that an update occurred is sufficient when the scholarly reason
for the update is absent.

Do not introduce this comparator post hoc.

## 11. What is not imported from neighbors

This project does not claim:
- TEI revisionDesc is insufficient in general;
- PROV-O/CIDOC/CRMinf are insufficient;
- explicit event ledgers are universally required;
- every scholarly edition needs the same representation.

The present contribution remains task-relative:

    what distinctions must remain available for a declared scholarly inquiry/action to remain
    warranted, executable and historically auditable?

## 12. References consulted for design

- TEI P5 Guidelines: revisionDesc, listChange and change.
- Bleier et al.-style digital edition versioning discussion as represented by
  "Digital Editions and Version Numbering" (Digital Humanities Quarterly, 2020).
- Massari, Peroni, Tomasi, Heibi, "Representing provenance and track changes of cultural heritage
  metadata in RDF: a survey of existing approaches" (Digital Scholarship in the Humanities,
  published 2025; volume 41 supplement, 2026).
- W3C PROV-O.
- CIDOC CRM E13 Attribute Assignment.
- CRMinf 1.2.1.
- The Versioning Machine.
