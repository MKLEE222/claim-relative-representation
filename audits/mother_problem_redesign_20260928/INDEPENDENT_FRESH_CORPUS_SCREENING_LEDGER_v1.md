# Independent fresh-corpus screening ledger v1

Date: 2026-09-29
Status: PRE-FRESH. NO AMP EDITION XML HAS BEEN OPENED.

This ledger implements the requirement in the frozen Module-L screening protocol to retain
seriously screened candidates, rejections, and accidental exposure.

## Screening rule

Episode-level XML/content must not be inspected before a candidate population is frozen.
Allowed pre-screening material:
- repository/project README;
- project ODD/schema/guidelines;
- generic templates and transformation code;
- repository tree/path metadata and file counts.

If a search result exposes episode content, the project is marked EXPOSED_DURING_SCREENING and
cannot be used as a fresh holdout.

A generic TEI schema merely allowing an element is not evidence that a project actually uses
that carrier. Project-specific documentation/customization is required.

## Candidate ledger

### FloChiff/DAHNProject — GeStA

Status:

    CONSUMED_FRESH / NULL_APPLICABILITY

Authoritative Module K:
- 83 XML;
- 83/83 parsed;
- 0 single primary object;
- 0 full trajectory.

Never fresh again.

### FloChiff/DAHNProject — BBAW / Humboldt-Archiv

Status:

    NOT_OPENED, BUT INDEPENDENCE_GATE_FAIL

Only tree/path metadata was inspected.

Reason:
same DAHN project/schema ecology as exposed Berlin/Paul/StaBi/GeStA.
Not eligible for Module-L independent-project confirmation.

### Edirom/WeGA-ODD / WeGA ecology

Status:

    REJECTED_PREOPEN_OBJECT_GRAMMAR

Project-level ODD encodes the whole letter as text type="letter" with writing-session divs,
rather than frozen Route A/B/C.

No episode XML was opened.

### digicademy/sturm-exist-app

Status:

    EXPOSED_DURING_SCREENING

A broad repository code search unexpectedly returned specific rendered letter/date fragments.
The project cannot be treated as fresh.

### Pantagrueliste/CavrianaCorr

Status:

    REJECTED_FOR_CURRENT_FULL_TRAJECTORY / RETAIN AS FUTURE DEVELOPMENT ECOLOGY

Project ODD strongly establishes:
- one letter per TEI file;
- one body div type="letter";
- correspAction type=sent/date;
- dateline;
- date range support;
- manuscript/archive provenance.

However no project-level documentation inspected before opening established the independent
history/origin/origDate evidence layer required by the current full J/L trajectory.

No episode XML was opened.

### kb-dk/SKS_tei

Status:

    REJECTED_FOR_CURRENT_FULL_TRAJECTORY

Generic conversion/project code establishes letter/correspondence structure, but the required
independent origDate/later-evidence layer was not prospectively established.

No episode XML was opened.

### thecdil/mancini_source

Status:

    REJECTED_PREOPEN_CURRENT_ENGINE_CONTRACT

Project documentation is highly relevant:
- one XML file per letter workflow;
- msDesc/history/origin/origDate;
- dateline;
- explicit editorial note for archive date mislabelling/correction.

But inspected project-level documentation/XSL did not establish:
- correspDesc/correspAction use;
- frozen explicit div type="letter" object grammar.

The current portable engine therefore cannot prospectively certify full-trajectory
compatibility.

No episode XML was opened.

### Masculinites-Esclavagistes/Draft-structure-of-the-TEI-edition-of-plantation-correspondences

Status:

    REJECTED_PREOPEN_POPULATION_GATE

README describes a draft based on a few example letters.
The repository does not provide the closed, sufficiently sized population required for the next
confirmatory holdout.

### blumenbach/blumenbach-tei

Status:

    REJECTED_PREOPEN_TASK/ECOLOGY_GATE

Repository purpose is primarily writings/bibliographic data integration rather than a closed
one-letter-per-object correspondence population suited to the frozen dynamic task.

### telota/jean_paul_briefe

Status:

    EXPOSED_DURING_SCREENING

A public search engine unexpectedly returned concrete episode XML, including correspondence
metadata and letter body content.

Although the exposed snippets show a promising correspondence structure, the corpus may not be
used as a fresh holdout.

### arthur-schnitzler/schnitzler-briefe-data

Status:

    EXPOSED_DURING_SCREENING

A public repository search unexpectedly returned concrete edition XML content for multiple
letters.

The project may not be used as a fresh holdout.

### Auden-Musulin-Papers/amp-data

Status:

    PROVISIONAL_PREOPEN_CANDIDATE — DO NOT OPEN YET

Current frozen upstream candidate commit:

    289a52de61aef0b6354e3c8298173bf1f889feb2

Closed population metadata:

    data/editions/
    73 XML files
    0 subdirectories

No edition XML has been fetched/opened during screening.

Project-specific schema.odd prospectively establishes:
- TEI customization explicitly for AMP correspondence;
- correspDesc must contain at least one correspAction;
- correspAction/@type is required and closed over sent/transmitted/redirected/received;
- correspAction date supports ISO temporal ranges;
- msDesc/history/origin/origDate is part of the project schema;
- origDate requires notBefore-iso and notAfter-iso in the current project schema;
- text structure includes body/div/opener/closer/dateline/salute/signed;
- body contains one transcription wrapper;
- transcription contains project letter/envelope/enclosure objects;
- explicit div type="letter" is a project-native scholarly object;
- manuscript repository/collection/idno provenance is represented.

Object caveat:
the inspected schema guarantees project-native explicit letter objects but does not by itself
prove that every edition file contains exactly one div type="letter".
The frozen portable object gate must therefore retain MULTIPLE/NO_PRIMARY as legitimate
applicability outcomes. No first-letter fallback is authorized.

### AMP pre-opening engine gap

The AMP project schema requires ISO datetime values such as:

    YYYY-MM-DDTHH:MM:SS+HH:MM

for notBefore-iso/notAfter-iso.

The current portable engine advertises these TEI attributes but inherited temporal parsers only
accept date-granularity strings such as YYYY-MM-DD.

Therefore AMP must NOT be opened yet.

Before AMP can be frozen as a one-shot holdout:
1. freeze a generic ISO-datetime portability amendment;
2. implement independent oracle/runtime parsing of ISO datetime values at declared day
   granularity;
3. add synthetic controls;
4. rerun all portable/inherited controls;
5. rerun exposed Berlin/Paul/StaBi and record any delta;
6. only if the pre-fresh gate closes may the AMP population be opened.

This repair is justified by project-level schema inspection before episode opening, not by
observed AMP outcomes.
