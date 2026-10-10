# MCR-V0 PRECODE SCIENTIFIC CONTRACT — 2026-10-10

Project: **Mediated Claim Representation (MCR)**, a DH x LLM representation research candidate. This branch is a new, separately scoped ALGORITHM DEVELOPMENT program, NOT a continuation / rescore / rescue of any frozen Yule-Cordier experiment. Parent `main` = `3f4f31792a59bdb2d1a2bd57893f417d2d3c6a07`.

**Question:** Can a claim-conditioned, mediation- and relation-aware representation for LLMs preserve claim-critical source distinctions, counterevidence and response chains under a fixed evidence/token budget, as opposed to treating semantically relevant text spans as mutually substitutable?

**Method object:** A computable **representation**, not a purported new epistemic logic. A state consists of separate learned/estimated content channels (claim-facing relevance, challenge, response, uncertainty), a provenance/referent relation structure, and a budgeted grounded evidence packet for an LLM. The REPRESENTATION must differ when a relevant documentary anchor or evidence stance changes, and remain stable under irrelevant metadata/case changes, under frozen extraction inputs. This condition is about the REPRESENTATION, NOT automatic recovery of truth.

## Constraints inherited from the existing DH research

1. `G_D` source-verifiable documentary structure and `G_E` scholar-adjudicated epistemic assertions are **NOT one data layer**. Machine-inferred relation edges are separate from BOTH; use `model_predicted`, `source_attested` or `simulated` fields as provenance classes.
2. Never convert a `G_D` citation, edition chronology, or page verification into claim entailment; a witness can be authentic and still challenge another witness.
3. Frozen negative 2026-09-26 three-model result is AUTHORITATIVE: Qwen2.5 7B was unstable on the sham; Gemma3 12B and Llama3.1 8B were stable but constant RETAIN. No packet/prompt/label changes will retroactively turn that result into success.
4. Prior formal PM01/PM02/PM03 grounded-argument reinstatement is **not a new machine learning result**. Synthetic regression may mirror generic attack/rebuttal topology, but cannot re-count it as real-world LLM performance.
5. Historical Yule-Cordier, Frankenstein Variorum, Whitman Archive and Digital Faust cases have already been inspected. They are **development / external-context sources**, NOT untouched confirmatory holdouts.
6. The old `manuscript/`, `reports/`, `spec/`, `coding/`, `experiments/warrant_closure_*`, original Yule-Cordier data and historic workflows are read-only. This new branch adds exclusively namespaced `mcr_v0/` and `experiments/mcr_v0/` content plus possibly a separate branch-specific CI workflow. No authority/claim-state label in model features.
7. All toy tests are flagged `SYNTHETIC_DEV`; no human judgment, neural model effect, benchmark advantage, or generalization is established without NEW prospective data.

## Exact computation in V0

- **Inputs**: a claim identifier, claim embedding from a FROZEN text encoder, a documented set of evidence spans with embeddings, source IDs/version/page locus/verifier status, separate source-attested DOCUMENTARY edges, and typed **CANDIDATE** epistemic edges carrying a declared producer origin. At present relation predictions may be caller-supplied; they are NOT ground truth.
- **Output**: (1) claim-conditioned embedding channels for affirmation, challenge, response, and unresolved; (2) source/edition/claim scope and an explicit budgeted packet with counterevidence/response links; (3) missing-source and missing-link flags; (4) a formatted downstream LLM context that describes suggestions as unverified when their epistemic source is a model.
- **Contract**: only page/object-verified spans can become 'qualified native witnesses' in a source-confirmatory claim. Unverified spans can be candidate retrievals but not grounds for an asserted source-backed entailment.
- **Strong information parity**: every baseline has the SAME texts, embeddings, authorized documentary/epistemic predictions, token budget, source roster and declared label availability. Never compare a model that sees relation annotations to a baseline only given text and claim it won by algorithm.
- **Main missing technical piece**: trainable RELATION PREDICTOR and claim-conditioned representation computation on real source-grounded DH annotation. Until implemented/evaluated, V0 is an executable reference encoder and a feasibility boundary, not a publishable LLM algorithm.

## PRE-DECLARED negative/positive structural tests (not accuracy or new scored cases)

N1: Two high-similarity passages cannot become uniquely warranting simply because embeddings are identical, if one is blocked/edition-incompatible and the other source-verified. Excluded material must remain visible as excluded, not silently thrown away.

N2: A supported assertion with a candidate challenge should encode a nonzero challenge channel and include the attacker (if accessible within packet budget) or record an unmet counterevidence obligation; a flat top-K baseline may omit it but must be run with equal available inputs.

