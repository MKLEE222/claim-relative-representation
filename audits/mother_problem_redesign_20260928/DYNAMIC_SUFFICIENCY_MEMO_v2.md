# Dynamic sufficiency memo v2 — after Module E

Date: 2026-09-28  
Status: THEORY-DESIGN UPDATE FROM EXECUTED DEVELOPMENT EVIDENCE. NOT A NEW THEOREM.

## 1. Static sufficiency is no longer the right primary object

The earlier bounded formulation asked whether a retained representation preserves enough information for a declared inquiry.

Modules D1/D2/E show that sustained inquiry is different.

At revision step t -> t+1, the decision-relevant information is distributed across:

    S_t = retained state
    E_t = incoming correction / revision / evidence channel
    A_t = lawful source access
    T   = continuation task

The appropriate bounded object is therefore:

    DynamicResearchability(S_t, E_t, A_t, T)

rather than a property of S_t alone.

## 2. Two dynamic tasks must remain distinct

Module E empirically separates:

### Terminal-state reconstruction

Can the system determine the exact revised child state?

### Transition audit

Can the system determine which relations changed, which were added/removed, and what their prior statuses were?

These are not equivalent.

Observed D2 witness:

    S_ENDPOINTS + E_LINK_NEW + A_CHILD_REOPEN

gives:

    child state exact = 113/113
    transition exact = 105/113

The missing eight cases are the eight removed relations.
The child source cannot reveal the old certainty of an object no longer present.

Therefore:

    revised-state recoverability
    !=
    revision-history auditability.

## 3. State/event duality

D1/D2 previously showed:

    coarse parent state + identity-rich event
    can be sufficient.

Module E adds the converse:

    full parent state + identity-free event
    can be insufficient.

D1:

    full parent state
    + one high->low operation at pr323
    + no relation identity
    -> 2 admissible revisions

D2:

    full parent state
    + correct per-locus operation bags
    + no operation-to-relation binding
    -> only 78/113 affected loci determined

The other 35 loci remain ambiguous.

Thus identity binding may be carried on either side of the interaction:

    state binding
    or event binding

but if neither side carries the required distinction and source access does not restore it, the update is non-determining.

## 4. Aggregate equality is not binding equality

D2's weak event channel preserves:
- affected locus identity;
- number and direction of certainty changes;
- certainty multiset of additions/removals.

Yet 35 affected loci remain ambiguous.

Of these:
- 30 are certainty-only revision loci;
- 3 topology-only;
- 2 combined.

At l1780:

    exact parent state known
    eight low->high operations known

but removal of operation-to-relation binding yields:

    1,287 compatible revisions.

Therefore:

    same operation multiset
    !=
    same warranted revision.

This is the dynamic analogue of the earlier proposition-binding separations.

## 5. Delta knowledge is not background-state knowledge

Another D2 witness:

    S_ENDPOINTS + E_LINK_FULL + A_NONE

gives:

    exact transition = 113/113
    exact affected child state = 77/113

The event packet can say exactly what changed while unchanged relation certainties remain unknown because they were not retained in S_t.

Thus:

    exact delta
    !=
    exact resulting epistemic state

unless persistent background state is also available.

## 6. Source access is a substitute, not magic

Child-source reopening repairs every terminal-state failure in the Module E matrix.

But it does not universally repair transition history.

A source at t+1 cannot by itself recover a status that disappeared at t.

This gives a temporal carrier principle:

> Information may be delegated to future lawful source access only if the future source still exposes the distinction required by the later task.

If the distinction is destroyed by deletion or replacement, it must survive elsewhere:
- retained state;
- event history;
- versioned source access;
- or another lawful carrier.

## 7. Revised determinacy criterion

For admissible histories h in H, define the available interface at decision time:

    I_T(h) = (S_t(h), E_t(h), Obs_A(h))

where Obs_A is the information lawfully obtainable under the declared access contract.

Dynamic sufficiency for task T requires:

    I_T(h1) = I_T(h2)
    =>
    W_T(h1) = W_T(h2)

The research program should now search for finite separation witnesses over this whole interface, not demand that S_t alone be maximally rich.

## 8. Distributed information obligation

A better carrier statement is:

> Every distinction required for a warranted continuation must be available at decision time from the retained state, incoming evidence/event channel, lawful source access, or an explicitly declared composition of them.

This formulation permits nonredundant systems.

It also makes failure conditions clearer:

    missing in state
    AND missing in event
    AND unrecoverable from lawful access
    =>
    task-relative dynamic non-determinacy.

## 9. Connection to prior modules

### A/B — continuation

Current local answer can be preserved while source-triggered follow-up differs.

### B2 — evidence selection

Current endpoints and global uncertainty profile can be preserved while endpoint-specific next-evidence targets differ.

### C — delayed source dependence

Stable symbolic relations can have time-varying source executability.

### D1/D2 — natural selective revision

Real editorial epistemic and topology revisions can be applied selectively without collateral rewriting.

### E — information allocation

The information obligation can move between state, event channel, and source access; terminal-state reconstruction and transition audit are distinct tasks.

This sequence now addresses a materially larger portion of:

    reliable + sustained + warranted discovery

than the original static representation experiments.

## 10. What is still missing

The main remaining weakness is domain concentration.

A-E now contain strong mechanism evidence, but D/E are still inside the already-exposed Whitman ecology.

The next transfer should therefore test the interaction-level claim on a qualitatively different revision object without altering D/E.

The source-verified Urumtsi 1903 -> 1920 erratum is a suitable pressure test:

    found -> founded

because:
- it is an explicit historical correction;
- it changes a substantive action description;
- the correction target is source-grounded;
- unaffected neighboring propositions can serve as stability controls;
- its event channel is an authored erratum, not a Git diff.

This transfer would test whether the state/event/access decomposition survives a different scholarly revision mechanism.

## 11. Claim discipline

Current development evidence supports:

    dynamic sufficiency is interface-relative and task-relative.

It does not yet support:

    a universal minimal carrier,
    a universal update algorithm,
    independent cross-domain replication,
    or historian consensus.

The manuscript should not be upgraded beyond those bounds until the transfer layer is executed.
