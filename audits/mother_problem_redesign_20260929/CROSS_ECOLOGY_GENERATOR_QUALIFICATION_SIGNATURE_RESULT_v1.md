# Cross-ecology generator qualification signature result v1

Date: 2026-09-30
Status: POST-FRESH / EXPOSED CROSS-ECOLOGY CONDITIONAL-MINIMALITY AUDIT / PASS.

## 1. Workflow

Workflow:

    cross-ecology-generator-signature-audit-v1

Run:

    36660547327

Head:

    c25866f7ddedbdd3441a5801cda2a0aa8a5eb39d

Artifact:

    11073604129

Artifact ZIP SHA-256:

    f9e79482a251fa58d41072458de6ba16c26be26cead38f67b352b6e3854c8ce0

Overall:

    PASS

## 2. Formalization Papers signatures reproduced

Natural action denominators:

    RECORD_REVIEW             48/48
    REPLACE_FORMALIZATION      8/8
    RECORD_RESPONSE           52/52
    REVISE_PUBLICATION_STATUS  8/8

Signatures:

### RECORD_REVIEW

    TARGET_IDENTITY             REQUIRED
    TARGET_LIVE_OR_CURRENT      REQUIRED
    RETAINED_TRANSITION_HISTORY ROOT_ACTION_NO_PRIOR_HISTORY

### REPLACE_FORMALIZATION

    TARGET_IDENTITY             REQUIRED
    VERSION_OR_VALIDITY_STATE   REQUIRED
    RETAINED_TRANSITION_HISTORY NOT_REQUIRED_IN_REGISTERED_TASK

### RECORD_RESPONSE

    TARGET_IDENTITY             REQUIRED
    TARGET_LIVE_OR_CURRENT      REQUIRED
    RETAINED_TRANSITION_HISTORY REQUIRED

### REVISE_PUBLICATION_STATUS

    TARGET_IDENTITY             REQUIRED
    TARGET_LIVE_OR_CURRENT      REQUIRED
    RETAINED_TRANSITION_HISTORY NOT_REQUIRED_IN_REGISTERED_TASK

## 3. Yule-Cordier natural signatures

The shared case-independent target-bound v2 engine was used.

Oracle/runtime agreement:

    exact

Case-specific branch scan:

    clean

### ADD_ALTERNATIVE

Natural acts:

    Paper Money PM02
    Arbre Sec Houtum-Schindler proposal

Result:

    2/2 PASS

Signature:

    TARGET_IDENTITY             REQUIRED
    TARGET_LIVE_OR_CURRENT      REQUIRED
    RETAINED_TRANSITION_HISTORY NOT_REQUIRED_IN_REGISTERED_TASK

Both acts qualify from their initial live-target states with empty transition history.

Replacing the relation target with a non-live claim rejects.

### RESOLVE

Natural act:

    Paper Money PM03 correction of the prior criticism

Result:

    1/1 PASS

Signature:

    TARGET_IDENTITY             REQUIRED
    TARGET_LIVE_OR_CURRENT      REQUIRED
    RETAINED_TRANSITION_HISTORY REQUIRED

After PM02 enters the live assertion state, PM03 qualifies as RESOLVE.

Holding the exact current assertions fixed while erasing the evidence/event/transition ledgers
produces:

    RELATION_TARGET_HISTORY_UNRESOLVED

Thus live target state is insufficient for this resolution act.

### RECORD_EVIDENCE

Natural act:

    Arbre Sec bibliographic reply to the Houtum-Schindler proposal

Result:

    1/1 PASS

Signature:

    TARGET_IDENTITY             REQUIRED
    TARGET_LIVE_OR_CURRENT      REQUIRED
    RETAINED_TRANSITION_HISTORY NOT_REQUIRED_IN_REGISTERED_TASK

The reply is unavailable before the targeted competing proposal exists.

After that proposal is live, erasing transition history while retaining the exact live target does
not block the bibliographic reply.

## 4. Cross-ecology history heterogeneity

History-required generators:

    Formalization Papers:
        RECORD_RESPONSE

    Yule-Cordier:
        RESOLVE

History-not-required generators:

    Formalization Papers:
        REPLACE_FORMALIZATION
        REVISE_PUBLICATION_STATUS

    Yule-Cordier:
        ADD_ALTERNATIVE
        RECORD_EVIDENCE

Formalization also contains the root action:

    RECORD_REVIEW
    -> ROOT_ACTION_NO_PRIOR_HISTORY

Thus both ecologies independently contain:
- at least one generator whose lawful availability depends on retained transition history;
- at least one generator whose registered qualification does not require that history.

## 5. Theoretical result

A universal predicate:

    Q(S,rho,target,H,e)

with all representational distinctions treated as mandatory for every action is too coarse.

The evidence supports generator-specific signatures:

    Sigma(g)

and generator-indexed qualification:

    Q_g(
        projection_{Sigma(g)}(S,H),
        rho,
        target,
        e
    )

Different generators can inspect different projections of the same full scholarly state.

For the audited cases:

    H in Sigma(RECORD_RESPONSE)
    H in Sigma(RESOLVE)

while:

    H not in Sigma(REPLACE_FORMALIZATION)
    H not in Sigma(REVISE_PUBLICATION_STATUS)
    H not in Sigma(ADD_ALTERNATIVE)
    H not in Sigma(RECORD_EVIDENCE)

under their registered tasks.

## 6. Why this matters for researchability

Researchability is not preserved by keeping one maximal metadata checklist merely because that
checklist contains everything observed to matter somewhere.

The stronger claim is task/action-relative:

> A representation remains adequate for a future scholarly action when it preserves the
> distinctions in that action's qualification signature.

For a sequence of actions, the relevant representation burden can change after each transition
because:
- the next generator can be different;
- its signature can be different;
- earlier generators can create the target/history that a later signature inspects.

Thus:

    representation sufficiency
    is generator-relative
    and sequence-dependent.

## 7. Relation to composition

This result sharpens the composition problem.

The first transition can affect future researchability in two distinct ways:

1. it changes the scholarly state inspected by a later generator;
2. it can create the transition history required by the later generator's signature.

Example:

    Paper Money:
        ADD_ALTERNATIVE
        -> creates PM02 + contradiction history
        -> RESOLVE can later inspect that history

Example:

    Formalization Papers:
        RECORD_REVIEW + REPLACE_FORMALIZATION
        -> create target/history
        -> RECORD_RESPONSE becomes lawfully interpretable

Therefore composition is not simply function composition over one fixed state vector.

It is composition across generator-indexed qualification domains.

## 8. Claim ceiling

This result is exposed/conditional-minimality evidence.

It does not establish:
- globally minimal signatures;
- completeness of the generator vocabularies;
- that untested historical information can never matter;
- a universal action algebra;
- literal prospective fresh confirmation.

It establishes that universal all-fields-required qualification is empirically too coarse across
the registered natural action families.
