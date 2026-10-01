# Module L — independent ecology candidate screening protocol v1

Date frozen: 2026-09-28
Status: PRE-CONTENT SCREENING PROTOCOL. NO NEW CANDIDATE EPISODE XML MAY BE OPENED DURING THIS STAGE.

## 1. Purpose

Module K produced a legitimate fresh NULL_APPLICABILITY result because all 83 GeStA XML files fell outside the frozen Module J scholarly-object grammar.

The next empirical objective is to fill the still-open cell:

    fresh eligible scholarly objects
    -> prospective dynamic trajectories
    -> independent confirmatory evidence

without weakening the object-boundary protections established in Modules J/K.

This screening stage selects a genuinely independent correspondence ecology using only project-level metadata, repository trees, README/documentation, schema/ODD/RNG/XSD files, XSLT templates, and other generic encoding documentation.

It is forbidden to inspect candidate episode XML/TEI bodies, date values, D1/D2 outcomes, or trajectory outcomes before a final holdout population is frozen.

## 2. Independence gate

A candidate project is eligible for Module L screening only if all are true:

1. It is not FloChiff/DAHNProject and is not a DAHN subcollection.
2. It did not participate in Modules A-K design, debugging, threshold selection, or object-boundary repair.
3. The claim-relative-representation repository contains no prior episode-level result for that project.
4. Candidate discovery uses only public project-level documentation and repository metadata.

A project that fails this gate is not a fresh confirmatory candidate.

## 3. Frozen object-compatibility requirement

Module J Routes A/B/C remain unchanged.

A candidate must be demonstrably compatible from generic project documentation/schema alone.

Strongest acceptable evidence:
- project schema, ODD, conversion rule, or generic template requires/produces exactly one non-annex div type="letter" per episode file (Route A).

Also acceptable:
- project-generic schema/template establishes one transcription-as-letter object satisfying frozen Route B;
- project-generic schema/template establishes one untyped body div plus frozen Route C letter-structural markers and correspondence metadata.

Not acceptable:
- inferring objecthood from filenames alone;
- opening episode files to see whether they happen to fit;
- proposing a Route D;
- selecting only the files that fit after content inspection.

If generic documentation cannot establish compatibility prospectively, reject the project for the next confirmatory run.

## 4. Temporal-carrier feasibility gate

Before episode opening, project-level documentation/schema must establish at least two independently represented temporal/evidential carrier families that could in principle support D1/D2 adjudication, such as:

- visible/document date versus correspondence sent date;
- source/manuscript date versus editorial/origin date;
- exact date versus notBefore/notAfter/from/to/approximate/uncertain date;
- postmark or archival source date versus editorial date;
- explicit generic dating note / certainty / evidence attribute tied to the same correspondence object.

This gate establishes only possibility. No actual disagreement or uncertainty episode may be inspected before holdout freeze.

A project with only one documented date carrier family is rejected as a dynamic-confirmation candidate.

## 5. Population feasibility gate

Repository-tree metadata must support a closed population rule before opening episode content.

Preferred:
- one repository path dedicated to correspondence episode XML;
- at least 50 XML episode files.

A smaller population may pass only if project documentation gives a complete closed register and there is no content-based subset selection.

All XML under the frozen population prefix/register must be included. No favorable subset may be chosen after opening.

## 6. Provenance/source audit gate

Generic project documentation must expose enough source/provenance structure for a later deterministic documentary audit, for example:
- facsimile/source identifiers;
- manuscript/archive references;
- responsibility metadata;
- stable edition identifiers.

This is required because a computational pass without source validation is not final scientific PASS.

## 7. Candidate discovery procedure

Search may use:
- public GitHub repository/file search;
- project websites and documentation;
- TEI Correspondence SIG / CMIF documentation;
- generic schema/template files.

During discovery:
- do not fetch or open candidate episode XML files;
- do not search for specific conflicting dates, uncertain letters, or correction examples;
- do not use observed D1/D2 prevalence to choose a project.

Record every seriously screened candidate, including rejected candidates and the first failed hard gate.

## 8. Selection rule

The next holdout project must satisfy all four hard gates:

    independence
    + frozen A/B/C object compatibility
    + >=2 documented temporal-carrier families
    + closed population/provenance feasibility

Among multiple passers, prefer in this order using only pre-content metadata:

1. explicit Route A in a generic schema/template;
2. one-file-per-letter organization;
3. larger closed XML population;
4. stronger generic source/facsimile provenance;
5. canonical repository full name as deterministic tie-break.

No observed scientific outcome may enter this choice.

## 9. Next-step freeze

Once a project passes screening:

1. freeze repository URL, commit SHA, population path/register, expected XML count, and generic schema evidence;
2. record that no episode XML has been opened;
3. freeze the exact Module J engine SHAs or a separately justified future engine version before data opening;
4. run inherited hardening tests first;
5. open the full frozen population exactly once;
6. retain PASS / BOUNDED_PARTIAL / NULL_APPLICABILITY / INVALID without rescue.

## 10. Scientific intent

The next successful empirical step must add evidence that Modules J/K currently lack:

    prospective eligible objects under the already strict object gate

and, if such objects exist,

    prospective dynamic trajectories in an ecology independent of DAHN.

The goal is not a positive result at any cost. The goal is an independently auditable result whose evidential status survives failure as well as success.
