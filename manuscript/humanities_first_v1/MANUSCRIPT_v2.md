# After Revision: Scholarly Continuation and Action-Relative Researchability in Digital Editions

*Integrated second working draft, 30 September 2026. Source readings and experimental labels follow the frozen evidence register; the figure and submission checks remain explicit companion work.*

## Abstract

Digital scholarly editions do more than preserve textual states and document their histories. They also shape the conditions under which later scholarship can continue from those histories. This article develops a Digital Humanities account of **scholarly continuation**: the historically grounded capacity of a representation to support later acts that address, revise, qualify, or record earlier scholarship. The problem is distinct from preserving a latest state, and it is not exhausted by recording provenance in the abstract. A later correction may depend on identifying the precise criticism it corrects; a bibliographical reply may matter to the history of an interpretation without settling that interpretation. We argue that digital scholarly representations therefore have a **continuation structure** in addition to a current scholarly state and a record of prior intervention.

Two sequences in the Yule–Cordier editorial record of *Marco Polo* provide the central cases. In the Paper Money sequence, a criticism becomes the specific object of a later counter-criticism. In the Arbre Sec sequence, a competing identification occasions a bibliographical reply that changes the recorded history of discussion without establishing assent to the proposal. Their contrast motivates an action-relative account of researchability: different scholarly continuations require different relations, targets, and historical conditions. We operationalize these requirements through a source-bound model that separates event-side binding from state- and history-side qualification, and we test the same distinction in a second machine-readable ecology of scholarly review and revision.

The article's contribution is a theory of how digital representations mediate the **continuability of scholarship**: the conditions under which a later intervention remains reconstructible as the historically specific intervention it is.

**Keywords:** digital scholarly editing; scholarly continuation; researchability; provenance; editorial history; digital humanities modelling; scholarly activities

## 1. Digital editions condition how scholarship continues

A scholarly edition is often evaluated by the texts, variants, witnesses, annotations, provenance, and revision history it preserves. Scholarship also acts upon earlier scholarly acts. A critic answers a prior interpretation. An editor corrects an earlier note. A later scholar distinguishes transmission from adoption, revises an attribution, records new evidence, or reopens a proposition that had appeared settled. Later scholarship inherits a text or current answer together with a structured field of interventions to which new interventions can attach.

This article calls that relation **scholarly continuation**.

A scholarly continuation is a later act whose scholarly identity depends on how it attaches to an existing record. To call an intervention a correction *of a prior criticism* is to claim more than that one proposition differs from another. It identifies a target, a relation, and a position in an argumentative history. To record a reply *to a proposal* is likewise different from simply adding another proposition to the same topic. These distinctions are routine in close reading and scholarly editing. Digital representation makes them technically consequential because a model, schema, interface, or access route may preserve some of them while flattening others.

A revision history can document that changes occurred while leaving a particular relation among them difficult to substantiate. Presence, discoverability, target identity, responsibility, and the conditions for a later intervention are distinct scholarly properties. The relevant question is:

> **How does a digital scholarly representation preserve, constrain, or transform the historically grounded possibilities for scholarship to continue?**

This question places the article within several established Digital Humanities traditions while identifying a different unit of analysis. Digital scholarly editing has long treated editions as interpretive constructions. DH modelling theory understands models as selective and purposive ways to make scholarly assumptions explicit and manipulable. Work on scholarly primitives and information activities shifts attention from scholarly products to activities such as discovering, comparing, referring, annotating, representing, reading, and assessing (Unsworth 2000). DH modelling makes the selective, interpretive character of computational representations a central object of inquiry (McCarty 2003). Work on versioning and provenance has shown that the history of digital scholarly resources affects citation, interpretation, and future use (Broyles 2020; Vancisin et al. 2023). Broyles explicitly observes that the significance of a change depends on a theory of text, a research use, and an interface. Our question therefore concerns the historical dependencies *among* scholarly acts: how an earlier criticism, proposal, or response becomes a possible object of later scholarship.

Our additional claim is that **the history represented by an edition has a structure of possible scholarly continuation**. The same represented state can support one later act but not another. Two later acts can require different parts of the past. And an earlier scholarly act can create the very target or relation that makes a later act intelligible. Digital representation thereby mediates what can be reconstructed *next* from the record under a declared evidentiary horizon.

The claim concerns a declared representation and access horizon: **representational choices condition which later acts can be substantiated as historically grounded continuations of that record.** A scholar may restore a missing relation by reopening an archive, consulting another edition, or extending the representation. Each route adds identifiable interpretive and evidentiary work.

