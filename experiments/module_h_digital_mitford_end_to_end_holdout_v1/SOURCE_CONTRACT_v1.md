# Module H source/evaluator contract v1

Date: 2026-09-28
Status: FROZEN AFTER H0 AGGREGATE POPULATION FREEZE, BEFORE R* OR ABLATION EXECUTION.

## 1. H0 authority

Authoritative population run:
36385026285

Artifact:
module-h0-digital-mitford-population-v1

Artifact ID:
10954236686

Artifact ZIP SHA-256:
53a704f81eba101d639ebd0fafed1aa772d4c274f18774ad9482964c9a923406

Population JSON SHA-256:
7944aac0d711c1b3d9f2bc09cfd3662fa79bafb5f5ed2faecdb274af9dd80613

H0 aggregates:
- T0 checklist lines: 258
- T1: 365
- T2: 362
- T3: 357
- all eligible person episodes: 218
- clean confirmatory eligible episodes: 214
- post-freeze accidental-exposure eligible episodes: 4
- clean first appearance T0/T1 is inherited from the frozen population extraction
- clean T3 status: OPEN 144, ABSENT 43, RESOLVED 27

No item-level H0 artifact was manually inspected before this contract.

## 2. Journal access representation

The frozen Journal source contains malformed outer XML in some checkpoints.

The source bytes remain immutable.

Person mentions are extracted only from complete literal:

    <persName ...>...</persName>

fragments.

Retained source locator:
- raw character start/end;
- document-order ordinal;
- frozen commit/blob.

No recovered XML tree is used for Journal person evidence.

## 3. Site Index representation

The frozen Site Index is strict-parsed TEI/XML.

Person records retain:
- xml:id;
- all descendant persName strings;
- all note strings;
- all explicit ref attributes inside the person entry;
- element path within the frozen Site Index;
- frozen commit/blob.

Comments/processing instructions are ignored as structural nodes but their source bytes remain unchanged.

## 4. Global person-surface normalization

For source matching and candidate keys:

1. Unicode NFC;
2. casefold;
3. decode XML entities for Journal raw fragments;
4. collapse whitespace;
5. strip leading/trailing punctuation;
6. tokenize on whitespace and punctuation except apostrophe/hyphen inside a token.

Frozen honorific set:

    mr
    mrs
    miss
    ms
    sir
    lady
    lord
    dr
    rev

A core-name token sequence removes only those honorific tokens.

No fuzzy edit distance, phonetic matching, external alias table, or post-outcome spelling repair is permitted.

## 5. Candidate identity keys

For a Journal person mention m:

### Exact surface key

    CORE(m)

after the normalization above.

### Surname key

If CORE(m) is nonempty:

    LAST_TOKEN(CORE(m))

A Site Index person is a lexical candidate when any normalized current persName:

- has CORE exactly equal to CORE(m); OR
- has the same last core token as m.

The exact-surface relation is recorded separately from surname-only relation.

No candidate is removed because it looks implausible.

## 6. Name compatibility for Q5

For a Journal mention with an existing ref target:

CompatibleName(m,target)=1 iff at least one non-honorific source token of length >= 2 occurs in at least one normalized target persName token set.

If the Site Index explicitly contains the exact Journal surface as any persName/addName string, compatibility is also true.

This rule is lexical and may generate false mismatches for nicknames; those are retained as holdout outcomes.

## 7. Frozen uncertainty detector

Use exactly the phrases frozen in PROTOCOL.md:

- possibly
- may be
- might be
- probably
- presumably
- unknown
- unidentified
- not sure
- unclear
- more research needed
- check

Also flag a literal question mark within a current person-entry note.

Matching is case-insensitive after NFC/whitespace normalization.

Do not add phrases after outcome.

## 8. R* discovery records

Journal mentions are grouped by:

1. ref ID when present;
2. otherwise normalized exact source surface.

For every group, generate zero or more frozen triggers:

Q1 MISSING_TARGET:
at least one ref in the group is absent from current Site Index.

Q2 EXPLICIT_UNCERTAINTY:
the current matched/ref target Site Index person contains a frozen uncertainty marker.

Q3 CANDIDATE_COLLISION:
the union of lexical current Site Index candidates contains more than one ID and no unique existing ref resolves the group.

Q4 REFERENCE_INCONSISTENCY:
the same exact normalized Journal surface is bound to more than one non-null ref ID in the current Journal.

Q5 STATE_NAME_MISMATCH:
an existing ref target fails the frozen compatibility rule.

A live generated question record contains:
- trigger set;
- Journal source mention locators;
- source surface(s);
- ref IDs;
- candidate Site Index IDs;
- current Site Index evidence records;
- source/version provenance.

## 9. R* warrant state

For each source-bound question group:

### SOURCE_INCOMPATIBLE

if its non-null ref target is absent or an existing ref target fails Q5.

### AMBIGUOUS

if:
- Q3 or Q4 is active; OR
- Q2 is active and the evidence does not independently eliminate all alternatives.

