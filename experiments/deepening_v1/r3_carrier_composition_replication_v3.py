from __future__ import annotations

import collections
import hashlib
import json
import math
import re
import time
import urllib.request
from pathlib import Path

URL_V1="https://www.gutenberg.org/cache/epub/10636/pg10636.txt"
URL_V2="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
SHA_V1="7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5"
SHA_V2="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"

STOP={
"a","an","and","are","as","at","be","been","being","but","by","for","from","had","has","have","he","her","his",
"i","if","in","into","is","it","its","may","more","most","not","of","on","or","our","she","so","that","the","their",
"them","there","these","they","this","to","was","we","were","which","who","with","would","you"
}

CASES={
"C05":{
    "target":"YC1920E-0082",
    "target_sha256":"84dd8de5207389ddfecdefdc22083b3f6300f700c84ba9d5f4e7e24d781c2f49",
    "chapter":"LVIII",
    "page":283,
    "anchor":"Among the names of these were Sling, Shirum, Gurun, and Khoza",
},
"C06":{
    "target":"YC1920E-0083",
    "target_sha256":"afc27e9a3ee1b998adfad87c449649e362bddfcf869aa1b3fd92517b3ea00ef4",
    "chapter":"LVIII",
    "page":283,
    "anchor":"Cunningham also mentions camlets of camel's hair, under the name of Suklat",
},
}

def fetch(url):
    last=None
    for attempt in range(5):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0"})
            with urllib.request.urlopen(req,timeout=60) as r:
                return r.read()
        except Exception as e:
            last=e
            if attempt<4:
                time.sleep(2**attempt)
    raise RuntimeError(last)

def ws(x):
    return " ".join((x or "").split())

def build_entries(text):
    sm=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
    if not sm:
        raise RuntimeError("addenda start missing")
    start=sm.start()
    stops=[]
    for pat in [r"\nBIBLIOGRAPHY\b",r"\nSUPPLEMENTARY NOTE\b",r"\nINDEX\b"]:
        m=re.search(pat,text[start:],re.I)
        if m:
            stops.append(start+m.start())
    stop=min(stops) if stops else len(text)
    region=text[start:stop]
    head_re=re.compile(
        r"(?m)^(?P<head>(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?"
        r"[IVXLCDM]+(?:\.|,)[^\n]{0,120}?\bp{1,2}\.\s*[^\n]{0,80})$"
    )
    heads=list(head_re.finditer(region))
    months=r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    def excluded(head):
        if re.search(rf"^[IVXLCDM]+\.,\s*(?:{months}|(?:18|19)\d{{2}})\b",head,re.I):
            return True
        if re.search(r"^[A-Z]\.\s*Chap\.",head,re.I):
            return True
        if re.search(r"\bp{1,2}\.\s*[^,]{0,40}\),",head,re.I):
            return True
        if re.search(r"^[IVXLCDM]+\.,\s*pp?\.\s*[^\n]{0,90}\bin\s+(?:(?:Mr\.|Dr\.|Prof\.)\s+[A-Z][A-Za-z'’.-]+|Sir\s+[A-Z][A-Za-z'’.-]+|[A-Z][A-Za-z'’.-]+['’]s)\s+paper\b",head,re.I):
            return True
        return False
    raw=[]
    for i,m in enumerate(heads):
        s=m.start()
        e=heads[i+1].start() if i+1<len(heads) else len(region)
        raw.append({"head":m.group("head").strip(),"block":region[s:e].strip()})
    entries=[]
    for r in raw:
        if excluded(r["head"]):
            if entries:
                entries[-1]["block"] += "\n"+r["block"]
            continue
        entries.append({
            "entry_id":f"YC1920E-{len(entries)+1:04d}",
            "head":r["head"],
            "block":r["block"],
        })
    for e in entries:
        e["entry_text"]=ws(e["block"])
        e["entry_sha256"]=hashlib.sha256(e["entry_text"].encode("utf-8")).hexdigest()
    return entries

def tokenize(text):
    toks=re.findall(r"[^\W\d_]{3,}",text.casefold(),flags=re.UNICODE)
    return [t for t in toks if t not in STOP]

def scorer(query, docs):
    q=tokenize(query)
    ds=[tokenize(x) for x in docs]
    N=len(ds)+1
    df=collections.Counter()
    for ts in ds+[q]:
        for t in set(ts):
            df[t]+=1
    def vec(ts):
        cnt=collections.Counter(ts)
        total=sum(cnt.values()) or 1
        return {t:(n/total)*(math.log((N+1)/(df[t]+1))+1.0) for t,n in cnt.items()}
    qv=vec(q)
    qn=math.sqrt(sum(v*v for v in qv.values())) or 1.0
    out=[]
    for i,ts in enumerate(ds):
        dv=vec(ts)
        dn=math.sqrt(sum(v*v for v in dv.values())) or 1.0
        dot=sum(qv.get(t,0.0)*v for t,v in dv.items())
        out.append((dot/(qn*dn),i))
    out.sort(key=lambda z:(-z[0],z[1]))
    return out

