from __future__ import annotations
import csv, sys
from pathlib import Path

p=Path("experiments/deepening_v1/r3_pass1_B02_entry_labels_v1.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8")))
errs=[]
if len(rows)!=20: errs.append(f"expected 20 B02 rows, got {len(rows)}")
expected=[f"YC1920E-{i:04d}" for i in range(21,41)]
if [r["entry_id"] for r in rows]!=expected: errs.append("B02 entry sequence drift")
allowed={"ADDITIVE_EVIDENCE","CORROBORATION","CRITICISM","FACTUAL_CORRECTION","CORRECTION_OF_PRIOR_CRITICISM","IDENTIFICATION_UPDATE","ATTRIBUTION_UPDATE","TEXTUAL_UPDATE","QUALIFICATION"}
for r in rows:
    bad=set(r["relation_labels"].split("|"))-allowed
    if bad: errs.append(f"{r['entry_id']} bad labels {bad}")
    if not r["source_basis"].strip(): errs.append(f"{r['entry_id']} missing source basis")
    if not r["evidence_span"].strip(): errs.append(f"{r['entry_id']} missing evidence span")
    if r["authority"]!="TRANSCRIPTION_ONLY": errs.append(f"{r['entry_id']} authority drift")
sel=list(csv.DictReader(Path("experiments/deepening_v1/r3_fg_transfer_selection_v1.csv").open(encoding="utf-8")))
if len(sel)!=5: errs.append("expected five transfer strata")
if any(r["representation_outcome_opened"]!="0" for r in sel): errs.append("representation outcome seal broken")
if {r["stratum"] for r in sel}!={"ADDITIVE_EVIDENCE","FACTUAL_CORRECTION","QUALIFICATION","IDENTIFICATION_UPDATE","ATTRIBUTION_UPDATE"}:
    errs.append("transfer strata drift")
if errs:
    print("\n".join("FAIL "+e for e in errs)); sys.exit(1)
print("R3_B02_AND_TRANSFER_SELECTION=PASS")
print("B02_rows=20")
print("transfer_acts=5")
print("representation_outcomes_opened=0")
