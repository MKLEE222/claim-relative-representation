from __future__ import annotations
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

protocol=(ROOT/"experiments/warrant_closure_final/PROTOCOL.md").read_text(encoding="utf-8")
manual=(ROOT/"coding/EPISTEMIC_ADJUDICATION_MANUAL_v2.md").read_text(encoding="utf-8")
prompt=(ROOT/"experiments/warrant_closure_final/judge_prompt_v2.txt").read_text(encoding="utf-8")
stability=(ROOT/"experiments/warrant_closure_final/STABILITY_CONTRACT.md").read_text(encoding="utf-8")
builder=(ROOT/"experiments/warrant_closure_final/build_packets.py").read_text(encoding="utf-8")
schema=json.loads((ROOT/"experiments/warrant_closure_final/judge_output_schema_v2.json").read_text(encoding="utf-8"))

if "C_PM_ATOMIC" not in protocol:
    errors.append("atomic claim id missing")
if "B_final = min(|U_G|, |U_S|)" not in protocol:
    errors.append("equal unique-unit budget rule missing")
for name in ["GENERIC_RESCUE_PM03","GENERIC_SHAM","GUIDED_REMOVE_PM03"]:
    if name not in protocol or name not in stability:
        errors.append(f"selective control missing: {name}")

states=set(schema["properties"]["warrant_state"]["enum"])
if states!={"RETAIN","DEFER","WITHHOLD"}:
    errors.append(f"final warrant-state set drift: {states}")

for rel in [
    "E_SUPPORT","E_UNDERCUT","E_QUALIFY_AUTHORITY",
    "E_REHABILITATE","E_ACCRETION","E_IDENTIFICATION_UPDATE","E_UNRESOLVED"
]:
    if rel not in prompt or rel not in manual:
        errors.append(f"epistemic definition missing: {rel}")

if "Do not substitute a broader claim" not in prompt:
    errors.append("atomic no-broader-claim instruction missing")

if 'B_FINAL=6' not in builder:
    errors.append("audited final unique-unit budget not frozen at 6")

for pid in ["K4N","R8Q","M3V","H7C","T2P"]:
    if pid not in builder:
        errors.append(f"opaque packet id missing: {pid}")

for leak in ["contains_pm03","member_token_starts","char_start","char_end","excerpt_sha256"]:
    if f'"{leak}"' not in builder:
        errors.append(f"builder no longer explicitly audits leakage field: {leak}")

if "fresh/stateless or model-separated" not in stability:
    errors.append("independent final replication requirement missing")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("FINAL_ATOMIC_CLAIM=PASS")
print("UNIQUE_EVIDENCE_UNIT_BUDGET=6")
print("SELECTIVE_RESCUE_SHAM_REMOVAL=PASS")
print("FINAL_WARRANT_STATES=RETAIN|DEFER|WITHHOLD")
print("EPISTEMIC_DEFINITIONS_EMBEDDED=PASS")
print("JUDGE_VISIBLE_LEAKAGE_GUARD=PASS")
print("FINAL_LLM_REPLICATION_GATE=PASS")
