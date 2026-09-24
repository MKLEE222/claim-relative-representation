from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def rows(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

materials=rows("spec/external_dh_materials_v1.csv")
sources=rows("spec/external_dh_sources_v1.csv")

errors=[]
ids={r["material_id"] for r in materials}

required={"P1_FV","P2_WW","P3_FAUST","P4_ELTEC","P5_SCRIVENER"}
missing=required-ids
if missing:
    errors.append(f"missing required external material roles: {sorted(missing)}")

independent={r["material_id"] for r in materials if r["independent_of_this_study"]=="yes"}
for mid in ("P1_FV","P2_WW","P3_FAUST","P4_ELTEC"):
    if mid not in independent:
        errors.append(f"{mid}: must remain independent of this study")

roles=[r["portfolio_role"] for r in materials]
if len(roles)!=len(set(roles)):
    errors.append("portfolio roles must be unique")

for r in materials:
    if r["material_id"] in {"P1_FV","P2_WW","P3_FAUST"} and "external mechanism" not in r["claim_ceiling"]:
        errors.append(f'{r["material_id"]}: independent validation claim ceiling drift')
    if r["material_id"]=="P4_ELTEC" and r["current_status"]!="REFERENCE_ONLY":
        errors.append("ELTeC must remain methodological reference unless separately preregistered")
    if r["material_id"]=="P5_SCRIVENER" and r["independent_of_this_study"]!="no":
        errors.append("Scrivener must remain classified as self-constructed holdout")

src_by={mid:0 for mid in ids}
for s in sources:
    if s["material_id"] not in ids:
        errors.append(f'{s["material_id"]}: source references unknown material')
    else:
        src_by[s["material_id"]]+=1

for mid in ("P1_FV","P2_WW","P3_FAUST","P4_ELTEC"):
    if src_by.get(mid,0)==0:
        errors.append(f"{mid}: no authoritative source frozen")

print(f"external_materials={len(materials)}")
print(f"external_sources={len(sources)}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("EXTERNAL_DH_PORTFOLIO=PASS")
print("NATIVE_SEMANTICS_SEPARATION=PASS")
print("INDEPENDENCE_CLASSIFICATION=PASS")
