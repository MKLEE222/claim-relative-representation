# Theoretical Foundations Audit v1

Date: 2026-09-26
Status: manuscript foundation; literature-grounded, not a novelty claim by itself

## Purpose

This audit asks what intellectual foundations the paper should inherit before claiming a new framework.

The paper should not present task-relative adequacy, provenance, editorial modelling, or argument acceptance as if they arose from nowhere. Its contribution is narrower: to connect these traditions into a source-bound, experimentally auditable account of when a scholarly representation remains sufficient for a specific historical task.

---

## 1. Digital scholarly editing: representation is already known to be interpretive and use-dependent

### Shillingsburg: electronic surrogates are shaped by intended use

Peter Shillingsburg's account of electronic scholarly editions treats the electronic surrogate as a representation whose design depends on what users are expected to do with it. This directly blocks any naive premise that a digital text is simply a neutral copy of a material witness.

Relevant works:

- Peter Shillingsburg, “How Literary Works Exist: Convenient Scholarly Editions,” *Digital Humanities Quarterly* 3.3 (2009).
  https://www.digitalhumanities.org/dhq/vol/3/3/000054/000054.html

- Peter Shillingsburg, “Reliable social scholarly editing,” *Digital Scholarship in the Humanities* 31.4 (2016), 890–897.
  https://doi.org/10.1093/llc/fqw044

Important inheritance:

- archive and edition are not the same object;
- an edition is an argument about archival material, not a neutral container;
- representational choices should be judged relative to scholarly use.

Our paper should NOT claim these as novel.

### Pierazzo: digital transcription requires principled stopping rules

Elena Pierazzo argues that the permissiveness of the digital medium does not remove editorial selection; it makes the stopping problem more explicit. A digital documentary edition is not merely a transcription but a publication form comprising source, outputs, and tools.

Relevant works:

- Elena Pierazzo, “A rationale of digital documentary editions,” *Literary and Linguistic Computing* 26.4 (2011), 463–477.
  https://doi.org/10.1093/llc/fqr033

- Elena Pierazzo, “Modelling Digital Scholarly Editing: From Plato to Heraclitus,” in *Digital Scholarly Editing: Theories and Practices* (2016), 41–58.
  https://doi.org/10.11647/OBP.0095.03

Important inheritance:

- digital representation is selective;
- modelling choices instantiate scholarly assumptions;
- “more encodable detail” is not equivalent to “better edition.”

Our paper extends this by asking which retained relations are sufficient for a declared task and by making that question experimentally testable.

### Robinson / Textual Communities: document and work views are distinct operational structures

Peter Robinson explicitly warns that digital methods should not displace the editor's basic questions about why and for whom an edition is made. His later work on Textual Communities distinguishes document views from work/entity views and treats multiple texts as computationally comparable objects.

Relevant works:

- Peter Robinson, “What text really is not, and why editors have to learn to swim,” *Literary and Linguistic Computing* 24.1 (2009), 41–52.
  https://doi.org/10.1093/llc/fqn030

- Peter Robinson, “Some principles for making collaborative scholarly editions in digital form,” *Digital Humanities Quarterly* 11.2 (2017).
  https://www.digitalhumanities.org/dhq/vol/11/2/000293/000293.html

Important inheritance:

- document/text/work distinctions matter operationally;
- digital scholarly environments encode a model of scholarly use;
- comparison and reconstruction depend on the model, not only on visible strings.

### van Zundert: graph-based editions expose what book-shaped representations close down

Joris van Zundert argues that graph-based modelling can keep relations among textual, material, interpretive, and computational information processable in ways that book-like models can obscure.

Relevant work:

- Joris van Zundert, “The case of the bold button: Social shaping of technology and the digital scholarly edition,” *Digital Scholarship in the Humanities* 31.4 (2016).

Important inheritance:

- relation structure may be a first-class computational object;
- representation architecture can enable or disable later algorithmic negotiation.

Our paper should position its carrier/relation model as an experimentally constrained version of this broader modelling insight, not as the first claim that graphs or relations matter.

---

## 2. Markup and modelling: encoding is an interpretive act

Work on digital editions and markup repeatedly emphasizes that encoding choices are interpretive rather than transparent.

A useful concrete statement appears in the DHQ “Model of Versions and Layers” discussion: markup is an interpretative act, and syntactic consistency does not guarantee semantic consistency.

Relevant work:

- “A Model of Versions and Layers,” *Digital Humanities Quarterly* 13.3 (2019).
  https://www.digitalhumanities.org/dhq/vol/13/3/000430/000430.html

This supports our distinction among:

- semantic presence;
- explicit encoding;
- recoverability;
- operational availability.

The paper's novelty is not that markup interprets. It is the task-contract framework for determining when a representation still carries enough source-grounded structure for a scholarly operation.

---

## 3. Provenance: origin and transformation history are established requirements

### W3C PROV

W3C PROV formalizes provenance in terms of entities, activities, agents, derivation, responsibility, and versioned transformation.

Relevant sources:

- W3C, *PROV Model Primer*.
  https://www.w3.org/TR/prov-primer/

- W3C, *PROV-O: The PROV Ontology*.
  https://www.w3.org/TR/prov-o/

Important inheritance:

- attribution, derivation, activity, responsibility, and version history are standard provenance concerns;
- provenance can support assessments of quality, reliability, and trustworthiness.

This is a direct intellectual ancestor of our Stage-A documentary ontology.

Our paper should therefore say that D_ATTRIBUTION, D_TEMPORAL_SUCCESSION, D_CITATION_DERIVATION, etc. operationalize scholarly-documentary relations for a narrower experimental task; they are not a replacement for PROV.

