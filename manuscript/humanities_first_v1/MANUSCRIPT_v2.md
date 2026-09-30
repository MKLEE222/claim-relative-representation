# After Revision: Scholarly Continuation in Digital Editions

## Abstract

A digital edition can preserve an answer while obscuring the exchange through which it was defended. It can also record a reply in a way that makes continued disagreement appear to have been settled. This article develops an account of scholarly continuation through two editorial sequences in the 1903 Yule-Cordier edition of *Marco Polo* and Cordier's 1920 addenda. The Paper Money sequence distinguishes Laufer's correction of Bretschneider's criticism from his endorsement of an earlier material identification. Arbre Sec distinguishes Cordier's bibliographical reply from acceptance of a competing identification. Reading these interventions alongside theories of scholarly editing, revision, and humanistic modelling, we ask what a representation must make recoverable for a later act to remain identifiable as an intervention upon an earlier one. A controlled comparison preserves current assertions while removing the criticism's recorded entry relation; connected review-and-revision records provide a bounded second test, reported as a corrected reproduction. The resulting account makes preservation requirements action-relative and distinguishes the continuation of scholarly discussion from a change in its represented conclusions.


**Keywords:** digital scholarly editing; scholarly continuation; editorial history; provenance; digital humanities modelling

## 1. Digital editions and the continuation of scholarship

In the Paper Money notes to *Marco Polo*, a botanical identification becomes the occasion for an exchange among scholars. The 1903 Yule-Cordier edition transmits Emil Bretschneider's criticism of the identification of mulberry bark in Polo's account. Cordier's 1920 addendum then transmits Berthold Laufer's response, which challenges that criticism while endorsing the earlier identification (Yule and Cordier 1903, I:423, 430; Cordier 1920, 70-72). A reader seeking only the material answer might extract the endorsement. A reader reconstructing the exchange needs something further: the distinction between the proposition Laufer supports and the prior criticism he corrects. The same intervention acquires its scholarly significance through both attachments.

The Arbre Sec entry presents a different editorial problem. Cordier reports Houtum-Schindler's proposal to identify the tree with the Cypress of Zoroaster and responds concerning his own earlier reading and citation of Schindler. The inspected passage establishes a bibliographical reply, but does not establish acceptance of the proposed identification (Yule and Cordier 1903, I:113, 128; Cordier 1920, 31). Omitting that reply would lose part of the discussion. Treating it as a replacement of the earlier identification would attribute a settlement that the passage does not supply. To represent this exchange, an edition must be able to register that something consequential has happened without requiring the identification itself to change.

These are problems of editorial interpretation before they become problems of computation. The distinction between a correction and an endorsement, or between a reply and assent, depends on reading who speaks, what is addressed, and how an editor transmits the exchange. Our concern is what happens to these distinctions when the record is represented for subsequent use. An interface might foreground a current identification, a dataset might expose assertions without their entry relations, or an annotation system might preserve a response while leaving its precise target unclear. Each arrangement makes a different part of the exchange available to the next reader.

The question belongs within a long-standing discussion of what editions do. Gabler (2010) conceives the digital scholarly edition through relations among textual and editorial discourses and their readers. Broyles (2020) shows why changes to an edition need to be identifiable and meaningful for its different uses. These accounts establish that an edition's research value involves more than the delivery of a stable text. We examine a particular demand within that larger understanding: the evidence needed to reconstruct one scholarly act as an intervention upon another.

We call this relation **scholarly continuation**. A criticism can become the object of a later correction; a proposal can become the object of a reply. The earlier act matters not only as a step on the way to a conclusion but as something later scholarship addresses. The distinction is especially apparent when the later act preserves an earlier proposition, as in Laufer's endorsement, or leaves competing propositions unresolved, as in Cordier's reply. A history organized solely around changes of answer would make both sequences difficult to describe adequately.

The article therefore asks:

> What must a digital scholarly representation make recoverable for a later correction, reply, or revision to remain identifiable as an intervention upon a particular earlier act?

We answer through close reading and controlled representational comparison. The historical readings establish the actors, targets, and relations at issue. The computational model then makes the requirements of specified continuations explicit and compares representations that preserve some requirements while removing others. A second documentary ecology, Formalization Papers, tests related distinctions in connected review-and-revision records. Its corrected-reproduction status and the diagnostic status of subsequent comparisons remain part of the evidence account.

The argument concerns the support a representation provides within a declared evidence horizon. A scholar may recover an omitted relation by returning to an admissible source. Such recovery matters: it supplies evidence the reduced view did not itself expose. The comparison identifies where that additional work is needed, without treating the limits of a working representation as limits on what scholars may investigate.

### 1.1 State, history, and continuation structure

We distinguish three aspects of the represented record. **Scholarly state** comprises the assertions and statuses treated as current for the local inquiry. **Scholarly history** comprises the interventions, evidence, responsibilities, and relations through which that state is interpreted. **Continuation structure** concerns the specified later acts that this state and history support, including what those acts address and what they change.

These are analytical distinctions within the model. A current assertion may itself contain historical information, and a sufficiently enriched state can retain every distinction inspected by an operation. The question is which distinctions remain available in the representation actually being used. Two views can expose the same current assertions while supporting different reconstructions of a later intervention.

### 1.2 Four propositions

The paired readings and comparisons develop four propositions.

**T1 - Preserving current assertions need not preserve continuation support.** Two representations may agree on the current assertions specified for an inquiry while differing in whether a later intervention can be reconstructed with its historical target and relation. The claim is not that any difference in retained history must alter later scholarly action. The controlled Paper Money comparison identifies a specific case in which current-assertion equivalence is preserved while support for a specified later act changes.

