# Manuscript v0 — Working Draft

Working title:
# When Is a Scholarly Representation Enough?
## Task-Relative Evidence Relations in Digital Humanities

Status: first integrated prose draft
Date: 2026-09-26

---

## Abstract — placeholder

Digital scholarly resources preserve texts through selections about structure, metadata, provenance, linkage, and interface. Yet the adequacy of a representation cannot be inferred from textual fidelity alone: a representation may preserve wording while making the relations required for a scholarly task difficult to recover, or may omit information irrelevant to that task without impairing it. This paper develops a task-relative account of scholarly representation adequacy. For a frozen task and recovery contract, we define adequacy in terms of the source-grounded carriers needed to reproduce the task output and identify minimal sufficient carrier families rather than ranking representations globally. We instantiate the framework in the Yule–Cordier editorial history of Marco Polo and pressure-test it across independent digital-humanities infrastructures including the Frankenstein Variorum, the Walt Whitman Archive, Digital Faust, and a historical corrigenda corpus. The results show that distinct tasks require distinct carrier sets: editorial grouping is not reducible to exact string identity, endpoint recovery can be independent of encoded certainty while certainty adjudication is not, and source-qualified conflict auditing requires provenance not recoverable from file context alone. In the paper-money case, representation-mediated access determines whether a later explicit correction enters the active source-bound argument graph; under a fixed grounded argumentation semantics, selective addition restores the focal claim's formal acceptance while a matched sham does not, and removal reverses the result. A preregistered stress test using three local language models does not reproduce this relation-sensitive consequence, illustrating that textual availability alone does not guarantee computational use of evidential structure. We argue that scholarly representations should be evaluated not by global richness but by the relations they make available for declared tasks.

---

## 1. Introduction — provisional

Digital scholarship rarely encounters a source without mediation. A manuscript becomes an image, a transcription, a TEI document, a collation, a database record, a graph, an interface, or some combination of these. Each form can preserve substantial textual content while changing what is explicit, what is linked, what must be reconstructed, and what can be used computationally. The practical question is therefore not simply whether a digital representation is faithful, detailed, or richly encoded. It is whether the representation is sufficient for the scholarly operation being asked of it.

That distinction is familiar in textual scholarship but difficult to operationalize. Digital editions have long been understood as interpretive models rather than transparent copies, and provenance research has established the importance of recording transformation, derivation, responsibility, and version history. Information-quality research likewise treats quality as contextual and fit for use. These traditions explain why representation and task matter. They do not, however, by themselves tell us how to identify which particular documentary relations are necessary for a given humanities task, which are redundant, or how a representational difference propagates into a downstream scholarly consequence.

We address that problem through a task-relative framework for scholarly representation adequacy. Instead of asking whether one representation is globally “better” than another, we freeze a scholarly task \(\tau\) and a recovery contract \(K\), then ask which source-grounded carriers must remain available or recoverable for the task output to be reproduced. This gives the central object:

\[
Adequacy(R,\tau,K),
\]

where adequacy is a relation among a representation, a task, and a contract rather than an intrinsic scalar property of the representation.

The framework separates three levels that are often collapsed. First, a documentary level records source-verifiable relations such as attribution, attachment, temporal succession, citation, referent binding, witness identity, and editorial layer. Second, an operational level asks whether those relations are explicit, recoverable, composable, or unavailable under a declared access process. Third, a downstream consequence level asks what follows once a scholarly relation is or is not active. The representation layer never directly deletes or inserts an epistemic judgment.

We develop the framework around the Yule–Cordier editorial history of Marco Polo, where later editorial layers sometimes challenge, qualify, or rehabilitate earlier evidential claims. The paper-money episode is the primary consequence case: a 1903 note transmits a botanical objection to Polo's identification of the material used for paper money, while a 1920 addendum transmits a later correction of that objection. The wording of Polo's base report can remain available while the later relation needed to evaluate it falls outside the active evidence state.

The paper then asks whether the framework survives outside this historical chain. We examine a historical corrigenda corpus, the Frankenstein Variorum, the Walt Whitman Archive, and Digital Faust. These independent infrastructures provide different kinds of pressure tests: documentary pointers, editorial grouping, linked loci and certainty, and temporally conflicting scholarly assertions. Across them, the required carrier set changes with the task. More information is not uniformly better, and the same carrier can be redundant for one operation while necessary for another.

