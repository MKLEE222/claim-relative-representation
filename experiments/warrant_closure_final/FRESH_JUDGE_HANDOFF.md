# Fresh Final LLM Judge Handoff v1

Date frozen: 2026-09-26
Status: READY AFTER V3 PACKET BUILD

## Purpose

The final confirmatory computational adjudication must not reuse J0's same-session model context.

## Judge-visible input

Use only `judge_calls_v1.jsonl`.

Do NOT provide the model:
- repository URL;
- audit manifest;
- packet-to-condition mapping;
- J0 outputs;
- claim ledger;
- expected selective-restoration pattern.

## Execution unit

Each JSONL record is one independent call.

A model call receives exactly one record's prompt and response schema.

Never batch multiple records into the same conversational context.

Do not let a call see previous call outputs.

## Total calls

15 per model:
- 5 anonymous packet families;
- canonical;
- reverse-order;
- ID-relabel-only.

## Required recording

For each call save:
- call_id;
- exact model identifier/version if available;
- date/time;
- product/API mode;
- sampling parameters if exposed;
- raw structured response;
- schema-validation status.

## Primary analysis

Unblind only after all 15 outputs for that model are frozen.

First test packet-level stability:
- canonical state = reverse-order state = ID-relabel state.

Only stable packets enter selective-restoration analysis.

## Confirmatory selective-restoration pattern

The audit-only mapping evaluates:
- generic base;
- guided base;
- generic + PM03 rescue;
- generic + sham later/source unit;
- guided - PM03 with donor replacement.

The model never sees those condition names.

## Failure handling

- malformed output: one schema-repair retry using the same evidence, logged;
- context/tool failure: BLOCKED_EXECUTION;
- perturbation state disagreement: MODEL_SENSITIVE;
- same warrant state across causal contrasts: retain null.

## Claim ceiling

A successful fresh run can support an independent/stateless computational replication.

It still does not measure human historian behavior.