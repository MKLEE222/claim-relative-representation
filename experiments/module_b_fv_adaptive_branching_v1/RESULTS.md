# Module B: Frankenstein source-triggered branching and selective update results v1

Date: 2026-09-28
Status: EXECUTED DEVELOPMENT RESULT ON ALREADY-EXPOSED C18. NOT INDEPENDENT TRANSFER.
Successful run: GitHub Actions 36372745090
Artifact: module-b-fv-adaptive-branching-v1
Artifact ID: 10950085906
Artifact ZIP SHA-256: 34ebf8659939d16e0a535096cbf85b671ec7ac5a4017df7cbf9305cb9cfad6e5
results.json SHA-256: d3dbb77ac98ecd5265b802dd264b28b4e7f5d38a00b876967b5a368499b53d54

## 1. Execution history

The first run (36372539414) stopped before producing any scientific outcome because arbitrary `sga-add` milestone-bounded slices are not guaranteed to be standalone well-formed XML subtrees.

The support repair was frozen in `IMPLEMENTATION_REPAIR_v1.md` before successful execution:
- reference semantics moved to a full-document event traversal;
- `LOCAL_SCOPE_XML` was weakened to `LOCAL_SCOPE_SERIALIZATION`;
- local cancellation negatives are not inferred without inherited context;
- source, population, branch families, current output and controlled `@next` event remained unchanged.

The successful run completed after that repair.

## 2. Population

Pinned source:
- FrankensteinVariorum/collationWorkspace
- commit: 5a208f869ff1213defa000e3181d5315a072a15f
- source: collationChunks/C18/msColl_C18.xml
- Git blob: 8e537331ebf46dd4f013da9afcbe38c14092b6fd
- source SHA-256: fef75b357d9cdb8c261b2922b2ad9881287361ab2fb920454f2b93ef5af63112
- bytes: 47,854

The complete frozen population contains 112 well-formed `sga-add` scopes.

Positive source-native continuation instances:
- B-INCOMING: 2 scopes;
- B-OUTGOING: 2 scopes;
- B-CANCEL: 5 scopes.

Branch-profile distribution:
- no positive registered branch: 103 scopes;
- cancellation only: 5;
- outgoing-next only: 2;
- incoming-next only: 2.

No scope instantiates more than one of the three positive branch families in this C18 population.

## 3. Natural collision result

Natural CURRENT_SUMMARY collision with different full continuation profiles:

**NOT OBSERVED**

Count: 0.

Byte-identical LOCAL_SCOPE_SERIALIZATION with different B-INCOMING outputs:

**NOT OBSERVED**

Count: 0.

Therefore Module B does not supply a new natural same-current-answer/different-continuation collision at the scope-summary level.

This null is retained.

Module A's app-level natural collisions remain separate evidence and are not upgraded by Module B.

## 4. Continuation exposure by retained interface

There are 9 positive branch instances across the 112 scopes.

| Interface | Exact structured branch decisions | UNKNOWN | Informative wrong | Positive branch triggers surfaced |
|---|---:|---:|---:|---:|
| CURRENT_SUMMARY | 0 / 336 | 336 | 0 | 0 / 9 |
| START_ATTRS_PLUS_TEXT | 110 / 336 | 226 | 0 | 2 / 9 |
| LOCAL_SCOPE_SERIALIZATION | 110 / 336 | 226 | 0 | 5 / 9 |
| SOURCE_LINKED | 336 / 336 | 0 | 0 | 9 / 9 |

No interface produced a false positive branch trigger under the frozen trigger rules.

The 110 exact determinations in START_ATTRS_PLUS_TEXT and LOCAL_SCOPE_SERIALIZATION are B-OUTGOING=NONE cases. Positive `@next` literals are visible and can license following the reference, but the registered structured output includes target-resolution status, so those positive cases remain UNKNOWN until source-level resolution.

Payload accounting, canonical encoding:

| Interface | Total bytes across 112 scopes | Median bytes/scope | Max |
|---|---:|---:|---:|
| CURRENT_SUMMARY | 6,619 | 55.5 | 162 |
| START_ATTRS_PLUS_TEXT | 10,231 | 85 | 189 |
| LOCAL_SCOPE_SERIALIZATION | 19,135 | 159 | 996 |
| SOURCE_LINKED locator | 14,532 | 129 | 136 |

