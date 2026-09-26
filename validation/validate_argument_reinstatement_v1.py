from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def read(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

args=read("experiments/argument_reinstatement_v1/arguments_v1.csv")
attacks=read("experiments/argument_reinstatement_v1/attacks_v1.csv")
conds=read("experiments/argument_reinstatement_v1/condition_activation_v1.csv")

arg_ids={r["argument_id"] for r in args}
if arg_ids!={"A0_PM01_ASSERTION","A1_PM02_OBJECTION","A2_PM03_CORRECTION"}:
    errors.append(f"argument set drift: {arg_ids}")

for r in args:
    if r["verification_status"]!="PAGE_VERIFIED":
        errors.append(f'{r["argument_id"]}: non-page-verified source basis')

for r in attacks:
    if r["attacker"] not in arg_ids or r["target"] not in arg_ids:
        errors.append(f'{r["attack_id"]}: unknown argument endpoint')
    if r["verification_status"]!="PAGE_VERIFIED":
        errors.append(f'{r["attack_id"]}: attack not page verified')

expected={
    "GENERIC_BASE":"no",
    "GUIDED_BASE":"yes",
    "GENERIC_RESCUE_PM03":"yes",
    "GENERIC_SHAM":"no",
    "GUIDED_REMOVE_PM03":"no",
}
got={r["scientific_condition"]:r["pm03_argument_active"] for r in conds}
if got!=expected:
    errors.append(f"condition activation drift: {got}")

proto=(ROOT/"experiments/argument_reinstatement_v1/PROTOCOL.md").read_text(encoding="utf-8")
for phrase in [
    "NEW STUDY AFTER NEGATIVE LLM-JUDGE RESULT",
    "Use standard grounded semantics",
    "formal acceptance statuses under the declared semantics",
    "NOT:",
]:
    if phrase not in proto:
        errors.append(f"protocol missing phrase: {phrase}")

if errors:
    for e in errors:
        print("FAIL:",e)
    sys.exit(1)

proc=subprocess.run(
    [sys.executable,str(ROOT/"experiments/argument_reinstatement_v1/run.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
print(proc.stdout,end="")
if proc.returncode!=0:
    print(proc.stderr,end="",file=sys.stderr)
    sys.exit(proc.returncode)

if "SELECTIVE_REINSTATEMENT_FORMAL_CONSEQUENCE=PASS" not in proc.stdout:
    raise RuntimeError("formal consequence gate not reached")

print("ARGUMENT_REINSTATEMENT_CONTRACT=PASS")
