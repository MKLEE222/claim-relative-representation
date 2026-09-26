from __future__ import annotations

import collections
import hashlib
import json
import math
import re
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

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
B_FINAL=6
STOP={
    "the","and","that","this","with","from","have","has","had","were","was","are","for","not",
    "but","his","her","their","there","which","into","than","then","they","them","you","your",
    "its","who","whom","what","when","where","how","all","any","some","more","most","such",
    "only","seems","made","make","makes","been","being","will","would","could","should","about",
    "over","under","after","before","between","also","very","upon","our","out","off","one","two",
    "marco","polo","china","paper"
}

ATOMIC_CLAIM="Under the supplied editorial record, Polo's specific identification of mulberry bark as material used for Yuan paper-money is admissible as evidence for the material composition of that paper-money."

@dataclass(frozen=True)
class W:
    coord:str
    doc:str
    start:int
    words:tuple[str,...]
    char_start:int
    char_end:int

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

def token_spans(text):
    ms=list(re.finditer(r"[A-Za-z][A-Za-z'-]{2,}",text))
    return [m.group(0).lower() for m in ms],ms

def make_windows(coord,doc,text,base_char=0):
    words,ms=token_spans(text)
    out=[]
    for s in range(0,max(1,len(words)-WINDOW+1),STRIDE):
        ch=tuple(words[s:s+WINDOW])
        if len(ch)<WINDOW//2:
            continue
        cs=base_char+ms[s].start()
        ce=base_char+ms[min(s+WINDOW-1,len(ms)-1)].end()
        out.append(W(coord,doc,s,ch,cs,ce))
    return out

def normalize_terms(words):
    out=set()
    for w in words:
        out.add(w)
        if "-" in w:
            out.update(x for x in w.split("-") if x)
    return out

def contains(w,*phrases):
    s=set(w.words)
    return all(set(re.findall(r"[A-Za-z][A-Za-z'-]{2,}",p.lower()))<=s for p in phrases)

def find_window(ws,*phrases):
    for w in ws:
        if contains(w,*phrases):
            return w
    raise RuntimeError(f"window not found: {phrases}")

def is_pm03(w):
    return contains(w,"Regarding Bretschneider","Laufer")

def idf(ws):
    n=len(ws); df=collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def query(seed,w1):
    iw=idf(w1)
    tf=collections.Counter(t for t in seed.words if t not in STOP and len(t)>=4)
    q=sorted(((t,c*iw.get(t,1.0)) for t,c in tf.items()),key=lambda x:(-x[1],x[0]))[:QUERY_K]
    if any(t=="laufer" for t,_ in q):
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
    if "bretschneider" not in ctx.lower(): raise RuntimeError("Bretschneider missing")
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
    n=len(ws); seen=set(); comps=[]
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

def unit_from_component(label,ws,c,source_text,ordinal):
    members=[ws[i] for i in c]
    doc=members[0].doc
    if any(w.doc!=doc for w in members):
        raise RuntimeError("unit crosses documents")
    cs=min(w.char_start for w in members)
    ce=max(w.char_end for w in members)
    excerpt=" ".join(source_text[doc][cs:ce].split())
    return {
        "unit_id":f"{label}-{ordinal:02d}",
        "witness":doc,
        "coord":members[0].coord,
        "member_token_starts":[w.start for w in members],
        "char_start":cs,
        "char_end":ce,
        "excerpt_sha256":hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
        "excerpt":excerpt,
        "contains_pm03":any(is_pm03(w) for w in members),
    }

def exact_context(label,w,source_text,page_anchor):
    excerpt=" ".join(source_text[w.doc][w.char_start:w.char_end].split())
    return {
        "context_id":label,
        "witness":w.doc,
        "page_anchor":page_anchor,
        "char_start":w.char_start,
        "char_end":w.char_end,
        "excerpt_sha256":hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
        "excerpt":excerpt,
    }

raw={k:fetch(v) for k,v in URLS.items()}
for k,b in raw.items():
    got=hashlib.sha256(b).hexdigest()
    if got!=EXPECTED[k]:
        raise RuntimeError(f"{k} hash drift: {got}")
text={k:b.decode("utf-8",errors="replace") for k,b in raw.items()}

w1=make_windows("FULL_V1","V1",text["V1"])
w2=make_windows("FULL_V2","V2",text["V2"])
seed=find_window(w1,"Bretschneider","Broussonetia")
pm01w=find_window(w1,"bark of trees","money coined and struck")
pm02w=seed

q=query(seed,w1)
ranked=[]
for w in w1+w2:
    if w.doc==seed.doc and abs(w.start-seed.start)<WINDOW:
        continue
    ranked.append((score(w,q),w))
ranked.sort(key=lambda x:(-x[0],x[1].doc,x[1].start))
generic_raw=[w for _,w in ranked[:12]]

