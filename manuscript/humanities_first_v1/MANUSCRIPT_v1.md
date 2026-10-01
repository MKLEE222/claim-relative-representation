# After Revision: Preserving the Conditions of Scholarly Inquiry in Digital Editions

*First integrated working draft, 30 September 2026. This is a new manuscript, not a revision of the experimental record. Evidence baseline: `c6f56fa17a5e3d02f16a336ed6e450b1843d8fb6`. Bracketed E-notes link to the companion evidence register; submission preparation remains open.*

## Abstract

A scholarly edition can preserve an assertion while obscuring the relations that make a later correction intelligible. Conversely, an editorial intervention can change the history of a discussion without changing its currently represented conclusions. This article asks what must remain recoverable when a scholarly record changes so that subsequent acts of correction, attribution, and interpretation retain their documentary grounds. Two sequences in the Yule–Cordier editorial record of Marco Polo supply the central cases. In the Paper Money sequence, a criticism becomes the specific target of a later correction. In the Arbre Sec sequence, a competing identification occasions a bibliographical reply that does not establish adoption of the proposal. We formalize these differences through action-relative qualification: the conditions that a representation must establish before a specified scholarly act is supported under a declared interpretive and access contract. Controlled transformations show why equal current assertions need not preserve equal qualifications, while contrasting actions identify cases where retained entry history is not required. A bounded test in a second, machine-readable scholarly ecology examines the same distinction across connected review and revision records. The contribution is an executable account of preservation obligations for continuing inquiry, not a universal action vocabulary, an automated historical adjudicator, or a claim that plain text inherently destroys provenance.

**Keywords:** digital scholarly editing; editorial history; provenance; historical interpretation; scholarly revision; action-relative representation

## 1. The problem after a correction

A correction does more than replace one statement with another. It identifies something as requiring correction, assigns responsibility for the intervention, and establishes a relation between an earlier assertion and a later judgment. An edition that preserves only the resulting statement may remain adequate for reading that statement. It need not remain adequate for determining what was corrected, whose position was challenged, or what a subsequent response would be responding to. The editorial problem is therefore not exhausted by retaining the newest wording. It includes retaining the grounds on which the record can continue to be questioned.

The Yule–Cordier editorial record offers a concrete instance. Marco Polo's account of paper money contains a material identification involving mulberry bark. A note in the 1903 edition transmits Emil Bretschneider's criticism of that identification. Cordier's 1920 addendum then transmits Berthold Laufer's correction of Bretschneider and endorsement of the original material claim. Treating the final endorsement as a return to an earlier answer misses an important difference: the answer is now situated after a criticism and a correction of that criticism. Its place in the scholarly discussion has changed even where its normalized material content resembles the starting position (Yule and Cordier 1903, I:423, 430; Cordier 1920, 70–72).

Another entry prevents this observation from becoming a rule that every intervention updates the accepted answer. In the Arbre Sec discussion, Cordier transmits Houtum-Schindler's competing identification and then replies about his own earlier reading and citation of Schindler. The reply belongs to the history of the discussion, but it does not establish Cordier's adoption of the competing identification. Recording that reply as an identification update would add a commitment not warranted by the inspected passage (Yule and Cordier 1903, I:113, 128; Cordier 1920, 31).

These cases concern familiar editorial practices: distinguishing a commentator from the author quoted, identifying the target of an objection, and separating acknowledgment from assent. Their computational treatment matters because a digital representation must make choices about which of these distinctions remain available to later operations. Those choices are not neutral preliminaries to scholarship. Birnbaum and Spadini (2020) show that normalization in machine-assisted collation is interpretive and distributed across multiple stages, rather than confined to one technical step. Bleeker and colleagues (2022) similarly begin from the philological problem of in-text revision and develop a nonlinear representation through which a collation tool can respect revision layers. Both studies demonstrate that computational operations expose, rather than eliminate, scholarly assumptions.

We pursue a related problem at the level of scholarly interventions upon claims. What must remain recoverable when a scholarly record changes, so that later researchers can determine which historically grounded acts of correction, attribution, and interpretation the record supports? The emphasis is on the conditions of a subsequent act, not merely the intelligibility of a past change. A record can support a reply to a particular proposal only if that proposal is distinguishable as the reply's target. Some acts additionally depend on how the target entered the discussion. Others do not.

