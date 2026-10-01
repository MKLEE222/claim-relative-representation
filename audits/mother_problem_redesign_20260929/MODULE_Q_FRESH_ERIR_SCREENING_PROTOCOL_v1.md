# Module Q — fresh ERIR ecology screening protocol v1

Date frozen: 2026-09-29
Status: PRE-CANDIDATE / PRE-CONTENT SCREENING.

## 1. Purpose

Module P has source-audited exposed development evidence for:

    evidence-release-induced scholarly revision (ERIR)

The next empirical burden is prospective confirmation in an independent, unexposed humanities
ecology.

Module Q selects that ecology without inspecting episode-level outcome content.

The goal is NOT to find a corpus known to contain positive revisions.
The goal is to choose a project in which the ERIR task is prospectively well-defined and
scientifically applicable in principle.

## 2. Freshness rule

Before a project can become the Module-Q holdout candidate, only the following may be inspected:

- repository/project metadata;
- README and project documentation;
- ODD/RNG/XSD/schema/customization files;
- generic XSLT/XQuery/templates;
- repository tree/path metadata;
- generic encoding guidelines;
- closed register/file counts.

Forbidden before population freeze:

- episode TEI/XML files;
- rendered episode pages containing concrete evidence values;
- specific date disagreements;
- specific attribution/correction outcomes;
- searches for "interesting", "uncertain", "wrong", "corrected", or otherwise favorable episodes;
- any empirical estimate of ERIR-positive prevalence.

If a search result exposes concrete episode content/evidence values, mark the project:

    EXPOSED_DURING_SCREENING

and never use it as a fresh holdout.

## 3. Independence gate

A candidate must satisfy all:

1. not FloChiff/DAHNProject or a DAHN subcollection;
2. not Auden-Musulin-Papers/amp-data;
3. not any project already exposed at episode level during prior screening;
4. not used to design P-F1-P-F10, Phi, ERIR eligibility, or transition classes;
5. no existing episode-level result for the project in this repository.

Failure is terminal for fresh confirmation.

## 4. Closed population gate

Pre-content project/tree metadata must establish a complete deterministic population.

Preferred form:

    one dedicated correspondence/edition path
    + all XML/TEI files in that path
    + no result-dependent subset

Preferred N:

    >= 40 scholarly objects

A smaller closed population can pass only if project documentation establishes a complete
edition/register and there is no discretionary selection.

The population rule must be frozen before content opening.

## 5. Scholarly-object gate

Project-level documentation/schema must prospectively establish a repeatable scholarly-object
unit compatible with a frozen object contract.

Preferred:
- one edition file per letter/document;
- explicit div type="letter" or another project-native object boundary that can be mapped
  prospectively and generically.

If the existing portable A/B/C grammar directly applies, use it unchanged.

If the project uses a genuinely different generic object serialization, a portable object
adapter may be developed ONLY:
- from project-level schema/documentation;
- before any episode opening;
- with independent oracle/runtime implementation;
- with synthetic false-positive controls;
- with full exposed regression on existing development corpora.

No outcome-specific first-object fallback is allowed.

## 6. Initial/current claim-layer gate

Project-level schema/documentation must establish at least one machine-addressable layer
representing the current/pre-event scholarly state for the declared task.

For the temporal ERIR confirmation this can include:
- sent/correspondence date;
- document/dateline date;
- manuscript current date;
- another project-native present-state temporal claim.

The gate establishes only existence of the carrier family.
It must not inspect whether any particular episode differs from later evidence.

## 7. Independent later-evidence/revision-layer gate

This is the crucial Module-Q gate.

Before episode opening, project-level documentation/schema must establish an independently
represented later/evidential layer that is NOT merely another serialization of the current
claim.

Acceptable examples:
- editorial/origin dating distinguished from sent/document dating;
- explicit source-history/origin evidence;
- revision/correction record tied to a scholarly claim;
- source reclassification or attribution evidence layer;
- documented editorial conjecture/identification distinct from current literal carrier.

