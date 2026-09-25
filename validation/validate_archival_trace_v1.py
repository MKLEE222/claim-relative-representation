from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

with open(ROOT/"spec/archival_stance_trace_ontology_v1.csv",newline="",encoding="utf-8") as f:
    ont=list(csv.DictReader(f))
with open(ROOT/"data/paper_money_archival_stance_traces_v1.csv",newline="",encoding="utf-8") as f:
    traces=list(csv.DictReader(f))

allowed={r["trace_type"] for r in ont}
for r in traces:
    if r["trace_type"] not in allowed:
        errors.append(f'{r["trace_id"]}: unknown trace type')
    if r["verification_status"]!="PAGE_VERIFIED":
        errors.append(f'{r["trace_id"]}: PM confirmatory trace must be PAGE_VERIFIED')
    if not r["verbatim_cue"].strip():
        errors.append(f'{r["trace_id"]}: missing source cue')

proto=(ROOT/"experiments/warrant_closure_pm/PROTOCOL_v2.md").read_text(encoding="utf-8")
for term in [
    "Stage C - LLM judge (LAST)",
    "The mandatory independent-human gate is removed.",
    "No human participant study is required",
    "Null retention",
]:
    if term not in proto:
        errors.append(f"protocol missing: {term}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print(f"archival_trace_types={len(ont)}")
print(f"paper_money_traces={len(traces)}")
print("ARCHIVAL_TRACE_LAYER=PASS")
print("LLM_LAST_STAGE_POLICY=PASS")
print("HUMAN_PARTICIPANT_GATE_REMOVED=PASS")
