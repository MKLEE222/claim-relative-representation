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
