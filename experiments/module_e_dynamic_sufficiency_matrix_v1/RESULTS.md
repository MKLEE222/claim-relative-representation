# Module E results — distributed information obligations for warranted selective revision

Date: 2026-09-28  
Status: EXECUTED CONTROLLED CHANNEL-ABLATION STUDY AROUND TWO ALREADY-OBSERVED NATURAL WHITMAN REVISION EVENTS. NOT INDEPENDENT TRANSFER.

Authoritative execution:
- GitHub Actions run: 36379931025
- artifact: module-e-dynamic-sufficiency-matrix-v1
- artifact ID: 10952880045
- artifact ZIP SHA-256: c5051d6464458d6e0ef50c4da47c9c3005e7e0317f06bc17daa154b057a67b27
- results SHA-256: edf96f71b32edb20418e24a05d9f5156d51ca1bd304c41325f06eaf0f20647bf

## 1. Question

Modules D1/D2 established two real editorial revision events but also showed that identity-rich event packets can compensate for bindings omitted from the retained state.

Module E holds the natural parent and child states fixed and projects only the available information interface:

    retained state
    x revision-event channel
    x child-source access

The study asks two distinct questions:

1. **terminal-state determinacy**  
   Is the exact child endpoint+certainty state uniquely determined?

2. **transition auditability**  
   Is the exact parent->child selective revision uniquely determined?

These are deliberately separated because a system can know the revised object without knowing exactly what changed.

## 2. Natural events

### D1

Parent:
7cdf5ddc9d0cfff83289f687613ee3d0510e6520

Child:
fe63fcfbeca16f85583a29355c2d3a44e09b280f

Natural delta:
- 1 certainty revision
- 0 add
- 0 remove
- 1,435 unchanged relation identities
- 1 affected printed locus

### D2

Parent:
fe63fcfbeca16f85583a29355c2d3a44e09b280f

Child:
8c6aba338bd3b8a52ec74d014ec1afc8137cc4a9

Natural delta:
- 141 certainty revisions
- 7 additions
- 8 removals
- 1,287 unchanged relation identities
- 113 affected printed loci

The source parsers independently reproduced the authoritative D1/D2 delta counts before the matrix was evaluated.

## 3. Matrix

For each natural event:

    3 retained-state arms
  x 3 event-channel arms
  x 2 access arms
  = 18 cells

Total:
36 cells.

State arms:
- S_FULL: full endpoint -> certainty parent binding
- S_LOCUS_COUNTS: endpoints + high/low counts per locus
- S_ENDPOINTS: endpoints only

Event channels:
- E_LINK_FULL: exact identity + old/new state
- E_LINK_NEW: exact identity + new state, no old certainty
- E_LOCUS_OPERATION_BAG: operation multiset by locus, no operation -> relation binding

Access:
- A_NONE
- A_CHILD_REOPEN

All state arms preserve the current parent endpoint task Q0.

## 4. D1: one natural high -> low revision

Without child-source reopening:

| parent state | event channel | affected child exact | transition exact | global child exact | complete warranted update |
|---|---|---:|---:|---|---|
| S_FULL | E_LINK_FULL | 1/1 | 1/1 | yes | yes |
| S_FULL | E_LINK_NEW | 1/1 | 1/1 | yes | yes |
| S_FULL | E_LOCUS_OPERATION_BAG | 0/1 | 0/1 | no | no |
| S_LOCUS_COUNTS | E_LINK_FULL | 1/1 | 1/1 | no | no |
| S_LOCUS_COUNTS | E_LINK_NEW | 1/1 | 1/1 | no | no |
| S_LOCUS_COUNTS | E_LOCUS_OPERATION_BAG | 0/1 | 0/1 | no | no |
| S_ENDPOINTS | E_LINK_FULL | 0/1 | 1/1 | no | no |
| S_ENDPOINTS | E_LINK_NEW | 0/1 | 1/1 | no | no |
| S_ENDPOINTS | E_LOCUS_OPERATION_BAG | 0/1 | 0/1 | no | no |

The key D1 separation occurs even with the full parent relation state known.

Natural D1 says:
- exactly one high -> low revision occurs at locus pr323;
- the locus has two candidate relations.

If the event channel preserves the changed relation identity, the update is exact.

If the event channel retains only:

    one high -> low operation at pr323

there are exactly two admissible child states and two admissible transition histories.

Thus:

    full parent state
    + correct operation type/count
    !=
    identity of the revised relation

This is an event-channel binding obligation, not a pre-state binding failure.

## 5. D2: broad certainty + topology revision

Without child-source reopening:

