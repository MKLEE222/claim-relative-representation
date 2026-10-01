# eLife Reviewed Preprints clean prospective confirmation protocol v1

Date frozen: 2026-09-30
Status: CANDIDATE-SPECIFIC PRE_DATA / RECORD CONTENT UNOPENED.

Governing infrastructure:

    PROSPECTIVE_CONFIRMATION_MASTER_EXECUTION_PROTOCOL_v1.md

Governing theory:

    Sigma(g) = (Beta(g), Kappa(g))

## 1. Candidate

Ecology:

    eLife Reviewed Preprints

Authoritative source repository:

    elifesciences/elife-article-xml

Frozen commit:

    ec0fbc8e81cfae472260f96a03ba078b57007612

Frozen tree:

    d6bba934b495f7e4272f370de53817c0fc28af84

Documentation/schema anchors:

    elifesciences/eLife-JATS-schematron
    commit 4c2359460359160b3e02c98fc07804b304627bb7

    elifesciences/data-hub-api
    commit 2515b474a449e79932acd7d8805c96ec1b2daaa5

No eLife preprint XML content was opened before this protocol.

## 2. Frozen denominator

Repository tree metadata at the frozen commit contains:

    9,270 preprint XML files
    4,806 manuscript IDs
    1,597,080,287 total XML bytes

The authoritative study uses the outcome-blind manuscript rule:

    int(manuscript_id) mod 16 == 0

and includes every Reviewed Preprint XML version for every selected manuscript.

Frozen tree accounting for this rule:

    manuscripts      297
    XML files        568
    source bytes     96,584,062

All files matching the rule are included.

No file is removed because:
- it has one version;
- it lacks an author response;
- it has one versus multiple reviews;
- it produces a null/invalid/partial scientific outcome.

## 3. Registered XML surface

The scientific engine reads only:

### Main version identity
- filename manuscript ID;
- filename Reviewed Preprint version;
- article-id pub-id-type=publisher-id;
- article-id pub-id-type=doi specific-use=version;
- article-version article-version-type=preprint-version;
- article-version article-version-type=publication-state.

### Current version evaluation sub-articles
- editor-report;
- referee-report;
- author-comment.

For each registered sub-article:
- article-type;
- front-stub/article-id pub-id-type=doi.

### Publication history
- pub-history/event;
- event-desc;
- date date-type;
- self-uri content-type;
- self-uri xlink:href.

No:
- title;
- abstract;
- body text;
- claims;
- author identity;
- discipline;
- figures;
- references

enter the scientific state.

## 4. Source-native schema facts frozen before opening

The Reviewed Preprint Schematron requires:

1. at least one:
       sub-article article-type=editor-report
   representing the eLife Assessment;

2. at least one:
       sub-article article-type=referee-report
   representing Public Review;

3. no more than one:
       sub-article article-type=author-comment;

4. peer-review sub-article DOI format:
       10.7554/eLife.<msid>.<version>.sa<n>;

5. every peer-review sub-article DOI starts with the exact current Reviewed Preprint version DOI;

6. for a revised Reviewed Preprint version k:
       pub-history contains exactly k - 1
       prior reviewed-preprint publication events;

7. each prior reviewed-preprint publication event contains:
       one reviewed-preprint version DOI link;
       an editor-report DOI link;
       at least one referee-report DOI link;

8. previous reviewed-preprint publication events are ordered by version/date constraints.

These are provider schema requirements, not post-outcome rules.

## 5. Scientific state

For XML version x define state S(x):

    manuscript_id
    rp_version
    version_doi
    preprint_version
    publication_state
    current_assessment_doi
    current_review_dois
    current_author_response_doi?
    prior_publication_events

Each prior publication event retains:

    prior_version_doi
    assessment_doi
    review_dois
    author_response_doi?
    publication_date?

The current scholarly projection Psi contains:

    manuscript_id
    rp_version
    version_doi
    preprint_version
    publication_state

The history projection Xi contains:

    current evaluation bindings
    prior_publication_events

## 6. Registered generators

### G1 REGISTER_PUBLIC_REVIEW

Input:
- one current referee-report sub-article.

Beta:
- exact current version DOI;
- exact review DOI;
- review DOI has current version DOI as prefix;
- type = referee-report.

Kappa:
- current Reviewed Preprint version exists.

Retained prior publication history:

    NOT_REQUIRED_IN_REGISTERED_TASK

### G2 REGISTER_ASSESSMENT

Input:
- current editor-report sub-article.

Beta:
- exact current version DOI;
- exact assessment DOI;
- assessment DOI has current version DOI as prefix;
- type = editor-report.

