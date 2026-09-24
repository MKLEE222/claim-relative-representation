# Holdout Promotion Gate v1

A development workflow may be promoted to holdout testing only if:

1. source hashes/IDs are frozen;
2. task entry state is frozen;
3. workflow version is frozen;
4. target-only information is isolated to evaluation code;
5. null/failure retention is explicit;
6. case-specific tuning hooks are absent;
7. the holdout role is declared before execution;
8. the holdout has not been used to design the workflow.

Current disposition:

- EP_PM_01: DEV, not eligible as replication.
- EP_KS_01/02/03: eligible for NEAR_HOLDOUT construction after exact scan verification is complete for the required target relation.
- EP_CL_01: eligible as BOUNDARY after exact scan verification is complete.
- EP_EXT_01: blocked pending external-carrier selection under the eligibility criteria.
