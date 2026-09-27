# Faust X3C Published Conflict-State Graph Results v1

Date: 2026-09-27
Status: EXECUTED ECOLOGICAL EXTERNAL GRAPH AUDIT
Original protocol frozen: 2026-09-24
Transport-repair GitHub Actions run: 36311643612

## Source

Official Digital Faust Macrogenesis published base graph:

`https://www.faustedition.net/macrogenesis/base.gexf`

GEXF SHA-256:

`6512f51c627dce9d88649750f421e9d7847deb0d609d80a9bf1fa00966997ed5`

The graph URL was fixed by the upstream report generator's published `base.gexf` output path before any graph outcome was inspected.

## Published graph state

- nodes: 1127
- edges: 3409
- ignore=true: 209
- delete=true: 168
- source present: 2942
- weight present: 3319
- active edges after excluding ignore/delete: 3032

The removed-from-active count is:

[
3409 - 3032 = 377
]

which equals:

[
209 + 168 = 377.
]

Thus in this published graph the counted `ignore` and `delete` states are disjoint at the edge-count level.

## Frozen cycle test

All published edges:

[
ALL_EDGES_CYCLE = 1
]

After excluding every edge with `ignore=true` or `delete=true`:

[
ACTIVE_EDGES_CYCLE = 1
]

Therefore the protocol's strongest predeclared pattern:

[
ALL_CYCLIC land ACTIVE_ACYCLIC
]

is **not observed**.

[
STRONG_PATTERN = 0
]

This null must be retained.

## What the ecological result does establish

The published external representation natively distinguishes:

[
relation presence
]

from

[
relation active status.
]

At least 377 published edges remain represented in the base graph while carrying a native workflow state that excludes them from the project's active-edge subset under the frozen X3C rule.

This is not a researcher-created projection. The `ignore` / `delete` states are attributes of the published Digital Faust graph.

Therefore the external object supplies a natural relation-status witness:

> the existence of a scholarly temporal relation in the published graph does not by itself determine whether that relation is treated as active under the graph's own conflict-handling state.

## What the result does not establish

Because the active-edge graph remains cyclic, X3C does **not** establish that:

- removing `ignore` and `delete` edges alone produces the final executable chronology;
- the published base graph's active subset is a DAG;
- the flagged edges are the only conflict-resolution mechanism used downstream;
- the active subset encodes a unique historical chronology;
- every cycle corresponds to a historical contradiction of the same semantic kind.

The result also does not identify any particular source assertion as historically wrong.

## Relation to X3D

X3D independently established that the pinned raw source-qualified temporal assertion ecology contains cycles and reciprocal constraints.

X3C now closes the previously transport-blocked published-graph side:

- raw assertion conflict ecology exists;
- the published base graph exposes native ignore/delete state;
- relation status changes the active edge set;
- but the active base-graph subset remains cyclic.

The appropriate synthesis is therefore not "conflict metadata turns the graph into a DAG."

It is:

> raw/published relation presence, conflict-handling status, and final executable chronology are distinct representational stages and must not be collapsed.

## Relevance to the mother problem

X3C provides an independent external ecological example of a distinction already central to the R3 framework:

[
availability of a relation 
eq status of that relation for a downstream scholarly operation.
]

It is stronger than a controlled field-deletion analogue because the status is native to an external scholarly infrastructure.

It is not the same mechanism as Yule-Cordier proposition-binding deletion and must not be presented as such.

## Claim ceiling

Supported:
> an external scholarly infrastructure can preserve a relation while separately encoding whether that relation is ignored/deleted for downstream graph use.

Not supported:
> ignore/delete metadata alone resolves the graph into an acyclic or uniquely correct chronology.

## Preservation rule

The original BLOCKED_TRANSPORT record remains part of provenance.
The transport repair changes only source access; it does not rewrite the frozen X3C scientific contract.
