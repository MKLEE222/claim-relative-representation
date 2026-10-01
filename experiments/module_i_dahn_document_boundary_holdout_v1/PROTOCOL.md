# Module I v1 — Prospective end-to-end holdout with explicit current-document boundaries

Date frozen: 2026-09-28
Status: PRE-HOLDOUT-SOURCE-INSPECTION PROTOCOL.

## 0. Scientific role

Module H's Paul holdout is scientifically invalid for confirmatory use because the frozen dateline extractor admitted dates from embedded annex documents into the current-document temporal state.

Module I repeats the end-to-end mother-problem test on a still-unopened DAHN correspondence collection with the document-boundary obligation fixed before holdout-body inspection.

Module H's raw output remains preserved and is not reused as confirmation.

## 1. Development versus holdout separation

Development corpora now include:
- Correspondence/Berlin_Intellectuals/Corpus/
- Correspondence/Paul_d_Estournelles_de_Constant/Corpus/

Both are exposed and may be used only to validate generic extraction/evaluation code.

Prospective holdout corpus:

    Correspondence/Nachlassprojekt/StaBi/Correspondence/

Frozen upstream:

    FloChiff/DAHNProject
    commit e7d4a81d42ea10a3d672e5c0869f033a8c2c8149

Pre-protocol exposure to this holdout is limited to:
- repository tree/path counting;
- 465 XML paths under the frozen prefix.

No XML body under the StaBi/Correspondence holdout prefix has been opened before this protocol.

## 2. Root task

> Construct and maintain a source-grounded chronology of the correspondence. When currently visible current-document date carriers do not uniquely warrant a temporal placement, identify the live temporal question, pursue lawful origin evidence, preserve unresolved alternatives, apply only source-compatible updates, ignore unrelated maintenance events, and retain enough history for delayed audit.

No document-specific follow-up question is supplied.

## 3. Current-document boundary

Document identity is part of the source/admissibility contract.

Before extracting any body/dateline date, determine one PRIMARY DOCUMENT CONTAINER.

Generic rule:

1. locate the first body descendant `div` with `type="transcription"`;
2. among its DIRECT child `div` elements with `type="letter"`, choose the first one;
3. if step 2 yields none, choose the first descendant `div type="letter"` that has no ancestor `div type="annex"`;
4. if no such letter container exists, C_DATELINE is unavailable; do NOT fall back to whole-document dateline scanning.

All descendants of `div type="annex"` are excluded from root current-document temporal carriers.

Additional sibling/nested `div type="letter"` objects after the chosen primary container are not root carriers unless a future separately frozen protocol gives them a relation.

Two independent parsers must agree on the selected primary-container identity and extracted current dateline dates.

## 4. t0 root temporal carriers

Visible before discovery:

### C_DOC
All docDate elements under the current document's manuscript description/msContents.

### C_SENT
All date elements under correspAction type="sent".

### C_DATELINE
Only date elements inside opener/dateline elements that are descendants of the PRIMARY DOCUMENT CONTAINER from section 3.

The primary origDate is NOT visible at t0.

## 5. Later origin evidence

OPEN_ORIGIN reveals the canonical primary current-document origDate using the already-developed language rule:
- first history/origin;
- prefer direct language paragraph en, then de, then fr, then first available;
- first origDate inside the chosen paragraph;
- later origDate values in prose are contextual, not current-document root claims.

The operation reveals:
- raw temporal attributes;
- normalized interval;
- exact source locator;
- responsibility/uncertainty attributes if encoded.

## 6. Temporal normalization

Same frozen interval semantics as repaired Module H:
- YYYY
- YYYY-MM
- YYYY-MM-DD
- YYYY/YYYY
- YYYY-MM/MM
- YYYY-MM-DD/DD
- when/when-iso
- notBefore/notAfter and -iso forms
- from/to and -iso forms.

Partial values become closed intervals; open bounds remain open.

Eligibility uses interval compatibility, not raw-string inequality.

## 7. Prospective discovery eligibility

Every holdout XML remains in the denominator.

A document is PRIMARY DISCOVERY eligible only if:
1. it has correspDesc/correspAction;
2. at least two t0 root carriers exist;
3. H-D1 or H-D2 holds.

H-D1:
at least two t0 carrier intervals are disjoint.

H-D2:
at least one t0 carrier is bounded/open/explicitly uncertain and another t0 carrier gives a compatible but non-identical temporal constraint.

origDate cannot trigger eligibility before OPEN_ORIGIN.

## 8. Full trajectory eligibility

A PRIMARY episode enters FULL_TRAJECTORY only if:
1. canonical primary origDate exists behind OPEN_ORIGIN;
2. adding that newly released origin claim changes the contracted root warrant state:

    W_root != W_post_origin

3. a neutral revisionDesc maintenance event exists under the frozen neutral classifier;
4. delayed reuse can query final warrant + alternatives + provenance + update history.

No favorable subset is selected.

## 9. Q0

Q0 remains the edition-facing chronology output:
- sent date(s) if present;
- otherwise canonical primary origDate.

Q0 is used only for current-answer equivalence.

It is NOT the root research warrant.

## 10. Candidate interface R*

R* is unchanged in substance from Module H:
- document/claim identity;
- root temporal values and normalized intervals;
- source/version provenance and locators;
- claim/evidence binding;
- uncertainty and unresolved alternatives;
- opaque lawful OPEN_ORIGIN handle before evidence release;
- appended origin claim after evidence release;
- event applicability/preconditions;
- before/after update ledger;
- unaffected-claim set;
- lawful source handles.

R* never needs to copy all TEI bytes.

## 11. Compared interfaces

I_NATIVE:
full frozen TEI, but staged visibility still applies: origin content is inaccessible until OPEN_ORIGIN.

