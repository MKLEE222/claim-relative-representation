from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

FORBIDDEN_STAGE_A={
    "SUPPORT","CHALLENGE","UNDERCUT","QUALIFY","REHABILIT",
    "ACCRET","RETAIN","REVISE","DEFER","WITHHOLD"
}

def rows(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

doc=rows("spec/documentary_relation_ontology_v1.csv")
epi=rows("spec/epistemic_adjudication_ontology_v1.csv")
tasks=rows("spec/task_contracts_v3.csv")
ref=rows("spec/paper_money_documentary_reference_v1.csv")

for r in doc:
    if r["stage"]!="A":
        errors.append(f'{r["relation_id"]}: documentary stage drift')
    text=(r["name"]+" "+r["definition"]).upper()
    for token in FORBIDDEN_STAGE_A:
        if token in text:
            errors.append(f'{r["relation_id"]}: Stage-A epistemic token {token}')

for r in epi:
    if r["stage"]!="B":
        errors.append(f'{r["relation_id"]}: epistemic stage drift')
    if r["representation_transformable"].lower()!="no":
        errors.append(f'{r["relation_id"]}: epistemic label marked transformable')

doc_ids={r["relation_id"] for r in doc}
epi_ids={r["relation_id"] for r in epi}

for r in tasks:
    if r["stage"]=="A":
        blob=(r["question"]+" "+r["candidate_documentary_distinctions"]+" "+r["admissible_outputs"]).upper()
        for token in FORBIDDEN_STAGE_A:
            if token in blob:
                errors.append(f'{r["task_id"]}: Stage-A task leaks epistemic token {token}')
        if "E_" in r["admissible_outputs"]:
            errors.append(f'{r["task_id"]}: Stage-A output includes E_ label')
    elif r["stage"]=="B":
        deps=[x for x in r["hypothesized_dependencies"].split("|") if x]
        for d in deps:
            if d not in doc_ids:
                errors.append(f'{r["task_id"]}: Stage-B dependency {d} not documentary ontology')
        outs=[x for x in r["admissible_outputs"].split("|") if x]
        for o in outs:
            if o not in epi_ids:
                errors.append(f'{r["task_id"]}: unknown Stage-B output {o}')
    else:
        errors.append(f'{r["task_id"]}: unknown stage {r["stage"]}')

for r in ref:
    if r["relation_type"] not in doc_ids:
        errors.append(f'{r["ref_id"]}: reference relation not in documentary ontology')
    if r["epistemic_label_present"].lower()!="no":
        errors.append(f'{r["ref_id"]}: epistemic label leaked into documentary reference')

tax=(ROOT/"spec/TRANSFORMATION_TAXONOMY_v2.md").read_text(encoding="utf-8")
if "TR_EVIDENCE" not in tax or "prohibited" not in tax.lower():
    errors.append("taxonomy must explicitly prohibit legacy TR_EVIDENCE")
if "No Stage-B output is a legal transformation coordinate." not in tax:
    errors.append("taxonomy missing Stage-B transformation prohibition")

print(f"documentary_relations={len(doc)}")
print(f"epistemic_relations={len(epi)}")
print(f"task_contracts_v3={len(tasks)}")
print(f"paper_money_documentary_refs={len(ref)}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("GD_GE_SEPARATION=PASS")
print("STAGE_A_EPISTEMIC_LEAKAGE=PASS")
print("STAGE_B_TRANSFORMATION_PROHIBITION=PASS")
print("PM_DOCUMENTARY_REFERENCE=PASS")
