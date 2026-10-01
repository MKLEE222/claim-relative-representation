from __future__ import annotations
import csv,sys
from pathlib import Path
sel=list(csv.DictReader(Path("experiments/deepening_v1/r3_fg_transfer_selection_v2.csv").open(encoding="utf-8")))
errs=[]
if len(sel)!=5: errs.append("expected five strata")
if any(r["representation_outcome_opened"]!="0" for r in sel): errs.append("representation outcomes opened")
expected={"ADDITIVE_EVIDENCE","FACTUAL_CORRECTION","QUALIFICATION","IDENTIFICATION_UPDATE","ATTRIBUTION_UPDATE"}
if {r["stratum"] for r in sel}!=expected: errs.append("strata drift")
if next(r for r in sel if r["stratum"]=="ATTRIBUTION_UPDATE")["entry_id"]=="YC1920E-0030":
    errs.append("superseded E0030 attribution-update selection retained")
audit=list(csv.DictReader(Path("experiments/deepening_v1/r3_B02_B03_contrast_audit_v1.csv").open(encoding="utf-8")))
row=next(r for r in audit if r["entry_id"]=="YC1920E-0030")
if "ATTRIBUTION_UPDATE" in row["final_diachronic_relation"]:
    errs.append("E0030 not demoted")
if errs:
    print("\n".join("FAIL "+e for e in errs)); sys.exit(1)
print("R3_DIACHRONIC_CONTRAST_GATE=PASS")
print("transfer_strata=5")
print("representation_outcomes_opened=0")
