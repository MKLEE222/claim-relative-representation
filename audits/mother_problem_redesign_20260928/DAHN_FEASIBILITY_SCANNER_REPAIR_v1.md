# DAHN feasibility scanner repair note v1

Date: 2026-09-28
Status: PRE-HOLDOUT FEASIBILITY EVALUATOR REPAIR. NO SCIENTIFIC HOLDOUT EXPERIMENT HAS BEEN RUN.

First feasibility run:
GitHub Actions run 36391961233
artifact 10956890750
results SHA-256 eef0e35bcc4befe83f42a8a8f094cc8a8087c2fdf2d8768c226cbeff9b1b8d22

The first scan reported 189/190 Berlin_Intellectuals XML documents as eligible.

Audit showed the implementation exceeded the frozen eligibility contract in two ways:

1. every generic TEI <date> outside the declared document-dating contexts was assigned role "date_other";
   this imported bibliography dates, dates mentioned in letter content, and other non-document-dating values into D1 disagreement tests;

2. any explicit relation was counted as D4_CANDIDATE and that candidate flag was allowed to make a document eligible even though the frozen contract requires D4 to establish an encoded temporal incompatibility/narrowing constraint.

Repair before any holdout protocol or outcome:

- generic <date> is a carrier only when it is inside:
  - correspAction (typed sent/received/etc.),
  - opener/dateline;
- docDate and origDate remain carriers;
- generic body/bibliography/revision dates are excluded;
- D3 note/comment evidence is restricted to document-history/correspondence/dating contexts;
- D4 remains a descriptive candidate flag only and cannot by itself make a document eligible;
- revisionDesc remains available only as an irrelevant/null-event feasibility flag.

The frozen feasibility thresholds and source commit are unchanged.

The first scan is retained as an implementation-invalid overinclusive diagnostic and is not used to decide candidate viability.
