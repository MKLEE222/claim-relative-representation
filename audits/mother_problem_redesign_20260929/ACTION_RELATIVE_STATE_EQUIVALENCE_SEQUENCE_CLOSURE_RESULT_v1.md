# Action-relative state equivalence and sequence-closure result v1

Date: 2026-09-30
Status: ACTION_RELATIVE_EQUIVALENCE_SEQUENCE_CLOSURE_PASS.

## 1. Governing protocol

Frozen before implementation:

    ACTION_RELATIVE_STATE_EQUIVALENCE_SEQUENCE_CLOSURE_PROTOCOL_v1.md

Formal typing clarification:

    ACTION_RELATIVE_EQUIVALENCE_SIGNATURE_TYPING_AMENDMENT_v1.md

The amendment separates:
- event/relation binding requirements Beta(g);
- state/history qualification requirements Kappa(g).

Thus state equivalence is defined on the state-side signature rather than conflating exact event
binding with target live/current status.

## 2. Workflow

Workflow:

    action-relative-equivalence-sequence-closure-v1

Successful run:

    36661636458

Head:

    56b26c6f53001b55eabb23c9f91370fed5225f2d

Artifact:

    11074423748

Artifact ZIP SHA-256:

    b94d1335c155c3e8d9f07b519e92ecea57b53349ca72c6ddbc078a28a45cd0f7

Overall:

    ACTION_RELATIVE_EQUIVALENCE_SEQUENCE_CLOSURE_PASS

## 3. Frozen evidence input

Formalization Papers is read from the already frozen corrected reproduction artifact:

    corrected run      36659349160
    corrected artifact 11073656774
    corrected ZIP SHA-256
        3819e4cd06fe4b22a6a68aaa4ca3ee01515fac08b25ac4cdb63e61463bf46e8d

The closure audit does not rerun candidate discovery or redefine the population.

Formalization denominators:

    RECORD_REVIEW              48
    REPLACE_FORMALIZATION       8
    RECORD_RESPONSE            52
    REVISE_PUBLICATION_STATUS   8

Yule-Cordier inputs remain the pre-existing page-verified Paper Money and Arbre Sec natural
sequences.

## 4. Action-relative state equivalence

For fixed admissible event/relation binding e and generator g, define:

    S ~_g S'

when S and S' agree on the registered state-side qualification signature:

    Kappa(g)

