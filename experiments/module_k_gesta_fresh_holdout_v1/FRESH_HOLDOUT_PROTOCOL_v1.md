# Module K — GeStA fresh object-bound confirmatory holdout v1

Date frozen: 2026-09-28
Status: PRE-OPENING PREREGISTRATION. XML CONTENT UNDER THE HOLDOUT PREFIX HAS NOT BEEN READ FOR THIS MODULE.

## 1. Scientific purpose

Module J repaired scholarly-object identity on already exposed Berlin, Paul, and StaBi corpora.
Module K asks whether the frozen object-bound dynamic-researchability mechanism transfers to a genuinely unexposed episode population without any further object-boundary repair.

This is an empirical confirmatory test of the frozen D1/D2 dynamic mechanism under one unchanged evaluator family. It is not a manuscript-writing exercise and it is not a search for a favorable corpus.

## 2. Frozen source population

Upstream repository:

    FloChiff/DAHNProject

Frozen upstream commit:

    e7d4a81d42ea10a3d672e5c0869f033a8c2c8149

Frozen source prefix:

    Correspondence/Nachlassprojekt/GeStA/

Frozen subtree tree SHA observed from Git metadata before opening XML content:

    c6d695e1df251e3ebcea30a14e5060832691b5da

Population rule:

    ALL *.xml blobs recursively below the frozen prefix.

No filename, sender, date, archive subfolder, or anticipated outcome may be used to select a favorable subset.

Pre-opening Git-tree metadata showed:

- 83 XML blobs in the frozen subtree;
- 82 path names contain Brief/letter-like naming;
- one path does not;
- two top-level archive groups are present.

These facts are metadata exposure only. They do not establish object eligibility, D1/D2 eligibility, origin evidence, full trajectories, or success.

## 3. Exposure registry

Already exposed and therefore forbidden as confirmatory populations:

- Correspondence/Berlin_Intellectuals/Corpus/
- Correspondence/Paul_d_Estournelles_de_Constant/Corpus/
- Correspondence/Nachlassprojekt/StaBi/Correspondence/

For GeStA before this freeze:

- repository and directory names were inspected;
- recursive Git tree metadata/path names and blob counts were inspected;
- no GeStA XML blob/body was fetched or read for episode selection;
- no GeStA D1/D2 candidate, object boundary, date value, origin value, warrant, or trajectory outcome is known;
- project-repository indexed search returned no prior GeStA/BBAW/Humboldt holdout record in claim-relative-representation.

The full GeStA subtree is selected precisely to avoid path-level cherry-picking after the metadata inspection.

## 4. Frozen scholarly-object grammar

The Module J object grammar is immutable for this holdout.

Route A:
- exactly one eligible non-annex div type="letter".

Route B:
- when Route A finds none, exactly one substantive div type="transcription" may be the letter object only under the previously frozen unique correspDesc/sent-action conditions.

Route C:
- when A/B fail, exactly one direct untyped body div may be the letter object only under the previously frozen correspondence metadata and letter-structural-marker conditions.

No Route D may be added after any GeStA XML is opened.

No first-object fallback is allowed.
No cross-object temporal composition is allowed.
No aggregate file-level dates may create a single-letter contradiction without one uniquely established primary scholarly object.

## 5. Frozen engine

The holdout must reuse the Module J engine without editing its scientific logic.

Expected Git blob SHAs:

- experiments/module_j_dahn_object_bound_holdout_v1/runtime_j.py
  - 002a5a5f9c4253a6bf1ee90bde4b7b4727636146
- experiments/module_j_dahn_object_bound_holdout_v1/oracle_j.py
  - 282b8db3cc44c3d23aaa15b0bf59f84676eef0e9
- experiments/module_j_dahn_object_bound_holdout_v1/evaluator_j.py
  - 6c588f3c1f723f33020e050fc35af7931fb8eb2e
- experiments/module_j_dahn_object_bound_holdout_v1/test_object_contract_v1.py
  - d7ecddea804e73f53048bfdfc91b84d21eba8c09

The inherited Module I runtime/oracle/evaluator remain whatever is imported by these frozen Module J files at the preregistration commit. Their F1-F9 hardening tests and Module J object-bound F10-F16 tests must pass before the GeStA source archive is fetched by the confirmatory job.

Oracle and runtime remain separate implementations. The confirmatory wrapper may choose the frozen prefix, aggregate results, and serialize artifacts; it may not change object eligibility, temporal eligibility, warrant construction, transitions, ablations, or evaluation semantics.