| parent state | event channel | affected child exact | transition exact | global child exact | complete warranted update |
|---|---|---:|---:|---|---|
| S_FULL | E_LINK_FULL | 113/113 | 113/113 | yes | yes |
| S_FULL | E_LINK_NEW | 113/113 | 113/113 | yes | yes |
| S_FULL | E_LOCUS_OPERATION_BAG | 78/113 | 78/113 | no | no |
| S_LOCUS_COUNTS | E_LINK_FULL | 113/113 | 113/113 | no | no |
| S_LOCUS_COUNTS | E_LINK_NEW | 113/113 | 113/113 | no | no |
| S_LOCUS_COUNTS | E_LOCUS_OPERATION_BAG | 78/113 | 78/113 | no | no |
| S_ENDPOINTS | E_LINK_FULL | 77/113 | 113/113 | no | no |
| S_ENDPOINTS | E_LINK_NEW | 77/113 | 105/113 | no | no |
| S_ENDPOINTS | E_LOCUS_OPERATION_BAG | 77/113 | 78/113 | no | no |

The strongest primary result is:

    S_FULL + E_LINK_FULL + A_NONE
    = 113/113 child exact, 113/113 transition exact

versus:

    S_FULL + E_LOCUS_OPERATION_BAG + A_NONE
    = 78/113 child exact, 78/113 transition exact

The retained state is identical in this comparison.
The natural revision target is identical.
The only difference is whether revision operations remain bound to relation identities.

Therefore 35/113 affected loci are non-determining after event-binding removal.

## 6. The 35 D2 ambiguous loci are not a topology artifact

Among those 35 ambiguous loci:

- certainty-only revision loci: 30
- topology-only loci: 3
- certainty + topology loci: 2

Thus the separation is predominantly driven by epistemic-status assignment, not by relation insertion/deletion.

Examples under S_FULL + E_LOCUS_OPERATION_BAG + A_NONE:

- one-operation loci can already have 2-4 admissible revisions;
- l1585: 10 admissible child/transition states;
- l1725: 15;
- l1775: 120;
- l1780: 1,287.

At l1780 the exact parent endpoint-certainty state is known and the event bag correctly reports eight low -> high revisions, but it does not state which eight relations changed.

That alone yields:

    1,287

distinct compatible child states and transition histories.

This is a direct finite separation between:

    knowing how many epistemic revisions occurred

and:

    knowing which scholarly relations were revised.

## 7. Exact transition does not imply exact child state

D2 exposes the reverse dependency as well.

Under:

    S_ENDPOINTS + E_LINK_FULL + A_NONE

the natural delta identity and old/new values are known exactly.

Therefore:

    transition exact = 113/113

But:

    child state exact = 77/113

because unchanged relations inside affected loci still carry parent certainty values that S_ENDPOINTS never retained.

So:

    exact revision packet
    !=
    complete revised epistemic state

when the unchanged background state is not otherwise recoverable.

The event channel can supply the delta without supplying all persistent background epistemic information.

## 8. Exact child state does not imply exact transition history

The opposite separation also occurs.

Under D2:

    S_ENDPOINTS
    + E_LINK_NEW
    + A_CHILD_REOPEN

the exact child source is reopened.

Result:

    child state exact = 113/113
    global child state exact = yes

But:

    transition exact = 105/113

The eight ambiguous loci are:

- l1424
- l1782
- l2089
- l2090
- l2130
- l2133
- l2276
- rev02

These correspond to the eight natural relation removals.

Why?

E_LINK_NEW preserves the identity of a removed relation but deliberately omits its old certainty.
S_ENDPOINTS also omitted parent certainty.
The child source cannot recover that old certainty because the relation no longer exists in the child object.

Therefore:

    exact child object
    + exact removed identity
    !=
    exact epistemic history of the removed relation

without either:
- retained parent status,
- an event channel carrying old status,
- or lawful access to the parent source.

This is the clearest Module E witness that:

    terminal-state recoverability
    !=
    transition auditability.

## 9. Child-source reopening as a substitutable information path

A_CHILD_REOPEN supplies the exact child object.

For D2 it repairs every child-state failure in the matrix:

    affected child exact = 113/113

for all nine state x event combinations.

It also resolves the operation-bag ambiguity when combined with the natural operation counts.

For example:

    S_ENDPOINTS
    + E_LOCUS_OPERATION_BAG
    + A_CHILD_REOPEN

reaches:
- child exact: 113/113
- transition exact: 113/113
- global child exact: yes
- unaffected stability audit: yes
- complete warranted update: yes

where the same state/event pair without source reopening is non-determining.

