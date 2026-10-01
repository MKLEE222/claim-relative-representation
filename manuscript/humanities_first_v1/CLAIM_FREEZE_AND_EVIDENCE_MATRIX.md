# Humanities-first manuscript v1: identity and evidence freeze

Date: 2026-09-30  
Status: WRITING FREEZE / NOT AN EXPERIMENTAL PREREGISTRATION  
Evidence baseline: `c6f56fa17a5e3d02f16a336ed6e450b1843d8fb6`  
Governing planning documents: [domain-drift audit](../../audits/mother_problem_redesign_20260929/DOMAIN_DRIFT_AND_STRONG_PAPER_GAP_AUDIT_v1.md) and [acceptance handoff](../../audits/mother_problem_redesign_20260929/ACCEPTANCE_AND_NEXT_STEPS_20260930.md).

This document freezes the scope of the first integrated manuscript. It does not change source interpretations, outcome labels, registered tasks, experiment criteria, or the historical adjudication gate. The old manuscripts remain intact as research history.

## 1. Paper identity

**Working title:** After Revision: Preserving the Conditions of Scholarly Inquiry in Digital Editions.

**Mother question:** What must remain recoverable when a scholarly record changes, so that later researchers can determine which historically grounded acts of correction, attribution, and interpretation the record supports?

**Disciplinary identity:** digital textual scholarship and scholarly editing, with a source-bound computational account of continuing inquiry. The historical object is the Yule–Cordier editorial record, not a generic workflow platform. The formal model answers an editorial question; its notation is not the opening problem.

**Central distinction:** preserving a current assertion is not necessarily preserving the relations and history that justify a subsequent act upon it. Conversely, recording a scholarly act need not change the current assertion.

**Meaning of qualification:** an action is qualified under a declared source, representation, and access contract. This is neither a verdict on historical truth nor a restriction on a scholar's freedom to propose another interpretation. A failed qualification identifies what this representation has not established for this action.

## 2. Exactly three headline claims

### C1. Current assertions do not by themselves preserve all conditions of subsequent inquiry

Two representations can agree on the registered current-assertion projection while differing in whether a later source-bound correction is qualified. Paper Money is the main historical illustration. Its documentary sequence is natural; the deletion of history is a controlled transformation, not an observed historical loss.

**Licensed wording:** In the audited Paper Money representation, holding current assertions fixed while removing their entry history blocks the registered correction-of-prior-criticism action.

**Not licensed:** every plain-text edition loses this relation; no reader can reconstruct it; equal current projections imply equality of the complete scholarly record; the model establishes Polo's historical correctness.

### C2. Preservation obligations differ between scholarly actions

The later Paper Money correction requires entry history in the registered model. The Arbre Sec bibliographical reply requires its exact live target, but not that target's retained entry history. Formalization Papers supplies a second ecology with the same contrast between history-requiring and history-independent qualifications.

**Licensed wording:** Required distinctions are action-relative within the registered action and intervention families. The typed signature separates event/relation binding from state/history requirements.

**Not licensed:** a globally minimal representation; a universal metadata checklist; irrelevance of omitted history to all other questions; the novelty of purpose-relative representation itself.

### C3. Earlier scholarly acts establish conditions for later acts

In Paper Money, recording the criticism establishes both a live target and its critical relation to the earlier assertion. The later correction reads those conditions. In Arbre Sec, the competing proposal establishes the target of a later reply, without the reply resolving the identification. The independent ecology checks analogous write/read dependencies.

**Licensed wording:** Across the audited sequences, earlier acts create target, current-state, and sometimes history conditions required by later acts.

**Not licensed:** observed reversal of historical chronology; all natural sequences are noncommutative in the same sense; complete discovery of the available action vocabulary; a universal scholarly action algebra.

## 3. Historical spine and source anchors

