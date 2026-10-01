# DH theory identity redesign v1

Date: 2026-09-30  
Status: MANUSCRIPT-THEORY REDESIGN / NO CHANGE TO FROZEN EXPERIMENTS  
Target: next integrated manuscript revision after `MANUSCRIPT_v1.md`

## 1. Reason for the redesign

The first integrated manuscript successfully moved the paper away from a generic information-systems identity. The next revision should go further. It should not merely be a humanities-first presentation of an already-complete computational framework. It should make a Digital Humanities theoretical claim in its own right.

The paper's object is not only provenance, metadata, representation adequacy, or workflow correctness. Its object is the relation between a digital scholarly record and the **continuation of scholarship through that record**.

The central question is therefore sharpened from:

> What must remain recoverable when a scholarly record changes?

to:

> **How does a digital scholarly representation preserve, constrain, or transform the historically grounded possibilities for scholarship to continue?**

This is the paper's DH identity. The historical cases supply the phenomenon; the formal model makes one part of the phenomenon inspectable; the external ecology tests portability. The formalism is not the disciplinary identity.

## 2. First theoretical step: from preservation to scholarly continuation

Digital scholarly editing already treats editions as interpretive constructions rather than transparent copies. Work on scholarly primitives and scholarly information activities treats humanities research as activities rather than only outputs. Work on digital-edition versioning and provenance shows that changes, mediation, and histories matter to scholarly use. DH modelling theory likewise treats models as explicit, interpretive constructions shaped by their intended functions.

The manuscript should enter this conversation by identifying a further object:

### Scholarly continuation

A **scholarly continuation** is a later act that attaches to an existing scholarly record in a historically specific way: for example, correcting a criticism, adding an alternative identification, replying to a proposal, recording evidence, revising an editorial status, or reattributing a claim.

A continuation is not merely "a future action" in the abstract. It is historically grounded when its target, relation, responsibility, and evidentiary basis can be reconstructed under the declared scholarly conditions.

The paper therefore shifts attention from:

- what the edition currently says;
- whether its revision history exists;
- whether provenance metadata is present;

to:

- **which later scholarly continuations the represented record can substantiate, and on what historical grounds.**

## 3. Second theoretical step: from scholarly continuation to continuation-shaped representation

The stronger DH proposition is that digital representation is not only retrospective.

A representation does not merely describe prior scholarship. By preserving some distinctions and flattening others, it also structures which subsequent scholarly acts can be carried out *as historically grounded continuations of that record*.

This does not mean software determines what scholars are allowed to think. Scholars can always reopen sources, reject an editorial model, introduce new evidence, or formulate a different interpretation. The claim is narrower and more useful:

> **Within a declared scholarly representation and access horizon, representational choices condition which continuations can be substantiated from the record itself.**

The paper should therefore describe digital scholarly representations as having a **continuation structure** in addition to a current state and a recorded past.

A useful conceptual triad is:

1. **Scholarly state** — what assertions, identifications, statuses, or readings are represented as current for the local inquiry.
2. **Scholarly history** — how those represented states arose: interventions, targets, responsibility, relations, evidence, and transitions.
3. **Continuation structure** — which specified later scholarly acts can be grounded in that state-plus-history, and which distinctions those acts require.

The third term is the paper's theoretical center.

## 4. Core DH propositions

The manuscript should state four propositions in humanities language before introducing `Sigma(g)`.

### T1 — Current-state preservation is not continuation preservation

A digital representation can preserve the same current scholarly assertions while failing to preserve the historical relation required to reconstruct a later correction, reply, or attribution.

Paper Money is the principal demonstration.

This is not a claim that every textual format loses the relation or that history is irreducible to state. It is a claim that equality of one current scholarly view does not settle equality of continuation structure.

### T2 — Continuation requirements are action-relative

Different scholarly continuations require different distinctions.

A correction-of-a-criticism can require evidence of how the target entered the record. A bibliographical reply can require the existence and identity of its target without requiring that same entry history. A status revision can require still another set of conditions.

Thus preservation should not be theorized as one undifferentiated demand for "more provenance".