This does not make source reopening universally sufficient: the E_LINK_NEW removal case above shows that a child-only source can still fail to recover old transition status.

## 10. Current-task sufficiency is not dynamic sufficiency

S_ENDPOINTS is sufficient for the parent current endpoint task by construction.

Yet without child reopening:

D2 + E_LINK_FULL:
- transition exact: 113/113
- child exact: only 77/113
- global child exact: no

D2 + E_LINK_NEW:
- transition exact: 105/113
- child exact: 77/113

D2 + E_LOCUS_OPERATION_BAG:
- transition exact: 78/113
- child exact: 77/113

Therefore preserving the current endpoint answer does not determine the later epistemic state or revision history.

The missing obligation can be supplied by other interface components, but it must be supplied somewhere.

## 11. Global background state matters separately from event-local revision

S_LOCUS_COUNTS + identity-rich event channels is event-locally exact:

D2:
- affected child exact: 113/113
- affected transition exact: 113/113

But without source reopening:

    global child exact = no
    unaffected-stability audit exact = no

because some unchanged loci already contain endpoint-specific epistemic ambiguity under S_LOCUS_COUNTS.

This separates two tasks:

    updating the naturally affected region correctly

from:

    maintaining a completely auditable global epistemic state.

An event-local success must not be promoted to global dynamic sufficiency.

## 12. Information sizes

Canonical implementation payloads:

### D1

Retained state:
- S_FULL: 99,111 bytes
- S_LOCUS_COUNTS: 102,518 bytes
- S_ENDPOINTS: 65,206 bytes

Event channel:
- E_LINK_FULL: 124 bytes
- E_LINK_NEW: 111 bytes
- E_LOCUS_OPERATION_BAG: 110 bytes

Child source:
- 121,563 bytes

### D2

Retained state:
- S_FULL: 99,110 bytes
- S_LOCUS_COUNTS: 102,514 bytes
- S_ENDPOINTS: 65,206 bytes

Event channel:
- E_LINK_FULL: 16,500 bytes
- E_LINK_NEW: 14,712 bytes
- E_LOCUS_OPERATION_BAG: 12,282 bytes

Child source:
- 121,447 bytes

These byte counts are descriptive JSON/source encodings only.
S_LOCUS_COUNTS being larger than S_FULL under this verbose serialization is not interpreted as an information-theoretic result.

## 13. Scientific dispositions

EVENT_CHANNEL_BINDING_SEPARATION = YES

REOPEN_CHILD_NOT_TRANSITION = YES

CURRENT_TASK_NOT_DYNAMIC_SUFFICIENCY = YES

DISTRIBUTED_SUFFICIENCY_OBSERVED = YES

All four were preregistered as possible outcomes before matrix execution.

## 14. Revised dynamic sufficiency claim

The experiment supports a distributed determinacy view.

For task T at revision step t -> t+1, define the available information interface:

    I_t = (S_t, E_{t->t+1}, A)

where:
- S_t is retained research state;
- E is the incoming revision/evidence channel;
- A is lawful source access.

A bounded dynamic sufficiency condition is:

    I_t(h1) = I_t(h2)
    =>
    W_T(h1) = W_T(h2)

over the declared admissible history class.

Module E shows that no one component should be treated as the sole carrier by default.

The same task-relevant distinction can sometimes be supplied by:
- retained parent binding;
- identity-bound incoming evidence;
- lawful source reopening;
- or a composition of these.

Conversely, the same amount of information in aggregate form can fail when its binding to relation identity is removed.

## 15. Claim ceiling

Supported:

> For two real Whitman editorial revisions, exact selective update and exact revision audit depend jointly on retained state, event-channel structure, and lawful source access. Identity-bound event evidence can substitute for some omitted pre-state binding; aggregate operation notices can be non-determining even when operation counts and directions are correct. Exact child-source recovery is distinct from exact transition-history recovery.

Not supported:
- a universal minimal dynamic representation;
- that Git commits are the canonical scholarly event channel;
- that all future revision tasks have the same information allocation;
- that child editorial states are historically truer;
- independent cross-domain transfer;
- general human behavior.

## 16. Next obligation

Do not add more Whitman channel arms to improve this matrix.

The next high-value test is cross-domain transfer of the **interaction-level** claim:

    current state
    + incoming correction/revision
    + source access
    -> warranted selective update

The already-source-verified Urumtsi erratum is a candidate historical pressure test because it supplies a different event type:

    explicit textual/factual correction

rather than digital-edition certainty revision.

That transfer must be separately frozen and must preserve the current Yule-Cordier claim ceiling.