| Role | Source object and location | Act and relation | Interpretive boundary |
| --- | --- | --- | --- |
| Paper Money baseline | Yule–Cordier 1903, vol. I, p. 423; ledger PM01; recorded scan page 723 | Narrative material-identification assertion | Model only the mulberry-bark material proposition, not every fiscal or historical claim in the passage |
| Paper Money criticism | 1903, vol. I, p. 430; PM02/PMT01; scan 732 | Bretschneider, transmitted by Cordier, criticizes PM01 | Transmission is not silently reassigned to Cordier as original critic |
| Paper Money later intervention | Cordier 1920, pp. 70–72; PM03/PMT02–03; scans 84–86 | Laufer, transmitted by Cordier, corrects Bretschneider and endorses the original material identification | PM03 is a compound event; its two stance traces do not make the current implementation an atomic-act decomposition |
| Arbre Sec earlier position | 1903, vol. I, pp. 113, 128; ARBR-ID-1903 | Oriental Plane identification | Earlier note already contains an objection and response; the model's starting state is a local projection, not the whole edition without history |
| Arbre Sec proposal | 1920, p. 31; ARBR-ID-HS | Houtum-Schindler's cypress proposal, transmitted by Cordier | 1920 is the transmission layer, not an assertion that the proposal originated then |
| Arbre Sec reply | 1920, p. 31; ARBR-REPLY-CORDIER | Cordier's bibliographical reply to that proposal | Earlier reading/citation does not establish adoption of the cypress identification |

Source ledgers: [claim events](../../data/yule_cordier_claim_events.csv), [Paper Money stance traces](../../data/paper_money_archival_stance_traces_v1.csv), [verified proposition panel](../../data/r3_verified_proposition_panel_v1.csv). These carry earlier page-verification records. This writing pass reads the ledgers; it does not claim a new independent page-image adjudication.

## 4. Claim–evidence–comparison–wording matrix

