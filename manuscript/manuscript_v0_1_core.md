# When Is a Scholarly Representation Enough?
## Auditing Recovery and Use in Digital Scholarly Resources

Working manuscript core v0.1 — 2026-09-26

**Revision status.** This is a replacement core, not a submission-ready paper. It incorporates the post-result audit at Actions run 36244824296. It does not supersede the frozen experiments. Complete native-normalization replay, executable subset decoders and the historical source appendix remain submission tasks. Figures remain schematic specifications for author production.

## Abstract

Digital scholarly resources preserve texts together with selected structures, attributions, links and editorial distinctions. Evaluating those resources requires separating three questions: whether an answer remains determined by the retained information, whether a permitted procedure can recover it, and how a subsequent interpreter uses it. We develop a source-bound audit for making these distinctions explicit in task-relative comparisons. The audit registers a scholarly question, a source hierarchy, a representation transformation, permitted recovery operations and a precisely delimited output. Preservation requires an exhibited recovery procedure; claims of information loss require a counterexample to the complete retained representation rather than failure of one decoder. Historical Yule-Cordier materials motivate the access problem, while published Frankenstein, Whitman and Faust data provide independent source structures for testing the audit. A reassessment of 493 Frankenstein collation units reduces 166 raw-string grouping disagreements to five under two simple normalization diagnostics, showing that apparent relation loss can instead reflect an inappropriate reconstruction rule. Whitman and Faust expose concrete ambiguities in manuscript and source binding, including 20 ambiguous Whitman keys after printed locus, local locus and certainty are retained, and 53 Faust assertions carrying multiple source elements. A separate three-model adjudication experiment does not support its predicted categorical warrant contrast. We retain that null and distinguish it from a later conditional argumentation illustration. The resulting account treats representation adequacy as a claim requiring inspectable source and recovery evidence, not as a global measure of richness.

## 1. Introduction

A scholar may encounter a historical statement in a transcription while missing the note that identifies its source, the later correction that revisits it, or the editorial convention that determines how it can be compared with another witness. Conversely, a purpose-built representation may make a comparison easier without reproducing the documentary organization of its inputs. These are not simply differences between complete and incomplete copies. They concern which scholarly operations a particular representation supports and what must be reconstructed before an answer can be used.

Our historical starting point is the Yule-Cordier editorial record of Marco Polo. A base description associates paper money with mulberry bark. A 1903 editorial note transmits Bretschneider's objection to that identification, and a 1920 addendum transmits Laufer's response. The study's source registry distinguishes printed witnesses from their searchable digital assembly and records page-image checks for this chain. Preserving the initial passage does not itself establish that a reader following a particular digital route will encounter its subsequent discussion. Encountering all three passages, in turn, does not settle whether a disputed statement is admissible evidence, accepted belief or historical fact. Those are different questions.

The paper does not introduce the proposition that editions are interpretive or that representation depends on purpose. Pierazzo's account of digital documentary editions already makes selection and stopping decisions central [P1]. Birnbaum and Spadini explain how normalization shapes both collation and interpretation, including examples from Frankenstein [P2]. Database work has formally distinguished the information required to determine a query from procedures that reconstruct its answer [P3, P4]. CRMinf represents reasoning, inference and belief adoption in cultural-heritage settings [P5]. These are foundations and close comparators, not gaps to erase with new terminology.

Our candidate contribution is an executable audit connecting a specific scholarly question to a source-grounded representation and a permitted recovery procedure. The audit is designed to reject three shortcuts: treating the failure of a simple decoder as proof of irrecoverable loss; declaring carrier coordinates necessary because they appear in the output schema; and using an interpreter's behavior as an unexamined definition of warrant. The case studies reveal both useful representation-specific distinctions and places where earlier, stronger formulations of our own claims exceeded the tests.

## 2. Source-to-task audit

### 2.1 Register the task before comparing representations

Let X_K be the source states admitted by an evidence contract K. The contract specifies the evidence horizon, source identity, permissible background, recovery operations and resource restrictions. For a scholarly task tau, F_tau(x) is the required output at source state x. Examples include a manuscript endpoint set, a source-qualified temporal constraint or a witness partition under a named collation convention.