**T2 - Continuation requirements are action-relative.** A correction of a prior criticism, a bibliographical reply, and a publication-status revision can require different distinctions. Their requirements cannot be inferred simply from the amount of history a representation retains.

**T3 - Earlier scholarly acts establish objects and conditions for later acts.** Introducing a criticism or proposal makes something available that a subsequent correction or reply can address. The relevant dependency concerns the identity and status of that target, not chronology alone.

**T4 - Discussion can continue without changing the represented conclusion.** An intervention may alter the record of acknowledgment, evidence, or disagreement while leaving the current identification assertions unchanged. Representing that intervention requires preserving its effect on the discussion without manufacturing assent.

The next section develops the source readings and their relation to editorial theory. The formal account then asks what those readings require of a representation and how the requirements behave when interventions are composed.


## 2. Two ways scholarship continues

The Yule–Cordier editorial record of *Marco Polo* makes the continuation problem visible because its later editorial layers do not behave as a sequence of simple replacements. They transmit criticism, endorsement, competing identifications, replies, and source judgments with different actors and targets. Two local sequences are especially useful because they show opposite dangers: reducing a historically situated correction to a latest-state replacement, and turning a reply into an assent it does not establish.

### 2.1 Paper Money: correcting a critic

The Paper Money case concerns the material identified in Marco Polo's description of paper currency. In the 1903 third edition, the base discussion associates the material with mulberry bark. A note then transmits Emil Bretschneider's objection: “He seems to be mistaken.” Cordier's 1920 *Notes and Addenda* later introduces Laufer's response with “Laufer writes to me”; Laufer calls the objection “a singular error of Bretschneider” and states that “Marco Polo is perfectly correct” (Yule and Cordier 1903, I:423, 430; Cordier 1920, 70–72). Laufer also accepts Bretschneider's observation that paper was made from *Broussonetia* while rejecting the exclusion of mulberry. The disagreement concerns a specific negative claim, not every part of Bretschneider's botanical account.

The important structure is therefore not merely:

    earlier claim -> later claim

but:

    material claim
        -> criticism of that claim
            -> later correction of the critic
               + endorsement of the material claim

The last intervention addresses two targets in two ways. Laufer criticizes Bretschneider's prior judgment and supports the material identification associated with Polo's account; Cordier transmits both judgments. The distinction prevents the editor's act of transmission from being mistaken for authorship of Laufer's claims.

For the declared material-identification inquiry, the model treats Laufer's response as a local resolution of the represented competition. The criticism remains in the record because it is the target of Laufer's correction. A latest-answer view that removes the criticism would preserve the material identification while losing the exchange through which that answer was defended.

Paper Money therefore motivates T1. The current material identification and the continuation structure of the discussion are not identical objects. A representation can preserve the same current answer yet differ in whether it retains the relation needed to reconstruct the later act as a correction of a prior criticism.


| Documentary position | Interpreted relation | Consequence in the local model |
| --- | --- | --- |
| PM01: material identification | Baseline assertion | Makes the proposition available as a target |
| PM02: Bretschneider's criticism, transmitted by Cordier | Criticizes PM01 | Adds a competing assertion and records its entry relation |
| PM03: Laufer's response, transmitted by Cordier | Corrects PM02 and endorses PM01 | Updates the local material-result state while retaining the critical history |

**Table 1.** Paper Money as a proposition-level sequence. PM03 retains Laufer's correction and endorsement as a compound intervention; the modeled resolution concerns the local represented inquiry state.

### 2.2 Arbre Sec: replying without assenting

The Arbre Sec case makes the opposite point. The earlier edition identifies the object with an Oriental Plane while already preserving an objection-and-response context. The 1920 entry reports Houtum-Schindler's competing identification with the Cypress of Zoroaster. Cordier responds, “I read his paper,” and refers the reader to his citation in the third edition (Yule and Cordier 1903, I:113, 128; Cordier 1920, 31). The response concerns Cordier's prior knowledge and citation of Schindler.

That reply belongs to the history of the identification dispute, but it does not establish that Cordier adopts the cypress identification.

This distinction is easy to lose in a representation that equates meaningful intervention with substantive state change. If Cordier's reply is ignored because it does not replace the current identification, part of the intellectual history disappears. If it is instead encoded as acceptance of Schindler's proposal, the representation invents a settlement not established by the passage.

Arbre Sec therefore motivates T4. A scholarly act can alter the history of discussion without changing the represented proposition. Digital scholarly editing requires a way to preserve such acts as first-class elements of the record.

The case also motivates T2. The Paper Money correction and the Arbre Sec reply do not require exactly the same past. To reconstruct the former as a correction of a prior criticism, the earlier critical relation matters. To record the latter as a bibliographical reply, the immediate requirement is that the specific proposal to which Cordier responds be identifiable as its target; the reply need not thereby inherit or resolve every earlier relation in the identification history.

### 2.3 Sources and interpretive procedure

The close reading uses the 1903 third edition of *The Book of Ser Marco Polo*, volume I (printed pages 113, 128, 423, and 430), and Cordier's 1920 *Notes and Addenda* (printed pages 31 and 70–72). The two sequences were selected from earlier project work because they expose contrasting editorial acts; they are analytical cases, not a sample from which to estimate how often these acts occur. Prior page-image verification and proposition-level source records identify each speaker, the claim addressed, the kind of response, and the editorial layer that transmits it. The passages quoted above have additionally been checked against accessible digitized source text for this revision. Final line-by-line comparison with the fixed page images remains part of submission preparation.

