# CI execution policy

Date: 2026-09-25

## Why validation and live replay are separated

The repository contains two executable classes:

1. deterministic contract/schema/construction validation using repository-local inputs;
2. scientific replays that fetch pinned external source objects.

Running every live-source replay on every commit made ordinary CI sensitive to transient network outages. A failed HTTP connection could display a red build even though no scientific or schema assertion failed.

## Policy

The validate-research-contract workflow runs on push and pull request and contains repository-local deterministic checks.

The replay-live-source-experiments workflow is manual (workflow_dispatch) and reruns source-fetching experiments against pinned URLs, commits, and hashes.

A live replay that fails before source identity/hash verification because the source cannot be fetched is classified as BLOCKED_TRANSPORT, not a scientific failure.

A scientific result changes only when the pinned source is fetched, identity checks pass, the registered scientific gate is reached, and the result itself changes.

Previously recorded authoritative run IDs remain authoritative unless deliberately superseded. Separating CI pathways does not silently re-run or reopen holdouts.
