# After Revision: Scholarly Continuation and Action-Relative Researchability in Digital Editions

*Theory-first opening draft for manuscript v2 — 30 September 2026. This file rewrites the paper's disciplinary entry point. It does not replace or modify frozen experiments.*

## Abstract

Digital scholarly editions do more than preserve textual states and document their histories. They also shape the conditions under which later scholarship can continue from those histories. This article develops a Digital Humanities account of **scholarly continuation**: the historically grounded capacity of a representation to support later acts that address, revise, qualify, or record earlier scholarship. The problem is distinct from preserving a latest state, and it is not exhausted by recording provenance in the abstract. A later correction may depend on identifying the precise criticism it corrects; a bibliographical reply may matter to the history of an interpretation without settling that interpretation. We argue that digital scholarly representations therefore have a **continuation structure** in addition to a current scholarly state and a record of prior intervention.

Two sequences in the Yule–Cordier editorial record of *Marco Polo* provide the central cases. In the Paper Money sequence, a criticism becomes the specific object of a later counter-criticism. In the Arbre Sec sequence, a competing identification occasions a bibliographical reply that changes the recorded history of discussion without establishing assent to the proposal. Their contrast motivates an action-relative account of researchability: different scholarly continuations require different relations, targets, and historical conditions. We operationalize these requirements through a source-bound model that separates event-side binding from state- and history-side qualification, and we test the same distinction in a second machine-readable ecology of scholarly review and revision.

The contribution is not a universal vocabulary of scholarly acts or a claim that software determines what scholars may do. It is a theory of how digital representations mediate the **continuability of scholarship**: what must remain recoverable for a later intervention to remain reconstructible as the historically specific intervention it is.

**Keywords:** digital scholarly editing; scholarly continuation; researchability; provenance; editorial history; digital humanities modelling; scholarly activities

## 1. Digital editions do not only preserve scholarship; they condition its continuation

A scholarly edition is often evaluated in terms of what it preserves: texts, variants, witnesses, annotations, provenance, revision history, or the state of a digital resource at a given version. Each of these questions matters. Yet scholarship proceeds not only by recovering what a record contains, but by acting upon earlier scholarly acts. A critic answers a prior interpretation. An editor corrects an earlier note. A later scholar distinguishes transmission from adoption, revises an attribution, records new evidence, or reopens a proposition that had appeared settled. The object inherited by later scholarship is therefore not only a text or a current answer. It is also a structured field of previous interventions to which new interventions can attach.

This article calls that relation **scholarly continuation**.

A scholarly continuation is a later act whose scholarly identity depends on how it attaches to an existing record. To call an intervention a correction *of a prior criticism* is to claim more than that one proposition differs from another. It identifies a target, a relation, and a position in an argumentative history. To record a reply *to a proposal* is likewise different from simply adding another proposition to the same topic. These distinctions are routine in close reading and scholarly editing. Digital representation makes them technically consequential because a model, schema, interface, or access route may preserve some of them while flattening others.

The resulting problem is not reducible to the familiar question of whether an edition has a revision history. A representation can document that changes occurred yet remain insufficient for substantiating a particular relation among them. Nor is the problem reducible to whether a historical statement is still present somewhere in the source. Presence, discoverability, target identity, responsibility, and the conditions for a later intervention are not the same scholarly property. The relevant question is:

> **How does a digital scholarly representation preserve, constrain, or transform the historically grounded possibilities for scholarship to continue?**

This question places the article within several established Digital Humanities traditions while identifying a different unit of analysis. Digital scholarly editing has long treated editions as interpretive constructions rather than transparent surrogates. DH modelling theory similarly understands models as selective and purposive: their value lies partly in making assumptions explicit and manipulable, not in eliminating interpretation. Work on scholarly primitives and information activities shifts attention from scholarly products to activities such as discovering, comparing, referring, annotating, representing, reading, and assessing. Work on versioning and provenance has shown that the history of digital scholarly resources affects citation, interpretation, and future use. We take these positions as premises rather than gaps.

Our additional claim is that **the history represented by an edition has a structure of possible scholarly continuation**. The same represented state can support one later act but not another. Two later acts can require different parts of the past. And an earlier scholarly act can create the very target or relation that makes a later act intelligible. In this sense, the digital representation of scholarship is not only retrospective. It mediates what can be reconstructed *next* from the record under a declared evidentiary horizon.

This does not mean that a digital system determines what scholars may think. A scholar can reopen an archive, consult another edition, challenge a prior interpretation, introduce new evidence, or reject the representation altogether. The claim is narrower: **within a declared scholarly representation and access horizon, representational choices condition which later acts can be substantiated as historically grounded continuations of that record.** A missing relation may be recoverable elsewhere. A different interface may expose it. A richer edition may encode it explicitly. These possibilities do not make the representational question disappear; they identify the scholarly work required to restore or reconstruct the distinction.

### 1.1 From state and history to continuation structure

To make this claim precise without reducing it immediately to implementation, we distinguish three aspects of a scholarly representation.

**Scholarly state** concerns what the local inquiry currently represents: for example, an identification, reading, attribution, or status.

**Scholarly history** concerns how that represented state arose: the interventions, targets, evidence, responsibility, and relations that connect one scholarly act to another.

**Continuation structure** concerns which specified later scholarly acts can be grounded in that state and history, and which distinctions those acts require.

The third category is not another metadata field. It is a relation between a representation and a family of scholarly continuations. It asks whether a record still supports such acts as correcting a criticism, replying to a proposal, or revising a status *as those acts*, rather than merely allowing some new string or node to be appended.

This triad helps distinguish three claims that are often conflated. A representation may preserve a current assertion without preserving the history needed to reconstruct how a later intervention addresses it. It may preserve an extensive history without exposing the relation a particular continuation requires. And it may preserve an act that changes the history of discussion without changing the current proposition at all.

The two historical sequences examined below instantiate exactly these contrasts.

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

These propositions are theoretical claims about digital scholarly representation. The computational formalism introduced later is an operationalization of them, not their disciplinary justification.

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

The remainder of the article asks how these continuation conditions can be made explicit, compared, and tested. The next section therefore introduces **action-relative researchability**: not as a universal logic of scholarship, but as a way to state which historically grounded distinctions a particular continuation requires and to test whether a given representation keeps those distinctions available.
