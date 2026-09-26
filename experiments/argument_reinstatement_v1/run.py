from __future__ import annotations

ARGUMENTS={
    "A0_PM01_ASSERTION",
    "A1_PM02_OBJECTION",
    "A2_PM03_CORRECTION",
}
ATTACKS={
    ("A1_PM02_OBJECTION","A0_PM01_ASSERTION"),
    ("A2_PM03_CORRECTION","A1_PM02_OBJECTION"),
}
FOCAL="A0_PM01_ASSERTION"

CONDITIONS={
    "GENERIC_BASE":{"A0_PM01_ASSERTION","A1_PM02_OBJECTION"},
    "GUIDED_BASE":{"A0_PM01_ASSERTION","A1_PM02_OBJECTION","A2_PM03_CORRECTION"},
    "GENERIC_RESCUE_PM03":{"A0_PM01_ASSERTION","A1_PM02_OBJECTION","A2_PM03_CORRECTION"},
    "GENERIC_SHAM":{"A0_PM01_ASSERTION","A1_PM02_OBJECTION"},
    "GUIDED_REMOVE_PM03":{"A0_PM01_ASSERTION","A1_PM02_OBJECTION"},
}

def grounded(active):
    attacks={(a,b) for a,b in ATTACKS if a in active and b in active}
    attackers={x:set() for x in active}
    for a,b in attacks:
        attackers[b].add(a)

    ext=set()
    changed=True
    while changed:
        changed=False
        for x in sorted(active):
            if x in ext:
                continue
            defended=True
            for y in attackers[x]:
                # Every attacker y must itself be attacked by an accepted argument.
                if not any((z,y) in attacks for z in ext):
                    defended=False
                    break
            if defended:
                ext.add(x)
                changed=True
    return ext

print("ARCHIVAL_ARGUMENT_REINSTATEMENT_V1")
for name,active in CONDITIONS.items():
    ext=grounded(active)
    status="IN_GROUNDED_EXTENSION" if FOCAL in ext else "OUT_GROUNDED_EXTENSION"
    print(f"RESULT,{name},active={'|'.join(sorted(active))},grounded={'|'.join(sorted(ext))},focal={status}")

expected={
    "GENERIC_BASE":"OUT_GROUNDED_EXTENSION",
    "GUIDED_BASE":"IN_GROUNDED_EXTENSION",
    "GENERIC_RESCUE_PM03":"IN_GROUNDED_EXTENSION",
    "GENERIC_SHAM":"OUT_GROUNDED_EXTENSION",
    "GUIDED_REMOVE_PM03":"OUT_GROUNDED_EXTENSION",
}

for name,active in CONDITIONS.items():
    ext=grounded(active)
    got="IN_GROUNDED_EXTENSION" if FOCAL in ext else "OUT_GROUNDED_EXTENSION"
    if got!=expected[name]:
        raise RuntimeError(f"{name}: expected {expected[name]} got {got}")

print("SELECTIVE_REINSTATEMENT_FORMAL_CONSEQUENCE=PASS")
print("LLM_JUDGE_USED=0")
print("HUMAN_BEHAVIOR_CLAIM=0")
