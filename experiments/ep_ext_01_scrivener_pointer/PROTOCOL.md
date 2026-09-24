# EP_EXT_01 - Scrivener explicit-pointer external holdout

Date frozen: 2026-09-24
Status: PRE-OUTCOME EXTERNAL HOLDOUT

## Selection rule

External object:
F. H. A. Scrivener, *A Plain Introduction to the Criticism of the New Testament*, Vol. I, 4th ed. (1894), edited by Edward Miller.

Native digital object:
Project Gutenberg eBook #36548.

Episode selection is structural, not outcome-based.

From "Addenda Et Corrigenda", choose the first entry satisfying all of:

1. single page pointer;
2. single line pointer;
3. lexical substitution of the form "for X read Y";
4. page number > 20;
5. X/Y are not chapter-number navigation labels.

The selected frozen entry is:

P. 87, l. 19, for Synaxaria read Menologies.

No retrieval/localization outcome for this entry was inspected before freeze.

## Scientific task

Given the correction entry, locate the source locus in the body to which the correction applies.

This is a documentary localization task, not a textual-critical truth judgment.

## Mediation primitive

M_EXPLICIT_POINTER

Native bridge coordinates:

- page = 87
- line = 19
- old reading = Synaxaria
- corrected reading = Menologies

## Conditions

### SCR-FULL-POINTER

Expose page + line + lexical substitution.

The target source page is explicit.

### SCR-PAGE-ONLY

Remove line coordinate while retaining page + lexical substitution.

Search only the native page-87 segment for the old reading.

Question:
is the page coordinate sufficient to isolate the corrected source occurrence under this task?

### SCR-POINTER-FREE

Remove page and line coordinates while retaining only:

for Synaxaria read Menologies

Search the full body for the old reading.

Question:
does lexical identity substitute for the documentary pointer, and at what candidate burden?

## Frozen target

Evaluation target:
the occurrence of "Synaxaria" inside native page 87.

The target page is taken from the native correction pointer and is not inferred from retrieval results.

## Metrics

- source SHA-256;
- page-87 marker availability;
- count of old-reading occurrences on page 87;
- count of old-reading occurrences in the body after Addenda;
- candidate ordinal of the page-87 occurrence under pointer-free document order;
- task state for each condition;
- minimal sufficient pointer subset among:
  {page, line} under the frozen lexical substitution.

## Outcome states

### EXACT_LOCALIZATION
one candidate source occurrence.

### MULTIPLE_CANDIDATES
target is among multiple admissible occurrences.

### BLOCKED_SOURCE
native page marker or target old reading cannot be verified.

No search rule or episode is changed after outcome.

## Prior-method reuse

The experiment deliberately reuses two earlier methodological disciplines:

- fixed-target comparison;
- minimal sufficient information under a frozen task contract.

The current scientific object is the DH documentary pointer and its task-relative carrier substitution, not the prior formal machinery.

## Claim ceiling

The experiment may establish:
- whether page/line pointer coordinates are necessary or redundant for this localization task;
- whether lexical recovery substitutes for pointer loss in this native object.

It cannot establish:
- global adequacy of Project Gutenberg;
- correctness of Scrivener/Miller's textual criticism;
- a universal rule for corrigenda.
