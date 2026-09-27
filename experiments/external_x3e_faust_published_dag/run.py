from __future__ import annotations
import hashlib, re, urllib.request
from collections import defaultdict, deque, Counter

URL="https://www.faustedition.net/macrogenesis/dag-graph.dot"
UA={"User-Agent":"claim-relative-representation/1.0"}

def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=60) as r:
        return r.read(),r.geturl(),r.headers.get("Content-Type","")

print("FAUST_X3E_PUBLISHED_DAG_STAGE")
try:
    raw,final_url,ctype=get(URL)
except Exception as e:
    print("STATUS=BLOCKED_TRANSPORT")
    print("URL="+URL)
    print("ERROR="+type(e).__name__+":"+str(e).replace("\n"," "))
    print("DAG_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

text=raw.decode("utf-8",errors="replace")
if "digraph" not in text.lower() and "->" not in text:
    print("STATUS=BLOCKED_TRANSPORT")
    print("URL="+URL)
    print("FINAL_URL="+final_url)
    print("CONTENT_TYPE="+ctype)
    print("BYTES="+str(len(raw)))
    print("SHA256="+hashlib.sha256(raw).hexdigest())
    print("ERROR=RESPONSE_NOT_DIRECTED_DOT")
    print("DAG_OUTCOME_OBSERVED=0")
    raise SystemExit(0)

# Graphviz node IDs may be quoted strings or unquoted tokens.
Q=r'"(?:[^"\\]|\\.)*"'
U=r'[A-Za-z0-9_.:/#-]+'
edge_re=re.compile(rf'(?m)^\s*(?P<u>{Q}|{U})\s*->\s*(?P<v>{Q}|{U})\b')

def unquote(x):
    x=x.strip()
    if len(x)>=2 and x[0]=='"' and x[-1]=='"':
        # For graph identity/cycle purposes escaped lexical form is sufficient;
        # only strip the outer quotes.
        return x[1:-1]
    return x

edges=[]
for m in edge_re.finditer(text):
    edges.append((unquote(m.group("u")),unquote(m.group("v"))))

if not edges:
    print("STATUS=PARSE_FAILURE")
    print("URL="+URL)
    print("FINAL_URL="+final_url)
    print("CONTENT_TYPE="+ctype)
    print("BYTES="+str(len(raw)))
    print("SHA256="+hashlib.sha256(raw).hexdigest())
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
print("sha256="+hashlib.sha256(raw).hexdigest())
print("bytes="+str(len(raw)))
print("directed_edge_statements="+str(len(edges)))
print("unique_directed_pairs="+str(len(unique_edges)))
print("duplicate_directed_pairs="+str(duplicates))
print("nodes_on_directed_edges="+str(len(nodes)))
print("published_dag_cycle="+str(int(cyclic)))
print("BASE_X3C_CYCLE=1")
print("BASE_FILTERED_X3C_CYCLE=1")
print("STAGE_SEPARATION_STRONG_PATTERN="+str(int(not cyclic)))
print("UNIQUE_HISTORICAL_ORDER=NOT_CLAIMED")
