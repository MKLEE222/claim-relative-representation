# Nearest-neighbor audit: uncertainty, ambiguity, and responsibility

Date: 2026-09-27
Status: literature-positioning amendment.

## Existing work

TEI has long provided mechanisms for representing certainty, precision, responsibility, ambiguous readings, unclear source material, and related editorial uncertainty.

Digital-humanities research has explicitly argued that uncertainty cannot simply be eliminated from computational models and that scholarly editions routinely preserve uncertain readings, identifications, and competing interpretations.

Graph-based DH work on uncertainty also emphasizes responsibility information at uncertain points as important for interoperability and intersubjective traceability.

Therefore this project must not claim novelty for modeling uncertainty itself.

## Project-specific gap

The sharper question is preservation fidelity under representation change:

Can a representation preserve the documentary fact that a relation is uncertain, contested, multiply supported, or unresolved, while still supporting the historical task?

This differs from simply assigning a numeric confidence value.

## Existing empirical anchors in this project

Whitman:
link endpoints can be preserved while encoded certainty status is removed.

Faust:
source-qualified temporal assertions can all remain present while the complete assertion set is mutually conflicting and requires a separate resolution policy before one executable chronology is obtained.

Yule-Cordier:
the source itself contains explicit doubt, criticism, competing scholarly voices, qualifications, and corrections of earlier criticism.

## R3 consequence

`UNRESOLVED_RELATION` should not be treated as coding failure or a residual garbage class.

R3 must distinguish at least:
- source explicitly uncertain/contested;
- analyst cannot resolve because evidence is insufficient;
- multiple historical actors advance competing positions;
- representation has lost the marker that distinguished a tentative from a stronger relation.

These states have different humanistic meanings and should not be pooled.

## Candidate contribution

Not 'we preserve uncertainty.'

Rather: the audit can test whether a transformation preserves the source's resolution state and responsibility structure, separately from preserving the linked textual endpoints.