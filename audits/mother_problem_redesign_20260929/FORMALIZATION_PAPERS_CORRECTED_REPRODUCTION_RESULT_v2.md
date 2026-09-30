# Formalization Papers corrected reproduction result v2

Date: 2026-09-30
Status: POST_FRESH_CORRECTED_REPRODUCTION_PASS.

## 1. Authoritative fresh result is unchanged

Authoritative prospective run:

    36657856767

remains permanently:

    INVALID

Freshness was consumed at the registered DATA_OPEN event before the first source archive download.

The corrected result below does not restore or replace that fresh label.

## 2. Corrected reproduction

Workflow:

    formalization-papers-corrected-reproduction-v1

Successful v2 run:

    36659349160

Head:

    92f16bf4e0476890851409be951bdce06a58ed43

Artifact:

    11073656774

Artifact ZIP SHA-256:

    3819e4cd06fe4b22a6a68aaa4ca3ee01515fac08b25ac4cdb63e61463bf46e8d

Corrected disposition:

    POST_FRESH_CORRECTED_REPRODUCTION_PASS

Scientific disposition under the unchanged population/qualification/finalization rules:

    PASS

## 3. Byte-identical source

The corrected run used the exact first-opening source archive:

    LaraHack/formalization_papers_supplemental
    commit 2f68d8498aeeb724e3438deda13e74ae7fb076d8

Archive SHA-256:

    c2349aa34350dc5f02f3ad7ccfc1ff6f879e88950fee948b0d5ffa206d4ca9e3

Record files:

    10

No record subset, alternate release or published-index fallback was used.

## 4. Implementation corrections

Two post-fresh implementation defects were isolated before corrected population execution.

### 4.1 xsd:dateTime lexical precision

RDFLib and pyoxigraph represented the same parsed dateTime value with different fractional-second
precision:

    .526000+02:00
    vs
    .526+02:00

The frozen correction canonicalizes the parsed dateTime value to microsecond precision while
preserving the represented UTC offset.

It does not change chronology or infer missing time.

### 4.2 dct:creator relation cardinality

The source ecology contains multi-valued creator relations.

Full-archive audit:

    nanopublications = 404

    creator cardinality:
        exactly 1 = 379
        exactly 2 = 25

    created timestamp cardinality:
        exactly 1 = 404

The first extractor incorrectly collapsed:

    nanopublication -> creator*

into a scalar dictionary entry.

The v2 correction preserves the registered RDF relation as the complete set of:

    (nanopublication_uri, creator_uri)

pairs.

No primary creator is selected.

## 5. Real-source parser closure

After both implementation corrections:

    file_count = 10
    exact_file_count = 10

Registered component mismatches:

    none

Exact components include:
- roots;
- reviews;
- updates;
- responses;
- decisions;
- supersedes;
- retracts;
- creators;
- created timestamps.

Registered scientific surface SHA-256:

    75002d78703c02d53121d570bd8512d3bd62c4fc967da6ffd5734279e1c28d02

Thus the corrected run enters population analysis only after exact independent-parser agreement on
the complete registered graph surface.

## 6. Complete population accounting

Graph-derived root population:

    15

Every root receives exactly one frozen T0-T9 disposition.

Observed:

    T0_COMPLETE_REVIEW_UPDATE_RESPONSE_DECISION = 8
    T8_AMBIGUOUS_OR_NONFUNCTIONAL_TARGET         = 7

No root was discarded.

The T8 roots remain negative/ambiguous population outcomes and are not rescued into the primary
denominator.

## 7. Connected qualified-composition denominator

For the eight T0 roots, the frozen grammar enumerates ALL connected chains rather than selecting
one favorable chain per root.

Eligible connected chains:

    52

Every chain includes:

    submission/root
    -> review
    -> update
    -> response
    -> decision

with exact project-native target binding.

Corrected forward/counterfactual result:

    chain pass = 52/52

No operation label is read from provider data.

Registered generator sequence:

    RECORD_REVIEW
    -> REPLACE_FORMALIZATION
    -> RECORD_RESPONSE
    -> REVISE_PUBLICATION_STATUS

## 8. Load-bearing composition tests

For every eligible chain, the frozen prospective design tests:
- response before targeted review;
- response after review but before targeted update;
- same-current-update history ablation;
- decision before targeted update;
- deterministic wrong-target injection when structurally available;
- retraction/supersession discipline.

The main corrected analysis reports:

    52/52 eligible chains PASS

under the complete frozen criterion set.

The central cross-ecology proposition is therefore executable on all registered eligible chains:

> A later response is lawfully available only after the project-native review and update targets
> it references have entered the retained scholarly state/history.

Most importantly, the history-ablation design holds the current formalization/update projection
fixed while removing the prior review/update history required for response interpretation.

This tests:

    same current scholarly state projection
    !=
    same future action availability

in an independent semantic-publishing ecology.

## 9. Independent documentary audit

The documentary auditor does not import the main extractor or population classifier.

Result:

    root_set_exact            = true
    connected_chain_set_exact = true
    T0_chain_set_exact         = true

Audited chains:

    52

Pass:

    52/52

Errors:

    0

Thus the primary chain denominator itself is independently reconstructed from raw TriG rather than
only rechecked after selection.

## 10. Result hashes

Corrected main result SHA-256:

    a0848c8accb2988f7b45f758d85a86d1170e5bf7524ff1b496d587706c33845d

Independent documentary audit SHA-256:

    76f1458f32c09017fb5afa8b5cade20845d50c2a884640f4b2b2739d39274faf

Corrected parser diagnostic SHA-256:

    87bb10d9bd5f17c0a28e14895f0fe62dd52a59cd4bd4ebc6cffb5e9f4486941c

## 11. Scientific interpretation

This result materially strengthens the qualified-composition line.

Before Formalization Papers:
- state-dependent qualification was established structurally;
- Paper Money showed natural history-dependent correction;
- Arbre Sec showed natural act-level proposal -> history-only reply;
- both natural sequences were exposed and from one historical corpus.

Formalization Papers now supplies an independent scholarly ecology with:
- native machine-readable target relations;
- explicit review/update/response/decision acts;
- a closed graph-derived root population;
- 52 complete connected composition chains;
- exact independent parser agreement;
- same-current-state history ablation;
- independent raw-source denominator reconstruction.

The strongest licensed cross-ecology statement is:

> In the frozen Formalization Papers v1.0 population, after implementation-only corrections to
> parser-output dateTime serialization and preservation of multi-valued creator relations, all 52
> registered connected review-update-response-decision chains satisfy the pre-specified
> target-bound and history-sensitive qualified-composition tests. The same current updated
> formalization is insufficient to determine later response availability when the retained
> review/update history it targets is removed.

## 12. Evidentiary ceiling

This is strong:

    independent ecology
    closed population
    pre-specified scientific protocol
    byte-identical first-opening source
    full corrected reproduction
    52 connected natural chains
    independent documentary audit

But it is:

    POST_FRESH CORRECTED REPRODUCTION

not:

    literal prospective fresh PASS

because the authoritative first DATA_OPEN execution was INVALID at the parser-surface gate.

Do not claim:
- freshness restoration;
- prevalence outside the frozen 15-root population;
- universal scholarly action algebra;
- automatic semantic interpretation of review text;
- quality or correctness judgments about authors/reviewers;
- causal effects on acceptance.