Candidate set is the current candidate IDs plus any distinct current ref IDs.

### RESOLVED_TO_ID(id)

only if:
- exactly one current existing ref ID is used consistently across the group; OR
- there is no ref but exactly one exact-surface Site Index candidate;
- Q1/Q3/Q4/Q5 are false;
- no Q2 uncertainty marker remains on the relevant identity proposition.

### UNRESOLVED

otherwise.

The evaluator never turns a human checkmark directly into this warrant state.

## 10. Gold-to-source matching

Gold remains evaluator-only.

At each checkpoint, a live gold episode is matched to generated source questions using the same mechanical H0 source-match procedure.

A generated question matches a gold episode iff at least one of these holds:

- non-null entity ID overlap;
- exact normalized Journal surface overlap;
- exact normalized Site Index person-name overlap.

Surname-only overlap is insufficient for a gold match.

If one gold episode maps to multiple generated question groups, detection counts as present but source-bound exactness is false unless one group is uniquely compatible under exact ID/surface matching.

## 11. Discovery metrics

Report both:

### Checklist precision

generated questions matching at least one currently OPEN clean gold episode / all generated questions.

The checklist may not be exhaustive; this is explicitly labeled checklist precision.

### Source-licensed rate

fraction of generated questions satisfying at least one frozen Q1-Q5 condition with an auditable source span.

By construction this should be 1 unless implementation inconsistency occurs.

Primary mother-problem discovery emphasis is:
- clean gold recall;
- first-detection latency;
- unsupported/source-unbound question count.

## 12. Gold resolution materialization

For a clean episode whose hidden gold becomes RESOLVED:

1. parse explicit mapping text only with the phrase family frozen in PROTOCOL.md;
2. if a target ID/name can be extracted and mechanically mapped to current Journal/Site Index state, compare R* warrant;
3. if no explicit mapping is parseable, evaluate only whether R* changes from live unresolved/ambiguous to a single source-supported identity/relationship by or before the human resolved checkpoint;
4. a human RESOLVED state without source-compatible materialization is:

       EDITOR_RESOLVED_BUT_SOURCE_NOT_MATERIALIZED

and does not count as a warrant error for safe abstention.

## 13. Null event

For an episode between adjacent checkpoints, the interval is a null event only when:
- gold status is unchanged;
- all exact source-bound Journal mention records used by R* are unchanged in surface/ref;
- the matched Site Index person record relevant to the episode is unchanged in names, notes and explicit person refs.

A null event must not change R* warrant state.

## 14. R_NO_HISTORY

At each checkpoint use the exact same current R* extraction and warrant rule, but discard all earlier episode state.

For delayed reuse, R_NO_HISTORY may use only T3 current source.

R* may use the accumulated last warranted state and unresolved alternatives when the T3 current mention/source is insufficient or absent.

## 15. R_REF_ONLY

Retain:
- Journal surface;
- ref;
- ref-target existence;
- current canonical names.

Ignore:
- uncertainty notes;
- alternative ledger beyond exact current target existence;
- person-person refs;
- history.

Warrant:
- existing unique ref -> RESOLVED_TO_ID;
- absent ref target -> SOURCE_INCOMPATIBLE;
- no ref + exactly one exact-surface name candidate -> RESOLVED_TO_ID;
- otherwise UNRESOLVED.

Discovery:
- Q1 only;
- Q4 from conflicting refs;
- Q5 by name compatibility.

Q2 and Q3 are unavailable.

## 16. R_TEXT

R_TEXT has no person/entity markup or IDs.

To avoid importing an external NER model after holdout freeze, Module H v1 does not infer person spans from flattened text.

Disposition for addressable person-question generation:

    OPERATION_UNSUPPORTED_WITHOUT_DECLARED_NER

R_TEXT therefore produces no source-bound person-identity questions in the primary metric.

This is an operation-support ablation, not evidence that raw text can never support prosopographic discovery with an added NER/linking system.

## 17. Delayed reuse

For clean episodes with at least two exact source-bound Journal mention occurrences over the frozen horizon:

- earliest source occurrence is trigger;
- latest distinct occurrence is delayed query.

R* answer:
- most recent warranted resolved identity if later evidence does not defeat it;
- otherwise most recent retained ambiguous/unresolved state.

R_NO_HISTORY answer:
- T3 current-source warrant only.

Gold comparison uses source-materialized T3 state, not checklist wording alone.

## 18. Statistical/claim discipline

The 214 clean episodes are not independent human subjects or independent corpora.

Report:
- finite-population counts;
- per-episode trajectories;
- grouped dependence by shared entity/ref where possible.

No p-values are required for the primary claim.

Do not call R* globally minimal.

## 19. Stop rule

After this contract:
- no normalization changes;
- no new uncertainty phrases;
- no new discovery triggers;
- no external NER;
- no fuzzy identity matching;
- no external authority dereferencing;
- no item-specific mapping rule;
- no checkpoint change.

Any implementation defect before output must be separately documented.
