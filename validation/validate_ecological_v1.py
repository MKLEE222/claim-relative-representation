from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def rows(p):
    with open(ROOT/p,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

reps=rows("spec/representation_provenance_v1.csv")
entries=rows("spec/task_entry_states_v1.csv")

errors=[]

allowed_classes={"N","W","C","R"}
for r in reps:
    if r["class"] not in allowed_classes:
        errors.append(f'{r["representation_id"]}: invalid class {r["class"]}')
    if r["class"]=="R" and "Tier 1" in r["claim_ceiling"]:
        errors.append(f'{r["representation_id"]}: reference reconstruction cannot support ecological Tier 1 claims')
    if r["class"]=="C" and r["claim_ceiling"]!="Tier 2":
        errors.append(f'{r["representation_id"]}: controlled projection claim ceiling must be Tier 2')
    if r["class"]=="W" and "Tier 3" not in r["claim_ceiling"]:
        errors.append(f'{r["representation_id"]}: workflow replay must explicitly require convergence for Tier 3')

for e in entries:
    if e["task_block"]=="access" and "locator" in e["provided_by_experiment"].lower():
        errors.append(f'{e["entry_id"]}: access task leaks the target locator')
    if e["task_block"]=="relation" and "endpoints" not in e["provided_by_experiment"].lower():
        errors.append(f'{e["entry_id"]}: relation task must declare endpoints supplied')

print(f"representation_provenance_rows={len(reps)}")
print(f"task_entry_states={len(entries)}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("ECOLOGICAL_PROVENANCE_SCHEMA=PASS")
print("ANTI_IDEALIZATION_CLAIM_CEILINGS=PASS")
print("TASK_ENTRY_STAGE_BOUNDARIES=PASS")
