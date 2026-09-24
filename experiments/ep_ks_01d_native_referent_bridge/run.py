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
FORBIDDEN={"tanner","wall","poet","visited"}

@dataclass
class W:
    start:int
    words:list[str]

def get():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def toks(s):
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
        raise RuntimeError("seed not found")
    start=max(text.rfind("\n",0,a),0)
    end=text.find("\n",b)
    return text[start:end]

def addenda(text):
    m=re.search(r"NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE[’']S\s+EDITION",text,flags=re.I)
    if not m:
        raise RuntimeError("addenda boundary not found")
    return m.start()

def note1_aliases(text,seed_pos):
    m=re.search(r"NOTE\s+1\.—KINSAY\b",text[seed_pos:],flags=re.I)
    if not m:
        raise RuntimeError("seed-side Kinsay Note 1 not found")
    s=seed_pos+m.start()
    e=text.find(".",s)
    if e<0:
        raise RuntimeError("Note 1 first sentence end not found")
    sent=text[s:e+1]

    names=[]
    # All-uppercase names and hyphenated mixed-case historical forms.
    for tok in re.findall(r"\b[A-Za-z]+(?:-[A-Za-z]+)+\b|\b[A-Z]{4,}\b",sent):
        if tok.upper()=="NOTE":
            continue
        names.append(tok)

    expanded=[]
    for n in names:
        expanded.append(n.lower())
        if "-" in n:
            expanded.extend(p.lower() for p in n.split("-") if len(p)>=3)
    # stable order, no duplicates
    seen=set()
    return [x for x in expanded if not (x in seen or seen.add(x))],sent

def windows(text):
    ts=toks(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2:
            out.append(W(s,ch))
    return out

def idf(ws):
    n=len(ws)
    df=collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def base_query(seed,base_ws):
    c=collections.Counter(t for t in toks(seed+" "+TASK) if t not in STOP and len(t)>=4)
    iw=idf(base_ws)
    return sorted(((t,n*iw.get(t,1.0)) for t,n in c.items()),key=lambda z:(-z[1],z[0]))[:K]

def target(ws):
    a=set(toks(TARGET_A)); b=set(toks(TARGET_B))
    for w in ws:
        s=set(w.words)
        if a<=s and b<=s:
            return w
    raise RuntimeError("target not found")

def score(w,q):
    c=collections.Counter(w.words)
    return sum(weight*min(c.get(term,0),3) for term,weight in q)

raw=get()
sha=hashlib.sha256(raw).hexdigest()
assert sha==EXPECTED_SHA
text=raw.decode("utf-8",errors="replace")
seed=locate_seed(text)
seed_pos=text.lower().find(SEED_A.lower())
boundary=addenda(text)
base_ws=windows(text[:boundary])
later_ws=windows(text[boundary:])
tgt=target(later_ws)

q=base_query(seed,base_ws)
aliases,sentence=note1_aliases(text,seed_pos)
median=sorted(w for t,w in q)[len(q)//2]
qmap={t:w for t,w in q}
for a in aliases:
    if a not in STOP and len(a)>=3:
        qmap.setdefault(a,median)
bridged=sorted(qmap.items())

if set(t for t,w in bridged) & FORBIDDEN:
    raise RuntimeError("target-only leakage detected")

ranked=sorted(((score(w,bridged),w) for w in later_ws),key=lambda z:(-z[0],z[1].start))
rank=None; tscore=None
for i,(s,w) in enumerate(ranked,1):
    if abs(w.start-tgt.start)<STRIDE:
        rank=i; tscore=s; break

print("EP_KS_01D_NATIVE_REFERENT_BRIDGE")
print("source_sha256="+sha)
print("aliases="+"|".join(aliases))
print("query_terms="+"|".join(t for t,w in bridged))
print("forbidden_query_overlap=0")
print(f"RESULT,candidates={len(ranked)},target_rank={rank},target_score={tscore},MRR={(0 if rank is None else 1/rank):.6f},H10={int(rank is not None and rank<=10)},H20={int(rank is not None and rank<=20)},H50={int(rank is not None and rank<=50)}")
print("BASELINE_V1_LATER_RANK=304")
print("BASELINE_V1_LATER_SCORE=0")
print("GENERAL_TRANSFER_CLAIM=0")
