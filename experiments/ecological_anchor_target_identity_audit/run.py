from __future__ import annotations

import collections
import hashlib
import math
import re
import urllib.request
from dataclasses import dataclass

URLS={
    "V1":"https://www.gutenberg.org/cache/epub/10636/pg10636.txt",
    "V2":"https://www.gutenberg.org/cache/epub/12410/pg12410.txt",
}
EXPECTED={
    "V1":"7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5",
    "V2":"c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c",
}
WINDOW=180
STRIDE=90
QUERY_K=12
STOP={
    "the","and","that","this","with","from","have","has","had","were","was","are","for","not",
    "but","his","her","their","there","which","into","than","then","they","them","you","your",
    "its","who","whom","what","when","where","how","all","any","some","more","most","such",
    "only","seems","made","make","makes","been","being","will","would","could","should","about",
    "over","under","after","before","between","also","very","upon","our","out","off","one","two",
    "marco","polo","china","paper"
}
TARGET1={"regarding","bretschneider"}
TARGET2={"laufer"}

@dataclass
class W:
    doc:str
    start:int
    words:list[str]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def toks(s):
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}",s.lower())

def make_windows(doc,text):
    ts=toks(text); out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2:
            out.append(W(doc,s,ch))
    return out

def strict_target(w):
    s=set(w.words)
    return TARGET1<=s and TARGET2<=s

def normalize_terms(words):
    out=set()
    for w in words:
        out.add(w)
        if "-" in w:
            out.update(x for x in w.split("-") if x)
    return out

def find_seed(ws):
    for w in ws:
        s=set(w.words)
        if {"bretschneider","broussonetia"}<=s:
            return w
    raise RuntimeError("PM02 seed not found")

def idf(ws):
    n=len(ws); df=collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def generic_query(seed,w1):
    iw=idf(w1)
    tf=collections.Counter(t for t in seed.words if t not in STOP and len(t)>=4)
    q=sorted(((t,c*iw.get(t,1.0)) for t,c in tf.items()),key=lambda z:(-z[1],z[0]))[:QUERY_K]
    if any(t=="laufer" for t,w in q):
        raise RuntimeError("target leakage")
    return q

def score(w,q):
    c=collections.Counter(w.words)
    return sum(weight*min(c.get(t,0),3) for t,weight in q)

def seed_context(v1):
    low=v1.lower()
    p=low.find("broussonetia")
    if p<0: raise RuntimeError("Broussonetia missing")
    ctx=v1[max(0,p-1200):p+1800]
    if "bretschneider" not in ctx.lower():
        raise RuntimeError("Bretschneider missing in PM02 context")
    return ctx

def surname_from_context(ctx):
    m=re.search(r"\bDr\.?\s+([A-Z][A-Za-z-]+)",ctx)
    if not m: raise RuntimeError("source surname missing")
    return m.group(1).lower()

def addenda(v2):
    m=re.search(r"notes\s+and\s+addenda\s+to\s+sir\s+henry\s+yule(?:['’]s)?\s+edition",v2,flags=re.I)
    if not m: raise RuntimeError("addenda boundary missing")
    return v2[m.start():]

raw={k:fetch(v) for k,v in URLS.items()}
for k,b in raw.items():
    got=hashlib.sha256(b).hexdigest()
    if got!=EXPECTED[k]:
        raise RuntimeError(f"{k} hash drift: {got}")

text={k:b.decode("utf-8",errors="replace") for k,b in raw.items()}
w1=make_windows("V1",text["V1"])
w2=make_windows("V2",text["V2"])
seed=find_seed(w1)

print("PM_TARGET_IDENTITY_AUDIT_V1")
print("sha256_V1="+EXPECTED["V1"])
print("sha256_V2="+EXPECTED["V2"])
print("strict_rule=candidate_contains_regarding+bretschneider+laufer")

# E1 generic declared collection.
q=generic_query(seed,w1)
ranked=[]
for w in w1+w2:
    if w.doc==seed.doc and abs(w.start-seed.start)<WINDOW:
        continue
    ranked.append((score(w,q),w))
ranked.sort(key=lambda z:(-z[0],z[1].doc,z[1].start))
generic_rank=next((i for i,(_,w) in enumerate(ranked,1) if strict_target(w)),None)
print(f"RESULT,E1_DECLARED_COLLECTION,candidates={len(ranked)},strict_target_rank={generic_rank if generic_rank else 'NA'},H12={int(generic_rank is not None and generic_rank<=12)},H20={int(generic_rank is not None and generic_rank<=20)}")

# E1D.
ctx=seed_context(text["V1"])
surname=surname_from_context(ctx)
seed_terms=normalize_terms(seed.words)
domain_vocab={"mulberry","mulberry-trees","bark","broussonetia","papyrifera","bank-notes","money"}
active=sorted(domain_vocab & seed_terms)
scope=w1+w2
named=[]
for w in scope:
    if w.doc==seed.doc and abs(w.start-seed.start)<WINDOW:
        continue
    norm=normalize_terms(w.words)
    if surname in norm:
        named.append(w)
active_norm=normalize_terms(active)
filtered=[w for w in named if normalize_terms(w.words) & active_norm]
for name,cands in (
    ("E1D_NAMED_SOURCE",named),
    ("E1D_NAMED_SOURCE_DOMAIN",filtered),
):
    ordn=next((i for i,w in enumerate(cands,1) if strict_target(w)),None)
    print(f"RESULT,{name},candidates={len(cands)},strict_target_in_set={int(ordn is not None)},strict_target_ordinal={ordn if ordn else 'NA'}")

# E1W.
ad=addenda(text["V2"])
aws=make_windows("V2",ad)
ctx2=seed_context(text["V1"])
surname2=surname_from_context(ctx2)
seed_ctx_terms=normalize_terms(toks(ctx2))
active2=sorted(domain_vocab & seed_ctx_terms)
a2=normalize_terms(active2)
seq_named=[]
seq_domain=[]
for w in aws:
    norm=normalize_terms(w.words)
    if surname2 in norm:
        seq_named.append(w)
        if norm & a2:
            seq_domain.append(w)

for name,cands in (
    ("E1W_SEQUENCE_SOURCE",seq_named),
    ("E1W_SEQUENCE_DOMAIN",seq_domain),
):
    ordn=next((i for i,w in enumerate(cands,1) if strict_target(w)),None)
    print(f"RESULT,{name},candidates={len(cands)},strict_target_in_set={int(ordn is not None)},strict_target_ordinal={ordn if ordn else 'NA'}")
    if ordn is not None:
        w=cands[ordn-1]
        print("STRICT_TARGET_WINDOW,"+name+f",ordinal={ordn},start={w.start},"+" ".join(w.words[:40]))
