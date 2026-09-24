from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

with open(ROOT/"spec/minimal_carrier_searches_v1.csv",newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))

ids={r["search_id"] for r in rows}
if ids!={"MC_FV_C18","MC_WW_01","MC_FA_01"}:
    errors.append(f"search registry drift: {sorted(ids)}")

with open(ROOT/"spec/frankenstein_c18_minimal_carrier_seal.csv",newline="",encoding="utf-8") as f:
    seal=list(csv.DictReader(f))
if len(seal)!=1:
    errors.append("C18 seal must have exactly one row")
else:
    r=seal[0]
    if r["git_blob_sha"]!="bca0548912ab1d7b2676360d33a6468290296d7e":
        errors.append("C18 blob drift")
    if r["content_opened_by_this_study"]!="no":
        errors.append("C18 marked opened before minimal-carrier freeze")
    if r["status"]!="SEALED_BEFORE_MC_FV_C18":
        errors.append("C18 seal status drift")

contract=(ROOT/"spec/MINIMAL_SUFFICIENT_CARRIER_CONTRACT.md").read_text(encoding="utf-8")
for term in [
    "Stage 0 - support feasibility",
    "Stage 1 - fixed task output",
    "Multiple minimal families",
    "Cost is separate",
    "Native versus derived carriers",
]:
    if term not in contract:
        errors.append(f"minimal carrier contract missing: {term}")

fv=(ROOT/"experiments/minimal_carrier_fv_c18/PROTOCOL.md").read_text(encoding="utf-8")
for term in ["WITNESS_ID","RDGGRP_MEMBERSHIP","READING_TEXT","D_GROUP","D_TEXT"]:
    if term not in fv:
        errors.append(f"C18 protocol missing: {term}")

print(f"minimal_carrier_searches={len(rows)}")
if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("MINIMAL_CARRIER_CONTRACT=PASS")
print("C18_PREOUTCOME_SEAL=PASS")
print("FIXED_TASK_SUBSET_SEARCH=PASS")
