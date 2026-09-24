from __future__ import annotations
import collections
import hashlib
import io
import tarfile
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="502eca65120dd6189ceaf41d4e5017775e6e4677"
URL=f"https://github.com/faustedition/faust-xml/archive/{COMMIT}.tar.gz"
NS={"f":"http://www.faustedition.net/ns"}

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=60) as r:
    raw=r.read()

tf=tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz")
records=[]
file_sources=collections.defaultdict(set)

for member in tf.getmembers():
    name=member.name
    if not member.isfile() or "/xml/macrogenesis/" not in name or not name.endswith(".xml"):
        continue
    f=tf.extractfile(member)
    if f is None:
        continue
    data=f.read()
    try:
        root=ET.fromstring(data)
    except ET.ParseError:
        continue
    for rel in root.findall(".//f:relation[@name='temp-pre']",NS):
        items=[x.attrib.get("uri") for x in rel.findall("./f:item",NS) if x.attrib.get("uri")]
        if len(items)<2:
            continue
        src=rel.find("./f:source",NS)
        src_uri=src.attrib.get("uri") if src is not None else None
        locator=" ".join((src.text or "").split()) if src is not None else ""
        records.append((name,tuple(items),src_uri,locator))
        if src_uri:
            file_sources[name].add(src_uri)

edges=[]
for name,items,src,loc in records:
    for a,b in zip(items,items[1:]):
        edges.append((a,b,src,loc,name))

# SCCs for task A.
adj=collections.defaultdict(set)
nodes=set()
for a,b,src,loc,name in edges:
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
        c=[]
        while True:
            w=stack.pop(); on.remove(w); c.append(w)
            if w==v: break
        comps.append(set(c))

for v in sorted(nodes):
    if v not in idx: sc(v)

nontrivial=[c for c in comps if len(c)>1]
conflict_nodes=set().union(*nontrivial) if nontrivial else set()
conflict_edges=[e for e in edges if e[0] in conflict_nodes and e[1] in conflict_nodes and any(e[0] in c and e[1] in c for c in nontrivial)]

# File-context substitution test.
ambiguous_files={f:s for f,s in file_sources.items() if len(s)!=1}
source_to_files=collections.defaultdict(set)
for f,ss in file_sources.items():
    for s in ss:
        source_to_files[s].add(f)

file_context_functional = bool(file_sources) and not ambiguous_files
# This is only functional equivalence to source URI within the frozen corpus.
# It does not claim the path text independently means the bibliography entry.

print("MC_FA_01_RAW_CONFLICT_CARRIERS")
print("tar_sha256="+hashlib.sha256(raw).hexdigest())
print("relations="+str(len(records)))
print("directed_edges="+str(len(edges)))
print("conflict_sccs="+str(len(nontrivial)))
print("conflict_edges="+str(len(conflict_edges)))
print("TASK_A_MINIMAL=ORDERED_ITEMS")
print("source_bearing_files="+str(len(file_sources)))
print("ambiguous_file_to_source_mappings="+str(len(ambiguous_files)))
print("FILE_CONTEXT_FUNCTIONALLY_DETERMINES_SOURCE_URI="+str(int(file_context_functional)))
if file_context_functional:
    print("TASK_B_MINIMAL_FAMILIES=ORDERED_ITEMS+SOURCE_URI|ORDERED_ITEMS+FILE_CONTEXT")
else:
    print("TASK_B_MINIMAL_FAMILIES=ORDERED_ITEMS+SOURCE_URI")
for f,ss in sorted(ambiguous_files.items())[:10]:
    print("AMBIGUOUS_FILE,"+f+","+"|".join(sorted(ss)))

assert records and edges and nontrivial
