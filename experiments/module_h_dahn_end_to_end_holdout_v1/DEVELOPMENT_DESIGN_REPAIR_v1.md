# Module H development design repair v1 — separate discovery state from later origin evidence

Date: 2026-09-28
Status: PRE-HOLDOUT SCIENTIFIC DESIGN REPAIR AFTER BERLIN DEVELOPMENT VERIFICATION.

## 1. Development result that exposed the problem

Berlin development run:
- GitHub Actions run 36393462158
- 190 parsed documents
- 46 primary/full-trajectory episodes under the first implementation
- I_NATIVE and I_RSTAR passed 46/46

This apparent pass is NOT accepted as evidence for the mother problem.

Audit found that the implementation placed the canonical current-document `origDate` in the visible retained state at t0 and then counted OPEN_ORIGIN as evidence pursuit without releasing any new temporal information.

Therefore:

    t0 state already contained the evidence
    later OPEN_ORIGIN only proved that a handle existed

and the observed Q0 -> warrant change was largely a reevaluation of already visible information, not:

    question emergence -> new evidence -> warranted update.

This violates the intended E2/E3 separation in PROTOCOL.md.

Paul d'Estournelles de Constant holdout XML bodies have still NOT been opened.

## 2. Source-guideline basis for the repair

DAHN's public correspondence guidelines explicitly distinguish:

- `docDate`: date actually written on the manuscript;
- `origDate`: actual date of creation as identified by the editors, which may be a supposition;
- `correspAction type="sent"/date`: correspondence metadata used in profileDesc/CMIF.

The guideline also states that the actual date of creation may differ from a date written on the manuscript.

This provides a source-native staged evidence design without inventing a new temporal relation.

## 3. Repaired evidence-release schedule

### t0 visible temporal state

Only root/current-document carriers are visible:

- C_DOC: manuscript `docDate`;
- C_SENT: `correspAction type="sent"/date`;
- C_DATELINE: opener/dateline date.

The canonical primary `origDate` is NOT visible as a temporal claim at t0.

R* may retain a lawful opaque OPEN_ORIGIN handle identifying that history/origin evidence exists, but it may not contain the origin date value before the operation is executed.

### t1 question emergence

Eligibility and discovery are computed ONLY from the t0 carriers above.

A live question exists when:
- root carriers are disjoint; or
- one root carrier is bounded/open/uncertain and another gives a compatible but non-identical constraint.

No `origDate` value can trigger the question before OPEN_ORIGIN.

### t2 evidence pursuit

OPEN_ORIGIN lawfully reveals:
- the canonical primary current-document `origDate`;
- its raw TEI attributes;
- source locator;
- editorial responsibility if encoded;
- origin source identity.

### t3 warranted state

The primary origin-date evidence is now added to the research state.

The temporal-warrant contract evaluates the updated claim set.

A FULL_TRAJECTORY episode requires that this newly released origin evidence changes the warranted temporal state relative to the t0/Q0 state.

Thus E3 is no longer satisfied by merely reevaluating already-visible claims.

## 4. Full-trajectory eligibility repair

An episode enters FULL_TRAJECTORY only if all are true:

1. H-D1/H-D2 is triggered using t0 root carriers only;
2. a canonical primary `origDate` exists behind OPEN_ORIGIN;
3. adding that origin evidence changes the contracted warrant state;
4. a frozen neutral revisionDesc event exists;
5. delayed reuse can query the post-origin state and update history.

The previous Berlin 46/46 full-trajectory count is retired as an implementation-development result.

## 5. Interface repair

### I_RSTAR

At t0 retains:
- root temporal claims;
- identities/bindings/provenance for those root claims;
- opaque lawful OPEN_ORIGIN handle;
- unresolved alternatives from root claims;
- update ledger structure.

After OPEN_ORIGIN, the new origin claim is appended with full provenance.

### I_NATIVE

Same staged visibility contract:
the policy cannot inspect origin date contents until OPEN_ORIGIN is called, even though the full native TEI is lawfully reopenable.

This prevents I_NATIVE from receiving hidden future evidence for free.

### I_NO_ALTERNATIVES

Preserves Q0 and its source identity but removes competing root temporal claims needed to identify the live question.

It may retain an origin handle only if that handle is ordinarily available independently of the removed alternative claims; it cannot open it before a valid question is formed.

### I_NO_BINDING

Preserves root temporal values and aggregate status but removes claim-role/source binding and the target-specific OPEN_ORIGIN binding.

### I_NO_HISTORY

Matches R* through t4 but drops before-state/update-target history before delayed reuse.

## 6. No use of correspContext chronology

Although DAHN labels correspContext refs as previous/following letters, Module H v1 does NOT infer temporal inequalities from prev/next.

Those links may be retained as source navigation metadata but do not license chronological narrowing in the primary evaluator.

This avoids importing an unstated chronological semantics.

## 7. Holdout integrity

This repair is allowed because:
- it was caused by a Berlin development design leak;
- no Paul holdout XML body has been opened;
- no Paul outcome exists;
- the holdout corpus, source commit, root task, R* family, and mother-problem gate remain unchanged.

The repaired implementation must be rerun on Berlin.

Only after it passes implementation checks may the exact frozen evaluator be executed once on Paul.
