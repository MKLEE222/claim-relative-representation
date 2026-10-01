# Module H v1 — Digital Mitford end-to-end discovery and sustained-warrant holdout

Date frozen: 2026-09-28
Status: PRE-HOLDOUT-INSPECTION PROTOCOL.

## Scientific role

Module H is the prospective end-to-end test for the remaining burden in the mother problem:

    reliable + sustained + warranted + discovery

It is not another local representation-loss experiment.

The same candidate interface must support:

    question emergence
    -> lawful evidence pursuit
    -> unresolved-state persistence
    -> selective resolution/revision
    -> null-event stability
    -> delayed reuse

across T0 -> T1 -> T2 -> T3.

## Sources

Project:
Digital Mitford.

Primary Journal:
DigitalMitford/DM_Journal_1819-1823

Prosopographic state:
DigitalMitford/DM_SiteIndex

Hidden human editorial evaluation:
PossibleMissingSI.md

All commits/blobs and the pre-freeze exposure ledger are frozen in:

    audits/mother_problem_redesign_20260928/FRESH_HOLDOUT_SELECTION_DIGITAL_MITFORD_v1.md

No later source state may replace them.

## Hidden gold

PossibleMissingSI.md is evaluator-only.

It is never exposed to:
- the candidate interface;
- any ablation;
- the question generator;
- the update policy.

The primary discovery metric therefore compares source-generated live questions against a pre-existing human editorial research log that was not produced by the tested system.

## Confirmatory population

The evaluator parses every Markdown checklist line from the four frozen gold blobs.

A stable key is formed from the normalized checklist text before the first "::":
- remove checkbox syntax;
- Unicode NFC;
- collapse whitespace;
- casefold;
- preserve IDs/names;
- keep duplicate keys separate by source-order ordinal.

An eligible discovery episode must:

1. first appear at T0, T1 or T2 as unchecked [ ];
2. concern a PERSON identity/reference/relationship question;
3. mechanically match at least one current Journal persName occurrence OR one current Site Index person entry;
4. not match the pre-freeze exposure ledger;
5. not be a pure schema/template/formatting instruction.

Person classification is mechanical:
- Journal match must be a persName;
- Site Index match must be a person entry.

Every eligible item remains in the denominator even if later unresolved, deleted, malformed, source-incompatible or untrackable.

## Gold trajectory

For each eligible item at every checkpoint:

- OPEN: unchecked;
- RESOLVED: checked;
- ABSENT: stable key absent;
- AMBIGUOUS_GOLD_MATCH: tracking is not unique.

For RESOLVED items the evaluator mechanically parses explicit mapping phrases such as:

- correct to
- changed to
- same as
- already in SI as
- should be
- this is
- renamed to

A checked item with no parseable mapping is RESOLVED_BY_EDITOR but not a mapping-exactness target.

Human resolution is not automatically historical truth.

A FULL WARRANTED RESOLUTION additionally requires that the frozen Journal/Site Index source state materialize a compatible result.

Otherwise report:

    EDITOR_RESOLVED_BUT_SOURCE_NOT_MATERIALIZED

## Root task

The tested system receives only this generic instruction:

> Maintain a source-grounded prosopographic research state for people mentioned in the Digital Mitford Journal. Surface live identity/reference/relationship questions when the available Journal and Site Index evidence makes them researchable; do not invent unsupported questions.

It is not given:
- a list of people;
- checklist entries;
- future answers;
- a target number of questions.

## Candidate positive interface R*

R* is fixed before unexposed gold inspection.

At every checkpoint it retains mechanically derived records for each person mention and linked Site Index entity.

### Source identity
- Journal commit/blob;
- source element path;
- journal date/entry identity when encoded;
- source surface form.

### Addressable entity state
- persName ref when present;
- whether the target exists in current Site Index;
- Site Index xml:id;
- normalized names/aliases;
- directly encoded person-person refs in the current Site Index entry.

### Epistemic status
Use only the following frozen phrases in the current source/index context:

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

Also retain whether a question mark occurs in the immediate current person-entry note context.

Record the exact matched phrase and source span.

### Alternatives
- current candidate person IDs with the same normalized surname/honorific/surface key;
- explicit alternative IDs/names encoded in the current Site Index entry.

### Provenance/access
- repository;
- commit;
- blob;
- element path;
- lawful Journal and Site Index handles.

### History
Across checkpoints retain:
- prior R* warrant state;
- prior unresolved alternatives;
- prior entity binding;
- checkpoint/version.

R* never contains the hidden checklist.

## Ablations

### R_TEXT

Retain flattened readable Journal and Site Index text.

Remove:
- XML IDs;
- refs;
- hierarchy;
- source paths;
- version-bound entity binding;
- retained alternatives/history.

### R_REF_ONLY

Retain:
- source person surface;
- ref when present;
- whether the target exists;
- current canonical person name.

Remove:
- uncertainty/status;
- alternatives;
- person-person dependency refs;
- prior unresolved/history state.

### R_NO_HISTORY

Same current-checkpoint information as R* but carry no state from earlier checkpoints.

## Frozen discovery operator

Primary discovery is deterministic.

Generate a live identity/reference question when at least one condition holds.

### Q1 MISSING TARGET
A Journal persName ref points to an ID absent from the current Site Index.

### Q2 EXPLICIT UNCERTAINTY
The matched current Site Index person entry contains a frozen uncertainty phrase.

### Q3 CANDIDATE COLLISION
A normalized source surname/honorific/surface key is compatible with more than one current Site Index person and the available binding does not uniquely distinguish them.

