# Final Warrant Pre-LLM Readiness v1

Date: 2026-09-26
Status: READY FOR FRESH STATELESS/MODEL-SEPARATED EXECUTION

## What changed after J0

J0 is retained as development/pipeline evidence only.
The final design repairs the main weaknesses revealed by J0:

1. atomic claim instead of unconstrained REVISE;
2. exact PM01/PM02 source spans instead of hand-compressed ellipses;
3. overlapping retrieval windows collapsed to unique evidence units;
4. equal unique-unit budget B=6;
5. PM03 rescue/add-back;
6. non-PM03 sham add-back;
7. PM03 removal with controlled donor replacement;
8. E_* definitions embedded directly in the final judge prompt;
9. judge-visible packet bundle separated from audit mapping and PM03 flags;
10. one independent stateless call per packet perturbation.

## Structural audit result

Generic raw top-12 -> 8 unique units.
Guided domain raw 12 -> 6 unique units.
Therefore the frozen maximum common budget is:
`B_FINAL=6`.

The guided PM03 material occupies one deduplicated unit.
A non-PM03 source-chain donor exists, so both sham and removal controls are constructible.

## Frozen packet family

Five opaque packet IDs, each with 6 unique units:
- K4N
- R8Q
- M3V
- H7C
- T2P

The judge-visible bundle contains no policy names, target rank, PM03 flag, raw retrieval offsets, or audit mapping.

## Exact shared context

PM01 exact context SHA-256:
`b545dc2dbc1227dab749e607a5fad2cfd2e21bb4dcc212ef0621cbba0373cc03`

PM02 exact context SHA-256:
`347f763c84099bd0ee6a70165729094d94cfdb7251ded6e0d868cf944467be51`

## Build and call artifacts

Authoritative preparation run:
`36210409872`

Judge bundle artifact:
`pm-final-judge-bundle-v3`

Judge-call artifact:
`pm-final-judge-calls-v1`

Audit-only artifact:
`pm-final-audit-manifests-v3`

Judge call file SHA-256:
`cf8a9853eb8281db3e77d2dfe742f0b89063d5a21cb02a18251f1a086e88536c`

Total independent calls:
`15`.

## Final hard rule

No more scientific design changes are authorized after a fresh final judge output is opened.

If a transport/provider problem prevents execution, mark BLOCKED_EXECUTION.
If outputs are unstable, mark MODEL_SENSITIVE.
If causal contrasts are null, retain the null.