### 1.1 From state and history to continuation structure

To make this claim precise without reducing it immediately to implementation, we distinguish three aspects of a scholarly representation.

**Scholarly state** concerns what the local inquiry currently represents: for example, an identification, reading, attribution, or status.

**Scholarly history** concerns how that represented state arose: the interventions, targets, evidence, responsibility, and relations that connect one scholarly act to another.

**Continuation structure** concerns which specified later scholarly acts can be grounded in that state and history, and which distinctions those acts require.

The third category names a relation between a representation and a family of scholarly continuations. It asks whether a record still supports such acts as correcting a criticism, replying to a proposal, or revising a status *as those acts*, rather than merely allowing some new string or node to be appended.

This triad helps distinguish three claims that are often conflated. A representation may preserve a current assertion without preserving the history needed to reconstruct how a later intervention addresses it. It may preserve an extensive history without exposing the relation a particular continuation requires. And it may preserve an act that changes the history of discussion without changing the current proposition at all.

The two historical sequences examined below instantiate exactly these contrasts. Figure 1 places their actors, targets, and editorial transmission side by side; its arrows summarize the registered source reading rather than supply an independent historical judgment.

### 1.2 The paper's theoretical propositions

The argument proceeds through four propositions.

**T1 — Current-state preservation is not continuation preservation.**  
Two representations can agree on the registered current scholarly state while differing in whether a later source-bound intervention can be reconstructed with its historical target and relation.

**T2 — Continuation requirements are action-relative.**  
Different scholarly continuations require different distinctions. A correction of a criticism need not have the same evidentiary requirements as a bibliographical reply or a publication-status revision.

**T3 — Earlier scholarly acts are productive of later possibility.**  
An earlier intervention does not merely become archival residue. It can create a target, relation, or status that a later intervention addresses. A criticism can become the object of a correction; a proposal can become the object of a reply.

**T4 — Scholarly history can change without a change in current scholarly state.**  
An intervention can matter because it alters the record of acknowledgment, responsibility, evidence, or disagreement even when the represented proposition remains unchanged. A digital edition that treats such an event as irrelevant risks erasing the continuation of discussion; one that treats it as a substantive settlement risks manufacturing consensus.

These propositions arise from the editorial distinctions read in the sources. The computational formalism introduced later operationalizes their consequences.

## 2. Two ways scholarship continues

The Yule–Cordier editorial record of *Marco Polo* makes the continuation problem visible because its later editorial layers do not behave as a sequence of simple replacements. They transmit criticism, endorsement, competing identifications, replies, and source judgments with different actors and targets. Two local sequences are especially useful because they show opposite dangers: reducing a historically situated correction to a latest-state replacement, and turning a reply into an assent it does not establish.

### 2.1 Paper Money: correcting a critic

The Paper Money case concerns the material identified in Marco Polo's description of paper currency. In the 1903 third edition, the base discussion associates the material with mulberry bark. A note then transmits Emil Bretschneider's objection to that identification. Cordier's 1920 *Notes and Addenda* later transmits Berthold Laufer's response. Laufer's intervention is proposition-specific: he challenges Bretschneider's exclusion of mulberry while distinguishing that disagreement from other aspects of the botanical discussion.

The important structure is therefore not merely:

    earlier claim -> later claim

but:

    material claim
        -> criticism of that claim
            -> later correction of the critic
               + endorsement of the material claim

The last intervention is historically intelligible because it addresses two different targets in two different ways. Laufer criticizes Bretschneider's prior judgment and supports the material identification associated with Polo's account. Cordier transmits these judgments. The present article does not convert that transmission into a claim that the entire scholarly community adopted Laufer's view.

This distinction matters for the digital representation of the sequence. A local model may treat the later intervention as resolving the represented competition for the purpose of following that particular material-identification dispute. But such a modeled resolution is not the same thing as saying that the historical controversy ceased to exist. Indeed, the criticism remains part of the record precisely because the later intervention is a correction *of it*. Removing the criticism after adopting the later answer would erase part of what makes the later answer historically intelligible.

Paper Money therefore motivates T1. The current material identification and the continuation structure of the discussion are not identical objects. A representation can preserve the same current answer yet differ in whether it retains the relation needed to reconstruct the later act as a correction of a prior criticism.


