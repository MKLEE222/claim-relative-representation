# Formalization Papers prospective qualified-composition protocol v1

Date frozen: 2026-09-29
Status: PRE-RECORD / PRE-DATA-OPEN.

## 1. Scientific question

Can target-bound, history-sensitive scholarly action qualification be prospectively reproduced in
an independent semantic-publishing/reviewing ecology whose relations and object identities are
native to that project?

The target is not review sentiment, acceptance prediction or workflow accuracy.

The target is:

> whether project-native relations and retained target/provenance history are sufficient to
> determine which scholarly action is lawfully available from the current formalization state,
> and whether earlier acts constrain later acts.

## 2. Independent ecology

Candidate:

    Formalization Papers semantic publishing/reviewing field study

This ecology is independent of:
- Yule-Cordier;
- Berlin/Paul/AMP/AAD;
- VGW.

Its native representation uses nanopublications and Linkflows/PSO/NPX relations.

No Yule-Cordier relation label is required for the primary adapter.

## 3. Frozen source scope

Authoritative record scope:

    LaraHack/formalization_papers_supplemental
    release tag v1.0
    commit 2f68d8498aeeb724e3438deda13e74ae7fb076d8

Supporting generic relation documentation:

    LaraHack/fpsi_analytics
    commit b6aef0049b3b2f02fc67030c080218617d71ab41

Published nanopublication index known but unopened:

    http://purl.org/np/RAkLJW7vIsnKKJDf1iswdgtFPQSo3lEG_z8DhHfD7dofE

The primary one-shot opening should prefer the immutable v1.0 supplemental snapshot if all
required nanopublication files are contained there.

The public index may be used only if the v1.0 snapshot cannot provide a complete bounded
population and that fallback is pre-declared before DATA_OPEN.

## 4. Population root

A population root is a submitted formalization belonging to:

    https://w3id.org/linkflows/formalization-papers/DataScienceSpecialIssue

with:

    pso:withStatus pso:submitted

Every unique submitted-formalization root in the frozen scope is retained.

Published documentation reports 15 submissions.

That number is a pre-open consistency expectation, not a license to drop or add records.

If graph-derived root count differs from the published expectation:
- preserve the graph-derived count;
- classify the discrepancy;
- do not subset-rescue to 15.

## 5. Project-native relation adapter

Only the following pre-registered relations are used for the primary prospective study.

### R1 REVIEW_REFERS_TO_FORMALIZATION

Native structure:

    ReviewComment
    lf:refersTo
    submitted formalization

Target:
    formalization object/claim nanopublication represented by the referred object.

### R2 UPDATE_OF_FORMALIZATION

Native structure:

    update nanopublication
    lf:isUpdateOf
    submitted formalization

Target:
    submitted formalization.

### R3 RESPONSE_TO_REVIEW

Native structure:

    response comment
    lf:isResponseTo
    review nanopublication

Target:
    review nanopublication.

### R4 RESPONSE_REFERS_TO_UPDATE

Native structure:

    response comment
    lf:refersTo
    updated formalization nanopublication

Target:
    updated formalization nanopublication.

### R5 DECISION_STATUS_OF_UPDATE

Native structure:

    decision nanopublication assertion
    updated formalization
    pso:withStatus
    decision status

Target:
    updated formalization.

### R6 SUPERSEDES

Native structure:

    new nanopublication
    npx:supersedes
    old nanopublication

Target:
    earlier nanopublication.

### R7 RETRACTS

Native structure:

    retraction nanopublication
    npx:retracts
    target nanopublication

Target:
    retracted nanopublication.

No relation is inferred from record text.

## 6. Scholarly state

For one submitted-formalization root, scholarly state S contains:

### Current formalization layer
- root submission identity;
- current formalization/update identity;
- current publication status if present.

### Live scholarly acts
- registered review identities targeting the formalization;
- response identities targeting reviews and updates;
- update identities;
- decision identities.

### History H
- immutable nanopublication IDs;
- relation-target edges;
- supersession/retraction edges;
- creator/provenance information;
- publication/version information available in the frozen source.

The state is target-bound. An act cannot be admitted merely because it belongs to the same
submission bundle.

## 7. Generator vocabulary

The prospective study uses four bounded generators:

    RECORD_REVIEW
    REPLACE_FORMALIZATION
    RECORD_RESPONSE
    REVISE_PUBLICATION_STATUS

and one exclusion action:

    RETRACT_TARGET

Interpretation:

### RECORD_REVIEW
Register a review relation against the currently live formalization.
Current formalization assertion may remain unchanged; H changes.

### REPLACE_FORMALIZATION
Replace the current formalization version with the native update targeted to the prior submitted
formalization.

### RECORD_RESPONSE
Register an author response only when:
- the targeted review is already live/retained;
- the response's referred update is the current or retained update target;
- relation-target identity is resolvable from H.

