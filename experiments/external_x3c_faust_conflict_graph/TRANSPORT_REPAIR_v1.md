# Faust X3C Transport Repair v1

Date: 2026-09-27
Status: TRANSPORT-ONLY REPAIR BEFORE GRAPH OUTCOME

## Original frozen study

X3C was frozen on 2026-09-24 to audit the Digital Faust Edition's own published Macrogenesis base graph.

Its scientific tasks and metrics remain unchanged:
- count published ignore=true edges;
- count published delete=true edges;
- preserve source/weight exposure counts;
- test directed-cycle status of all edges;
- test directed-cycle status after removing ignore/delete edges.

The original run stopped before graph outcome because the downloads HTML did not expose a GEXF href to the non-browser client.

## New source-side transport evidence

The upstream Digital Faust `faust-macrogen` report generator writes:

`base.gexf`

into the Macrogenesis report/download target and links it as:

`<a href='base.gexf'>GEXF</a>`

The official downloads documentation currently identifies the downloadable base graph and documents edge attributes including `ignore`, `delete`, `source`, and `weight`.

Therefore the transport repair is uniquely determined from the original official page location:

downloads page:
`https://www.faustedition.net/macrogenesis/downloads`

official relative href:
`base.gexf`

resolved graph URL:
`https://www.faustedition.net/macrogenesis/base.gexf`

## Repair boundary

Only source retrieval is changed.

Unchanged from the frozen X3C contract:
- graph identity: published base graph;
- edge-status semantics;
- metrics;
- active-edge rule;
- cycle tests;
- claim ceiling.

No alternative graph URL may be tried after graph outcome.
If the resolved official URL is unavailable, status remains BLOCKED_TRANSPORT.
