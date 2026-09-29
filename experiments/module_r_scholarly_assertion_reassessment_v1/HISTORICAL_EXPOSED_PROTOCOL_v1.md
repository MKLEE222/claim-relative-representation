# Module R — Yule-Cordier exposed historical reassessment development protocol v1

Date frozen: 2026-09-29
Status: PRE-EXECUTION EXPOSED DEVELOPMENT PROTOCOL.

## 1. Purpose

Module R has passed encoding-neutral synthetic hardening.

The next step tests whether the same assertion-reassessment distinctions correspond to real,
already source-verified Digital Humanities editorial-history episodes.

This study does NOT consume FRUS or any other fresh candidate.

It uses a historical contrast panel frozen before Module R existed.

## 2. Fixed exposed denominator

The denominator is every row of:

    experiments/deepening_v1/r3_B02_B03_contrast_audit_v1.csv

That file contains exactly five contrast-audited entries:

    YC1920E-0022
    YC1920E-0023
    YC1920E-0024
    YC1920E-0030
    YC1920E-0049

All five rows are retained.

No row is selected or removed according to Module-R outcome.

The source audit marks all five:

    OBJECT_VERIFIED

The panel was created and corrected before any Module-R implementation or result.

## 3. Why this panel is suitable

The pre-existing contrast audit explicitly records:
- earlier target state;
- later candidate label;
- contrast type;
- final diachronic relation;
- source authority.

It also contains both change and non-change cases.

This is essential because Module R must not promote every later scholarly intervention into a
reassessment.

## 4. Registered mapping to Module R

The mapping is a source-grounded abstraction of the already verified contrast relation.

It is NOT a claim that the historical source itself uses Module-R terminology.

### YC1920E-0022 — Sykes route-position revision

Earlier source-grounded state:
- Sykes supports/adopts Yule's Tun-o-Kain route theory.

Later verified contrast:
- 1920 explicitly states that Sykes has since altered his opinion.

Module-R target:

    sykes-route-position-toward-yule

Representation:
- S0 value = YULE_ROUTE_THEORY;
- S0 status = ADOPTED;
- event operation = REVISE_STATUS;
- S1 value remains the identified prior theory;
- S1 status = ALTERED_FROM_PRIOR.

Expected Module-R class:

    R-U3 EVIDENTIAL_STATUS_REVISION

Interpretation ceiling:
the new route position is not invented; only the source-explicit fact that the prior position has
been altered is represented.

### YC1920E-0023 — Tutia comparative evidence, no replacement

Earlier verified state already contains Tutia identification context involving zinc/copper
compounds and collyrium.

Later Parker material adds etymological/Chinese comparative evidence.

The frozen contrast audit classifies it:

    ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT
    ADDITIVE_EVIDENCE|CORROBORATION

and explicitly refuses to call it replacement of the prior identification.

Module-R target:

    tutia-identification-core

Representation:
- S0 core value remains the earlier registered identification state;
- event supplies new evidence/provenance;
- operation reasserts the same task-level value/status.

Expected disposition:

    ADMISSIBLE_NULL_EVENT

This is a natural null against indiscriminate change inflation.

### YC1920E-0024 — Arbre Sec alternative identification

Earlier verified state:
- Arbre Sec is identified as Chinar / Oriental Plane.

Later verified contrast:
- Houtum-Schindler proposes the Cypress of Zoroaster identification;
- Cordier transmits/responds;
- Cordier adoption is NOT established by the inspected entry.

Module-R target:

    arbre-sec-identification

Representation:
- S0 = ORIENTAL_PLANE_CHINAR, status ACCEPTED_EARLIER_IDENTIFICATION;
- event operation = ADD_ALTERNATIVE;
- new assertion = CYPRESS_OF_ZOROASTER, status PROPOSED;
- responsible agent = Houtum-Schindler.

Expected class:

    R-U2 ALTERNATIVE_FORMATION

The existing Plane/Chinar assertion remains live.
The mapping does not encode Cordier as adopter.

### YC1920E-0030 — Pashai source attribution corroboration

Earlier verified state already says:
- Polo likely did not personally visit the countries;
- information was probably derived from Mongol/hearsay material.

The corrected contrast audit classifies the 1920 Stein statement as:

    CORROBORATES_PRIOR
    CORROBORATION|ADDITIVE_EVIDENCE

