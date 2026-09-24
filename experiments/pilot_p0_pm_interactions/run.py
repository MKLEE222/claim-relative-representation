from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def read_csv(path):
    with open(ROOT/path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

fixture={r["event_ref"]:r for r in json.loads((ROOT/"representation/baseline_fixture_v1.json").read_text(encoding="utf-8"))}
texts={r["event_ref"]:r["text"] for r in read_csv("experiments/exp1_residual_cue_leakage/inputs.csv")}

TASK_EVENTS=["PM01","PM02","PM03"]
AUX_CONTEXT=["PM04"]

CUES={
    "temporal_order":[
        r"regarding .*statement",
        r"p\.\s*\d+",
        r"later",
        r"1903",
        r"1920",
        r"addenda?",
    ],
    "claim_binding":[
        r"paper[- ]?money",
        r"mulberry",
        r"bark",
        r"bretschneider",
        r"laufer",
    ],
    "evidence_relation":[
        r"mistaken",
        r"error",
        r"correct",
        r"regarding .*statement",
        r"preferred for making paper-money",
    ],
}

FIELD={
    "temporal_order":"temporal_order",
    "claim_binding":"claim_binding",
    "evidence_relation":"evidence_relation",
}

INTERACTIONS=[
    ("I01","temporal_order","TD_TEMPORAL"),
    ("I02","claim_binding","TR_BINDING"),
    ("I03","evidence_relation","TR_EVIDENCE"),
]

def has_cue(event_ids, distinction):
    pats=CUES[distinction]
    for eid in event_ids:
        text=texts[eid]
        for p in pats:
            if re.search(p,text,flags=re.I):
                return True
    return False

def make_state(remove_field=None, span_only=False):
    records=[]
    for eid in TASK_EVENTS:
        rec=dict(fixture[eid])
        if remove_field is not None:
            rec[remove_field]=None
        records.append(rec)
    return {
        "records":records,
        "task_events":list(TASK_EVENTS),
        "aux_context":[] if span_only else list(AUX_CONTEXT),
    }

def recover(state, distinction):
    field=FIELD[distinction]
    if all(r.get(field) is not None for r in state["records"]):
        return ("E","D0","B_STRUCTURED_METADATA")

    if has_cue(state["task_events"],distinction):
        return ("R","D1","B_LEXICAL_CUE")

    if state["aux_context"] and has_cue(state["aux_context"],distinction):
        return ("R","D3","B_CROSS_LAYER_CONTEXT")

    return ("Q","NA","NONE_DETECTED")

def fmt(profile):
    return "/".join(profile)

print("PILOT_P0_PM_INTERACTIONS")
print("interaction,distinction,R00,R10,R01,R11,classification")

for iid,dist,t1 in INTERACTIONS:
    field=FIELD[dist]
    states={
        "R00":make_state(),
        "R10":make_state(remove_field=field),
        "R01":make_state(span_only=True),
        "R11":make_state(remove_field=field,span_only=True),
    }
    prof={k:recover(v,dist) for k,v in states.items()}

    if prof["R10"][0] in {"E","R"} and prof["R01"][0] in {"E","R"} and prof["R11"][0] in {"Q","U"}:
        cls="BASIS_EXHAUSTION_CANDIDATE"
    elif prof["R11"][0]=="R" and prof["R11"][2]=="B_LEXICAL_CUE":
        cls="NO_EXHAUSTION_LEXICAL_SUBSTITUTION_SURVIVES"
    else:
        cls="NO_STRONG_INTERACTION"

    print(",".join([
        iid,dist,fmt(prof["R00"]),fmt(prof["R10"]),fmt(prof["R01"]),fmt(prof["R11"]),cls
    ]))
