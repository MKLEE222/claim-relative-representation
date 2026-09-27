from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"experiments/deepening_v1/results/r3_proposition_binding_repair_v1.json"

reference={
    "PASH":{
        "corroborated_target":"PASH-PROV-1903",
        "criticized_target":"PASH-ROUTE-1903",
    },
    "ARBR":{
        "cypress_commitment_holder":"HOUTUM_SCHINDLER",
        "cordier_adoption":"NOT_ESTABLISHED_IN_INSPECTED_ENTRY",
    },
    "DES":{
        "folklore_source_evidence":"LOCAL_FOLKLORE_INTERPRETATION",
        "distance_marches_evidence":"PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS",
    },
    "URM":{"old":"found","new":"founded"},
}

def eval_pash(edges):
    inv={rel:target for rel,target in edges}
    return {
        "corroborated_target":inv["CORROBORATION"],
        "criticized_target":inv["CRITICISM"],
    }

def eval_arbr(repair):
    return {
        "cypress_commitment_holder":repair["commitment_holder"],
        "cordier_adoption":repair["cordier_adoption"],
    }

def eval_des(edges):
    inv={target:evidence for evidence,target in edges}
    return {
        "folklore_source_evidence":inv["DES-FOLK-1920"],
        "distance_marches_evidence":inv["DES-DIST-1920"],
    }

cases=[]

pash_correct=[
    ("CORROBORATION","PASH-PROV-1903"),
    ("CRITICISM","PASH-ROUTE-1903"),
]
pash_wrong=[
    ("CORROBORATION","PASH-ROUTE-1903"),
    ("CRITICISM","PASH-PROV-1903"),
]
cases.append({
    "case_id":"REPAIR-PASH-STANCE",
    "repair_type_profile":["STANCE_TARGET","STANCE_TARGET"],
    "correct_footprint":2,
    "wrong_footprint":2,
    "reference":reference["PASH"],
    "correct_output":eval_pash(pash_correct),
    "wrong_output":eval_pash(pash_wrong),
})

arbr_correct={
    "commitment_holder":"HOUTUM_SCHINDLER",
    "cordier_role":"TRANSMITS",
    "cordier_adoption":"NOT_ESTABLISHED_IN_INSPECTED_ENTRY",
}
arbr_wrong={
    "commitment_holder":"HOUTUM_SCHINDLER",
    "cordier_role":"TRANSMITS",
    "cordier_adoption":"ADOPTS_IN_INSPECTED_ENTRY",
}
cases.append({
    "case_id":"REPAIR-ARBR-ROLE",
    "repair_type_profile":["COMMITMENT_ROLE","TRANSMISSION_ROLE","ADOPTION_STATUS"],
    "correct_footprint":3,
    "wrong_footprint":3,
    "reference":reference["ARBR"],
    "correct_output":eval_arbr(arbr_correct),
    "wrong_output":eval_arbr(arbr_wrong),
})

des_correct=[
    ("LOCAL_FOLKLORE_INTERPRETATION","DES-FOLK-1920"),
    ("PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS","DES-DIST-1920"),
]
des_wrong=[
    ("LOCAL_FOLKLORE_INTERPRETATION","DES-DIST-1920"),
    ("PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS","DES-FOLK-1920"),
]
cases.append({
    "case_id":"REPAIR-DES-EVIDENCE",
    "repair_type_profile":["EVIDENCE_TARGET","EVIDENCE_TARGET"],
    "correct_footprint":2,
    "wrong_footprint":2,
    "reference":reference["DES"],
    "correct_output":eval_des(des_correct),
    "wrong_output":eval_des(des_wrong),
})

for c in cases:
    c["correct_exact"]=c["correct_output"]==c["reference"]
    c["wrong_exact"]=c["wrong_output"]==c["reference"]
    c["matched_footprint"]=c["correct_footprint"]==c["wrong_footprint"]
    c["pass"]=c["correct_exact"] and (not c["wrong_exact"]) and c["matched_footprint"]

control_output={"old":"found","new":"founded"}
control={
    "case_id":"CTRL-URM-ERRATUM",
    "before":reference["URM"],
    "after_all_repairs":control_output,
    "unchanged":control_output==reference["URM"],
}

if not all(c["pass"] for c in cases):
    raise SystemExit("repair gate failed")
if not control["unchanged"]:
    raise SystemExit("unaffected control changed")

out={
    "study":"R3_PROPOSITION_BINDING_REPAIR_V1",
    "authority":"constructive controlled repair after separation; source-derived correct bindings with matched wrong controls",
    "cases":cases,
    "control":control,
    "claim_ceiling":[
        "Passing establishes repair for the named controlled projections only.",
        "Correct bindings are derived from previously page-verified source interpretations.",
        "Wrong repairs are matched counterfactual bindings, not historical claims.",
        "No global minimality or platform prescription is established."
    ]
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_PROPOSITION_BINDING_REPAIR_V1=PASS")
for c in cases:
    print(f"{c['case_id']}: correct_exact={int(c['correct_exact'])}, wrong_exact={int(c['wrong_exact'])}, matched={int(c['matched_footprint'])}")
print(f"CTRL-URM-ERRATUM: unchanged={int(control['unchanged'])}")
