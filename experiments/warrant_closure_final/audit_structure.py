from __future__ import annotations

import collections
import hashlib
import math
import re
import time
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

@dataclass(frozen=True)
class W:
    coord:str
    doc:str
    start:int
    words:tuple[str,...]

def fetch(url):
    last=None
    for attempt in range(5):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0"})
            with urllib.request.urlopen(req,timeout=45) as r:
                return r.read()
        except Exception as e:
            last=e
            if attempt<4:
                time.sleep(2**attempt)
    raise RuntimeError(f"BLOCKED_TRANSPORT: {url}: {last}")

def toks(s):
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}",s.lower())

def make_windows(coord,doc,text):
    ts=toks(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=tuple(ts[s:s+WINDOW])
        if len(ch)>=WINDOW//2:
            out.append(W(coord,doc,s,ch))
    return out

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

def is_pm03(w):
    s=set(w.words)
    return {"regarding","bretschneider"}<=s and {"laufer"}<=s

def idf(ws):
    n=len(ws); df=collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def query(seed,w1):
    iw=idf(w1)
    tf=collections.Counter(t for t in seed.words if t not in STOP and len(t)>=4)
    return sorted(((t,c*iw.get(t,1.0)) for t,c in tf.items()),key=lambda x:(-x[1],x[0]))[:QUERY_K]

def score(w,q):
    c=collections.Counter(w.words)
    return sum(weight*min(c.get(t,0),3) for t,weight in q)

def seed_context(v1):
    low=v1.lower()
    p=low.find("broussonetia")
    if p<0: raise RuntimeError("Broussonetia missing")
    ctx=v1[max(0,p-1200):p+1800]
    if "bretschneider" not in ctx.lower():
        raise RuntimeError("Bretschneider missing")
    return ctx

def surname(ctx):
    m=re.search(r"\bDr\.?\s+([A-Z][A-Za-z-]+)",ctx)
    if not m: raise RuntimeError("surname missing")
    return m.group(1).lower()

def addenda(v2):
    m=re.search(r"notes\s+and\s+addenda\s+to\s+sir\s+henry\s+yule(?:['’]s)?\s+edition",v2,flags=re.I)
    if not m: raise RuntimeError("addenda missing")
    return m.start(),v2[m.start():]

def overlap(a,b):
    if a.coord!=b.coord:
        return False
    a0,a1=a.start,a.start+len(a.words)
    b0,b1=b.start,b.start+len(b.words)
    inter=max(0,min(a1,b1)-max(a0,b0))
    denom=min(a1-a0,b1-b0)
    return denom>0 and inter/denom>=0.5

def components(ws):
    n=len(ws)
    seen=set()
    comps=[]
    for i in range(n):
        if i in seen: continue
        stack=[i]; seen.add(i); c=[]
        while stack:
            j=stack.pop(); c.append(j)
            for k in range(n):
                if k not in seen and overlap(ws[j],ws[k]):
                    seen.add(k); stack.append(k)
        comps.append(sorted(c))
    return comps

raw={k:fetch(v) for k,v in URLS.items()}
for k,b in raw.items():
    got=hashlib.sha256(b).hexdigest()
    if got!=EXPECTED[k]:
        raise RuntimeError(f"{k} hash drift: {got}")
text={k:b.decode("utf-8",errors="replace") for k,b in raw.items()}

w1=make_windows("FULL_V1","V1",text["V1"])
w2=make_windows("FULL_V2","V2",text["V2"])
seed=find_seed(w1)

# Frozen generic top-12.
q=query(seed,w1)
ranked=[]
for w in w1+w2:
    if w.doc==seed.doc and abs(w.start-seed.start)<WINDOW:
        continue
    ranked.append((score(w,q),w))
ranked.sort(key=lambda x:(-x[0],x[1].doc,x[1].start))
generic=[w for _,w in ranked[:12]]

# Frozen sequence-guided policies.
ctx=seed_context(text["V1"])
sn=surname(ctx)
domain_vocab={"mulberry","mulberry-trees","bark","broussonetia","papyrifera","bank-notes","money"}
active=normalize_terms(domain_vocab & normalize_terms(toks(ctx)))
_,ad=addenda(text["V2"])
aws=make_windows("ADDENDA_V2","V2",ad)
source_chain=[]
domain_chain=[]
for w in aws:
    norm=normalize_terms(w.words)
    if sn in norm:
        source_chain.append(w)
        if norm & active:
            domain_chain.append(w)

if len(domain_chain)!=12:
    raise RuntimeError(f"domain-chain drift: {len(domain_chain)}")

gc=components(generic)
dc=components(domain_chain)
sc=components(source_chain)

def describe(label,ws,cs):
    print(f"{label}_RAW={len(ws)}")
    print(f"{label}_UNIQUE={len(cs)}")
    for ui,c in enumerate(cs,1):
        starts=[ws[i].start for i in c]
        flags=[int(is_pm03(ws[i])) for i in c]
        print(f"UNIT,{label},{ui},members={'|'.join(map(str,c))},starts={'|'.join(map(str,starts))},pm03={int(any(flags))}")

describe("GENERIC",generic,gc)
describe("GUIDED_DOMAIN",domain_chain,dc)
describe("GUIDED_SOURCE",source_chain,sc)

B=min(len(gc),len(dc))
print("B_FINAL="+str(B))

pm03_units=[ui for ui,c in enumerate(dc) if any(is_pm03(domain_chain[i]) for i in c)]
print("GUIDED_PM03_UNITS="+"|".join(str(x+1) for x in pm03_units))
if len(pm03_units)!=1:
    raise RuntimeError(f"expected exactly one deduplicated PM03 unit, got {pm03_units}")
pm03_idx=pm03_units[0]

# Donor search among deduped source-chain units in source order.
guided_selected=dc[:B]
selected_windows={i for c in guided_selected for i in c}
pm03_members=set(dc[pm03_idx])

def source_unit_windows(c):
    return [source_chain[i] for i in c]

donor=None
for sui,c in enumerate(sc):
    ws=source_unit_windows(c)
    if any(is_pm03(w) for w in ws):
        continue
    # reject if this source unit overlaps any raw domain window represented in the selected guided base
    bad=False
    for w in ws:
        for di in selected_windows:
            if overlap(w,domain_chain[di]):
                bad=True; break
        if bad: break
    if not bad:
        donor=sui
        break

print("GUIDED_REMOVE_DONOR_UNIT="+(str(donor+1) if donor is not None else "NONE"))
if donor is None:
    print("GUIDED_REMOVE_STATUS=BLOCKED_CONSTRUCTION")
else:
    print("GUIDED_REMOVE_STATUS=CONSTRUCTIBLE")

# Sham donor uses the same first eligible source-chain unit.
print("GENERIC_SHAM_DONOR_UNIT="+(str(donor+1) if donor is not None else "NONE"))
