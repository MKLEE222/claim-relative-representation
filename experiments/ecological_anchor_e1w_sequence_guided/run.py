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
    start:int
    words:list[str]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0 research reproducibility"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def sha(b): return hashlib.sha256(b).hexdigest()

def toks(text):
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}",text.lower())

def make_windows(text):
    ts=toks(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2:
            out.append(W(s,ch))
    return out

def normalize_terms(words):
    out=set()
    for w in words:
        out.add(w)
        if "-" in w:
            out.update(x for x in w.split("-") if x)
    return out

def locate_seed_context(v1):
    # Anchor on the PM02-specific botanical term first, so we do not
    # accidentally use an earlier Bretschneider mention in the preface.
    low=v1.lower()
    p=low.find("broussonetia")
    if p<0:
        raise RuntimeError("PM02 Broussonetia anchor not found")
    context=v1[max(0,p-1200):p+1800]
    if "bretschneider" not in context.lower():
        raise RuntimeError("PM02 context lacks Bretschneider")
    return context

def extract_surname(context):
    m=re.search(r"\bDr\.?\s+([A-Z][A-Za-z-]+)",context)
    if not m:
        raise RuntimeError("source surname extraction failed")
    return m.group(1).lower()

def find_addenda(v2):
    # Native Gutenberg line wrapping is not semantically meaningful, so match
    # the printed heading across arbitrary whitespace without changing scope.
    m=re.search(
        r"notes\s+and\s+addenda\s+to\s+sir\s+henry\s+yule(?:['’]s)?\s+edition",
        v2,
        flags=re.I,
    )
    if not m:
        raise RuntimeError("native addenda heading not found")
    p=m.start()
    return p,v2[p:]

def find_target_window(ws):
    need1=set(toks("Regarding Bretschneider"))
    need2=set(toks("Laufer"))
    for w in ws:
        s=set(w.words)
        if need1<=s and need2<=s:
            return w
    raise RuntimeError("PM03 evaluation target not found in addenda")

def main():
    raw={k:fetch(v) for k,v in URLS.items()}
    text={k:v.decode("utf-8",errors="replace") for k,v in raw.items()}

    seed_context=locate_seed_context(text["V1"])
    surname=extract_surname(seed_context)
    if surname=="laufer":
        raise RuntimeError("TARGET LEAKAGE")

    seed_tokens=normalize_terms(toks(seed_context))
    domain_vocab={"mulberry","mulberry-trees","bark","broussonetia","papyrifera","bank-notes","money"}
    active=sorted(domain_vocab & seed_tokens)
    if not active:
        raise RuntimeError("PM02-specific seed produced no active domain terms")

    addenda_char,addenda=find_addenda(text["V2"])
    ws=make_windows(addenda)
    target=find_target_window(ws)

    named=[]
    domain=[]
    active_norm=normalize_terms(active)
    for w in ws:
        norm=normalize_terms(w.words)
        if surname in norm:
            named.append(w)
            if norm & active_norm:
                domain.append(w)

    print("ECOLOGICAL_ANCHOR_E1W")
    print("source_sha256_V1="+sha(raw["V1"]))
    print("source_sha256_V2="+sha(raw["V2"]))
    print("addenda_char_offset="+str(addenda_char))
    print("extracted_source_name="+surname)
    print("active_domain_terms="+"|".join(active))
    print("laufer_used_in_query=0")

    for name,cands in (
        ("PI_SEQUENCE_GUIDED_SOURCE_CHAIN",named),
        ("PI_SEQUENCE_GUIDED_DOMAIN_CHAIN",domain),
    ):
        ordn=None
        for i,w in enumerate(cands,1):
            if abs(w.start-target.start)<STRIDE:
                ordn=i
                break
        print(",".join([
            "RESULT",name,
            f"candidates={len(cands)}",
            f"target_in_set={int(ordn is not None)}",
            f"target_ordinal={ordn if ordn is not None else 'NA'}"
        ]))
        for i,w in enumerate(cands[:10],1):
            print(f"CAND,{name},{i},{w.start},"+" ".join(w.words[:20]))

if __name__=="__main__":
    main()
