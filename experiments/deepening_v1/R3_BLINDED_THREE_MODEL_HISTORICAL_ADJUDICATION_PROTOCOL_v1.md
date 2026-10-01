# R3 Blinded Three-Model Historical Adjudication Protocol v1

Date frozen: 2026-09-27
Status: PRE-OUTCOME REPLACEMENT FOR UNAVAILABLE SECOND-HUMAN REVIEW

## Resource constraint and gate redesign

This project is being executed by one human researcher. A second independent human historical reviewer is not available.

The previous human-review packet remains preserved as an optional future validation asset, but Track-A closure no longer requires an unavailable second person.

The replacement gate is:

BLINDED_MODEL_SEPARATED_HISTORICAL_ADJUDICATION.

This is not described as human validation.

## Scientific purpose

The test asks whether the five load-bearing historical readings are reproducible under source-only, answer-blinded adjudication by heterogeneous local language models.

The models do not evaluate the computational experiments.
They perform bounded historical extraction and relation adjudication from the sealed source pages.

This deliberately differs from the earlier warrant-judge experiment, which asked models to implement an abstract defeasible warrant state and produced a model-sensitive/null result.

## Models

Default frozen local panel:

- qwen2.5:7b
- gemma3:12b
- llama3.1:8b

All three were previously available in the project's Ollama environment and are retained to avoid post-result model shopping.

If one model is unavailable at execution time, the run stops rather than silently substituting another model.

## Source-only input

For every call the model receives only:

- one frozen historical question;
- the exact source-page text from the already sealed 1903/1920 page set;
- an answer-neutral list of atomic fields to extract;
- symmetric allowed values for those fields;
- output schema.

The model does not receive:

- data/r3_verified_proposition_panel_v1.csv;
- registered answers;
- required_output;
- required_bindings;
- controlled projection results;
- repair results;
- AW1/AW2 ranks;
- claim ledger;
- expected agreement pattern;
- other models' outputs.

## Cases

All five cases are mandatory:

- R3Q-PASH-STANCE
- R3Q-ARBR-COMMIT
- R3Q-DES-EVIDENCE
- R3Q-URM-ERRATUM
- R3Q-TUN-CONTROVERSY

No favorable subset may be reported as the main result.

## Atomic fields

The 21 comparison dimensions are frozen in:

R3_SECOND_PASS_ATOMIC_COMPONENTS_v1.csv

The LLM-facing schema uses the same dimensions but not the registered values.

Each field is answered with a normalized value from a symmetric case-specific choice set plus:

UNRESOLVED.

The model must also return:
- source page label(s);
- a short exact supporting phrase;
- component confidence HIGH / MEDIUM / LOW.

## Perturbations

Every case is executed under three semantically equivalent prompt forms:

### P0_CANONICAL
Question first; source pages in chronological/page order.

### P1_SOURCES_FIRST
Same page order and same evidence; sources appear before the question.

### P2_REVERSE_PAGE_ORDER
Question first; identical source pages shown in reverse order. Explicit year/page labels remain unchanged.

No content is added or removed across perturbations.

Purpose:
detect order/framing sensitivity without changing the evidence contract.

## Call count

5 cases x 3 perturbations x 3 models = 45 independent calls.

Every call is stateless.

Execution parameters:
- Ollama
- temperature = 0
- seed = 20260927
- num_ctx = 16384
- num_predict = 1600
- no conversation history
- structured JSON output requested

No prompt or option set may be changed after any outcome is opened.

## Stability

For component c and model m:

MODEL_STABLE(m,c)=1

iff the normalized value is identical across P0, P1 and P2.

A model that changes value across perturbations is MODEL_SENSITIVE for that component.

Only stable model values enter ensemble consensus.

## Ensemble consensus

For component c:

ENSEMBLE_CONSENSUS(c)=v

iff at least two of the three models are stable and return the same non-UNRESOLVED value v.

Otherwise:

NO_CONSENSUS.

The third model may disagree; that disagreement remains reported.

## Comparison to sealed historical reading

The registered answer is opened only by the post-run analyzer after all 45 raw outputs are frozen.

For each atomic component:

- MATCH: ensemble consensus equals the sealed normalized value;
- CONTRADICTION: ensemble consensus exists and differs;
- NO_CONSENSUS: no stable two-model consensus;
- CONSENSUS_UNRESOLVED: stable consensus is UNRESOLVED.

No post-outcome answer normalization may be invented.
The normalized answer key is frozen in the analyzer before execution and each key points back to proposition-panel row IDs.

## Gate disposition

### BLINDED_MODEL_REPLICATION_PASS

All 21 components:
- have stable ensemble consensus;
- match the sealed historical reading;
- contain source-grounded evidence citations.

Then Gate II may close as:

SOURCE-GROUNDED BLINDED MODEL REPLICATION PASS.

This does not license a claim of human historian agreement.

### BOUNDED_PARTIAL

No component contradicts the sealed reading, but one or more components lack stable consensus or remain unresolved.

Affected manuscript claims are downgraded or marked unresolved.
Unaffected components remain usable.

### HISTORICAL_READING_REOPENED

Any stable ensemble consensus contradicts a sealed load-bearing component.

The affected historical claim is reopened.
Its dependent controlled experiment is not discarded numerically, but its historical interpretation cannot be frozen until the discrepancy is resolved from source evidence.

No prompt retuning is permitted to rescue the component.

## Claim ceiling

Supported if passed:

> The load-bearing historical readings were reproduced under sealed, source-only, answer-blinded adjudication by three heterogeneous local language models with perturbation stability checks.

Not supported:

- independent human validation;
- historian consensus;
- human inter-annotator reliability;
- general LLM reliability for historical scholarship;
- replacement of expert historical judgment in other tasks.

## Human review status

The existing blinded human-review bundle is preserved.

A future human reviewer would be an optional external validation layer, not a prerequisite for the current single-researcher project.
