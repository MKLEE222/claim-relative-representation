from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

rows=[]
with open(ROOT/"spec/frankenstein_chunk_seal_v1.csv",newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))

errors=[]
c17=[r for r in rows if r["chunk_id"]=="C17"]
if len(c17)!=5:
    errors.append(f"C17 input seal expected 5 rows, found {len(c17)}")
for r in c17:
    if r["role"]!="HOLDOUT":
        errors.append(f'{r["file_path"]}: C17 role drift')
    if r["content_opened_by_this_study"]!="no":
        errors.append(f'{r["file_path"]}: C17 input was marked opened before holdout')
    if r["status"]!="SEALED":
        errors.append(f'{r["file_path"]}: C17 not sealed')

protocol=(ROOT/"experiments/external_x1b_frankenstein_holdout/PROTOCOL.md").read_text(encoding="utf-8")
for term in ["FV-ALIGN","FV-SOURCE-GEOGRAPHY","FV-PRINT-PAGINATION","surface","zone","graphic","lb","pb"]:
    if term not in protocol:
        errors.append(f"missing frozen task/coordinate {term}")

print(f"c17_sealed_inputs={len(c17)}")
if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)
print("C17_HOLDOUT_SEAL=PASS")
print("X1B_TASKS_FROZEN=PASS")
print("C17_OUTPUT_CONTENT_OPENED_BY_PROTOCOL=NO")
