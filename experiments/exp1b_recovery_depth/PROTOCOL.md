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