Interpretation precedes computation. The Paper Money record distinguishes Polo's material claim, Bretschneider's criticism, and Laufer's compound correction-and-endorsement as transmitted by Cordier. The Arbre Sec record distinguishes the earlier identification, Houtum-Schindler's alternative, and Cordier's bibliographical reply. These readings determine the event relations supplied to the model; the program does not extract them automatically. Table 1 shows the documentary-to-model mapping for Paper Money, while Figure 1 compares the attachments in both cases. The controlled deletion in Figure 2 removes recorded entry history from a modeled view while leaving the current assertion projection and later intervention fixed. It is a comparison of representations of the same interpreted sequence, not an observed loss in a historical edition.

### 2.4 From editorial acts to conditions of continuation

The paired cases concern the history of scholarship represented within an edition. That history intersects with, but is not exhausted by, either the formation of the edited text or the revision history of the digital resource. A textual alteration, a scholar's criticism of an identification, and a modern encoder's change to a file can be related events without being the same event. Keeping these levels distinct allows us to ask whose intervention is being reconstructed and what evidence establishes its relation to another.

#### 2.4.1 Editorial mediation and the identity of an intervention

Gabler's (2010) account of the edition as an interplay of discourses provides an important starting point: commentary participates in the edition's intellectual work rather than merely accompanying an independently complete text. Eggert (2019, 80-92) similarly treats archival and editorial purposes as interdependent. Recording documents involves interpretive judgment, while an editorial argument depends on the documentary record and anticipates the concerns of its readers. Together these positions direct attention to the relation between preserving evidence and making an interpretation available for scrutiny.

In the present cases, that relation is visible in Cordier's editorial mediation. The Paper Money addendum conveys Laufer's judgment; our reading must not silently make Cordier its author. Within Laufer's response, the proposition endorsed and the criticism corrected have different roles. Arbre Sec requires another distinction: Cordier's act of replying belongs to the exchange, but the content of that reply does not establish adoption of the competing identification. A representation that records only a speaker, a date, and a proposition would need further interpretation to recover these differences.

Calling the later act a correction *of* the criticism is consequently an editorial commitment. It binds two interventions and identifies the aspect of the earlier one that is at issue. Calling the other act a reply *to* a proposal makes a different commitment, without incorporating assent into the relation. Our use of these descriptions remains answerable to the passages, their attribution, and the scope of the inquiry. The model gives the commitments explicit consequences; it does not supply the interpretation that justifies them.

#### 2.4.2 Revision, disagreement, and the significance of what remains

Bryant (2010) argues that the study of textual evolution requires access not only to versions but also to the processes of revision made intelligible through sequences and narratives. Fyfe (2012) places digital correction within a longer history of error and the labor of correcting it. These discussions caution against treating an amended result as an adequate account of what has happened. The record of change is itself an object of scholarly interpretation.

The Paper Money reading makes this concern particularly precise. Laufer's endorsement does not make Bretschneider's criticism irrelevant to the exchange. Under our interpretation, the criticism remains necessary to identify what Laufer is correcting. It can cease to determine the local material-result state while continuing to matter as the target of an intervention. The scholarly relevance of an earlier act therefore need not coincide with the continuing acceptance of its proposition.

Arbre Sec reveals a complementary possibility. The record can gain an intervention without acquiring a new accepted identification. Work on co-existing scholarly perspectives already addresses the importance of representing divergent interpretations: Bleeker, Buitendijk, and Haentjens Dekker (2019) combine multiple markup perspectives with a distributed editorial workflow. Their concern with sustaining scholarly discourse is directly relevant here. We focus on the attachments among particular interventions within such a discourse, asking what distinguishes a reply from acceptance of the proposition to which it responds.

These distinctions also connect to computational editing without making the two objects identical. Bleeker and colleagues (2022) show how modelling in-text variation as nonlinear text changes the possibilities of collation. Their work demonstrates the consequences of making a particular understanding of revision computationally explicit. Our comparison concerns relations among scholarly interventions rather than the collation of textual variants. In both settings, the representational choice needs an editorial rationale before its computational consequences can be assessed.

#### 2.4.3 From useful histories to the requirements of a specified act

The importance of history depends on its use, a point already developed by Broyles (2020). His account distinguishes edition content from the environment through which it is encountered, while recognizing the intellectual significance of their interaction. Vancisin and colleagues (2023) likewise make the transformations of historical records relevant to subsequent interpretation, exposing curatorial decisions and otherwise obscured labor. These studies provide grounds for asking how changes become visible and consequential for later research.

We examine a more specific relation within that problem. The relevant inquiry is not simply whether the resource changed or whether its history can be consulted. It is whether the evidence available to a particular operation establishes which earlier act a later intervention addresses. Two researchers using the same edition can legitimately need different parts of that evidence. Reporting Laufer's characterization of his response requires its wording and attribution. Reconstructing the response as a correction of Bretschneider's earlier criticism additionally requires the earlier critical relation. The second inquiry cannot be reduced to the first without changing what has been established.

Unsworth's (2000) discussion of scholarly primitives directs attention to activities rather than scholarly products alone. Here the analytical focus is on the dependencies among activities: an earlier criticism helps constitute the object of a later correction. This is the sense in which prior scholarship produces possibilities for continuation. It does not determine what a later scholar must do. It provides something that a later act can be an act upon.

#### 2.4.4 Making an interpretation testable without making it final

