from __future__ import annotations
import hashlib, re, urllib.request
from collections import defaultdict, deque, Counter

URL="https://www.faustedition.net/macrogenesis/dag-graph.dot"
EXPECTED_SHA="a76c25331da9408560682c835de8cf5f02ee2773a6f3595fa086aee1fa2c849b"
UA={"User-Agent":"claim-relative-representation/1.0"}

def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=60) as r:
        return r.read(),r.geturl(),r.headers.get("Content-Type","")

print("FAUST_X3E_PUBLISHED_DAG_STAGE_PARSE_REPAIR")
try:
    raw,final_url,ctype=get(URL)
except Exception as e:
    print("STATUS=BLOCKED_TRANSPORT")
    print("ERROR="+type(e).__name__+":"+str(e).replace("\n"," "))
    print("DAG_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

sha=hashlib.sha256(raw).hexdigest()
print("sha256="+sha)
print("bytes="+str(len(raw)))
if sha!=EXPECTED_SHA:
    print("STATUS=SOURCE_DRIFT")
    print("EXPECTED_SHA="+EXPECTED_SHA)
    print("DAG_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

text=raw.decode("utf-8",errors="replace")
print("raw_directed_operator_count="+str(text.count("->")))
print("raw_undirected_operator_count="+str(text.count("--")))

Q=r'"(?:[^"\\]|\\.)*"'
U=r'[A-Za-z0-9_.:/#-]+'
# The post-v delimiter is asserted without consuming it.
edge_re=re.compile(rf'(?m)^\s*(?P<u>{Q}|{U})\s*->\s*(?P<v>{Q}|{U})(?=\s|\[|;|$)')

def unquote(x):
    x=x.strip()
    return x[1:-1] if len(x)>=2 and x[0]=='"' and x[-1]=='"' else x

edges=[(unquote(m.group("u")),unquote(m.group("v"))) for m in edge_re.finditer(text)]

if not edges:
    print("STATUS=PARSE_FAILURE")
    print("URL="+URL)
    print("FINAL_URL="+final_url)
    print("CONTENT_TYPE="+ctype)
    print("DIRECTED_EDGES=0")
    print("DAG_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

pairs=Counter(edges)
unique_edges=list(pairs)
nodes=set()
adj=defaultdict(set)
indeg=defaultdict(int)
for u,v in unique_edges:
    nodes.add(u); nodes.add(v)
    if v not in adj[u]:
        adj[u].add(v); indeg[v]+=1
    indeg.setdefault(u,indeg.get(u,0))

q=deque([n for n in nodes if indeg[n]==0])
seen=0
while q:
    u=q.popleft(); seen+=1
    for v in adj.get(u,()):
        indeg[v]-=1
        if indeg[v]==0: q.append(v)
cyclic=seen<len(nodes)

duplicates=sum(c-1 for c in pairs.values() if c>1)

print("STATUS=EXECUTED")
print("url="+URL)
print("final_url="+final_url)
print("content_type="+ctype)
print("directed_edge_statements="+str(len(edges)))
print("unique_directed_pairs="+str(len(unique_edges)))
print("duplicate_directed_pairs="+str(duplicates))
print("nodes_on_directed_edges="+str(len(nodes)))
print("published_dag_cycle="+str(int(cyclic)))
print("BASE_X3C_CYCLE=1")
print("BASE_FILTERED_X3C_CYCLE=1")
print("STAGE_SEPARATION_STRONG_PATTERN="+str(int(not cyclic)))
print("UNIQUE_HISTORICAL_ORDER=NOT_CLAIMED")