| Claim or boundary | Evidence and comparison | Main-text role | Allowed inference and ceiling |
| --- | --- | --- | --- |
| C1: same assertions, different correction qualification | [Paper Money history amendment](../../audits/mother_problem_redesign_20260929/NATURAL_QUALIFIED_COMPOSITION_PAPER_MONEY_HISTORY_AMENDMENT_v1.md); [natural v2 result](../../audits/mother_problem_redesign_20260929/NATURAL_ACT_LEVEL_COMPOSITION_RESULT_v2.md). Full state versus identical current assertions with evidence/event/transition ledgers removed | Detailed historical case | Contract-relative separation. PM02 status was made relation-neutral before implementation; the critical relation is carried in history. No claim of format-inherent or information-theoretically irrecoverable loss |
| C2: unequal history requirements | [cross-ecology signatures](../../audits/mother_problem_redesign_20260929/CROSS_ECOLOGY_GENERATOR_QUALIFICATION_SIGNATURE_RESULT_v1.md). RESOLVE versus RECORD_EVIDENCE; RECORD_RESPONSE versus REVISE_PUBLICATION_STATUS | One compact signature table | Conditional necessity and nonnecessity under the registered tasks; not a storage-deletion policy |
| C2: equivalent-state and required/nonrequired probes | [closure result](../../audits/mother_problem_redesign_20260929/ACTION_RELATIVE_STATE_EQUIVALENCE_SEQUENCE_CLOSURE_RESULT_v1.md). 120 contexts, 393 required-condition witnesses, 19 nonrequired-history witnesses | One compact results paragraph/table | Finite model checks, not 532 independent historical cases or a probability estimate. Required witnesses span binding and state dimensions, not history alone |
| C3: natural composition | [Arbre protocol](../../audits/mother_problem_redesign_20260929/NATURAL_ACT_LEVEL_COMPOSITION_ARBRE_SEC_PROTOCOL_v2.md); natural v2 result; closure result | Paired Paper Money/Arbre Sec explanation | Two exposed sequences in one historical corpus. Premature-action rejection tests partial availability; it is not an observed alternative chronology |
| C1–C3: independent mechanism | [Formalization corrected result](../../audits/mother_problem_redesign_20260929/FORMALIZATION_PAPERS_CORRECTED_REPRODUCTION_RESULT_v2.md). Frozen 15-root population; 8 complete and 7 ambiguous/nonfunctional roots; all 52 eligible connected chains | One bounded external-validation section | Independent source ecology and independent implementations, not independent historical adjudication. Chains can share roots and records. First fresh run INVALID; corrected reproduction PASS |
| Stronger comparator | [action-availability comparator](../../audits/mother_problem_redesign_20260929/FORMALIZATION_PAPERS_ACTION_AVAILABILITY_COMPARATOR_RESULT_v1.md). Functional targets, then current targets, then entry history | Small table in external-validation section | 47 natural non-live response acts and 52 controlled history-ablated contexts are different denominators. The full model keeps all 52 valid contexts. Comparators are defined projections, not benchmarks against PROV or every version-control system |
| Object-boundary false positives | [dynamic evidence map](../../audits/mother_problem_redesign_20260929/DYNAMIC_MOTHER_PROBLEM_EVIDENCE_MAP_v1.md), D0–D1 | One methods warning; research history in supplement | Early H 77/77 VOID and invalid StaBi object aggregation are not successes. Source-object identity precedes composition |
| Historical adjudication limitation | [Gate II local report](../../experiments/deepening_v1/llm_second_pass_v1/LOCAL_EXECUTION_REPORT_2026-09-27.md); existing PR #3 record | Explicit limitation | 45 calls completed; 9 passed frozen citation validation; none of 21 components reached valid stable two-model consensus. BOUNDED_PARTIAL, not successful independent validation and not historical refutation |
| Native-text recovery boundary | [historical source-round prose](../r3_historical_results_source_round_v1.md); [existing PR #3](https://github.com/MKLEE222/claim-relative-representation/pull/3) | Methods/limits, with exact experiment pointer to be checked before submission | The recorded native Gutenberg null rejects a generic claim that plain text inherently destroys the five tested distinctions. Reopening or reconstructing from full source changes the access contract |
| Typed identification limitation | closure result, section 9 | Short limitation; expanded supplement | Three Yule witnesses couple target identity and live lookup. Yule alone does not identify those axes independently; Formalization supplies separate probes |

## 5. How the formalism will be presented

The paper introduces the historical question and paired cases before `Sigma(g)=(Beta(g),Kappa(g))`.

For fixed admissible event binding, agreement on the registered state-side projection implies equal qualification in the registered model. If qualification is specified to factor through that projection, the implication follows mathematically from the specification. The empirical work concerns source-grounding, implementation agreement, finite perturbation witnesses, and sequence dependencies. The manuscript must not advertise this elementary implication as an unrestricted new mathematical theorem.

An action label is not supplied as the correct answer in the event input. Relation labels and target bindings nevertheless remain substantive source interpretations. Removing an operation label does not make historical interpretation assumption-free or automatically extracted.

## 6. Deliberate evidence compression

Main text: one historical spine, the action-relative comparison, one external ecology, necessary negative controls and limitations. No leaderboard across corpora.

Supplementary research history: earlier retrieval/access experiments; old categorical-warrant LLM null; historical Gate II details; object-boundary invalidations; parser repairs; full protocol/run/hash register; AAD/VGW and static carrier audits where needed for provenance of the research program.

Not part of the empirical identity: TMLR/OpenReview/eLife. No new DATA_OPEN, candidate screening, model rerun, or corpus collection is authorized by this writing task. eLife remains PRE_DATA at this baseline.

## 7. Literature dialogue to preserve

Birnbaum and Spadini already establish that normalization is interpretive and distributed across stages. Bleeker and colleagues already model revision layers rather than flattening them into linear text. Broyles already makes versioning sensitive to scholarly use and meaning, not merely storage. Vancisin and colleagues already connect provenance disclosure to transformations, labor, and interpretation. Williamson extends the critical treatment of digitized records' production and access contexts. None is to be dismissed as having ignored history.

Our narrower addition is a source-bound, executable comparison of the conditions for specified subsequent acts, including different demands after the same first act. PROV and TEI are possible representational substrates, not intrinsically deficient competitors. A definitive priority claim against all provenance or workflow research is outside this writing freeze.

## 8. Completion labels

Identity and evidence compression: implemented by this file, subject to revision if source checking exposes a conflict.

Integrated prose: a separate new manuscript, not an update to the frozen experiments or the obsolete v0.

Submission closure remains open until source-note/quotation checks, figure production, adversarial review of the actual prose, and venue-specific preparation are complete. This freeze is a writing decision informed by existing results, not a retrospective preregistration.
