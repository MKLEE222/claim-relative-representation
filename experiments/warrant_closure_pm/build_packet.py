from __future__ import annotations

import hashlib
import json
import math
import re
import urllib.request
from collections import Counter
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
K=12

STOP={
    "the","and","that","this","with","from","have","has","had","were","was","are","for","not",
    "but","his","her","their","there","which","into","than","then","they","them","you","your",
    "its","who","whom","what","when","where","how","all","any","some","more","most","such",
    "only","seems","made","make","makes","been","being","will","would","could","should","about",
    "over","under","after","before","between","also","very","upon","our","out","off","one","two",
    "marco","polo","china","paper"
}

@dataclass
class W:
    doc:str
    start:int
    words:list[str]
    char_start:int
    char_end:int

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def token_spans(text):
    ms=list(re.finditer(r"[A-Za-z][A-Za-z'-]{2,}",text))
    words=[m.group(0).lower() for m in ms]
    return words,ms

def make_windows(doc,text):
    words,ms=token_spans(text)
    out=[]
    for s in range(0,max(1,len(words)-WINDOW+1),STRIDE):
        chunk=words[s:s+WINDOW]
        if len(chunk)<WINDOW//2:
            continue
        cs=ms[s].start()
        ce=ms[min(s+WINDOW-1,len(ms)-1)].end()
        out.append(W(doc,s,chunk,cs,ce))
    return out

def normalize_terms(words):
    out=set()
    for w in words:
        out.add(w)
        if "-" in w:
            out.update(x for x in w.split("-") if x)
    return out

def find_seed(ws):
    need1={"dr","bretschneider"}
    need2={"broussonetia"}
    for w in ws:
        s=set(w.words)
        if need1<=s and need2<=s:
            return w
    raise RuntimeError("seed not found")

def find_target(ws):
    need1={"regarding","bretschneider"}
    need2={"laufer"}
    for w in ws:
        s=set(w.words)
        if need1<=s and need2<=s:
            return w
    raise RuntimeError("target not found")

def idf(ws):
    n=len(ws); df=Counter()
    for w in ws:
        for t in set(w.words): df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def generic_query(seed,w1):
    iw=idf(w1)
    tf=Counter(t for t in seed.words if t not in STOP and len(t)>=4)
    q=sorted(((t,c*iw.get(t,1.0)) for t,c in tf.items()),key=lambda z:(-z[1],z[0]))[:K]
    assert all(t!="laufer" for t,w in q)
    return q

def score(w,q):
    c=Counter(w.words)
    return sum(weight*min(c.get(t,0),3) for t,weight in q)

def locate_pm02_context(v1):
    low=v1.lower()
    p=low.find("broussonetia")
    if p<0: raise RuntimeError("Broussonetia missing")
    context=v1[max(0,p-1200):p+1800]
    if "bretschneider" not in context.lower(): raise RuntimeError("Bretschneider missing")
    return context

def find_addenda(v2):
    m=re.search(r"notes\s+and\s+addenda\s+to\s+sir\s+henry\s+yule(?:['’]s)?\s+edition",v2,flags=re.I)
    if not m: raise RuntimeError("addenda missing")
    return m.start(),v2[m.start():]

def clean_excerpt(s):
    return " ".join(s.split())

raw={k:fetch(u) for k,u in URLS.items()}
for k,b in raw.items():
    assert hashlib.sha256(b).hexdigest()==EXPECTED[k]
text={k:b.decode("utf-8",errors="replace") for k,b in raw.items()}

w1=make_windows("V1",text["V1"])
w2=make_windows("V2",text["V2"])
seed=find_seed(w1)
target=find_target(w2)

# Generic declared-collection top 12.
q=generic_query(seed,w1)
generic=[]
for w in w1+w2:
    if w.doc==seed.doc and abs(w.start-seed.start)<WINDOW:
        continue
    generic.append((score(w,q),w))
generic.sort(key=lambda z:(-z[0],z[1].doc,z[1].start))
generic=[w for s,w in generic[:12]]

# Sequence-guided domain chain, exactly as frozen E1W logic.
ctx=locate_pm02_context(text["V1"])
m=re.search(r"\bDr\.?\s+([A-Z][A-Za-z-]+)",ctx)
surname=m.group(1).lower()
seed_tokens=normalize_terms(re.findall(r"[A-Za-z][A-Za-z'-]{2,}",ctx.lower()))
domain_vocab={"mulberry","mulberry-trees","bark","broussonetia","papyrifera","bank-notes","money"}
active=sorted(domain_vocab & seed_tokens)
addenda_char,addenda=find_addenda(text["V2"])
aws=make_windows("V2",addenda)
guided=[]
for w in aws:
    norm=normalize_terms(w.words)
    if surname in norm and norm & normalize_terms(active):
        guided.append(w)

assert len(guided)==12
assert not any(abs(w.start-target.start)<STRIDE for w in generic)
assert any(abs(w.start-target.start)<STRIDE for w in guided)

# Fixed exact source context from page-verified alignment.
fixed={
    "claim":"Polo's identification of mulberry bark as material used for paper-money is usable as evidence for Yuan paper-money practice under the supplied editorial record.",
    "PM01":"HOW THE GREAT KAAN CAUSETH THE BARK OF TREES, MADE INTO SOMETHING LIKE PAPER, TO PASS FOR MONEY OVER ALL HIS COUNTRY ... he hath his money coined and struck",
    "PM02":"Dr. Bretschneider ... makes the following remark ... He seems to be mistaken. Paper in China is not made from mulberry-trees but from the Broussonetia papyrifera ... —H. C.",
}

def packet(label,windows,source_texts):
    rows=[]
    for i,w in enumerate(windows,1):
        src=source_texts[w.doc]
        excerpt=clean_excerpt(src[w.char_start:w.char_end])
        rows.append({"candidate":f"{label}-{i:02d}","witness":w.doc,"excerpt":excerpt})
    return rows

# Masked labels. Mapping is frozen separately.
packet_a=packet("A",guided,{"V1":text["V1"],"V2":addenda})
packet_b=packet("B",generic,text)

print("PM_WARRANT_PACKET_BUILD")
print("PACKET_A_CANDIDATES="+str(len(packet_a)))
print("PACKET_B_CANDIDATES="+str(len(packet_b)))
print("PACKET_A_TARGET_PRESENT=1")
print("PACKET_B_TARGET_PRESENT=0")
print("CODER_POLICY_IDENTITY_EXPOSED=0")
print("PACKET_JSON="+json.dumps({"fixed":fixed,"PACKET_A":packet_a,"PACKET_B":packet_b},ensure_ascii=False))