For McCarty (2003), modelling is an exploratory engagement with its object; what resists formalization remains a source of questions. Drucker (2011) presses a related but more demanding issue by treating humanistic data and their display as constituted through interpretation, rather than as observer-independent givens. A declaration of inputs alone does not settle that issue. The reproducibility of a computational consequence must be distinguished from agreement among readers about the interpretation on which it depends.

Our procedure uses that distinction to assign different responsibilities to reading and computation. Close reading identifies the proposed correction, endorsement, or reply and gives reasons for its target binding. The model expresses the requirements of reconstructing the act under that interpretation. Controlled transformations then expose which requirements a representation satisfies, which it leaves unresolved, and which information the operation does not inspect. A disagreement with the historical reading calls for reconsidering the reading and its formalization; it cannot be answered by pointing to passing software tests.

The history-ablation comparison has a correspondingly specific purpose. Once a qualification rule requires a relation, removing that relation should affect its result. That fact alone would merely restate the rule. The interpretive work lies in explaining why reconstructing this correction requires the relation, while recording the specified bibliographical reply does not require the same entry history. The comparison then tests whether the implementation and its information views respect that distinction. The argument depends on this relation between source interpretation and contrastive testing, not on treating either as sufficient by itself.

Figure 1 brings the two readings together by displaying the targets and effects of their interventions. The following formal account turns those distinctions into inspectable conditions while retaining the sources as the basis on which the conditions can be challenged.


![Two editorial continuations in Paper Money and Arbre Sec](figures/figure_1_scholarly_continuation.svg)

**Figure 1.** Relations among interventions in two editorial sequences. Arrows run forward through the documentary layers and identify the target of each later act. Cordier transmits Laufer's response in Paper Money and answers Houtum-Schindler's proposal in Arbre Sec; the latter reply records a bibliographical response without an adoption of the cypress identification. Printed source loci are specified in Section 2.3.

The remainder of the article makes these continuation conditions explicit, compares them, and tests them. The next section defines the evidentiary conditions under which a particular later act can be reconstructed from a represented state.

## 3. Testing support for a later scholarly act

### 3.1 The inquiry and its evidence horizon

We use *qualification* for the evidentiary conditions under which a represented record supports a specified later act. For Paper Money, the inquiry asks whether the later passage can be reconstructed as a correction **of Bretschneider's earlier criticism**. Qualification concerns support for that relational description within the declared record; historical truth and wider scholarly acceptance remain questions for source criticism.

This inquiry has a different evidence demand from reporting how Laufer characterizes his own intervention. The latter needs Laufer's passage and its attribution; reconstructing the exchange also needs the earlier criticism and the relation by which it entered. The PM03 event carries an interpreted relation label, while the state supplies independent evidence that PM02 entered as a criticism of PM01. The controlled comparison tests whether that second component remains available. A missing component is reported as an unresolved condition rather than silently converted into a generic update.

Qualification is evaluated against a declared evidence horizon: the available source passages, their interpreted relations, the represented state, and any permitted recovery procedure. Consulting another edition or reconstructing an omitted relation from the full passage may restore support for the act. The experiment fixes that horizon so that its two representations can be compared.

### 3.2 Current assertions and retained history

Let S denote the represented scholarly state. Its current-assertion projection, Ψ(S), records the assertions and statuses treated as current in the local inquiry. Its evidence and history projection, Ξ(S), retains the relevant documentary events, relations, responsibility, and transitions. These projections operationalize the state/history distinction introduced in Section 1.1.

An incoming intervention e supplies its source-bound relation kind, target, and evidence or proposal. For an action type g, Q_g(S,e) records whether the specified act is qualified. The model also records why a test fails: the target may be absent, the current version may be invalid, or the required target history may be unresolved. If an act qualifies, execution produces a revised state and a record of change. Thus the article's **continuation structure** is the pattern of which specified later acts a representation supports, why, and how each supported act changes the record; Q_g is its testable qualification component.

The Paper Money comparison can now be stated compactly:

\[
\Psi(S_{\mathrm{full}})=\Psi(S_{\mathrm{ablated}}),
\qquad
Q_{\mathrm{RESOLVE}}(S_{\mathrm{full}},e_{\mathrm{PM03}})
\ne
Q_{\mathrm{RESOLVE}}(S_{\mathrm{ablated}},e_{\mathrm{PM03}}).
\]


![Equal current assertions with different continuation support](figures/figure_2_current_state_vs_continuation.svg)

**Figure 2.** Controlled Paper Money comparison. Both representations retain the same current assertions and receive the same later intervention. The full view retains the record that PM02 entered as a criticism of PM01; the reduced view removes that record. Only the full view supports reconstruction of PM03 as a correction *of PM02* under the declared evidence horizon. The reduced view is constructed for this test.

The equality concerns the declared current projection. The full documentary record, including other admissible ways to recover the missing relation, remains a separate object of inquiry. Under the fixed horizon of this comparison, the reduced representation lacks a distinction needed for the specified reconstruction.

### 3.3 Binding requirements differ from state requirements

The exact target of an intervention and the current status of that target are related but distinct. The event can name the correct proposition even when that proposition is absent from the state being consulted. Conversely, an appropriate-looking assertion can be present while the event is bound to a different proposition. Treating both cases as a single target field would conceal the difference between misbinding an intervention and misrepresenting the status of its correctly named target.

We therefore represent the requirements of an action by a typed signature:

\[
\Sigma(g)=(\Beta(g),\Kappa(g)).
\]

Β(g) identifies the event-side binding conditions: the exact object, source or version, relation kind, and target identity. Κ(g) identifies the state-side conditions: whether the bound target is available for the action, whether an update is current, what competing assertions are represented, and whether required target-entry history is retained. *Live* is the model's term for a target available under these state conditions; it does not designate consensus in the wider scholarly community.

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

