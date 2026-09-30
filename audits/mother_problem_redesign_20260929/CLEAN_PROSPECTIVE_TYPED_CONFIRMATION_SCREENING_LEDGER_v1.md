# Clean prospective typed-confirmation screening ledger v1

Date: 2026-09-30
Status: ACTIVE DOCUMENTATION-ONLY SCREENING.

Governing protocol:

    CLEAN_PROSPECTIVE_TYPED_CONFIRMATION_SCREENING_PROTOCOL_v1.md

No candidate record/article/review payload has been opened under this ledger.

## Candidate A — TMLR / OpenReview journal workflow

Documentation inspected:
- openreview/openreview-py generic journal workflow code at commit
  d8fc46bfbdfeb34aa78854f60629a627bdecc3ba;
- generic OpenReview API documentation embedded in the repository;
- TMLR generic/example configuration in the same codebase.

Record-level TMLR content opened:

    no

### Structural strengths

Stable object/relation identities:
- submission Note IDs;
- forum root;
- replyto exact parent Note;
- immutable true creation time tcdate;
- note edit history;
- per-paper Review / Rating / Decision invitations.

Connected workflow:
- submission/revision;
- reviews;
- reviewer-quality ratings by AE;
- decision.

Source-native history-dependent gate:

    review_rating_process.py

retrieves the submission with replies, counts:
- Review notes;
- Rating notes;

and creates the Decision invitation only if:

    len(reviews) == len(ratings)

Each rating invitation is created with:

    replytoId = exact review.id

so the internal decision-enabling history is target-bound.

### Public-auditability failure

The generic journal rating invitation sets Rating note readers to:

    Editors_In_Chief
    Action_Editors

and explicitly excludes authors.

The public/anonymous researcher therefore cannot in general reconstruct the review-rating history
that internally enables Decision.

The later released decision may be public, but this does not expose the private qualifying history.

Using:
- eventual decision presence;
- decision timestamp;
- submission status

as a proxy would replace the missing Kappa history with an outcome-derived surrogate and is not
authorized.

### Gate disposition

G1 independent ecology:
    PASS

G2 stable object/exact relation target:
    PASS

G3 source-native relation semantics:
    PASS

G4 connected multi-step structure:
    PASS

G5 publicly auditable Beta(g):
    PASS / BOUNDED
    public review/reply/submission bindings are available structurally.

G6 publicly auditable Kappa(g):
    FAIL
    the decisive rating-history state for Decision is private to editorial roles.

G7 signature heterogeneity:
    STRUCTURALLY PLAUSIBLE BUT NOT PUBLICLY AUDITABLE
    submission revision is a plausible history-not-required action;
    Decision is internally history-required;
    the latter cannot be reconstructed publicly.

G8 closed denominator:
    PASS IN PRINCIPLE
    TMLR/-/Submission plus immutable tcdate and get_all_notes permit an outcome-blind natural
    time-window denominator.

G9 independent extraction/audit feasibility:
    FAIL FOR THE CLAIMED HISTORY-REQUIRED ACTION
    a public documentary auditor cannot inspect the private rating history.

G10 exact-path pre-data feasibility:
    NOT REACHED

Screening disposition:

    SCREEN_FAIL_PUBLIC_HISTORY_UNOBSERVABLE

Freshness status:

    RECORD_LEVEL_UNOPENED

Scientific interpretation:

> OpenReview/TMLR is evidence that platform execution state and externally researchable scholarly
> history can diverge. That makes it conceptually relevant to the mother problem, but unsuitable
> as the clean prospective confirmation ecology because the decisive Kappa history cannot be
> independently reconstructed from the public source.

No TMLR record query or DATA_OPEN is authorized.


## Candidate B — eLife Reviewed Preprints / immutable JATS XML

Documentation/schema inspected only:
- eLife public peer-review model documentation;
- elifesciences/elife-article-xml README/tree metadata;
- article-xml commit:
  ec0fbc8e81cfae472260f96a03ba078b57007612;
- article-xml tree:
  d6bba934b495f7e4272f370de53817c0fc28af84;
- elifesciences/eLife-JATS-schematron Reviewed Preprint schema at:
  4c2359460359160b3e02c98fc07804b304627bb7;
- elifesciences/data-hub-api DocMap model/code at:
  2515b474a449e79932acd7d8805c96ec1b2daaa5.

Record-level eLife preprint XML opened:

    no

Only repository tree metadata/filenames/sizes were inspected.

### Source-native structural model

The public eLife model defines a Reviewed Preprint as including:
- the preprint/version;
- eLife Assessment;
- one or more Public Reviews;
- Author Response when available.

