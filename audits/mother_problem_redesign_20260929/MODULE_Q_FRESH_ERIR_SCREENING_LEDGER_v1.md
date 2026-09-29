# Module Q — fresh ERIR candidate screening ledger v1

Date started: 2026-09-29
Status: ACTIVE PRE-CONTENT SCREENING.

All statuses in this ledger are governed by MODULE_Q_FRESH_ERIR_SCREENING_PROTOCOL_v1.md.

## Previously known non-fresh / rejected projects

### FloChiff/DAHNProject

Status:

    EXPOSED / INDEPENDENCE FAIL

Berlin, Paul, StaBi and GeStA are already consumed/exposed.

### Auden-Musulin-Papers/amp-data

Status:

    EXPOSED DEVELOPMENT

Authoritative Module O and Module P development study have opened the complete population.

### digicademy/sturm-exist-app

Status:

    EXPOSED_DURING_PRIOR_SCREENING

Concrete rendered episode/date fragments were returned during earlier code search.

### telota/jean_paul_briefe

Status:

    EXPOSED_DURING_PRIOR_SCREENING

Concrete episode XML was returned during earlier public search.

### arthur-schnitzler/schnitzler-briefe-data

Status:

    EXPOSED_DURING_PRIOR_SCREENING

Concrete episode XML was returned during earlier public search.

## Current Module-Q screening

### cambridge-collection/darwin-correspondence-data

Repository metadata inspected only.

Frozen-at-screening default-branch commit observed:

    74351699d19e7a3a0840c48c00962a0fd0b897bc

Tree metadata:

    xml/ contains 36507 XML files

Current status:

    PROVISIONAL / DOCUMENTATION INSUFFICIENT

README establishes Darwin Project data but the repository-level generic documentation inspected so
far does not prospectively establish a project-specific current-claim versus independent
later-evidence semantic split.

No Darwin episode XML has been opened.

### whitmanarchive/whitman-correspondence

Repository metadata, README and generic transformation code inspected only.

Screening commit:

    0961a202320498be56f81a155e47707bbdeb20f5

Tree metadata:

    source/ contains 6041 XML files

Generic documentation establishes:
- a dedicated Whitman correspondence TEI data repository;
- strong source/editorial provenance in generic transforms;
- an editorial practice of supplementing/updating correspondence notes.

Current status:

    PROVISIONAL / LATER-EVIDENCE CARRIER NOT YET ESTABLISHED

The inspected generic files do not yet establish a machine-separable later evidence layer
satisfying Module Q.

No Whitman episode XML has been opened.

### KONDE-AT/thun-data

Repository metadata, README and process.xsl inspected only.

Screening commit:

    ad1248e7fd36252e95b391782731437b0de09314

Tree metadata:

    editions/ contains 865 XML files

README establishes a correspondence edition.
process.xsl generically normalizes date @when to @when-iso.

Current status:

    PROVISIONAL / LATER-EVIDENCE GATE NOT ESTABLISHED

No inspected project-level documentation yet establishes an independent origin/editorial evidence
layer distinct from the current correspondence date.

No Thun episode XML has been opened.

### CarlaMenegat/VarelaDigital

Repository metadata, project data-model HTML and generic TEI-to-HTML transform inspected only.

Screening commit:

    57c13db409c91503ffd39d2e6e3a131f5dbb59d0

Tree metadata:

    letters_data/ contains 306 XML files

Project-level material establishes:
- explicit modelling of letters as documentary works;
- current sent-date rendering through correspDesc/correspAction;
- project provenance/editorial framing.

Generic transform explicitly permits more than one div type=letter in one file.

Current status:

    PROVISIONAL / LATER-EVIDENCE GATE NOT ESTABLISHED

No inspected generic material establishes a separate later origin/editorial evidence layer.
The multi-letter-per-file ecology would also require a prospectively justified object adapter if
this project later passed the evidence gate.

No Varela episode XML has been opened.

### Unlocking the Mary Hamilton Papers

