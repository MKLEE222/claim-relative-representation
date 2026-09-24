from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def rows(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

manifest=rows("spec/holdout_manifest_v1.csv")
cands=rows("spec/external_carrier_candidates_v1.csv")

errors=[]

roles={"DEV","NEAR_HOLDOUT","BOUNDARY","EXTERNAL_HOLDOUT"}
for r in manifest:
    if r["role"] not in roles:
        errors.append(f'{r["episode_id"]}: unknown role')
    if r["role"]!="DEV":
        if r["outcome_status"] not in {"SEALED","OUTCOME_RECORDED"}:
            errors.append(f'{r["episode_id"]}: invalid non-development outcome status {r["outcome_status"]}')
        if r["outcome_status"]=="OUTCOME_RECORDED" and not r["workflow_status"].startswith("EXECUTED"):
            errors.append(f'{r["episode_id"]}: recorded outcome requires EXECUTED workflow status')
    if r["role"]!="DEV" and r["target_visible_to_workflow"].lower()!="no":
        errors.append(f'{r["episode_id"]}: target visible to holdout workflow')

for c in cands:
    if c["outcome_inspected"].lower()!="no":
        errors.append(f'{c["candidate_id"]}: candidate outcome already inspected before selection')

if not any(c["selection_status"].startswith("PRIMARY_CANDIDATE") for c in cands):
    errors.append("no primary external carrier candidate")

print(f"holdout_episodes={len(manifest)}")
print(f"external_candidates={len(cands)}")
if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("HOLDOUT_ROLE_SEAL=PASS")
print("EXTERNAL_SELECTION_LEAKAGE_CHECK=PASS")
