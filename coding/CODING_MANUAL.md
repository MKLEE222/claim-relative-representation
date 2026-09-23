# CEDL Coding Manual v0.1

## Purpose

This manual tests whether the proposed Claim-Evidence Dependency Layer is recoverable from source material without coding the downstream humanistic decision into the relation label.

The primary coding unit is a **source span relative to a frozen claim**. Coders record primitive relations first. Higher-order mechanisms such as *rehabilitation*, *qualification*, and *interpretive accretion* are derived later.

## Separation rule

Do **not** code `retain / revise / defer / withhold` while coding source relations. Those are downstream adjudications.

Do **not** use `REVISES` as a primitive label merely because a later passage differs from an earlier one. Revision is a derived cross-layer pattern.

## Primitive relation labels

A span may carry more than one primitive label when each is independently source-supported.

### ASSERTS_CONTENT
The span directly states the proposition or observation under study.

### ATTRIBUTES_SOURCE
The span explicitly says that a proposition, document, observation, calculation, or report comes from a named or typed source.

### SUPPORTS
The span supplies evidence that increases the evidential support for the frozen claim without merely restating it.

### CHALLENGES
The span supplies evidence or argument against the frozen claim or against a prior supporting relation.

### QUALIFIES_AUTHORITY
The span leaves substantive content potentially intact but weakens or narrows the authority, eyewitness status, scope, or entitlement under which it may be used.

### DISTINGUISHES_WITNESSES
The span establishes that two textual witnesses or editions make materially different assertions relevant to the claim.

### UPDATES_IDENTIFICATION
The span changes or narrows an editor-level identification of a place, person, source, or referent.

### ACCRETES_INTERPRETATION
The span adds a later interpretive projection not required to report the base observation itself.

### LINKS_PRIOR
The span explicitly targets, cites, corrects, answers, or otherwise binds itself to an earlier note or claim.

### DIGITAL_ASSEMBLES
A digital object places historically distinct layers into one composite object. This label alone does not imply epistemic loss.

## Representation status

For every required relation, code one of:

- `explicit`: directly represented as structure or unambiguous source marking.
- `recoverable`: not explicit as a typed relation but recoverable from retained cues without external source supplementation.
- `unresolved`: retained cues permit multiple materially different relation assignments.
- `unavailable`: the representation lacks the information required to recover the relation.

A higher reconstruction cost is **not** by itself `unavailable`.

## Claim binding

Code:

- `direct`: the span clearly bears on the frozen claim/referent.
- `indirect`: it bears on a premise or prior relation needed by the claim.
- `unresolved`: the target of the span is ambiguous.

## Attribution

Code the actor/source only when the representation supplies a basis. Distinguish narrator/travel account, editor, cited scholar, textual witness, and digital assembler.

## Derived mechanisms

These are computed after primitive coding.

### Rehabilitation
A later source-grounded edge defeats or substantially weakens an earlier challenge to a claim while the base assertion remains available.

### Authority qualification
A later edge weakens the authority under which a claim may be used (for example eyewitness status) without necessarily negating the reported content.

### Interpretive accretion
An editorial layer adds an interpretation at a broader historical or geopolitical scale than the base observation itself requires.

## Disagreement policy

Two coders disagree when they assign different primitive labels, different claim bindings, or different representation status to the same span.

Do not resolve disagreement by consulting the provisional downstream decision. Record the disagreement and adjudicate from the source witness.

## Scientific-object failure signals

The ontology must be revised rather than rescued if:

1. relation labels cannot be applied reproducibly even after source context is fixed;
2. a purportedly orthogonal intervention changes relations outside its declared coordinate;
3. matched controls depend on the removed relation after closer source inspection;
4. a claimed loss is only increased reconstruction cost;
5. downstream claim changes cannot be connected to a frozen dependency edge.
