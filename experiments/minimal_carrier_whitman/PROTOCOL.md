# MC_WW_01 - Whitman endpoint minimal-carrier search

Date frozen: 2026-09-24
Status: MECHANISM SEARCH ON ALREADY-INSPECTED NATIVE OBJECT

## Task

Given a printed locus in the 1855 relation list, recover the full set of linked manuscript/notebook endpoints:

\[
(ms\_file,\ ms\_local\_locus).
\]

## Candidate carriers

- PRINT_LOCUS: first token of link @target
- MS_LOCUS: second token of link @target
- MS_FILE: linkGrp @corresp
- CERTAINTY: link @cert

## Reference output

The intact native mapping from each printed locus to its set of (MS_FILE, MS_LOCUS) pairs.

## Frozen subset logic

A subset can be sufficient only if:

1. PRINT_LOCUS is retained, because the task input addresses relations by printed locus;
2. MS_FILE is retained or another retained native carrier explicitly names the manuscript file;
3. MS_LOCUS is retained or another retained native carrier explicitly names the manuscript local locus.

CERTAINTY is not part of the endpoint task output.

The script also checks whether local manuscript locus strings repeat across manuscript files, which would rule out treating MS_LOCUS as a hidden file identifier.

## Expected scientific question

Is the certainty coordinate redundant for endpoint recovery while manuscript file identity remains necessary?

This is development/mechanism evidence, not a fresh holdout.
