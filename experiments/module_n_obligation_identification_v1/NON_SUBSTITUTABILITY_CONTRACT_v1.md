# Module N — obligation non-substitutability contract v1

Date frozen: 2026-09-29
Status: PRE-IMPLEMENTATION / PRE-RESULT CONTRACT. NO NEW FRESH CORPUS IS CONSUMED.

## 1. Scientific objective

The project already shows that several rich-information ablations fail.
That is not yet sufficient to claim that distinct scholarly obligations are independently
required, because some inherited ablations remove multiple distinctions at once.

The clearest example is I_NO_BINDING, which jointly disrupts:
- object identity;
- claim applicability;
- source/locator binding;
- event authorization.

Module N therefore tests non-substitutability by intervening on one obligation at a time while
holding the others as intact as the frozen portable contract permits.

The unit of result is a capability vector, not a scalar representation score.

## 2. Reference capability vector

For a full eligible episode define:

C1 CURRENT_STATE
- current/root warrant is available for the information currently admitted.

C2 DISCOVERY
- the task-relevant dispute/question is correctly identified.

C3 EVENT_APPLICABILITY
- a later evidence event is correctly authorized or rejected.

C4 RESULT_DETERMINACY
- the post-event warrant preserves exact/interval/open/alternative/unresolved status.

C5 SELECTIVITY
- the authorized event changes only licensed temporal paths.

C6 CURRENT_PROVENANCE
- current live claims retain source/object/applicability proof.

C7 TRANSITION_ATTRIBUTION
- event, target object and admitted evidence are bound exactly.

C8 DELAYED_HISTORY
- the transition can later be reconstructed with before/after warrant and event/evidence identity.

The retained portable RSTAR path is the reference development condition.

## 3. Registered single-obligation interventions

### N_NO_OBJECT_ID — O1 ObjectIdentity

Preserve:
- claim values/intervals;
- claim roles;
- applicability-class labels;
- source file/locator/provenance fields.

Remove:
- object_id;
- object_boundary_signature from active/action binding.

The intervention must not erase source provenance merely because object identity is absent.

Expected separation:
- C1 may remain reconstructable from values;
- O2/O6 labels remain visibly present;
- C3/C7 must fail because the event cannot be authorized to one scholarly object.

Purpose:
show that applicability/provenance labels do not substitute for object identity.

### N_NO_APPLICABILITY — O2 ClaimApplicability

Preserve:
- object_id;
- object boundary signature;
- source repository/version/file/locator;
- claim role/value.

Remove only:
- applicability_class proof from active claims/evidence.

Expected separation:
- object identity and source provenance remain;
- current value-level state may remain available;
- C3/C7 must fail under the frozen portable admission rule.

Purpose:
show that knowing the object and source does not by itself establish that evidence applies.

### N_NO_CURRENT_PROVENANCE — O6 ProvenancePreservation

Preserve:
- object identity;
- applicability class;
- claim role/value;
- current warrant/result.

Remove from the scholar-visible current representation:
- source file;
- source locator contract;
- source repository/version provenance needed to audit live claims.

Do not alter the underlying event engine in this arm; this is an information-surface intervention.

Expected separation:
- C1/C4 can remain correct;
- C6 fails.

Purpose:
show that a correct current answer is not equivalent to a warranted/auditable answer.

### N_NO_TRANSITION_BINDING — O7 TransitionCompatibility

Preserve:
- current claim provenance;
- object identity;
- applicability proof;
- current root warrant;
- later evidence content.

Remove only the durable authorization link required to bind the later event to:
- target object;
- source context;
- evidence claim.

The evidence may be visible but cannot be lawfully applied by the transition engine.

Expected separation:
- C1/C6 remain;
- C3/C7 fail.

Purpose:
show that provenance does not substitute for transition compatibility.

### N_COLLATERAL_UPDATE — O5 Selectivity

Preserve:
- valid object/evidence/event binding;
- event applicability;
- history ledger.

Inject one declared collateral mutation to an unrelated root temporal claim/state path.

Expected separation:
- C3/C7 remain;
- C5 fails;
- C8 may remain capable of revealing the bad transition.

Purpose:
show that history retention does not substitute for selective update.

### N_NO_HISTORY — O8 HistoryRetention

Use the existing frozen no-history semantics:
- valid event applies;
- post-event current state remains correct;
- selective update remains correct;
- transition history is removed before delayed audit.

Expected separation:
- C4/C5 can remain;
- C8 fails.

Purpose:
show that correct/selective current state does not substitute for retained history.

### N_COLLAPSE_RESULT_STATUS — O4 ResultDeterminacy

On episodes whose correct post-event warrant is ALTERNATIVE_SET, INTERVAL, OPEN_INTERVAL or
UNRESOLVED, replace that status with an unjustified single/exact resolution while leaving
object/source/history metadata otherwise available.

Expected separation:
- object/provenance/history may remain;
- C4 fails.

This arm is evaluated only on episodes for which a non-singleton/non-exact warrant is required.

## 4. Primary non-substitutability contrasts

The following contrasts are preregistered.

A. O1 vs O2
- N_NO_OBJECT_ID retains applicability labels but loses event authorization.
- N_NO_APPLICABILITY retains object identity but loses event authorization for a different reason.
- The failure records must distinguish these causes.

B. O6 vs O7
- N_NO_CURRENT_PROVENANCE: current result can remain, provenance audit fails.
- N_NO_TRANSITION_BINDING: current provenance remains, event authorization fails.

C. O5 vs O8
- N_COLLATERAL_UPDATE: transition history exists but selectivity fails.
- N_NO_HISTORY: selectivity succeeds but delayed history fails.

D. O4 vs O8
- N_COLLAPSE_RESULT_STATUS may retain history but misrepresent the warranted result.
- N_NO_HISTORY retains the correct result but loses transition history.

A contrast is not established merely because both arms fail overall.
It requires the predicted capability cross-over.

## 5. Evaluation rule

For every arm report C1-C8 separately.

Do not compute:
- an average obligation score;
- a weighted representation score;
- a winner ranking.

A non-substitutability contrast passes only if the preregistered cross-over pattern is observed.

Unexpected preserved capability must be retained and may weaken the theoretical claim.

## 6. Data status

Development stages:
1. synthetic positive/fault controls;
2. exposed Berlin/Paul full eligible Module-L episodes.

StaBi remains an applicability null where no valid object exists.

Module N is not fresh confirmatory evidence.

A future independent holdout may test a subset of these contrasts only after the relevant
interventions and evaluator are frozen.

## 7. Implementation independence

Do not implement Module N as a collection of evaluator-side forced failures.

Each intervention must alter the information/action surface before evaluation.

The evaluator reads resulting traces/states and checks C1-C8 against the unchanged oracle.

Where an intervention is scholar-visible only (N_NO_CURRENT_PROVENANCE), the surface projection
must actually omit provenance fields; the evaluator may not simply mark provenance false.

## 8. Stop condition

Module N is complete when:
- all single-obligation intervention contracts are executable;
- the four preregistered cross-over contrasts are evaluated on synthetic controls;
- exposed Berlin/Paul results are reported without tuning;
- any failure to isolate an obligation is documented rather than repaired post hoc by changing
  the conceptual definition.
