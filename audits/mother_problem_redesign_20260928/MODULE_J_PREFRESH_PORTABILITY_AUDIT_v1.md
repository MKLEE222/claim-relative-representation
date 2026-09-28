# Pre-fresh portability audit — Module J object/claim contract

Date: 2026-09-28
Status: FROZEN CODE-AUDIT FINDING BEFORE ANY NEW INDEPENDENT EPISODE CORPUS IS OPENED.

## 1. Scope

This audit compares the final documented Module J object grammar against the actual frozen Module J / inherited Module I implementation.

No new independent candidate episode XML was opened to obtain these findings. The findings arise from:
- the already frozen Module J contracts;
- the already exposed/synthetic J test suite;
- direct inspection of the project code;
- project-level encoding documentation used only for prospective candidate screening.

Module K remains unchanged and authoritative at NULL_APPLICABILITY.

## 2. Finding P1 — direct explicit letter route is not implemented as documented

Final documented grammar describes Route A as a unique explicit non-annex:

    div type="letter"

However both frozen Module J object selectors first search for:

    div type="transcription"

If no transcription exists, they skip explicit-letter selection and enter the Route-C-style direct-div branch.

That branch currently accepts any sole direct div with:
- one correspDesc;
- at least one sent action;
- at least one letter structural marker.

It does not require that the direct div be untyped.

Consequences:

1. a direct body child div type="letter" can be accepted but mislabeled:

       UNTYPED_BODY_LETTER

2. the implementation therefore does not implement the final A/B/C grammar literally;

3. F10-F16 contain no control for a direct explicit letter outside a transcription wrapper.

This mismatch must be repaired before a new independent holdout.

## 3. Finding P2 — temporal text-carrier extraction uses an older, narrower primary selector

The inherited Module I runtime chooses the primary textual letter only under a transcription container.

Therefore, even when Module J later accepts a no-transcription object through its own object gate, inherited dateline extraction may still see:

    primary = None

and omit text-internal dateline claims.

The Module J wrapper subsequently rekeys the claims returned by Module I but does not reconstruct dateline claims from the Module-J-selected boundary.

Thus:

    object accepted by J
    !=
    text carriers necessarily extracted from the same J object boundary

This is a contract/implementation gap.

## 4. Finding P3 — file-level admissibility is object-gated but not claim-boundary audited

After Module J establishes one primary object, it rekeys all inherited root claims and the origin claim to the selected object_id.

This is appropriate for file-level metadata only under the documented single-object applicability assumption.

But the implementation does not store, for each temporal claim, an explicit proof class such as:

- FILE_LEVEL_APPLIES_BY_UNIQUE_OBJECT;
- INSIDE_SELECTED_OBJECT_BOUNDARY;
- OUTSIDE_SELECTED_OBJECT_BOUNDARY;
- ANNEX_EXCLUDED.

As a result, a future multi-div encoding ecology could silently rely on the unique-file-object assumption even when a textual date lies outside the selected boundary.

A new independent holdout must not depend on this implicit rebinding.

## 5. Finding P4 — source identity is DAHN-specific

The frozen J runtime/oracle inherit or hard-code the DAHN source commit:

    e7d4a81d42ea10a3d672e5c0869f033a8c2c8149

Object IDs and evidence handles include that source-version value.

This is correct for Modules I-K, all of which use the frozen DAHN source.

It is not portable to a genuinely independent project.

A cross-project confirmatory engine must accept a frozen source context:

    source_repository
    source_version
    population_prefix/register

before data opening.

Changing only the input files while retaining the DAHN source-version label would be scientifically invalid.

## 6. Finding P5 — the existing hardening suite does not test cross-project portability obligations

F10-F16 cover:
- no-primary aggregate rejection;
- multiple primary letters under transcription;
- cross-object injection;
- transcription-as-letter;
- multiple transcriptions;
- untyped body letter;
- placeholder rejection.

They do not cover:

- direct explicit letter under body without transcription;
- typed direct div incorrectly entering Route C;
- selected-boundary dateline extraction outside a transcription wrapper;
- temporal date outside the selected boundary;
- source-context mismatch;
- multi-div object-closure ambiguity.

These become mandatory pre-fresh tests.

## 7. Scientific disposition

Do not modify or reinterpret Modules J/K retrospectively.

For the next independent study:

1. create a new engine version rather than overwriting J;
2. implement the documented A/B/C grammar literally;
3. make selected-object boundary the authority for text-internal temporal claims;
4. attach an applicability proof to every temporal claim;
5. parameterize/freeze source repository and version;
6. add portability fault/positive controls before any candidate episode corpus is opened;
7. rerun Berlin/Paul/StaBi only as exposed regression data;
8. only after those checks pass may a separately frozen independent holdout be opened.

## 8. Candidate implications known before opening

Prospective project-level documentation already shows why this matters:

- a project may encode a whole letter as text type="letter" with writing-session divs;
- a project may encode one direct div type="letter" per file;
- a project may split one physical letter across letter/continuation/address sibling divs.

These are schema-level facts, not observed holdout outcomes.

The next confirmatory population must either:
- be demonstrably compatible with the repaired closed-object grammar before episode opening; or
- be rejected prospectively.

No target-project-specific Route D is permitted after opening.
