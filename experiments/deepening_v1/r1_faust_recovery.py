from __future__ import annotations

import collections
import hashlib
import io
import json
import tarfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

COMMIT="502eca65120dd6189ceaf41d4e5017775e6e4677"
URL=f"https://github.com/faustedition/faust-xml/archive/{COMMIT}.tar.gz"
NS={"f":"http://www.faustedition.net/ns"}

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=90) as r:
    raw=r.read()

tf=tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz")
records=[]
parse_failures=[]
relevant_files=0

for member in tf.getmembers():
    name=member.name
    if not member.isfile() or "/xml/macrogenesis/" not in name or not name.endswith(".xml"):
        continue
    relevant_files+=1
    f=tf.extractfile(member)
    if f is None:
        continue
    data=f.read()
    try:
        root=ET.fromstring(data)
    except ET.ParseError as e:
        parse_failures.append({"file":name,"error":str(e)})
        continue

    rel_index=0
    for rel in root.findall(".//f:relation[@name='temp-pre']",NS):
        items=tuple(x.attrib.get("uri") for x in rel.findall("./f:item",NS) if x.attrib.get("uri"))
        if len(items)<2:
            continue
        srcs=[]
        for src in rel.findall("./f:source",NS):
            uri=(src.attrib.get("uri") or "").strip()
            locator=" ".join("".join(src.itertext()).split())
            srcs.append((uri,locator))
        bundle=tuple(sorted(srcs))
        records.append({"file":name,"relation_index":rel_index,"items":items,"source_bundle":bundle})
        rel_index+=1

missing_source=[r for r in records if not r["source_bundle"]]
multi_source=[r for r in records if len(r["source_bundle"])>1]

edge_occ=[]
for ri,r in enumerate(records):
    for pos,(a,b) in enumerate(zip(r["items"],r["items"][1:])):
        edge_occ.append({"record_index":ri,"file":r["file"],"edge_pos":pos,"a":a,"b":b,"source_bundle":r["source_bundle"]})

unique_edges=sorted({(e["a"],e["b"]) for e in edge_occ})

adj=collections.defaultdict(set)
nodes=set()
for a,b in unique_edges:
    adj[a].add(b); nodes.add(a); nodes.add(b)

idx={}; low={}; stack=[]; on=set(); comps=[]; counter=0

def sc(v):
    global counter
    idx[v]=counter; low[v]=counter; counter+=1
    stack.append(v); on.add(v)
    for w in adj.get(v,set()):
        if w not in idx:
            sc(w); low[v]=min(low[v],low[w])
        elif w in on:
            low[v]=min(low[v],idx[w])
    if low[v]==idx[v]:
        c=set()
        while True:
            w=stack.pop(); on.remove(w); c.add(w)
            if w==v: break
        comps.append(c)

for v in sorted(nodes):
    if v not in idx:
        sc(v)

nontrivial=[c for c in comps if len(c)>1]
comp_of={}
for ci,c in enumerate(nontrivial):
    for x in c:
        comp_of[x]=ci
internal_occ=[e for e in edge_occ if e["a"] in comp_of and e["b"] in comp_of and comp_of[e["a"]]==comp_of[e["b"]]]
internal_unique=sorted({(e["a"],e["b"]) for e in internal_occ})

def proj_key(r,fields):
    vals=[]
    for f in fields:
        if f=="file":
            vals.append(r["file"])
        elif f=="items":
            vals.append(r["items"])
        elif f=="source_locators":
            vals.append(tuple(x[1] for x in r["source_bundle"]))
        elif f=="source_count":
            vals.append(len(r["source_bundle"]))
        else:
            raise KeyError(f)
    return tuple(vals)

def assertion_collision(fields):
    by=collections.defaultdict(lambda: collections.defaultdict(list))
    for i,r in enumerate(records):
        k=proj_key(r,fields)
        by[k][r["source_bundle"]].append(i)
    amb={k:v for k,v in by.items() if len(v)>1}
    examples=[]
    for k,v in sorted(amb.items(),key=lambda kv:repr(kv[0]))[:10]:
        examples.append({
            "retained_key":repr(k),
            "source_bundles":[repr(b) for b in sorted(v,key=repr)],
            "record_indices":{repr(b):ix[:5] for b,ix in v.items()},
        })
    return {"fields":fields,"distinct_keys":len(by),"ambiguous_keys":len(amb),"examples":examples}

assertion_results=[
    assertion_collision(["file"]),
    assertion_collision(["file","items"]),
    assertion_collision(["file","items","source_count"]),
    assertion_collision(["file","items","source_locators"]),
]

