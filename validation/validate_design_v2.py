from __future__ import annotations
import csv, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def rows(p):
    with open(ROOT/p,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

tasks=rows("spec/task_contracts_v2.csv")
facts=rows("spec/transformation_task_factorial_v2.csv")
inv=rows("spec/transformation_invariants_v1.csv")

errors=[]

task_ids={r["task_id"] for r in tasks}
trans_ids={r["transformation_id"] for r in inv}
coord={r["transformation_id"]:r["primary_changed_coordinate"] for r in inv}

allowed_dist={
"text_presence","referent_identity","attribution","temporal_order","claim_binding",
"evidence_relation","witness_identity","editorial_layer","distinction_class"
}

for t in tasks:
    cand={x for x in t["candidate_distinctions"].split("|") if x}
    hyp={x for x in t["hypothesized_dependencies"].split("|") if x}
    if not hyp <= cand:
        errors.append(f'{t["task_id"]}: hypothesis not subset of candidate distinctions')
    bad=cand-allowed_dist
    if bad:
        errors.append(f'{t["task_id"]}: unknown candidate distinctions {sorted(bad)}')
    q=t["question"].lower()
    if re.search(r"retain|revise|defer|withhold|rehabilitat|accret",q):
        errors.append(f'{t["task_id"]}: task question leaks downstream answer language')
    if t["outcome_sealed"].lower()!="yes":
        errors.append(f'{t["task_id"]}: outcome is not sealed')

for f in facts:
    if f["task_id"] not in task_ids:
        errors.append(f'{f["block_id"]}: unknown task')
    if f["transformation_id"] not in trans_ids:
        errors.append(f'{f["block_id"]}: unknown transformation')
    if f["transformation_id"]=="TD_NORMALIZE" and f["phase"]=="main_effect":
        errors.append(f'{f["block_id"]}: TD_NORMALIZE cannot enter main-effect block before semantic audit')
    if f["transformation_id"]=="TA_EXTERNAL" and f["phase"]!="sensitivity":
        errors.append(f'{f["block_id"]}: TA_EXTERNAL is sensitivity-only in v2')

print(f"task_contracts={len(tasks)}")
print(f"factorial_cells={len(facts)}")
print(f"typed_transformations={len(inv)}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("TASK_CONTRACT_V2=PASS")
print("FACTORIAL_APPLICABILITY_SCHEMA=PASS")
print("OUTCOME_SEAL_CHECK=PASS")