This implication follows from the stated rule: states that agree on every condition inspected by that rule must yield the same qualification result. The general question of whether a view determines an answer has a substantial technical literature (Nash, Segoufin, and Vianu 2010). Here the substantive work is to establish the historically meaningful conditions for particular editorial acts and to test how those conditions behave when acts are composed. The finite checks assess implementation and contrastive behavior; they do not turn the implication into a new general theorem.

### 3.4 What the evaluation tests

The evaluation combines the close readings described in Section 2.3, two separately implemented qualification-and-execution paths, and controlled transformations of the represented state. The source-derived relation labels were fixed before the relevant composition tests. Both historical sequences run through the same target-bound implementation without episode-name or claim-identifier branches. Agreement between implementations checks conformity to the specified rules; determining whether a passage is a correction or bibliographical reply remains an interpretive act documented in the source reading.

The controls have different purposes. Removing a required relation tests whether the specified act loses support. Perturbing a condition the rule does not inspect tests whether the implementation is unnecessarily restrictive. Supplying a later intervention before its target has entered tests sequence dependence. These are finite model tests over documentary inputs.

## 4. Not every continuation requires the same past

### 4.1 Arbre Sec: recording a reply without manufacturing assent

The Arbre Sec reading in Section 2.2 supplies the contrast. Its 1903 layer already contains an identification and a botanical objection-and-response context. The modeled starting state therefore contains an identification with prior interpretation. The 1920 layer introduces Houtum-Schindler's cypress proposal and Cordier's bibliographical reply. Recording that reply as assent would turn evidence of prior reading and citation into an identification Cordier did not explicitly adopt in the inspected passage.

The distinction is consequential. Were Cordier's reply treated as a resolution of the identification, the representation would turn evidence of prior reading into evidence of assent. Were the reply omitted because it leaves the competing identifications unchanged, the representation would erase an act that bears on the history and responsibility of the discussion. The model therefore records it as an evidence-bearing reply directed at the proposal, while retaining both competing identification assertions.

In the model, adding the alternative makes the cypress proposal available as a distinct target; recording Cordier's reply then attaches evidence to that target. The implemented action types are `ADD_ALTERNATIVE` and `RECORD_EVIDENCE`. Their execution preserves the current assertion projection while changing the retained evidence and history:

\[
\Psi(S_{\mathrm{before\ reply}})=\Psi(S_{\mathrm{after\ reply}}),
\qquad
\Xi(S_{\mathrm{before\ reply}})\ne\Xi(S_{\mathrm{after\ reply}}).
\]

For this specified reply, the model inspects the target's identity and availability, without requiring its earlier entry transition. Paper Money's correction has the additional demand of identifying the target's entry as a criticism. The two later acts therefore read different parts of their represented histories.

### 4.2 Comparing obligations rather than quantities of metadata

The paired cases show that the evidence needed for a later act depends on the act's relation to its target. Table 2 compares these requirements with two actions from the machine-readable record examined in Section 6. Its rows report the focal conditions; the full specifications also check source, relation, proposal, and status.

| Specified later act | Focal binding and current-state conditions | Is retained target-entry history inspected for qualification? |
| --- | --- | --- |
| Paper Money: correct the prior criticism, modeled as RESOLVE | The correction addresses the live critical assertion; the proposal matches the relevant live alternative | Yes: the target's entry as a criticism of the prior assertion must be established |
| Arbre Sec: record Cordier's bibliographical reply | The reply addresses the particular available competing proposal | No, for this specified reply |
| Formalization Papers: record a response | Exact review/update targets are available and current | Yes: the relevant review/update entry history must be established |
| Formalization Papers: revise publication status | Exact target binding and the required current update | No, for this specified status action |

**Table 2.** Contrasting requirements for four specified actions. “No” means that the named action does not inspect target-entry history during qualification; another inquiry may still need it.

The finite signature audit checks 120 action contexts: four from the two Yule–Cordier sequences and 116 from Formalization Papers (48 review, eight replacement, 52 response, and eight publication-status contexts). All 120 retained their qualification result under transformations that preserve the conditions inspected by the action. All 393 required-condition tests changed or blocked the specified action as expected; all 19 tests altering a nonrequired history condition preserved qualification. The 393 include target binding and state requirements as well as history requirements.

These are tests of a specified finite model, not independent historical episodes or estimates of prevalence. Their value is discriminatory: changing a required condition affects the action, while changing a tested nonrequired history condition does not. The comparison asks what a particular continuation reads, rather than rewarding a representation simply for carrying more metadata.

## 5. Earlier acts establish later possibilities

The two historical sequences show why later acts cannot be assessed from an unordered inventory of statements. In Paper Money, recording the criticism creates a competing target and establishes its relation to the baseline. A correction attempted before that target enters is rejected because the target is absent. If the target remains but its critical entry relation is removed, the same later intervention receives a different diagnosis: the target exists, but the history needed to substantiate the correction is unresolved.

Arbre Sec separates target creation from history-dependent continuation. Recording the competing identification creates the target to which Cordier's reply is bound. Before that proposal is present, the reply does not qualify. After it is present, the reply can be recorded without reading its entry history. The earlier act therefore enables a later act even where the later act neither changes the current identification assertions nor requires the full transition record.

An earlier act can create the target named by a later event, make it available in the represented state, establish its version status, or supply the entry relation inspected by a later qualification rule. The sequence audit checks these concrete dependencies. Both historical sequences satisfy the specified forward and premature-action controls.

