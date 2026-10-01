# Action-relative state equivalence and sequence-closure contract v1

Date frozen: 2026-09-30
Status: PRE-IMPLEMENTATION / EXISTING EXPOSED EVIDENCE ONLY.

## 1. Goal

Convert the empirical qualification-signature results into a bounded generator-indexed theory of
researchability.

The project has already established that different scholarly generators require different
representational distinctions.

Let:

    Sigma(g)

be the registered qualification signature of generator g.

Define action-relative state equivalence:

    S ~_g S'

iff the two states agree on every distinction in Sigma(g) that the registered qualification rule
for g actually inspects.

The question is whether ~_g is sufficient for qualification invariance under the registered
models, and whether every dimension marked REQUIRED has a witnessed counterexample when removed.

## 2. Scope

No new corpus is opened.

Evidence is restricted to:

### Formalization Papers corrected population

Frozen corrected reproduction artifact:

    run 36659349160
    artifact 11073656774

Population:
- 15 roots;
- 8 T0 roots;
- 52 connected chains.

Natural action denominators:
- RECORD_REVIEW = 48;
- REPLACE_FORMALIZATION = 8;
- RECORD_RESPONSE = 52;
- REVISE_PUBLICATION_STATUS = 8.

### Yule-Cordier natural sequences

Page-verified/exposed sequences already frozen in:
- Paper Money;
- Arbre Sec.

Registered generators:
- ADD_ALTERNATIVE;
- RESOLVE;
- RECORD_EVIDENCE.

No new source reading is authorized by this audit.

## 3. Registered signatures

### Formalization Papers

RECORD_REVIEW:
- TARGET_IDENTITY = REQUIRED
- TARGET_LIVE_OR_CURRENT = REQUIRED
- RETAINED_TRANSITION_HISTORY = ROOT_ACTION_NO_PRIOR_HISTORY

REPLACE_FORMALIZATION:
- TARGET_IDENTITY = REQUIRED
- VERSION_OR_VALIDITY_STATE = REQUIRED
- RETAINED_TRANSITION_HISTORY = NOT_REQUIRED_IN_REGISTERED_TASK

RECORD_RESPONSE:
- TARGET_IDENTITY = REQUIRED
- TARGET_LIVE_OR_CURRENT = REQUIRED
- RETAINED_TRANSITION_HISTORY = REQUIRED

REVISE_PUBLICATION_STATUS:
- TARGET_IDENTITY = REQUIRED
- TARGET_LIVE_OR_CURRENT = REQUIRED
- RETAINED_TRANSITION_HISTORY = NOT_REQUIRED_IN_REGISTERED_TASK

### Yule-Cordier

ADD_ALTERNATIVE:
- TARGET_IDENTITY = REQUIRED
- TARGET_LIVE_OR_CURRENT = REQUIRED
- RETAINED_TRANSITION_HISTORY = NOT_REQUIRED_IN_REGISTERED_TASK

RESOLVE:
- TARGET_IDENTITY = REQUIRED
- TARGET_LIVE_OR_CURRENT = REQUIRED
- RETAINED_TRANSITION_HISTORY = REQUIRED

RECORD_EVIDENCE:
- TARGET_IDENTITY = REQUIRED
- TARGET_LIVE_OR_CURRENT = REQUIRED
- RETAINED_TRANSITION_HISTORY = NOT_REQUIRED_IN_REGISTERED_TASK

## 4. Qualification invariance

For each registered natural action context and admissible event e:

