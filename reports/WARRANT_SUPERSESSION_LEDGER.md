# Warrant Closure Supersession Ledger v1

Date: 2026-09-26

| Earlier artifact | Status | Successor / interpretation |
|---|---|---|
| experiments/warrant_closure_pm/PROTOCOL.md | superseded before human adjudication | PROTOCOL_v2 removed mandatory human gate |
| experiments/warrant_closure_pm/PROTOCOL_v2.md | development architecture retained | experiments/warrant_closure_final/PROTOCOL.md is final confirmatory design |
| build_packet.py / pm-warrant-packets-v1 | development packet | final builder deduplicates unique evidence units and freezes selective controls |
| LLM_JUDGE_CONTRACT_v1.md | J0-only | final atomic manual + judge_prompt_v2 + STABILITY_CONTRACT |
| judge_results_J0.json | development/pipeline result | never counted as independent final replication |
| CLAIM_LEDGER_v2 C5a | development support only | final C5 awaits fresh/stateless or model-separated replication |

## Why J0 is retained

J0 is not deleted because it documents that the computational pipeline can produce a warrant consequence and exposed useful design weaknesses:
- unconstrained REVISE could move to a broader claim;
- overlapping windows could duplicate evidence;
- full A/B packet differences did not isolate PM03.

The final design directly repairs those weaknesses before any final judge output is observed.