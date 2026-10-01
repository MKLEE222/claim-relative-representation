# Source notes, evidence status, and submission gaps

Date: 2026-09-30  
Applies to: [MANUSCRIPT_v1.md](MANUSCRIPT_v1.md)  
Scientific evidence baseline: `c6f56fa17a5e3d02f16a336ed6e450b1843d8fb6`  
Status: COMPANION TO FIRST INTEGRATED DRAFT / NOT INDEPENDENT RED-TEAM ACCEPTANCE.

The manuscript was written against existing repository evidence. No natural corpus was opened, no model called, no experimental success criterion changed, and no fresh confirmation claimed as part of this writing task. Original manuscripts, protocols, and negative results remain historical records. Relative evidence links below resolve on the research branch; the baseline SHA identifies the scientific snapshot used for writing.

## Evidence register

<a id="e1"></a>
### E1. Historical sources and prior source verification

Primary witnesses cited in the manuscript are the 1903 third edition of *The Book of Ser Marco Polo*, volume I, and Cordier's 1920 *Notes and Addenda*.

| Manuscript reading | Printed locus | Repository record | Earlier recorded verification |
| --- | --- | --- | --- |
| Paper Money baseline material identification | 1903, I:423 | PM01 | page image verified; recorded scan page 723 |
| Bretschneider criticism transmitted by Cordier | 1903, I:430 | PM02, PMT01 | page image verified / PAGE_VERIFIED; scan 732 |
| Laufer correction of Bretschneider and endorsement of Polo, transmitted by Cordier | 1920, 70–72 | PM03, PMT02–03 | page image verified / PAGE_VERIFIED; scans 84–86 |
| Earlier Arbre Sec identification, including the existing objection/response context | 1903, I:113, 128 | ARBR-ID-1903 | PAGE_VERIFIED_BOTH |
| Houtum-Schindler competing identification | 1920, 31 | ARBR-ID-HS | PAGE_VERIFIED_BOTH |
| Cordier bibliographical reply, without established adoption | 1920, 31 | ARBR-REPLY-CORDIER | PAGE_VERIFIED_BOTH |

Files:

- [Historical claim events](../../data/yule_cordier_claim_events.csv), blob `807e2aeef5054553e59de1cd017a216dfa46283d`.
- [Paper Money stance traces](../../data/paper_money_archival_stance_traces_v1.csv), blob `7a032f814536911fa27001dbbb93660cd0f67221`.
- [Verified proposition panel](../../data/r3_verified_proposition_panel_v1.csv), blob `f1ffa2aefde17f731fc9d0a19781aed81c94622c`.
- [Earlier historical findings prose](../r3_historical_results_source_round_v1.md).

The three short Paper Money quotations in Section 2 are copied from the registered stance traces, not newly transcribed from page images during this writing pass. The scan numbers above are the ledger's recorded scan-page labels; they should not be silently treated as zero-based PDF indexes. Printed page numbers are used in the prose.

**Authority boundary:** this writing pass inspected source ledgers and prior verification records. It did not perform new independent page-image adjudication. Before submission, check the quotations against the fixed PDF witnesses and inspect the surrounding paragraphs, not only the extracted cues. Do not treat a later Gutenberg aggregation as an additional independent historical witness. Do not date the origin of a transmitted argument simply by the 1903 or 1920 editorial layer.

**Granularity boundary:** PM03 remains a compound event containing correction plus endorsement. Its separately verified stance cues are not evidence that the implemented last event is already split into atomic acts. Arbre Sec is the cleaner act-level sequence.

<a id="e2"></a>
### E2. Natural sequences and the controlled history contrast

Governing documents:

- [Paper Money protocol](../../audits/mother_problem_redesign_20260929/NATURAL_QUALIFIED_COMPOSITION_PAPER_MONEY_PROTOCOL_v1.md).
- [Pre-implementation history-binding amendment](../../audits/mother_problem_redesign_20260929/NATURAL_QUALIFIED_COMPOSITION_PAPER_MONEY_HISTORY_AMENDMENT_v1.md).
- [Arbre Sec act-level protocol](../../audits/mother_problem_redesign_20260929/NATURAL_ACT_LEVEL_COMPOSITION_ARBRE_SEC_PROTOCOL_v2.md).
- [Natural act-level composition result](../../audits/mother_problem_redesign_20260929/NATURAL_ACT_LEVEL_COMPOSITION_RESULT_v2.md).