The paper makes four main contributions. First, it formalizes task-relative scholarly representation adequacy without reducing it to global richness. Second, it introduces minimal sufficient carrier families for declared humanities tasks. Third, it shows that source-grounded mediation is typed: attachment, citation, referent identity, sequence, and source binding play different roles in different tasks. Fourth, it links representation-mediated evidence exposure to a transparent downstream consequence: in the paper-money case, activating or suppressing an explicit historical correction changes the active argument graph and therefore the focal claim's acceptance under fixed grounded semantics. A preregistered three-model language-model stress test is retained as a negative boundary: two models are stable but insensitive to the relation change, while one is perturbation-sensitive.

The result is not a universal ranking of digital representations. It is a way to ask a more constrained question: what must remain available in a representation for a particular scholarly operation to remain evidentially defensible?

---

## 2. Intellectual foundations and gap — provisional

### 2.1 Editions are models and arguments

Digital scholarly editing has already rejected the premise that an electronic text is a neutral surrogate. Shillingsburg emphasizes that the construction of electronic representations depends on intended use and distinguishes archival surrogates from scholarly editions, which he characterizes as arguments about archival materials. Pierazzo similarly treats digital transcription as a selective scholarly practice whose permissive technical environment intensifies rather than eliminates the need for principled stopping rules. Robinson's work on document and work views, and van Zundert's argument for graph-oriented scholarly models, further establish that the architecture of a representation shapes what can be compared, traversed, and computed.

We inherit this premise rather than claim it as new. Our narrower question is how to determine, for a declared task, which parts of that model are operationally necessary.

### 2.2 Provenance is necessary but not sufficient

W3C PROV provides a general account of entities, activities, agents, derivation, attribution, and transformation history. Recent digital-humanities work likewise emphasizes provenance disclosure for historical records transformed by transcription, reorganization, and digitization. These traditions motivate our documentary relation layer.

Yet complete provenance is not itself our target. A task may require only a subset of available provenance relations, while another task may require a relation that is absent or inaccessible. We therefore ask not merely whether provenance exists, but whether the task-relevant relation can be recovered and used under a declared contract.

### 2.3 Adequacy is contextual

Information-quality research has long treated quality as “fit for use,” distinguishing intrinsic accuracy from contextual, representational, and accessibility dimensions. This supplies a useful ancestor for task-relative adequacy.

Our extension is to make the relevant unit relational and scholarly: instead of asking whether a dataset is useful in general, we ask whether a source-bound relation required for a particular humanistic operation remains available, and whether a smaller carrier set would suffice.

### 2.4 Formal consequence without behavioural overclaim

For the final paper-money consequence, we use Dung-style abstract argumentation only after source-bound relations have been established. Attack and counter-attack are not inferred from model confidence; they are licensed by explicit historical criticism and correction. Grounded semantics then provides a transparent skeptical acceptance status.

This formal layer is intentionally separate from human behaviour. It shows what follows under a declared reasoning contract once the active argument graph changes. It does not claim that historians must reason identically.

### 2.5 Gap

Existing work therefore supplies four foundations: representation is interpretive, provenance matters, quality is task-dependent, and argument acceptance can be formalized. What is missing is an experimentally auditable bridge among them.

We ask:

> Which source-grounded documentary relations are sufficient for a specific scholarly task, which can be removed without consequence, and what downstream effect follows when a required relation ceases to be operationally active?

---

## 3. Framework — first-pass prose

### 3.1 Task contract

Let \(R\) denote a scholarly representation and \(\tau\) a frozen scholarly task. A task contract \(K\) specifies the admissible source universe, background knowledge, recovery operations, output form, and unresolved-state policy.

We write:

\[
Adequacy(R,\tau,K)
\]

for the claim that \(R\), under contract \(K\), is sufficient to reproduce the task output licensed by the reference state.

This definition is intentionally contract-relative. It does not imply that \(R\) is complete, ideal, or preferable for another task.

### 3.2 Documentary relations

We distinguish source-verifiable documentary relations from later epistemic or formal consequences.

The documentary layer includes relations such as:

- attribution;
- attachment;
- temporal succession;
- citation or derivation;
- referent binding;
- witness identity;
- editorial layer;
- modality or certainty markers;
- explicit pointers.

A representation transformation may expose, suppress, or make these harder to recover. It may not directly insert or delete a judgment such as “supports,” “undercuts,” or “rehabilitates.”

This separation prevents a circular experiment in which an analyst-authored epistemic label is first encoded as a representation coordinate and then removed to demonstrate its own importance.

### 3.3 Carrier states and mediation