This is assertion-layer identity for the formalization but history nonidentity.

### REVISE_PUBLICATION_STATUS
Apply the decision status to the exact updated formalization targeted by the decision relation.

### RETRACT_TARGET
Remove/inactivate the targeted nanopublication from live qualification while retaining the
retraction history.

The generator label is never taken from file names or hand-coded per episode.

## 8. Qualification relation

Write:

    Q(S, rho, target(rho), H, e, g)

Primary rules:

### REVIEW_REFERS_TO_FORMALIZATION
If target is the currently live formalization:

    g = RECORD_REVIEW

Else:
    reject RELATION_TARGET_NOT_LIVE

### UPDATE_OF_FORMALIZATION
If target is the root/current predecessor formalization and update identity is not retracted:

    g = REPLACE_FORMALIZATION

Else:
    reject UPDATE_TARGET_UNRESOLVED

### RESPONSE_TO_REVIEW + RESPONSE_REFERS_TO_UPDATE
Both bindings are required.

If:
- targeted review exists in H;
- referred update exists in H;
- referred update is the current formalization or a retained direct update of the root;
- response is not retracted;

then:

    g = RECORD_RESPONSE

Otherwise reject one of:
- RESPONSE_REVIEW_TARGET_NOT_LIVE
- RESPONSE_UPDATE_TARGET_NOT_LIVE
- RESPONSE_TARGET_HISTORY_UNRESOLVED

### DECISION_STATUS_OF_UPDATE
If decision target is the current exact update:

    g = REVISE_PUBLICATION_STATUS

Else:
    reject DECISION_TARGET_NOT_CURRENT

### SUPERSEDES
Used to canonicalize native nanopublication versions, not as an additional substantive generator
when it only replaces a nanopublication package representing the same act.

The latest non-retracted superseding version of an act is the live version.
All earlier versions remain in H.

### RETRACTS
If exact target exists in live state/history:

    g = RETRACT_TARGET

Else:
    reject RETRACTION_TARGET_UNKNOWN

## 9. Registered multi-step trajectory grammar

For each submission root, derive all relations first and classify the whole root without
post-opening selection.

### T0 COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION

Required connected graph:

    F0 <-R- Review
    F0 <-isUpdateOf- U
    Review <-isResponseTo- Response
    Response -refersTo-> U
    U <-status- Decision

The exact native direction of RDF predicates is retained; the diagram expresses semantic target
binding only.

Registered generator sequence in source-time order:

    RECORD_REVIEW
    REPLACE_FORMALIZATION
    RECORD_RESPONSE
    REVISE_PUBLICATION_STATUS

if timestamps/order support that sequence.

### T1 REVIEW_UPDATE_RESPONSE_NO_DECISION

Same as T0 without decision.

### T2 REVIEW_UPDATE_NO_RESPONSE

Review + update exist but no connected response.

### T3 REVIEW_ONLY

Review exists, no update.

### T4 UPDATE_WITHOUT_CONNECTED_REVIEW

Update exists but no review relation connected to the root.

### T5 DECISION_WITHOUT_CONNECTED_RESPONSE

Decision exists for update but no connected response chain.

### T6 ROOT_ONLY

Submitted root has none of the registered later relations.

### T7 RETRACTED_OR_SUPERSEDED_ONLY

Only relation activity is version/retraction maintenance with no registered scholarly review
trajectory.

### T8 AMBIGUOUS_OR_NONFUNCTIONAL_TARGET

Any required relation has:
- multiple incompatible targets;
- missing target identity;
- target outside the root trajectory;
- unresolved supersession/retraction status.

### T9 PARSE_OR_CONTRACT_INVALID

Record cannot be safely interpreted under the frozen adapter.

Every population root gets exactly one primary trajectory disposition.

Priority for conflicting categories:

    T9 > T8 > T0 > T1 > T2 > T5 > T4 > T3 > T7 > T6

This priority is frozen before record opening.

## 10. Primary confirmatory denominator

Primary substantive composition denominator:

    all roots classified T0 or T1

These are complete enough to test:
- review target;
- update target;
- response target to both review and update;
- sequential qualified composition.

T0 additionally tests decision/status qualification.

Other categories remain in the full population accounting and are never discarded.

No prevalence claim is made unless explicitly denominator-bounded to the frozen population.

## 11. Primary prospective tests

For every T0/T1 root:

### P1 Target-bound forward execution
Execute relations in their project-supported chronological order.

Require each step to qualify without supplied operation labels.

### P2 Response-before-review counterfactual
Attempt the exact response before its targeted review exists.

Require:

    reject RESPONSE_REVIEW_TARGET_NOT_LIVE

### P3 Response-before-update counterfactual
Attempt the exact response before its referred update exists.

Require:

    reject RESPONSE_UPDATE_TARGET_NOT_LIVE

