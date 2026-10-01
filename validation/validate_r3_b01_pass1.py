from __future__ import annotations
import csv, sys
from pathlib import Path

P=Path("experiments/deepening_v1/r3_pass1_B01_entry_labels_v1.csv")
rows=list(csv.DictReader(P.open(encoding="utf-8")))
allowed={
"ADDITIVE_EVIDENCE","CORROBORATION","CRITICISM","FACTUAL_CORRECTION",
"CORRECTION_OF_PRIOR_CRITICISM","IDENTIFICATION_UPDATE","ATTRIBUTION_UPDATE",
"TEXTUAL_UPDATE","QUALIFICATION","UNRESOLVED_RELATION"
}
errs=[]
if len(rows)!=20: errs.append(f"expected 20 rows, got {len(rows)}")
expected=[f"YC1920E-{i:04d}" for i in range(1,21)]
if [r["entry_id"] for r in rows]!=expected: errs.append("entry ids drift")
for r in rows:
    labs=set(r["relation_labels"].split("|"))
    bad=labs-allowed
    if bad: errs.append(f"{r['entry_id']}: bad labels {sorted(bad)}")
    if not r["evidence_span"].strip(): errs.append(f"{r['entry_id']}: missing evidence span")
    if r["authority"]!="TRANSCRIPTION_ONLY": errs.append(f"{r['entry_id']}: authority drift")
    if "cue" in r["pass1_note"].lower(): errs.append(f"{r['entry_id']}: cue language in pass note")
if errs:
    print("\n".join("FAIL "+e for e in errs)); sys.exit(1)
print("R3_B01_PASS1_CONTRACT=PASS")
print("rows=20")
