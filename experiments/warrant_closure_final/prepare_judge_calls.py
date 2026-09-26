from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
GEN=ROOT/"experiments/warrant_closure_final/generated"

bundle=json.loads((GEN/"judge_bundle_v3.json").read_text(encoding="utf-8"))
audit=json.loads((GEN/"audit_manifest_v3.json").read_text(encoding="utf-8"))
prompt_template=(ROOT/"experiments/warrant_closure_final/judge_prompt_v2.txt").read_text(encoding="utf-8")
schema=json.loads((ROOT/"experiments/warrant_closure_final/judge_output_schema_v2.json").read_text(encoding="utf-8"))

fixed=bundle["fixed"]
fixed_context=json.dumps(
    {"PM01":fixed["PM01"],"PM02":fixed["PM02"]},
    ensure_ascii=False,
    indent=2,
)

calls=[]
call_map={}
for pid in sorted(bundle["packets"]):
    for variant in ("canonical","reverse_order","relabel_only"):
        units=bundle["packets"][pid][variant]
        seed=f"FINAL_WARRANT_V1|{pid}|{variant}"
        call_id="C"+hashlib.sha256(seed.encode("utf-8")).hexdigest()[:11].upper()
        prompt=prompt_template
        prompt=prompt.replace("{{CLAIM}}",fixed["claim"])
        prompt=prompt.replace("{{FIXED_CONTEXT}}",fixed_context)
        prompt=prompt.replace("{{EVIDENCE_UNITS}}",json.dumps(units,ensure_ascii=False,indent=2))
        if "{{" in prompt or "}}" in prompt:
            raise RuntimeError(f"unfilled prompt template for {call_id}")
        calls.append({
            "call_id":call_id,
            "instruction":"Execute this record as one independent stateless model call. Do not expose any other call record in the same model context.",
            "prompt":prompt,
            "response_schema":schema,
        })
        call_map[call_id]={
            "packet_id":pid,
            "variant":variant,
            "scientific_condition":audit["mapping"][pid],
            "judge_packet_sha256":audit["canonical_judge_packet_sha256"][pid],
        }

if len(calls)!=15:
    raise RuntimeError(f"expected 15 independent calls, got {len(calls)}")
if len({x["call_id"] for x in calls})!=15:
    raise RuntimeError("call id collision")

visible=json.dumps(calls,ensure_ascii=False)
for condition in audit["mapping"].values():
    if condition in visible:
        raise RuntimeError(f"scientific condition leaked to judge calls: {condition}")

calls_path=GEN/"judge_calls_v1.jsonl"
with calls_path.open("w",encoding="utf-8") as f:
    for call in calls:
        f.write(json.dumps(call,ensure_ascii=False)+"\n")

map_path=GEN/"judge_call_audit_map_v1.json"
map_path.write_text(json.dumps(call_map,ensure_ascii=False,indent=2),encoding="utf-8")

print("FINAL_JUDGE_CALLS_PREPARED=15")
print("CALL_CONTEXT_POLICY=ONE_RECORD_PER_STATELESS_CALL")
print("SCIENTIFIC_CONDITION_VISIBLE=0")
print("CALL_FILE_SHA256="+hashlib.sha256(calls_path.read_bytes()).hexdigest())