N3: A subsequent source-linked rebuttal should generate a RESPONSE channel distinct from CHALLENGE, not automatically erase the challenge; downstream LLM receives both plus their attachment.

N4: An irrelevant sham edge not bound to the target claim must not change its claim-conditioned representation/packet, modulo deterministic tie ordering.

N5: With insufficient token budget, a focal assertion may be retrieved while the challenge/rebuttal is missing. The system MUST report `budget_truncated` or `unresolved_links` and MUST NOT advertise complete warrant or force RETAIN.

N6: Unverified documentary ancestry / anchor must not be magically upgraded by model-predicted epistemic labels. Proof of source fidelity is external to latent-space similarity.

N7: Equal text but different claim ID / edition binding may lead to distinct representations. A mere passage match cannot launder source identity.

N8: The encoder must have a deterministic output for deterministic inputs and an externally pluggable frozen encoder. No hidden role labels or expected claim outcome can be embedded into real evaluation inputs.

These are technical invariants for a DEVELOPMENT toy model, not confirmatory test scores.

## Baseline and eventual empirical kill plan

Baseline tiers:
- lexical BM25, dense cosine + top-k; identical frozen encoder;
- metadata-concatenation top-k RAG, provenance-ranked RAG, RA-RAG (EMNLP 2025);
- candidate-relation-aware naive graph expansion / GraphRAG using the SAME relation proposals;
- argumentation-aware RAG and source conflict-aware Astute RAG (ACL 2025);
- full-context reference LLM under explicit equal budget (when feasible); and source-assisted humanistic retrieval if independently arranged.

Development cohort = historical available DH sources with no claim of untouchedness. A FRESH source-stratified DH test corpus is required: preregister 20+ separate claims across distinct edition families and annotation categories, page/span refs, candidate alternative source states (affirmation, objection, reinstatement, unresolved, provenance-swap and referent-swap), hard negatives and adversarial paraphrases. Number is a SAMPLE-DESIGN CANDIDATE not an achieved count nor a hard power-analysis threshold.

Metrics must separate (A) candidate relation extraction P/R/calibration; (B) exact source/binding fidelity; (C) counterevidence and restoration chain recall at fixed token budget; (D) overreach/refusal on expert-verified answer sets; (E) final LLM generation quality with blinded human adjudication; (F) runtime/VRAM/token overhead. Evaluate matched counterfactual effects AND equal-cost method comparisons, confidence intervals, and abstention denominators. Leave conflicting expert judgments set-valued. No 'accuracy' score if the model simply reads the answer labels in input annotations.

Split by **source work, witness, edition family and claim identity**, not random overlapping chunks. Freeze gold labels separately, after panel adjudication and before model outputs. Do not choose new packets by inspecting failed historic prompt outputs.

## Closest literature that might kill novelty

- Hwang et al., EMNLP 2025, *Retrieval-Augmented Generation with Estimation of Source Reliability*, https://aclanthology.org/2025.emnlp-main.1738/ .
- Wang et al., ACL 2025, *Astute RAG: Overcoming Imperfect Retrieval Augmentation and Knowledge Conflicts for Large Language Models*, https://aclanthology.org/2025.acl-long.1476/ .
- Dhole et al., NAACL 2025, *ConQRet*, https://aclanthology.org/2025.naacl-long.293/ .
- Abolghasemi et al., Findings ACL 2025, *Evaluation of Attribution Bias in Generator-Aware Retrieval-Augmented Large Language Models*, https://aclanthology.org/2025.findings-acl.1087/ .
- Li et al., CustomNLP4U 2026, *Efficiency vs. Verifiability in Evidence-Aware RAG*, https://aclanthology.org/2026.customnlp4u-1.19/ .
- Digital text scholarly standards: TEI and W3C PROV already distinguish witnesses, variations and provenance. Formal grounded argumentation is old; not claimed invented.

**V0 GO** iff we can build a functioning zero-external-data pipeline that keeps G_D, machine `G_E_hat`, and final human `G_E_gold` separate; passes all preregistered STRUCTURAL tests; and exposes a direct, reproducible LLM model interface.

**V0 NO-GO** if outputs are just metadata tags attached to passages, if relation votes are mistaken for historical warrant, if the model uses human gold labels at inference, if a generic graph expansion with same inputs trivially duplicates the entire proposed algorithm, or if historical frozen LLM failures are relabeled as success.

**No new original-paper status implied.** This is a branch-isolated algorithm-preflight experiment; old accepted/rejected results and scholarly source identities remain untouched.
