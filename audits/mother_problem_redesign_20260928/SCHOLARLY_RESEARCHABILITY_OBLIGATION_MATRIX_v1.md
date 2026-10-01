# Scholarly researchability obligation identification matrix v1

Date frozen: 2026-09-29
Status: PRE-NEW-RESULT IDENTIFICATION CHARTER.

## 1. Purpose

The project must not treat a richer representation as valuable merely because it contains more
fields. The scientific target is to identify information distinctions required by declared
scholarly actions.

For an obligation O_i, evidence is strongest when an intervention preserves the other relevant
information while removing or scrambling O_i and produces a specific predicted failure.

The matrix therefore distinguishes:

    information amount
    from
    information distinction required for warranted scholarly action.

## 2. Obligation set

### O1 ObjectIdentity

Question:
Which scholarly object is the claim/evidence/event about?

Operational requirement:
A claim or event must be bound to one admissible scholarly object boundary.

Predicted failure when absent:
cross-object composition, aggregate-object false positives, or inability to authorize an update.

Existing evidence:
- Module H invalidation by annex/object contamination;
- Module I StaBi false positives under aggregate files;
- Module J/K/L object-boundary controls and null applicability;
- F10-F30 object-scope controls.

Primary DH action:
identify the edition/document/letter whose knowledge state is being reconstructed.

### O2 ClaimApplicability

Question:
Does this evidence or temporal carrier lawfully apply to the selected scholarly object/claim?

Operational requirement:
Each active claim carries a proof class such as FILE_LEVEL_UNIQUE_OBJECT or
INSIDE_SELECTED_OBJECT_BOUNDARY.

Predicted failure when absent:
outside-boundary, annex, embedded-object or foreign-source evidence can change the warrant.

Existing evidence:
- Module L portable applicability proofs;
- outside-boundary / annex / embedded exclusions;
- source/object/claim/boundary mismatch controls.

Primary DH action:
determine whether a cited fact is evidence for this scholarly object rather than merely present
in the same file/container.

### O3 TargetDeterminacy

Question:
Which proposition or scholarly assertion is being criticized, corrected, attributed or supported?

Operational requirement:
The representation preserves the relation from stance/evidence/action to the target proposition.

Predicted failure when absent:
same visible items permit different required scholarly answers.

Existing evidence:
- E1 controlled stance -> target proposition;
- E1 evidence -> proposition;
- E1 responsibility/transmission/adoption witnesses.

Primary DH action:
identify what exactly a correction, criticism, attribution or evidence item is about.

### O4 ResultDeterminacy

Question:
Given the admissible target/evidence set, is the warranted result represented with enough
resolution to preserve exact, interval, alternative or unresolved status?

Operational requirement:
Do not collapse uncertainty or competing alternatives into an unjustified single value.

Predicted failure when absent:
false resolution, lost alternative interpretations, or incorrect downstream action.

Existing evidence:
- Module I/J/L EXACT / INTERVAL / OPEN_INTERVAL / ALTERNATIVE_SET distinctions;
- I_NO_ALTERNATIVES ablation;
- natural source interval/alternative-set cases.

Primary DH action:
preserve qualified or unresolved scholarly positions rather than manufacturing certainty.

### O5 Selectivity

Question:
When new evidence arrives, which parts of the knowledge state are licensed to change?

Operational requirement:
The transition modifies only claims/warrant components targeted by the admitted evidence event.

Predicted failure when absent:
collateral revision of unrelated claims/history.

Existing evidence:
- selective-update checks in Modules I/J/L;
- collateral mutation fault injection;
- null-event stability controls.

Primary DH action:
revise one scholarly judgment without silently rewriting unrelated historical knowledge.

### O6 ProvenancePreservation

Question:
Can the scholar recover the source/evidence/responsibility basis for the present judgment?

Operational requirement:
Active evidence retains source repository/version/file/locator and evidence handle binding.

Predicted failure when absent:
current answer may remain available but cannot be warranted or independently audited.

Existing evidence:
- E1/E4 source-grounded cases;
- Module I/J/L origin/evidence handle and source-context controls;
- F20+ source binding controls.

