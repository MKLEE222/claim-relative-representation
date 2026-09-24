from __future__ import annotations

import hashlib
import io
import tarfile
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

COMMIT="502eca65120dd6189ceaf41d4e5017775e6e4677"
URL=f"https://github.com/faustedition/faust-xml/archive/{COMMIT}.tar.gz"
NS={"f":"http://www.faustedition.net/ns"}

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=60) as r:
    raw=r.read()

tf=tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz")

files=[]
relations=0
edges=[]
sources=Counter()
nodes=set()

for member in tf.getmembers():
    name=member.name
    if not member.isfile():
        continue
    if "/xml/macrogenesis/" not in name or not name.endswith(".xml"):
        continue
    f=tf.extractfile(member)
    if f is None:
        continue
    data=f.read()
    try:
        root=ET.fromstring(data)
    except ET.ParseError:
        continue
    used=False
    for rel in root.findall(".//f:relation[@name='temp-pre']",NS):
        items=[x.attrib.get("uri") for x in rel.findall("./f:item",NS) if x.attrib.get("uri")]
        if len(items)<2:
            continue
        src=rel.find("./f:source",NS)
        src_uri=src.attrib.get("uri") if src is not None else None
        locator=" ".join((src.text or "").split()) if src is not None else ""
        relations+=1
        used=True
        if src_uri:
            sources[src_uri]+=1
        for a,b in zip(items,items[1:]):
            nodes.add(a); nodes.add(b)
            edges.append((a,b,src_uri,locator,name))
    if used:
        files.append(name)

adj=defaultdict(set)
for a,b,src,loc,file in edges:
    adj[a].add(b)

# Direct reciprocal unordered pairs.
recip=set()
for a,vs in adj.items():
    for b in vs:
        if a in adj.get(b,set()):
            recip.add(tuple(sorted((a,b))))

# Tarjan SCC.
index=0
stack=[]
onstack=set()
idx={}
low={}
sccs=[]

def strongconnect(v):
    global index
    idx[v]=index
    low[v]=index
    index+=1
    stack.append(v)
    onstack.add(v)
    for w in adj.get(v,set()):
        if w not in idx:
            strongconnect(w)
            low[v]=min(low[v],low[w])
        elif w in onstack:
            low[v]=min(low[v],idx[w])
    if low[v]==idx[v]:
        comp=[]
        while True:
            w=stack.pop()
            onstack.remove(w)
            comp.append(w)
            if w==v:
                break
        sccs.append(comp)

for v in sorted(nodes):
    if v not in idx:
        strongconnect(v)

nontrivial=[set(c) for c in sccs if len(c)>1]
conflict_nodes=set().union(*nontrivial) if nontrivial else set()
internal_edges=0
source_in_conflicts=Counter()
for a,b,src,loc,file in edges:
    if any(a in c and b in c for c in nontrivial):
        internal_edges+=1
        if src:
            source_in_conflicts[src]+=1

print("FAUST_X3D_RAW_ASSERTION_CONFLICT_ECOLOGY")
print("tar_sha256="+hashlib.sha256(raw).hexdigest())
print("source_xml_files="+str(len(files)))
print("temp_pre_relations="+str(relations))
print("directed_edges="+str(len(edges)))
print("distinct_nodes="+str(len(nodes)))
print("distinct_source_uris="+str(len(sources)))
print("direct_reciprocal_pairs="+str(len(recip)))
print("nontrivial_sccs="+str(len(nontrivial)))
print("nodes_in_nontrivial_sccs="+str(len(conflict_nodes)))
print("edges_inside_nontrivial_sccs="+str(internal_edges))
print("sources_represented_inside_conflict_sccs="+str(len(source_in_conflicts)))
print("RAW_ASSERTION_GRAPH_ACYCLIC="+str(int(len(nontrivial)==0)))
print("PUBLISHED_FES_REPRODUCED=0")

# No expected direction is asserted, but source universe must be nonempty.
assert relations>0 and len(edges)>0
