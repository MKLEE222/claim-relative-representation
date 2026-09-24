# External Validation X3D - Faust raw source-qualified conflict ecology

Date frozen: 2026-09-24
Status: PRE-OUTCOME RAW ASSERTION AUDIT

## Motivation

X3C was transport-blocked before the published GEXF graph could be inspected.

X3D asks a narrower question using the pinned public source XML only:

> Do the source-qualified raw temporal assertions themselves contain directed incompatibilities/cycles before Macrogenesis conflict resolution?

This does not reproduce the project's feedback-edge-set solution.

## External source

Repository:
faustedition/faust-xml

Pinned commit:
502eca65120dd6189ceaf41d4e5017775e6e4677

Input universe:
all XML files under xml/macrogenesis/ in the pinned repository tarball.

## Relation scope

Only relation elements with:

\[
name = temp-pre
\]

and at least two item elements are included.

For a relation with ordered items:

\[
(i_1,i_2,\ldots,i_k)
\]

the audit emits adjacent directed constraints:

\[
i_1\rightarrow i_2,\ i_2\rightarrow i_3,\ldots,i_{k-1}\rightarrow i_k.
\]

Each emitted edge retains:
- source URI;
- source locator text;
- source XML file.

## Conflict measures

The raw graph is summarized by:

- source XML file count;
- temp-pre relation count;
- emitted directed edge count;
- distinct nodes;
- distinct source URIs;
- direct reciprocal edge pairs;
- strongly connected components (SCCs) with more than one node;
- nodes and internal edges participating in nontrivial SCCs.

## Interpretation

A nontrivial SCC is evidence that the raw assertion graph cannot be represented as one acyclic precedence order without discarding/reinterpreting at least one constraint in that SCC.

It is **not** evidence that any particular source is historically wrong.

## Relation to the external project's semantics

The Digital Faust Edition documents that contradictory assertions are handled to produce an acyclic graph.

X3D tests the raw-data side of that workflow.

It does not claim to reproduce:
- ignore flags;
- delete flags;
- edge weights;
- the exact minimum feedback edge set;
- the published final ordering.

## Outcome discipline

If the raw graph is acyclic, report that result.

No additional relation type may be added post hoc to create cycles.
