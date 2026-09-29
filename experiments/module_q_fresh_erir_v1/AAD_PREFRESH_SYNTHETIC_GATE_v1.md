# Module Q — AAD pre-fresh synthetic compatibility gate v1

Date frozen: 2026-09-29
Status: PRE-FRESH / NO AAD EDITION XML OPENED.

## Purpose

Auden in Austria Digital (AAD) is currently the best deterministic fresh temporal ERIR candidate
that passes project-level screening, but it is explicitly a same-framework relative of AMP.

Before any AAD edition episode is opened, this gate tests whether the already frozen portable
object/claim engine can represent the project-native hierarchy derived only from:
- AAD README;
- project ODD/Schematron;
- generic XML template generator.

No real AAD episode value is used.

## Frozen synthetic shape

The fixture contains:
- one TEI document;
- one msDesc/history/origin/origDate;
- one correspDesc;
- one correspAction type=sent with one machine date;
- one body/div type=transcription;
- inside it, one div type=letter;
- inside it, one div type=letter_message;
- one opener/dateline/date.

The dates are synthetic and intentionally disjoint.

The fixture is not copied from any AAD edition XML.

## Required compatibility checks

Oracle and runtime must agree on:

1. object contract:
   SINGLE_PRIMARY_DOCUMENT_OBJECT

2. boundary kind:
   EXPLICIT_LETTER_DIV

3. origin contract:
   SINGLE_ORIGIN_ADMISSIBLE

4. pre-event warrant:
   determined from current/root temporal carrier(s)

5. post-event warrant:
   changes after opening origDate

6. Module-P disposition:
   ERIR_ELIGIBLE

7. Module-P transition class:
   frozen classifier output

8. P1-P7 reference capability vector:
   all PASS

9. failure interventions:
   wrong object rejected;
   wrong source version rejected;
   missing applicability rejected;
   collateral mutation detected;
   delayed-history drop detected.

## Decision rule

PASS:
all compatibility checks pass without any AAD-specific parser code.

FAIL:
the frozen portable engine cannot represent the generic AAD shape.

If FAIL:
do not open AAD edition XML. Any adapter must be specified and hardened using synthetic material
before AAD can be reconsidered.

If PASS:
AAD may proceed to a separately frozen one-shot population protocol over all 148 direct XML files.

## Scientific ceiling

A PASS establishes parser/task compatibility only.

It does not establish:
- that any of the 148 real AAD documents are ERIR-eligible;
- that AAD contains a substantive warrant transition;
- that AAD is independent of AMP at the encoding-framework level;
- cross-ecology generalization.

The real AAD population remains fresh after this synthetic gate.