| Documentary position | Relation in the registered reading | Local representational consequence |
| --- | --- | --- |
| PM01: material identification | Baseline assertion | Makes the proposition available as a target |
| PM02: Bretschneider's criticism, transmitted by Cordier | Criticizes PM01 | Adds a competing assertion and records its entry relation |
| PM03: Laufer's response, transmitted by Cordier | Corrects PM02 and endorses PM01 | Updates the local material-result state while retaining the critical history |

**Table 1.** Paper Money as a proposition-level sequence. PM03 is a compound intervention. The local model's update concerns the represented inquiry state; it is not an assertion that the wider scholarly dispute reached consensus ([E1](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e1); [E2](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e2)).

### 2.2 Arbre Sec: replying without assenting

The Arbre Sec case makes the opposite point. The earlier edition identifies the object with an Oriental Plane while already preserving an objection-and-response context. The 1920 entry later reports Houtum-Schindler's competing identification with the Cypress of Zoroaster. Cordier then responds bibliographically, defending his prior knowledge and citation of Schindler.

That reply belongs to the history of the identification dispute, but it does not establish that Cordier adopts the cypress identification.

This distinction is easy to lose in a representation that equates meaningful intervention with substantive state change. If Cordier's reply is ignored because it does not replace the current identification, part of the intellectual history disappears. If it is instead encoded as acceptance of Schindler's proposal, the representation invents a settlement not established by the passage.

Arbre Sec therefore motivates T4. A scholarly act can alter the history of discussion without changing the represented proposition. Digital scholarly editing requires a way to preserve such acts as first-class elements of the record.

The case also motivates T2. The Paper Money correction and the Arbre Sec reply do not require exactly the same past. To reconstruct the former as a correction of a prior criticism, the earlier critical relation matters. To record the latter as a bibliographical reply, the immediate requirement is that the specific proposal to which Cordier responds be identifiable as its target; the reply need not thereby inherit or resolve every earlier relation in the identification history.

### 2.3 From two cases to a DH theory of continuation

Taken together, the two sequences suggest a stronger account of digital scholarly representation than a uniform injunction to preserve more history.

The first lesson is that **the current scholarly state is only one layer of an edition's research value**. A latest reading or normalized assertion may be useful for one task and insufficient for reconstructing a later intervention.

The second is that **history is not one undifferentiated resource**. Different continuations inspect different relations. A representation that forces every later act to depend on the entire available past is no more theoretically adequate than one that discards the past whenever the current proposition can be preserved.

The third is that **scholarly interventions can be generative**. By introducing a criticism or proposal, they create objects that later scholarship can address. This is the point at which provenance becomes continuation: the earlier act matters not only because it happened, but because it helps constitute what the later act is an act *upon*.

The fourth is that a digital scholarly edition should be able to distinguish **continued discussion from settled state**. That distinction is central to the article's DH identity. It connects editorial interpretation, scholarly activity, and computational representation without reducing any of them to the others.


![Two editorial continuations in Paper Money and Arbre Sec](figures/figure_1_scholarly_continuation.svg)

**Figure 1.** Source-grounded relations across two editorial sequences. Arrows run forward through the documentary layers and label how the later intervention addresses the earlier one. Cordier transmits Laufer's response in Paper Money and answers Houtum-Schindler's proposal in Arbre Sec; the latter reply supplies no assent to the cypress identification. Source loci and interpretive qualifications are given in [the figure contract](figures/FIGURE_1_CONTRACT.md).

The remainder of the article makes these continuation conditions explicit, compares them, and tests them. The next section introduces **action-relative researchability** to state which historically grounded distinctions a particular continuation requires and whether a given representation keeps them available.

## 3. Researchability as qualified scholarly action

### 3.1 A declared scope of support

We use *qualification* for the conditions under which a representation supports a specified scholarly act. The term is intentionally narrower than validity in every scholarly sense. A qualified correction is not thereby historically true. An unqualified correction is not forbidden to a scholar. Rather, the current representation and declared evidence do not establish the conditions for recording it as that particular kind of intervention.

This distinction locates the authority of the model. It does not replace interpretation with a permission system. It makes an interpretation's representational commitments inspectable. Calling a passage a correction of a prior criticism, for example, commits the analysis to an identifiable prior criticism and to a defensible binding between the two interventions. Two legitimate inquiries must be separated here. One can report that the later source *characterizes* its own intervention as a correction; that report needs the later passage and an attribution to its speaker. The stronger inquiry asks whether the record permits a researcher to reconstruct *which earlier criticism* is corrected and why this is a correction of that criticism. Our controlled comparison tests support for the stronger inquiry. The relation label supplied with PM03 is an interpreted description of Laufer's intervention; it does not by itself supply the earlier criticism's entry relation. A model that cannot exhibit that relation should expose the unresolved condition.

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


