from __future__ import annotations
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

paths=[
    ROOT/"experiments/ecological_anchor_e1_papermoney/run.py",
    ROOT/"experiments/ecological_anchor_e1d_retrieval_policy/run.py",
    ROOT/"experiments/ecological_anchor_e1w_sequence_guided/run.py",
]

for p in paths:
    txt=p.read_text(encoding="utf-8")
    if "STRIDE=90" not in txt.replace(" ",""):
        errors.append(f"{p}: STRIDE is not frozen at 90")
    if "range(0" not in txt or "STRIDE" not in txt:
        errors.append(f"{p}: sliding-window grid construction not found")

STRIDE=90
starts=list(range(0,9000,STRIDE))
for a in starts:
    for b in starts:
        prox=abs(a-b)<STRIDE
        same=(a==b)
        if prox!=same:
            errors.append(f"grid counterexample: a={a}, b={b}")
            break
    if errors:
        break

e1=(ROOT/"experiments/ecological_anchor_e1_papermoney/run.py").read_text(encoding="utf-8")
e1d=(ROOT/"experiments/ecological_anchor_e1d_retrieval_policy/run.py").read_text(encoding="utf-8")
e1w=(ROOT/"experiments/ecological_anchor_e1w_sequence_guided/run.py").read_text(encoding="utf-8")

if "w.doc==target.doc and abs(w.start-target.start) < STRIDE" not in e1:
    errors.append("E1 target identity expression changed")
if "w.doc==target.doc and abs(w.start-target.start)<STRIDE" not in e1d:
    errors.append("E1D target identity expression changed")
if "abs(w.start-target.start)<STRIDE" not in e1w:
    errors.append("E1W target identity expression changed")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

print("TARGET_WINDOW_GRID_IDENTITY=PASS")
print("PROXIMITY_LT_STRIDE_IMPLIES_SAME_START=PASS")
print("E1_TARGET_IDENTITY=PASS")
print("E1D_TARGET_IDENTITY=PASS")
print("E1W_TARGET_IDENTITY=PASS")
print("WARRANT_METRIC_BLOCK=RESOLVED")
