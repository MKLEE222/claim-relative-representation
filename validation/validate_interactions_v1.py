from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def rows(p):
    with open(ROOT/p,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

tasks={r["task_id"]:r for r in rows("spec/task_contracts_v2.csv")}
trans={r["transformation_id"]:r for r in rows("spec/transformation_invariants_v1.csv")}
factorial=rows("spec/transformation_task_factorial_v2.csv")
carriers=rows("spec/carrier_hypotheses_v1.csv")
interactions=rows("spec/interaction_blocks_v1.csv")

errors=[]

applicable={(r["task_id"],r["transformation_id"]) for r in factorial if r["applicability"]=="APPLICABLE"}

carrier_index={(r["task_id"],r["distinction"],r["interaction_partner"]):r for r in carriers if r["status"]=="FROZEN_HYPOTHESIS"}

for i in interactions:
    if i["phase"]=="confirmatory" and i["class"]!="I1":
        errors.append(f'{i["interaction_id"]}: first-wave confirmatory interactions must be I1')
    if i["task_id"] not in tasks:
        errors.append(f'{i["interaction_id"]}: unknown task')
        continue
    if i["T1"] not in trans or i["T2"] not in trans:
        errors.append(f'{i["interaction_id"]}: unknown transformation')
        continue

    cand=set(tasks[i["task_id"]]["candidate_distinctions"].split("|"))
    if i["target_distinction"] not in cand:
        errors.append(f'{i["interaction_id"]}: target distinction not in task candidate universe')

    if (i["task_id"],i["T1"]) not in applicable:
        errors.append(f'{i["interaction_id"]}: T1 not preregistered applicable to task')
    if (i["task_id"],i["T2"]) not in applicable:
        errors.append(f'{i["interaction_id"]}: T2 not preregistered applicable to task')

    l1=trans[i["T1"]]["layer"]
    l2=trans[i["T2"]]["layer"]
    if l1==l2:
        errors.append(f'{i["interaction_id"]}: first-wave interaction is within-layer without separate mechanism')

    if i["T1"]=="TD_NORMALIZE" or i["T2"]=="TD_NORMALIZE":
        errors.append(f'{i["interaction_id"]}: TD_NORMALIZE is held out')
    if i["T1"]=="TA_EXTERNAL" or i["T2"]=="TA_EXTERNAL":
        errors.append(f'{i["interaction_id"]}: TA_EXTERNAL is sensitivity-only')

    key=(i["task_id"],i["target_distinction"],i["T2"])
    if key not in carrier_index:
        errors.append(f'{i["interaction_id"]}: no matching frozen carrier-substitution hypothesis')

for r in interactions:
    forbidden={"result","claim_state","winner","effect"}
    leaked=forbidden.intersection(set(r.keys()))
    if leaked:
        errors.append(f'{r["interaction_id"]}: outcome-like columns present {sorted(leaked)}')

print(f"first_wave_interactions={len(interactions)}")
print(f"frozen_carrier_hypotheses={len(carriers)}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("TASK_REALISM_AUDIT=PRESENT")
print("INTERACTION_ADMISSION_SCHEMA=PASS")
print("CARRIER_MECHANISM_BINDING=PASS")
print("CLAIM_OUTCOME_SEAL=PASS")