Successful result: `NATURAL_ACT_COMPOSITION_REPLICATION_PASS`; workflow run `36569809971`; head `45bc27858f8a1c1178f661563af19fca038c4f06`; artifact `11034225348`; ZIP SHA-256 `c3dea98b89508f2b1726a623c59664319e0c9292f05dddf10c7371dbff355ffe`.

Paper Money: `ADD_ALTERNATIVE ; RESOLVE`. Premature PM03 is rejected as `RELATION_TARGET_NOT_LIVE`. With the current assertion projection held fixed, erasing the registered evidence/event/transition histories changes PM03 from qualified to `RELATION_TARGET_HISTORY_UNRESOLVED`.

The amendment makes the current PM02 status relation-neutral, changing its protocol-only status from `EDITORIAL_CRITICISM_ASSERTED` to `ASSERTED`. The claim that PM02 entered as a criticism remains in the transition record. This placement is explicitly disclosed in Section 2; the manuscript does not assert necessity of one storage location across every representation.

Arbre Sec: `ADD_ALTERNATIVE ; RECORD_EVIDENCE`. A premature reply is rejected when the proposed identification is not live. Once qualified, the reply changes the retained evidence/history projection while preserving the current assertion projection. Explicit Cordier adoption of the competing identification is not established.

The same independently implemented engines handle both sequences without episode-name or claim-ID branches. A preceding execution stopped because of the incorrect CSV field name `pass1_note` instead of `act_note`; the successful result document records this without changing the scientific cases or source readings.

**Evidence type:** natural documentary sequences; exposed/development analysis; controlled deletion and order interventions; one historical corpus. Not naturally observed information loss, prospective fresh replication, historical prevalence, or automatic relation extraction.

<a id="e3"></a>
### E3. Typed signatures and the scope of equivalence

- [Signature typing amendment](../../audits/mother_problem_redesign_20260929/ACTION_RELATIVE_EQUIVALENCE_SIGNATURE_TYPING_AMENDMENT_v1.md).
- [Action-relative state-equivalence and sequence-closure result](../../audits/mother_problem_redesign_20260929/ACTION_RELATIVE_STATE_EQUIVALENCE_SEQUENCE_CLOSURE_RESULT_v1.md).

`Sigma(g)=(Beta(g),Kappa(g))` separates event/relation binding conditions from current-state and retained-history qualification conditions. Exact target identity is not interchangeable with whether that target is live/current.

The manuscript uses `Q_g` as a Boolean qualification predicate and `Gamma` as the set of qualified action types. Rejection reasons remain separate diagnostic outputs. `S` denotes the full represented state, while `Psi(S)` denotes the registered current assertion projection. In the equivalence statement, the event binding is fixed and admissible; state predicates are evaluated with respect to that same binding.

If the specified rule factors through the registered state-side projection, equal projections imply equal qualification. This implication follows from the specification; finite passing counts are not presented as a proof over unrestricted states. The empirical burden is the source interpretation, appropriate specification, implementation conformance, perturbation coverage, and composed dependencies.

**Review question still open:** distinguish a later source's assertion that it corrects a prior criticism from independent retained support for the target's critical role. The event relation label may carry a presupposition about history. The manuscript must not turn a contract requiring that presupposition to be independently grounded into a claim of information-theoretic impossibility when the event itself, another carrier, or permitted source access could establish it. This is a priority for the substantive red-team, not a reason to silently redesign the frozen rule.

<a id="e4"></a>
### E4. Action-relative requirements

- [Cross-ecology qualification signature result](../../audits/mother_problem_redesign_20260929/CROSS_ECOLOGY_GENERATOR_QUALIFICATION_SIGNATURE_RESULT_v1.md).

Result run `36660547327`; artifact `11073604129`; artifact SHA-256 `f9e79482a251fa58d41072458de6ba16c26be26cead38f67b352b6e3854c8ce0`.

