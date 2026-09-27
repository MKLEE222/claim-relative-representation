from __future__ import annotations

import collections
import csv
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
SHA_V2="c1ce61dd8c6c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"
# Corrected below at runtime check: keep literal registry value separate to avoid accidental silent drift.
SHA_V2_REGISTRY="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"

STOP={
"a","an","and","are","as","at","be","been","being","but","by","for","from","had","has","have","he","her","his",
"i","if","in","into","is","it","its","may","more","most","not","of","on","or","our","she","so","that","the","their",
"them","there","these","they","this","to","was","we","were","which","who","with","would","you"
}

CASES={
"R3FG-S01":{"entry_id":"YC1920E-0021","chapter":"XIX","page":116,
    "anchor":"Their food when in health consists of dates and salt-fish"},
"R3FG-S02":{"entry_id":"YC1920E-0022","chapter":"XXII","page":128,
    "anchor":"would lead me to suppose that he reached the Province of TUN-O-KAIN about Tabbas"},
"R3FG-S03":{"entry_id":"YC1920E-0022","chapter":"XXII","page":128,
    "anchor":"would lead me to suppose that he reached the Province of TUN-O-KAIN about Tabbas"},
"R3FG-S04":{"entry_id":"YC1920E-0024","chapter":"XXII","page":127,
    "anchor":"There can be no doubt that the tree described is"},
"R3FG-S05":{"entry_id":"YC1920E-0049","chapter":"XXXIX","page":196,
    "anchor":"when he tries to gain his company again he will hear spirits talking"},
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
    def exclusion_reason(head):
        if re.search(rf"^[IVXLCDM]+\.,\s*(?:{months}|(?:18|19)\d{{2}})\b",head,re.I):
            return "F1"
        if re.search(r"^[A-Z]\.\s*Chap\.",head,re.I):
            return "F2"
        if re.search(r"\bp{1,2}\.\s*[^,]{0,40}\),",head,re.I):
            return "F3"
        if re.search(r"^[IVXLCDM]+\.,\s*pp?\.\s*[^\n]{0,90}\bin\s+(?:(?:Mr\.|Dr\.|Prof\.)\s+[A-Z][A-Za-z'’.-]+|Sir\s+[A-Z][A-Za-z'’.-]+|[A-Z][A-Za-z'’.-]+['’]s)\s+paper\b",head,re.I):
            return "F4"
        return ""
    raw=[]
    for i,m in enumerate(heads):
        s=m.start()
        e=heads[i+1].start() if i+1<len(heads) else len(region)
        raw.append({"raw_id":f"YC1920-{i+1:04d}","head":m.group("head").strip(),"block":region[s:e].strip()})
    entries=[]
    for r in raw:
        if exclusion_reason(r["head"]):
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

def tfidf_rank(query, docs):
    q=tokenize(query)
    doc_toks=[tokenize(x) for x in docs]
    N=len(doc_toks)+1
    df=collections.Counter()
    for ts in doc_toks+[q]:
        for t in set(ts):
            df[t]+=1
    def vec(ts):
        cnt=collections.Counter(ts)
        total=sum(cnt.values()) or 1
        return {t:(n/total)*(math.log((N+1)/(df[t]+1))+1.0) for t,n in cnt.items()}
    qv=vec(q)
    qn=math.sqrt(sum(v*v for v in qv.values())) or 1.0
    out=[]
    for i,ts in enumerate(doc_toks):
        dv=vec(ts)
        dn=math.sqrt(sum(v*v for v in dv.values())) or 1.0
        dot=sum(qv.get(t,0.0)*v for t,v in dv.items())
        out.append((dot/(qn*dn),i))
    out.sort(key=lambda z:(-z[0],z[1]))
    return out

def roman_head(head):
    m=re.match(r"^(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?([IVXLCDM]+)",head)
    return m.group(1) if m else ""

def head_pages(head):
    nums=[]
    for m in re.finditer(r"\bp{1,2}\.\s*([^A-Za-z\n]{0,50})",head,re.I):
        nums.extend(int(x) for x in re.findall(r"\d+",m.group(1)))
    return nums

def seed_window(text,anchor):
    words=re.findall(r"[^\\W\\d_]+",anchor,flags=re.UNICODE)
    pat=r"\\W+".join(re.escape(w) for w in words)
    m=re.search(pat,text,re.I|re.UNICODE)
    if not m:
        raise RuntimeError(f"1903 anchor not found: {anchor}")
    return text[max(0,m.start()-900):min(len(text),m.end()+900)]

raw1=fetch(URL_V1)
raw2=fetch(URL_V2)
sha1=hashlib.sha256(raw1).hexdigest()
sha2=hashlib.sha256(raw2).hexdigest()
if sha1!=SHA_V1:
    raise RuntimeError(f"vol1 source drift {sha1}")
if sha2!=SHA_V2_REGISTRY:
    raise RuntimeError(f"vol2 source drift {sha2}")

v1=raw1.decode("utf-8",errors="replace")
v2=raw2.decode("utf-8",errors="replace")
entries=build_entries(v2)
if len(entries)!=223:
    raise RuntimeError(f"expected 223 refined entries, got {len(entries)}")
by_id={e["entry_id"]:e for e in entries}

selection=list(csv.DictReader(open("experiments/deepening_v1/r3_fg_transfer_selection_v2.csv",encoding="utf-8")))
sel={r["selection_id"]:r for r in selection}

results=[]
for case_id,cfg in CASES.items():
    target=by_id[cfg["entry_id"]]
    frozen_hash=sel[case_id]["entry_sha256"]
    if frozen_hash and target["entry_sha256"]!=frozen_hash:
        raise RuntimeError(f"{case_id} target hash mismatch")
    seed=seed_window(v1,cfg["anchor"])

    pointer_candidates=[]
    for e in entries:
        if roman_head(e["head"])==cfg["chapter"] and cfg["page"] in head_pages(e["head"]):
            pointer_candidates.append(e["entry_id"])

    body_docs=[e["entry_text"][len(e["head"]):].strip() if e["entry_text"].startswith(e["head"]) else e["entry_text"] for e in entries]
    full_docs=[e["entry_text"] for e in entries]

    body_rank=tfidf_rank(seed,body_docs)
    full_rank=tfidf_rank(seed,full_docs)

    def summarize(ranking):
        order=[entries[i]["entry_id"] for _,i in ranking]
        rank=order.index(cfg["entry_id"])+1
        score=next(s for s,i in ranking if entries[i]["entry_id"]==cfg["entry_id"])
        return {
            "rank":rank,
            "score":score,
            "hit1":rank<=1,
            "hit5":rank<=5,
            "hit10":rank<=10,
            "hit20":rank<=20,
            "top20":order[:20],
        }

    br=summarize(body_rank)
    fr=summarize(full_rank)
    results.append({
        "case_id":case_id,
        "stratum":sel[case_id]["stratum"],
        "target_entry":cfg["entry_id"],
        "entry_sha256":target["entry_sha256"],
        "entry_state":"HISTORICAL_START",
        "scope_inclusion":True,
        "native_pointer":{
            "chapter":cfg["chapter"],
            "page":cfg["page"],
            "candidate_count":len(pointer_candidates),
            "target_in_candidates":cfg["entry_id"] in pointer_candidates,
            "target_ordinal":pointer_candidates.index(cfg["entry_id"])+1 if cfg["entry_id"] in pointer_candidates else None,
            "candidates":pointer_candidates,
        },
        "body_lexical":br,
        "full_lexical":fr,
        "profile":{
            "pointer_basis_active":cfg["entry_id"] in pointer_candidates,
            "lexical_substitution_under_budget20":br["hit20"],
            "output_preserved_under_body_lexical_budget20":br["hit20"],
            "profile_non_equivalence_vs_pointer":bool(cfg["entry_id"] in pointer_candidates and br["rank"]>max(1,len(pointer_candidates))),
        },
    })

out={
    "study":"R3_FG_ENTRY_STATE_V1",
    "authority":"frozen transfer panel; deterministic native-pointer and seed-side lexical routes",
    "sources":{
        "vol1_sha256":sha1,
        "vol2_sha256":sha2,
        "refined_entries":len(entries),
    },
    "results":results,
    "limits":[
        "Rank is a deterministic operational exposure measure, not human difficulty.",
        "A lexical miss does not establish information-theoretic insufficiency.",
        "Pointer and lexical routes are both source-grounded but answer different research-path questions.",
        "Historical update labels remain subject to the separate diachronic contrast gate and page verification."
    ],
}
Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r3_fg_entry_state_v1.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_FG_ENTRY_STATE_V1")
print("entries=223")
for r in results:
    p=r["native_pointer"]; b=r["body_lexical"]; f=r["full_lexical"]
    print(f"CASE,{r['case_id']},{r['target_entry']},pointer_candidates={p['candidate_count']},pointer_hit={int(p['target_in_candidates'])},body_rank={b['rank']},body_H20={int(b['hit20'])},full_rank={f['rank']},full_H20={int(f['hit20'])}")
