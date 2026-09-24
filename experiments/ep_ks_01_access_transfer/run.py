from __future__ import annotations
import collections
import hashlib
import math
import re
import urllib.request
from dataclasses import dataclass

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED_SHA="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"

TASK="Find later editorial material in the same declared edition that bears on whether Marco Polo personally observed the Kinsay description."
SEED_A="written statement which the Queen"
SEED_B="For truth it was"
TARGET_A="Mr. P. von Tanner"
TARGET_B="never visited Hang Chau"

WINDOW=180
STRIDE=90
K=12

STOP={
"the","and","that","this","with","from","have","has","had","were","was","are","for","not","but",
"his","her","their","there","which","into","than","then","they","them","you","your","its","who",
"whom","what","when","where","how","all","any","some","more","most","such","only","been","being",
"will","would","could","should","about","over","under","after","before","between","also","very",
"upon","our","out","off","one","two","same","find","material","edition","bears","whether"
}

FORBIDDEN={"tanner","wall","poet","visited","chau"}

@dataclass
class W:
    scope:str
    start:int
    words:list[str]

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def toks(s):
    # hyphenated forms contribute both whole and component tokens.
    base=re.findall(r"[A-Za-z][A-Za-z'-]{2,}",s.lower())
    out=[]
    for x in base:
        out.append(x)
        if "-" in x:
            out.extend(p for p in x.split("-") if len(p)>=3)
    return out

def locate_seed(text):
    low=text.lower()
    a=low.find(SEED_A.lower())
    b=low.find(SEED_B.lower(),a)
    if a<0 or b<0:
        raise RuntimeError("seed anchors not found")
    end=text.find("\n",b)
    if end<0: end=b+600
    # exact local paragraph-sized native span, not an arbitrary broad context window.
    start=max(text.rfind("\n",0,a),0)
    return text[start:end]

def locate_addenda(text):
    m=re.search(r"NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE[’']S\s+EDITION",text,flags=re.I)
    if not m:
        raise RuntimeError("native Addenda boundary not found")
    return m.start()

def windows(scope,text):
    ts=toks(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2:
            out.append(W(scope,s,ch))
    return out

def find_target(ws):
    need_a=set(toks(TARGET_A))
    need_b=set(toks(TARGET_B))
    for w in ws:
        s=set(w.words)
        if need_a<=s and need_b<=s:
            return w
    raise RuntimeError("target evaluation window not found")

def idf(ws):
    n=len(ws)
    df=collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def query(seed,base_ws):
    counts=collections.Counter(t for t in toks(seed+" "+TASK) if t not in STOP and len(t)>=4)
    weights=idf(base_ws)
    scored=sorted(((t,c*weights.get(t,1.0)) for t,c in counts.items()),key=lambda z:(-z[1],z[0]))
    q=scored[:K]
    qterms={t for t,w in q}
    leak=sorted(qterms & FORBIDDEN)
    if leak:
        raise RuntimeError("TARGET LEAKAGE: "+",".join(leak))
    return q

def score(w,q):
    c=collections.Counter(w.words)
    return sum(weight*min(c.get(term,0),3) for term,weight in q)

def rank(ws,target,q):
    ranked=sorted(((score(w,q),w) for w in ws),key=lambda z:(-z[0],z[1].start))
    for i,(s,w) in enumerate(ranked,1):
        if abs(w.start-target.start)<STRIDE and w.scope==target.scope:
            return i,s,ranked
    return None,None,ranked

raw=fetch()
sha=hashlib.sha256(raw).hexdigest()
assert sha==EXPECTED_SHA, (sha,EXPECTED_SHA)
text=raw.decode("utf-8",errors="replace")

seed=locate_seed(text)
boundary=locate_addenda(text)
base=text[:boundary]
later=text[boundary:]

base_ws=windows("BASE",base)
full_ws=windows("FULL",text)
later_ws=windows("LATER",later)
target_later=find_target(later_ws)

# Map target to the full-object token coordinate by finding evaluation anchors there independently.
target_full=find_target(full_ws)
q=query(seed,base_ws)

print("EP_KS_01_GENERIC_ACCESS_TRANSFER")
print("source_sha256="+sha)
print("addenda_char_offset="+str(boundary))
print("query_terms="+"|".join(t for t,w in q))
print("forbidden_query_overlap=0")

for name,ws,target in [
    ("GSA_FULL_OBJECT",full_ws,target_full),
    ("GSA_LATER_LAYER",later_ws,target_later),
]:
    r,s,ranked=rank(ws,target,q)
    rr=0 if r is None else 1/r
    print(",".join([
        "RESULT",name,
        f"candidates={len(ranked)}",
        f"target_rank={r if r is not None else 'NA'}",
        f"target_score={s if s is not None else 'NA'}",
        f"MRR={rr:.6f}",
        f"H10={int(r is not None and r<=10)}",
        f"H20={int(r is not None and r<=20)}",
        f"H50={int(r is not None and r<=50)}",
    ]))

print("CLAIM_STATE_OPENED=0")
