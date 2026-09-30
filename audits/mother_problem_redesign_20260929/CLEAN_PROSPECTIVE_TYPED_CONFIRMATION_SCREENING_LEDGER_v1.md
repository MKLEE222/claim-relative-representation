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
