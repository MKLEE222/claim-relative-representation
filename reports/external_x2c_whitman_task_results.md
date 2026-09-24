# Whitman X2C results - printed-locus task audit

Date: 2026-09-24
Authoritative completed step: GitHub Actions run 35958181827 (Whitman step passed; later Faust transport step failed)

## Task-facing result

The native 1855 Leaves of Grass relation file contains:

- 764 unique printed loci with at least one manuscript/notebook relation;
- 329 printed loci linked to more than one manuscript/notebook passage;
- 120 printed loci whose linked passages include both high- and low-certainty relations;
- 251 loci with high-only links;
- 393 loci with low-only links;
- maximum 16 linked manuscript/notebook passages for a single printed locus.

## Projection result

Removing per-link certainty while preserving all endpoints leaves the printed-locus endpoint task unchanged:

\[
Y^{-cert}_{link}(p)=Y_{link}(p)
\]

for all 764 printed loci.

However, on the 120 mixed-certainty loci, the Archive's relation-status output is not preserved.

## Interpretation

This is stronger than a schema-level observation.

For many real printed loci, "there is an explicit relation" does not determine a single editorial certainty state.

Therefore:

\[
endpoint\ recoverability \neq certainty\ recoverability.
\]

The task boundary is native to the external project and occurs at substantial scale.

No independent genetic judgment is inferred.
