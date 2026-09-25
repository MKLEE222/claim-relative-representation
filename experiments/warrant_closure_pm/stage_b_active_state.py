from __future__ import annotations

import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BUDGET=12

def read_csv(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

# Authoritative stored results.
e1=read_csv("experiments/ecological_anchor_e1_papermoney/results_v1.csv")
e1w=read_csv("experiments/ecological_anchor_e1w_sequence_guided/results_v1.csv")
traces=read_csv("data/paper_money_archival_stance_traces_v1.csv")

declared=next(r for r in e1 if r["condition"]=="W_DECLARED_COLLECTION")
guided=next(r for r in e1w if r["policy"]=="PI_SEQUENCE_GUIDED_DOMAIN_CHAIN")

generic_rank=int(declared["target_rank"])
guided_present=int(guided["target_in_set"])==1
guided_ord=int(guided["target_ordinal"])

conditions={
    "GENERIC_TOP12":{
        "PM01":True,
        "PM02":True,
        "PM03":generic_rank<=BUDGET,
        "construction_basis":f"authoritative E1 rank={generic_rank}",
    },
    "GUIDED_TOP12":{
        "PM01":True,
        "PM02":True,
        "PM03":guided_present and guided_ord<=BUDGET,
        "construction_basis":f"authoritative E1W ordinal={guided_ord}",
    },
}

print("PM_WARRANT_STAGE_B_ACTIVE_STATE")
print("budget="+str(BUDGET))

for name,state in conditions.items():
    active=[e for e in ("PM01","PM02","PM03") if state[e]]
    active_traces=[r["trace_id"] for r in traces if state.get(r["event_ref"],False)]
    trace_types=[r["trace_type"] for r in traces if state.get(r["event_ref"],False)]
    print("CONDITION="+name)
    print("ACTIVE_EVENTS="+"|".join(active))
    print("ACTIVE_TRACES="+"|".join(active_traces))
    print("ACTIVE_TRACE_TYPES="+"|".join(trace_types))
    print("BASIS="+state["construction_basis"])
    print("EPISTEMIC_RELATION_ASSIGNED=0")
    print("WARRANT_STATE_ASSIGNED=0")

assert conditions["GENERIC_TOP12"]["PM03"] is False
assert conditions["GUIDED_TOP12"]["PM03"] is True

generic_trace_ids={r["trace_id"] for r in traces if conditions["GENERIC_TOP12"].get(r["event_ref"],False)}
guided_trace_ids={r["trace_id"] for r in traces if conditions["GUIDED_TOP12"].get(r["event_ref"],False)}

assert generic_trace_ids=={"PMT01"}
assert guided_trace_ids=={"PMT01","PMT02","PMT03"}

print("GENERIC_TRACE_SET=PMT01")
print("GUIDED_TRACE_SET=PMT01|PMT02|PMT03")
print("TRACE_SET_DIFFERENCE=PMT02|PMT03")
print("FINAL_LLM_JUDGE_EXECUTED=0")
