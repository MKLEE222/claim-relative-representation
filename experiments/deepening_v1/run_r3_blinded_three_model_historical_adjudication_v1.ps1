param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

Write-Host "R3 blinded three-model historical adjudication"
Write-Host "Frozen models: qwen2.5:7b, gemma3:12b, llama3.1:8b"

& $Python -m pip install pymupdf==1.26.4
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $Python experiments/deepening_v1/r3_blinded_three_model_historical_adjudication_v1.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $Python experiments/deepening_v1/analyze_r3_blinded_three_model_historical_adjudication_v1.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Completed."
Write-Host "See experiments/deepening_v1/llm_second_pass_v1/RESULTS_v1.md"
