# Module B v1 — Source-triggered branching and selective state update on Frankenstein C18

Date frozen: 2026-09-28
Status: DEVELOPMENT PROTOCOL ON ALREADY-EXPOSED C18. NOT INDEPENDENT TRANSFER.

## Purpose

Test the next step beyond Module A:

> Can a research interface preserve not only the current collation answer, but also the source-grounded distinctions that license which follow-up inquiry becomes admissible and which research-state fields should be updated?

This study does not test autonomous natural-language question generation. It tests a frozen branch grammar whose eligibility is triggered by source evidence rather than by a hand-authored case list.

## Source

FrankensteinVariorum/collationWorkspace
commit: 5a208f869ff1213defa000e3181d5315a072a15f
chunk: C18

C18 is development material already inspected in this project.

## Population

All 493 published C18 apparatus units are retained.

No positive-only case filtering is permitted.

## Current task

Q0_ALIGNMENT:
recover the native published normalized comparison for the current apparatus unit.

All compared interfaces must preserve Q0_ALIGNMENT before continuation claims are interpreted.

## Frozen source-grounded branch grammar

The evaluator first determines whether the selected manuscript text is inside an encoded sga-add scope.

From an enclosing addition scope, the following branch types are licensed:

### B_PREDECESSOR

Eligible iff:
- the enclosing sga-add carries xml:id = X; and
- another source sga-add has @next="#X".

Question:
Does the selected insertion continue an earlier explicitly linked source fragment, and what source fragment is linked?

Required evidence:
the incoming @next relation and the referenced/current source spans.

### B_INTERNAL_CANCELLATION

Eligible iff the enclosing source span contains a nested del or mdel with nonempty textual content.

Question:
Which characters or words are cancelled inside the encoded addition?

Required evidence:
the nested source deletion/cancellation element and its text.

### B_SCOPE_ONLY

Eligible iff the selected text is inside an encoded addition but neither of the two richer branches is licensed.

Question:
What is the encoded addition's identity and encoded place/hand state?

### B_OUTSIDE_CONTROL

If the selected text is outside every encoded sga-add, no insertion-specific branch is licensed under this grammar.

This does not mean no scholarly follow-up exists. It means none of the frozen insertion-specific branches is licensed.

## Important anti-tautology rule

The branch label is not supplied to the consumer.

The consumer receives only its declared representation plus permitted source-reopening operations. The evaluator derives the reference branch set independently from the pinned source.

A model that simply emits all branch labels fails precision.

## Interfaces

### I_NATIVE_FULL

Complete published apparatus stream with inherited state, plus the pinned raw manuscript source for source relations.

### I_LOCAL_ONLY

Complete serialized local app only.
No app ordinal, neighboring units, inherited open-scope state, original object handle, or hidden source lookup.

### I_SOURCE_LINKED

Complete local app plus:
- pinned source commit/path;
- fixed-width 1-based app ordinal;
- lawful source reopening.

### I_SCOPE_STATE

Complete local app plus the source-derived open-scope state entering that app.
When a source relation beyond the scope header is needed, source reopening by scope identity is charged.

## Research-state update schema

Before continuation:
- alignment = Q0_ALIGNMENT output;
- insertion_scope = UNRESOLVED unless determined by the interface;
- predecessor_relation = NOT_ASSESSED;
- internal_cancellation = NOT_ASSESSED.

After legal branch execution, update only fields for which source evidence was inspected.

Allowed field states:
- insertion_scope: INSIDE / OUTSIDE / UNRESOLVED
- predecessor_relation: PRESENT / ABSENT_AFTER_INSPECTION / NOT_ASSESSED / UNRESOLVED
- internal_cancellation: PRESENT / ABSENT_AFTER_INSPECTION / NOT_ASSESSED / UNRESOLVED

A missing branch is not automatically evidence of ABSENT. Absence is licensed only after the relevant source span/relation domain has been inspected.

Q0_ALIGNMENT must remain unchanged.

## Primary metrics

For all 493 checkpoints:
- reference branch set;
- exact branch-set recovery;
- branch precision and recall;
- safe ambiguity/abstention;
- unsupported branch emissions;
- insertion-scope recovery;
- predecessor and cancellation state updates;
- collateral changes to Q0_ALIGNMENT;
- source reopen count;
- source bytes read under the implemented route;
- extra retained payload bytes.

Report dependency-aware counts. Multiple checkpoints in one source addition are not independent replications.

## Local-only identifiability audit

For each byte-identical local-app equivalence class, compute the set of reference branch sets observed among its source occurrences.

If one local payload maps to more than one branch set, I_LOCAL_ONLY is non-determining for exact branch selection on that class.

This is a finite-population interface collision, not a claim that the entire edition is information-theoretically unrecoverable.

## Controls

1. Matched wrong locator on every ambiguous local class member:
   same commit/path and same serialized byte length; wrong ordinal chosen from an identical local payload with a different reference branch set.

2. Harmless current-task control:
   all interface/branch operations must preserve Q0_ALIGNMENT.

3. Outside-scope controls:
   checkpoints outside encoded additions must not be forced into insertion-specific follow-up.

4. Source-native strong baseline:
   ordinary lawful source reopening receives full credit.

## Dispositions

MODULE_B_BRANCHING_OBSERVED:
the source contains at least two distinct eligible continuation types or branch/no-branch states.

LOCAL_CURRENT_EQUIVALENCE_CONTINUATION_SEPARATION:
at least one byte-identical local payload has the same Q0_ALIGNMENT but different source-licensed branch sets.

SOURCE_LINKED_BRANCH_RECOVERY:
I_SOURCE_LINKED exactly recovers the reference branch set on all eligible text-bearing checkpoints.

SCOPE_STATE_BRANCH_RECOVERY:
report exact finite-population result; no success is assumed.

SELECTIVE_STATE_UPDATE:
legal branch execution updates only evidence-supported continuation fields while Q0_ALIGNMENT remains invariant.

AUTONOMOUS_QUESTION_DISCOVERY:
NOT TESTED.

SELECTIVE_BELIEF_REVISION:
NOT ESTABLISHED unless a prior substantive conclusion changes under later source evidence. Resolving NOT_ASSESSED/UNRESOLVED is state refinement, not belief revision.

## Stop rule

If ordinary source-linked reopening already recovers the entire branch set, retain that as the strong result/null. Do not invent a bespoke repair advantage.

If the frozen branch grammar yields only trivial duplication of scope membership, report that and stop rather than adding branches after outcome.

Any later LLM or agent question-generation study must be separately frozen.