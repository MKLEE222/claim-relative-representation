# DAHN feasibility scanner repair note v2

Date: 2026-09-28
Status: PRE-HOLDOUT FEASIBILITY EVALUATOR REPAIR. NO HOLDOUT EXPERIMENT HAS BEEN RUN.

Second feasibility run:
GitHub Actions run 36392129992

The second scan corrected the first overinclusive use of arbitrary TEI <date> elements and reduced eligibility from 189/190 to 55/190.

Inspection of source examples exposed two remaining semantic implementation problems:

1. the scanner omitted TEI attributes notBefore-iso and notAfter-iso, so source-native bounded dating uncertainty was underdetected;

2. D1 disagreement used raw string inequality/disjointness. This incorrectly treats compatible precision levels such as 1805 and 1805-03-01 as contradictory rather than nested temporal constraints.

Repair before any prospective holdout protocol:

- add notBefore-iso, notAfter-iso, from-iso, and to-iso to the date contract;
- map supported machine-readable date values to closed temporal intervals;
- compare carriers by interval compatibility, not string identity;
- preserve disjoint multiple docDate elements as separate manuscript date carriers;
- allow D2 when a bounded/uncertain carrier is narrowed by another compatible carrier;
- require an actual correspDesc with at least one correspAction for final episode eligibility, consistent with the frozen root task of constructing a correspondence chronology;
- non-correspondence corpus XML remains in the population and is reported, but cannot become a holdout episode.

The source commit and feasibility thresholds remain unchanged.

The second scan is retained as an intermediate diagnostic and is not the final viability decision.