For the next temporal Regime-B holdout, the simplest acceptable structure is:

    current temporal carrier family
    +
    independently encoded editorial/origin evidence family

No actual disagreement is required or inspected at screening time.

A project with only one temporal/evidential carrier family is rejected.

## 8. Evidence-release semantics gate

Project documentation must support a prospective staged-access interpretation:

    S0 = current/root layer
    E  = later/evidential layer released under the study workflow
    S1 = source-grounded updated warrant

The evidence layer may coexist in the frozen source file physically.
The study is about declared research-entry state and lawful evidence release, not file creation
chronology.

However the two layers must have distinct scholarly semantics documented before opening.

Do not invent "later evidence" merely because two XML elements exist.

## 9. Provenance/source-audit gate

The project must expose enough generic provenance for later source audit:
- stable file/object identifier;
- manuscript/archive/repository identifier and/or facsimile pointer;
- source locator;
- editorial responsibility/evidence context where available.

A computational result without a feasible source audit cannot be the next confirmatory study.

## 10. Engine portability gate

Before opening the selected candidate, inspect only project-level schemas to ensure:
- declared temporal/evidence lexical forms are parseable;
- object grammar is prospectively compatible;
- source identity is portable;
- no candidate-specific outcome rule is needed.

Any generic portability repair must be:
1. frozen before episode opening;
2. implemented independently in oracle/runtime;
3. synthetic-tested;
4. regression-tested on all exposed development corpora;
5. shown not to change prior scientific classifications except for separately documented
   generic parser coverage.

## 11. Candidate scoring is prohibited

Do not rank candidates by estimated probability of a positive result.

Candidate choice is deterministic among hard-gate passers using only pre-content metadata:

1. strongest explicit separation of current vs later-evidence semantics;
2. direct compatibility with already frozen object/applicability contract;
3. closed one-object-per-file population;
4. stronger provenance/source-audit documentation;
5. larger closed population;
6. canonical repository full name as final lexical tie-break.

This is a selection rule, not a scientific performance score.

## 12. Screening ledger

Every seriously considered project must be recorded with:
- project/repository;
- documentation/schema commit/version;
- freshness status;
- closed population evidence;
- object gate;
- current-claim gate;
- later-evidence gate;
- provenance gate;
- engine portability issues;
- first failed hard gate.

Rejected and accidentally exposed candidates remain in the ledger.

## 13. Holdout freeze requirements

Before opening the chosen project:

1. freeze upstream repository/version/commit;
2. freeze complete population path/register and expected N;
3. freeze source context;
4. freeze object adapter if any;
5. freeze Phi and ERIR eligibility unchanged from Module P unless a new version is explicitly
   justified before opening;
6. freeze event-release rule;
7. freeze primary capabilities P1-P7;
8. freeze Module-M comparator budgets;
9. freeze a small obligation-intervention subset;
10. freeze documentary audit;
11. freeze PASS / BOUNDED_PARTIAL / NULL_APPLICABILITY / INVALID classifications;
12. run all inherited hardening gates;
13. only then open the population once.

## 14. Prospective outcome classes

### INVALID
Protocol/integrity/source accounting failure.

### NULL_APPLICABILITY
No valid ERIR-eligible events under the frozen task.

This remains scientifically informative and cannot trigger rescue.

### BOUNDED_PARTIAL
Some eligible events exist but denominator/source audit/capability conditions are insufficient
for the registered pass.

### COMPUTATIONAL_PASS_PENDING_SOURCE_AUDIT
Predeclared minimum eligible denominator and all computational gates pass.

### PASS
Computational gate plus deterministic source audit pass.

Exact minimum N and audit rule must be frozen in the holdout-specific protocol before opening.

## 15. Claim ceiling

Even a fresh PASS establishes only one prospective independent ERIR ecology.

It does not establish:
- prevalence;
- universal necessity;
- non-temporal event-family generality.

The second non-temporal humanities event family remains a separate required study.