The premature-action controls ask whether an intervention is available from a specified starting state. They reveal order-sensitive dependencies within the tested sequences. “Sequence closure” means that the earlier acts in a tested chain supply the conditions inspected by its later acts.

The resulting humanistic claim concerns the afterlife of an intervention. A criticism can become an object of later criticism; a proposal can become the object of a reply. Earlier scholarly work thus produces some of the objects and relations through which later inquiry proceeds. Preserving only a conclusion can remove the means of distinguishing these continuations. Preserving a reply only as a conclusion change can do the opposite: invent a settlement where the record contains a further act of discussion.

## 6. A bounded test in an independent scholarly ecology

The Yule–Cordier cases establish the article's interpretive problem. Formalization Papers, a scholarly publishing record associated with Bucur and colleagues (2023), provides a second documentary setting in which later acts explicitly target earlier ones. Its machine-readable links among submissions, reviews, updates, responses, and decisions permit the same distinctions—exact target, available target, and retained entry history—to be tested without supplying relations by close-reading these two editorial passages. This is a mechanism comparison across two kinds of scholarly record, with the printed edition remaining the historical core of the DH argument.

The source snapshot contains ten record files. Reconstructing the relation graph yields fifteen candidate roots: eight have the complete structure required by the declared composition test, and seven are ambiguous or lack functional relations for that test. All fifteen receive a documented disposition. The eight eligible roots yield 52 connected review–update–response–decision chains under the fixed enumeration rule. Chains share roots and documentary components, so 52 is the number of testable paths, not 52 independent scholarly episodes.

In the corrected execution, all 52 eligible chains satisfy the specified forward and counterfactual checks. A chain records a review, replaces the represented formalization, records a response, and revises publication status. Controls attempt later acts before their targets exist, substitute wrong targets where structurally possible, and remove required history while holding the current update projection fixed. A separate auditor reconstructs the roots and connected chains from the source files and obtains the same population as the main analysis.

A further diagnostic comparison uses three information views: one with functional relation-target bindings, one that also checks whether a target is currently available, and one that additionally retains the history required for the response action. Table 3 reports the results on three different test populations. “False availability” means that a view admits an action despite the source-derived conditions specified for this test.

| Test population | Functional target binding | Binding plus live/current target | Binding, current target, and required history |
| --- | ---: | ---: | ---: |
| Valid response contexts retained, n = 52 | 52/52 | 52/52 | 52/52 |
| False availability on natural non-live-target response acts, n = 47 | 47/47 | 0/47 | 0/47 |
| False availability on controlled history-ablated response contexts, n = 52 | 52/52 | 52/52 | 0/52 |
| Availability on the nonfunctional-target control, n = 1 | 0/1 | 0/1 | 0/1 |

**Table 3.** Information-view comparison for response qualification. The 47 naturally non-live-target acts and 52 constructed history-ablated contexts have different denominators. The columns are defined information projections, not implementations of a named metadata standard.

The comparison distinguishes two obligations. A relation can point to a target that is unavailable for the specified action; checking target availability removes the 47 false admissions in that population. An available target can still lack the recorded entry history required for a response; checking that history removes the 52 false admissions in the constructed ablation population. All 52 valid response contexts remain available in every view. The publication-status contrast in Table 2 shows why entry history is required for some acts but not all.

The first prospective execution failed a parser check and yielded no valid confirmatory result. The corrected reproduction used the identical source archive after repairs to date-time serialization and multi-valued creator handling; independent parsers then agreed on the relevant source surface. The 52-chain result is reported as a **corrected reproduction**, while the subsequent signature and information-view comparisons are post-exposure diagnostic analyses. The initial failed execution remains part of the public evidence record.

## 7. Implications for digital editions and historical records

### 7.1 What persists after a correction, and what changes in a reply

The two sequences give different answers to the question of what a later intervention changes. In Paper Money, the local model allows Laufer's response to resolve the represented material competition while retaining the criticism it addresses. In Arbre Sec, Cordier's reply adds to the history of the exchange without establishing adoption of the competing identification. Neither sequence is adequately described by equating scholarly significance with a replacement of the current answer.

For the first sequence, the persistence of the criticism has a positive purpose. It allows a later reader to distinguish endorsement of an identification from correction of a particular objection to it. Its retention does not require continuing to treat its proposition as accepted. For the second, recording the reply allows the discussion to remain visible without taking the further interpretive step of declaring agreement. The representation must distinguish what happened in the exchange from what, on the available evidence, happened to the competing claims.

The notion of continuation structure identifies these dependencies as an object of editorial attention. It develops the relational understanding of editions articulated by Gabler and the concern with intelligible revision expressed by Bryant, while concentrating on the conditions needed to reconstruct particular later interventions (Gabler 2010; Bryant 2010). Its contribution is the connection among a source reading, an action-specific evidentiary requirement, and a comparison of what different representations support. The article does not establish that relational editing, interpretive revision histories, or task-dependent uses of provenance originate here.

This perspective also gives the controlled comparison an editorial interpretation. Equal current assertions establish a carefully bounded point of agreement between two views. The difference in continuation support identifies something else a specified inquiry needs. Recovering that distinction from an admissible passage would repair the reduced view for that inquiry. The possibility of repair is consistent with the argument: it locates the evidence whose availability matters.

### 7.2 Representation standards and editorial obligations

The required distinctions do not dictate a single encoding. PROV-DM supplies resources for relating entities, activities, and agents (W3C 2013). TEI should not be represented solely by its file-revision facilities: alongside `revisionDesc`, its `relation` and `standOff` elements provide resources for relationships and stand-off annotation (TEI Consortium n.d.). These facilities make possible implementations worth considering, rather than constituting comparators already tested in this article.