Focal contrasts: Paper Money RESOLVE requires retained target-entry history; Arbre Sec RECORD_EVIDENCE does not. Formalization Papers RECORD_RESPONSE requires the registered target history; REVISE_PUBLICATION_STATUS does not. Both Yule ADD_ALTERNATIVE contexts are history-nonrequiring for the registered qualification. Formalization RECORD_REVIEW is the initial review action rather than an action requiring an earlier review entry; REPLACE_FORMALIZATION inspects the registered target validity/current conditions without requiring prior transition history.

Table 2 deliberately summarizes focal contrasts rather than claiming to list every source, relation, proposal, cardinality, value, or status check. `NOT_REQUIRED` concerns qualification for the specified action, not all scholarly uses, retrospective explanation, or permission to delete the source history.

<a id="e5"></a>
### E5. Finite equivalence, required-condition, and sequence checks

- [Authoritative closure result](../../audits/mother_problem_redesign_20260929/ACTION_RELATIVE_STATE_EQUIVALENCE_SEQUENCE_CLOSURE_RESULT_v1.md).

Run `36661636458`; head `56b26c6f53001b55eabb23c9f91370fed5225f2d`; artifact `11074423748`; ZIP SHA-256 `b94d1335c155c3e8d9f07b519e92ecea57b53349ca72c6ddbc078a28a45cd0f7`.

| Result | Denominator and meaning |
| --- | --- |
| 120/120 equivalent-context qualifications preserved | 116 Formalization contexts plus 4 Yule contexts |
| Formalization context breakdown | 48 review + 8 replacement + 52 response + 8 publication-status |
| 393/393 REQUIRED witnesses | Registered event-binding and state-side counterfactuals, not 393 historical documents or history-only ablations |
| 19/19 NOT_REQUIRED invariance witnesses | Registered nonrequired-history perturbations |
| 52/52 Formalization sequence checks | Connected eligible chains, with shared roots and records |
| 2/2 Yule sequence checks | Paper Money and Arbre Sec |

Three Yule witnesses couple target identity with live-target lookup: Paper Money ADD_ALTERNATIVE, Arbre Sec ADD_ALTERNATIVE, and Arbre Sec RECORD_EVIDENCE. They cannot identify those dimensions independently in the Yule cases. The result records this limitation; the manuscript retains it.

These are finite conformance and contrast counts. Do not add them together as a natural corpus size, call them independent observations, calculate a generalization accuracy from them, or relabel them as prospective external confirmation.

<a id="e6"></a>
### E6. Formalization Papers corrected reproduction

- [Corrected reproduction result v2](../../audits/mother_problem_redesign_20260929/FORMALIZATION_PAPERS_CORRECTED_REPRODUCTION_RESULT_v2.md).

Source: `LaraHack/formalization_papers_supplemental`, frozen v1.0 population, commit `2f68d8498aeeb724e3438deda13e74ae7fb076d8`; first-opening archive SHA-256 `c2349aa34350dc5f02f3ad7ccfc1ff6f879e88950fee948b0d5ffa206d4ca9e3`.

Authoritative first prospective run `36657856767` remains `INVALID`. Corrected run `36659349160`, head `92f16bf4e0476890851409be951bdce06a58ed43`, artifact `11073656774`, ZIP SHA-256 `3819e4cd06fe4b22a6a68aaa4ca3ee01515fac08b25ac4cdb63e61463bf46e8d` is `POST_FRESH_CORRECTED_REPRODUCTION_PASS`.

The corrections address dateTime lexical precision between parsers and preservation of multi-valued creator relations. The audit records 404 nanopublications: 379 with one creator and 25 with two. These counts explain the implementation correction; they are not the denominator of the composition result. Corrected independent parsing is exact across the ten source record files and registered components.

The population has fifteen roots: eight complete eligible roots and seven ambiguous/nonfunctional roots. All roots receive dispositions. The frozen grammar yields 52 eligible connected chains; all 52 meet the corrected test criteria. The raw-source documentary auditor independently reconstructs the root and chain sets and agrees exactly. No alternate archive, selected subset, or published-index fallback is substituted for the first-opening bytes.

**Independence boundary:** independent source ecology, separate implementations, and separate documentary reconstruction do not mean independent human historical adjudication or a new research team. The corrected result does not restore freshness. The manuscript makes neither claim.

<a id="e7"></a>
### E7. Representation comparator

