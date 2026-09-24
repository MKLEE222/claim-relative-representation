from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

with open(ROOT/"spec/frankenstein_chunk_seal_v1.csv",newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))
c17=[r for r in rows if r["chunk_id"]=="C17"]
if len(c17)!=5:
    errors.append(f"C17 input seal expected 5 rows, found {len(c17)}")
for r in c17:
    if r["role"]!="HOLDOUT" or r["status"]!="SEALED":
        errors.append(f'{r["file_path"]}: C17 input role/status drift')
    if r["content_opened_by_this_study"]!="no":
        errors.append(f'{r["file_path"]}: C17 input marked opened before holdout')

with open(ROOT/"spec/frankenstein_c17_output_seal_v1.csv",newline="",encoding="utf-8") as f:
    out=list(csv.DictReader(f))
if len(out)!=1:
    errors.append("C17 output seal must contain exactly one authoritative complete output")
else:
    r=out[0]
    if r["git_blob_sha"]!="41032625f93e62dcb632f1ff8b35aa04e32df40c":
        errors.append("C17 output blob drift")
    if r["content_opened_by_this_study"]!="no":
        errors.append("C17 output content marked opened before protocol freeze")

p=(ROOT/"experiments/external_x1b_frankenstein_holdout/PROTOCOL_v2.md").read_text(encoding="utf-8")
required=[
    "FV-ALIGN","FV-SOURCE-GEOGRAPHY","FV-PRINT-PAGINATION",
    "surface | zone | graphic | lb","pb","PASS_SELECTIVE_ADEQUACY",
    "GLOBAL_EQUIVALENCE_NOT_REJECTED"
]
for x in required:
    if x not in p:
        errors.append(f"missing frozen X1B v2 term: {x}")

print(f"c17_input_seals={len(c17)}")
print(f"c17_output_seals={len(out)}")
if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("C17_INPUT_SEAL=PASS")
print("C17_OUTPUT_METADATA_SEAL=PASS")
print("X1B_V2_TASKS_FROZEN=PASS")
print("C17_OUTPUT_CONTENT_OPENED_BEFORE_FREEZE=NO")