The tested implication is:

    S ~_g S'
    =>
    Q_g(S,e) = Q_g(S',e)

for the registered qualification model.

Natural action contexts checked:

    120

Qualification-invariance result:

    120/120 PASS

The state pairs retain the registered required conditions while changing information outside the
state-side signature, including irrelevant history/noise or registered nonrequired history.

No selected generator changes under a registered equivalent-state perturbation.

## 5. REQUIRED-dimension witnesses

Total registered REQUIRED witnesses:

    393

Pass:

    393/393

Witness families include:

### Event/relation-side Beta(g)

- wrong root/object binding;
- wrong formalization target;
- wrong review target;
- wrong update target;
- wrong scholarly-claim target.

### State-side Kappa(g)

- target no longer live/current;
- update explicitly retracted;
- response attempted before review;
- response attempted before current update;
- decision attempted before current update;
- same-current-state retained-history ablation for RECORD_RESPONSE;
- same-current-assertion retained-history ablation for RESOLVE.

Thus every registered REQUIRED condition used in the closure has an availability-changing witness.

## 6. NOT_REQUIRED-dimension invariance

Registered nonrequired witnesses:

    19

Pass:

    19/19

These include:
- REPLACE_FORMALIZATION with changed/added irrelevant prior history;
- REVISE_PUBLICATION_STATUS with transition history erased while current update is retained;
- Yule ADD_ALTERNATIVE with irrelevant history variation;
- Yule RECORD_EVIDENCE with history ablation while the exact live relation target remains.

Therefore:

    NOT_REQUIRED_IN_REGISTERED_TASK

is operational rather than rhetorical.

The result is task-relative and does not assert that the same information can never matter under
another action family.

## 7. Formalization Papers sequence closure

Connected natural chains:

    52

Closure:

    52/52 PASS

Registered chain:

    RECORD_REVIEW
    -> REPLACE_FORMALIZATION
    -> RECORD_RESPONSE
    -> REVISE_PUBLICATION_STATUS

For every chain, the state before RECORD_RESPONSE contains all conditions read by its registered
signature:

    exact review target live          true
    exact update target current       true
    review-entry history retained     true
    update-entry history retained     true

Writers:

    RECORD_REVIEW
        -> live review target
        -> review transition/history

    REPLACE_FORMALIZATION
        -> current update target
        -> update transition/history

RECORD_RESPONSE then lawfully reads those conditions.

For the final decision:

    REPLACE_FORMALIZATION
        -> current update target

is sufficient for the registered:

    REVISE_PUBLICATION_STATUS

qualification, while retained transition history is not required.

Thus sequence closure is generator-specific rather than one globally increasing metadata burden.

## 8. Yule-Cordier sequence closure

Natural sequences:

    2

Pass:

    2/2

### Paper Money

    ADD_ALTERNATIVE
    -> RESOLVE

ADD_ALTERNATIVE writes:
- live PM02 target claim;
- CONTRADICTS_PRIOR transition history for PM02.

RESOLVE reads:
- live PM02 target;
- retained contradiction/origin history.

Closure:

    PASS

### Arbre Sec

    ADD_ALTERNATIVE
    -> RECORD_EVIDENCE

ADD_ALTERNATIVE writes:
- live ARBR-ID-HS target;
- transition history.

RECORD_EVIDENCE reads:
- exact live ARBR-ID-HS target;

but does not require retained transition history under the registered task.

Closure:

    PASS

This directly demonstrates two different sequence burdens after the same first-order generator.

## 9. Typed limitation

Three Yule witnesses retain a bounded identification limitation:

    typed_limitation_count = 3

These are:
- Paper Money ADD_ALTERNATIVE;
- Arbre Sec ADD_ALTERNATIVE;
- Arbre Sec RECORD_EVIDENCE.

In the current natural Yule engine, exact relation-target identity and live-target lookup are
coupled for those acts.

Therefore that ecology does not independently identify:

    Beta TARGET_IDENTITY

versus:

    Kappa TARGET_LIVE_OR_CURRENT

for those three witnesses.

This does not affect their combined target-binding/live-target necessity.

Formalization Papers contains independently separated event-target and live/current-state probes,
so the distinction is identified elsewhere in the cross-ecology evidence.

Do not claim that Yule alone separates those axes.

## 10. Bounded theorem

The strongest licensed theorem is:

> For the registered natural scholarly action families, and for a fixed admissible event/relation
> binding, two scholarly states that agree on the state/history distinctions in the generator's
> registered qualification signature are equivalent with respect to that generator's availability.
> Every registered required distinction has an availability-changing witness, while registered
> nonrequired history dimensions can be changed or removed without changing qualification.
> Across the audited natural sequences, earlier generators create the target, live/current-state,
> and history conditions read by later generators.

Formally, with:

    Sigma(g) = (Beta(g), Kappa(g))

and fixed admissible e satisfying Beta(g):

    S ~_g S'
    iff
    P_Kappa(g)(S) = P_Kappa(g)(S')

then, under the registered models:

    S ~_g S'
    =>
    Q_g(S,e) = Q_g(S',e)

The sequence burden is an ordered family:

    Sigma(g1)
    -> Sigma(g2)
    -> ...
    -> Sigma(gn)

rather than one universal metadata checklist.

## 11. Relation to the original obligation list

The original representation obligations are no longer best understood as fields that every
representation must preserve maximally.

They are conditions distributed across generator-specific qualification signatures.

Examples:

    object/target identity
        -> event/relation binding domain

    live/version state
        -> current-state qualification

    provenance/relation binding
        -> justification and target semantics

    transition history
        -> required only for generators whose Sigma(g) reads it

    selectivity/result determinacy
        -> lawful execution of the selected generator

Thus researchability is action-relative and sequence-dependent.

## 12. Claim ceiling

This result does not establish:
- universal minimal signatures;
- a complete scholarly generator vocabulary;
- a universal action algebra;
- that dimensions marked nonrequired here are irrelevant to other tasks;
- prevalence;
- literal prospective fresh confirmation.

The authoritative Formalization Papers fresh attempt remains INVALID.

The result is a formal/empirical closure over existing corrected and exposed evidence.
