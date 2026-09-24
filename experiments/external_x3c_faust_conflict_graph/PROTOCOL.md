# External Validation X3C - Faust published conflict-state graph audit

Date frozen: 2026-09-24
Status: ECOLOGICAL EXTERNAL GRAPH AUDIT

## Purpose

Test whether the published Macrogenesis graph exposes conflict-handling state that is operationally relevant to chronology construction.

This audit uses the Digital Faust Edition's own downloadable base graph.

## Source discovery

The run must:

1. fetch the official Macrogenesis downloads page;
2. identify the first link whose href ends in .gexf and whose anchor text/URL denotes the base graph;
3. resolve the link against the official site;
4. fetch the GEXF bytes;
5. record URL and SHA-256.

No alternate graph may be selected after inspecting its result.

## Native edge states

The official documentation defines edge attributes including:

- ignore: an edge to be ignored for philological reasons;
- delete: an edge removed by the minimum-feedback-edge-set heuristic;
- source: scholarly source URI;
- weight: generated trust/weight information.

## Tasks

### FA-ACTIVE-ORDER

Recover the temporal graph after respecting the published ignore/delete state.

### FA-CONFLICT-AUDIT

Recover which assertions are ignored/deleted and, where available, their source/provenance.

## Metrics

- total nodes and edges;
- counts of ignore=true edges;
- counts of delete=true edges;
- counts carrying source and weight;
- directed-cycle status of:
  - all edges;
  - active edges after removing ignore/delete edges.

Cycle detection treats the graph as directed and ignores duplicate parallel edges.

## Strong mechanistic pattern

The highest-value pattern is:

- all-edge graph contains a directed cycle;
- active graph does not.

This would show that conflict-state metadata is not merely descriptive annotation: it changes the executable chronology graph.

If both graphs are cyclic or both acyclic, report that result without reinterpretation.

## Boundary

The audit does not claim that the active graph is the unique historical chronology.

It tests only the external project's published conflict-handling representation.