not ATTRIBUTION_UPDATE.

Module-R target:

    pashai-source-attribution-core

Representation:
- later evidence reasserts the same task-level non-eyewitness/hearsay source-attribution state;
- source/provenance changes;
- Psi does not.

Expected disposition:

    ADMISSIBLE_NULL_EVENT

This is the second natural null.

### YC1920E-0049 — Great Desert source-derivation assignment

Earlier verified state:
- broad comparative folklore context exists;
- no explicit assignment says Polo's desert-spirit account derives from local oral beliefs heard
  on the spot.

Later verified contrast:
- Stein explicitly supplies that source-derivation assignment.

Frozen contrast:

    ADDS_PREVIOUSLY_UNSTATED_ASSIGNMENT
    ATTRIBUTION_UPDATE|CORROBORATION

Module-R target:

    great-desert-polo-source-derivation

Representation:
- S0 = NO_EXPLICIT_ASSIGNMENT, status UNRESOLVED;
- event operation = RESOLVE;
- S1 = LOCAL_FOLKLORE_HEARD_ON_SPOT, status ATTRIBUTED.

Expected class:

    R-U4 RESOLUTION

The broader prior folklore interpretation is not erased.

## 5. Actor / editor responsibility

Historical actor and editor/transmitter roles are not collapsed.

Where the later proposition is attributed to a cited scholar:
- responsible_agent is that scholar;
- Cordier/Yule is not silently substituted as the proposition actor merely because the edition
  transmits the statement.

This preserves the already frozen R3 responsibility discipline.

## 6. Evidence identifiers

The study uses stable pre-existing historical entry IDs as evidence identifiers.

Example:

    evidence_id = YC1920E-0024

The source locator surface records:
- the historical entry ID;
- the relevant earlier target state from the frozen contrast audit;
- OBJECT_VERIFIED authority.

This is sufficient for the controlled representation study.

It is not a replacement for the underlying page-image witnesses.

## 7. Primary tests

For substantive cases:
- oracle/runtime transition class agrees with the pre-registered mapping;
- R1-R8 retained interface pass;
- no collateral target mutation occurs.

For null cases:
- event remains applicable;
- Psi before == Psi after;
- transition class = ADMISSIBLE_NULL_EVENT;
- the event is not counted in the substantive denominator.

## 8. Strong comparator tests

For every substantive case:

B_CURRENT_REOPEN_R must recover:
- current assertion result;
- current provenance.

B_ORDERED_SNAPSHOTS_R must recover:
- S0;
- S1;
- exact state delta;
- current provenance.

B_CHANGE_LOG_NO_JUSTIFICATION_R must recover:
- event identity;
- target;
- exact old/new assertion diff.

The evidence-grounded delayed-audit limitation remains evaluated under the already frozen
comparator information budgets.

## 9. Natural-source grounding audit

The runner must load the pre-existing contrast-audit CSV and verify for every panel row:
- entry ID exists exactly once;
- earlier target state matches the frozen panel record;
- contrast type matches;
- final diachronic relation matches;
- evidence authority == OBJECT_VERIFIED.

A mismatch makes this development study INVALID.

This check validates provenance to the pre-existing source audit.
It is not independent historian adjudication.

## 10. Result categories

### INVALID
Any panel/source-audit mismatch or oracle/runtime disagreement.

### EXPOSED_DEVELOPMENT_PASS
All three substantive episodes satisfy their registered transition classes and R1-R8;
both registered nulls remain null; strong comparator positive capabilities hold.

### EXPOSED_DEVELOPMENT_PARTIAL
The source-audit panel matches, but at least one registered mapping/capability fails.

No result can be promoted to fresh confirmation.

## 11. Claim ceiling

A pass would support:

> Source-verified editorial-history contrasts involving position revision, competing
> identification, and newly assigned source derivation can be represented as distinct scholarly
> reassessment operations while corroborative/additive episodes remain null under the same
> task-level projection.

It would also test whether the state/change/justification separation survives a real historical
DH panel.

It would NOT establish:
- automatic extraction from historical text;
- independent historian agreement;
- fresh external generalization;
- prevalence;
- universal necessity.

FRUS remains unopened throughout this study.
