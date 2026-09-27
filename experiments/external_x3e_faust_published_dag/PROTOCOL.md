# External Validation X3E — Digital Faust Published DAG Stage

Date frozen: 2026-09-27
Status: PRE-OUTCOME ECOLOGICAL PIPELINE-STAGE AUDIT

## Motivation

X3C successfully opened the published `base.gexf` and established native `ignore` / `delete` relation status, but the graph obtained by simply filtering those two flags remained cyclic.

The upstream Digital Faust implementation clarifies that this filtered-base approximation is not the actual final chronology object.

Its documented analysis pipeline is:

[
base ightarrow working ightarrow MFES ightarrow dag
]

The source code states:

1. clean the base graph into `working`;
2. calculate the minimum feedback edge set;
3. remove those edges to construct `dag`;
4. double-check that `dag` is acyclic;
5. optionally re-add removed edges only when doing so preserves acyclicity;
6. use the resulting DAG for downstream topological ordering.

The report generator writes:

`write_dot(graphs.dag, target / 'dag-graph.dot')`

and labels its HTML view as the effective overall graph without conflicts.

## External object

The report target that exposes the already-verified official `base.gexf` is:

`https://www.faustedition.net/macrogenesis/`

The upstream report generator fixes the DAG filename before this study:

`dag-graph.dot`

Therefore the one predeclared URL is:

`https://www.faustedition.net/macrogenesis/dag-graph.dot`

No alternate DAG filename may be tried after outcome.

## Question

Does the separately published DAG-stage object instantiate an acyclic relation set, as distinct from the cyclic published base graph?

## Metrics

If transport succeeds:

- URL and final URL;
- SHA-256;
- byte length;
- directed edge statements parsed from DOT;
- distinct node identifiers appearing on directed edges;
- directed cycle status;
- duplicate directed-pair count.

The base-graph result from X3C is retained independently:

- base nodes: 1127;
- base edges: 3409;
- base cyclic: yes;
- active-by-ignore/delete-filter subset cyclic: yes.

X3E does not redefine those results.

## Success / null discipline

Strong external stage-separation pattern:

[
BASE_CYCLIC = 1
]

and

[
PUBLISHED_DAG_CYCLIC = 0.
]

If the DOT is unavailable, mark BLOCKED_TRANSPORT.

If the object is available but cyclic, retain that result and do not search for another DAG representation.

## Claim ceiling

A positive result can support:

> the external infrastructure publishes different graph stages for relation assertion/conflict state and for downstream acyclic chronology.

It cannot support:

- a unique historically true chronology;
- correctness of each removed edge;
- equivalence between Faust conflict state and Yule-Cordier proposition binding;
- a claim that `ignore/delete` alone performs the complete transition.