I_RSTAR:
frozen candidate interface.

I_NO_ALTERNATIVES:
preserve Q0 but remove competing t0 temporal claims/uncertainty needed to notice the live question.

I_NO_BINDING:
preserve temporal values/status but remove role/source binding and target-specific origin handle.

I_NO_HISTORY:
match R* through the relevant update, then discard before-state/event-target transition history before delayed audit.

All arms preserve Q0 at t0.

## 12. Discovery and lawful evidence policy

Deterministic primary policy emits TEMPORAL_WARRANT_QUERY only when the visible interface contains H-D1/H-D2.

Then it may execute OPEN_ORIGIN.

No LLM selects episodes, generates gold, or scores outcomes.

No correspContext prev/next temporal inequality is inferred.

No facsimile OCR is used as primary evidence.

## 13. Warrant contract

Outputs:
- EXACT
- INTERVAL
- OPEN_INTERVAL
- ALTERNATIVE_SET
- UNRESOLVED.

Rules:
1. never emit a point outside all active admissible intervals;
2. a point is warranted only if the active contract uniquely licenses it;
3. preserve disjoint source-supported alternatives unless admissible later evidence excludes them;
4. after OPEN_ORIGIN, primary origDate is an editorial actual-date/supposition carrier and may change the current warrant;
5. other root carriers that remain disjoint from origDate remain live alternatives, not silently discarded;
6. if relation semantics are insufficient, return UNRESOLVED.

This remains a documentary-temporal warrant contract, not independent historical truth.

## 14. Episode horizon

t0: reproduce Q0 and construct W_root from root carriers.

t1: without supplied follow-up, detect live temporal question.

t2: OPEN_ORIGIN releases new source-grounded evidence.

t3: compute W_post_origin and evidence ledger.

t4: selectively record the relevant warrant update; unrelated claims remain stable.

t5: replay one frozen neutral revisionDesc event; temporal warrant must remain stable.

t6: delayed query asks for current warrant, live alternatives, evidence path and transition history.

Same R* persists through the whole episode.

## 15. Neutral event

Neutral revisionDesc event classifier is frozen before holdout:
positive maintenance families include facsimile/IIIF, translation, formatting/encoding, layout, image/illustration, identifier and non-date metadata maintenance.

Any event text mentioning date/dating/chronology/calendar/origDate/docDate is excluded from the neutral class.

revisionDesc is not historical evidence for the chronology.

## 16. Independent implementation checks

Before holdout execution, exposed Berlin + Paul development data must verify:
1. primary-document boundary selection;
2. annex exclusion;
3. t0 root carrier extraction;
4. canonical later origDate extraction;
5. two independent parser implementations agree;
6. Q0 equivalence;
7. evidence is not visible before OPEN_ORIGIN.

Holdout execution may not alter these rules.

## 17. Holdout population and adequacy threshold

Process every XML under the frozen StaBi/Correspondence prefix exactly once.

Report:
- parsed documents;
- parse errors/contract unresolved;
- primary discovery pool;
- full trajectory pool.

Mother-problem adequacy requires FULL_TRAJECTORY_POOL >= 5.

## 18. Positive R* sufficiency gate

For EVERY FULL_TRAJECTORY holdout episode, I_RSTAR must:
1. preserve Q0;
2. identify the unsupplied live temporal question;
3. execute lawful OPEN_ORIGIN;
4. produce exact contracted W_post_origin;
5. record the relevant selective update with zero collateral revision;
6. preserve unresolved alternatives;
7. remain stable under neutral event;
8. satisfy source/version applicability;
9. answer delayed warrant/provenance/history query.

I_NATIVE is a mandatory strong baseline and must also be reported.

## 19. Ablation hypotheses

H1: I_NO_ALTERNATIVES can preserve Q0 yet miss live questions.

H2: I_NO_BINDING can preserve values while failing lawful evidence pursuit/selective application.

H3: I_NO_HISTORY can reach the final warrant yet fail delayed transition audit.

H4: ordinary native reopening may lawfully substitute for some retained information; such nulls reduce the claimed persistence obligation.

## 20. Mother-problem adequacy gate

A-G plus Module I support a bounded substantive empirical answer to reliable + sustained + warranted discovery only if:
1. full trajectory pool >= 5;
2. R* end-to-end passes every full trajectory episode;
3. native baseline also passes or any discrepancy is conservatively resolved against R*;
4. at least one prospective question-emergence ablation witness exists;
5. at least one unresolved/interval/alternative state persists across delay;
6. at least one origin evidence release changes the research warrant;
7. at least one neutral event leaves warrant stable;
8. at least one binding ablation witness exists;
9. at least one history ablation witness exists;
10. no holdout-specific parser/eligibility/representation repair is made after outcomes.

## 21. Claim ceiling

If successful:

> For a prospectively held-out correspondence corpus and frozen temporal-inquiry family, a declared source-grounded information interface can be sufficient to preserve current answers, detect previously unsupplied live documentary questions, acquire later evidence through lawful source access, maintain uncertainty/alternatives, perform selective source-compatible warrant updates, ignore irrelevant maintenance events, and support delayed audit over the declared horizon.

This does NOT establish arbitrary open-ended discovery, universal minimality, human-equivalent question generation, or independent historical truth outside the documentary contract.

## 22. Stop rule

After this protocol:
- do not open holdout bodies until development code is frozen;
- do not change the holdout prefix;
- do not change the primary-document boundary after holdout outcome;
- do not drop episodes;
- do not add episode-specific XPath/source knowledge;
- do not alter R* based on holdout performance;
- do not rerun the same holdout as confirmatory evidence after a scientific validity failure.

If the holdout reveals another contract failure, preserve it and the full mother-problem gate remains unestablished.