A documentary distinction can be:

\[
\text{held}
\rightarrow
\text{accessible}
\rightarrow
\text{recoverable}
\rightarrow
\text{composable}.
\]

The distinctions matter. A relation may remain somewhere in the broader source universe while falling outside a task's accessible evidence state. Conversely, a relation may be recoverable through a native pointer, referent bridge, or sequence even when it is not directly adjacent to the seed passage.

We call the source-grounded relation used to bridge such gaps a mediation primitive. The empirical cases instantiate different primitives rather than one universal retrieval method.

### 3.4 Minimal sufficient carrier families

For a frozen task \(\tau\), contract \(K\), and candidate carrier set \(C_\tau\), let \(P_S(R)\) retain only carrier subset \(S\) together with the declared background. \(S\) is task-sufficient when the frozen decoder reproduces the reference output for every registered instance.

A minimal sufficient carrier family is:

\[
\mathcal{M}_{\tau,K}
=
\left\{
S:
S\text{ sufficient and no strict subset of }S\text{ sufficient}
\right\}.
\]

There may be multiple minimal families. The object is not a scalar representation score and not a claim of global storage minimality.

### 3.5 Authority classes

We distinguish:

- **N — native representation:** relations encoded by the historical or external digital object;
- **W — workflow representation:** relations available through a documented scholarly workflow;
- **C — controlled projection:** experimental transformation introduced to test a mechanism;
- **R — source-aligned reference reconstruction:** a source-verified reference state used for evaluation.

R is not treated as an ecological ideal.

### 3.6 Downstream consequence

The empirical framework ends when it establishes which source-bound arguments and relations are active under a representation condition.

A separate formal layer may then evaluate:

\[
AF=(A,\rightarrow)
\]

under a fixed argumentation semantics.

This separation keeps the empirical claim modest:

> representation changes the active scholarly relation structure.

The formal claim is conditional:

> given that structure, the declared semantics yields a different acceptance status.

---

## 4. Historical primary case — section skeleton

### 4.1 Yule–Cordier as a revision chain

[Write historical context: 1903 third edition, Cordier/Yule layer, 1920 addenda, Pelliot review.]

### 4.2 Paper money: criticism and later correction

Load-bearing source events:

- PM01 — base Polo/Yule description;
- PM02 — 1903 Bretschneider objection transmitted by Cordier;
- PM03 — 1920 Laufer correction transmitted by Cordier.

Documentary relations to narrate:

- attribution;
- citation derivation;
- temporal succession;
- explicit pointer from PM03 to the earlier objection;
- referent continuity around the same material-identification question.

### 4.3 Kinsay: eyewitness authority

Use as a qualification mechanism case, not a confirmatory consequence case.

### 4.4 Coal: editorial accretion

Use as a boundary demonstrating that native local attachment can be sufficient.

---

## 5. Results — claim skeleton

### 5.1 Adequacy is task-relative

Use Whitman and Faust to show that the same representation coordinate can matter for one task and not another.

### 5.2 Minimal carrier families differ across infrastructures

Use Scrivener, Frankenstein C18, Whitman, Faust.

### 5.3 Source-grounded mediation is typed

Use PM / Kinsay / Coal.

### 5.4 Paper-money selective reinstatement

Empirical:
generic/guided/rescue/remove conditions change whether PM03 correction is active.

Formal:
grounded status of focal argument changes OUT → IN when the explicit counter-objection is active; sham remains OUT; removal returns OUT.

### 5.5 LLM stress-test boundary

Report:
- Qwen perturbation-sensitive on sham;
- Gemma stable but all RETAIN;
- Llama stable but all RETAIN.

Interpretation:
textual visibility does not guarantee relation-sensitive computational use.

Do not generalize beyond the tested models/task.

---

## 6. Discussion — section skeleton

### 6.1 Richness is not adequacy

### 6.2 Re-expandability and future researchability

### 6.3 Provenance availability versus operational availability

### 6.4 Relation-sensitive computation is a separate requirement

### 6.5 Limitations

- no human behavioural validation;
- PM consequence is one historical chain;
- Kinsay mediation success is exploratory after failure;
- formal argument semantics is a declared contract, not historical truth;
- external infrastructures demonstrate mechanism recurrence, not universal generality.

---

## 7. Conclusion — placeholder

The paper does not propose a universal ideal representation. It proposes a way to ask when a representation is enough for a declared scholarly task, to identify which relations carry that adequacy, and to test what happens when those relations become operationally unavailable.

