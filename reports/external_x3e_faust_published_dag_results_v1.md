# Faust X3E Published DAG Stage Results v1

Date: 2026-09-27
Status: EXECUTED ECOLOGICAL PIPELINE-STAGE RESULT
Protocol frozen before outcome: 2026-09-27
Primary transport run: GitHub Actions 36311783515
Parser-only repair run: GitHub Actions 36311836554

## External object

Official Digital Faust Macrogenesis DAG report object:

`https://www.faustedition.net/macrogenesis/dag-graph.dot`

SHA-256:

`a76c25331da9408560682c835de8cf5f02ee2773a6f3595fa086aee1fa2c849b`

Bytes:

`443462`

The filename was fixed by the upstream `faust-macrogen` report generator before outcome inspection:

`write_dot(graphs.dag, target / 'dag-graph.dot')`.

## Parser provenance

The first X3E run fetched the correct object but returned PARSE_FAILURE because the local regex required a word boundary after a quoted Graphviz node identifier.

The repair changed only the DOT lexical parser:
- URL unchanged;
- source SHA unchanged;
- metrics unchanged;
- cycle algorithm unchanged;
- no alternate object searched.

The frozen DOT contains:
- raw `->` operator occurrences: 2942;
- raw `--` occurrences: 0.

## Published DAG result

- directed edge statements: 2942
- unique directed node pairs: 2409
- duplicate directed-pair statements: 533
- nodes participating in directed edges: 1114

Cycle test:

[
PUBLISHED_DAG_CYCLE = 0
]

Thus the separately published DAG-stage object is acyclic.

## Relation to X3C

X3C opened the official published `base.gexf`:

- nodes: 1127
- edges: 3409
- ignore=true: 209
- delete=true: 168
- active-by-simple-flag-filter edges: 3032
- full base graph cyclic: yes
- simple ignore/delete-filtered base graph cyclic: yes

X3E now establishes:

[
BASE_CYCLIC = 1
]

[
SIMPLE_FILTERED_BASE_CYCLIC = 1
]

[
PUBLISHED_DAG_CYCLIC = 0
]

Therefore:

[
STAGE_SEPARATION_STRONG_PATTERN = 1.
]

## Mechanistic interpretation

The upstream implementation documents distinct stages:

[
base ightarrow working ightarrow MFES ightarrow dag.
]

The empirical results are consistent with that architecture.

Crucially, X3C shows that merely dropping base edges carrying `ignore` / `delete` is not equivalent to the actual published DAG stage: that simple subset remains cyclic.

X3E shows that the separately generated downstream DAG object is acyclic.

Therefore the external infrastructure provides a natural, non-synthetic witness that:

[
relation presence
]

[

eq conflict/status encoding
]

[

eq executable chronology representation.
]

These stages cannot be collapsed without changing what downstream operations are licensed.

## Scientific value for the mother problem

This is the strongest external ecological counterpart currently available to the R3 staged account.

It does not reproduce the Yule-Cordier stance/commitment/evidence-binding mechanism.

Instead, it independently demonstrates the more general principle that a scholarly relation can exist in one representational stage while its status and admissibility for a downstream scholarly operation are represented separately, and that the operational representation is a distinct transformed object.

This supports a task-relative researchability framework without requiring the claim that every real transformation literally deletes proposition bindings.

## Important null retained

The X3C strong pattern failed:

[
BASE_FILTERED_ONLY_ACYCLIC = 0.
]

That null remains scientifically necessary.

The correct conclusion is not:
> ignore/delete flags alone make the base graph executable.

The correct conclusion is:
> the external pipeline has additional representational stages between base assertions/conflict state and the final acyclic DAG.

## Claim ceiling

Supported:
> a real scholarly infrastructure exposes distinct representations for raw/published relation assertions, conflict-handling state, and an acyclic downstream chronology graph; preserving the existence of relations is not equivalent to preserving or determining their operational status in the executable stage.

Not supported:
- the DAG is the unique historically true chronology;
- every removed/reweighted relation is historically wrong;
- Yule-Cordier proposition binding and Faust conflict resolution are identical mechanisms;
- all DH infrastructures require the same stages.

## Outcome

[
STAGE_SEPARATION_STRONG_PATTERN = 1
]

[
UNIQUE_HISTORICAL_ORDER = NOT CLAIMED
]
