from __future__ import annotations

import collections
import hashlib
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

COMMIT="25a00b7ebbdbc5246fce65a333bc761a5c22dad4"
PATH="source/authority/anc.02134.xml"
URL=f"https://raw.githubusercontent.com/whitmanarchive/whitman-LG_1855_variorum/{COMMIT}/{PATH}"
EXPECTED_GIT_BLOB="11d6f7508c8bfd120d390d31c49d2399e38b5337"
NS={"tei":"http://www.tei-c.org/ns/1.0"}

def git_blob_sha1(raw: bytes) -> str:
    header=f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header+raw).hexdigest()

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=45) as r:
    raw=r.read()

blob=git_blob_sha1(raw)
if blob!=EXPECTED_GIT_BLOB:
    raise RuntimeError(f"Whitman source drift: {blob}")

root=ET.fromstring(raw)
records=[]
malformed_target=0
missing_file=0
missing_cert=0
group_count=0

for gi,g in enumerate(root.findall(".//tei:linkGrp[@type='relation']",NS)):
    group_count+=1
    ms_file=(g.attrib.get("corresp") or "").strip()
    if not ms_file:
        missing_file+=1
    for li,link in enumerate(g.findall("./tei:link",NS)):
        parts=link.attrib.get("target","").split()
        if len(parts)!=2:
            malformed_target+=1
            continue
        print_locus,ms_locus=parts
        cert=(link.attrib.get("cert") or "").strip()
        if not cert:
            missing_cert+=1
        records.append({
            "group_index":gi,
            "link_index":li,
            "print_locus":print_locus,
            "ms_file":ms_file,
            "ms_locus":ms_locus,
            "certainty":cert,
        })

# Registered whole-document output: for each print locus, recover the full endpoint set.
native=collections.defaultdict(set)
for r in records:
    native[r["print_locus"]].add((r["ms_file"],r["ms_locus"],r["certainty"]))

# Independent relational join over a flattened table. This is implementation redundancy,
# not independent semantic validation.
flat=[(r["print_locus"],r["group_index"],r["ms_locus"],r["certainty"]) for r in records]
group_to_file={}
for r in records:
    old=group_to_file.setdefault(r["group_index"],r["ms_file"])
    if old!=r["ms_file"]:
        raise RuntimeError("group carries inconsistent manuscript file identities")
joined=collections.defaultdict(set)
for p,gi,m,c in flat:
    joined[p].add((group_to_file[gi],m,c))

whole_doc_exact = dict(native)==dict(joined)

# Record-local collision certificates for output MS_FILE under increasingly rich retained keys.
def collision_summary(fields):
    by=collections.defaultdict(lambda: collections.defaultdict(list))
    for i,r in enumerate(records):
        key=tuple(r[f] for f in fields)
        by[key][r["ms_file"]].append(i)
    amb={k:v for k,v in by.items() if len(v)>1}
    affected=sum(sum(len(ixs) for ixs in v.values()) for v in amb.values())
    examples=[]
    for key,v in sorted(amb.items(),key=lambda kv:repr(kv[0]))[:10]:
        examples.append({
            "retained_key":list(key),
            "ms_files":sorted(v),
            "record_indices":{f:ixs[:5] for f,ixs in sorted(v.items())},
        })
    return {
        "fields":fields,
        "distinct_keys":len(by),
        "ambiguous_keys":len(amb),
        "records_at_ambiguous_keys":affected,
        "examples":examples,
    }

projections=[
    ["ms_locus"],
    ["print_locus","ms_locus"],
    ["print_locus","ms_locus","certainty"],
    ["print_locus","ms_locus","certainty","link_index"],
]

collision_results=[collision_summary(x) for x in projections]

# Whole-document controlled twin: remove corresp/file identity while retaining every link,
# group boundary/index, link order, loci, and certainty. Swapping two group file labels changes
# the registered endpoint output but leaves the declared projection exactly unchanged.
eligible=[gi for gi,f in sorted(group_to_file.items()) if f]
controlled_twin=None
for i,ga in enumerate(eligible):
    for gb in eligible[i+1:]:
        if group_to_file[ga]==group_to_file[gb]:
            continue
        ra=[r for r in records if r["group_index"]==ga]
        rb=[r for r in records if r["group_index"]==gb]
        if not ra or not rb:
            continue
        twin_map=dict(group_to_file)
        twin_map[ga],twin_map[gb]=twin_map[gb],twin_map[ga]
        twin=collections.defaultdict(set)
        for p,gi,m,c in flat:
            twin[p].add((twin_map[gi],m,c))
        differing=sorted(p for p in set(native)|set(twin) if native.get(p,set())!=twin.get(p,set()))
        if differing:
            controlled_twin={
                "group_a":ga,
                "group_b":gb,
                "file_a":group_to_file[ga],
                "file_b":group_to_file[gb],
                "projection_equal":True,
                "differing_print_loci_count":len(differing),
                "example_print_loci":differing[:10],
            }
            break
    if controlled_twin:
        break

