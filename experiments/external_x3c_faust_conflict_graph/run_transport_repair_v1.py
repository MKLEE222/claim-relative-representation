from __future__ import annotations
import hashlib, urllib.request, xml.etree.ElementTree as ET
from collections import defaultdict, deque

URL="https://www.faustedition.net/macrogenesis/base.gexf"
UA={"User-Agent":"claim-relative-representation/1.0"}

def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=60) as r:
        return r.read(),r.geturl(),r.headers.get("Content-Type","")

print("FAUST_X3C_TRANSPORT_REPAIR")
try:
    raw,final_url,content_type=get(URL)
except Exception as e:
    print("STATUS=BLOCKED_TRANSPORT")
    print("URL="+URL)
    print("ERROR="+type(e).__name__+":"+str(e).replace("\n"," "))
    print("GRAPH_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

try:
    root=ET.fromstring(raw)
except Exception as e:
    print("STATUS=BLOCKED_TRANSPORT")
    print("URL="+URL)
    print("FINAL_URL="+final_url)
    print("CONTENT_TYPE="+content_type)
    print("BYTES="+str(len(raw)))
    print("SHA256="+hashlib.sha256(raw).hexdigest())
    print("ERROR=NON_XML_RESPONSE:"+type(e).__name__)
    print("GRAPH_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

if root.tag.startswith("{"):
    nsuri=root.tag.split("}",1)[0][1:]
    ns={"g":nsuri}
    q=lambda x: "g:"+x
else:
    ns={}
    q=lambda x:x

attr_names={}
for attrs in root.findall(".//"+q("attributes"),ns):
    if attrs.attrib.get("class")!="edge":
        continue
    for a in attrs.findall("./"+q("attribute"),ns):
        aid=a.attrib.get("id")
        attr_names[aid]=a.attrib.get("title") or aid

nodes=root.findall(".//"+q("graph")+"/"+q("nodes")+"/"+q("node"),ns)
edges=root.findall(".//"+q("graph")+"/"+q("edges")+"/"+q("edge"),ns)

def edge_attrs(e):
    d={}
    av=e.find("./"+q("attvalues"),ns)
    if av is not None:
        for v in av.findall("./"+q("attvalue"),ns):
            key=attr_names.get(v.attrib.get("for"),v.attrib.get("for"))
            d[key]=v.attrib.get("value")
    for k,v in e.attrib.items():
        if k not in {"id","source","target","label","type"}:
            d.setdefault(k,v)
    return d

def truth(v):
    return str(v).strip().lower() in {"1","true","yes"}

records=[]
for e in edges:
    a=edge_attrs(e)
    records.append((e.attrib["source"],e.attrib["target"],a))

ignore=sum(1 for u,v,a in records if truth(a.get("ignore",False)))
delete=sum(1 for u,v,a in records if truth(a.get("delete",False)))
source_count=sum(1 for u,v,a in records if a.get("source") not in {None,""})
weight_count=sum(1 for u,v,a in records if a.get("weight") not in {None,""})

active=[r for r in records if not truth(r[2].get("ignore",False)) and not truth(r[2].get("delete",False))]

def has_cycle(recs):
    vertices=set()
    adj=defaultdict(set)
    indeg=defaultdict(int)
    for u,v,a in recs:
        vertices.add(u); vertices.add(v)
        if v not in adj[u]:
            adj[u].add(v); indeg[v]+=1
        indeg.setdefault(u,indeg.get(u,0))
    dq=deque([x for x in vertices if indeg[x]==0])
    seen=0
    while dq:
        u=dq.popleft(); seen+=1
        for v in adj.get(u,()):
            indeg[v]-=1
            if indeg[v]==0: dq.append(v)
    return seen<len(vertices)

all_cycle=has_cycle(records)
active_cycle=has_cycle(active)

print("STATUS=EXECUTED")
print("gexf_url="+URL)
print("final_url="+final_url)
print("content_type="+content_type)
print("gexf_sha256="+hashlib.sha256(raw).hexdigest())
print("bytes="+str(len(raw)))
print("namespace="+(nsuri if root.tag.startswith("{") else "NONE"))
print("nodes="+str(len(nodes)))
print("edges="+str(len(records)))
print("ignore_true="+str(ignore))
print("delete_true="+str(delete))
print("source_present="+str(source_count))
print("weight_present="+str(weight_count))
print("active_edges="+str(len(active)))
print("all_edges_cycle="+str(int(all_cycle)))
print("active_edges_cycle="+str(int(active_cycle)))
print("STRONG_PATTERN="+str(int(all_cycle and not active_cycle)))
print("UNIQUE_HISTORICAL_ORDER=NOT_CLAIMED")

if ignore+delete==0:
    raise RuntimeError("published graph exposed no ignore/delete state; inspect exporter semantics before interpretation")