The article develops three claims. First, equal current assertions do not by themselves guarantee equal support for subsequent source-bound acts. Second, the relevant preservation obligations differ between acts: correcting a prior criticism and recording a bibliographical reply need not inspect the same historical conditions. Third, earlier scholarly acts can establish the targets and relations on which later acts depend. We make these claims through two historically situated readings, controlled representational comparisons, and a bounded external mechanism test. We do not infer the truth of an historical proposition from the successful execution of a rule.

## 2. A correction of a criticism: Paper Money

### 2.1 The documentary sequence

The Paper Money case spans three documentary layers. The base narrative, represented here by the 1903 edition, describes the use of mulberry bark in paper money. The editorial note on page 430 transmits Bretschneider's contrary judgment: “He seems to be mistaken.” The later addendum does not merely offer another botanical opinion. Laufer, as transmitted by Cordier, writes, “This is a singular error of Bretschneider,” and subsequently, “Marco Polo is perfectly correct.” The first statement addresses the prior critic; the second endorses the earlier material identification (Yule and Cordier 1903, I:423, 430; Cordier 1920, 70–72; [E1](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e1)).

The two targets are indispensable to the reading. Laufer's criticism is directed at Bretschneider, not at Polo, while the endorsement concerns Polo's material claim. Collapsing the passage into a single undirected relation such as disagreement would therefore misidentify its argumentative structure. Collapsing all statements transmitted in Cordier's edition into Cordier's own assertions would introduce a different error, one of responsibility. The documentary unit is not simply an editor, a page, or a topic. It is an intervention whose relation, target, and transmission can be distinguished.

Our reconstruction is deliberately local. It concerns the material-identification proposition needed to follow this criticism and correction. It does not cover every fiscal or administrative assertion in Polo's passage, establish the ultimate historical correctness of Laufer's account, or reconstruct the full development of the commentary across all editions. The earlier works quoted by Cordier are studied through that transmission rather than treated as independently inspected witnesses. The source register preserves printed loci, the project's recorded scan anchors, and the previously verified stance traces. The 1903 and 1920 labels identify the inspected editorial layers, not necessarily the first dates on which the arguments were formulated ([E1](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e1)).

### 2.2 Representing the intervention rather than only its answer

For the computational comparison, the three positions are assigned stable claim identifiers. PM01 is the baseline material claim. PM02 is Bretschneider's criticism as transmitted in 1903. PM03 is the later compound intervention transmitted in 1920. These identifiers distinguish documentary roles; their strings do not determine the operations that the engine selects.

| Documentary position | Relation represented | Consequence in the registered local model |
| --- | --- | --- |
| PM01: baseline material identification | Initial assertion | The baseline claim is available as a target |
| PM02: criticism of the identification | Contradicts PM01 | Add a competing assertion and preserve the relation by which it entered |
| PM03: correction of the prior critic, with endorsement of the original material claim | Corrects PM02; supports the material position represented by PM01 | Resolve the represented competition while retaining the intervening history |

**Table 1.** A local model of the Paper Money sequence. Resolution denotes the modeled consequence of the later source intervention, not the article's independent adjudication of the historical question. PM03 contains two stance acts in the documentary trace and remains a compound event in this implementation.

