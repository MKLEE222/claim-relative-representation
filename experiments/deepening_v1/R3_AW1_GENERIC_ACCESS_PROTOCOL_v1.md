# R3-AW1 — Frozen Generic Access Workflow Transfer

Date frozen: 2026-09-27
Status: PRE-OUTCOME PROTOCOL

## Purpose

Apply the already-frozen Generic Seed-Task Access Policy v1 (2026-09-24) unchanged to the five R3 load-bearing historical inquiries frozen on 2026-09-27.

This is a workflow-replay test of research discoverability from HISTORICAL_START. It is not a controlled relation-deletion experiment.

## Independence advantage

The access policy predates the R3 proposition-level inquiry panel.

Therefore the following are inherited without tuning:
- 180-word candidate windows;
- 90-word stride;
- top K = 12 seed/task TF×IDF terms;
- frozen general-English stoplist;
- IDF estimated from the base/earlier object;
- identical lexical weighted-overlap ranker;
- native later-layer restriction only when the task asks for later treatment.

No rank-dependent retuning is allowed.

## Native objects

- 1903 Volume I Project Gutenberg UTF-8: expected SHA-256
  7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5
- 1920 Notes and Addenda Project Gutenberg UTF-8: expected SHA-256
  c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

## Cases

All five frozen inquiries are run, not a favorable subset:

- R3Q-PASH-STANCE
- R3Q-ARBR-COMMIT
- R3Q-DES-EVIDENCE
- R3Q-URM-ERRATUM
- R3Q-TUN-CONTROVERSY

Each case begins from its frozen 1903 historical locus and answer-neutral task wording. The later 1920 target is hidden from query construction and used only after candidates have been generated.

## Evaluation-only target anchors

Target anchors are implementation locators only. They may not enter the query unless independently present in the seed/task.

The script declares case-specific forbidden target-only terms and aborts if any appears among the top-K query terms.

## Conditions

### GSA_FULL_OBJECT
Search the union of the declared 1903 and 1920 digital objects using the frozen window/ranking procedure.

### GSA_LATER_LAYER
Because every R3 question explicitly asks about later 1920 treatment, search only the native 1920 Addenda layer identified by its own heading.

No target-specific page, chapter, or subsection restriction is allowed.

## Outcomes

For each case and condition report:
- query terms;
- candidate count;
- target rank;
- reciprocal rank;
- Hit@10 / Hit@20 / Hit@50.

No threshold is retrofitted after results.

Interpretation:
- low rank / miss = discoverability burden under this frozen workflow;
- high rank = the workflow preserves practical access for that case;
- mixed results = workflow/case interaction, not one global representation score.

## Proposition-level follow-through

If the target enters the inspection budget, the later passage is then evaluated against the already-frozen historical inquiry answer. Retrieval success alone is not proposition-level relation success.

If the target does not enter the inspection budget, do not infer that the relation is absent from the representation; classify as discoverability failure under the declared policy.

## Claim ceiling

This workflow can establish ecological access/discoverability effects from realistic historical starts.

It cannot by itself establish:
- information-theoretic loss;
- human inability;
- universal plain-text insufficiency;
- global minimal carrier sets.

Any positive ecological attrition claim requires preserving the distinction between:
scope, discoverability, relation determinacy, provenance traceability, uncertainty fidelity, and composability.
