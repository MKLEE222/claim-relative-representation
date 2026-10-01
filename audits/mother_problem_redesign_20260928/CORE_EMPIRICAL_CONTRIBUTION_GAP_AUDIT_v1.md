# Core empirical contribution gap audit v1

Date: 2026-09-28
Status: EMPIRICAL PLANNING / CLAIM-LICENSING AUDIT. NOT MANUSCRIPT ARCHITECTURE.

## 1. Purpose

The project now has substantial mechanism evidence, but the strongest paper-level empirical contribution is not yet fully identified.

This audit asks a narrower question:

    What empirical facts would have to be true for the core dynamic-researchability contribution to stand independently of implementation artifacts, development-corpus reuse, and overbroad representation claims?

The answer is expressed as missing identification obligations, not as a publication narrative.

## 2. What is already empirically strong

The following are already supported by executed studies and are not the main missing pieces.

### 2.1 Current-task sufficiency is not dynamic sufficiency

Module E shows on natural Whitman revisions that a state sufficient for the current endpoint task can fail to determine the revised epistemic state or transition history.

In particular, for D2:
- identity-rich event channels can make transition identity exact while a reduced parent state still fails to recover the complete child epistemic state;
- reopening the exact child object can recover the terminal child state while still failing to recover old status for removed relations.

Thus:

    current answer
    !=
    revised state
    !=
    transition history

as empirical tasks.

### 2.2 Dynamic sufficiency is distributed across an information interface

The strongest current formulation is not "one representation is sufficient".

It is:

    I_t = (S_t, E_t, A_t)

where:
- S_t = retained state;
- E_t = incoming revision/evidence channel;
- A_t = lawful source access.

Module E shows that the same task-relevant distinction may be supplied by more than one component, while aggregate information can remain non-determining when binding is removed.

Modules F/G transfer parts of this mechanism to published corrigenda.

### 2.3 Target determinacy is not transition applicability

Module G shows that:

    exact target + exact proposed result

does not license:

    exact warranted transition

when the event's assumed parent state is incompatible with the frozen source snapshot.

This supplies an applicability obligation separate from target recovery.

### 2.4 Object identity is an empirical precondition, not a parser detail

Modules H/I/J/K establish a real failure sequence:
- broad/incorrect document composition created false temporal positives;
- freezing a scholarly-object grammar removed those false positives;
- the first truly fresh GeStA holdout then produced a legitimate applicability null rather than a performance score.

Thus temporal composition must be object-gated.

## 3. Critical gap G1 — no genuine positive R* versus native baseline

Current inherited dynamic runtime contains:

    if arm in ("I_NATIVE", "I_RSTAR", "I_NO_HISTORY"):
        claims = copy.deepcopy(doc["claims"])
        origin_handle = copy.deepcopy(doc["origin_handle"])

Therefore I_NATIVE and I_RSTAR are not currently distinct representations.

Consequences:

1. no observed I_NATIVE versus I_RSTAR difference can identify an R* advantage;
2. the current dynamic experiments can identify component necessity through ablations, but not superiority of a proposed representation over a native baseline;
3. any paper-level claim that "R* outperforms native representation" is currently unlicensed.

### Required empirical repair

Freeze a genuinely distinct comparator before the next fresh outcome is opened.

Candidate comparator families that preserve scientific meaning:

#### B_NATIVE_SOURCE

Expose only the project's native machine-readable carriers and ordinary source-local relations.

Do not materialize:
- an added transition ledger;
- a synthetic alternative set;
- cross-event retained history not present in the native project state.

This tests whether the proposed dynamic interface adds task-relevant state beyond ordinary project-native encoding.

#### B_CURRENT_REOPEN

Allow lawful reopening of the current/latest source object but retain no prior transition ledger.

This is a strong baseline for current-state reconstruction.

Expected scientific separation, if real:

    current state may be recoverable
    while deleted/removed transition history is not.

#### B_FLAT_CLAIMS

Retain all temporal values but remove object/applicability/transition binding.

This tests whether quantity of information can substitute for binding structure.

No comparator may be chosen or modified after seeing the next fresh results.

## 4. Critical gap G2 — no fresh eligible independent dynamic trajectory yet

Current state:

    J: eligible trajectories, but exposed development corpora
    K: genuinely fresh, but N_eligible = 0

Therefore the key cell remains empty:

    fresh
    + independent project
    + prospectively eligible scholarly object
    + dynamic trajectory
    + source audit

### Required evidence

A future holdout must be selected from project-level documentation before episode opening and must prospectively establish:
- frozen A/B/C object compatibility;
- a closed population;
- source/provenance auditability;
- the temporal/evidential carrier layers required by the registered dynamic gate.

If the study is claimed to be J-equivalent, the independent later-evidence layer must be prospectively documented as well.

Do not rename a sent date or dateline as "origin evidence" after opening merely to make a trajectory exist.