ctx=seed_context(text["V1"])
sn=surname(ctx)
domain_vocab={"mulberry","mulberry-trees","bark","broussonetia","papyrifera","bank-notes","money"}
active=normalize_terms(domain_vocab & normalize_terms(re.findall(r"[A-Za-z][A-Za-z'-]{2,}",ctx.lower())))
addenda_char,ad=addenda(text["V2"])
aws=make_windows("ADDENDA_V2","V2",ad,base_char=addenda_char)
source_chain=[]; domain_chain=[]
for w in aws:
    norm=normalize_terms(w.words)
    if sn in norm:
        source_chain.append(w)
        if norm & active:
            domain_chain.append(w)

if len(domain_chain)!=12:
    raise RuntimeError(f"domain-chain drift: {len(domain_chain)}")

gc=components(generic_raw)
dc=components(domain_chain)
sc=components(source_chain)
if min(len(gc),len(dc))!=B_FINAL:
    raise RuntimeError(f"B_FINAL drift: generic={len(gc)} guided={len(dc)}")

source_text={"V1":text["V1"],"V2":text["V2"]}

generic_units=[unit_from_component("G",generic_raw,c,source_text,i+1) for i,c in enumerate(gc[:B_FINAL])]
guided_units=[unit_from_component("S",domain_chain,c,source_text,i+1) for i,c in enumerate(dc[:B_FINAL])]

pm03_indices=[i for i,u in enumerate(guided_units) if u["contains_pm03"]]
if pm03_indices!=[0]:
    raise RuntimeError(f"PM03 unit drift: {pm03_indices}")
pm03_unit=guided_units[0]

# First source-chain component that is non-PM03 and does not overlap any selected guided raw window.
selected_guided_raw={i for c in dc[:B_FINAL] for i in c}
donor_comp=None
for c in sc:
    members=[source_chain[i] for i in c]
    if any(is_pm03(w) for w in members):
        continue
    if any(overlap(w,domain_chain[di]) for w in members for di in selected_guided_raw):
        continue
    donor_comp=c
    break
if donor_comp is None:
    raise RuntimeError("BLOCKED_CONSTRUCTION: donor missing")
donor=unit_from_component("D",source_chain,donor_comp,source_text,1)

def relabel(units,prefix):
    out=[]
    for i,u in enumerate(units,1):
        x=dict(u)
        x["unit_id"]=f"{prefix}-{i:02d}"
        out.append(x)
    return out

conditions={
    "K4N":relabel(generic_units,"K4N"),
    "R8Q":relabel(guided_units,"R8Q"),
    "M3V":relabel(generic_units[:-1]+[pm03_unit],"M3V"),
    "H7C":relabel(generic_units[:-1]+[donor],"H7C"),
    "T2P":relabel(guided_units[1:]+[donor],"T2P"),
}

for pid,units in conditions.items():
    if len(units)!=B_FINAL:
        raise RuntimeError(f"{pid}: budget drift")
    hashes=[u["excerpt_sha256"] for u in units]
    if len(hashes)!=len(set(hashes)):
        raise RuntimeError(f"{pid}: duplicate exact evidence unit")

fixed={
    "claim_id":"C_PM_ATOMIC",
    "claim":ATOMIC_CLAIM,
    "admissible_warrant_states":["RETAIN","DEFER","WITHHOLD"],
    "PM01":exact_context("PM01",pm01w,source_text,"1903 vol.1 p423 / scan723"),
    "PM02":exact_context("PM02",pm02w,source_text,"1903 vol.1 p430 / scan732"),
    "source_sha256":EXPECTED,
    "unique_unit_budget":B_FINAL,
}

# Perturbations are deterministic and content-preserving.
variants={}
for pid,units in conditions.items():
    variants[pid]={
        "canonical":units,
        "reverse_order":list(reversed(units)),
        "relabel_only":[dict(u,unit_id=f"X{i:02d}") for i,u in enumerate(units,1)],
    }

payload={"fixed":fixed,"packets":variants}
mapping={
    "K4N":"GENERIC_BASE",
    "R8Q":"GUIDED_BASE",
    "M3V":"GENERIC_RESCUE_PM03",
    "H7C":"GENERIC_SHAM",
    "T2P":"GUIDED_REMOVE_PM03",
}

out=Path("experiments/warrant_closure_final/generated")
out.mkdir(parents=True,exist_ok=True)
packet_path=out/"final_packets_v1.json"
mapping_path=out/"sealed_mapping_v1.json"
packet_path.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
mapping_path.write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding="utf-8")

print("FINAL_WARRANT_PACKET_BUILD_V1")
print("B_FINAL="+str(B_FINAL))
for pid,variants_ in variants.items():
    canonical=variants_["canonical"]
    print(f"PACKET,{pid},units={len(canonical)},pm03_units={sum(int(u['contains_pm03']) for u in canonical)},packet_sha256={hashlib.sha256(json.dumps(canonical,ensure_ascii=False,sort_keys=True).encode()).hexdigest()}")
print("PM01_EXACT_SHA256="+fixed["PM01"]["excerpt_sha256"])
print("PM02_EXACT_SHA256="+fixed["PM02"]["excerpt_sha256"])
print("DONOR_SHA256="+donor["excerpt_sha256"])
print("FINAL_LLM_EXECUTED=0")
