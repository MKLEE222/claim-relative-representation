from __future__ import annotations
import hashlib
import html
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict

DOWNLOADS="https://www.faustedition.net/macrogenesis/downloads"
UA={"User-Agent":"claim-relative-representation/1.0"}

def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

page=get(DOWNLOADS).decode("utf-8",errors="replace")
links=re.findall(r"href=[\"']([^\"']+\\.gexf(?:\\?[^\"']*)?)[\"']",page,flags=re.I)
if not links:
    print("FAUST_X3C_PUBLISHED_CONFLICT_GRAPH")
    print("STATUS=BLOCKED_TRANSPORT")
    print("REASON=official downloads page exposed no GEXF link to this non-browser client")
    print("GRAPH_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

# Prefer a base.gexf-like official link if available; otherwise fail rather than tune.
base_links=[x for x in links if "base" in x.lower()]
if len(base_links)!=1:
    print("FAUST_X3C_PUBLISHED_CONFLICT_GRAPH")
    print("STATUS=BLOCKED_TRANSPORT")
    print("REASON=base GEXF link was not uniquely exposed to this non-browser client")
    print("GRAPH_OUTCOME_OBSERVED=0")
    raise SystemExit(0)
gexf_url=urllib.parse.urljoin(DOWNLOADS,html.unescape(base_links[0]))
raw=get(gexf_url)

root=ET.fromstring(raw)
ns={"g":"http://www.gexf.net/1.2draft"}

# Attribute-id -> title mapping for edge attributes.
attr_names={}
for attrs in root.findall(".//g:attributes[@class='edge']",ns):
    for a in attrs.findall("./g:attribute",ns):
        attr_names[a.attrib.get("id")]=a.attrib.get("title") or a.attrib.get("id")

nodes=root.findall(".//g:graph/g:nodes/g:node",ns)
edges=root.findall(".//g:graph/g:edges/g:edge",ns)

def edge_attrs(e):
    d={}
    av=e.find("./g:attvalues",ns)
    if av is not None:
        for v in av.findall("./g:attvalue",ns):
            key=attr_names.get(v.attrib.get("for"),v.attrib.get("for"))
            d[key]=v.attrib.get("value")
    # Some exporters may encode attributes directly.
    for k,v in e.attrib.items():
        if k not in {"id","source","target","label","weight","type"}:
            d.setdefault(k,v)
    if "weight" in e.attrib:
        d.setdefault("weight",e.attrib["weight"])
    return d

def truth(v):
    return str(v).strip().lower() in {"1","true","yes"}

records=[]
for e in edges:
    a=edge_attrs(e)
    records.append((e.attrib["source"],e.attrib["target"],a))

ignore=sum(1 for u,v,a in records if truth(a.get("ignore",False)))
delete=sum(1 for u,v,a in records if truth(a.get("delete",False)))
source_count=sum(1 for u,v,a in records if a.get("source"))
weight_count=sum(1 for u,v,a in records if a.get("weight") not in {None,""})

def has_cycle(recs):
    adj=defaultdict(set)
    vertices=set()
    for u,v,a in recs:
        adj[u].add(v)
        vertices.add(u); vertices.add(v)
    color={}
    def dfs(u):
        color[u]=1
        for v in adj.get(u,()):
            if color.get(v,0)==1:
                return True
            if color.get(v,0)==0 and dfs(v):
                return True
        color[u]=2
        return False
    for u in vertices:
        if color.get(u,0)==0 and dfs(u):
            return True
    return False

active=[r for r in records if not truth(r[2].get("ignore",False)) and not truth(r[2].get("delete",False))]

print("FAUST_X3C_PUBLISHED_CONFLICT_GRAPH")
print("gexf_url="+gexf_url)
print("gexf_sha256="+hashlib.sha256(raw).hexdigest())
print("nodes="+str(len(nodes)))
print("edges="+str(len(records)))
print("ignore_true="+str(ignore))
print("delete_true="+str(delete))
print("source_present="+str(source_count))
print("weight_present="+str(weight_count))
print("active_edges="+str(len(active)))
print("all_edges_cycle="+str(int(has_cycle(records))))
print("active_edges_cycle="+str(int(has_cycle(active))))
print("UNIQUE_HISTORICAL_ORDER=NOT_CLAIMED")

assert ignore+delete>0
