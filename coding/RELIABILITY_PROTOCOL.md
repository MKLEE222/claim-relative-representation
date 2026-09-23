# Independent relation-coding reliability protocol v1

## Goal

Test whether CEDL primitive relations are recoverable from source-facing evidence without access to provisional downstream decisions.

## Inputs

- `coding/blind_packet_v1.csv`
- `coding/CODING_MANUAL.md`
- `coding/independent_coder_template.csv`

The second coder must not inspect:

- `provisional_decision`
- `author_claim_hypothesis`
- `relation_to_claim`
- `coding/author_ledger_projection_v1.csv`

## Coding unit

One row per frozen event. Multiple primitive labels are allowed when each is independently justified.

## Required fields

- primitive relation labels
- claim binding
- attribution actor/status
- temporal relation
- representation status
- uncertainty note
- coder identifier
- declaration that provisional decisions were not consulted

## Primary reliability statistics

1. exact primitive-label-set agreement
2. mean Jaccard agreement over primitive-label sets
3. exact claim-binding agreement
4. exact representation-status agreement
5. per-label positive agreement counts
6. disagreement ledger by event

No single scalar is treated as sufficient. A high aggregate score does not rescue a systematic disagreement on a load-bearing relation type.

## Predeclared interpretation

- **PASS_CLEAN**: no load-bearing label has unresolved systematic disagreement, and exact/Jaccard results show the ontology is reproducibly usable on this carrier.
- **PASS_WITH_REFINEMENT**: disagreements are localized to a definitional boundary that can be revised without seeing intervention outcomes; the revised manual is re-frozen and both coders recode affected rows.
- **FAIL_ONTOLOGY**: disagreements show that the proposed primitive distinction is not stably recoverable from the source evidence.
- **BLOCKED**: the second coding pass is absent, contaminated by answer leakage, or lacks source access needed by the manual.

Thresholds will not be chosen post hoc to rescue the ontology. The event-level disagreement pattern is the primary scientific diagnostic.
