# Experiment 1B - Recovery depth of claim-evidence relations

**Status: SUPERSEDED_BEFORE_RUN**

Superseded on: 2026-09-24

This protocol was frozen after Experiment 1A but before any recovery-depth coding was executed. It is retained for provenance because the redesign was triggered by a conceptual audit, not by unfavorable Experiment 1B outcomes.

## Why it was superseded

The protocol treated recovery depth as the primary experimental object. Further design review showed that depth is only one coordinate of a larger task-relative recoverability construct.

The replacement design separates:

1. task-independent typed representation transformations;
2. frozen scholarly task contracts;
3. recovery contracts;
4. task-adapted states;
5. recoverability profiles;
6. only later, humanistic claim adjudication.

See:

- `spec/TASK_CONTRACT.md`
- `spec/RECOVERY_CONTRACT.md`
- `spec/TRANSFORMATION_TAXONOMY.md`
- `spec/task_contracts_v1.csv`
- `spec/transformation_task_factorial_v1.csv`

The original protocol follows below unchanged for auditability.

---

# Experiment 1B - Recovery depth of claim-evidence relations

Date frozen: 2026-09-23

## Motivation

Experiment 1A showed that metadata-only ablation often leaves direct lexical cues. The main binary-loss design is therefore rejected.

Experiment 1B measures the **minimum reconstruction depth** needed to recover each frozen claim-relevant relation from a representation.

## Recovery-depth scale

- **D0 - explicit**: the representation contains a typed structured relation or directly queryable field.
- **D1 - local-span recoverable**: the relation is absent structurally but recoverable from the source span itself.
- **D2 - local-context recoverable**: recovery requires the surrounding note, chapter, heading, signature, or immediately adjacent passage.
- **D3 - cross-layer recoverable**: recovery requires traversal to another page, edition layer, addendum, or explicitly linked historical witness within the digital object.
- **D4 - external-witness recoverable**: recovery requires a source outside the representation, such as a printed witness, source registry, or scholarly edition.
- **U - unavailable**: the relation cannot be recovered under the frozen source contract.

`unresolved` is recorded separately when more than one materially different relation assignment remains compatible at the minimum available depth.

## Primary unit

A frozen tuple:

`(claim_id, relation_coordinate, representation_id)`

The coder assigns the minimum depth at which the required relation can be recovered without consulting downstream retain/revise/defer/withhold outcomes.

## Representations

R0: source-grounded structured CEDL representation.

R1: text-preserving projection with explicit CEDL relation fields removed.

R2: local-span projection with note/chapter metadata omitted but substantive span retained.

R3: local corpus chunk that retains only the selected passage plus minimal bibliographic identity.

The experiment does not assume that R3 is always less adequate than R2. Recovery depth is measured claim by claim.

## Hypotheses

H1. R1 will often move load-bearing relations from D0 to D1 rather than to U.

H2. Cross-layer revision claims, especially paper-money rehabilitation, will require greater depth when chronology and link structure are not explicit.

H3. Matched negative-control claims whose dependencies do not intersect the removed coordinate will not show a systematic increase in required depth.

H4. Relation types differ: attribution and claim binding may be text-entangled more often than chronology and cross-layer revision structure.

## Outcome

The primary outcome is change in minimum recovery depth:

`Delta D = D(representation_intervention) - D(R0)`

No single aggregate mean is sufficient. Results are reported by claim family, relation coordinate, and matched control.

## Failure conditions

- coders cannot apply the depth scale reproducibly;
- an R1/R2/R3 transformation changes substantive claim content;
- a supposed depth increase is produced only by an arbitrary truncation with no documented workflow analogue;
- matched controls show comparable depth increases, indicating nonselective degradation.

## Sequencing

1. freeze representation constructors and invariants;
2. complete independent relation coding;
3. blind recovery-depth coding;
4. only then open claim-state adjudication.