def chapter(head):
    m=re.match(r"^(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?([IVXLCDM]+)",head)
    return m.group(1) if m else ""

def pages(head):
    nums=[]
    for m in re.finditer(r"\bp{1,2}\.\s*([^A-Za-z\n]{0,50})",head,re.I):
        nums.extend(int(x) for x in re.findall(r"\d+",m.group(1)))
    return nums

def seed_window(text,anchor):
    words=re.findall(r"[^\W\d_]+",anchor,flags=re.UNICODE)
    pat=r"\W+".join(re.escape(w) for w in words)
    m=re.search(pat,text,re.I|re.UNICODE)
    if not m:
        raise RuntimeError(f"1903 anchor not found: {anchor}")
    return text[max(0,m.start()-900):min(len(text),m.end()+900)]

raw1=fetch(URL_V1)
raw2=fetch(URL_V2)
if hashlib.sha256(raw1).hexdigest()!=SHA_V1:
    raise RuntimeError("vol1 source drift")
if hashlib.sha256(raw2).hexdigest()!=SHA_V2:
    raise RuntimeError("vol2 source drift")

v1=raw1.decode("utf-8",errors="replace")
v2=raw2.decode("utf-8",errors="replace")
entries=build_entries(v2)
if len(entries)!=223:
    raise RuntimeError(f"refined frame drift: {len(entries)}")
by_id={e["entry_id"]:e for e in entries}
body_docs=[
    e["entry_text"][len(e["head"]):].strip() if e["entry_text"].startswith(e["head"]) else e["entry_text"]
    for e in entries
]

results=[]
for cid,cfg in CASES.items():
    target=by_id[cfg["target"]]
    if target["entry_sha256"]!=cfg["target_sha256"]:
        raise RuntimeError(f"{cid} target hash mismatch")
    seed=seed_window(v1,cfg["anchor"])
    pointer=[
        e for e in entries
        if chapter(e["head"])==cfg["chapter"] and cfg["page"] in pages(e["head"])
    ]
    if len(pointer)<=1:
        raise RuntimeError(f"{cid} pointer group no longer ambiguous")
    if cfg["target"] not in {e["entry_id"] for e in pointer}:
        raise RuntimeError(f"{cid} target not in pointer group")

    global_rank=scorer(seed,body_docs)
    global_order=[entries[i]["entry_id"] for _,i in global_rank]
    global_pos=global_order.index(cfg["target"])+1
    global_score=next(s for s,i in global_rank if entries[i]["entry_id"]==cfg["target"])

    pointer_docs=[
        e["entry_text"][len(e["head"]):].strip() if e["entry_text"].startswith(e["head"]) else e["entry_text"]
        for e in pointer
    ]
    composed=scorer(seed,pointer_docs)
    comp_order=[pointer[i]["entry_id"] for _,i in composed]
    comp_pos=comp_order.index(cfg["target"])+1

    results.append({
        "case_id":cid,
        "target":cfg["target"],
        "entry_state":"HISTORICAL_START",
        "pointer_only":{
            "candidate_count":len(pointer),
            "candidates":[e["entry_id"] for e in pointer],
            "target_unique":False,
        },
        "lexical_global":{
            "rank":global_pos,
            "score":global_score,
            "hit20":global_pos<=20,
        },
        "pointer_then_lexical":{
            "rank_within_pointer_set":comp_pos,
            "order":comp_order,
            "target_rank1":comp_pos==1,
        },
        "composition_support":len(pointer)>1 and comp_pos==1,\n        "category":("STRONG_COMPLEMENTARITY" if len(pointer)>1 and global_pos>1 and comp_pos==1 else ("REDUNDANT_WITH_COMPOSITION" if len(pointer)>1 and global_pos==1 and comp_pos==1 else "COMPOSITION_FAILURE")),
    })

out={
    "study":"R3_CARRIER_COMPOSITION_REPLICATION_V3",
    "authority":"prospective third source-order duplicate-pointer replication",
    "source":{"vol1_sha256":SHA_V1,"vol2_sha256":SHA_V2,"refined_entries":len(entries)},
    "results":results,
    "limits":[
        "The two cases share one chapter/page group and are not independent infrastructures.",
        "TF-IDF is an operational discriminator, not a model of human reading.",
        "A positive result supports complementarity in this group only.",
        "Historical relation interpretation remains separate from retrieval-route performance."
    ],
}
Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r3_carrier_composition_replication_v3.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_CARRIER_COMPOSITION_REPLICATION_V3")
for r in results:
    print(f"CASE,{r['case_id']},{r['target']},pointer_n={r['pointer_only']['candidate_count']},global_rank={r['lexical_global']['rank']},composed_rank={r['pointer_then_lexical']['rank_within_pointer_set']},composition_support={int(r['composition_support'])}")