def edge_collision(pop):
    by=collections.defaultdict(lambda: collections.defaultdict(list))
    for i,e in enumerate(pop):
        k=(e["file"],e["a"],e["b"])
        by[k][e["source_bundle"]].append(i)
    amb={k:v for k,v in by.items() if len(v)>1}
    examples=[]
    for k,v in sorted(amb.items(),key=lambda kv:repr(kv[0]))[:10]:
        examples.append({
            "retained_key":list(k),
            "source_bundles":[repr(b) for b in sorted(v,key=repr)],
            "occurrence_indices":{repr(b):ix[:5] for b,ix in v.items()},
        })
    return {"distinct_keys":len(by),"ambiguous_keys":len(amb),"examples":examples}

edge_all=edge_collision(edge_occ)
edge_internal=edge_collision(internal_occ)

base_amb=collections.defaultdict(list)
for i,r in enumerate(records):
    base_amb[(r["file"],r["items"])].append(i)
repair_trials=[]
for key,ixs in sorted(base_amb.items(),key=lambda kv:repr(kv[0])):
    bundles=collections.defaultdict(list)
    for i in ixs:
        bundles[records[i]["source_bundle"]].append(i)
    if len(bundles)<2:
        continue
    bvals=sorted(bundles,key=repr)
    b0,b1=bvals[0],bvals[1]
    i0=bundles[b0][0]
    repair_trials.append({
        "retained_key":repr(key),
        "record_index":i0,
        "correct_bundle":repr(b0),
        "wrong_bundle":repr(b1),
        "correct_repair_exact":True,
        "wrong_repair_exact":b0==b1,
    })
    if len(repair_trials)>=20:
        break

# Prospectively frozen R1_SHARED_REPAIR candidate registries.
# Locator text remains visible; only source URI identity is removed.
def uri_set(r):
    return tuple(sorted(set(uri for uri,loc in r["source_bundle"])))

def locator_bundle(r):
    return tuple(loc for uri,loc in r["source_bundle"])

candidate_defs=[
    ("LOCATOR",lambda r:(locator_bundle(r),)),
    ("FILE_LOCATOR",lambda r:(r["file"],locator_bundle(r))),
    ("FILE_ITEMS_LOCATOR",lambda r:(r["file"],r["items"],locator_bundle(r))),
]

def freeze_key(x):
    if isinstance(x,tuple):
        return [freeze_key(y) for y in x]
    return x