### P4 History ablation
Construct a state with the same current formalization/update identity but remove the review
transition/history needed to bind the response.

Require:

    current formalization projection identical

but:

    response qualification fails
    RESPONSE_TARGET_HISTORY_UNRESOLVED
    or RESPONSE_REVIEW_TARGET_NOT_LIVE

### P5 Decision-before-update counterfactual
For T0:

Attempt the exact decision before the targeted update is current.

Require:

    reject DECISION_TARGET_NOT_CURRENT

### P6 Wrong-target injection
Replace one relation target with a foreign valid nanopublication from another population root.

Require rejection before mutation.

### P7 Retraction/supersession discipline
A retracted target cannot remain live merely because an older edge refers to it.
Superseded package versions cannot be double-counted as distinct acts.

## 12. State-dependent composition criterion

Primary prospective success does NOT require the same relation type to select two different
generator labels under two states.

That stronger phenomenon was already demonstrated structurally.

For this independent ecology, the required confirmation is:

> later generator availability depends on prior target-bound acts/history.

Specifically, response qualification must differ between:
- a state containing the targeted review/update history;
- a state with the same current update but the required target/history removed.

Thus:

    Psi_current equal

but:

    Gamma_response different

is the load-bearing prospective composition criterion.

## 13. Null/history semantics

RECORD_REVIEW and RECORD_RESPONSE may leave the current formalization content/version unchanged.

They are NOT null actions.

They are:

    FORMALIZATION_STATE_IDENTITY
    + SCHOLARLY_HISTORY_NONIDENTITY

This is the cross-ecology analogue of RECORD_EVIDENCE.

## 14. Independent extraction requirement

Two independent implementations must derive the registered relation graph.

Preferred:

### Oracle
RDFLib parse of the frozen RDF/TriG records.

### Runtime
A second independent RDF engine/library, preferably pyoxigraph, reading the same bytes.

Do not hand-roll a partial TriG grammar if a mature independent parser can be installed and
synthetically verified before opening records.

Both implementations must independently derive:
- population roots;
- live/superseded/retracted nanopublication identities;
- review targets;
- update targets;
- response review/update targets;
- decision targets/status;
- provenance/time ordering used by the trajectory engine.

Exact agreement is required on the registered scientific graph surface.

## 15. Synthetic gate

Before DATA_OPEN, synthetic RDF fixtures must cover:

1. complete T0 chain;
2. T1 chain without decision;
3. review-only;
4. update without review;
5. response with missing review target;
6. response with missing update target;
7. decision with wrong update target;
8. superseded review version;
9. retracted response;
10. duplicate/multiple review targets;
11. cross-root wrong target;
12. same-current-update history ablation;
13. timestamp/order ambiguity.

Both parsers and both qualification engines must agree on all fixtures.

## 16. PRE_DATA / DATA_OPEN boundary

### PRE_DATA
Allowed:
- dependency installation;
- compilation;
- frozen commit/release verification;
- generic ontology/query-script blob verification;
- synthetic fixtures;
- oracle/runtime parser comparison on synthetic RDF;
- qualification/composition synthetic gates.

No candidate record/index opening.

Failures are:

    PRE_DATA_ABORT

and recoverable if scientific contracts remain unchanged.

### DATA_OPEN
Immediately before first record/index access:
- write immutable DATA_OPEN_EVENT metadata;
- record Git SHA;
- record frozen external source anchors;
- record scientific engine blob hashes.

The first opening/dereference of candidate record data consumes freshness.

## 17. Outcome categories

### INVALID
Any:
- incomplete population accounting;
- parser disagreement;
- contract mismatch;
- unresolved source snapshot;
- qualification disagreement;
- documentary source audit failure.

### NULL_APPLICABILITY
No roots expose any registered connected review/update trajectory.

### BOUNDED_PARTIAL
Connected trajectories exist, but:
- no T0/T1 roots;
- or one registered prospective counterfactual is structurally unsupported for all eligible
  roots.

### PASS
At least one T0/T1 root exists and for every T0/T1 root:
- oracle/runtime exact;
- target-bound forward sequence executes;
- response-before-review rejects;
- response-before-update rejects;
- history ablation changes response availability while current update projection is held fixed;
- wrong-target injection rejects;
- retraction/supersession discipline passes;
- T0 decision-before-update rejects.

All non-T0/T1 roots remain fully accounted.

## 18. Claim ceiling

If PASS:

> In an independent semantic-publishing ecology, prospectively registered review/update/response
> chains require stable relation targets and retained scholarly history: the same current updated
> formalization can differ in whether a later response is lawfully interpretable depending on
> whether the review/update history it targets is retained.

Not licensed:
- universal scholarly action algebra;
- prevalence outside the frozen field-study population;
- automatic interpretation of review text;
- causal claims about acceptance;
- quality judgments about authors/reviewers;
- claim-level semantic agreement with the paper content itself.