## 6. Population accounting

The run must report all XML files under the frozen prefix.

The expected total population is 83.

For every file, the run must preserve one of:

- successfully parsed document with object-contract status;
- parse error with path and error record.

If parsed_documents + parse_errors != 83, the run is INVALID.

Object outcomes must include at least:

- SINGLE_PRIMARY_DOCUMENT_OBJECT
- NO_PRIMARY_DOCUMENT_OBJECT
- MULTIPLE_PRIMARY_DOCUMENT_OBJECTS

Discovery/full-trajectory denominators must be reported separately from the total corpus denominator.

A zero eligible/full-trajectory population is a legitimate applicability result, not evaluator accuracy 0/83.

## 7. Frozen primary computational gate

Let N_full be the number of frozen-engine full_trajectory_eligible episodes after the object gate.

Classification before documentary source audit:

### INVALID

Any of:
- frozen engine blob mismatch;
- F1-F16 pre-opening tests fail;
- source population count differs from 83 without a preregistered source failure explanation;
- source archive or execution integrity failure prevents complete accounting.

### NULL_APPLICABILITY

- N_full = 0.

This means the full GeStA population supplies no full trajectory under the frozen contract. It is not an algorithm failure.

### BOUNDED_PARTIAL

Any of:
- 1 <= N_full < 5;
- any full trajectory has unresolved oracle/runtime source contract;
- N_full >= 5 but the primary mechanism conditions below are not all satisfied.

### COMPUTATIONAL_PASS_PENDING_SOURCE_AUDIT

All of:
1. N_full >= 5;
2. I_RSTAR end_to_end_pass = N_full;
3. at least one held-out alternative-separation witness exists;
4. at least one held-out binding-separation witness exists;
5. at least one held-out history-separation witness exists;
6. no full trajectory has unresolved oracle/runtime source contract.

I_NATIVE is reported as a secondary comparator and is not itself a primary pass requirement.

No threshold may be changed after opening GeStA.

## 8. Post-run documentary audit gate

A computational pass is not yet the final scientific PASS.

After the one-time run, source inspection is permitted only for a deterministic audit set generated by the frozen runner.

Audit rule:
- if N_full <= 12, audit all full trajectories;
- otherwise audit a deterministic set of 12 selected by the existing Module J audit routine, which preferentially includes available D1/D2, annex, alternative-set, and interval/open-interval witnesses before hash-ranked fill.

The audit must verify from the source XML that:
- the selected primary scholarly object is real and unique under A/B/C;
- admitted date carriers belong to that object;
- annex/aggregate material is not misbound;
- the D1/D2 trigger is source-present;
- origin evidence and later warrant are represented exactly as claimed by the frozen parser;
- the sampled ablation witness is not an artifact of misparsed source structure.

Final disposition:

- PASS: computational pass + all deterministic documentary-audit cases valid.
- BOUNDED_PARTIAL: computational gate passes but at least one audited scientific interpretation cannot be source-validated, or the computational gate itself is bounded partial.
- NULL_APPLICABILITY: as above.
- INVALID: as above.

A failed documentary audit cannot be repaired inside Module K. Any repair belongs to a future version/study and the original Module K result remains frozen.

## 9. One-run authority

The first completed GitHub Actions run created from the preregistered Module K workflow and this frozen protocol is the authoritative confirmatory run.

Any later rerun, amended workflow, changed engine, changed source selection, or changed threshold is diagnostic/future-work only and cannot replace the first result.

## 10. Required artifacts

The authoritative run must preserve:

- upstream repository/commit/prefix;
- downloaded archive SHA-256;
- complete population counts;
- parse errors;
- object-status manifest;
- complete primary discovery manifest;
- all full trajectory results for every interface;
- deterministic documentary-audit manifest;
- result JSON SHA-256;
- audit-manifest SHA-256;
- engine Git blob checks;
- final pre-audit computational classification.

## 11. Interpretation boundary

A positive Module K result licenses only a bounded statement that the frozen object-bound dynamic mechanism transferred prospectively to this previously unexposed GeStA population under the same DAHN encoding ecology.

Because GeStA shares the DAHN project/schema family with Berlin and Paul, even a PASS is not by itself cross-project validation.

A NULL or BOUNDED_PARTIAL result is retained as scientific evidence and must not trigger post-hoc corpus rescue.
