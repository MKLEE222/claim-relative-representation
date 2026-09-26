from __future__ import annotations

import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
GEN=ROOT/"experiments/warrant_closure_final/generated"

OUTPUTS=GEN/"judge_outputs_v1.jsonl"
MAP=GEN/"judge_call_audit_map_v1.json"

ALLOWED_REL={
    "E_SUPPORT","E_UNDERCUT","E_QUALIFY_AUTHORITY","E_REHABILITATE",
    "E_ACCRETION","E_IDENTIFICATION_UPDATE","E_UNRESOLVED"
}
ALLOWED_STATE={"RETAIN","DEFER","WITHHOLD"}

if not OUTPUTS.exists():
    print("FINAL_JUDGE_ANALYSIS=PENDING_OUTPUTS")
    sys.exit(0)
if not MAP.exists():
    raise RuntimeError("audit call map missing")

call_map=json.loads(MAP.read_text(encoding="utf-8"))
rows=[]
with OUTPUTS.open(encoding="utf-8") as f:
    for line in f:
        if line.strip():
            rows.append(json.loads(line))

if len(rows)!=15:
    raise RuntimeError(f"expected 15 outputs, got {len(rows)}")
if len({r["call_id"] for r in rows})!=15:
    raise RuntimeError("duplicate call ids")

by_packet=defaultdict(dict)
for r in rows:
    cid=r["call_id"]
    if cid not in call_map:
        raise RuntimeError(f"unknown call id: {cid}")
    resp=r["response"]
    state=resp.get("warrant_state")
    rel=set(resp.get("epistemic_relations",[]))
    if state not in ALLOWED_STATE:
        raise RuntimeError(f"{cid}: invalid warrant state {state}")
    if not rel<=ALLOWED_REL:
        raise RuntimeError(f"{cid}: invalid epistemic relation set {rel-ALLOWED_REL}")
    meta=call_map[cid]
    by_packet[meta["packet_id"]][meta["variant"]]={
        "state":state,
        "relations":rel,
        "call_id":cid,
        "model_id":r.get("model_id","UNRECORDED"),
    }

expected_variants={"canonical","reverse_order","relabel_only"}
stable={}
for pid,v in by_packet.items():
    if set(v)!=expected_variants:
        raise RuntimeError(f"{pid}: missing variants {expected_variants-set(v)}")
    states={x["state"] for x in v.values()}
    stable[pid]=len(states)==1
    rels=[x["relations"] for x in v.values()]
    jacc=[]
    for a,b in itertools.combinations(rels,2):
        denom=len(a|b)
        jacc.append(1.0 if denom==0 else len(a&b)/denom)
    print(f"PACKET,{pid},stable={int(stable[pid])},state={'|'.join(sorted(states))},relation_jaccard_min={min(jacc):.3f},relation_jaccard_mean={sum(jacc)/len(jacc):.3f}")

if not all(stable.values()):
    print("FINAL_WARRANT_STATUS=MODEL_SENSITIVE")
    print("SELECTIVE_RESTORATION_CLAIM=BLOCKED")
    sys.exit(0)

# Unblind only after stability is established.
condition_to_pid={}
for cid,meta in call_map.items():
    condition_to_pid[meta["scientific_condition"]]=meta["packet_id"]

def state(condition):
    pid=condition_to_pid[condition]
    return by_packet[pid]["canonical"]["state"]

g=state("GENERIC_BASE")
s=state("GUIDED_BASE")
r=state("GENERIC_RESCUE_PM03")
h=state("GENERIC_SHAM")
m=state("GUIDED_REMOVE_PM03")

base_difference=(g!=s)
rescue=(g!=r)
sham_specific=(g==h)
removal=(s!=m)
strong=rescue and sham_specific and removal

print("UNBLINDED_AFTER_STABILITY=1")
print(f"STATE,GENERIC_BASE,{g}")
print(f"STATE,GUIDED_BASE,{s}")
print(f"STATE,GENERIC_RESCUE_PM03,{r}")
print(f"STATE,GENERIC_SHAM,{h}")
print(f"STATE,GUIDED_REMOVE_PM03,{m}")
print(f"BASE_NAVIGATION_DIFFERENCE={int(base_difference)}")
print(f"PM03_RESCUE_DIFFERENCE={int(rescue)}")
print(f"SHAM_MATCHES_GENERIC={int(sham_specific)}")
print(f"PM03_REMOVAL_DIFFERENCE={int(removal)}")
print(f"SELECTIVE_RESTORATION_PASS={int(strong)}")

if strong:
    print("FINAL_WARRANT_STATUS=SELECTIVE_RESTORATION_SUPPORTED")
elif base_difference:
    print("FINAL_WARRANT_STATUS=NAVIGATION_CONSEQUENCE_WITHOUT_SELECTIVE_CLOSURE")
else:
    print("FINAL_WARRANT_STATUS=NULL_OR_NO_BASE_DIFFERENCE")
