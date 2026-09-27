# R3 Proposition-Binding Separation Protocol v1

Date frozen: 2026-09-27
Status: PRE-EXECUTION controlled separation study.

## Purpose

Test a narrow implication of the mother problem:

If a transformed representation preserves the participating people, propositions, stance/evidence items and visible snippets but removes the bindings among them, are selected scholarly-history questions still uniquely determined?

This does NOT test whether plain linear text is sufficient. The tested projections are deliberately relationally flattened controlled representations.

## Historical anchors

Use only PAGE_VERIFIED_BOTH rows in `data/r3_verified_proposition_panel_v1.csv`.

Primary inquiries:
- Pashai target-specific stance;
- Arbre Sec commitment/adoption;
- Great Desert evidence-to-proposition binding.

Control:
- Urumtsi found -> founded erratum.

## Reference state

The reference state consists of source-audited proposition acts and typed bindings.

## Controlled projections

### P_STANCE_BAG
Retain:
- actor names;
- proposition identifiers and proposition summaries;
- multiset of stance/modality labels.

Remove:
- which stance/modality attaches to which proposition.

Question tested: R3Q-PASH-STANCE.

### P_ROLE_BAG
Retain:
- Cordier, Houtum-Schindler and the cypress proposition;
- the fact that the proposition is present in the inspected 1920 entry;
- the bibliographical reply/citation fact.

Remove:
- proposer/transmitter/adopter commitment-role binding.

Question tested: R3Q-ARBR-COMMIT.

### P_EVIDENCE_BAG
Retain:
- both Great Desert propositions;
- both evidence descriptions;
- actor and mediator identities.

Remove:
- evidence-to-proposition edges.

Question tested: R3Q-DES-EVIDENCE.

### P_TEXT_PAIR control
Retain the earlier token and explicit replacement token for the Urumtsi erratum.

Question tested: R3Q-URM-ERRATUM.

## Separation criterion

A projection is non-determining for inquiry Q when two admissible completions have identical projected visible content but different required Q outputs.

For each primary inquiry, construct the minimum pair of completions needed to test this condition. The alternate completion must change only the removed binding, not the retained entities/items.

## Control criterion

The Urumtsi control should remain determined under P_TEXT_PAIR because the query concerns the explicitly retained substitution itself.

## Interpretation

A positive witness establishes only:
`the removed binding is necessary for determining this inquiry under this projection`.

It does NOT establish:
- that the historical source lost the relation;
- that plain text cannot recover it;
- that real users fail;
- that all digital transformations remove the binding;
- that the controlled alternate completion is historically true.

## Scientific value

The study isolates a proposition-level information obligation discovered by close reading. It moves the project beyond target localization while preserving the distinction between source history and controlled representation analysis.