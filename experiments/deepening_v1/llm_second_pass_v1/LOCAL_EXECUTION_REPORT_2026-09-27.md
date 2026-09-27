# R3 blinded historical adjudication — local execution report

Date: 2026-09-27 (Asia/Shanghai)

## Frozen run identity

- Repository: `MKLEE222/claim-relative-representation`
- Branch: `audit/cold-start-20260926`
- Commit: `4175b736af514b4515e4db4ed8ccfedcf43872df`
- Protocol: `R3_BLINDED_THREE_MODEL_HISTORICAL_ADJUDICATION_PROTOCOL_v1`
- Models: `qwen2.5:7b`, `gemma3:12b`, `llama3.1:8b`
- Ollama: 0.18.2; model directory `D:\ollama\models`
- PyMuPDF: 1.26.4, isolated in the D-drive work directory
- Fixed source PDF SHA-256 values: 1903 `6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7`; 1920 `dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941`
- Unique source pages: 18
- Parameters: temperature 0; seed 20260927; context 16384; prediction limit 1600; one stateless request per call
- Resource guard: `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NUM_PARALLEL=1`, model store on D drive; no visible Ollama window

## Frozen execution outcome

All 45 planned calls were recorded, with 15 per model. Every request ended with `done_reason=stop`; all 45 responses parsed as JSON; no execution error was recorded. The runner marked 9 calls schema-valid and 36 schema-invalid. No prompt, model, source page, atomic field, answer key, or output was changed after any response was opened. No call was repeated.

`raw_results_v1.jsonl` SHA-256:
`d648a61b6ef6ecaaf50e0d25de27538233a0eff68c869750338aaba82fb4e248`

The frozen analyzer returns:

- `gate_disposition`: `BOUNDED_PARTIAL`
- `MATCH`: 0
- `CONTRADICTION`: 0
- `NO_CONSENSUS`: 21
- `CONSENSUS_UNRESOLVED`: 0
- strict stable components: Qwen 1/21; Gemma 0/21; Llama 0/21
- `analysis_v1.json` SHA-256: `70b9971933fedaf3628153c8838881c503a0cb7a976e17f3c843a6b31d587730`

Interpretation: the registered Gate II has **not closed**. The absence of a registered contradiction is not positive confirmation because no atomic component reached a valid two-model source-cited consensus.

## Post-freeze diagnostic only

The 36 invalid calls were caused by citation validation, not JSON parsing or Ollama execution. Across the invalid calls, 111 field-level errors concerned a supporting quote missing from its cited extracted page and 47 concerned a page label that did not exactly match the long frozen label including PDF index. These are field-level counts, not counts of separate calls.

For a sensitivity diagnosis only, if all parsed normalized values are considered while ignoring the frozen citation-validity gate, 9 of 21 fields would match the sealed reading by stable two-model consensus, 11 would have no consensus, and 1 would contradict it. The single label-only contradiction is the Urumtsi `correction_direction`: Qwen and Llama consistently chose `FOUNDED_TO_FOUND`, while the sealed value and Gemma chose `FOUND_TO_FOUNDED`. Some individual outputs choose the latter direction's endpoints yet reverse the direction label. This is an output-consistency warning, not an authorized change to the confirmatory Gate-II disposition.

The quoted correction and earlier-page evidence remain the proper basis for historical adjudication. Do not retroactively relax citation validation or rerun the same frozen calls to obtain a positive gate.

## Windows line-ending transport note

The first analyzer attempt refused to open the sealed panel because Windows Git checkout converted the CSV worktree copy to CRLF. Its repository blob SHA was already the expected `f1ffa2aefde17f731fc9d0a19781aed81c94622c`. The local copy was restored byte-for-byte to the LF Git blob, without changing any row or answer; the unchanged frozen analyzer then ran successfully. The original model outputs and their SHA-256 were unaffected.

The result directory uses a local `.gitattributes` rule to preserve its files byte-for-byte in Git. This prevents Windows line-ending normalization from changing the frozen JSONL/JSON hashes when the run is published.

## Claim ceiling

This is a complete frozen execution and a bounded partial result for the predeclared three-model instrument. It supplies no independent human validation and no successful model-separated replication of all 21 historical components. The previous three-model paper-money warrant null remains a separate experiment.

The run was performed in a D-drive local checkout. The frozen outputs and this report were subsequently prepared for publication on the project's GitHub audit branch; no model call or analysis result was changed for that publication.