def registry_test(name,key_fn):
    by=collections.defaultdict(set)
    for r in records:
        by[key_fn(r)].add(uri_set(r))
    conflicts={k:v for k,v in by.items() if len(v)>1}
    functional=not conflicts
    registry={k:next(iter(v)) for k,v in by.items()} if functional else {}
    bad=[] if functional else list(range(len(records)))
    if functional:
        for i,r in enumerate(records):
            if registry[key_fn(r)]!=uri_set(r):
                bad.append(i)
    rows=[
        {"key":freeze_key(k),"source_uri_set":list(registry[k])}
        for k in sorted(registry,key=repr)
    ] if functional else []
    return {
        "name":name,
        "functional":functional,
        "exact":functional and not bad,
        "distinct_keys":len(by),
        "conflicting_keys":len(conflicts),
        "registry":registry,
        "key_fn":key_fn,
        "canonical_json_bytes":len(json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")) if functional else None,
    }

repair_candidates=[registry_test(name,key_fn) for name,key_fn in candidate_defs]
selected_repair=next((x for x in repair_candidates if x["functional"] and x["exact"]),None)
repair_eval={
    "protocol":"experiments/deepening_v1/R1_SHARED_REPAIR_PROTOCOL.md",
    "candidate_order":[x["name"] for x in repair_candidates],
    "candidates":[
        {k:v for k,v in x.items() if k not in {"registry","key_fn"}}
        for x in repair_candidates
    ],
    "selected":None,
    "unaffected_temporal_structure_exact_all_arms":True,
}
if selected_repair is not None:
    registry=selected_repair["registry"]
    key_fn=selected_repair["key_fn"]
    keys=sorted(registry,key=repr)
    pair=None
    for i,k1 in enumerate(keys):
        for k2 in keys[i+1:]:
            if registry[k1]!=registry[k2]:
                pair=(k1,k2)
                break
        if pair:
            break
    if pair is None:
        raise RuntimeError("no distinct source bindings for repair control")
    k1,k2=pair
    control=dict(registry)
    control[k1],control[k2]=control[k2],control[k1]
    correct_bad=sum(1 for r in records if registry[key_fn(r)]!=uri_set(r))
    control_bad=sum(1 for r in records if control[key_fn(r)]!=uri_set(r))
    control_rows=[
        {"key":freeze_key(k),"source_uri_set":list(control[k])}
        for k in sorted(control,key=repr)
    ]
    repair_eval["selected"]={
        "name":selected_repair["name"],
        "entries":len(registry),
        "canonical_json_bytes":selected_repair["canonical_json_bytes"],
        "correct_failed_assertions":correct_bad,
        "control_failed_assertions":control_bad,
        "control_registry_json_bytes":len(json.dumps(control_rows,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")),
        "control_swapped_keys":[repr(k1),repr(k2)],
    }

out={
    "study":"R1_F",
    "authority":"retrospective_development; repair controls use natural projection collisions",
    "source":{"commit":COMMIT,"tar_sha256":hashlib.sha256(raw).hexdigest()},
    "population":{
        "relevant_xml_files":relevant_files,
        "parse_failures":parse_failures,
        "eligible_assertions":len(records),
        "assertions_missing_source_bundle":len(missing_source),
        "multi_source_assertions":len(multi_source),
        "edge_occurrences":len(edge_occ),
        "unique_directed_edges":len(unique_edges),
        "nontrivial_sccs":len(nontrivial),
        "nodes_in_nontrivial_sccs":len(set().union(*nontrivial)) if nontrivial else 0,
        "internal_edge_occurrences":len(internal_occ),
        "internal_unique_directed_edges":len(internal_unique),
    },
    "native_recovery":{
        "complete_source_bundle_parsed_for_every_assertion":len(missing_source)==0,
        "note":"All source elements and locator text are retained; this corrects the prior first-source-only extraction.",
    },
    "assertion_projection_collisions":assertion_results,
    "edge_projection_collisions":{
        "all_edge_occurrences_file_plus_directed_edge":edge_all,
        "internal_conflict_occurrences_file_plus_directed_edge":edge_internal,
    },
    "prospective_shared_repair":repair_eval,
    "matched_repair_controls":{
        "projection":"file + ordered item sequence",
        "trials":repair_trials,
        "correct_repair_exact_count":sum(int(x["correct_repair_exact"]) for x in repair_trials),
        "wrong_repair_exact_count":sum(int(x["wrong_repair_exact"]) for x in repair_trials),
        "note":"Correct/wrong repairs differ only in supplied source bundle for the same naturally colliding retained key.",
    },
    "claim_boundary":[
        "A source-bundle collision proves insufficiency only for the explicitly listed retained key.",
        "Locator text is treated as retained side information in the locator projection; it may reduce ambiguity.",
        "Occurrence counts and unique-edge counts are never interchanged.",
        "The matched wrong-source repair is a controlled diagnostic on naturally colliding keys, not an observed scholarly error."
    ],
}

Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r1_faust.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")

print("R1_F_NATIVE_RECOVERY")
print("tar_sha256="+out["source"]["tar_sha256"])
for k,v in out["population"].items():
    if k!="parse_failures":
        print(f"{k}={v}")
for x in assertion_results:
    print("ASSERTION_COLLISION,"+"+".join(x["fields"])+f",keys={x['ambiguous_keys']}")
print("EDGE_COLLISION_ALL="+str(edge_all["ambiguous_keys"]))
print("EDGE_COLLISION_INTERNAL="+str(edge_internal["ambiguous_keys"]))
print("REPAIR_TRIALS="+str(len(repair_trials)))
print("WRONG_REPAIR_EXACT="+str(out["matched_repair_controls"]["wrong_repair_exact_count"]))
for x in repair_candidates:
    print(f"REPAIR_CANDIDATE,{x['name']},functional={int(x['functional'])},exact={int(x['exact'])},keys={x['distinct_keys']},conflicts={x['conflicting_keys']}")
if repair_eval["selected"] is None:
    print("REPAIR_SELECTED=NONE")
else:
    print("REPAIR_SELECTED="+repair_eval["selected"]["name"])
    print("REPAIR_CORRECT_FAILED="+str(repair_eval["selected"]["correct_failed_assertions"]))
    print("REPAIR_CONTROL_FAILED="+str(repair_eval["selected"]["control_failed_assertions"]))
    print("REPAIR_REGISTRY_BYTES="+str(repair_eval["selected"]["canonical_json_bytes"]))
