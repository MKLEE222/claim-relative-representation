# Module O — AMP fresh independent dynamic holdout v1

Date frozen: 2026-09-29
Status: PRE-OPENING PREREGISTRATION. NO AMP EDITION XML HAS BEEN OPENED.

## 1. Scientific purpose

Module O is the first post-portability fresh independent holdout designed to fill the still-open
empirical cell:

    fresh independent eligible scholarly objects
    -> prospective dynamic trajectories
    -> source-audited result

It tests whether the portable object/claim mechanism survives outside the DAHN ecology.

It is not a corpus search for a positive result.
PASS, BOUNDED_PARTIAL, NULL_APPLICABILITY and INVALID are all retained outcomes.

## 2. Frozen upstream population

Repository:

    Auden-Musulin-Papers/amp-data

Frozen commit:

    289a52de61aef0b6354e3c8298173bf1f889feb2

Frozen population prefix:

    data/editions/

Population rule:

    ALL *.xml files directly under data/editions/

Pre-opening repository metadata shows:

    73 XML files
    0 subdirectories

Expected population:

    73

No filename/date/person/content-based subset selection is permitted.

## 3. Freshness record

Before this freeze:

Allowed material inspected:
- repository metadata;
- README/project documentation;
- framework/auden-musulin/schema/schema.odd;
- repository tree/path metadata and file counts.