### T3 — Scholarly acts are productive, not only archival

An earlier scholarly act does not merely become past metadata. It can create the object, relation, or status that a later act addresses.

A criticism can become the target of a correction. A competing identification can become the target of a reply.

The history of scholarship is therefore partly **productive of later scholarly possibility**.

This is the conceptual bridge from provenance to continuation.

### T4 — Continuation can change scholarly history without changing scholarly state

Some interventions matter because they alter the record of acknowledgment, responsibility, disagreement, or evidence without changing the current represented proposition.

Arbre Sec is the key case.

This prevents a digital edition from equating "no change in current answer" with "no scholarly event worth preserving", and prevents it from turning continued discussion into artificial settlement.

## 5. Relation to established DH theory

The next manuscript should explicitly position itself at the intersection of four DH conversations rather than placing them in a late related-work section.

### 5.1 Digital scholarly editions as interpretation

The paper accepts as a premise that editions and digital models are interpretive, selective constructions. It does not claim to discover that representation is purpose-relative.

### 5.2 Scholarly primitives and information activities

Unsworth and later work conceptualize scholarship through activities such as discovering, comparing, referring, annotating, representing, reading, and assessing. The present paper adds a historical-relational question:

> What must a represented record retain so that one scholarly act can be grounded as a continuation of earlier acts?

The contribution is not a replacement taxonomy of scholarly primitives. It concerns the historical preconditions and dependencies among selected scholarly acts.

### 5.3 Versioning, provenance, and the history of digital scholarly objects

Broyles, Vancisin and colleagues, Williamson, and related work establish that revision, mediation, provenance, and research use matter. The paper builds on that foundation.

Its additional unit of analysis is neither the version alone nor provenance disclosure alone, but the **continuation condition**: the specific historically grounded distinctions needed for a later act to attach to the record.

### 5.4 DH modelling as explicit interpretation

The formalism should be presented as a DH modelling act: an explicit, revisable interpretation that makes assumptions inspectable and permits controlled comparison.

The model does not eliminate hermeneutics. Its value is that a reader can see exactly what a particular reconstruction treats as necessary, test the consequences, and contest the interpretation.

## 6. Revised paper identity

### Recommended working title

**After Revision: Scholarly Continuation and Action-Relative Researchability in Digital Editions**

Alternative stronger title:

**How Scholarship Continues: Historical Action and Researchability in Digital Editions**

Use the first unless a later venue/style review favors the more declarative second title.

### One-sentence identity

> This article develops a DH account of **scholarly continuation**: the historically grounded capacity of a digital scholarly representation to support later acts that address, revise, qualify, or record earlier scholarship.

### One-sentence central contribution

> It shows that scholarly continuation depends neither on current state alone nor on provenance in the abstract, but on action-relative relations whose preservation can determine whether a later intervention remains reconstructible as the intervention it historically is.

## 7. Revised manuscript architecture

The next manuscript should not use the v1 sequence "Paper Money -> extended formalism -> Arbre Sec -> external ecology".

### 1. After revision: the DH problem

Open with the conceptual problem, not the model.

Introduce the triad:

- current scholarly state;
- history of scholarly intervention;
- continuation structure.

Locate the paper immediately in digital scholarly editing, scholarly activities, provenance/versioning, and DH modelling.

End the introduction with T1-T4 and the two historical sequences.

### 2. Two ways scholarship continues

#### 2.1 Paper Money: correction of a critic

Close reading, actor/mediator distinction, target distinction, proposition-specific scope.

Explain that `RESOLVE` is the local modeled consequence of Laufer's attributed intervention, not community consensus.

#### 2.2 Arbre Sec: reply without assent

Close reading of the proposal, its historical/documentary layering, and Cordier's bibliographical reply.

Make the positive DH point explicit:

> an edition must be able to represent continuation of discussion without manufacturing settlement.

#### 2.3 First theoretical synthesis

State T1-T4 in prose.

Only after this point should the paper ask how to operationalize them.

### 3. Action-relative researchability

Define "qualified scholarly continuation" in humanities-first language.

