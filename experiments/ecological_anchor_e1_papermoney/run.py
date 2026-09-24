from __future__ import annotations

import hashlib
import math
import re
import urllib.request
from collections import Counter
from dataclasses import dataclass

URLS = {
    "V1": "https://www.gutenberg.org/cache/epub/10636/pg10636.txt",
    "V2": "https://www.gutenberg.org/cache/epub/12410/pg12410.txt",
}

STOP = {
    "the","and","that","this","with","from","have","has","had","were","was","are","for","not",
    "but","his","her","their","there","which","into","than","then","they","them","you","your",
    "its","who","whom","what","when","where","how","all","any","some","more","most","such",
    "only","seems","made","make","makes","been","being","will","would","could","should","about",
    "over","under","after","before","between","also","very","upon","our","out","off","one","two",
    "marco","polo","china","paper"
}

SEED_ANCHORS = ("Dr. Bretschneider", "Broussonetia")
TARGET_ANCHORS = ("Regarding Bretschneider", "Laufer")

WINDOW = 180
STRIDE = 90
QUERY_K = 12

@dataclass
class Window:
    doc: str
    start: int
    words: list[str]
    raw: str

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent":"claim-relative-representation/1.0 research reproducibility"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text.lower())

def windows(doc: str, text: str) -> list[Window]:
    toks = tokenize(text)
    out=[]
    for s in range(0, max(1, len(toks)-WINDOW+1), STRIDE):
        chunk=toks[s:s+WINDOW]
        if len(chunk) < WINDOW//2:
            continue
        out.append(Window(doc=doc,start=s,words=chunk,raw=" ".join(chunk)))
    return out

def find_window(ws: list[Window], anchors: tuple[str,...]) -> Window:
    anchor_tokens=[set(tokenize(a)) for a in anchors]
    for w in ws:
        s=set(w.words)
        if all(t <= s for t in anchor_tokens):
            return w
    raise RuntimeError(f"window not found for anchors={anchors}")

def idf_v1(ws: list[Window]) -> dict[str,float]:
    n=len(ws)
    df=Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t: math.log((n+1)/(c+1))+1.0 for t,c in df.items()}

def query_terms(seed: Window, idf: dict[str,float]) -> list[tuple[str,float]]:
    tf=Counter(t for t in seed.words if t not in STOP and len(t)>=4)
    scored=[]
    for t,c in tf.items():
        scored.append((t, c*idf.get(t,1.0)))
    scored.sort(key=lambda x:(-x[1],x[0]))
    q=scored[:QUERY_K]
    if any(t=="laufer" for t,_ in q):
        raise RuntimeError("TARGET LEAKAGE: laufer entered query terms")
    return q

def score(w: Window, q: list[tuple[str,float]]) -> float:
    c=Counter(w.words)
    return sum(weight * min(c.get(term,0),3) for term,weight in q)

def rank(scope: list[Window], seed: Window, target: Window|None, q):
    candidates=[]
    for w in scope:
        if w.doc==seed.doc and abs(w.start-seed.start) < WINDOW:
            continue
        candidates.append((score(w,q),w))
    candidates.sort(key=lambda x:(-x[0],x[1].doc,x[1].start))
    if target is None:
        return candidates,None
    for i,(_,w) in enumerate(candidates,1):
        if w.doc==target.doc and abs(w.start-target.start) < STRIDE:
            return candidates,i
    return candidates,None

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main():
    raw={k:fetch(u) for k,u in URLS.items()}
    txt={k:v.decode("utf-8",errors="replace") for k,v in raw.items()}

    w1=windows("V1",txt["V1"])
    w2=windows("V2",txt["V2"])

    seed=find_window(w1,SEED_ANCHORS)
    target=find_window(w2,TARGET_ANCHORS)

    idf=idf_v1(w1)
    q=query_terms(seed,idf)

    print("ECOLOGICAL_ANCHOR_E1")
    print("source_sha256_V1="+sha(raw["V1"]))
    print("source_sha256_V2="+sha(raw["V2"]))
    print("seed_start="+str(seed.start))
    print("target_start="+str(target.start))
    print("query_terms="+"|".join(t for t,_ in q))

    conditions = {
        "W_CURRENT_OBJECT": w1,
        "W_DECLARED_COLLECTION": w1+w2,
    }

    for name,scope in conditions.items():
        target_in_scope = any(w.doc==target.doc for w in scope)
        candidates,r = rank(scope,seed,target if target_in_scope else None,q)
        rr = 0.0 if r is None else 1.0/r
        hits = {k:int(r is not None and r<=k) for k in (1,5,10,20)}
        print(",".join([
            "RESULT",name,
            f"target_in_scope={int(target_in_scope)}",
            f"candidates={len(candidates)}",
            f"rank={r if r is not None else 'NA'}",
            f"MRR={rr:.6f}",
            f"H1={hits[1]}",
            f"H5={hits[5]}",
            f"H10={hits[10]}",
            f"H20={hits[20]}",
        ]))

        for j,(s,w) in enumerate(candidates[:5],1):
            print(f"TOP,{name},{j},{w.doc},{w.start},{s:.6f},"+" ".join(w.words[:18]))

if __name__=="__main__":
    main()
