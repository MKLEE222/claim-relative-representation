# Formalization Papers generator qualification signature audit v1

Date: 2026-09-30
Status: POST-FRESH / EXPOSED CONDITIONAL-MINIMALITY AUDIT.

## 1. Goal

Determine whether the registered qualification inputs are generator-relative rather than a
universal all-fields-required checklist.

The audit operates on the already exposed, corrected Formalization Papers population.

It does not create a fresh confirmation claim.

## 2. Natural generator families

Audit the four generators occurring in complete T0 chains:

    RECORD_REVIEW
    REPLACE_FORMALIZATION
    RECORD_RESPONSE
    REVISE_PUBLICATION_STATUS

RETRACT_TARGET remains synthetic/maintenance-only and is not part of the primary natural
signature matrix.

## 3. Action-level denominators

Decision-extended chain duplication must not inflate action counts.

Define unique action denominators:

### D_REVIEW

Unique:

    (root, submission_np, review_np)

from eligible connected chains.

### D_UPDATE

Unique:

    (root, submission_np, update_np)

from eligible connected chains.

### D_RESPONSE

Unique:

    (root, submission_np, review_np, update_np, response_np)

from eligible connected chains.

### D_DECISION

Unique:

    (root, submission_np, update_np, decision_np, status)

from eligible T0 chains.

All actions come from the frozen eligible denominator.

## 4. Qualification dimensions

The audit distinguishes:

### TARGET_IDENTITY

Does replacing the exact target with a valid foreign-root target make qualification fail?

### CURRENT_OR_LIVE_TARGET

Does qualification depend on the target being the current/live object at that state?

### RETRACTION_STATUS

Where registered, does explicit retraction block qualification?

### RETAINED_HISTORY

Holding the current state fields used by the action fixed, does removing transition history change
qualification?

The audit does not assume every dimension is meaningful for every generator.

Use:

    REQUIRED
    NOT_REQUIRED_IN_REGISTERED_TASK
    ROOT_ACTION_NO_PRIOR_HISTORY
    NOT_APPLICABLE

rather than forcing a universal Boolean vector.

## 5. RECORD_REVIEW probes

For every D_REVIEW action:

### Valid

At S0, review of the current root formalization must qualify.

### Wrong target

Replace target_formalization with the lexicographically first valid foreign root.

Must reject.

### Current-target counterfactual

First apply the registered update associated with the lexicographically first connected context
for that review/root.

Then attempt the same review still targeting the original root.

Because current_formalization is now the update nanopublication, require:

    RELATION_TARGET_NOT_LIVE

Interpretation:

    exact/current formalization target REQUIRED

History:

    ROOT_ACTION_NO_PRIOR_HISTORY

No claim is made that arbitrary prior history can never affect all possible review systems.

## 6. REPLACE_FORMALIZATION probes

For every D_UPDATE action:

### Valid without prior review history

Apply the update directly from S0.

Require qualification.

This demonstrates that review history is not a precondition for this registered update generator.

### Wrong root

Replace target_root with the lexicographically first valid foreign root.

Require:

    UPDATE_TARGET_UNRESOLVED

### Retraction

Mark the exact update nanopublication retracted before execution.

Require:

    UPDATE_TARGET_RETRACTED

Signature:

    root identity REQUIRED
    update non-retracted status REQUIRED
    prior review history NOT_REQUIRED_IN_REGISTERED_TASK

## 7. RECORD_RESPONSE probes

For every D_RESPONSE context:

### Valid

After exact review + exact update history, response qualifies.

### Review target not live

Attempt response before review.

Require:

    RESPONSE_REVIEW_TARGET_NOT_LIVE

### Update target not current

Attempt after review but before update.

Require:

    RESPONSE_UPDATE_TARGET_NOT_LIVE

### History ablation

After review + update:
- keep live review;
- keep current update/formalization;
- erase transition history only.

Require:

    RESPONSE_TARGET_HISTORY_UNRESOLVED

### Wrong targets

Valid foreign review/update substitutions must reject.

Signature:

    live review target REQUIRED
    current update target REQUIRED
    retained review/update history REQUIRED

## 8. REVISE_PUBLICATION_STATUS probes

For every D_DECISION action:

### Valid

Apply the exact update, then decision.

Require qualification.

### Before update

Attempt decision at S0.

Require:

    DECISION_TARGET_NOT_CURRENT

### History ablation

After the exact update:
- keep current update/formalization unchanged;
- erase history;
- apply decision.

Require qualification.

Thus retained transition history is not a precondition for this registered decision generator.

### Wrong update

Replace target_update_np with a valid foreign-root update.

Require rejection.

Signature:

    current update identity REQUIRED
    retained history NOT_REQUIRED_IN_REGISTERED_TASK

## 9. Decision rule

PASS if every natural action in every denominator satisfies its registered signature probes.

The desired scientific result is heterogeneity:

    qualification signature(RECORD_RESPONSE)
    !=
    qualification signature(REPLACE_FORMALIZATION)
    !=
    qualification signature(REVISE_PUBLICATION_STATUS)

At minimum, history dependence must be localized rather than universal.

## 10. Claim ceiling

If PASS, licensed:

> Qualification requirements are generator-relative in the frozen Formalization Papers task:
> responses require retained review/update history, whereas updates and publication decisions do
> not require that same history once their registered current target conditions are satisfied.

Not licensed:
- universal minimal signatures for all scholarly actions;
- proof that no unregistered history can ever matter;
- a universal action algebra;
- literal prospective confirmation.
