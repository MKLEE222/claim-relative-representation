# Final Blind LLM Judge — Three-Model Negative Result

Date: 2026-09-26
Status: FINAL FOR THE FROZEN LLM-JUDGE EXPERIMENT

## Frozen input

`judge_calls_v1.jsonl` SHA-256:
`cf8a9853eb8281db3e77d2dfe742f0b89063d5a21cb02a18251f1a086e88536c`

User-supplied complete local result archive SHA-256:
`4d83876d90ac5e1a7417706d0137ef7cc767c470b5b17e113f5b5a65a27ad850`

Execution environment:
- Ollama 0.18.2
- temperature 0
- seed 20260926
- context 16384
- max generation 1024
- each frozen record executed in an independent request
- 45 / 45 outputs passed structural validation

## Model outcomes

| Model | Frozen-gate outcome |
|---|---|
| qwen2.5:7b | MODEL_SENSITIVE: opaque packet H7C changed WITHHOLD / RETAIN / WITHHOLD across frozen perturbations |
| gemma3:12b | STABLE_NO_PACKET_CONTRAST: all five opaque packets RETAIN under all perturbations |
| llama3.1:8b | STABLE_NO_PACKET_CONTRAST: all five opaque packets RETAIN under all perturbations |

## Confirmatory disposition

The preregistered selective-restoration LLM claim is NOT SUPPORTED.

No prompt, packet, donor, state vocabulary, or pass criterion is changed to rescue this experiment.

Qwen fails the predeclared stability gate.
Gemma and Llama pass stability but cannot satisfy selective restoration because all packet states are identical.

## Diagnostic failure mode

The stable models repeatedly treat PM01's direct assertion as sufficient for RETAIN even when PM02 explicitly contests the material identification.

Several rationales characterize the PM02 botanical objection as merely qualifying or not negating Polo's mulberry identification.

This shows that the tested off-the-shelf LLM adjudicators do not reliably implement the intended defeasible relation:

`assertion + undefeated explicit objection != assertion + defeated objection`.

That instrument failure is preserved as a negative result rather than repaired post hoc.

## Claim ceiling

This result does NOT falsify the already established access / documentary / archival-trace differences.

It falsifies the stronger measurement strategy:

> these three frozen local LLM judges can serve as stable categorical warrant instruments for the final selective-restoration test.

No claim about human historian judgment follows.