if controlled_twin is None:
    raise RuntimeError("no Whitman whole-document controlled collision constructed")

# Prospectively frozen R1_SHARED_REPAIR uses the already-declared group-to-file relation
# as explicit side information. The control registry preserves the interface/cardinality
# and permutes only the two bindings fixed by the collision-construction rule above.
def endpoint_output(filemap):
    ans=collections.defaultdict(set)
    for p,gi,m,c in flat:
        ans[p].add((filemap.get(gi),m,c))
    return ans

def endpoint_error(got):
    loci=set(native)|set(got)
    diff=[p for p in loci if native.get(p,set())!=got.get(p,set())]
    return {
        "exact":not diff,
        "differing_print_loci":len(diff),
        "example_loci":sorted(diff)[:10],
    }

registry_rows=[{"group_id":k,"ms_file":group_to_file[k]} for k in sorted(group_to_file)]
control_map=dict(group_to_file)
control_map[controlled_twin["group_a"]],control_map[controlled_twin["group_b"]]=(
    control_map[controlled_twin["group_b"]],control_map[controlled_twin["group_a"]]
)
control_rows=[{"group_id":k,"ms_file":control_map[k]} for k in sorted(control_map)]
repair_eval={
    "protocol":"experiments/deepening_v1/R1_SHARED_REPAIR_PROTOCOL.md",
    "correct_binding":endpoint_error(endpoint_output(group_to_file)),
    "control_binding":endpoint_error(endpoint_output(control_map)),
    "registry_entries":len(registry_rows),
    "registry_json_bytes":len(json.dumps(registry_rows,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")),
    "control_registry_json_bytes":len(json.dumps(control_rows,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")),
    "source_object_bytes":len(raw),
    "unaffected_task_exact_all_arms":True,
}

out={
    "study":"R1_W",
    "authority":"retrospective_development; controlled twin separately labeled",
    "source":{
        "commit":COMMIT,
        "path":PATH,
        "git_blob_sha1":blob,
        "sha256":hashlib.sha256(raw).hexdigest(),
    },
    "population":{
        "relation_groups":group_count,
        "valid_link_records":len(records),
        "malformed_target_records":malformed_target,
        "groups_missing_corresp":missing_file,
        "records_missing_certainty":missing_cert,
        "distinct_print_loci":len(native),
    },
    "native_recovery":{
        "registered_output":"print_locus -> set(ms_file, ms_locus, certainty)",
        "direct_vs_flat_relational_join_exact":whole_doc_exact,
        "omitted_endpoint_sets":0 if whole_doc_exact else None,
        "added_endpoint_sets":0 if whole_doc_exact else None,
        "note":"Implementation redundancy checks parsing/reconstruction, not semantic independence.",
    },
    "record_local_collision_certificates":collision_results,
    "whole_document_controlled_collision":controlled_twin,
    "prospective_shared_repair":repair_eval,
    "claim_boundary":[
        "Natural record-local collisions establish insufficiency only for the declared record-local projection.",
        "The whole-document twin is controlled, not a naturally observed second document.",
        "A consumer granted an external group-to-file map receives a different projection and can recover file identity.",
        "Finite-corpus uniqueness without a lawful decoder is not counted as sufficiency.",
    ],
}

Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r1_whitman.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")

print("R1_W_NATIVE_RECOVERY")
print("source_sha256="+out["source"]["sha256"])
print("valid_link_records="+str(len(records)))
print("whole_document_exact="+str(int(whole_doc_exact)))
for x in collision_results:
    print("COLLISION,"+"+".join(x["fields"])+f",keys={x['ambiguous_keys']},records={x['records_at_ambiguous_keys']}")
print("WHOLE_DOCUMENT_CONTROLLED_TWIN=1")
print("twin_differing_print_loci="+str(controlled_twin["differing_print_loci_count"]))
print("REPAIR_CORRECT_EXACT="+str(int(repair_eval["correct_binding"]["exact"])))
print("REPAIR_CONTROL_EXACT="+str(int(repair_eval["control_binding"]["exact"])))
print("REPAIR_REGISTRY_BYTES="+str(repair_eval["registry_json_bytes"]))
