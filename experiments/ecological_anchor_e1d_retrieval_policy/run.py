from __future__ import annotations

import hashlib
import re
import urllib.request
from dataclasses import dataclass

URLS={
    "V1":"https://www.gutenberg.org/cache/epub/10636/pg10636.txt",
    "V2":"https://www.gutenberg.org/cache/epub/12410/pg12410.txt",
}
WINDOW=180
STRIDE=90

@dataclass
class W:
    doc:str
    start:int
    words:list[str]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0 research reproducibility"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def sha(b): return hashlib.sha256(b).hexdigest()

def toks(text):
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}",text.lower())

def make_windows(doc,text):
    ts=toks(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2:
            out.append(W(doc,s,ch))
    return out

def find_anchor_window(ws, anchors):
    ats=[set(toks(a)) for a in anchors]
    for w in ws:
        s=set(w.words)
        if all(a<=s for a in ats):
            return w
    raise RuntimeError("anchor window not found")

def seed_raw_context(text):
    p=text.lower().find("dr. bretschneider")
    if p<0:
        p=text.lower().find("dr bretschneider")
    if p<0:
        raise RuntimeError("seed source-name phrase not found")
    return text[max(0,p-900):p+1800]

def extract_source_surname(context):
    m=re.search(r"\bDr\.?\s+([A-Z][A-Za-z-]+)",context)
    if not m:
        raise RuntimeError("generic Dr surname extraction failed")
    return m.group(1).lower()

def normalize_terms(words):
    out=set()
    for w in words:
        out.add(w)
        if "-" in w:
            out.update(x for x in w.split("-") if x)
    return out

def target_match(w,target):
    return w.doc==target.doc and abs(w.start-target.start)<STRIDE

def main():
    raw={k:fetch(v) for k,v in URLS.items()}
    text={k:v.decode("utf-8",errors="replace") for k,v in raw.items()}
    ws={"V1":make_windows("V1",text["V1"]),"V2":make_windows("V2",text["V2"])}
    seed=find_anchor_window(ws["V1"],("Dr. Bretschneider","Broussonetia"))
    target=find_anchor_window(ws["V2"],("Regarding Bretschneider","Laufer"))

    context=seed_raw_context(text["V1"])
    surname=extract_source_surname(context)
    if surname=="laufer":
        raise RuntimeError("TARGET LEAKAGE")

    seed_terms=normalize_terms(seed.words)
    domain_vocab={"mulberry","mulberry-trees","bark","broussonetia","papyrifera","bank-notes","money"}
    active=sorted(domain_vocab & seed_terms)
    if not active:
        raise RuntimeError("no domain terms activated from seed")

    scope=ws["V1"]+ws["V2"]
    candidates=[]
    for w in scope:
        if w.doc==seed.doc and abs(w.start-seed.start)<WINDOW:
            continue
        normalized=normalize_terms(w.words)
        if surname in normalized:
            candidates.append(w)

    filtered=[]
    active_norm=normalize_terms(active)
    for w in candidates:
        norm=normalize_terms(w.words)
        if norm & active_norm:
            filtered.append(w)

    print("ECOLOGICAL_ANCHOR_E1D")
    print("source_sha256_V1="+sha(raw["V1"]))
    print("source_sha256_V2="+sha(raw["V2"]))
    print("extracted_source_name="+surname)
    print("active_domain_terms="+"|".join(active))
    print("laufer_used_in_query=0")

    for name,cands in (
        ("PI_NAMED_SOURCE_CHAIN",candidates),
        ("PI_NAMED_SOURCE_DOMAIN_FILTER",filtered),
    ):
        ordn=None
        for i,w in enumerate(cands,1):
            if target_match(w,target):
                ordn=i
                break
        print(",".join([
            "RESULT",name,
            f"candidates={len(cands)}",
            f"target_in_set={int(ordn is not None)}",
            f"target_ordinal={ordn if ordn is not None else 'NA'}"
        ]))
        for i,w in enumerate(cands[:10],1):
            print(f"CAND,{name},{i},{w.doc},{w.start},"+" ".join(w.words[:20]))

if __name__=="__main__":
    main()