Project website, editorial schema/guidelines and collection-level documentation were inspected.

Project-level documentation strongly establishes the desired semantics:
- each master document is TEI XML;
- origDate represents date of writing/origin;
- correspDesc represents correspondence sending metadata;
- the schema explicitly discusses cases where date of writing and sending differ;
- rich manuscript/editorial provenance exists;
- the current edition contains thousands of items.

However, while checking whether a deterministic bulk XML distribution/API was publicly available,
web search results returned concrete individual-item pages including episode-level date/revision
metadata.

Status:

    EXPOSED_DURING_SCREENING — NOT ELIGIBLE FOR FRESH HOLDOUT

This status is permanent for Module Q.
The project remains valuable future development/comparative evidence.

The public distribution route also remains insufficiently clear for a frozen automated XML
population: current public documentation clearly offers the edition and plain-text distributions,
while bulk source-XML availability is not established by the inspected distribution pages.


### Edirom/WeGA-ODD / WeGA correspondence ecology

Only the generic ODD/customization repository was inspected.

Screening ODD commit:

    9d5b3343ce753cb53c218088636d7ab867671a54

Project-level schema establishes:
- one TEI letter resource with project-native text type=letter semantics;
- body divisions typed writingSession;
- exactly one correspDesc in profileDesc;
- required correspAction typing;
- strong source/facsimile/editorial metadata.

A future object adapter could be designed prospectively from the generic ODD because the project
does not use the frozen A/B/C serialization directly.

However generic ODD search did not establish:
- origDate as a project letter carrier;
- a postmark-versus-handwritten-date layer;
- another independent later evidence carrier satisfying Module-Q ERIR.

Current status:

    PROVISIONAL / OBJECT ADAPTER FEASIBLE / LATER-EVIDENCE GATE NOT ESTABLISHED

No WeGA episode XML has been opened.

### HistoryAtState/frus

Only repository metadata, README and schema/frus.odd were inspected.

Screening commit:

    8e5da08c1d99bbcdf69c34cef8c15dff91f95cf9

Closed repository metadata:
- volumes/ contains 744 XML files;
- README states one XML file per FRUS volume;
- each volume contains explicitly identified div type=document scholarly document units.

Generic ODD establishes a rich editorial provenance ecology:
- revisionDesc/change as a major revision log;
- editorialDecl/correction for corrections to source text and known issues;
- document datelines as source-visible origin-date text;
- machine date values that may be added or corrected;
- closed date/@ana categories documenting the evidence used in editorial dating.

Prospectively documented evidence categories include:
- correction from document content;
- correction from scanned original;
- correction from outside research;
- correction from sibling dates;
- compiler/editor correction;
- inference from document head;
- inference from editorial annotation;
- inference from editorial consultation;
- inference from related sources;
- inferred dates for otherwise undated documents.

This is stronger than a second serialization of the same date: the project explicitly records
the scholarly basis by which a date value was inferred or corrected.

