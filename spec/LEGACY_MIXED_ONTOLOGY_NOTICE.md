# Legacy mixed-ontology notice

Date: 2026-09-25

The following files are preserved as historical development artifacts and MUST NOT define new scientific experiments:

- spec/task_contracts_v2.csv
- spec/transformation_task_factorial_v2.csv
- spec/TRANSFORMATION_TAXONOMY.md
- spec/transformation_invariants_v1.csv
- spec/interventions.csv
- spec/claim_dependencies.csv
- representation/baseline_fixture_v1.json
- validation/interaction_ops.py
- coding/CODING_MANUAL.md
- coding/author_ledger_projection_v1.csv

Reason:

They mix source-verifiable documentary relations (G_D) with analyst-adjudicated epistemic relations (G_E), including fields such as evidence_relation, SUPPORTS, CHALLENGES, QUALIFIES_AUTHORITY, and ACCRETES_INTERPRETATION.

They remain valid only as provenance for how the design evolved.

All new work uses:

- spec/documentary_relation_ontology_v1.csv
- spec/epistemic_adjudication_ontology_v1.csv
- spec/task_contracts_v3.csv
- spec/TRANSFORMATION_TAXONOMY_v2.md