- [Action-availability comparator result](../../audits/mother_problem_redesign_20260929/FORMALIZATION_PAPERS_ACTION_AVAILABILITY_COMPARATOR_RESULT_v1.md).

Run `36659894077`; artifact `11074295756`; ZIP SHA-256 `2209e07c8b5231e434f1b369cade010d8ea9826b45bf8e9d67156da1ed2f526a`.

Three project-defined comparators are `B_RELATION_TARGET`, `B_LIVE_TARGET`, and `Q_FULL_HISTORY`. Table 3 reproduces their distinct denominators: 52 valid response contexts, 47 natural functional-but-non-live target response acts, 52 controlled same-current-state history-ablated contexts, and one nonfunctional-target control. Decision extensions were deduplicated for the response-context denominator.

The registered negative conditions predate the comparator outcomes, but the comparator is an exposed mechanism audit. “False availability” is relative to that source/qualification contract. It is not a judgment on an author's freedom to respond or a score for PROV, TEI, Git, or all possible provenance-aware implementations.

<a id="e8"></a>
### E8. Native-text recovery boundary

- [Earlier closure status](../../experiments/deepening_v1/MOTHER_PROBLEM_CLOSURE_STATUS_v1.md), Gate II and Gate III, E2.
- [Historical evidence-layer claim ledger](../../experiments/deepening_v1/R3_EVIDENCE_LAYER_CLAIM_LEDGER_v3.md).

The earlier closure record reports `NATURAL_GUTENBERG_PLAINTEXT_BINDING_ATTRITION = NOT OBSERVED`. When the relevant later passages were supplied, alternative textual carriers retained the five historical distinctions tested. This is why Section 7 rejects a generic format-inherent loss claim.

The native recovery result is a prior project result, not rerun for this manuscript. Its relation to the dynamic ablations must stay explicit: an ablation removes a declared carrier under a fixed access contract; recovery from an intact source uses another admissible carrier or expands access. A final supplement should link the precise native recovery run and artifacts in addition to these status/ledger references.

<a id="e9"></a>
### E9. Historical adjudication remains bounded partial

- [Local execution report](../../experiments/deepening_v1/llm_second_pass_v1/LOCAL_EXECUTION_REPORT_2026-09-27.md).
- [Frozen result summary](../../experiments/deepening_v1/llm_second_pass_v1/RESULTS_v1.md).

Five cases, three prompt-order variants, three local models: 45/45 calls completed and parsed as JSON. Nine passed the frozen citation validator; 36 did not. All 21 atomic components are `NO_CONSENSUS` under the valid stable two-model rule. The formal disposition remains `BOUNDED_PARTIAL`.

Raw output SHA-256 `d648a61b6ef6ecaaf50e0d25de27538233a0eff68c869750338aaba82fb4e248`; frozen analysis SHA-256 `70b9971933fedaf3628153c8838881c503a0cb7a976e17f3c843a6b31d587730`.

The earlier Paper Money categorical-warrant model experiment is a separate study, despite also having 45 calls. Do not mix its packet conditions, null result, or denominator with this historical adjudication experiment. Neither is newly rerun or upgraded in this writing task.

## Literature verification and positioning

The first draft cites original publication pages or official specifications, not merely the prior audit's comparisons. Birnbaum and Spadini (2020), Bleeker et al. (2022), and Broyles (2020) were checked through their DHQ HTML articles. Vancisin et al. (2023) was checked through the publisher's article text; its authors are Tomas Vancisin, Loraine Clarke, Mary Orr, and Uta Hinrichs, and its pages are 1322–1339, DOI `10.1093/llc/fqad020`. Williamson (2026) was checked through the publisher/DOI search text including the abstract and substantive passages; the article is by Elizabeth R. Williamson, pages 1705–1723, DOI `10.1093/llc/fqag062`.

The official PROV-DM and TEI revisionDesc pages support only the limited representational statements made. No inability of either standard to represent the tested distinctions is alleged. The file's revision history and the historical acts described by that file are explicitly distinguished.

For Nash, Segoufin, and Vianu (2010), the bibliographic record and abstract/full-text excerpt were checked through the author-uploaded record after the ACM landing page failed to load. The article establishes an existing determinacy/rewriting research context; the manuscript does not claim to reproduce or improve its technical theorems. A full technical comparison belongs in the subsequent novelty audit.