Argumentation models are also relevant. CRMinf 1.2.1 explicitly distinguishes propositions, beliefs, inference making, and belief adoption, including the interpretation and provenance of the sources on which adoption depends (CRMinf 2026). Its presence prevents us from treating the representation of scholarly argument as an unoccupied technical space. Establishing whether a particular implementation satisfies the continuation requirements examined here would require a specified mapping and the same source-bound tests. No such implementation comparison is reported in the present evidence.

For an editor, the resulting obligation is to make the relation needed by the inquiry recoverable under the declared means of access. A textual note may do this; so may linked annotations or a versioned graph. The name of a format cannot decide the matter. Nor does successful storage by itself establish successful exposure to a reader or availability to a particular operation. The distinction between content and access conditions, emphasized by Broyles (2020), becomes consequential at the level of an individual act.

Responsibility must remain visible across these arrangements. Laufer's correction, Cordier's transmission of it, and a present-day researcher's classification of the passage are distinct contributions to the record. An implementation may connect them, but should not let one stand silently for another. A future reader must be able to question our classification without thereby being forced to deny that the source contains the passage or that Cordier transmits it. This separation makes an interpretation revisable while keeping its documentary basis inspectable.

### 7.3 Working views and the openness of future inquiry

Action-relative requirements describe what a specified inquiry needs; they do not establish what every future inquiry will need. The registered Arbre Sec reply does not inspect its target's entry history. A study of priority, citation, mediation, or the development of the identification might require precisely that history. A successful reduced view for one operation therefore supplies no general argument for deleting evidence from the retained record.

The practical distinction is between a working view and the source resources to which it remains accountable. A working view can expose the information needed for a particular continuation while retaining a route back to the evidence from which its distinctions were drawn. When a new question falls outside the declared family of acts, returning to those sources is part of research rather than a failure to comply with the model. The findings specify where existing support ends; they do not close the range of questions an edition may sustain.

The relation to future inquiry is consequently both selective and open. A representation can explain why a particular correction or reply is supportable now, without claiming to have anticipated every later use. It can also report an unresolved relation without pretending that an unresolved condition is a settled negative historical judgment. The controlled failures are useful insofar as they identify what would have to be recovered, reinterpreted, or added before the stronger reconstruction could be made.

Computational precision has a role within this openness. It makes the consequences of selected interpretations repeatable and exposes when two operations require different evidence. The historical readings, however, remain available for disagreement, and the independent record ecology tests the specified mechanism rather than adjudicating those readings. The model's value is to articulate the obligations of an interpretation clearly enough that both its consequences and its premises can be examined.


## 8. Limits and conclusion

### 8.1 Evidentiary limits

The two historical sequences were selected because they distinguish a correction from a bibliographical reply. They support a bounded interpretive contrast, not an estimate of how often such acts occur in the Yule–Cordier corpus. Paper Money's last event combines a correction and endorsement in one modeled intervention; Arbre Sec offers a cleaner single-act reply. Earlier arguments quoted by Cordier are examined through their editorial transmission here, rather than as independently inspected witnesses.

Independent historical corroboration remains unresolved. A blinded three-model audit completed 45 calls over five cases; only nine responses met the predeclared source-citation criterion, and none of the 21 atomic components reached the required stable two-model agreement. This partial result is reported as a limitation on corroboration of the source readings. It is distinct from the computational tests of the specified representations.

The computational tests evaluate the consequences of the stated interpretations and rules. Independent implementations reduce implementation risk, while the historical requirement built into each rule remains open to scholarly challenge. The Paper Money comparison establishes what follows when reconstructing a correction *of an earlier criticism* requires evidence of that criticism's entry relation. An alternative inquiry that reports only Laufer's later characterization has a different evidence demand.

The finite tests also leave three Yule witnesses in which exact target identity and live-target lookup change together. Formalization Papers supplies additional typed probes, although its chains share roots and its first prospective execution failed. The reported counts describe tested contexts and paths; they provide no estimate of cross-domain prevalence or automatic extraction accuracy.

The current-state equality in Figure 2 is an experimental condition on a declared projection. Enriching that projection or permitting recovery from another source can restore the missing relation. This specifies the access boundary of the result and points to practical ways a digital edition can support the inquiry.

### 8.2 Conclusion

An edition can preserve a defensible answer and still lose the relations through which that answer became a correction of an earlier criticism. It can preserve the words of a reply and still misrepresent the exchange by treating the reply as assent. The paired readings show why the continuation of scholarship requires attention to the identity, target, and effect of an intervention, alongside the proposition it leaves in place or changes.

The requirements differ with the act. Under the declared Paper Money inquiry, the correction depends on the earlier critical relation; the Arbre Sec reply requires its identifiable proposal without thereby resolving the identification. The computational comparisons make these interpreted requirements inspectable and show where particular representations support or interrupt the corresponding reconstruction.

Scholarly continuation thus offers a way to connect editorial interpretation with the design and assessment of digital representations. An earlier act can remain consequential after its proposition ceases to govern the local answer, and a later act can matter without settling that answer. Preserving these possibilities allows an edition to transmit an argument while keeping the scholarship through which it developed available for further inquiry.


## References

Birnbaum, David J., and Elena Spadini. 2020. “Reassessing the Locus of Normalization in Machine-Assisted Collation.” *Digital Humanities Quarterly* 14 (3). https://www.digitalhumanities.org/dhq/vol/14/3/000489/000489.html.