A carrier is a concrete means by which a distinction is exposed: an XML attribute, a pointer, an attached note, a normalized token or an explicitly documented identity relation. It is not automatically a necessary field. A task may recover the same distinction from a different carrier.

For retained carrier subset S, write phi_S(x) for the complete visible representation, including any permitted side information. Representation comparisons must hold the task fixed. A report that a narrower question can be answered from fewer fields is legitimate, but it does not establish preservation of the original question.

### 2.2 Separate determinacy from implemented recovery

The information-level condition is:

\[
\phi_S(x)=\phi_S(x')\quad\Longrightarrow\quad F_\tau(x)=F_\tau(x')
\qquad(x,x'\in X_K).
\]

This is an application of established determinacy reasoning, not a new representation theorem [P3, P4]. A pair with identical visible input and different required outputs is a counterexample to sufficiency on the stated domain. The comparison must include all retained coordinates. Repetition of an identifier alone is not a counterexample when other visible coordinates might disambiguate it.

Operational recovery makes an additional demand: an admissible procedure d must produce F_tau(x) from phi_S(x), within the declared operations and budget. A theoretically unique answer may lack an implemented recovery path. Conversely, a procedure's failure does not establish that the information was absent.

These distinctions matter on finite corpora. Unique record IDs can make a target appear determined through memorization. An inverse lookup table constructed using the withheld answers is not free background. Its source, construction and access cost must be declared. The current study therefore separates observed key uniqueness, an exhibited source-authorized decoder and a general determinacy claim.

### 2.3 What a preservation certificate must show

A task-preservation certificate records the exact source/version, task input and output, transformation, visible carriers, admissible decoder, comparison population and outcome. Every supporting pointer or normalization rule must have a native or explicitly controlled basis. The certificate must identify additional information read during recovery; reopening a richer source is a valid recovery route only under a contract that permits it.

For a minimum within a finite candidate carrier family, a successful decoder establishes sufficiency. Every asserted removal failure then requires either a counterexample to the full retained interface or failure under an explicitly restricted decoder family. We distinguish information-relative minimality from decoder-relative minimality. A list of fields that a programmer declares necessary is neither by itself.

### 2.4 Keep documentary state separate from evaluation

The documentary layer records responsibility, citation, attachment, witness identity, temporal organization and explicit editorial modality. It does not silently encode our final acceptance judgment. Source statements such as a scholar's criticism or endorsement can be recorded as attributed historical acts without automatically treating them as successful defeats or support.

The final evaluator is another declared component. It may be a retrieval procedure, a structured comparison, an LLM rubric or a formal argumentation semantics. Their outputs are not interchangeable. A claim about the availability of criticism is not already a claim about belief revision.

## 3. Materials and evidence authority

The Yule-Cordier material is a purposive historical case, not a representative sample of editions. Printed witnesses provide the authority for historical quotations and attribution. Gutenberg supplies a native digital object for search and navigation studies. The two roles are recorded separately in the source registry [D1].

Frankenstein Variorum, Whitman's 1855 relations list and Faust macrogenesis supply independently authored structures [D2-D4]. Their independence concerns data and scholarly infrastructure: it does not automatically validate the tasks or decoders introduced by this study. Frankenstein files are identified as collation-workspace products at a pinned commit, not an unquestioned gold standard for interpretation. Scrivener's corrigenda provides a separately selected localization example, not an additional large corpus.

Four forms of evidence remain distinct: native-object description; controlled or workflow comparisons; prospective held-out runs; and post-result diagnostics. The normalization and conditional-key checks reported below belong to the last category. The prior C18 run remains unchanged, but C18 is no longer untouched material for subsequent tests. The three local-model results are also retained unchanged.

## 4. Audited results

### 4.1 Frankenstein: reconstruction rules are part of the comparison

The original C18 evaluation compares native witness groups with equality of serialized reading content after whitespace collapse. It reproduces 166 partition disagreements across 493 app units, 267 of which contain multiple groups. All original mismatches split a native group. However, the reading strings contain escaped documentary markup: line breaks, page identifiers and other structures remain within the strings being compared.

In a post-result diagnostic, removing serialized XML tags reduces the mismatch count to 25. Adding case folding and an ampersand-to-and normalization reduces it to five. The latter result includes one within-group split and four between-group merges. Thus normalization is not simply a monotone improvement toward a universal correct text. It can remove distinctions that the native collation retained.

For example, a manuscript reading of `benevo<lb .../>lent` and printed `benevolent` occur in distinct native groups. Stripping the line marker merges them. The native normalization descriptors expose the difference as `benevo lent` versus `benevolent`. This is a concrete contract difference, not proof that the groups contain information unattainable from the source readings.

The supported result is that the specified raw decoder does not recover the native partition. The stronger claim that no reading-based recovery can do so is withdrawn. A submission-level comparison must replay the project's normalization contract rather than stop at a knowingly weaker equality baseline. P2 and the upstream workflow documentation establish why that comparator is necessary.

### 4.2 Whitman: binding ambiguity survives a fuller retained key

The native relations file contains 1,444 valid two-endpoint links. Its local manuscript locus identifiers are scoped by file. Ninety-one local-locus keys appear with multiple manuscript files, but this alone does not prove the file coordinate necessary after the printed locus is retained.

The audit therefore conditions on progressively fuller keys. Printed locus plus manuscript-local locus yields 25 ambiguous keys, covering 52 records. Adding certainty still leaves 20 ambiguous keys, covering 41 records. One example associates `(ppp.01880.xml#l1045, #l01, high)` with two manuscript files, `duk.00261.xml` and `uva.00262.xml`.

These are stronger record-local witnesses than the original identifier-frequency count. They locate a specific binding ambiguity without claiming that every conceivable whole-document decoder fails. A complete minimality result still requires stating whether ordering, group context and auxiliary mappings remain visible, then comparing reconstructed endpoint sets for the actual projected interface.

### 4.3 Faust: source identity is set-valued

The pinned raw-assertion ecology contains 1,089 eligible temporal assertions. Fifty-three have more than one source element. An implementation that reads only the first source therefore changes the target from complete native provenance to a first-source projection.

The corpus contains 1,959 adjacent-constraint occurrences but 1,015 unique directed constraints. The conflict analysis identifies 20 nontrivial strongly connected components involving 118 nodes. Internal conflict constraints number 612 occurrences and 207 unique directed edges. The distinction between occurrences and unique edges is retained in all reports.

Source-set ambiguity occurs in five file keys. After retaining file and complete ordered item sequence, eight keys remain associated with different source sets. On the conflict-edge task, three file-plus-edge keys have multiple source sets. These observations show that source provenance is not simply synonymous with file membership. They do not yet establish a unique minimum across all retained carriers, particularly source locators. The revised decoder must preserve complete source sets and expose the information it actually uses.

### 4.4 Historical access and the null adjudication result

The earlier paper-money runs compare access/navigation policies over identified Gutenberg objects. They document whether the later response is surfaced under a specified candidate budget. Those results remain policy-relative observations; neither a target ranking nor the presence of a criticism supplies an automatic acceptance judgment.

The final local-model study made 45 independent calls: five evidence-packet conditions, three order/identifier variants and three models. Qwen2.5 7B is unstable on one packet; Gemma3 12B and Llama3.1 8B return RETAIN throughout. The frozen selective-restoration prediction is unsupported.

A delivery audit confirms the frozen input digest, call IDs and evidence-ID references. Every raw receipt reports a normal stop, with recorded prompt counts below 6,119 tokens against a configured 16,384-token context and outputs below 299 tokens against a 1,024-token generation limit. There is no positive evidence of limit-induced truncation. Equal six-unit packets nonetheless range from 2,103 to 2,401 candidate words, so unit count should not be described as equal reading burden.

The null is not reclassified as proof that the models are incapable of evidential reasoning. The prompt asks about admissibility as evidence, which can remain despite dispute. Some outputs acknowledge the criticism while retaining admissibility. The result establishes failure of the predicted categorical contrast under this rubric, not a unique causal diagnosis of why.

## 5. Conditional consequence, not replacement confirmation

After the LLM result, the study introduced a directed graph of a base assertion, an objection and a counter-objection. Under that graph, grounded semantics yields the familiar reinstatement pattern. Dung's framework supplies the semantics [P6]; the new empirical work does not supply a new acceptance theorem.

The analytical question is whether the historical acts warrant the chosen graph. Treating the base disagreement as mutual rebuttal changes the no-correction status from OUT to UNDECIDED. Treating the counter-disagreement as mutual as well can leave the focal argument UNDECIDED both before and after the added passage. These illustrative alternatives are not all claimed to be historically equally appropriate. They identify the mapping assumption on which the result depends. Structured argumentation also distinguishes attacks on premises, conclusions and inferences; an explicit criticism is not automatically one particular successful defeat [P7].

We therefore retain the formal construction as a post-result model illustration, not an empirical rescue of the failed judge prediction. Correct computation was checked against enumeration of complete extensions over all 512 directed three-node graphs. This verifies the small-graph implementation, not the archival interpretation.

## 6. Discussion and bounded completion requirements

A robust account of scholarly representation should be able to find harmless compression, recoverable reorganization and consequential ambiguity. It should also be able to reject its own tests when the proposed decoder is weaker than the native workflow or the inference exceeds the observed projection. The present audit demonstrates that these are practical distinctions: serialized markup accounts for much of one apparent collation failure, while concrete endpoint and provenance ambiguities remain after fuller conditional checks.

The intended humanistic contribution concerns the conditions under which an edition remains usable for revisiting a claim, not a universal claim that more structure produces better scholarship. The Yule-Cordier narrative must remain centered on who made each statement, which earlier statement was addressed, and what the editorial layering allows a later investigator to reconstruct. The external materials test the proposed audit across different native tasks without merging their counts into a leaderboard.

Three bounded tasks remain before submission. First, replace field-membership declarations with executable recovery/collision certificates for the named Whitman and Faust interfaces. Second, replay the native Frankenstein normalization contract and report provenance-preserving and distinction-collapsing operations separately. Third, finish the historical source appendix and integrated manuscript while keeping the LLM null and post-result formal illustration distinct. These tasks do not require new model recruitment, a new data collection or changing the completed experiments.

## References and evidence locations

[P1] Pierazzo, E. (2011). A rationale of digital documentary editions. *Literary and Linguistic Computing*, 26(4), 463-477. DOI: 10.1093/llc/fqr033.

[P2] Birnbaum, D. J., and Spadini, E. (2020). Reassessing the locus of normalization in machine-assisted collation. *Digital Humanities Quarterly*, 14(3). https://www.digitalhumanities.org/dhq/vol/14/3/000489/000489.html

[P3] Nash, A., Segoufin, L., and Vianu, V. (2010). Views and queries: Determinacy and rewriting. *ACM Transactions on Database Systems*, 35(3), Article 21. DOI: 10.1145/1806907.1806913.

[P4] Fan, W., Geerts, F., and Zheng, L. (2012). View determinacy for preserving selected information in data transformations. *Information Systems*, 37(1), 1-12. DOI: 10.1016/j.is.2011.09.001.

[P5] CIDOC CRM. CRMinf, formal ontology for argumentation and inference making. Official scope and versioned definitions, consulted 2026-09-26. https://cidoc-crm.org/crminf

[P6] Dung, P. M. (1995). On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games. *Artificial Intelligence*, 77(2), 321-357. DOI: 10.1016/0004-3702(94)00041-X.

[P7] Prakken, H. (2010). An abstract framework for argumentation with structured arguments. *Argument and Computation*, 1(2). DOI: 10.1080/19462160903564592.

[D1] Study source registry and Yule-Cordier alignment ledger. Printed-witness verification and searchable Gutenberg objects retain separate roles.

[D2] FrankensteinVariorum/collationWorkspace, commit 5a208f869ff1213defa000e3181d5315a072a15f, C18 complete apparatus and repository README.

[D3] whitmanarchive/whitman-LG_1855_variorum, commit 25a00b7ebbdbc5246fce65a333bc761a5c22dad4, source/authority/anc.02134.xml.

[D4] faustedition/faust-xml, commit 502eca65120dd6189ceaf41d4e5017775e6e4677, xml/macrogenesis.

[D5] Audits/cold_start_20260926 diagnostic protocol, code and Actions run 36244824296. Exact source bytes, identities, detailed counts and bounded examples are in artifact crr-cold-start-diagnostic-20260926.

[D6] User-supplied three-model final-run archive SHA-256 4d83876d90ac5e1a7417706d0137ef7cc767c470b5b17e113f5b5a65a27ad850. Local delivery audit reads its frozen calls and raw API receipts; it does not execute new calls.
