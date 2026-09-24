# Faust X3B results - temporal relation versus source provenance

Date: 2026-09-24
Authoritative CI run: 35957610722

## Construction result

The frozen source file contains 77 temporal assertions.

Two projections were validated.

### X3B-L - locator removal

Removed per-relation source locator text from all 77 relations while preserving:

- source URI;
- relation name;
- ordered item sequence.

Result:
- ordered temporal sequences changed: 0
- source work URI changed: 0
- source locators removed: 77

### X3B-S - relation-local source removal

Removed the source element from all 77 relations while preserving all ordered item sequences.

Result:
- temporal sequence changed: 0
- relation-local source elements removed: 77

## Task-relative disposition

### FA-TEMPORAL

Structural state: **PRESERVED** under both projections.

### FA-SOURCE-WORK

- preserved under X3B-L;
- under X3B-S, relation-local exposure is removed, but contextual recovery from the file path / collection organization has not yet been tested.

### FA-SOURCE-LOCATOR

Explicit state: **REMOVED** under X3B-L and X3B-S.

## Interpretation

This external object forces a finer distinction than "provenance present/absent":

\[
temporal\ order,\ source\ work,\ source\ locator
\]

are separable representational coordinates.

A temporal edge can remain fully explicit while the evidential basis for auditing that edge becomes less accessible.

The result does not claim a unique historical chronology.
