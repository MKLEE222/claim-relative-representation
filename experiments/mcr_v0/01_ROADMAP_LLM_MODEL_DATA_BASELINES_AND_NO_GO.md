# MCR research execution roadmap — v0 implemented / v1-v3 prospective

## Research identity

**MCR: Mediated Claim Representation for DH x LLM.** Mother problem: computing claim-relative representations of text mediated by witnesses, editions, translation, cataloging, cross-document references and later scholarly objections/corrections. This is a **computational representation / learning** target, NOT an attempt to invent a new foundational epistemic logic.

Existing DH project [`claim-relative-representation`](https://github.com/MKLEE222/claim-relative-representation) ALREADY documented realistic testimony/edition examples and failed LLM categorical adjudication: three frozen judges did not achieve the intended selective reinstatement. That failure is the motivating technical observation, not a rescore opportunity.

## What v0 really implements

- [x] Claim-conditioned typed input: externally frozen claim embedding; evidence embeddings, exact source/page/edition and claim binding.
- [x] `G_D` documentary links separate from `G_E_hat` candidate epistemic relations; no ability to read confirmatory `G_E_gold` at inference.
- [x] Per-source page/object verification gate, primary wording restriction and explicit documentary bridge contract.
- [x] Finite same-budget selection over evidence units (exhaustive best-of-current-heuristic for <=16 units, greedy non-exact above 16; neither has scientific optimality claim).
- [x] Vector-valued claim representation with affirmation/challenge/response/qualification/unclassified channels.
- [x] LLM context emitted with version, page anchor, explicit challenge/response hypotheses, unresolved links, completeness/coverage refusal flags.
- [x] Paired dense cosine and **same-edge naive graph-expansion** baselines, not only strawman BM25.
- [x] CPU-only trainable linear role-proposal head on frozen external embeddings; explicitly a REGRESSION BASELINE, not a newly invented neural architecture.
- [x] Synthetic source- and claim-binding counterfactual invariants; isolated GitHub Actions.
- [ ] Real pretrained encoder training or evaluation; LLM generator calls; historical-human warrant metric; end-to-end DH generalization.

**The current 'exact' flag means exact maximization of V0's *own declared finite heuristic packet score*, not global minimal evidence, true source sufficiency, or optimal human interpretation.** Model-predicted edges and source-attested quotations are never labels of historical truth.

## Scientific pipeline and stop rules

### M1 — Claim-relative inference, NOT labelled graph input

Acquire a specified frozen publicly licensed text encoder or cross-encoder. Freeze primary train/validation/test partitions at SOURCE-WORK / EDITION / CLAIM family level. Develop a trainable pairwise relation head using independently annotated SUPPORT / UNDERCUT / REHABILITATE / QUALIFY / UNRELATED observations with permitted ambiguity. Source span text, documentary G_D and training labels are disjoint artifacts. At evaluation time, NO human epistemic labels or hidden target units appear in model inputs.

First full task: predict **source stance links from evidence text and documentary information**. Score macro-F1, precision-recall, calibration, target-binding false positives and abstention. If model cannot outperform *same frozen embeddings + prompt-based stance extraction* under fair costs, STOP representation claims.

### M2 — Learned relation state, not arbitrary handwritten constants

Replace v0 hand-weighted set objective with a trainable, auditably constrained claim-conditioned encoder over predicted pairwise relations. Separate support/challenge/reinstatement channels and counterevidence coverage; do not substitute one scalar likelihood for an argument graph.

Train on source-stratified supervision plus controlled contrast pairs:
- identical source text, different authorized version or referent;
- same user-facing answer, different provenance/authority;
- objection added, objection defeated, irrelevant sham added;
- translation changes wording, but scope makes a historical wording claim unavailable;
- conflict- or source-incomplete cases requiring explicit uncertainty.

Two intended losses (not yet executed): cross-entropy over independently annotated relations and **paired intervention consistency** (change only target-relevant source link -> response changes; irrelevant sham -> stable). Architectural ablations: remove claim embedding, remove G_D, drop proposed G_E, merge role channels, disable closure, metadata-only prompt. These demonstrate causal component necessity only when independent controls and all strong baselines are run.

### M3 — LLM output + humanities evaluation

Run SAME generator(s), same base embeddings, same permitted source bytes, same prompt budget on:
BM25, dense RAG, metadata concatenation, provenance-rank RAG, RA-RAG, Astute RAG, typed GraphRAG, graph expansion with identical relation predictions, full-context where possible, MCR and ablations. Avoid granting MCR gold stance labels while denying them to baselines.

Measure separately:
(1) retrieved claim-bearing source recall;
(2) attack/reinstatement-chain recall, and retrieval burden at fixed tokens;
(3) exact text-locus citations and witness/source identity;
(4) expert-adjudicated overcommitment/abstention and uncertainty;
(5) literary/historical explanation utility and justified interpretive alternatives;
(6) runtime and model+graph memory.
Blind qualified humanities adjudicators see model outputs but not method names; ambiguous historical readings get SET-VALUED labels. Adjudicators cannot be replaced by an LLM that simply agrees with its own pseudo-labels.

Negative controls should include a false evidential premise for which the model should refuse to adjudicate, and seemingly similar text with a different historical referent. Target answer should NEVER be encoded as test input feature.

### M4 — New independent external DH evaluation

Previously inspected and exposed Yule–Cordier / Frankenstein Variorum / Whitman Archive / Digital Faust are OPEN DEVELOPMENT material only. Choose genuinely new works/corpora independently before seeing method outcome; freeze licenses/source identities and accessibility. No recycling a previously seen result as "holdout". Pre-register source-level splits and required evaluation axes; perform a native sample integrity check without treating corpus statistics as new epistemic accuracy. A mixed NLP+DH success criterion is mandatory: language reasoning metric and scholarly evidential adequacy metric must BOTH be reported.

### M5 — Paper-shape gate

A strong methods paper requires:
- true trainable computational representation beyond manually encoding gold stance graph;
- independently confirmed gains or important cost/accuracy trade-offs over strong relation-aware and source-aware RAG baselines;
- source-grounded DH test coverage with stratified uncertainty/overreach, not just positive cases;
- fair budgets, 95% uncertainty estimates, all run denominators and failure cases;
- enough operator ablations to separate graph structure from the learned representation.

If same-edge GraphRAG/metadata methods tie MCR and the trainable role head has no independent gain, **NO-GO on algorithm novelty**. Reposition as a transparent DH methodology or tool without pretending an algorithm win.

## Archived evidence boundary

Old 2026-09-26 final LLM study: qwen2.5:7b MODEL_SENSITIVE; gemma3:12b / llama3.1:8b STABLE_NO_PACKET_CONTRAST. Old formal PM grounded reinstatement succeeds mechanically; NO new LLM success inferred from it. The branch does not edit or rerun the original frozen artifacts, author ledgers, holdouts or manuscript. Old EEQ G4/G5/G6/G8 gates likewise not touched.

## Actual tools in new namespaced branch

- `mcr_v0/core.py` — graph-qualified representation and source-aware packet.
- `mcr_v0/trainable.py` — tiny supervised pair-relations role head, only frozen embedding input, explicit data boundary.
- `mcr_v0/test_mcr.py` — preregistered synthetic smoke and counterfactual tests.
- `mcr_v0/demo.py` — fictional citation/objection/rebuttal example.
- `.github/workflows/mcr-v0-synthetic-dev.yml` — Python 3.12, stdlib only, no live source requests.

This is a **V0 implementation and scientific execution plan**, not a complete paper or the output of a real fine-tuned LLM.