## 5. Critical gap G3 — object portability and event portability are currently conflated

A representation can fail for at least two scientifically different reasons:

1. OBJECT INAPPLICABILITY:
   no uniquely admissible scholarly object under the frozen grammar;

2. DYNAMIC INAPPLICABILITY:
   an object exists, but the required root disagreement / later evidence / revision event does not exist.

Module K establishes the first type.

The next study must report these denominators separately:

    N_total
    N_object_eligible
    N_root_dynamic_eligible
    N_full_trajectory_eligible

A positive evaluator rate may only use the last denominator.
A zero at an earlier gate is a scope result, not a model failure.

## 6. Critical gap G4 — the dynamic decomposition is stronger than the current J ablation set

J currently emphasizes:
- alternatives;
- binding;
- history.

The executed E/F/G studies imply a more precise decomposition:

    WarrantedDynamicResearchability
    =
    ObjectIdentity
    AND ClaimApplicability
    AND TargetDeterminacy
    AND ResultDeterminacy
    AND Selectivity
    AND ProvenancePreservation
    AND TransitionCompatibility
    AND HistoryRetention(T)

where HistoryRetention is required when the task asks for delayed transition audit.

This is not yet one fully identified intervention suite.

### Required controlled identification

Before a new fresh holdout, build synthetic/matched controls that independently break:

1. object identity;
2. claim-to-object applicability;
3. event-to-target binding;
4. source-side transition compatibility;
5. corrected-result specification;
6. selective update / collateral stability;
7. provenance preservation;
8. retained transition history.

The evaluator must distinguish which obligation failed rather than collapsing all failures into end_to_end_pass = false.

Natural corpora then serve as witnesses for these predeclared failure classes.

## 7. Critical gap G5 — necessity versus substitutability must remain explicit

Module E already falsifies a simplistic claim that every distinction must be stored in one retained representation.

The correct empirical object is distributed.

A distinction may be supplied by:
- retained state;
- incoming event detail;
- lawful parent/child/correction-source access;
- a valid composition of these.

Therefore future ablations must distinguish:

    globally necessary information

from:

    necessary-at-the-interface information

and from:

    one particular carrier being necessary.

A strong result is not:

    field X must always be stored.

A stronger and more defensible result is:

    distinction D must be available somewhere in the lawful information interface for task T; otherwise two admissible histories collapse to the same observed interface while requiring different warranted actions.

This is the direct bridge to the mother problem.

## 8. Priority empirical program

### P0 — finish portable-engine audit

No fresh corpus opening before:
- inherited F1-F16 pass;
- portable hardening controls pass;
- Berlin/Paul/StaBi exposed regression has zero unresolved oracle/runtime contracts;
- every count delta from Module J is explained rather than tuned away.

### P1 — freeze a real comparator

Implement and freeze at least one genuinely distinct positive baseline before the next fresh outcome.

I_NATIVE must not remain an alias for I_RSTAR if native-versus-R* comparison is part of the empirical contribution.

### P2 — fill the missing fresh eligible cell

Run exactly one preregistered independent holdout whose project-level documentation establishes object and dynamic feasibility before episode opening.

Retain PASS, BOUNDED_PARTIAL, NULL_APPLICABILITY, or INVALID without rescue.

### P3 — prospective cross-event validation

Do not make the next independent result another date-only copy if the core claim is meant to concern scholarly revision generally.

After the first clean portable trajectory, use a second, prospectively selected event family such as:
- relation-status revision;
- source-attribution/provenance revision;
- published correction with explicit parent-state precondition.

The same decomposition must be tested without introducing event-specific rescue rules.

### P4 — identification-completeness matrix

Construct the eight-obligation matched-control matrix in Section 6 and map each natural witness to the obligation(s) it identifies.

This is more valuable than adding many more corpora without new separation.

## 9. Current strongest empirical core

The strongest currently defensible core is not:

    our representation is richer and therefore better.

Nor is it:

    every scholarly system needs one fixed provenance schema.

The evidence currently points to:

    Researchability is task- and claim-relative, and dynamic researchability depends on preserving the distinctions needed to determine warranted action across a lawful information interface.

For dynamic tasks, those distinctions can be distributed across retained state, incoming evidence, and source access.

Object identity and claim applicability gate whether evidence can legally compose; target/result determinacy alone do not guarantee transition applicability; exact terminal-state recovery does not guarantee recoverable transition history.

## 10. What would make the core contribution stand materially stronger

The contribution becomes substantially harder to dismiss once all four are present:

1. controlled identification of the distinct obligations;
2. natural-event evidence showing the obligations are not toy artifacts;
3. at least one truly fresh, eligible, independent prospective trajectory under a frozen portable engine;
4. a genuinely distinct positive baseline showing what the proposed interface adds beyond ordinary native/current-state access.

Until then, the mechanism program is strong, but an R*-specific superiority claim and broad prospective generalization remain underidentified.