The first transition leaves PM01 and PM02 available as competing assertions. It also records that PM02 entered as a contradiction of PM01. The later intervention qualifies as a resolution only when its named target, PM02, is available and the relevant entry relation is retained. A generic replacement instruction would be weaker: it could replace an assertion without establishing that the replaced assertion was the criticism addressed by the source. The model thus separates obtaining the desired final value from representing the warranted route to that value ([E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

This separation enables a controlled comparison. Starting after PM02 has been recorded, we construct two representations with the same current assertion projection. One retains the transition, event, and evidence history. The other removes those ledgers while leaving the current assertions unchanged. The later PM03 intervention is then supplied identically to both. With history retained, the registered correction qualifies. With history removed, it is rejected because the history of the relation target has not been established. The difference is not between two observed historical editions. It is between two controlled representations of the same source-grounded local state ([E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

The design includes an important representational choice. Before implementation, PM02's normalized current status was changed from a label that already encoded its role as an editorial criticism to the relation-neutral label ASSERTED. Its critical relation to PM01 remained in the entry history. Otherwise, an experiment nominally deleting history would leave the disputed historical information duplicated in the current-status field. The amendment changes the location of the relation, not the historical reading. It also fixes the scope of the inference: the result concerns a representation in which that distinction is carried in the history being removed. It does not show that the distinction must always be stored in a chronological ledger ([E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

The humanistic consequence is specific. A later reader may know which material identification is currently represented without knowing whether a new passage corrects the original assertion, corrects its critic, or simply supplies parallel evidence. These are different scholarly acts, even when some produce similar normalized answers. To preserve their distinction is to preserve something about the continuing argument, not merely its latest content.

## 3. Researchability as qualified scholarly action

### 3.1 A declared scope of support

We use *qualification* for the conditions under which a representation supports a specified scholarly act. The term is intentionally narrower than validity in every scholarly sense. A qualified correction is not thereby historically true. An unqualified correction is not forbidden to a scholar. Rather, the current representation and declared evidence do not establish the conditions for recording it as that particular kind of intervention.

This distinction locates the authority of the model. It does not replace interpretation with a permission system. It makes an interpretation's representational commitments inspectable. Calling a passage a correction of a prior criticism, for example, commits the analysis to an identifiable prior criticism and to a defensible binding between the two interventions. A model that cannot exhibit that binding should not silently convert the passage into a generic update. It should expose the unresolved condition.

Qualification is evaluated under a declared contract: the source material available, the relations accepted from its interpretation, the represented state, and the forms of recovery permitted to the operation. Consulting another edition or reconstructing an omitted relation from the full passage can change the available evidence. Such recovery may be entirely legitimate, but it changes the input or access contract. It is not evidence that an operation using only the reduced representation already possessed the missing distinction.

### 3.2 Current assertions and retained history

Let S denote the full represented scholarly state. Its current-assertion projection, Ψ(S), records the assertions and statuses treated as current in the local inquiry. Its evidence and history projection, Ξ(S), retains the relevant documentary events, relations, responsibility, and transitions. These are distinctions within a model, not an assertion that historical knowledge naturally divides into two exhaustive compartments.

An incoming intervention e supplies source-grounded information, including its relation kind, the particular object or proposition addressed, and the evidence or proposal being recorded. For an action type g, write Q_g(S,e) for whether the action is qualified. Rejection reasons are retained separately so that an absent target, an invalid current version, and unresolved target history are not collapsed into the same unexplained failure. The set of qualified action types is then Γ(S,e) = {g : Q_g(S,e) = 1}. Execution is a further step: once an action qualifies, it produces a revised state and its record of change.

The Paper Money comparison can now be stated compactly:

\[
\Psi(S_{\mathrm{full}})=\Psi(S_{\mathrm{ablated}}),
\qquad
Q_{\mathrm{RESOLVE}}(S_{\mathrm{full}},e_{\mathrm{PM03}})
\ne
Q_{\mathrm{RESOLVE}}(S_{\mathrm{ablated}},e_{\mathrm{PM03}}).
\]

The equality is limited to the declared current projection. It is not equality of the full states, the documentary record, or everything a human reader could infer. This restriction is what makes the comparison meaningful: a representation that exposes only that projection does not distinguish two inputs for which the registered later action requires different treatment.

### 3.3 Binding requirements differ from state requirements

The exact target of an intervention and the current status of that target are related but distinct. The event can name the correct proposition even when that proposition is absent from the state being consulted. Conversely, an appropriate-looking assertion can be present while the event is bound to a different proposition. Treating both cases as a single target field would conceal the difference between misbinding an intervention and misrepresenting the status of its correctly named target.

We therefore represent the requirements of an action by a typed signature:

\[
\Sigma(g)=(\Beta(g),\Kappa(g)).
\]

Β(g) identifies the event-side binding conditions: for example, the exact object, source or version, relation kind, and target identity. Κ(g) identifies the state-side conditions: for example, whether the bound target is live or current, whether an update is valid, what competing assertions are represented, and whether the required target-entry history is retained. Here *live* means available as a target under the declared state model; it is not a claim about which interpretation a scholarly community presently accepts ([E3](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e3)).

This typing also disciplines the experiments. A wrong-target test changes the event binding while holding the state fixed. A missing-history test keeps the event fixed while changing the state. A requirement should not be counted twice merely because one perturbation simultaneously affects target identity and target lookup. Where the available cases do not separate these dimensions, the confounding must remain visible.

For a fixed admissible event binding, define action-relative state equivalence by agreement on the state distinctions inspected for that action:

\[
S\sim_g S'
\quad\Longleftrightarrow\quad
P_{\Kappa(g)}(S)=P_{\Kappa(g)}(S').
\]

The projection here is evaluated with the same bound event in both states. If the specified qualification rule factors through that projection, then

\[
S\sim_g S'\ \Longrightarrow\ Q_g(S,e)=Q_g(S',e).
\]

This implication follows from the factorization of the rule. It is not an unrestricted new theorem established by counting successful examples. The general information question—whether a representation determines the answer to a query—has a substantial technical literature, including Nash, Segoufin, and Vianu (2010). Our contribution concerns the source-grounded content of the qualification rules, their different requirements for editorial acts, and the consequences when those acts compose. The implementation checks ask whether the registered model behaves as specified under controlled changes; the historical readings supply the interpretation that makes the specification worth examining.

### 3.4 What the evaluation tests

The evaluation combines source interpretation, independent implementations, and controlled transformations. The historical relation labels were drawn from pre-existing, page-verified project assets and frozen for the relevant composition tests. The same target-bound implementation handles both historical sequences without branching on their episode names or claim identifiers. Independently implemented qualification and execution paths are compared for agreement. None of this makes the relation labels interpretation-free: withholding an operation label from the input prevents direct answer injection, but does not automate the judgment that a passage constitutes a correction or a bibliographical reply ([E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

The controls have different purposes. Removing a required relation tests whether the registered operation loses its support. Perturbing a condition registered as nonrequired tests whether the model is unnecessarily restrictive. Supplying a later intervention before its target has entered the state tests target-bound sequence dependence. These are finite model tests over documentary inputs, not estimates of the frequency of particular editorial practices.

## 4. Not every continuation requires the same past

### 4.1 Arbre Sec: recording a reply without manufacturing assent

The Arbre Sec sequence supplies the crucial contrast. The earlier edition identifies an Oriental Plane and already includes a botanical objection and response. The local starting state used in the model therefore represents one selected identification, not an edition imagined to have no prior interpretive history. In the 1920 entry, Houtum-Schindler's proposal identifies the object instead with the Cypress of Zoroaster. Cordier then replies that he had read Schindler's earlier paper and points back to a genuine citation in the third edition. The inspected reply establishes a bibliographical intervention; explicit adoption of the cypress proposal is not established (Yule and Cordier 1903, I:113, 128; Cordier 1920, 31; [E1](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e1)).

The distinction is consequential. Were Cordier's reply treated as a resolution of the identification, the representation would turn evidence of prior reading into evidence of assent. Were the reply omitted because it leaves the competing identifications unchanged, the representation would erase an act that bears on the history and responsibility of the discussion. The model therefore records it as an evidence-bearing reply directed at the proposal, while retaining both competing identification assertions.

The registered sequence is ADD_ALTERNATIVE followed by RECORD_EVIDENCE. The first action makes the cypress proposal available as a distinct target. The reply is then qualified by its source-bound relation to that target and the target's presence in the represented state. Execution preserves the current assertion projection while changing the retained evidence and history:

\[
\Psi(S_{\mathrm{before\ reply}})=\Psi(S_{\mathrm{after\ reply}}),
\qquad
\Xi(S_{\mathrm{before\ reply}})\ne\Xi(S_{\mathrm{after\ reply}}).
\]

Unlike the Paper Money correction, this registered reply does not need to inspect the earlier transition by which its target entered. It requires an identifiable live proposal, not a demonstration that the proposal had entered as a criticism of another claim. This is a difference in qualification requirements, not a judgment that the proposal's history is unimportant for other questions ([E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2); [E4](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e4)).

### 4.2 Comparing obligations rather than quantities of metadata

The paired cases reject two opposite shortcuts. Retaining current assertions alone is not always sufficient. Requiring all available history for every action is not justified either. The relevant question is which distinction a particular action actually reads. Table 2 summarizes the focal contrasts, including the independent ecology discussed in Section 6. It does not replace the complete specifications of source, relation, proposal, and status conditions.

| Registered action | Focal binding and current-state conditions | Is retained target-entry history inspected for qualification? |
| --- | --- | --- |
| Paper Money: correct the prior criticism, modeled as RESOLVE | The correction addresses the live critical assertion; the proposal matches the relevant live alternative | Yes: the target's entry as a criticism of the prior assertion must be established |
| Arbre Sec: record Cordier's bibliographical reply | The reply addresses the particular live competing proposal | No, for this registered reply |
| Formalization Papers: RECORD_RESPONSE | Exact review/update bindings and their required live/current conditions | Yes: the relevant review/update entry history must be established |
| Formalization Papers: REVISE_PUBLICATION_STATUS | Exact target binding and the required current update | No, for this registered status action |

**Table 2.** Action-relative qualification contrasts. “No” concerns admission of the specified action under the registered rule; it does not authorize deleting history needed for another inquiry, for explaining an outcome, or for auditing the record ([E4](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e4)).

The finite signature audit checks 120 action contexts: four in the two Yule–Cordier sequences and 116 in the Formalization Papers ecology. The latter comprise 48 review contexts, eight replacement contexts, 52 response contexts, and eight publication-status contexts. All 120 retained their qualification result under the registered equivalence-preserving changes. Across the associated required-condition tests, all 393 witnesses behaved as specified; all 19 nonrequired-history tests preserved qualification. The 393 witnesses include event-binding and state-side requirements, not 393 demonstrations that history alone is necessary ([E5](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e5)).

These counts document coverage of a registered finite model. They are not 120 independently sampled historical episodes, and the counterfactual witnesses are not additional natural documents. Likewise, the nonrequired tests establish invariance under the prescribed interventions, not under every conceivable change to the past. Their value is discriminatory: the implementation does not simply reward the representation with more metadata. It distinguishes conditions whose removal changes the registered action from conditions whose removal does not.

## 5. Earlier acts establish later possibilities

The two historical sequences also show why action qualification cannot be assessed as an unordered inventory of statements. After the Paper Money criticism has been recorded, there is both a live competing claim and an entry relation identifying it as a criticism of the baseline. The later correction reads those conditions. Attempting that correction at the baseline state, before the critical target has entered, yields an absent-target rejection. Attempting it after the criticism but with the entry history erased yields a different rejection: the target exists, but the relevant history has not been established ([E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

Arbre Sec separates target creation from history-dependent continuation. Recording the competing identification creates the target to which Cordier's reply is bound. Before that proposal is present, the reply does not qualify. After it is present, the reply can be recorded without reading its entry history. The earlier act therefore enables a later act even where the later act neither changes the current identification assertions nor requires the full transition record.

In computational terms, an earlier action writes information that a later action reads. But a useful description must go beyond overlapping field names. The first act can create an entity that appears in the binding of a later event; it can also make that entity live, establish its version status, or create the particular entry relation inspected by a later qualification rule. The sequence audit checks these bindings and conditions, not merely whether both functions mention a field called history. Both registered historical sequences satisfy these checks ([E3](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e3); [E5](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e5)).

The reverse-order controls should not be mistaken for a reconstruction of an alternative historical chronology. They ask whether an intervention can be applied from a specified represented starting state. A later reply attempted before its target exists is undefined under that contract. This demonstrates order-sensitive availability, not two complete histories that can always be executed in either order and then compared. Similarly, sequence closure here means that the required dependencies are supplied along the tested chains. It does not mean that the framework discovers all possible future acts or that its action vocabulary is universally closed.

The resulting humanistic claim concerns the afterlife of an intervention. A criticism can become an object of later criticism; a proposal can become the object of a reply. Earlier scholarly work thus produces some of the objects and relations through which later inquiry proceeds. Preserving only a conclusion can remove the means of distinguishing these continuations. Preserving a reply only as a conclusion change can do the opposite: invent a settlement where the record contains a further act of discussion.

## 6. A bounded test in an independent scholarly ecology

The historical cases supply the article's interpretive problem. To examine whether the target and history distinctions can also be operationalized outside that editorial record, the project tests a frozen Formalization Papers dataset. Unlike the Yule–Cordier prose, this ecology supplies machine-readable links among submissions, reviews, updates, responses, and decisions. Its role is to test the mechanism with independently structured documentary relations, not to replace the historical cases or establish the semantic correctness of their readings ([E6](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e6)).

The frozen archive contains ten record files and a graph-derived population of fifteen roots. Every root receives a registered disposition: eight have the complete structure required for the primary composition test, while seven remain ambiguous or nonfunctional for that purpose. They are not discarded or repaired into eligibility. Within the eight eligible roots, the grammar enumerates all 52 connected review–update–response–decision chains, rather than selecting one favorable chain per root. These chains share documentary components and must not be treated as 52 independent samples ([E6](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e6)).

All 52 eligible chains satisfy the prescribed forward and counterfactual checks in the corrected execution. The action sequence records a review, replaces the represented formalization, records a response, and revises publication status. Tests include responses attempted before their targeted review or update, a decision attempted before its targeted update, wrong-target interventions where structurally available, and removal of retained history while keeping the current update projection fixed. An independent documentary auditor reconstructs the root and connected-chain sets from the raw source rather than accepting the main runner's selected denominator. Its chain set agrees exactly with the main analysis ([E6](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e6)).

A subsequent exposed comparator audit separates three representations: one that retains functional relation-target bindings, one that additionally establishes live/current targets, and one that also retains the entry history required for the response action. Table 3 reports availability on their distinct test populations. “False availability” means availability contrary to the registered source and qualification conditions, not a judgment that a human response should never be made.

| Test population | Functional target binding | Binding plus live/current target | Binding, current target, and required history |
| --- | ---: | ---: | ---: |
| Valid response contexts retained, n = 52 | 52/52 | 52/52 | 52/52 |
| False availability on natural non-live-target response acts, n = 47 | 47/47 | 0/47 | 0/47 |
| False availability on controlled history-ablated response contexts, n = 52 | 52/52 | 52/52 | 0/52 |
| Availability on the nonfunctional-target control, n = 1 | 0/1 | 0/1 | 0/1 |

**Table 3.** Registered representation comparators for response qualification. The 47 natural non-live acts and 52 controlled history-ablated contexts are different denominators. The comparators are project-defined information projections, not benchmarked implementations of PROV, TEI, or version-control software ([E7](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e7)).

The comparison distinguishes two obligations. A correct-looking relation can point to a target that is not currently available for the registered action. Establishing the live target removes that class of false availability. Yet a live target alone does not establish the history required to interpret the registered response. Adding that distinction removes the history-ablation failures while retaining all valid contexts. The status-action contrast in Table 2 prevents this result from being generalized into a requirement that every scholarly operation read entry history.

The execution history imposes a further evidentiary boundary. The authoritative first prospective run was INVALID at the parser-surface gate. Corrected execution used the byte-identical first-opening archive after repairs to dateTime lexical serialization and preservation of multi-valued creator relations. It is recorded as POST_FRESH_CORRECTED_REPRODUCTION_PASS, not as a restored prospective fresh PASS. The independently implemented parsers agree on the registered surface after correction, but that agreement does not erase the initial failure. The mechanism results are consequently reported as a corrected reproduction under pre-specified scientific rules, with the subsequent signature and comparator audits labeled as exposed analyses ([E6](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e6)).

## 7. Implications for digital editions and historical records

### 7.1 From a history of changes to the conditions of continuation

The argument does not begin where provenance scholarship ends. Broyles (2020) already treats version numbering as a scholarly and social practice: changes need to be communicated meaningfully to readers and downstream users, and the relevant units of versioning need not coincide with a whole website. Vancisin and colleagues (2023) connect the transformations of historical records to interpretation, research questions, and the visibility of curatorial labor. Williamson (2026) likewise argues that digitized sources must be understood through their production, mediation, and access contexts. These approaches make historical and digital provenance part of scholarly understanding rather than an administrative supplement.

Our contribution is a narrower operational comparison within that larger problem. Instead of asking only whether the history of a resource is documented, we ask which documented distinctions are necessary to support a specified next act, and which are not. The Paper Money and Arbre Sec contrast makes this question substantive. Both records contain earlier and later interventions; only one of the tested continuations requires the target's critical entry history. Both histories matter to an account of the discussion; one later act changes the represented assertion set, while the other must be retained precisely without being converted into such a change.

This suggests a practical test for an editorial representation. Alongside asking whether a source or revision can be cited and recovered, an editor can ask whether the system can distinguish correction from correction-of-a-criticism, or transmission from adoption, in a concrete continuation. A failure should identify the missing binding or condition rather than silently substitute an easier operation. This is a proposal for making editorial commitments inspectable, not a claim that a new software interface has already improved scholars' performance.

### 7.2 Carrier-neutral obligations

No particular serialization is intrinsically the answer. The PROV data model offers entities, activities, agents, and relations through which histories can be represented (W3C 2013). TEI's revisionDesc records a file's revision history (TEI Consortium n.d.). These facilities can contribute to an implementation, but the history of changes to a modern encoded file must be distinguished from the historical scholarly acts represented within it. A file edit performed by a contemporary encoder is not automatically the same event as a criticism transmitted by Cordier.

The present requirements could be realized through suitable graph relations, explicit textual apparatus, recoverable versioned records, or combinations of these carriers. The tests therefore do not demonstrate a deficiency of PROV or TEI as standards. Nor do they show that native plain text necessarily erases the relevant distinctions. A prior project audit records that the native Gutenberg text retained recoverable carriers for the five historical distinctions tested when the relevant passages were supplied. That result remains a boundary on the stronger loss claim ([E8](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e8)).

What must survive is the needed distinction under the declared means of access, not necessarily a field with the same name as in our implementation. If another admissible carrier reconstructs the exact target relation, that is a legitimate solution. Conversely, merely retaining a large volume of historical material does not demonstrate that a specific operation can recover the relation it needs. Storage, exposure, interpretation, and qualification should not be treated as synonyms.

### 7.3 Minimality without premature deletion

An action-relative requirement is useful precisely because it is limited. A history field not read by the Arbre Sec reply rule may still be essential to a different inquiry into priority, mediation, or the development of an identification. A representation adequate for the registered publication-status action may be inadequate for assessing the response history that preceded it. Therefore, the nonrequired controls are not a policy for deleting unused evidence from an archive.

This distinction becomes more important when future questions are unknown. The framework can expose the commitments of an explicitly declared action family; it cannot certify that an unanticipated question will need no further evidence. A responsible preservation practice would therefore distinguish a reduced working view from the retained source record and document how the former can be related back to the latter. The bounded tests warrant a claim about supported operations, not a guarantee that the tested view exhausts the research value of the record.

Finally, the treatment of Arbre Sec shows why a current-state interface should leave room for consequential acts that do not settle a proposition. A bibliographical reply can change what the edition records about acknowledgment and participation without resolving the identification. Keeping that distinction available is not merely a technical refinement. It prevents the digital account from manufacturing consensus and permits the history of a discussion to remain visible as a history of discussion.

## 8. Limits and conclusion

### 8.1 Evidentiary limits

The historical argument is source-bound and case-bounded. The two sequences were already exposed during the project's development and were selected for their analytical contrasts. They do not constitute a prevalence sample of the Yule–Cordier corpus, still less of scholarly editing generally. Paper Money's last event combines a correction and an endorsement, although their stance traces are separately documented. Arbre Sec supplies the cleaner act-level contrast. Neither sequence is a complete reconstruction of its entire intellectual or editorial lineage ([E1](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e1); [E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

The prior page-verification records also must not be confused with successful independent historical adjudication. The project's frozen three-model second pass completed 45 calls over five historical cases. Nine responses passed the frozen source-citation validator, but none of the 21 predeclared atomic components reached the required valid, stable two-model consensus. The disposition remains BOUNDED_PARTIAL. It does not refute the page-grounded readings, but it does not supply the stronger corroboration either. This manuscript therefore makes no claim of historian consensus, independent human validation, or successful model-separated replication of those readings ([E9](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e9)).

The computational tests evaluate the consequences of registered interpretations and rules. Agreement between independent implementations reduces some implementation risks, but shared specifications can still encode a contestable assumption. Requiring historical grounding for a correction, or a particular target history for a response, is part of the contract being tested; a successful ablation cannot independently prove that contract philosophically mandatory. The contribution lies in articulating the source reading, making the rule inspectable, and contrasting its behavior with alternatives rather than disguising the rule as an assumption-free discovery.

The finite audits have further limits. Three Yule witnesses couple exact target identity and live-target lookup, so that corpus alone does not identify their effects separately. The Formalization Papers audit provides additional typed probes, but its source ecology is not an independent adjudicator of the historical cases. Its chains also share roots, and the literal first prospective execution remains invalid. None of the reported counts warrants universal completeness, cross-domain prevalence, or a generalization rate for automatic extraction ([E5](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e5); [E6](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e6)).

Finally, equality of a selected current projection is not an ontological claim that two complete scholarly situations are identical. Enriching that projection with the missing relation can eliminate the contrast, as can a permitted recovery procedure that reconstructs it. That possibility is consistent with the argument: it identifies information that must be available for the registered operation. We do not claim that history is irreducible to every enriched state representation, or that a chronological event log is the only way to retain it.

### 8.2 Conclusion

The editorial record must be able to preserve more than the answer that happens to be current. It must sometimes preserve the relations through which that answer became a correction, an alternative, or a response. Yet the required past is not the same for every continuation. The Paper Money correction needs the represented history of a prior criticism; the Arbre Sec reply needs its identifiable proposal without thereby adopting it. Their contrast makes preservation obligations action-relative rather than a uniform demand for more metadata.

Earlier scholarly acts also establish some of the targets and conditions on which later acts depend. The bounded computational account makes those dependencies explicit and tests where they survive controlled transformations. Its purpose is not to close historical interpretation with a rule system. It is to help digital editions disclose what their representations support, what they leave unresolved, and what must remain recoverable for inquiry to continue.

## References

Birnbaum, David J., and Elena Spadini. 2020. “Reassessing the Locus of Normalization in Machine-Assisted Collation.” *Digital Humanities Quarterly* 14 (3). https://www.digitalhumanities.org/dhq/vol/14/3/000489/000489.html.

Bleeker, Elli, Bram Buitendijk, Ronald Haentjens Dekker, Vincent Neyt, and Dirk Van Hulle. 2022. “Layers of Variation: A Computational Approach to Collating Texts with Revisions.” *Digital Humanities Quarterly* 16 (1). https://dhq.digitalhumanities.org/vol/16/1/000583/000583.html.

Broyles, Paul A. 2020. “Digital Editions and Version Numbering.” *Digital Humanities Quarterly* 14 (2). https://www.digitalhumanities.org/dhq/vol/14/2/000455/000455.html.

Cordier, Henri. 1920. *Ser Marco Polo: Notes and Addenda to Sir Henry Yule's Edition, Containing the Results of Recent Research and Discovery*. London: John Murray. Principal passages used here: 31, 70–72. The companion register distinguishes the source readings already page-verified in the project from this writing pass.

Nash, Alan, Luc Segoufin, and Victor Vianu. 2010. “Views and Queries: Determinacy and Rewriting.” *ACM Transactions on Database Systems* 35 (3), article 21: 1–41. https://doi.org/10.1145/1806907.1806913.

TEI Consortium. n.d. “revisionDesc (Revision Description).” *TEI P5: Guidelines for Electronic Text Encoding and Interchange*. https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-revisionDesc.html. Accessed 30 September 2026.

Vancisin, Tomas, Loraine Clarke, Mary Orr, and Uta Hinrichs. 2023. “Provenance Visualization: Tracing People, Processes, and Practices through a Data-Driven Approach to Provenance.” *Digital Scholarship in the Humanities* 38 (3): 1322–1339. https://doi.org/10.1093/llc/fqad020.

W3C. 2013. *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/.

Williamson, Elizabeth R. 2026. “Digitized Archives, Content Providers, and Slow Scholarship: Why Archival Researchers Should Care about Digital Provenance.” *Digital Scholarship in the Humanities* 41 (3): 1705–1723. https://doi.org/10.1093/llc/fqag062.

Yule, Henry, and Henri Cordier. 1903. *The Book of Ser Marco Polo*. Third edition. Vol. I. London: John Murray. Principal passages used here: 113, 128, 423, 430.

## Evidence and materials statement

The analysis uses existing, versioned project evidence rather than a new corpus opening. The [source and evidence register](SOURCE_NOTES_AND_SUBMISSION_GAPS.md) provides the source anchors, protocol and result paths, population accounting, execution labels, and drafting-stage limitations underlying E1–E9. The [claim and evidence freeze](CLAIM_FREEZE_AND_EVIDENCE_MATRIX.md) records the three headline claims and excluded inferences. The formal and empirical claims in this draft are bounded to those records. No eLife, TMLR, or OpenReview result is introduced as confirmatory evidence.
