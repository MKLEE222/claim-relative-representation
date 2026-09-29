# Module Q — AAD fresh temporal ERIR pre-fresh protocol v1

Date frozen: 2026-09-29
Status: PRE-FRESH / NO AAD EPISODE XML OPENED.

## 1. Scientific purpose

Module P has:
- synthetic mechanism hardening;
- exposed AMP development evidence.

Module Q is the prospective confirmation stage for the same temporal evidence-release-induced
revision (ERIR) family.

The currently selected fresh project is:

    auden-in-austria-digital/aad-data

Pinned upstream commit:

    34c3958686ab03614dedd8d979ffe94b6c0f2a28

No file under:

    data/xml/editions/*.xml

has been opened before this protocol.

## 2. Independence ceiling

AAD is a fresh project but is not an independent encoding ecology from AMP.

Its project ODD and editorial workflow are closely related to the AMP framework.

Therefore Module Q may license only:

    fresh cross-project prospective replication within a closely related TEI/edition framework

It may NOT be described as:

    cross-encoding confirmation
    independent infrastructure confirmation
    independent event-family confirmation

The separate Module R line is responsible for the non-temporal event-family extension.

## 3. Closed population

Repository tree inspection before episode opening establishes:

    data/xml/editions/
    148 direct files
    148 XML files
    0 subdirectories
    0 non-XML files

The fresh population is frozen as every direct XML file in that directory at the pinned commit.

No file may be excluded because of its later content or outcome.

Expected population:

    N_files = 148

If an archive/accounting mismatch occurs, the run is INVALID.

## 4. Project-level semantic basis frozen before opening

Only README, project ODD/Schematron, generic template generation code and repository directory
metadata were inspected.

Those project-level materials establish:

- an editorial TEI/XML workflow;
- project-native transcription structure;
- project-native letter / letter_message structure;
- msDesc/history/origin/origDate as a distinct origin carrier;
- origDate requiring notBefore-iso and notAfter-iso;
- correspDesc/correspAction support;
- a closed correspAction action vocabulary including sent;
- source/facsimile metadata in the editorial workflow.

This is sufficient to justify a prospective test for documents that actually instantiate both
a current/root temporal carrier and one later/origin evidence carrier.

It does NOT guarantee that any fresh document will be ERIR-eligible.

A zero-eligible result is a valid applicability null.

## 5. Frozen parser / engine rule

Module Q does not create a new AAD-specific scientific parser.

It must reuse unchanged:

    experiments/module_l_portable_object_claim_v1/oracle_l.py
    experiments/module_l_portable_object_claim_v1/runtime_l.py
    experiments/module_p_evidence_release_revision_v1/oracle_p.py
    experiments/module_p_evidence_release_revision_v1/runtime_p.py
    experiments/module_p_evidence_release_revision_v1/evaluator_p.py

and the already frozen Module-M comparators.

No post-opening source-specific route may be added.

## 6. Pre-fresh AAD-shaped synthetic gate

Before any AAD episode XML is opened, the unchanged engine must parse a synthetic fixture whose
serialization shape is derived only from already inspected project-level ODD/generator rules.

The fixture uses fabricated dates, names and identifiers.

Required positive shape:

    TEI
      teiHeader
        fileDesc/sourceDesc/msDesc/history/origin/origDate
        profileDesc/correspDesc/correspAction[@type='sent']/date
      text/body
        div[@type='transcription']
          div[@type='letter']
            div[@type='letter_message']
              opener/dateline/date
              ...

The fixture may include an envelope/enclosure sibling to test that the single explicit letter
remains the selected scholarly object.

The fixture must not copy any AAD episode content.

## 7. Synthetic gate requirements

The unchanged oracle/runtime must agree that the positive fixture has:

- SINGLE_PRIMARY_DOCUMENT_OBJECT;
- boundary kind EXPLICIT_LETTER_DIV;
- exactly one admissible origin claim;
- one current/root scholarly warrant;
- a substantive Phi change after origin evidence release;
- ERIR_ELIGIBLE;
- a registered Module-P transition class;
- exact P1-P7 retained-interface capabilities.

A paired synthetic null with the same root/origin warrant projection must remain:

    ADMISSIBLE_NULL_EVENT

not substantive ERIR.

The gate also checks that a date inside a non-letter sibling does not silently become part of the
selected letter object's root warrant.

## 8. No adapter rescue rule

If the synthetic AAD-shaped fixture fails under the unchanged engine:

- record the failure;
- do not open AAD episode XML;
- decide whether the project is incompatible with the frozen Module-P object/claim contract.

A new adapter may only be introduced under a separately versioned scientific contract before any
fresh episode content is opened.

No outcome-specific repair is permitted after AAD opening.

## 9. Fresh opening rule

AAD episode XML may be opened only if the pre-fresh synthetic gate passes.

The first fresh run must:
1. download the pinned upstream archive;
2. enumerate all 148 direct XML files;
3. parse every file independently with oracle/runtime;
4. retain parse failures and ineligible objects;
5. classify every file as:
   - ERIR_ELIGIBLE;
   - ADMISSIBLE_NULL_EVENT;
   - INELIGIBLE;
6. execute P1-P7 only on ERIR_ELIGIBLE documents;
7. preserve comparator capability vectors;
8. preserve failure-intervention results on eligible documents;
9. source-audit every eligible event after the run without changing eligibility.

## 10. Primary outcomes

Report separately:

- total files;
- parse errors;
- object-contract status counts;
- origin-contract status counts;
- ERIR_ELIGIBLE count;
- ADMISSIBLE_NULL_EVENT count;
- INELIGIBLE count;
- P-U1/P-U2/P-U3/P-U4/OTHER distribution;
- P1-P7 capability counts;
- comparator vectors;
- source-audit disposition.

No scalar representation-quality score.

## 11. Result categories

### INVALID
Examples:
- population accounting mismatch;
- source commit mismatch;
- oracle/runtime contract disagreement;
- post-opening scientific-contract change;
- episode exclusion not frozen in advance.

### NULL
The population is valid but:

    N_ERIR_ELIGIBLE = 0

This is a corpus-applicability result, not model failure.

### BOUNDED_PARTIAL
At least one eligible event exists, but one or more frozen capability/source-audit gates fail.

### PASS
At least one eligible event exists and all frozen reference/source-audit gates pass.

PASS still remains same-framework fresh replication, not cross-encoding confirmation.

## 12. Stop rule

After the first AAD opening:
- AAD becomes exposed;
- no rerun with changed eligibility, object grammar, carrier grammar or source interpretation can
  be called fresh;
- any repair is development only.

FRUS remains unopened and is not part of Module Q.
