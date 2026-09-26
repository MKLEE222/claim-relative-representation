from __future__ import annotations

import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def read(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

arg_rows=read("experiments/argument_reinstatement_v1/arguments_v1.csv")
atk_rows=read("experiments/argument_reinstatement_v1/attacks_v1.csv")
cond_rows=read("experiments/argument_reinstatement_v1/condition_activation_v1.csv")

ARGUMENTS={r["argument_id"] for r in arg_rows}
ATTACKS={(r["attacker"],r["target"]) for r in atk_rows}
FOCAL="A0_PM01_ASSERTION"
BASE={"A0_PM01_ASSERTION","A1_PM02_OBJECTION"}

def grounded(active):
    attacks={(a,b) for a,b in ATTACKS if a in active and b in active}
    attackers={x:set() for x in active}
    for a,b in attacks:
        attackers[b].add(a)

    ext=set()
    while True:
        next_ext=set()
        for x in active:
            acceptable=True
            for attacker in attackers[x]:
                if not any((defender,attacker) in attacks for defender in ext):
                    acceptable=False
                    break
            if acceptable:
                next_ext.add(x)
        if next_ext==ext:
            return ext
        ext=next_ext

expected={
    "GENERIC_BASE":"OUT_GROUNDED_EXTENSION",
    "GUIDED_BASE":"IN_GROUNDED_EXTENSION",
    "GENERIC_RESCUE_PM03":"IN_GROUNDED_EXTENSION",
    "GENERIC_SHAM":"OUT_GROUNDED_EXTENSION",
    "GUIDED_REMOVE_PM03":"OUT_GROUNDED_EXTENSION",
}

print("ARCHIVAL_ARGUMENT_REINSTATEMENT_V1")
for row in cond_rows:
    condition=row["scientific_condition"]
    active=set(BASE)
    if row["pm03_argument_active"]=="yes":
        active.add("A2_PM03_CORRECTION")
    ext=grounded(active)
    status="IN_GROUNDED_EXTENSION" if FOCAL in ext else "OUT_GROUNDED_EXTENSION"
    print(",".join([
        "RESULT",
        condition,
        "packet="+row["opaque_packet"],
        "active="+"|".join(sorted(active)),
        "grounded="+"|".join(sorted(ext)),
        "focal="+status,
    ]))
    if status!=expected[condition]:
        raise RuntimeError(f"{condition}: expected {expected[condition]} got {status}")

print("SELECTIVE_REINSTATEMENT_FORMAL_CONSEQUENCE=PASS")
print("LLM_JUDGE_USED=0")
print("HUMAN_BEHAVIOR_CLAIM=0")
