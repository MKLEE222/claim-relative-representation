# Ecological Anchor E1 - Paper-money access/discovery

Date frozen: 2026-09-24
Status: PRE-OUTCOME ECOLOGICAL PILOT

## Scientific question

Starting from the already-known 1903 Bretschneider botanical objection (PM02), can a researcher-facing retrieval workflow surface the later 1920 treatment (PM03) under different access scopes without being given the PM03 locator or relation label?

This is an access/discovery experiment. It does not evaluate the final evidential relation or humanistic claim state.

## Why this is not an ideal-vs-degraded comparison

The experiment begins from independently existing Project Gutenberg native texts:

- N_GUTENBERG_V1_TEXT: eBook #10636
- N_GUTENBERG_V2_TEXT: eBook #12410

No CEDL relation labels are inserted into either text.

The two retrieval conditions are workflow replays over native text:

### W_CURRENT_OBJECT
A deterministic search index over Volume I only, corresponding to a researcher searching the currently open digital object.

### W_DECLARED_COLLECTION
The same deterministic index over Volume I + Volume II/addenda, corresponding to a collection-level search over the declared two-volume Yule-Cordier edition.

The only manipulated factor is retrieval scope. Text content is unchanged.

## Entry state

Provided:
- PM02 seed passage in Volume I;
- identity of the currently studied digital edition.

Withheld:
- PM03 locator;
- the fact that PM03 is a correction/rehabilitation;
- PM03 relation labels;
- PM03 target terms not present in PM02.

## Query generation

The retrieval query is generated mechanically from the PM02 seed window only.

1. locate PM02 by its frozen source anchor;
2. tokenize the PM02 seed window;
3. remove a frozen stopword list;
4. compute IDF using Volume I only;
5. select the top 12 seed terms by TF x IDF;
6. rank candidate windows by weighted overlap with those seed terms.

The target document/PM03 window is not used in query construction.

A leakage assertion fails the run if the term LAUFER enters the query term set.

## Candidate windows

- 180-word windows
- 90-word stride
- seed-overlapping windows in Volume I are excluded from evaluation

## Gold evaluation only

After ranking, PM03 is located in Volume II using the frozen evaluation anchors:
- "Regarding Bretschneider's statement"
- "Laufer"

These anchors are used only to identify the target window for rank calculation.

## Outcomes

For each search scope report:

- whether the PM03 target is in scope;
- target rank if in scope;
- reciprocal rank;
- Hit@1, Hit@5, Hit@10, Hit@20;
- query terms;
- source SHA-256;
- candidate count.

## Interpretation ceiling

### Native/workflow descriptive result
The experiment can establish whether a realistic collection-level retrieval workflow changes discoverability relative to current-object-only retrieval.

### It cannot establish
- that all digital editions behave this way;
- that the later evidence would be interpreted correctly;
- that the final humanistic claim state changes;
- that collection-level search is globally superior.

## Falsification

The access hypothesis is weakened if PM03 is in the declared collection but ranks poorly under the seed-derived retrieval procedure, because broader scope alone would then be insufficient for practical discovery.

A null or adverse result is retained.