Primary DH action:
explain what source or editorial evidence licenses a scholarly conclusion.

### O7 TransitionCompatibility

Question:
Is a proposed evidence/update event compatible with the current object, claim and source state?

Operational requirement:
Before mutation, validate target object, boundary, applicability, source context, claim key and
evidence handle.

Predicted failure when absent:
a foreign/stale/wrongly bound event can mutate the current scholarly state.

Existing evidence:
- wrong-origin/wrong-binding/source-context/boundary-context fault controls;
- Module L pre-mutation origin binding.

Primary DH action:
decide whether a newly encountered correction/evidence item can legitimately revise this state.

### O8 HistoryRetention(T)

Question:
After the current state is known, can a later scholar reconstruct the transitions by which it
became warranted?

Operational requirement:
Retain the task-relevant event/evidence/transition history, not only the terminal state.

Predicted failure when absent:
current answer remains recoverable while the history of scholarly change is not determined.

Existing evidence:
- I_NO_HISTORY ablation;
- delayed audit;
- Module M CURRENT_REOPEN / ORDERED_SNAPSHOTS study to provide non-strawman positive
  comparators and indistinguishability witnesses.

Primary DH action:
reconstruct the history of correction, reattribution, evidential revision or editorial judgment.

## 3. Identification standard

For each obligation, classify evidence as one of:

- MECHANISM_IDENTIFIED:
  controlled intervention isolates a predicted failure while relevant alternatives are held fixed.

- NATURAL_SUPPORT:
  a natural/source-grounded case exhibits the distinction without experimental deletion.

- PROSPECTIVE_SUPPORT:
  a pre-frozen unexposed eligible population/event supports the predicted behavior.

- APPLICABILITY_NULL:
  the frozen population does not contain eligible objects/events for the obligation test.

- INVALID:
  evidence is contaminated by a known protocol/object error.

No obligation is called generally necessary solely from exposed development evidence.

## 4. Non-substitutability test

A core contribution requires more than showing that each field can be deleted.

For obligations O_i and O_j, evidence of non-substitutability requires at least one task where:

    preserve(O_j) + remove(O_i)
    -> predicted failure_i

while the capability associated with O_j remains intact.

Priority pairs:

1. ObjectIdentity vs ClaimApplicability
2. ClaimApplicability vs ProvenancePreservation
3. ResultDeterminacy vs HistoryRetention
4. CurrentState/ResultDeterminacy vs HistoryRetention
5. ProvenancePreservation vs TransitionCompatibility
6. Selectivity vs HistoryRetention

Module M is the primary test for pair 4.

## 5. Cross-layer synthesis

Static/access evidence primarily identifies:
- O3 TargetDeterminacy;
- O6 ProvenancePreservation;
- carrier exposure / discoverability preconditions.

Dynamic evidence primarily identifies:
- O1 ObjectIdentity;
- O2 ClaimApplicability;
- O4 ResultDeterminacy;
- O5 Selectivity;
- O7 TransitionCompatibility;
- O8 HistoryRetention.

The paper-level synthesis is not that every task requires every obligation.
The licensed theoretical form is task-relative:

    Researchability(R, tau, S, K, pi; B)

requires the subset of distinctions that make the declared scholarly action determinate,
warranted and auditable under that task/source/workflow contract.

## 6. Remaining evidence gaps

Before the dynamic contribution is considered empirically closed:

G1. Module M must establish a genuine positive current-state/snapshot comparator.

G2. At least one fresh independent eligible dynamic population must be opened under a
pre-frozen contract.

G3. At least one non-temporal humanities event family must test whether the same obligation
logic transfers beyond dating.

G4. If historical Yule-Cordier readings remain load-bearing, independent human scholarly
adjudication should replace the failed model-consensus attempt as the strongest corroboration.

Whole-object prevalence is not required unless a frequency claim is introduced.

## 7. Stop condition

Stop adding engineering controls merely because additional TEI edge cases can be imagined.

A new experiment enters the core program only if it:
- distinguishes two live scientific explanations;
- fills G1-G4;
- or provides a predeclared non-substitutability test in this matrix.