Explain the distinction between:
- recording a later source's characterization of its act;
- substantiating that characterization against retained earlier evidence.

Introduce the declared source/access contract.

### 4. A model of continuation conditions

Now introduce:

- `Psi(S)`;
- `Xi(S)`;
- `Q_g(S,e)`;
- `Sigma(g)=(Beta(g),Kappa(g))`;
- bounded equivalence.

Explicitly state that the factorization implication is specification-level, not the theoretical novelty.

### 5. Historical continuation under controlled transformation

Return to Paper Money and Arbre Sec as tests of the theoretical distinctions.

Put the same-current-state/history-ablation result here.

Keep reverse-order tests explicitly counterfactual and representational.

### 6. Independent ecological test

Introduce Formalization Papers with its originating publication and frozen structured ecology.

Report only the counts necessary to test the theory:
- 52 valid chains;
- non-live-target contrast;
- same-current-state history contrast;
- history-nonrequiring status control.

Retain INVALID -> corrected reproduction boundary.

Move implementation repair details to supplement unless needed for the evidentiary status.

### 7. Toward continuation-aware digital editions

This should be the main theoretical discussion rather than a late implication section.

Develop:
- continuation structure as an evaluative dimension of digital scholarly representation;
- relation to versioning and provenance;
- relation to scholarly activities;
- carrier neutrality;
- source record versus reduced working views;
- why history-only interventions must remain representable.

Do not turn this into software design recommendations unless directly supported.

### 8. Limits and conclusion

Lead with the limits of the *theory's demonstrated range*, not the development history.

Then conclude with the conceptual claim:
digital editions mediate not only what scholarship preserves from the past, but how scholarship can continue from that past.

## 8. Formalism's new role

The notation remains, but its rhetorical status changes.

It is **not**:

- the paper's primary identity;
- a general workflow algebra;
- a universal theory of human scholarly action;
- a proof that every historical relation must be stored in one form.

It **is**:

- an explicit operationalization of continuation conditions;
- a way to separate event-side binding from state/history-side requirements;
- a controlled means of comparing two representations with the same current scholarly view;
- a falsifiable record of what the authors' interpretation commits the model to.

The paper's DH theory must be understandable even if every equation is temporarily removed. The equations then earn their place by making the theory testable.

## 9. Empirical evidence under the new identity

No existing result needs inflation.

### Paper Money

Role: demonstrates current-state / continuation-structure separation.

### Arbre Sec

Role: demonstrates a history-changing continuation without a current-state change, and supplies the strongest anti-"settlement" argument.

### Formalization Papers

Role: tests that the continuation distinction can be operationalized in an independent machine-readable scholarly ecology.

### 120 / 393 / 19

Role: implementation and contrast coverage after the reader understands the theoretical object.

They are not the paper's opening evidence of importance.

### Gate-II BOUNDED_PARTIAL

Role: honest limitation on independent historical adjudication, not the paper's theory test.

## 10. New red-team questions

The next review should ask DH-theory questions first:

1. Does "scholarly continuation" name a real distinction not already exhausted by version history, provenance disclosure, scholarly primitives, or generic affordance?
2. Do Paper Money and Arbre Sec demonstrate two genuinely different forms of continuation rather than merely two programmer-defined action labels?
3. Does the theory explain why an editorial scholar should care about preserving target and relation structure?
4. Can the theory remain carrier-neutral and interpretation-explicit?
5. Does it avoid claiming that a digital system determines what scholars may think or do?
6. Does the external ecology test the theory without becoming the paper's disciplinary identity?
7. Can a reader understand the theoretical contribution before seeing `Sigma(g)`?

Only after these pass should the paper undergo another methods/reproducibility red-team.

## 11. Stop rule

Do not answer this redesign by adding another corpus, another action vocabulary, or a larger theorem.

The next scientific move is manuscript-level theoretical synthesis. New empirical work is justified only if the theory-first rewrite exposes a specific unsupported empirical claim.

Figures remain author-owned. Existing tables can be retained, but their placement and captions should serve the theory-first architecture.