Revised Reviewed Preprints publish a new version and may update the eLife Assessment and Public
Reviews.

The public DocMap model independently represents:
- ordered steps with previous-step / next-step;
- versionIdentifier;
- preprint inputs;
- evaluation outputs;
- evaluation types:
    evaluation-summary
    review-article
    reply;
- version-specific evaluation inputs to manuscript publication.

The public JATS Reviewed Preprint schema independently requires:
- exactly one eLife Assessment sub-article:
    article-type = editor-report;
- at least one Public Review sub-article:
    article-type = referee-report;
- no more than one Author Response:
    article-type = author-comment;
- version-specific reviewed-preprint DOI;
- version-specific peer-review sub-article DOI;
- publication-history events with direct self-uri links to the version's:
    reviewed-preprint
    editor-report
    referee-report
    author-comment when present.

The schema requires each peer-review sub-article DOI to begin with the exact Reviewed Preprint
version DOI.

Thus exact version-target binding and retained evaluation history are publicly encoded in the
immutable XML itself.

### Prospective action families

Candidate history-not-required generator:

    RECORD_EVALUATION

Beta:
- exact manuscript/version DOI;
- evaluation sub-article DOI whose prefix binds it to that exact version;
- evaluation kind.

Kappa:
- current target Reviewed Preprint version exists.

Retained earlier transition history is not required merely to register a version-bound Public
Review/eLife Assessment/Author Response.

Candidate history-required generator:

    PUBLISH_REVIEWED_PREPRINT

Beta:
- exact Reviewed Preprint version DOI;
- exact publication-history event for that version.

Kappa:
- eLife Assessment retained;
- at least one Public Review retained;
- publication-history event retains the direct Assessment/Review bindings for that version.

A state retaining the same current manuscript/version projection but erasing those evaluation
bindings is not sufficient for this generator.

This gives a natural connected sequence:

    RECORD_EVALUATION*
    -> PUBLISH_REVIEWED_PREPRINT

and, for later versions:

    prior reviewed version
    -> RECORD_EVALUATION*
    -> PUBLISH_REVISED_REVIEWED_PREPRINT

### Immutable denominator

Authoritative source candidate:

    elifesciences/elife-article-xml
    commit ec0fbc8e81cfae472260f96a03ba078b57007612

Tree metadata at this commit:
- 9,270 Reviewed Preprint XML files;
- 4,806 manuscript IDs;
- 3,715 manuscripts have more than one version;
- maximum observed version count in tree metadata = 5;
- total preprint XML byte size = 1,597,080,287.

To avoid a 1.6 GB fresh execution path while preserving outcome blindness, the candidate-specific
scope will use the deterministic manuscript rule:

    int(manuscript_id) mod 16 == 0

and include all Reviewed Preprint versions for every selected manuscript.

At the frozen tree this scope is:
- 297 manuscripts;
- 568 XML files;
- 96,584,062 bytes;
- 226 manuscripts have multiple version filenames.

This rule uses only stable manuscript identity and was frozen without opening XML content or
review/evaluation outcomes.

### Gate disposition

G1 independent scholarly ecology:
    PASS

G2 stable object and exact relation target:
    PASS
    version-specific article/sub-article DOI plus publication-history self-uri.

G3 source-native relation semantics:
    PASS
    reviewed-preprint version, assessment, public review, author response and publication event
    are schema-native.

G4 connected multi-step structure:
    PASS

G5 publicly auditable Beta(g):
    PASS
    exact version/evaluation bindings are public JATS.

G6 publicly auditable Kappa(g):
    PASS
    assessment/review/history bindings are public in the immutable XML.

G7 signature heterogeneity:
    PASS PROSPECTIVELY
    RECORD_EVALUATION does not require earlier transition history;
    PUBLISH_REVIEWED_PREPRINT requires retained version-bound evaluation history.

G8 closed denominator:
    PASS
    immutable Git commit plus outcome-blind modulo-16 manuscript scope.

G9 independent extraction/audit feasibility:
    PASS
    lxml tree oracle;
    independent Expat/SAX-style streaming runtime;
    third raw-XML documentary audit.

G10 exact-path pre-data feasibility:
    PASS IN PRINCIPLE
    approximately 96.6 MB source scope and schema-bounded XML surfaces are compatible with the
    prospective master execution contract.

Screening disposition:

    SCREEN_PASS_G1_G10

Freshness status:

    RECORD_CONTENT_UNOPENED

Broad discovery stop rule:

    ACTIVATED

No eLife preprint XML may be opened until the candidate-specific protocol, synthetic coverage
manifest, two independent engines, documentary audit, finalizer and exact-path artifact round-trip
are all frozen and green.