Forbidden episode material not inspected:
- no file under data/editions/*.xml was fetched/opened;
- no episode date value was read;
- no object status was observed;
- no D1/D2 eligibility was observed;
- no origin/sent/dateline disagreement was observed;
- no trajectory outcome was observed.

The AMP population is therefore fresh at freeze time.

## 4. Why AMP was selected before opening

The project-specific ODD prospectively establishes all of the following.

### Object ecology

- the customization is explicitly for AMP correspondence;
- body contains a transcription wrapper;
- project-native div type="letter" objects are allowed/required within the transcription;
- letter/message/opener/closer/dateline structures are project-native;
- envelope/enclosure structures are separately typed.

The frozen portable object grammar remains unchanged.
No first-letter fallback is permitted.

Files with:
- no valid primary object;
- multiple competing primary objects;
- placeholder status;
- only embedded/enclosure objects

remain legitimate applicability exclusions.

### Correspondence carrier

The project ODD requires correspDesc to contain at least one correspAction.
correspAction/@type is required and closed over:

    sent
    transmitted
    redirected
    received

correspAction/date is part of the project schema.

### Independent later/origin evidence carrier

The project ODD includes:

    msDesc/history/origin/origDate

and requires origDate to carry:

    notBefore-iso
    notAfter-iso

Thus a separate origin/history temporal carrier is prospectively available in the project
encoding ecology.

### Source/provenance structure

The project encodes manuscript description / repository / collection / identifier provenance
sufficient for later source audit.

## 5. ISO datetime portability repair

Project-level schema inspection revealed, before any AMP episode opening, that AMP uses ISO
datetime lexical forms in *-iso temporal attributes.

This triggered the frozen generic portability amendment:

    PORTABLE_OBJECT_CLAIM_CONTRACT_v1_ISO_DATETIME_AMENDMENT.md

The amendment:
- did not alter object grammar;
- did not alter eligibility;
- did not alter warrant logic;
- did not alter event logic;
- did not alter comparator budgets;
- did not alter obligation definitions.

Mandatory pre-fresh controls F31-F36 now pass.

At current pre-opening HEAD, the full pre-fresh gate passes:
- F1-F9;
- F10-F16;
- F17-F30;
- F31-F36;
- inherited I/J obligations;
- Berlin/Paul/StaBi exposed regression;
- Module M synthetic comparator gate;
- Module N synthetic obligation crossover gate.

The ISO repair did not change exposed portable counts:
- Berlin: discovery 38, full 29;
- Paul: discovery 38, full 33;
- StaBi: discovery 0, full 0.

## 6. Frozen engine family

The holdout uses the current portable Module-L oracle/runtime/evaluator contract exactly as
frozen before AMP opening.

Scientific logic that may not change after opening:
- object Routes A/B/C and embedded/enclosure exclusions;
- source-context binding;
- claim applicability classes;
- temporal carrier parsing including the frozen ISO amendment;
- D1/D2 eligibility;
- q0;
- root/post warrant construction;
- full-trajectory eligibility;
- transition execution;
- null-event semantics;
- delayed-history audit.

Any later bug repair creates a future study version.
It cannot replace the authoritative Module O result.

## 7. Source context

Every parsed AMP document is bound to:

    source_repository = Auden-Musulin-Papers/amp-data
    source_version = 289a52de61aef0b6354e3c8298173bf1f889feb2
    population_scope = MODULE_O_AMP_FRESH_HOLDOUT_V1

No DAHN source identity is inherited.

## 8. Complete population accounting

For all 73 frozen XML files, preserve:

- path;
- raw SHA-256;
- parse success/error;
- object-contract status;
- boundary kind;
- source context;
- oracle/runtime contract status.

Required accounting:

    parsed_documents + parse_errors = 73

If not, Module O = INVALID.

Report separately:
- total XML;
- single primary objects;
- no primary objects;
- multiple primary objects;
- discovery pool;
- full trajectory pool.

A zero eligible/full population is an applicability result, not 0/73 performance.

## 9. Primary prospective mechanism gate

Let N_full be the number of full_trajectory_eligible episodes under the frozen engine.

### INVALID

Any of:
- F1-F36 or inherited pre-fresh gate fails at the opening commit;
- AMP population accounting is incomplete;
- oracle/runtime source contract is unresolved on any full trajectory;
- the frozen upstream commit/prefix is not the one declared above;
- execution integrity prevents complete result preservation.

### NULL_APPLICABILITY

    N_full = 0

Interpretation:
the frozen AMP population supplies no full trajectory under the declared contract.
This is not model/evaluator failure.

### BOUNDED_PARTIAL

Any of:
- 1 <= N_full < 5;
- unresolved documentary interpretation in the deterministic source audit;
- N_full >= 5 but the primary prospective capability conditions are not all met.

### COMPUTATIONAL_PASS_PENDING_SOURCE_AUDIT

All of:

1. N_full >= 5;
2. portable retained interface passes the complete registered dynamic task for every full
   trajectory;
3. no full trajectory has unresolved oracle/runtime contract;
4. current/latest reopening comparator recovers T1/T2 on every full trajectory;
5. ordered-snapshot comparator recovers T1/T2/T3 on every full trajectory;
6. retained interface recovers T1-T5 on every full trajectory.

The final scientific PASS additionally requires the documentary audit in section 12.

## 10. Fresh comparator subset

The frozen Module-M information budgets are reused without modification.

For every full trajectory report:

RSTAR:
- T1 CURRENT_STATE
- T2 CURRENT_PROVENANCE
- T3 STATE_DELTA
- T4 TRANSITION_ATTRIBUTION
- T5 DELAYED_HISTORY

B_CURRENT_REOPEN:
- T1/T2 are required positive capabilities.

B_ORDERED_SNAPSHOTS:
- T1/T2/T3 are required positive capabilities.

T4/T5 outcomes for the comparators are recorded exactly as observed.
Do not force them to fail in the Module-O classification.
If a comparator unexpectedly determines T4/T5 under the frozen budget, retain that result and
weaken the history-separation claim.

## 11. Fresh obligation subset

To avoid overloading the fresh holdout with every development intervention, Module O preregisters
only four high-load-bearing contrasts from Module N:

A. O6 ProvenancePreservation
    N_NO_CURRENT_PROVENANCE

B. O7 TransitionCompatibility
    N_NO_TRANSITION_BINDING

C. O8 HistoryRetention
    N_NO_HISTORY

D. O4 ResultDeterminacy
    N_COLLAPSE_RESULT_STATUS, only where the correct post-event warrant is non-exact /
    alternative / interval / unresolved.

Report the same C1-C8 capability vector.

These fresh intervention results are secondary mechanism evidence.
They do not replace the primary retained-interface gate.

## 12. Deterministic documentary source audit

A computational result is not final PASS without source inspection after the one-shot run.

Audit set:
- if N_full <= 12: audit all full trajectories;
- if N_full > 12: audit 12 deterministic cases.

For N_full > 12, select:
1. one case from each observed non-empty warrant-after type, ordered by path hash;
2. one case from each observed object boundary kind, ordered by path hash;
3. fill remaining slots by ascending SHA-256(path), without duplicates.

The audit must verify from AMP source XML:
- selected primary object is real under frozen grammar;
- the active sent/dateline/root carriers belong to the selected object/source context;
- origDate is genuinely the independent origin/history carrier represented by the parser;
- no envelope/enclosure/embedded material was misbound;
- source repository/version/file/locator provenance is faithful;
- the registered D1/D2 trigger is source-present;
- the root and post-event warrant interpretation matches the encoded evidence.

Any failed audit item yields BOUNDED_PARTIAL.
Do not repair Module O after seeing audit failures.

## 13. One-run authority

The first completed preregistered Module-O workflow that opens AMP edition XML is authoritative.

Any later:
- rerun;
- threshold change;
- parser change;
- object-rule change;
- source-subset change;
- metric change

is diagnostic/future work only and cannot replace the first result.

## 14. Required artifacts

Preserve:

- protocol commit;
- opening commit;
- workflow run ID;
- upstream repo/commit/prefix;
- archive SHA-256;
- complete population manifest;
- parse-error manifest;
- object-status manifest;
- oracle/runtime contract manifest;
- full eligible trajectory results;
- Module-M comparator T1-T5 results;
- preregistered Module-N subset capability vectors;
- deterministic documentary-audit manifest;
- result JSON SHA-256;
- audit manifest SHA-256;
- workflow artifact digest.

## 15. Interpretation ceiling

A positive Module-O result licenses only a bounded claim that the frozen portable scholarly
researchability mechanism transferred prospectively to one independent AMP correspondence
ecology.

It does not establish:
- universal DH necessity;
- prevalence across digital editions;
- cross-event-family generality;
- that every project needs the same serialization.

A NULL/BOUNDED_PARTIAL result is retained and does not trigger corpus rescue.

The next major empirical gap after Module O remains the second non-temporal humanities event
family.
