# Paper-Money Warrant Closure Protocol v2

Date frozen: 2026-09-25
Status: SUPERSEDES v1 BEFORE ANY FINAL ADJUDICATION

## Change from v1

The mandatory independent-human gate is removed.

No human participant study is required for this paper.

The closure sequence is now:

\[
\text{Stage A: documentary state}
\rightarrow
\text{Stage B: deterministic active-evidence + archival-trace state}
\rightarrow
\text{Stage C: blinded LLM adjudication (LAST)}
\]

Stage C is deliberately postponed until Stages A-B are completely frozen and audited.

## Frozen claim

**C_PM_MATERIAL_USE**

> Polo's identification of mulberry bark as material used for paper-money is usable as evidence for Yuan paper-money practice under the supplied editorial record.

This is evidential usability under the supplied editorial record, not universal historical truth.

## Stage A - documentary state

Uses:
- paper_money_documentary_reference_v1.csv
- D_* ontology only.

No E_* labels.

## Stage B - active evidence state

Same across conditions:

- evidence universe: frozen V1+V2;
- fixed PM01 + PM02 context;
- H0 background;
- candidate budget = 12;
- same claim;
- same source hashes.

Only the previously frozen navigation policy differs.

### B1 Generic declared-collection retrieval

Authoritative prior result:
PM03 rank = 5835.

Under budget 12:
PM03 absent from active evidence state.

### B2 Sequence-guided domain chain

Authoritative prior result:
candidate count = 12;
PM03 target ordinal = 1.

Under budget 12:
PM03 present in active evidence state.

## Stage B - archival trace exposure

Use only PAGE_VERIFIED trace records from:

data/paper_money_archival_stance_traces_v1.csv

The deterministic comparison asks which explicit historical scholarly stance traces enter each active evidence state.

It does NOT emit E_* relations or a warrant state.

## Stage C - LLM judge (LAST)

Stage C is not executed until:

1. Stage-A ontology/reference validation passes;
2. Stage-B active-event signatures are frozen;
3. archival trace exposure is frozen;
4. anonymous packet construction is frozen;
5. judge prompt/schema and perturbation tests are frozen.

Only then may one or more LLM judges run.

## LLM claim ceiling

The final result may support:

> under a preregistered blinded LLM adjudication protocol, representation/navigation-mediated differences in active evidence can produce different operationalized epistemic-entitlement states.

It may not be described as:
- a human-subject result;
- observed historian behavior;
- universal humanistic judgment.

## Null retention

If all final LLM judges assign the same warrant state to both packets, the null is retained.

No navigation policy, claim, candidate budget, or evidence universe may change after the LLM result is observed.