![Equal current assertions with different continuation support](figures/figure_2_current_state_vs_continuation.svg)

**Figure 2.** Controlled Paper Money representation comparison. Both arms have the same registered current-assertion projection and receive the same PM03 event. Only the full representation retains the critical entry relation needed to substantiate PM03 as a correction *of PM02*. The ablated arm is a constructed comparison, not a second historical edition. The local qualification results do not adjudicate historical truth; see [the figure contract](figures/FIGURE_2_CONTRACT.md).

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

The historical cases supply the article's interpretive problem. To examine whether the target and history distinctions can also be operationalized outside that editorial record, the project tests a frozen Formalization Papers dataset associated with the semantic-publishing study of Bucur and colleagues (2023). Unlike the Yule–Cordier prose, this ecology supplies machine-readable links among submissions, reviews, updates, responses, and decisions. Its role is to test the mechanism with independently structured documentary relations, not to replace the historical cases or establish the semantic correctness of their readings ([E6](SOURCE_NOTES_AND_SUBMISSION_GAPS.md#e6)).

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

### 7.1 A theory of the continuation structure of editions

The paired readings revise the unit in which an edition's scholarly value is described. An edition has a current scholarly state and a history of interventions, yet its capacity to support further inquiry depends on how earlier acts remain available as the objects of later ones. This **continuation structure** is therefore a relation among acts across editorial layers. In Paper Money, Bretschneider's criticism creates a specific target for Laufer's correction. In Arbre Sec, Houtum-Schindler's proposal creates a target for Cordier's bibliographical reply. The second response changes what the record says about the discussion while leaving the identification unsettled. The editorial question is which of these relations a later researcher can substantiate from the representation at hand.

This claim develops, rather than displaces, established DH accounts of scholarly activities and modelling. Unsworth (2000) directs attention to recurring activities such as annotation, comparison, and reference. McCarty (2003) treats modelling as selective, experimental inquiry into its object. We ask what happens when *one scholarly activity becomes a condition for identifying another*: when a correction is a correction **of** an earlier criticism, or a reply is a reply **to** a proposal. The prepositions are not stylistic decoration. They bind responsibility, target, and relation within an interpretable history.

The neighbouring edition and provenance literature already recognizes the dependence of change significance on scholarly purpose. Broyles (2020, note 43) explicitly connects what counts as a breaking change to theories of the edited text, research uses, and interfaces. Vancisin and colleagues (2023) connect transformations of historical records to later questions and interpretation. Bleeker and colleagues (2022) show how revision layers demand an interpretive computational model. Our distinct step is to compare the *qualification of particular next acts* under representations with controlled differences in the histories they expose. The model does not establish the historical reading by computation; it makes the reading's consequences inspectable and reveals where a representation would turn a reply into assent, or a correction into an ungrounded latest-state update.

This framework also changes how a figure of preservation should be drawn. A timeline alone records order. A provenance graph records derivation. Figure 1 foregrounds the historically specific attachments between interventions. Figure 2 then isolates a different question: holding the registered current assertions fixed, does an admissible representation still support the later correction as a correction of the prior criticism? The answer depends on the declared operation and access horizon. If an omitted relation can be reconstructed from an admissible source passage, the working view can be repaired; the question becomes whether that reconstruction is available to the scholarly action under study.

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

Bucur, Cristina-Iulia, Tobias Kuhn, Davide Ceolin, and Jacco van Ossenbruggen. 2023. “Nanopublication-Based Semantic Publishing and Reviewing: A Field Study with Formalization Papers.” *PeerJ Computer Science* 9: e1159. https://doi.org/10.7717/peerj-cs.1159.

McCarty, Willard. 2003. “‘Knowing True Things by What Their Mockeries Be’: Modelling in the Humanities.” *Computing in the Humanities Working Papers* A.24. https://chwp.artsci.utoronto.ca/CHC2003/McCarty2.htm.

Unsworth, John. 2000. “Scholarly Primitives: What Methods Do Humanities Researchers Have in Common, and How Might Our Tools Reflect This?” King’s College London, 13 May. https://people.brandeis.edu/~unsworth/Kings.5-00/primitives.html.

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