### Q4 REFERENCE INCONSISTENCY
The same normalized person surface is bound to more than one Site Index ID in the current Journal unless extra source name/title tokens distinguish them.

### Q5 STATE/NAME MISMATCH
A current Journal ref resolves to a Site Index person whose normalized name set has no compatible token overlap with the source mention after globally declared honorific normalization.

The generated question is generic:

    What person identity or relationship should this source mention be bound to, given the current evidence?

The scientific object is detection of a live distinction and source-bound referent, not natural-language quality.

## Discovery metrics

At each checkpoint report:

- live gold person questions;
- generated live questions;
- precision;
- recall;
- source-bound referent exactness;
- unsupported question rate;
- duplicate question rate;
- safe unresolved rate.

Gold matching is by source referent/stable entity key, not wording.

No LLM grades the primary metric.

## Lawful evidence pursuit

For a generated question the primary experiment may:

1. inspect the current Journal source element;
2. inspect all same-entity/current-candidate Journal occurrences;
3. inspect the current Site Index person entry;
4. inspect later frozen Journal/Site Index checkpoints when time advances.

No web search, Wikipedia, ODNB, VIAF or later project state may be dereferenced in the primary experiment.

External pointers encoded in the Site Index may be recorded but not opened.

## Warrant states

Each episode is one of:

- RESOLVED_TO_ID(id)
- RESOLVED_RELATION(relation,target)
- AMBIGUOUS(candidate set)
- UNRESOLVED
- SOURCE_INCOMPATIBLE

Resolution is warranted only if:
- target identity is determinate;
- source/current-state evidence is compatible;
- no retained alternative remains equally admissible.

Safe unresolved is correct when the frozen evidence does not determine one answer.

## Sustained trajectory

The same R* schema and update rules execute at all four checkpoints.

For every eligible episode report:

- first source-detectable checkpoint;
- first generated-question checkpoint;
- gold first-open checkpoint;
- every null checkpoint with no gold/source-relevant state change;
- first warranted resolution checkpoint if any;
- gold first-resolved checkpoint if any;
- unresolved persistence;
- collateral changes to unrelated episodes.

No checkpoint-specific detector may be added.

## Selective update

When a new checkpoint affects one episode, only that episode may change unless the new source creates an explicit dependency for another episode.

Report:
- missed warranted resolution;
- premature resolution;
- collateral revision;
- source-incompatible resolution;
- correct unresolved persistence.

## Null-event stability

For each episode, a checkpoint is a null event when:
- gold status is unchanged;
- and the relevant source/index record is unchanged under the frozen identity binding.

The warrant state must remain unchanged.

This yields natural negative controls rather than fabricated events.

## Delayed reuse

For each eligible episode with at least two distinct Journal person occurrences:

- earliest occurrence = discovery/trigger occurrence;
- latest distinct occurrence = delayed-reuse query.

At T3 ask which identity/warrant state should be used for the later occurrence.

Correct output:
- resolved identity if warranted;
- otherwise retained ambiguous/unresolved state.

Report delayed-reuse exactness separately for resolved and unresolved episodes.

## Positive sufficiency criterion

R* passes the bounded holdout only if the complete unexposed population shows all of the following:

1. every source-materialized live gold question is detected no later than the checkpoint at which its distinction becomes available;
2. no source-incompatible item is falsely resolved;
3. source-materialized editorial resolutions are selectively incorporated;
4. gold-still-open items are not forced closed;
5. null checkpoints cause no gratuitous warrant changes;
6. delayed reuse preserves correct resolved/unresolved state;
7. the same R* schema works across T0-T3;
8. ablation failures occur only where the removed distinction is required.

Do not require 100% agreement with human wording or every human editorial decision.

Headline metrics must separately report:
- discovery precision/recall;
- source-materialization rate;
- warranted-resolution exactness;
- unresolved persistence;
- null-event stability;
- delayed reuse.

## Mother-problem interpretation

A successful R* result plus at least one predicted ablation separation supports only the bounded claim:

> For this prospectively frozen independent scholarly trajectory, a versioned source-grounded interface preserving addressable identities, uncertainty/alternatives, provenance, lawful source handles and research-state history is sufficient to detect live prosopographic questions, carry them through source investigation, selectively incorporate supported resolutions, preserve unresolved alternatives, and reuse the resulting warrant state later.

This is relative to:
- Digital Mitford person-identity/relationship inquiry;
- T0-T3;
- the frozen source/access contract.

It is not a universal theorem or a claim that every field in R* is globally necessary.

## Failure interpretations

If R* misses gold questions:
report discovery or grammar insufficiency; do not add item-specific triggers.

If editors resolve an item but sources do not materialize it:
preserve the discrepancy.

If R_TEXT or R_REF_ONLY matches R*:
the stronger R* information is not shown necessary here.

If R_NO_HISTORY matches R*:
retained research history is not shown necessary over this horizon.

If many items remain unresolved:
retain them as evidence about warranted abstention.

## Stop rule

After this protocol commit:

- do not manually inspect unexposed checklist entries before automatic population extraction;
- do not change T0-T3 commits/blobs;
- do not change the exposure ledger;
- do not remove unresolved/null/source-mismatch episodes;
- do not add uncertainty phrases after outcome;
- do not add item-specific question rules;
- do not dereference external authorities in the primary experiment;
- do not replace Digital Mitford based on outcome.

Any implementation repair before scientific output must be documented and must not alter these scientific rules.