Kappa:
- current Reviewed Preprint version exists.

Retained prior publication history:

    NOT_REQUIRED_IN_REGISTERED_TASK

### G3 REGISTER_AUTHOR_RESPONSE

Input:
- current author-comment sub-article when present.

Beta:
- exact current version DOI;
- exact author-response DOI;
- response DOI has current version DOI as prefix;
- type = author-comment.

Kappa:
- current Reviewed Preprint version exists.

Retained prior publication history:

    NOT_REQUIRED_IN_REGISTERED_TASK

Absence of an author response is not invalid.

### G4 PUBLISH_REVIEWED_PREPRINT

Applies to rp_version = 1.

Beta:
- exact current Reviewed Preprint version DOI.

Kappa:
- exactly one current eLife Assessment;
- at least one current Public Review.

Prior reviewed-preprint history:

    NOT_APPLICABLE

### G5 PUBLISH_REVISED_REVIEWED_PREPRINT

Applies to rp_version > 1.

Beta:
- exact current Reviewed Preprint version DOI.

Kappa:
- exactly one current eLife Assessment;
- at least one current Public Review;
- exactly rp_version - 1 prior reviewed-preprint publication events;
- prior event version DOIs are exactly versions 1..rp_version-1 for the same manuscript;
- every prior event retains:
    assessment binding;
    at least one Public Review binding.

Retained prior transition history:

    REQUIRED

This is the primary history-required generator.

## 7. Typed qualification signatures

### REGISTER_PUBLIC_REVIEW

Beta:
    VERSION_TARGET_IDENTITY      REQUIRED
    EVALUATION_DOI_IDENTITY      REQUIRED
    EVALUATION_TYPE              REQUIRED

Kappa:
    VERSION_EXISTS               REQUIRED
    PRIOR_PUBLICATION_HISTORY    NOT_REQUIRED

### REGISTER_ASSESSMENT

Beta:
    VERSION_TARGET_IDENTITY      REQUIRED
    EVALUATION_DOI_IDENTITY      REQUIRED
    EVALUATION_TYPE              REQUIRED

Kappa:
    VERSION_EXISTS               REQUIRED
    PRIOR_PUBLICATION_HISTORY    NOT_REQUIRED

### REGISTER_AUTHOR_RESPONSE

Beta:
    VERSION_TARGET_IDENTITY      REQUIRED
    EVALUATION_DOI_IDENTITY      REQUIRED
    EVALUATION_TYPE              REQUIRED

Kappa:
    VERSION_EXISTS               REQUIRED
    PRIOR_PUBLICATION_HISTORY    NOT_REQUIRED

### PUBLISH_REVIEWED_PREPRINT

Beta:
    VERSION_TARGET_IDENTITY      REQUIRED

Kappa:
    CURRENT_ASSESSMENT           REQUIRED
    CURRENT_PUBLIC_REVIEW        REQUIRED

### PUBLISH_REVISED_REVIEWED_PREPRINT

Beta:
    VERSION_TARGET_IDENTITY      REQUIRED

Kappa:
    CURRENT_ASSESSMENT           REQUIRED
    CURRENT_PUBLIC_REVIEW        REQUIRED
    COMPLETE_PRIOR_RP_HISTORY    REQUIRED
    PRIOR_EVENT_ASSESSMENT_BINDING REQUIRED
    PRIOR_EVENT_REVIEW_BINDING   REQUIRED

## 8. Connected composition

For each valid current version:

    REGISTER_ASSESSMENT
    -> REGISTER_PUBLIC_REVIEW*

optionally:

    -> REGISTER_AUTHOR_RESPONSE

then:

    -> PUBLISH_REVIEWED_PREPRINT

or for version > 1:

    -> PUBLISH_REVISED_REVIEWED_PREPRINT

The publication generator reads evaluation/history structures written or retained by earlier
actions.

## 9. Action-relative equivalence

### History-not-required action

For REGISTER_PUBLIC_REVIEW:

Hold fixed:
- current version identity;
- exact review DOI binding.

Compare:
- full prior publication history;
- prior publication history erased.

Required:

    qualification unchanged
    generator unchanged

### History-required action

For PUBLISH_REVISED_REVIEWED_PREPRINT:

Hold fixed:
- Psi current version projection;
- current assessment;
- current reviews.

Compare:
- full prior reviewed-preprint history;
- prior reviewed-preprint history erased.

Required:

    full history -> qualified
    erased history -> rejected

Thus:

    identical current version/evaluation state
    !=
    equivalent future publication availability

for the history-required generator.

## 10. REQUIRED counterfactuals

Registered rejection probes:

1. wrong review DOI version prefix;
2. wrong assessment DOI version prefix;
3. wrong author-response DOI version prefix;
4. missing current assessment;
5. missing all current Public Reviews;
6. revised version missing one prior publication event;
7. revised version with wrong prior manuscript/version DOI;
8. prior publication event missing assessment binding;
9. prior publication event missing all review bindings;
10. filename manuscript/version disagrees with XML identity;
11. rp_version exceeds preprint_version.

No post-open repair category is added.

## 11. NOT_REQUIRED invariance probes

For:
- REGISTER_PUBLIC_REVIEW;
- REGISTER_ASSESSMENT;
- REGISTER_AUTHOR_RESPONSE when present;

erase all prior reviewed-preprint publication events while holding current exact evaluation binding
fixed.

Required:

    selected generator unchanged

## 12. Population dispositions

Every selected XML is assigned exactly one top-level disposition:

    COMPLETE_V1
    COMPLETE_REVISED
    INVALID_IDENTITY
    INVALID_CURRENT_EVALUATION_BINDING
    INVALID_PRIOR_HISTORY
    PARSE_ERROR
    ORACLE_RUNTIME_UNRESOLVED

Author-response absence is not a separate failure.

Complete accounting:

    sum(dispositions) = 568

is mandatory.

## 13. Natural sequence denominator

For each COMPLETE XML:
- every current assessment contributes one REGISTER_ASSESSMENT act;
- every current Public Review contributes one REGISTER_PUBLIC_REVIEW act;
- present Author Response contributes one REGISTER_AUTHOR_RESPONSE act;
- the XML contributes one publication act.

No review/evaluation is dropped by content or sentiment.

## 14. Independent implementations

Oracle:
    lxml.etree tree/XPath-style extraction.

Runtime:
    Python xml.parsers.expat streaming state machine.

Shared:
- string constants;
- result comparison schema;
- frozen filename/scope rule.

Not shared:
- XML extraction logic;
- qualification implementation.

Documentary audit:
    xml.etree.ElementTree independent traversal.

## 15. Synthetic exact-path coverage

Before DATA_OPEN, synthetic_source must include:

- valid v1 with:
    one assessment;
    one review;
    author response absent;

- valid v1 with:
    one assessment;
    multiple reviews;
    author response present;

- valid v2 with:
    complete v1 history;
    current assessment/review;

- valid v3 with:
    complete v1/v2 history;
    current assessment/review;

- missing current assessment;
- missing current reviews;
- wrong review DOI prefix;
- wrong assessment DOI prefix;
- wrong response DOI prefix;
- missing prior version event;
- wrong prior version DOI;
- prior event without assessment link;
- prior event without review link;
- filename/XML identity mismatch fixture;
- rp_version > preprint_version;
- irrelevant nonregistered sub-article.

Coverage trace labels must include every parser/qualification branch used by the authoritative run.

## 16. Scientific pass rule

PASS only if:

1. source accounting exactly matches:
       297 manuscripts
       568 XML files
       96,584,062 bytes;

2. oracle/runtime exact on all 568 files;

3. complete population accounting closes;

4. at least one COMPLETE_REVISED case exists;

5. every natural registered evaluation act qualifies under full representation;

6. every complete publication act qualifies;

7. all applicable REQUIRED counterfactuals reject;

8. all applicable NOT_REQUIRED history ablations preserve evaluation registration;

9. every COMPLETE_REVISED case fails publication qualification under same-current-state prior-history
   ablation;

10. sequence write/read closure passes;

11. documentary audit passes all COMPLETE cases;

12. no natural execution trace lies outside the pre-data synthetic coverage manifest.

## 17. Other dispositions

NULL_APPLICABILITY:
    no COMPLETE XML in the frozen denominator.

BOUNDED_PARTIAL:
    source-valid structures exist but a preregistered scientific condition is naturally
    unavailable without parser/implementation failure.

INVALID:
    any source-accounting, parser, independent-engine, coverage, denominator, documentary-audit or
    finalizer failure.

## 18. Claim ceiling

A clean PASS licenses only:

> In an independently frozen, public, versioned open-peer-review ecology, generator-relative
> qualification signatures prospectively preserve action availability: version-bound evaluation
> registration does not require prior publication history, while publication of revised Reviewed
> Preprints requires retained version-specific evaluation and prior-publication history. The
> distinction survives action-relative equivalence tests and sequence closure under a complete
> outcome-blind denominator.

It does not establish:
- universal scholarly action algebra;
- semantic correctness of review content;
- causal claims about why authors revised scientific claims;
- prevalence outside the frozen eLife scope.
