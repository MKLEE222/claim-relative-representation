# External Validation X2B - Whitman certainty-projection preflight

Date frozen: 2026-09-24
Status: CONTROLLED EXTERNAL PROJECTION

## Transformation

Input:
the pinned native 1855 Leaves of Grass Relations List.

Projection:
remove every link @cert attribute while preserving:

- relation-group order;
- link-group corresp;
- every link target;
- number of groups;
- number of links;
- all other XML content.

## Task contracts

### WW-LINK
Given a printed locus, recover the explicitly linked manuscript/notebook locus.

Required native carrier:
link target/corresp.

### WW-CERTAINTY
Given an explicit link, recover the Archive's encoded certainty category for that link.

Required native carrier:
per-link @cert.

## Hypothesis

The projection should be:

\[
R_{native} \equiv^{structure}_{WW-LINK} R_{no-cert}
\]

but not:

\[
R_{native} \equiv^{structure}_{WW-CERTAINTY} R_{no-cert}
\]

This is a structural task-equivalence audit, not a human accuracy experiment.

## Anti-tautology boundary

The result does not establish that users would always need the @cert attribute to make their own independent scholarly judgment.

It establishes only whether the external project's **encoded editorial certainty state** remains available.
