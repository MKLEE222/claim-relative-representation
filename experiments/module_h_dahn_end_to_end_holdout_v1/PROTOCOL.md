# Module H v1 — Prospective end-to-end holdout for sustained warranted discovery

Date frozen: 2026-09-28
Status: PRE-HOLDOUT-SOURCE-INSPECTION PROTOCOL.

## 0. Scientific role

Modules A-G establish strong evidence for dynamic researchability, selective revision, information distribution across state/event/access, and one independent correction-project transfer.

The remaining mother-problem burden is:

    reliable
    + sustained
    + warranted
    + discovery

under one unchanged candidate interface over a nontrivial horizon.

Module H is designed as the final end-to-end prospective holdout program, not another local representation-loss example.

## 1. Development versus holdout separation

### Development corpus

DAHN Berlin Intellectuals:

    Correspondence/Berlin_Intellectuals/Corpus/*.xml

was used only to:
- test source feasibility;
- repair date-carrier parsing;
- define the branch grammar;
- define the candidate interface and evaluator.

Berlin is development data and receives no confirmatory status in Module H.

### Prospective holdout corpus

DAHN Paul d'Estournelles de Constant:

    Correspondence/Paul_d_Estournelles_de_Constant/Corpus/*.xml

Frozen upstream repository:

    FloChiff/DAHNProject

Frozen commit:

    e7d4a81d42ea10a3d672e5c0869f033a8c2c8149

Tree inspection before this protocol established only:
- 1,515 XML file paths under the holdout corpus;
- filenames.

No Paul holdout XML body was opened before this protocol freeze.

The same DAHN encoding guidelines apply, but holdout document content remains prospective.

## 2. Mother-problem question tested

Root task:

> Construct and maintain a source-grounded chronology of the correspondence. When the available evidence does not uniquely warrant a document's temporal placement, identify the live temporal question, pursue lawful source evidence, maintain unresolved alternatives when required, and update only the conclusions licensed by later evidence.

No per-document follow-up question is supplied.

The system must identify the live temporal distinction from its available research state.

Discovery here means:

    new-to-the-declared-research-state
    source-grounded question emergence

not novelty to human scholarship.

## 3. Current-document temporal carriers

Eligibility and evaluation use only machine-addressable carriers attached to the current correspondence document.

### C_DOC

All <docDate> elements under the document's manuscript description/msContents.

Multiple disjoint docDate values remain distinct carriers.

### C_ORIG

One canonical primary <origDate> for the current document.

Generic rule:

1. find <history>/<origin>;
2. among direct descendant language paragraphs, prefer:
       xml:lang="en"
       then "de"
       then "fr"
       then first available paragraph;
3. within that paragraph, use only the FIRST <origDate> descendant as the current-document origin-date carrier;
4. later <origDate> elements in the same prose are treated as contextual evidence about other documents/events, not as current-document date carriers.

If <origDate> is directly encoded without multilingual paragraph wrappers, use the first direct current-document origin-date element.

### C_SENT

All <date> elements under:

    <correspAction type="sent">

### C_DATELINE

A manuscript/body date is included only when structurally inside an opener/dateline.

Generic body dates elsewhere are contextual evidence, not root carriers.

## 4. Temporal normalization

Machine-readable date attributes accepted:

- when / when-iso
- notBefore / notAfter
- notBefore-iso / notAfter-iso
- from / to
- from-iso / to-iso

Supported partial/range forms are normalized to closed intervals where finite:
- YYYY
- YYYY-MM
- YYYY-MM-DD
- YYYY/YYYY
- YYYY-MM/MM
- YYYY-MM-DD/DD

Open bounds remain open.

Raw source attributes are preserved alongside normalized intervals.

No natural-language date inference is used to create eligibility.

## 5. Prospective holdout episode eligibility

Every one of the 1,515 XML files is parsed and retained in the denominator.

A document enters the PRIMARY DISCOVERY POOL if:

1. it contains correspDesc with at least one correspAction;
2. at least two current-document temporal carriers are present;
3. one of the following holds:

### H-D1 — incompatible current carriers

At least two current-document temporal intervals are disjoint.

### H-D2 — explicit bounded/uncertain temporal state

At least one current-document carrier has:
- a non-point interval;
- an open bound;
- cert/precision uncertainty;

AND at least one other current-document carrier gives a compatible but non-identical temporal constraint.

No generic note keyword can create eligibility by itself.

## 6. End-to-end trajectory eligibility

A PRIMARY DISCOVERY POOL episode enters the FULL TRAJECTORY POOL if the frozen source additionally exposes all of:

### E1 — lawful explanatory evidence route

At least one source-native route from the disputed document to evidence beyond the root carrier summary, via:
- <history>/<origin> contextual evidence;
- explicit <ref>/<ptr> to another corpus document;
- encoded facsimile/source handle.

### E2 — machine-addressable temporal evidence

The explanatory layer contains at least one machine-readable contextual date constraint, explicit related-document date handle, or other encoded temporal relation relevant to the disputed chronology.

### E3 — later relevant evidence effect

Applying E2 under the frozen inference contract changes the temporal warrant state by at least one of:
- narrowing an interval;
- excluding one alternative;
- replacing an unsupported point with an interval;
- moving a point/interval;
- retaining UNRESOLVED while adding a source-grounded defeater.

"No change" remains a valid result for the PRIMARY DISCOVERY POOL but does not satisfy FULL TRAJECTORY eligibility.

### E4 — irrelevant/null event available

The document has at least one revisionDesc event whose declared scope is unrelated to the temporal warrant, from a frozen neutral class such as:
- facsimile-link maintenance;
- translation of notes;
- formatting/encoding maintenance;
- non-date identifier/layout maintenance.

Date/dating corrections are NOT null events.

### E5 — delayed reuse query possible

After the relevant and null events, the episode still has a later evaluation query requiring:
- current temporal warrant;
- unresolved alternatives if any;
- provenance/evidence path;
- update history.

All FULL TRAJECTORY episodes are included.
No favorable subset is selected.

## 7. Candidate interface R*

R* is frozen before holdout body inspection.

For every active research claim it stores:

### Identity
- document ID/path;
- claim ID;
- relation/evidence IDs where applicable.

### Temporal state
- raw date value;
- normalized interval;
- current role:
  docDate / origDate / sent / dateline / contextual evidence;
- status:
  point / bounded / open / alternative / unresolved.

### Provenance
- exact source file/version;
- source element locator;
- editorial responsibility where encoded;
- source/facsimile handle where encoded.

### Dependencies
- claim -> evidence edges;
- claim -> related-document edges;
- competing/alternative claim edges.

### Unresolved state
- all live temporal alternatives not yet lawfully excluded;
- abstention reason when no unique point is warranted.

### Event/update ledger
For every later evidence or maintenance event:
- event ID;
- source/version;
- target claim(s);
- applicability/precondition;
- before state;
- after state;
- unaffected-claim set.

### Lawful access handles
- origin/history source handle;
- explicit related-document ref/ptr;
- facsimile/source URI where available.

R* does NOT copy every XML byte.
Native source reopening remains a separate baseline.

## 8. Compared interfaces

### I_NATIVE

Full frozen TEI with lawful reopening at every step.

Strong baseline, not a competitor to be beaten.

### I_RSTAR

R* persistent state plus declared lawful access.

This is the positive sufficiency candidate.

### I_NO_ALTERNATIVES

Preserve the same current displayed chronology Q0, document identity and source version.

Remove:
- competing temporal carriers not chosen for Q0;
- bounded/unresolved alternative state;
- uncertainty status that is not required to print Q0.

This tests whether current-output adequacy preserves question emergence.

### I_NO_BINDING

Preserve:
- all temporal values/intervals;
- same uncertainty counts/status;
- same Q0.

Remove:
- carrier role -> source-element binding;
- claim -> evidence/ref binding;
- source locator attached to each competing value.

Generic source reopening is still allowed only if the arm retains a lawful handle capable of identifying what to reopen.

### I_NO_HISTORY

Preserve R* during root discovery/evidence pursuit but do not retain:
- before-state snapshots;
- event target binding after update;
- update ledger.

Current child state remains available.

This specifically tests delayed transition auditability, not initial discovery.

All arms preserve Q0 at t0.

## 9. Q0 current task

Q0 is deliberately narrower than the mother-problem trajectory.

For each document, output the edition's current display-level sent/chronology value(s) available from correspAction sent; if absent, use the primary current-document origDate interval.

Every compared retained-state arm must reproduce Q0 before the episode begins.

Q0 equivalence is necessary to show that later differences are not ordinary current-answer failures.

## 10. Discovery operator

The primary policy is deterministic and representation-agnostic.

It receives only the selected interface, not evaluator truth.

It may emit:

    TEMPORAL_WARRANT_QUERY(
        document_id,
        disputed_claim_ids,
        reason
    )

only when the visible interface contains:
- disjoint current temporal carriers; or
- a bounded/open/uncertain carrier plus another non-identical constraint.

The evaluator freezes this grammar before holdout inspection.

The policy is NOT given the path/name of eligible documents.

### Discovery success

A discovery is correct if:
- it corresponds to a source-grounded H-D1/H-D2 live distinction;
- disputed claim IDs or source-bound referents are maintained;
- the policy does not assert a unique chronology when the interface only licenses a question.

Safe no-question output on ineligible documents is correct.

## 11. Lawful evidence operations

After a valid discovery, the policy may choose any supported source-native route:

### OPEN_ORIGIN
Inspect current document history/origin evidence.

### FOLLOW_REF
Open an explicitly encoded related-document ref/ptr.

### OPEN_RELATED_DATE
After FOLLOW_REF, inspect only that related document's current-document temporal carriers under the same parsing contract.

### OPEN_SOURCE_HANDLE
Resolve an encoded facsimile/source handle to its declared identity/availability.
Module H v1 does not OCR image content as primary evidence.

Equivalent lawful paths receive credit.

The evaluator does not require one author's preferred route.

## 12. Frozen temporal-warrant contract

The primary warranted output is one of:

- EXACT(date)
- INTERVAL([lo, hi])
- OPEN_INTERVAL(...)
- ALTERNATIVE_SET({...})
- UNRESOLVED(reason)

Rules:

1. Never return a point outside every source-grounded admissible interval.
2. A point is warranted only when the active admissible constraints uniquely determine that point under the declared source contract.
3. Intersect compatible constraints when they bear on the same asserted event.
4. Preserve disjoint source-supported alternatives unless an admissible evidence relation excludes one.
5. Contextual evidence can narrow/exclude only when its relation to the current document is explicit in the source.
6. A current editorial correspAction point does not automatically erase a broader source-origin interval.
7. When source relations remain semantically insufficient, output UNRESOLVED rather than guessing.

This is a bounded documentary-temporal inference contract, not a claim of independent historical truth.

## 13. Episode horizon

Every FULL TRAJECTORY episode follows the same horizon.

### t0 — current task
Produce Q0.

### t1 — question emergence
Without a supplied follow-up question, identify any live temporal-warrant distinction.

### t2 — evidence pursuit
Choose and execute lawful source operation(s).

### t3 — warrant state
Produce warranted temporal state and evidence ledger.

### t4 — relevant evidence/update event
Apply the frozen source-grounded evidence effect.
Revise only claims it bears on.

### t5 — irrelevant/null event
Apply one source-native maintenance event from the frozen neutral class.
Temporal warrant must remain unchanged.

### t6 — delayed reuse
Answer:

> What temporal placement is currently warranted for this document, which alternatives remain live, and what source path licenses that state?

The same retained interface is used across all steps.
No episode-specific repair is introduced.

## 14. Selective revision obligations

A correct relevant update must:
- change only the temporal claim(s) licensed by the evidence;
- preserve sender/recipient/place and unrelated document claims;
- retain alternatives not excluded;
- preserve source/version provenance;
- record applicability and before/after state in interfaces that claim transition auditability.

Collateral revision count is explicitly measured.

## 15. Applicability gate

Every evidence/update event must satisfy:

    Applicable(E_t, S_t; K)

before it can change a warrant state.

K includes:
- frozen DAHN commit;
- document identity;
- source-element identity;
- related-document identity;
- temporal normalization contract.

If a source event refers to a state not present in the declared parent, report NOT_APPLICABLE / UNRESOLVED.
Do not force the update.

## 16. Independent evaluation

Primary gold/evaluation uses deterministic source parsing and explicit interval/relation rules.

No LLM serves as:
- episode selector;
- historical gold;
- branch generator;
- outcome scorer.

Implementation checks:

1. two independently implemented current-date extractors;
2. source hash/tree verification;
3. exact related-document target verification;
4. duplicate multilingual metadata audit;
5. episode-level source-contract report;
6. all parse errors retained in denominator.

A later LLM policy may be added only as a secondary behavioral stress test and cannot upgrade the representation claim.

## 17. Prospective holdout population

Every 1,515 Paul corpus XML path is processed once.

Report:
- parseable correspondence documents;
- PRIMARY DISCOVERY POOL size;
- FULL TRAJECTORY POOL size;
- ineligible/null documents;
- contract-unresolved documents.

No minimum pool size is required for execution.

For mother-problem adequacy, a priori feasibility target is:

- at least 5 FULL TRAJECTORY episodes.

If fewer than 5 exist, Module H remains scientifically valid but does not close the empirical mother-problem burden.

## 18. Primary metrics

### Current task
- Q0 exactness.

### Discovery
- eligible live distinction detected;
- false discovery on ineligible documents;
- source-bound disputed referent preserved.

### Evidence pursuit
- lawful route reached;
- evidence source identity correct;
- unsupported route/action rate;
- reopening calls / bytes.

### Warrant
- exact contracted warrant state;
- unjustified point commitment;
- correct UNRESOLVED / ALTERNATIVE_SET;
- evidence/provenance ledger completeness.

### Sustained update
- selective relevant revision;
- collateral revision count;
- unresolved-alternative persistence;
- null-event stability;
- event applicability.

### Delayed reuse
- final warrant exact;
- provenance path exact;
- transition history exact where the interface claims it;
- earlier evidence still reachable/recoverable.

### Cost
- retained payload bytes;
- source reopenings;
- source bytes exposed;
- related-document opens;
- cumulative evidence spans.

## 19. Positive sufficiency criterion

Module H may support a finite positive sufficiency claim only if:

### RSTAR_END_TO_END_PASS

For every FULL TRAJECTORY holdout episode:

I_RSTAR must:
1. preserve Q0;
2. identify the eligible question without it being supplied;
3. reach at least one admissible evidence route;
4. produce the contracted warranted temporal state;
5. perform the relevant selective update with zero collateral revision;
6. preserve unresolved alternatives correctly;
7. ignore the null event with respect to temporal warrant;
8. satisfy applicability;
9. answer the delayed reuse query with complete required provenance.

### Native comparator

I_NATIVE must also be reported.
If native reopening succeeds where R* fails, R* is not sufficient for the declared horizon.

### Nulls

If ordinary source reopening allows a leaner arm to satisfy the same horizon, that is a valid reduction of retained-state obligations.

Do not redefine R* after holdout outcome.

## 20. Pre-registered ablation expectations

These are hypotheses, not required outcomes.

### H1 — question-emergence loss

I_NO_ALTERNATIVES may preserve Q0 while failing to identify some H-D1/H-D2 live questions.

### H2 — evidence-binding loss

I_NO_BINDING may detect that multiple temporal values exist yet fail to pursue or apply evidence selectively.

### H3 — transition-history loss

I_NO_HISTORY may reach the correct final chronology while failing delayed transition audit/provenance.

### H4 — native/reopening null

Some information omitted from retained state may be lawfully recovered by I_NATIVE or explicit source reopening, reducing the necessity of persistence.

## 21. Mother-problem adequacy gate

Current A-G evidence plus Module H is considered empirically sufficient for a bounded substantive answer to:

    reliable and sustained warranted discovery

only if all of the following hold:

1. FULL_TRAJECTORY_POOL >= 5;
2. RSTAR_END_TO_END_PASS holds over every full trajectory episode;
3. at least one prospective holdout episode exhibits genuine question emergence not visible in I_NO_ALTERNATIVES;
4. at least one episode carries an unresolved alternative across at least one later event;
5. at least one relevant evidence event changes/narrows the substantive temporal warrant selectively;
6. at least one null event leaves that warrant stable;
7. delayed reuse succeeds under R*;
8. native baseline does not expose a hidden ordinary route that invalidates the claimed obligation;
9. matched ablations fail only where their removed distinction is required;
10. no holdout-specific parser/representation repair is made after outcome.

Failure of this gate revises the mother-problem answer.
It is not repaired by adding easier corpora.

## 22. Claim ceiling if successful

A successful Module H can support:

> For a prospectively held-out scholarly correspondence corpus and a frozen temporal-inquiry family, a declared source-grounded information interface can be sufficient to preserve current answers, identify previously unsupplied live research questions, pursue lawful evidence, maintain warranted uncertainty, apply selective source-compatible revisions, ignore irrelevant events, and reuse the accumulated evidence state after delay. Sufficiency is relative to the task family, horizon, access operations and source/version contract, not to a universal static record schema.

It cannot establish:
- arbitrary open-ended scientific discovery;
- universal minimal representation;
- independent historical truth of every editorial date;
- human-equivalent question generation;
- sufficiency outside the declared temporal inquiry family and horizon.

## 23. Stop rule

After this protocol commit and before holdout execution:

Allowed:
- implementation fixes needed to instantiate already-declared generic rules, if documented before any scientific outcome is computed.

Not allowed:
- changing Paul holdout to Berlin or another corpus because outcomes are poor;
- dropping eligible episodes;
- adding episode-specific source paths;
- changing R* after holdout performance is known;
- broadening the live-question grammar;
- adding manual historical interpretations to rescue unresolved episodes;
- replacing the frozen DAHN commit;
- promoting a source-contract mismatch into a positive result.

Execute the holdout once after generic implementation verification on Berlin development data.