Freshness status:

    FRESH — NO volumes/*.xml FILE HAS BEEN OPENED

Module-Q temporal status:

    HOLD / DO NOT OPEN

Reason:
the current Module-P temporal implementation assumes a machine-addressable S0 warrant and an
independent later evidence claim. FRUS instead prospectively exposes a different structure:

    source-visible documentary date/status
    -> editorial assessment / evidence category
    -> normalized or corrected scholarly date

Mapping this into Module P would require a new prospectively frozen adapter/event model rather
than simply reusing the AMP origDate release mechanism.

Scientific routing:

    RESERVED HIGH-VALUE CANDIDATE FOR SECOND EVENT FAMILY
    OR FOR A SEPARATELY FROZEN EDITORIAL-ASSESSMENT ERIR STUDY

Do not consume FRUS episode XML while Module-Q fresh temporal confirmation remains unresolved.
The project is especially valuable because its generic model approaches the E13/CRMinf
assertion/evidence pattern identified in the near-neighbor design audit.


### auden-in-austria-digital/aad-data

Only repository metadata, README, project ODD/Schematron and generic template-generation code
were inspected.

Screening commit:

    34c3958686ab03614dedd8d979ffe94b6c0f2a28

Closed population metadata:

    data/xml/editions/
    148 direct XML files
    0 subdirectories

No file under data/xml/editions/*.xml has been opened.

Project-level evidence establishes:
- editorial data and XML-generation workflows for Auden in Austria Digital;
- every generated document receives msDesc/history/origin/origDate from project metadata;
- origDate uses required notBefore-iso / notAfter-iso;
- correspDesc requires at least one correspAction when present;
- correspAction has a closed action vocabulary including sent;
- correspondence-like document categories are validated for correspondence metadata;
- the transcription hierarchy includes project-native letter / letter_message structure;
- facsimile/source metadata is part of the project workflow.

Scientific independence limitation:

    SAME-FRAMEWORK / NOT CROSS-ENCODING

The ODD and editorial workflow are highly similar to the already exposed AMP project.
Therefore AAD can provide:
- fresh cross-project prospective replication;

but cannot by itself provide:
- independent encoding-ecology confirmation.

Current status:

    HARD-GATE PASSER WITH EXPLICIT SAME-FRAMEWORK CEILING

Before any episode opening, a synthetic AAD-shaped fixture derived only from the ODD must verify
that the frozen portable object/claim engine handles the project hierarchy without an
outcome-specific adapter.

If that pre-fresh synthetic gate passes, AAD is the current deterministic Module-Q choice among
hard-gate passers.

### stazh/briefedition-escher

Only repository metadata, README, generic conversion code and ODD were inspected.

Screening commit:

    e604c0e494aa217059038491f168fa50db45deba

Project-level material strongly establishes:
- a real digital correspondence edition;
- letter objects and stable IDs;
- conversion of source letter metadata to correspDesc/correspAction type=sent;
- separate timeline/context infrastructure.

However the generic conversion/schema inspected so far does not establish an independent
origDate/editorial-evidence layer distinct from the current correspondence date.

Current status:

    REJECT / LATER-EVIDENCE HARD GATE NOT ESTABLISHED

No letter episode XML has been opened.

### Briefverkehr-der-Stadt-St-Gallen/sg-missiven-app

A generic ODD search initially surfaced correspAction(sent) and origDate rendering rules.

Project README inspection showed that the application uses stazh/erqzh-data, whose documented
data are Zürcher Rechtsquellen/legal-source editions rather than the correspondence ecology
suggested by the search hit.

Current status:

    REJECT / PROJECT-SEMANTIC MISMATCH

This is retained as evidence that generic TEI vocabulary is not sufficient to establish the
scholarly semantics required by Module Q.

No source episode XML was opened.

### HistoryAtState/frus — reserved for Module R

Only repository metadata, README and schema/frus.odd have been inspected.

Screening commit:

    8e5da08c1d99bbcdf69c34cef8c15dff91f95cf9

Status:

    FRESH RESERVED / DO NOT OPEN

FRUS is no longer treated as the preferred temporal Module-Q candidate.
Its generic model is more valuable for the separately frozen Module-R scholarly assertion /
editorial reassessment family.

No volumes/*.xml file has been opened.


## FRUS freshness update — 2026-09-29

A repository-wide code-search query intended to locate project-level sender/recipient encoding
returned one incidental snippet from:

    volumes/frus1977-80v09.xml

The snippet contained only a General Editor byline / nearby publication URL fragment and no target
document-level reassessment episode.

Nevertheless the reserved-candidate rule prohibited any volumes/*.xml exposure.

Therefore:

    FRUS_STRICT_FRESHNESS = LOST
    FRESH_MODULE_R_USE = DISALLOWED

See:

    audits/mother_problem_redesign_20260929/
    FRUS_FRESHNESS_INCIDENT_MEMO_2026-09-29.md

FRUS remains usable for exposed design/development only.
