# Module R implementation contract v1 — alternative-set canonicalization amendment

Date: 2026-09-29
Status: POST-DEVELOPMENT-BUG / PRE-FRESH CLARIFICATION.

## 1. Trigger

The first source-grounded Yule-Cordier development run:

    36523435267

returned:

    EXPOSED_DEVELOPMENT_PARTIAL

Only YC1920E-0024 failed the exact capability checks.

The source-grounding audit passed.
Oracle and runtime both agreed that the episode was:

    SUBSTANTIVE
    R-U2_ALTERNATIVE_FORMATION

The mismatch was only the serialized order of the two live alternative assertions.

## 2. Cause

IMPLEMENTATION_CONTRACT_v1 froze Psi(ALTERNATIVE_SET) as a:

    canonical sorted set of projected assertions

but did not specify the canonical ordering function.

Independent implementations therefore used two different deterministic orders:

- oracle: canonical JSON serialization of the projected assertion;
- runtime: target/value/status/object tuple.

For synthetic fixtures A/B these happened to agree.
For the real Plane/Cypress values they differed.

Thus:

    set semantics agreed
    serialization order differed

This is an implementation underspecification, not a change to the scholarly state.

## 3. Frozen clarification

For every unordered assertion alternative set in Module R:

1. project each live assertion to exactly:
   - object_id;
   - target_property;
   - value;
   - status;

2. serialize that projected assertion using canonical JSON:

    json.dumps(
        projected_assertion,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":")
    )

3. sort alternatives lexicographically by that canonical serialization.

This rule applies equally to oracle and runtime.

No other Psi semantics change.

## 4. Scientific invariants

This amendment does NOT change:
- object identity;
- target property;
- assertion value;
- assertion status;
- event applicability;
- event operation;
- transition class;
- substantive/null classification;
- evidence/provenance;
- comparator information budgets;
- any historical mapping.

It only makes an unordered mathematical set have one reproducible serialized order.

## 5. Evidence discipline

The original partial run remains part of the audit trail and is not overwritten.

After implementation:
- rerun R-F1-R-F14;
- rerun the fixed five-row exposed historical panel;
- preserve any new discrepancy.

No fresh Module-R candidate, including FRUS, may be opened before this clarification is frozen and
all development gates are rerun.
