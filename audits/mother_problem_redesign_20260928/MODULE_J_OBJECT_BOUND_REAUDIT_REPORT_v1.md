# Module J object-bound exposed-corpus reaudit report v1

Date: 2026-09-28  
Status: COMPLETED DEVELOPMENT REAUDIT AFTER DOCUMENT/OBJECT-BOUNDARY REPAIR. NOT CONFIRMATORY EVIDENCE.

## 1. Purpose

This reaudit was run because Module H and Module I exposed two distinct source-object validity failures:

1. embedded annex dates were previously allowed to contaminate the current-document temporal state;
2. aggregate correspondence bundles with multiple file-level sent dates were previously allowed to masquerade as one scholarly document object.

The repair therefore makes scholarly-object identity a precondition for temporal claim composition.

No new fresh holdout was opened in this reaudit.

## 2. Final frozen object grammar before this run

Module J object boundary is defined by three exposed-development routes:

- Route A: exactly one explicit non-annex letter div;
- Route B: exactly one transcription container that itself functions as the letter object;
- Route C: exactly one untyped body div with correspondence metadata and letter-specific structural markers.

Rejected:
- no identifiable primary object;
- multiple competing primary objects;
- metadata-only/placeholder aggregate objects;
- claims whose object_id differs from the selected primary object.

Object identity is bound to:

    source file
    + source version
    + boundary kind
    + primary boundary signature

## 3. Hardening tests

Authoritative run:

    GitHub Actions 36429428059
    head 38fad4c860e4165fa06a37065ad763ff5c00069a

Inherited F1-F9 all detected:
- annex contamination;
- wrong origin binding;
- wrong warrant;
- collateral mutation;
- dropped live alternative;
- null-event mutation;
- missing history;
- wrong document boundary;
- composite-origin simplification.

Object-bound controls all passed:
- F10 aggregate without primary object rejected;
- F11 multiple primary objects rejected;
- F12 cross-object claim injection detected;
- F13 transcription-as-letter accepted;
- F14 multiple transcription containers rejected;
- F15 untyped body letter accepted;
- F16 placeholder body not accepted as a scholarly object;
- annex exclusion control passed.

Therefore the final run actually tests all requirements frozen through Object Boundary Contract v3.

## 4. Berlin exposed-development reaudit

Population:

- parsed XML: 190
- parse errors: 0
- NO_PRIMARY_DOCUMENT_OBJECT: 8
- SINGLE_PRIMARY_DOCUMENT_OBJECT: 178
- MULTIPLE_PRIMARY_DOCUMENT_OBJECTS: 4
- discovery pool after object gate: 26
- full trajectory pool: 17
- full-trajectory contract unresolved: 0

I_NATIVE:

    17/17 end-to-end exact

I_RSTAR:

    17/17 end-to-end exact

For all 17:
- Q0 exact;
- discovery exact;
- origin applicability exact;
- post-origin warrant exact;
- selective update exact;
- required alternative persistence exact;
- executed null event stable;
- provenance exact;
- delayed transition history exact;
- object contract exact.

Ablations:

I_NO_ALTERNATIVES:
- discovery exact 2/17
- selective update 0/17
- transition history exact 0/17
- end-to-end 0/17

I_NO_BINDING:
- discovery exact 0/17
- applicability exact 0/17
- end-to-end 0/17

I_NO_HISTORY:
- all current-state/update obligations 17/17
- delayed transition history exact 0/17
- end-to-end 0/17

Development mechanism checks:
- RSTAR all full trajectories: YES
- native all full trajectories: YES
- alternatives ablation witness: YES
- binding ablation witness: YES
- history ablation witness: YES

Result SHA-256:

    2446b9bbfa16d825abfb2a0aafb3472badc9bc98edf3ae1466c1d6daf9d673ba

Artifact:
- ID 10972053880
- ZIP SHA-256 570adc2b574d94903e97ec2dd11fb4465c13fd997058258909ef99fa082497de

