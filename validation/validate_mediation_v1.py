from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

errors=[]

with open(ROOT/"spec/mediation_primitives_v1.csv",newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))

expected={"M_LOCAL_ATTACHMENT","M_REFERENT_ALIAS","M_CITED_SOURCE","M_NATIVE_SEQUENCE","M_EXPLICIT_POINTER"}
ids={r["primitive_id"] for r in rows}
if ids!=expected:
    errors.append(f"primitive set drift: {sorted(ids)}")

for r in rows:
    if r["target_only_info_allowed"].lower()!="no":
        errors.append(f'{r["primitive_id"]}: target-only information allowed')

p=(ROOT/"spec/SOURCE_GROUNDED_MEDIATION_CONTRACT.md").read_text(encoding="utf-8")
for x in [
    "support feasibility before complexity",
    "fixed target",
    "WARRANT-AUTHORIZED",
    "M1 - legality",
    "M6 - verifier independence",
    "Support stop"
]:
    if x not in p:
        errors.append(f"mediation contract missing {x}")

cp=(ROOT/"experiments/ep_cl_01_boundary/PROTOCOL.md").read_text(encoding="utf-8")
for x in ["M_LOCAL_ATTACHMENT","CL-SPAN","CL-LOCAL-LINEAR","CL-ATTACHMENT","CLAIM"]:
    # CLAIM may occur only in claim ceiling; presence is not outcome opening.
    if x not in cp:
        errors.append(f"coal protocol missing {x}")

print(f"mediation_primitives={len(rows)}")
if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("MEDIATION_SUPPORT_GATE=PASS")
print("SOURCE_BINDING_OBLIGATIONS=PASS")
print("TARGET_LEAKAGE_POLICY=PASS")