If two states S and S' are identical on all REQUIRED dimensions in Sigma(g), then the registered
qualification result for g must agree:

    available_g(S,e) = available_g(S',e)

A state pair may differ arbitrarily on a dimension explicitly registered as:

    NOT_REQUIRED_IN_REGISTERED_TASK

provided all REQUIRED dimensions remain fixed.

The test concerns qualification availability and selected generator, not byte-equality of full
states.

## 5. REQUIRED-dimension counterexamples

For every REQUIRED dimension in every registered signature, construct or reuse a registered state
pair differing only in that dimension while holding the other registered conditions fixed.

Required result:

    available_g(S,e) != available_g(S',e)

or the expected qualified generator is replaced by a registered rejection.

Examples already licensed by prior audits include:
- wrong target;
- target no longer live/current;
- retracted update;
- same current state with erased required history.

A REQUIRED label without such a witnessed counterexample fails this closure.

## 6. NOT_REQUIRED-dimension invariance

For every dimension marked:

    NOT_REQUIRED_IN_REGISTERED_TASK

construct/reuse an ablation pair preserving all REQUIRED conditions while changing/removing that
dimension.

Required result:

    qualification unchanged
    selected generator unchanged

This is task-relative only.

It does not mean the ablated information can never matter under another task.

## 7. Sequence closure

For each registered two-or-more-step sequence, identify which output dimensions written by g_t are
read by Sigma(g_(t+1)).

### Paper Money

    ADD_ALTERNATIVE -> RESOLVE

The first action must create:
- the live target claim PM02;
- the contradiction transition history linking PM02 to its origin.

The second action reads:
- target identity/live status;
- retained transition history.

Required closure:

    writes(g1) covers reads(Sigma(g2))

for the registered natural sequence.

### Arbre Sec

    ADD_ALTERNATIVE -> RECORD_EVIDENCE

The first action must create:
- the live targeted competing claim.

The second action reads:
- target identity/live status;
- not retained transition history.

Required closure:

    target/live output of g1 covers the registered reads of g2

while history ablation remains qualification-invariant.

### Formalization Papers

    RECORD_REVIEW
    -> REPLACE_FORMALIZATION
    -> RECORD_RESPONSE
    -> REVISE_PUBLICATION_STATUS

For RECORD_RESPONSE, the prior actions must jointly create:
- live review target;
- current update target;
- retained review/update history.

For REVISE_PUBLICATION_STATUS, the prior update must create:
- current update target;

while retained transition history is not required by the registered decision task.

## 8. Sequence burden

For a registered sequence:

    g1, g2, ..., gn

define the representational burden at step t as:

    B_t = Sigma(g_t)

The sequence burden is not defined as one universal checklist.

Instead it is the ordered family:

    B_1 -> B_2 -> ... -> B_n

with earlier generators potentially writing dimensions required by later B_t.

The closure audit must report:
- which dimensions are read at each step;
- which preceding generator writes them;
- whether any required dimension is missing.

## 9. Independent-engine requirement

All qualification checks must preserve the existing independent-engine discipline.

Formalization Papers:
- RDFLib-derived oracle state/qualification;
- pyoxigraph-derived runtime state/qualification.

Yule-Cordier:
- target_bound_oracle_v2;
- target_bound_runtime_v2.

Any oracle/runtime disagreement is a failure.

## 10. Pass rule

ACTION_RELATIVE_EQUIVALENCE_SEQUENCE_CLOSURE_PASS only if:

1. qualification invariance passes for every registered natural action context;
2. every REQUIRED signature dimension has at least one witnessed counterexample;
3. every NOT_REQUIRED dimension has at least one invariance witness;
4. Paper Money sequence closure passes;
5. Arbre Sec sequence closure passes;
6. Formalization Papers sequence closure passes for all 52 connected chains;
7. oracle/runtime exactness remains intact.

## 11. Claim ceiling

If PASS, the licensed theorem is bounded:

> Under the registered action families and qualification rules, scholarly states that agree on
> the distinctions in a generator's empirical qualification signature are equivalent with respect
> to that generator's availability. Dimensions registered as required have witnessed
> counterexamples when removed, while registered nonrequired dimensions can be ablated without
> changing qualification. In the audited sequences, earlier generators write the target/state/
> history distinctions inspected by later generators.

This is not:
- a universal minimal representation theorem;
- a universal scholarly action algebra;
- proof that unregistered dimensions never matter;
- prevalence evidence;
- fresh confirmation.
