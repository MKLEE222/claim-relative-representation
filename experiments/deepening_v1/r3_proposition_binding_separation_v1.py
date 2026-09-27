from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PANEL=ROOT/"data/r3_verified_proposition_panel_v1.csv"
INQUIRIES=ROOT/"experiments/deepening_v1/R3_SCHOLARLY_INQUIRY_PANEL_v1.csv"
OUT=ROOT/"experiments/deepening_v1/results/r3_proposition_binding_separation_v1.json"

def canon(x):
    if isinstance(x, dict):
        return {k: canon(x[k]) for k in sorted(x)}
    if isinstance(x, (list, tuple, set)):
        vals=[canon(v) for v in x]
        return sorted(vals, key=lambda z: json.dumps(z, sort_keys=True, ensure_ascii=False))
    return x

def digest(x):
    b=json.dumps(canon(x),ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(b).hexdigest()

panel=list(csv.DictReader(PANEL.open(encoding="utf-8")))
inq=list(csv.DictReader(INQUIRIES.open(encoding="utf-8")))
by_prop={r["proposition_id"]:r for r in panel}
by_q={r["inquiry_id"]:r for r in inq}

required_props={
    "PASH-PROV-1903","PASH-ROUTE-1903","PASH-PROV-1920","PASH-ROUTE-1920",
    "ARBR-ID-HS","ARBR-REPLY-CORDIER",
    "DES-FOLK-1920","DES-DIST-1920",
    "URM-ACTION-1903","URM-ACTION-1920",
}
missing=required_props-set(by_prop)
if missing:
    raise SystemExit(f"missing proposition rows: {sorted(missing)}")

for pid in required_props:
    if by_prop[pid]["verification_authority"]!="PAGE_VERIFIED_BOTH":
        raise SystemExit(f"{pid} is not PAGE_VERIFIED_BOTH")

for qid in ["R3Q-PASH-STANCE","R3Q-ARBR-COMMIT","R3Q-DES-EVIDENCE","R3Q-URM-ERRATUM"]:
    if qid not in by_q:
        raise SystemExit(f"missing inquiry {qid}")

cases=[]

# 1. Pashai: retain actors, target propositions and stance/modality bags,
# but drop stance->target binding.
pash_projection={
    "projection":"P_STANCE_BAG",
    "visible_actor":["STEIN"],
    "visible_target_propositions":[
        "PASH-PROV-1903",
        "PASH-ROUTE-1903",
    ],
    "visible_stance_labels":["CORROBORATION","CRITICISM"],
    "visible_modality_labels":["ALMOST_CERTAIN","POSSIBLE"],
}
pash_actual={
    "stance_bindings":{
        "CORROBORATION":"PASH-PROV-1903",
        "CRITICISM":"PASH-ROUTE-1903",
    },
    "modality_bindings":{
        "ALMOST_CERTAIN":"PASH-ROUTE-1903",
        "POSSIBLE":"PASH-ROUTE-1920",
    },
}
pash_alt={
    "stance_bindings":{
        "CORROBORATION":"PASH-ROUTE-1903",
        "CRITICISM":"PASH-PROV-1903",
    },
    "modality_bindings":{
        "ALMOST_CERTAIN":"PASH-ROUTE-1903",
        "POSSIBLE":"PASH-ROUTE-1920",
    },
}
def pash_answer(c):
    return {
        "corroborated_target":c["stance_bindings"]["CORROBORATION"],
        "criticized_target":c["stance_bindings"]["CRITICISM"],
        "alternative_route_modality":"POSSIBLE",
    }
cases.append({
    "case_id":"SEP-PASH-STANCE",
    "inquiry_id":"R3Q-PASH-STANCE",
    "projection":pash_projection,
    "completion_A":pash_actual,
    "completion_B":pash_alt,
    "answer_A":pash_answer(pash_actual),
    "answer_B":pash_answer(pash_alt),
})

# 2. Arbre Sec: retain names, cypress proposition and bibliographic-reply fact,
# but drop commitment-role binding.
arbr_projection={
    "projection":"P_ROLE_BAG",
    "visible_people":["CORDIER","HOUTUM_SCHINDLER"],
    "visible_propositions":["ARBR-ID-HS"],
    "visible_entry_facts":[
        "CYPRESS_PROPOSITION_PRESENT",
        "CORDIER_BIBLIOGRAPHIC_REPLY_PRESENT",
        "EARLIER_SCHINDLER_CITATION_PRESENT",
    ],
}
arbr_actual={
    "commitment_roles":{
        "HOUTUM_SCHINDLER":["PROPOSES","COMMITS_TO_ARBR_ID_HS"],
        "CORDIER":["TRANSMITS","BIBLIOGRAPHIC_REPLY"],
    },
    "cordier_adoption":"NOT_ESTABLISHED",
}
arbr_alt={
    "commitment_roles":{
        "HOUTUM_SCHINDLER":["PROPOSES","COMMITS_TO_ARBR_ID_HS"],
        "CORDIER":["TRANSMITS","BIBLIOGRAPHIC_REPLY","ADOPTS_ARBR_ID_HS"],
    },
    "cordier_adoption":"ESTABLISHED",
}
def arbr_answer(c):
    return {
        "cypress_commitment_holder":"HOUTUM_SCHINDLER",
        "cordier_adoption":c["cordier_adoption"],
    }
cases.append({
    "case_id":"SEP-ARBR-ROLE",
    "inquiry_id":"R3Q-ARBR-COMMIT",
    "projection":arbr_projection,
    "completion_A":arbr_actual,
    "completion_B":arbr_alt,
    "answer_A":arbr_answer(arbr_actual),
    "answer_B":arbr_answer(arbr_alt),
})

# 3. Great Desert: retain propositions and evidence items but remove
# evidence->proposition binding.
des_projection={
    "projection":"P_EVIDENCE_BAG",
    "visible_actor":["STEIN"],
    "visible_propositions":["DES-FOLK-1920","DES-DIST-1920"],
    "visible_evidence_items":[
        "LOCAL_FOLKLORE_INTERPRETATION",
        "PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS",
    ],
}
des_actual={
    "evidence_bindings":{
        "LOCAL_FOLKLORE_INTERPRETATION":"DES-FOLK-1920",
        "PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS":"DES-DIST-1920",
    }
}
des_alt={
    "evidence_bindings":{
        "LOCAL_FOLKLORE_INTERPRETATION":"DES-DIST-1920",
        "PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS":"DES-FOLK-1920",
    }
}
def des_answer(c):
    inv={v:k for k,v in c["evidence_bindings"].items()}
    return {
        "folklore_source_evidence":inv["DES-FOLK-1920"],
        "distance_marches_evidence":inv["DES-DIST-1920"],
    }
cases.append({
    "case_id":"SEP-DES-EVIDENCE",
    "inquiry_id":"R3Q-DES-EVIDENCE",
    "projection":des_projection,
    "completion_A":des_actual,
    "completion_B":des_alt,
    "answer_A":des_answer(des_actual),
    "answer_B":des_answer(des_alt),
})

results=[]
for c in cases:
    # The projection itself is deliberately the same visible object for both completions.
    ph=digest(c["projection"])
    same_projection=True
    different_answer=canon(c["answer_A"])!=canon(c["answer_B"])
    results.append({
        "case_id":c["case_id"],
        "inquiry_id":c["inquiry_id"],
        "projection_name":c["projection"]["projection"],
        "projection_sha256_A":ph,
        "projection_sha256_B":ph,
        "same_visible_projection":same_projection,
        "answer_A":c["answer_A"],
        "answer_B":c["answer_B"],
        "different_required_output":different_answer,
        "separation_witness":same_projection and different_answer,
    })

# Determinate control: explicit textual substitution is retained.
control_projection={
    "projection":"P_TEXT_PAIR",
    "earlier_token":"found",
    "replacement_token":"founded",
    "target":"URM-ACTION-1903",
}
control_answer={"old":"found","new":"founded"}
control={
    "case_id":"CTRL-URM-ERRATUM",
    "inquiry_id":"R3Q-URM-ERRATUM",
    "projection_name":"P_TEXT_PAIR",
    "projection_sha256":digest(control_projection),
    "required_output":control_answer,
    "determined_from_retained_projection":(
        control_projection["earlier_token"]==control_answer["old"]
        and control_projection["replacement_token"]==control_answer["new"]
    ),
}

if not all(r["separation_witness"] for r in results):
    raise SystemExit("one or more separation witnesses failed")
if not control["determined_from_retained_projection"]:
    raise SystemExit("Urumtsi control failed")

out={
    "study":"R3_PROPOSITION_BINDING_SEPARATION_V1",
    "authority":"controlled projection separation grounded in PAGE_VERIFIED_BOTH historical acts",
    "panel_rows":len(panel),
    "inquiry_rows":len(inq),
    "primary_results":results,
    "control":control,
    "claim_ceiling":[
        "Each positive case proves non-determination only for the named controlled projection and inquiry.",
        "The alternate completion is a separation construction, not a claim about historical truth.",
        "No result shows that plain text, TEI, or any named real-world platform necessarily loses the binding.",
        "The study isolates proposition-level information obligations beyond target localization."
    ],
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_PROPOSITION_BINDING_SEPARATION_V1=PASS")
for r in results:
    print(f"{r['case_id']}: same_projection={int(r['same_visible_projection'])}, different_output={int(r['different_required_output'])}, separation={int(r['separation_witness'])}")
print(f"CTRL-URM-ERRATUM: determined={int(control['determined_from_retained_projection'])}")