## 5. Paul exposed-development reaudit

Population:

- parsed XML: 1,515
- parse errors: 0
- SINGLE_PRIMARY_DOCUMENT_OBJECT: 1,515
- discovery pool after object gate: 26
- full trajectory pool: 21
- full-trajectory contract unresolved: 0

I_NATIVE:

    21/21 end-to-end exact

I_RSTAR:

    21/21 end-to-end exact

Ablations:

I_NO_ALTERNATIVES:
- discovery exact 0/21
- selective update 0/21
- transition history exact 0/21
- end-to-end 0/21

I_NO_BINDING:
- discovery exact 0/21
- applicability exact 0/21
- end-to-end 0/21

I_NO_HISTORY:
- all current-state/update obligations 21/21
- delayed transition history exact 0/21
- end-to-end 0/21

Development mechanism checks:
- RSTAR all full trajectories: YES
- native all full trajectories: YES
- alternatives ablation witness: YES
- binding ablation witness: YES
- history ablation witness: YES

Result SHA-256:

    eb717c518f39ca7d630cfd5179e62870f1ba710bc4e2e572904fefa6467e8b39

Artifact:
- ID 10972629341
- ZIP SHA-256 ce943c7a498b231a48f1e472743b891782f6d90baf39a0999027af28fef17cb5

## 6. StaBi exposed reaudit

Population:

- parsed XML: 465
- parse errors: 0
- NO_PRIMARY_DOCUMENT_OBJECT: 465
- SINGLE_PRIMARY_DOCUMENT_OBJECT: 0
- discovery pool after object gate: 0
- full trajectory pool: 0

Therefore:

    no valid Module J discovery episode exists in this StaBi collection
    under the frozen scholarly-object contract.

The seven Module I discovery candidates were individually rechecked.

All seven are:
- present in the source;
- classified NO_PRIMARY_DOCUMENT_OBJECT;
- non-eligible after Module J;
- non-full-trajectory after Module J.

Thus the prior seven candidates are confirmed instrument false positives caused by treating aggregate file-level correspondence metadata as if it belonged to one letter object.

This is a negative scientific result, not an evaluator failure and not a corpus to rescue.

Result SHA-256:

    633fca07250b1ea08a6e1d04a0c572bf23e031bec860e8f3ce999152e6099e87

Artifact:
- ID 10972773919
- ZIP SHA-256 ee021953d6fe1353b5dce020031bb9839fe80d462d8f81fed6402e45c0969290

## 7. Scientific disposition

### Retained

The object-bound repair preserves the previously exposed Berlin/Paul development mechanism:

    alternatives/bindings/history
    carry separable information obligations

under valid single-document objects.

The result is not an artifact of annex mixing or aggregate correspondence metadata in those development corpora.

### Invalidated

Module H remains invalid as confirmatory evidence.

Module I StaBi discovery candidates remain invalid.

The repaired StaBi result is:

    ZERO valid discovery episodes

not a failed 0/x performance result.

### New requirement

A temporal contradiction/uncertainty can enter one warrant state only after the system has established that the participating claims refer to the same scholarly object under the declared source/version contract.

Hence object identity joins the dynamic sufficiency obligation:

    DynamicResearchability(S_t, E_t, A_t, T; K, O)

where O is the scholarly-object identity/boundary contract.

This is a bounded modeling update, not a universal theorem.

## 8. Confirmatory ceiling

This reaudit does NOT establish the mother-problem gate because all three corpora are now exposed development material.

What it does establish is stronger methodological discipline:

1. the previous false positives are reproducibly removed;
2. valid exposed development trajectories survive the stricter object contract;
3. the required ablation separations survive;
4. the repaired evaluator rejects the entire exposed StaBi collection rather than manufacturing usable episodes.

A future confirmatory holdout must use the frozen Route A/B/C object grammar and may not add a new Route D after source inspection.