Bleeker, Elli, Bram Buitendijk, and Ronald Haentjens Dekker. 2019. “Agree to Disagree: Modelling Co-existing Scholarly Perspectives on Literary Text.” *Digital Scholarship in the Humanities* 34 (4): 844–854. https://doi.org/10.1093/llc/fqz061.

Bleeker, Elli, Bram Buitendijk, Ronald Haentjens Dekker, Vincent Neyt, and Dirk Van Hulle. 2022. “Layers of Variation: A Computational Approach to Collating Texts with Revisions.” *Digital Humanities Quarterly* 16 (1). https://dhq.digitalhumanities.org/vol/16/1/000583/000583.html.

Broyles, Paul A. 2020. “Digital Editions and Version Numbering.” *Digital Humanities Quarterly* 14 (2). https://www.digitalhumanities.org/dhq/vol/14/2/000455/000455.html.

Bryant, John. 2010. “Rewriting Moby-Dick: Politics, Textual Identity, and the Revision Narrative.” *PMLA* 125 (4): 1043–1060. https://doi.org/10.1632/pmla.2010.125.4.1043.

Bucur, Cristina-Iulia, Tobias Kuhn, Davide Ceolin, and Jacco van Ossenbruggen. 2023. “Nanopublication-Based Semantic Publishing and Reviewing: A Field Study with Formalization Papers.” *PeerJ Computer Science* 9: e1159. https://doi.org/10.7717/peerj-cs.1159.

Cordier, Henri. 1920. *Ser Marco Polo: Notes and Addenda to Sir Henry Yule's Edition, Containing the Results of Recent Research and Discovery*. London: John Murray. [Digitized copy](https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf).

CRMinf. 2026. “Classes & Properties Declarations of CRMinf Version 1.2.1.” Version 1.2.1, April 2026. https://cidoc-crm.org/extensions/crminf/html/CRMinf_v1.2.1.html. Accessed 30 September 2026.

Drucker, Johanna. 2011. “Humanities Approaches to Graphical Display.” *Digital Humanities Quarterly* 5 (1). https://dhq.digitalhumanities.org/vol/5/1/000091/000091.html.

Eggert, Paul. 2019. “Digital Editions: The Archival Impulse and the Editorial Impulse.” In *The Work and the Reader in Literary Studies: Scholarly Editing and Book History*, 80–92. Cambridge: Cambridge University Press. https://doi.org/10.1017/9781108641012.006.

Fyfe, Paul. 2012. “Electronic Errata: Digital Publishing, Open Review, and the Futures of Correction.” In *Debates in the Digital Humanities*, edited by Matthew K. Gold, 259–280. Minneapolis: University of Minnesota Press. https://doi.org/10.5749/minnesota/9780816677948.003.0027.

Gabler, Hans Walter. 2010. “Theorizing the Digital Scholarly Edition.” *Literature Compass* 7 (2): 43–56. https://doi.org/10.1111/j.1741-4113.2009.00675.x.

McCarty, Willard. 2003. “‘Knowing True Things by What Their Mockeries Be’: Modelling in the Humanities.” *Computing in the Humanities Working Papers* A.24. https://chwp.artsci.utoronto.ca/CHC2003/McCarty2.htm.

Nash, Alan, Luc Segoufin, and Victor Vianu. 2010. “Views and Queries: Determinacy and Rewriting.” *ACM Transactions on Database Systems* 35 (3), article 21: 1–41. https://doi.org/10.1145/1806907.1806913.

TEI Consortium. n.d. “relation,” “standOff,” and “revisionDesc.” *TEI P5: Guidelines for Electronic Text Encoding and Interchange*. https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-relation.html; https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-standOff.html; https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-revisionDesc.html. Accessed 30 September 2026.

Unsworth, John. 2000. “Scholarly Primitives: What Methods Do Humanities Researchers Have in Common, and How Might Our Tools Reflect This?” King’s College London, 13 May. https://people.brandeis.edu/~unsworth/Kings.5-00/primitives.html.

Vancisin, Tomas, Loraine Clarke, Mary Orr, and Uta Hinrichs. 2023. “Provenance Visualization: Tracing People, Processes, and Practices through a Data-Driven Approach to Provenance.” *Digital Scholarship in the Humanities* 38 (3): 1322–1339. https://doi.org/10.1093/llc/fqad020.

W3C. 2013. *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/.

Williamson, Elizabeth R. 2026. “Digitized Archives, Content Providers, and Slow Scholarship: Why Archival Researchers Should Care about Digital Provenance.” *Digital Scholarship in the Humanities* 41 (3): 1705–1723. https://doi.org/10.1093/llc/fqag062.

Yule, Henry, and Henri Cordier. 1903. *The Book of Ser Marco Polo*. Third edition. Vol. I. London: John Murray. [Digitized volume](https://wellcomecollection.org/works/j5n87wpb).

## Evidence and materials statement

The printed source passages and their page-image anchors, interpretive claim records, protocols, scripts, raw outputs, correction history, and denominator audits are documented in the [source and evidence register](SOURCE_NOTES_AND_SUBMISSION_GAPS.md) in the [project repository](https://github.com/MKLEE222/claim-relative-representation). The Formalization Papers analysis used a fixed ten-file snapshot of the [supplementary repository](https://github.com/LaraHack/formalization_papers_supplemental); its exact commit and archive checksum appear in the register. That register also separates the failed prospective execution, corrected reproduction, and subsequent diagnostic analyses. Final source-image quotation checks and the dataset's reuse terms remain submission requirements.