### DH provenance work

Vancisin et al. argue that historical records undergo transformations in digitization and that provenance disclosure should document changes in transcription, organization, content, and representational form.

Relevant work:

- Tomas Vancisin, Loraine Clarke, Mary Orr, and Uta Hinrichs, “Provenance visualization: Tracing people, processes, and practices through a data-driven approach to provenance,” *Digital Scholarship in the Humanities* 38.3 (2023), 1322–1339.
  https://doi.org/10.1093/llc/fqad020

Recent work on cultural-heritage RDF likewise treats versioning, justification, entailment, access, trust, and provenance representation as live problems.

Relevant work:

- “Representing provenance and track changes of cultural heritage metadata in RDF: a survey of existing approaches,” *Digital Scholarship in the Humanities* 41.Supplement_1 (2026), i196–i212.
  https://doi.org/10.1093/llc/fqaf076

Gap relative to this literature:

Provenance work asks how to preserve and disclose transformation history. Our question is narrower and downstream:

> which provenance/documentary relations are actually required for a declared scholarly task, and what happens when one relation is inaccessible while lexical content remains?

---

## 4. Information and data quality: adequacy has long been “fit for use”

Information-quality research does not treat quality as only intrinsic accuracy.

Strong, Lee, and Wang define high-quality data as data fit for use by data consumers and distinguish intrinsic, contextual, representational, and accessibility dimensions.

Relevant work:

- Diane Strong, Yang Lee, and Richard Wang, “Data Quality in Context,” *Communications of the ACM* 40.5 (1997), 103–110.
  MIT TDQM version:
  https://web.mit.edu/tdqm/www/tdqmpub/StrongLeeWangCACMMay97.pdf

Important inheritance:

- adequacy depends on task context;
- accessibility and relevance matter in addition to correctness;
- representational quality is distinct from intrinsic quality.

Our paper should cite this tradition when introducing:

[
Adequacy(R,\tau,K)
]

The new move is not “fitness for use” itself. The new move is to make scholarly fitness relation-specific and to identify minimal source-grounded carrier families under explicit humanities tasks.

---

## 5. Abstract argumentation: attack and reinstatement are standard formal machinery

Dung's abstract argumentation framework models arguments as nodes and attacks as a binary relation, with semantics specifying which arguments can be collectively accepted. Grounded semantics is skeptical and uniquely defined.

Relevant work:

- Phan Minh Dung, “On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games,” *Artificial Intelligence* 77.2 (1995), 321–357.
  https://doi.org/10.1016/0004-3702(94)00041-X

Important inheritance:

- attack/counter-attack and reinstatement are established formal concepts;
- grounded acceptance is not a human-behaviour measure;
- formal semantics can make consequence transparent once an argument graph is supplied.

Our paper should therefore describe the paper-money formal result as an application of established abstract argumentation semantics to a source-verified active scholarly relation graph.

The novelty cannot be “we discovered grounded semantics.”

The manuscript contribution is instead:

> representation/navigation determines which source-bound scholarly arguments and attack relations are operationally active; once that active graph changes, a fixed semantics can produce a different acceptance status.

---

## 6. Where the paper actually sits

The paper is not best framed as:

- a new textual theory;
- a new provenance ontology;
- a new argumentation semantics;
- a generic retrieval algorithm;
- an LLM-evaluation paper.

It sits at the intersection:

[
\text{digital scholarly representation}
\cap
\text{provenance}
\cap
\text{task-relative information quality}
\cap
\text{formal argument availability}.
]

The proposed substantive contribution is:

### Contribution A — Task-relative scholarly representation adequacy

A representation is adequate only relative to a scholarly task and contract:

[
Adequacy(R,\tau,K).
]

### Contribution B — Minimal sufficient carrier families

For a frozen task, more information is not automatically better; there may be one or more minimal carrier sets sufficient for the task:

[
\mathcal{M}_{\tau,K}.
]

### Contribution C — Source-grounded mediation

Scholarly access depends on typed relations such as attachment, referent identity, citation, sequence, and explicit pointer, not only lexical similarity.

### Contribution D — Consequence through active argument structure

Representation/navigation can change the active source-bound argument graph. Under a fixed skeptical formal semantics, this can change formal claim acceptance.

### Contribution E — Negative boundary on generic LLM adjudication

Three frozen local LLM judges did not reliably recover the selective relation-sensitive consequence. This is a boundary result showing that textual availability alone does not guarantee computational use of evidential structure.

---

## 7. Novelty claims we should avoid

Do not claim:

- “digital editions are interpretive” — established;
- “provenance matters” — established;
- “data quality is task-dependent” — established;
- “argument graphs can represent attacks” — established;
- “graphs are better than books” — too broad and already argued in scholarly-editing literature;
- “LLMs cannot reason about evidence” — not supported by three models on one task.

Safer novelty sentence:

> We operationalize task-relative scholarly representation adequacy as a source-bound recovery problem, identify minimal carrier families across independent DH infrastructures, and show in a historical editorial case how representation-mediated evidence exposure changes the active argument graph and therefore formal claim acceptance under a fixed semantics.

---

## 8. Related-work structure for the manuscript

Recommended four-paragraph related-work sequence:

1. digital scholarly editing and representation as modelling / argument;
2. provenance and transformation history;
3. task-relative information quality and adequacy;
4. argumentation as downstream consequence semantics.

The final paragraph should identify the gap:

> these traditions explain why representation, provenance, task context, and argument relations matter, but they do not by themselves provide an experimentally auditable framework for asking which source-grounded relations are sufficient for a specific humanities task, which are redundant, and what downstream scholarly consequence follows when a required relation becomes operationally unavailable.
