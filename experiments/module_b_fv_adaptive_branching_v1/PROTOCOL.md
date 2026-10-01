# Module B: Frankenstein source-triggered branching and selective update v1

Date frozen: 2026-09-28
Status: DEVELOPMENT PROTOCOL ON ALREADY-EXPOSED C18. NOT INDEPENDENT TRANSFER.
Parent: audits/mother_problem_redesign_20260928/AUDIT.md
Predecessor: experiments/module_a_fv_scope_continuation_v1/

## 1. Purpose

Module A established a bounded natural local-interface ambiguity and showed that ordinary pinned-source reopening restores the inherited insertion scope. It also exposed source-native follow-up structure.

Module B asks a different question:

> Once a source-backed documentary scope has been recovered, which next research operations are licensed by the evidence actually present, and can a representation preserve the current documentary answer while changing the ability to recognize or update those continuation obligations?

This is not autonomous natural-language question generation. It isolates the representation-side prerequisite for adaptive inquiry: source evidence must expose a live distinction before a research policy can lawfully branch on it.

The development object is FrankensteinVariorum/collationWorkspace at pinned commit 5a208f869ff1213defa000e3181d5315a072a15f, C18 manuscript source. C18 is already exposed development material and remains development here.

## 2. Episode unit

The unit is every well-formed `sga-add` scope in the pinned C18 manuscript source.

No favorable subset is selected.

For each scope, define the current documentary answer:

- normalized enclosed text;
- encoded `place`, or NOT_ENCODED;
- encoded `hand`, or NOT_ENCODED.

The current answer intentionally does not include `next`, reverse links, or internal deletion markup. Those are continuation-relevant relations rather than the registered current output.

## 3. Frozen continuation grammar

Exactly three source-native continuation families are evaluated.

### B-INCOMING

Question licensed:

> Does another encoded insertion explicitly point into this insertion via `@next`, and which insertion(s)?

Reference output:
the exact set of predecessor `sga-add@sID` values whose `@next` resolves to this scope's `xml:id`.

### B-OUTGOING

Question licensed:

> Does this insertion explicitly point onward through `@next`, and to what encoded target?

Reference output:
the literal `@next` value plus target-resolution status and target `sga-add@sID` when the target resolves uniquely within the frozen source.

### B-CANCEL

Question licensed:

> Does this insertion contain explicitly encoded cancelled text, and what cancellation records are present?

Reference output:
the ordered `del` / `mdel` records inside the scope, including element type and normalized text.

Only explicit source markup licenses these branches. No authorship, intentionality, genetic priority, literary interpretation, or historical truth beyond the encoding is inferred.

No additional branch family may be added after outcomes are opened.

## 4. Representations / interfaces

### CURRENT_SUMMARY

Exposes only the registered current answer.

It cannot make an informative claim about any of B-INCOMING / B-OUTGOING / B-CANCEL. Correct output for those families is UNKNOWN.

### START_ATTRS_PLUS_TEXT

Exposes:
- all attributes on the opening `sga-add` marker;
- normalized enclosed text.

It can determine B-OUTGOING, because complete opening attributes include the presence or absence of `@next`.

It cannot determine B-INCOMING because predecessors may live outside the local scope.

It cannot determine B-CANCEL because cancellation markup has been flattened away.

### LOCAL_SCOPE_XML

Exposes:
- opening marker;
- complete XML inside the source span;
- closing marker.

It can determine:
- B-OUTGOING;
- B-CANCEL.

It cannot determine B-INCOMING from the local scope alone.

### SOURCE_LINKED

Exposes a version-pinned source route to the full C18 manuscript source and reopens/scans the source.

It may determine all three continuation families.

This is the strong ordinary provenance/navigation baseline.

## 5. Safe decoder semantics

Every interface returns, per continuation family:

- DETERMINED with an exact structured output; or
- UNKNOWN.

A representation is not penalized for abstaining when the interface does not determine the branch.

An informative wrong answer is an error.

For each interface report:
- exact determined outputs;
- UNKNOWN outputs;
- informative errors;
- positive licensed branches surfaced without reopening;
- serialized interface bytes.

Do not collapse UNKNOWN into FALSE.

## 6. Natural current-answer collisions

Group scopes by the complete CURRENT_SUMMARY payload.

If two or more scopes have byte-identical current summaries but different full-source continuation profiles, record them as natural current-answer collisions.

This is not a claim that the complete source-linked representations are identical.

Also test byte-identical LOCAL_SCOPE_XML collisions with different B-INCOMING outputs. A null is retained.

## 7. Adaptive continuation policy

For each scope, run a deterministic safe policy.

Without source reopening:
1. execute every continuation family that the interface determines as nonempty / positive;
2. retain UNKNOWN families as unresolved;
3. do not invent a branch from an UNKNOWN state.

With one charged source reopening:
1. reopen the frozen source through SOURCE_LINKED;
2. resolve every previously UNKNOWN family;
3. execute any newly licensed positive branch;
4. preserve the registered current answer.

Report immediate positive-branch coverage and complete coverage after reopening separately.

This tests branch availability under a declared policy. It does not establish that no other lawful policy exists.

## 8. Controlled selective-update test

Use every source-internal `sga-add@next` relation that resolves uniquely to another frozen `sga-add@xml:id`.

For each eligible relation:

1. freeze the source scope, target scope, literal relation and pre-event branch ledger;
2. create a controlled source twin that removes exactly that one `@next` attribute and changes no text;
3. rebuild the branch ledger from the mutated source;
4. require the registered current documentary answer for every scope to remain unchanged;
5. compare branch outputs globally.

The only licensed dependency changes are:

- source scope B-OUTGOING loses that relation;
- target scope B-INCOMING loses that predecessor.

B-CANCEL must remain unchanged everywhere.
All unrelated incoming/outgoing outputs must remain unchanged.

This is a controlled relation-status event, not a naturally observed editorial change.

### Unrelated-event control

Where a disjoint second internal `@next` relation exists, remove that relation instead and require the focal source/target pair's branch outputs to remain unchanged.

## 9. Source verification and anti-tautology boundaries

The experiment parses the original source directly and reconstructs each `sga-add` source span from its explicit start/end IDs.

Current-answer equality is tested from source text/place/hand independently of the branch ledger.

The experiment does not claim novelty for:
- following a pointer;
- building a reverse index;
- source reopening;
- dependency propagation;
- UNKNOWN / three-valued logic.

Scientific value, if any, must come from the source-backed boundary between current-answer preservation and continuation capability across real representation interfaces.

A controlled `@next` removal is mechanism evidence only.

## 10. Outcomes retained

The following are all valid outcomes:

- no natural current-answer collision;
- natural collisions with continuation divergence;
- LOCAL_SCOPE_XML already sufficient for all positive branches except reverse-link absence;
- ordinary SOURCE_LINKED recovery closes every gap;
- selective-update propagation passes;
- selective-update propagation exposes unexpected dependencies;
- malformed/unresolved `@next` targets.

No outcome triggers prompt/model/data tuning because no model is used.

## 11. Claim ceiling

A positive development result may support:

> Representations that preserve the same current documentary answer can expose different source-licensed continuation operations; ordinary provenance/source reopening can restore missing continuation context; and a controlled relation-status change can require selective updates to exactly the dependent continuation claims.

It does not establish:

- autonomous scholarly question generation;
- human discovery;
- literary interpretation;
- independent replication;
- long-horizon sustained inquiry;
- superiority to ordinary provenance/query systems;
- a universal representation-sufficiency theorem.

Module C and independent transfer remain separate obligations.
