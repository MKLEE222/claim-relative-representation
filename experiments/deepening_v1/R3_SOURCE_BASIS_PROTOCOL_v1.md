# R3 source-basis and explicitness protocol v1

Date: 2026-09-27
Status: frozen before full R3-A coding.

## Purpose

Separate the historical relation assigned to an intervention act from the evidential route by which that relation is licensed.

A relation label such as CRITICISM or IDENTIFICATION_UPDATE is not enough. The coding must state whether the source explicitly performs that act or whether the relation emerges only by comparing witnesses/contexts.

## Basis types

### B_EXPLICIT_STANCE
Historical actor explicitly uses evaluative wording such as mistaken, correct, doubtful, untenable, cannot accept, or equivalent language.

### B_EXPLICIT_ATTRIBUTION
The source explicitly identifies who speaks, writes, argues, reports, transmits, or is cited.

### B_EXPLICIT_POINTER
Page, note, chapter, hyperlink, or other source-native pointer explicitly targets a prior locus.

### B_EXPLICIT_IDENTITY
The source explicitly states that two names/forms designate the same or different referent.

### B_EXPLICIT_MODALITY
The source explicitly marks uncertainty, probability, conjecture, doubt, or restricted scope.

### B_PARALLEL_WITNESS_COMPARISON
The relation is obtained by comparing two verified edition/witness states; neither source alone states the update relation in evaluative language.

### B_CONTEXTUAL_DOCUMENTARY_INFERENCE
The relation is source-grounded but requires local documentary inference from heading, sequence, quotation frame, signature, or equivalent context.

### B_EXTERNAL_SCHOLARLY_INFERENCE
The assignment requires case-specific external scholarship beyond the represented object.

Primary R3 representation experiments should not silently use B_EXTERNAL_SCHOLARLY_INFERENCE under an H0 contract.

## Multi-basis rule

An act may have several independent bases.

Example: paper money PM03 has:
- explicit pointer to Bretschneider p.430;
- explicit Laufer attribution;
- explicit correction stance;
- explicit positive endorsement.

These bases must not be collapsed into one generic 'metadata' coordinate.

## Claim-strength rule

Source-explicit claims may be stated as observed editorial acts once source verification is adequate.

Comparison/inference-based relations must be described as reconstructed relations and retain their assumption burden.

Analyst uncertainty is recorded under coding status, not basis type.

## Representation consequence

Carrier-resilience experiments operate on bases, not directly on historical relation labels.

Removing B_EXPLICIT_POINTER while B_EXPLICIT_STANCE and B_EXPLICIT_ATTRIBUTION remain may increase recovery burden without eliminating the intervention act.

True basis exhaustion requires that every lawful basis registered for the task is absent, ambiguous, or outside the contract.

## Humanistic consequence

This protocol preserves a distinction between:
- what historical actors explicitly did in the editorial record;
- what a modern researcher can reconstruct by comparing layers;
- what requires external historiographic interpretation.