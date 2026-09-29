# AMP post-hoc trigger decomposition v1

Date: 2026-09-29
Status: POST-HOC DEVELOPMENT DIAGNOSTIC. DOES NOT CHANGE MODULE O.

## 1. Authority boundary

Authoritative Module O remains:

    NULL_APPLICABILITY

Run:

    36514630882

This diagnostic was executed only after Module O had opened and classified the AMP population.

Successful diagnostic run:

    36514882882

Artifact:

    ID 11010870610
    amp-posthoc-trigger-diagnostic-v1

Artifact ZIP digest:

    sha256:751759fdcd5bbb7da9e4ba7d88216b0553855ac32e1959e6cd3731ba04ced5d0

Diagnostic JSON SHA-256:

    7b0ac9cb287cbad1a7fecd9e2f7de8d282c38b9777e1fead242264cfc0dd74f5

The first diagnostic attempt failed only because of an incorrect repository-root import path.
That script bug was fixed without changing Module O or the diagnostic scientific calculation.

## 2. Accepted scholarly objects

Module O contained:

    48 SINGLE_PRIMARY_DOCUMENT_OBJECT

Among these:

    45 correspondence objects
    3 non-correspondence objects under the parser's correspondence predicate

Active t0 temporal root carrier patterns:

    37 objects: ('sent',) only
    11 objects: no active t0 temporal carrier

No accepted object had two active t0 temporal root carriers.

Therefore the pairwise root eligibility taxonomy is empty:

    no D1 pair
    no D2 pair

This exactly explains:

    primary_discovery_pool = 0

under the frozen Module-I/L discovery contract.

## 3. Later origin evidence

All 48 accepted objects had:

    SINGLE_ORIGIN_ADMISSIBLE

Thus AMP was not missing the later origin/history evidence layer.

Origin relation to the t0 root state:

    10 origin-root pairs: ORIGIN_DISJOINT_ROOT
    27 origin-root pairs: ORIGIN_COMPATIBLE_OR_IDENTICAL
    11 objects: ORIGIN_WITHOUT_ROOT_CLAIMS

At the full internal warrant-object level:

    root_warrant != post_warrant in 48/48

However claim-key/basis replacement alone can make the warrant object unequal.
A second projection therefore removes claim-key/basis identity and compares only the substantive
warrant state.

## 4. Substantive warrant projection

Ignoring claim-key/basis identity and comparing warrant type + represented interval/alternatives:

    substantive warrant change = 21/48
    substantive warrant projection unchanged = 27/48

The 21 substantive changes decompose naturally into:

### A. Disjoint correction / alternative formation

At least 10 accepted objects have:

    t0 root = one exact sent date
    later origin = disjoint date

and the contracted warrant changes from:

    EXACT(sent date)

to:

    ALTERNATIVE_SET(
        origDate,
        sent
    )

Examples include:
- amp-transcript__0001.xml;
- amp-transcript__0005.xml;
- amp-transcript__0007.xml;
- amp-transcript__0012.xml;
- amp-transcript__0014.xml;
- amp-transcript__0019.xml;
- amp-transcript__0021.xml;
- amp-transcript__0024.xml;
- amp-transcript__0032.xml;
- amp-transcript__0033.xml.

These are genuine post-evidence warrant changes under the frozen warrant semantics.

### B. Evidence resolving an initially unresolved state

11 accepted objects have:

    no machine-readable t0 root temporal carrier

but a single admissible origin claim.

Their substantive transition is:

    UNRESOLVED(NO_MACHINE_TEMPORAL_CARRIER)

to a source-grounded post-origin warranted state.

## 5. Why Module O still had zero eligible trajectories

The historical Module-I root task was explicitly narrower than generic update researchability.

Its frozen question was:

    when currently visible current-document date carriers do not uniquely warrant a temporal
    placement, identify the live temporal question, then pursue lawful origin evidence.

Prospective discovery therefore required:

1. at least two t0 root carriers;
2. D1 disjointness or D2 uncertain overlapping non-identity;
3. origDate could not trigger eligibility before OPEN_ORIGIN.

AMP violates condition 1 in every accepted object.

Thus Module O is correctly NULL under its frozen task.

The null must not be repaired by adding an AMP-specific D3 to Module O.

## 6. Scientific consequence

The AMP diagnostic reveals that the dynamic program currently conflates two distinct humanities
inquiry regimes.

### Regime A — ambiguity-triggered inquiry

Visible t0 evidence is already non-unique or conflicting.

Pattern:

    conflicting/qualified current carriers
    -> live question emerges
    -> lawful later evidence acquisition
    -> warrant update

This is the historical D1/D2 Module-I task.

### Regime B — evidence-release-induced revision

The current state may be unique or even unresolved without an explicit dispute.

Later admissible evidence itself creates or changes the scholarly question/warrant.

Pattern:

    apparently determinate or unresolved current state
    -> new source-grounded evidence release
    -> warrant revision / alternative formation / resolution
    -> history/provenance must remain reconstructable

AMP contains development examples of this second regime.

## 7. DH significance

Regime B is not a parser edge case.

It corresponds to familiar digital-humanities/editorial situations in which:
- a later archival identification changes a date;
- a later attribution challenges a previously accepted attribution;
- new provenance changes the status of a source;
- an editorial correction creates alternatives rather than resolving them;
- an initially unknown fact becomes warranted after evidence release.

Therefore researchability under representational change cannot be equated only with the ability
to discover a question from pre-existing ambiguity.

A broader theory must distinguish:

    question emergence from currently visible conflict

from:

    warranted revision caused by newly available evidence.

## 8. Next-study constraint

Do not modify Module O.

A future study may define a separate evidence-release-induced revision task only if:

1. its task/evidence/event contract is frozen independently of AMP outcomes;
2. AMP is used only as exposed development evidence;
3. the new task is first hardened with synthetic controls and exposed regression;
4. a new independent unexposed corpus/ecology is used for prospective confirmation;
5. the same object/applicability/provenance/selectivity/history obligations are retained rather
   than inventing event-specific rescue rules.

The next task should be chosen because it better matches the mother problem and real scholarly
revision practice, not because it makes AMP positive.