This is a checked first-draft dialogue with selected neighbors, not a completed exhaustive literature review. In particular, it does not establish priority over all action theories, workflow models, temporal provenance, argumentation frameworks, or scholarly-editing theories. The manuscript's novelty claim must remain the concrete conjunction of source-grounded editorial distinctions, typed action-relative obligations, contrastive controls, and tested continuations.

## What has been completed in this writing pass

| Work package | Delivered now | Not implied |
| --- | --- | --- |
| Humanities re-anchor | Working title, opening humanistic question, Paper Money/Arbre Sec spine, three contribution claims | That all historical interpretation or disciplinary positioning is settled |
| Evidence compression | Claim/evidence matrix; main text limited to paired historical cases, action contrasts, and one external ecology | Deletion or downgrading of frozen research records |
| Integrated rewriting | A new continuous manuscript with abstract, eight sections, three tables, conclusion, references, and evidence statement | Camera-ready prose, author approval, or final venue formatting |
| Submission red-team | Priority objections and explicit readiness gates below | Independent reviewer acceptance or completion of the full four-perspective red-team |

## Submission gates still open

### A. Source and humanistic argument

Recheck the short quotations and surrounding paragraphs against the original fixed page images. Confirm the printed/scan/index distinctions and exact bibliography of the primary witnesses. Test whether the treatment of Paper Money's compound final intervention is adequate for the claim, without retrospectively pretending it was an atomic sequence. Expand intellectual/editorial context where needed to explain why the target and responsibility distinctions matter to a textual scholar, rather than supplying more computational cases by default.

### B. Novelty and specification challenge

The central objection is not merely “history matters.” A reviewer can reasonably ask whether the rules make the observed dependence true by construction. Section 3 and the limitations acknowledge that qualification is contract-relative and that the equivalence implication follows from factorization. The red-team must still examine the difference between later-act labels that presuppose a history and independent retained evidence of that history; identify admissible alternative carriers; and compare the precise contribution against query determinacy, provenance, versioning, and action-precondition traditions. This cannot be marked passed solely because the tests reproduce their specifications.

### C. Evidence and reproducibility

Read the actual retained outputs behind the result reports when doing the final claim-to-evidence audit. Preserve the first Formalization INVALID label, the corrected reproduction label, the comparator's exposed status, and Gate II BOUNDED_PARTIAL. Confirm that all 120/393/19 counts and 52/2 sequence denominators retain the distinctions recorded above. Package the exact runtime/oracle, frozen scientific inputs, and durable result access rather than relying only on transient workflow artifact availability. No fresh experiment is automatically required by this gate; a new experiment would need a specific unresolved claim and separately frozen protocol.

### D. Figures and reading experience

The present manuscript has three Markdown tables and no completed figures. Two potentially useful figures are specified, not delivered:

1. **Paired editorial continuations:** Paper Money above, Arbre Sec below. Show historical actors and mediators separately, target arrows explicitly, and the contrast between changed assertions and changed history. PM03 must be labeled as a compound event. Use source loci, not only action enums.
2. **Same assertions, different qualification:** a before/after view in which the two current assertion panels are identical but the critical entry relation is missing from one history panel. Label deletion as a controlled intervention, never as an observed Gutenberg transformation. A side panel can show Arbre Sec's nonrequired-history control.

The final choice should reduce reading burden, not duplicate every table or convert the paper into a workflow diagram. No visualization or user-study benefit has been tested.

### E. Author and venue preparation

No author list, affiliation, funding statement, contributor role, ethics determination, or journal-specific disclosure has been invented. Obtain author review and supply the actual declarations, including any required account of AI-assisted writing, before submission. Convert the E-notes to the chosen venue's supplementary/reference style, check word and figure limits, proofread notation, and produce the publication-format file only after the substantive text is accepted.

## Scope stop rule

Do not reopen corpus collection or run eLife/TMLR/OpenReview merely to improve the appearance of confirmation. eLife remains PRE_DATA at the scientific baseline used here. New empirical work should follow a specific unresolved claim exposed by review of this actual manuscript, not a generic expectation that a strong paper always needs another PASS.