SOURCE_LINKED additionally requires the pinned source itself. The cold source object is 47,854 bytes and a batch may reuse one cached source read. These values are descriptive interface costs, not minimum coding bounds.

## 5. Inherited cancellation context

The five B-CANCEL scopes are:

- c57-0018__main__d4e3700: `del` -> “were”
- c57-0019__main__d4e4006: `del` -> “som”
- c57-0020__main__d4e4131: `del` -> “application”
- c57-0020__main__d4e4257: `mdel` -> “or”
- c57-0022__main__d4e4616: `del` -> “white”

Only three of these five expose a local `del` / `mdel` marker inside the milestone-bounded local serialization.

Two are inherited from an enclosing deletion whose opening/closing markup lies outside the `sga-add` scope:

- c57-0018__main__d4e3700 (“were”)
- c57-0019__main__d4e4006 (“som”)

Thus a milestone-bounded local slice can preserve the inserted text and insertion attributes while failing to expose the parent deletion context in which that insertion is encoded.

This is an interface/context observation, not a claim about authorial intention or genetic interpretation.

## 6. Native next relations

Two source-internal `sga-add@next` relations resolve uniquely:

1. c57-0015__main__d4e3192
   -> #c57-0015.05
   -> c57-0015__main__d4e3200

2. c57-0019__main__d4e3991
   -> #c57-0019.06
   -> c57-0019__main__d4e3996

The first source relation links the encoded fragments “hereafter consider” and “it proper to pursue that”.

The second links “experience &” and “feelings” under the source encoding.

These are documentary relations in the pinned source, not claims about independent literary interpretation.

## 7. Controlled selective-update result

For each of the two uniquely resolved internal `@next` relations, a controlled twin removed exactly that one `@next` attribute and changed no text.

Both events produced exactly the predeclared dependency changes:

- source scope B-OUTGOING changed;
- target scope B-INCOMING changed;
- no registered current documentary answer changed;
- B-CANCEL remained unchanged everywhere;
- no other branch coordinate changed.

Result:

`CONTROLLED_SELECTIVE_UPDATE = 2 / 2 PASS`

Each relation also served as the other's disjoint unrelated-event control:

`UNRELATED_EVENT_CONTROL = 2 / 2 PASS`

This is controlled dependency-propagation evidence. The `@next` removals are not naturally observed editorial events.

## 8. Source-linked recovery null

SOURCE_LINKED resolves all 336 branch-family decisions and all 9 positive branch instances.

Therefore:

`NATIVE_OR_ORDINARY_SOURCE_LINKED_BRANCH_FAILURE = NOT OBSERVED`

The experiment does not establish that the Frankenstein infrastructure loses continuation information globally.

Its supported result is interface-relative:

- current documentary output can survive aggressive local reduction;
- positive continuation triggers become progressively less exposed across reduced interfaces;
- ordinary provenance/source reopening recovers them;
- some local continuation state is inherited from enclosing structure rather than contained inside the selected scope.

## 9. Scientific disposition

Supported in development:

[
current documentary answer preservation

otRightarrow
immediate continuation	ext{-}trigger exposure
]

under the declared interfaces.

Also supported:

[
local milestone scope

otRightarrow
self	ext{-}contained documentary context
]

for two observed deletion-wrapped insertions.

Not supported:

- a natural scope-summary same-answer/different-continuation collision;
- autonomous question generation;
- human scholarly discovery;
- selective belief revision under real later evidence;
- failure of the full Frankenstein infrastructure;
- advantage over ordinary provenance/navigation;
- independent transfer;
- long-horizon sustained inquiry.

## 10. Next obligation

Before using a new corpus, audit the actual Frankenstein pipeline stages rather than comparing only constructed reductions.

The next development test should ask whether the nine registered continuation instances survive through:

1. raw manuscript source;
2. preprocessing stage 1;
3. preprocessing stage 2;
4. CollateX partway apparatus;
5. complete published apparatus.

This determines whether continuation-state loss is a property of the real workflow, only of local task-facing projections, or neither.

No favorable result is required.
