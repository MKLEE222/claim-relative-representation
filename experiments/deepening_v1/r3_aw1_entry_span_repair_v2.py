from __future__ import annotations
import collections, hashlib, math, re, urllib.request
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
"the","and","that","this","with","from","have","has","had","were","was","are","for","not","but",
"his","her","their","there","which","into","than","then","they","them","you","your","its","who",
"whom","what","when","where","how","all","any","some","more","most","such","only","been","being",
"will","would","could","should","about","over","under","after","before","between","also","very",
"upon","our","out","off","one","two","same","find","material","edition","bears","whether",
"later","earlier","which","does","what","given","discussion","entry","present"
}

CASES=[
 {
  "id":"R3Q-PASH-STANCE",
  "task":"Which earlier proposition does Stein corroborate, and which does he challenge?",
  "seed_a":"Pashai","seed_b":"Chitral",
  "gold_entry":"YC1920E-0030",
  "forbidden":{"kafiristan","stein"},
 },
 {
  "id":"R3Q-DES-EVIDENCE",
  "task":"Which evidence in the 1920 discussion supports distance and marches, and which supports the local-folklore source attribution?",
  "seed_a":"Great Desert","seed_b":"evil spirits",
  "gold_entry":"YC1920E-0049",
  "forbidden":{"plane-table","plane","table","cyclometer","stein"},
 },
]

@dataclass
class W:
    scope:str
    start:int
    words:list[str]
    char_lo:int
    char_hi:int

TOKEN_RE=re.compile(r"[A-Za-z][A-Za-z'-]{2,}")

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read()

def token_stream(text):
    out=[]
    for m in TOKEN_RE.finditer(text):
        x=m.group(0).lower()
        out.append((x,m.start(),m.end()))
        if "-" in x:
            for p in x.split("-"):
                if len(p)>=3: out.append((p,m.start(),m.end()))
    return out

def toks(s):
    return [x for x,_,__ in token_stream(s)]

def windows(scope,text,base_char=0):
    ts=token_stream(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)<WINDOW//2: continue
        out.append(W(
            scope=scope,
            start=s,
            words=[x for x,_,__ in ch],
            char_lo=base_char+ch[0][1],
            char_hi=base_char+ch[-1][2],
        ))
    return out

def all_positions(low,needle):
    n=needle.lower(); out=[]; p=0
    while True:
        p=low.find(n,p)
        if p<0: break
        out.append(p); p+=max(1,len(n))
    return out

def enclosing_paragraph(text,pos):
    # Project Gutenberg paragraphs are normally blank-line separated.
    left=text.rfind("\n\n",0,pos)
    right=text.find("\n\n",pos)
    if left<0: left=max(0,pos-1600)
    else: left+=2
    if right<0: right=min(len(text),pos+2200)
    # Avoid pathological tiny paragraphs caused by wrapped headings.
    if right-left<300:
        left=max(0,pos-1200); right=min(len(text),pos+1800)
    return text[left:right]

def seed_paragraph(text,a,b,focus_on_b=False):
    low=text.lower()
    aa=all_positions(low,a); bb=all_positions(low,b)
    if not aa or not bb: raise RuntimeError(f"seed anchor missing: {a} / {b}")
    _,pa,pb=min((abs(x-y),x,y) for x in aa for y in bb)
    focus=pb if focus_on_b else (pa+pb)//2
    return enclosing_paragraph(text,focus),pa,pb,abs(pa-pb)

def locate_addenda(text):
    m=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
    if not m: raise RuntimeError("addenda start missing")
    return m.start()

MONTHS=r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
def exclusion_reason(head):
    if re.search(rf"^[IVXLCDM]+\.,\s*(?:{MONTHS}|(?:18|19)\d{{2}})\b",head,re.I): return "F1"
    if re.search(r"^[A-Z]\.\s*Chap\.",head,re.I): return "F2"
    if re.search(r"\bp{1,2}\.\s*[^,]{0,40}\),",head,re.I): return "F3"
    if re.search(r"^[IVXLCDM]+\.,\s*pp?\.\s*[^\n]{0,90}\bin\s+(?:Mr\.|Dr\.|Prof\.|Sir\s+\w+['’]s|[A-Z][a-z]+['’]s)\s+paper\b",head,re.I): return "F4"
    return ""

def accepted_frame(text):
    start=locate_addenda(text)
    stops=[]
    for pat in [r"\nBIBLIOGRAPHY\b",r"\nSUPPLEMENTARY NOTE\b",r"\nINDEX\b"]:
        m=re.search(pat,text[start:],re.I)
        if m: stops.append(start+m.start())
    stop=min(stops) if stops else len(text)
    region=text[start:stop]
    head_re=re.compile(
      r"(?m)^(?P<head>(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?"
      r"[IVXLCDM]+(?:\.|,)[^\n]{0,120}?\bp{1,2}\.\s*[^\n]{0,80})$"
    )
    heads=list(head_re.finditer(region))
    accepted=[]
    for i,m in enumerate(heads):
        s=m.start(); e=heads[i+1].start() if i+1<len(heads) else len(region)
        head=m.group("head").strip()
        reason=exclusion_reason(head)
        if reason:
            if accepted: accepted[-1]["source_end"]=start+e
            continue
        accepted.append({
            "entry_id":f"YC1920E-{len(accepted)+1:04d}",
            "head":head,
            "source_start":start+s,
            "source_end":start+e,
        })
    return {x["entry_id"]:x for x in accepted},start

def idf(ws):
    n=len(ws); df=collections.Counter()
    for w in ws:
        for t in set(w.words): df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def query(seed,task,base_ws,forbidden):
    counts=collections.Counter(t for t in toks(seed+" "+task) if t not in STOP and len(t)>=4)
    weights=idf(base_ws)
    q=sorted(((t,c*weights.get(t,1.0)) for t,c in counts.items()),key=lambda z:(-z[1],z[0]))[:K]
    leak=sorted({t for t,_ in q}&forbidden)
    if leak: raise RuntimeError("TARGET LEAKAGE: "+",".join(leak))
    return q

def score(w,q):
    c=collections.Counter(w.words)
    return sum(weight*min(c.get(term,0),3) for term,weight in q)

def overlap(w,lo,hi):
    return w.char_hi>lo and w.char_lo<hi

def rank_entry(ws,entry,q):
    ranked=sorted(((score(w,q),w) for w in ws),key=lambda z:(-z[0],z[1].scope,z[1].start))
    hits=[]
    for i,(s,w) in enumerate(ranked,1):
        if w.scope in ("V2","LATER") and overlap(w,entry["source_start"],entry["source_end"]):
            hits.append((i,s,w))
    if not hits: return None,None,ranked,0
    best=min(hits,key=lambda z:z[0])
    return best[0],best[1],ranked,len(hits)

raw={k:fetch(v) for k,v in URLS.items()}
for k,b in raw.items():
    got=hashlib.sha256(b).hexdigest()
    if got!=EXPECTED[k]: raise RuntimeError(f"source drift {k}: {got}")
text={k:v.decode("utf-8",errors="replace") for k,v in raw.items()}
frame,boundary=accepted_frame(text["V2"])
base_ws=windows("V1",text["V1"])
full_ws=windows("V1",text["V1"])+windows("V2",text["V2"])
later_ws=windows("LATER",text["V2"][boundary:],base_char=boundary)

print("R3_AW1_ENTRY_SPAN_EVALUATOR_REPAIR_V2")
print("scientific_policy_changed=0")
for c in CASES:
    print("CASE="+c["id"])
    try:
        seed,pa,pb,dist=seed_paragraph(text["V1"],c["seed_a"],c["seed_b"],focus_on_b=(c["id"]=="R3Q-DES-EVIDENCE"))
        entry=frame[c["gold_entry"]]
        print(f"seed_anchor_distance_chars={dist}")
        print(f"gold_entry={entry['entry_id']}")
        print(f"gold_entry_head={entry['head']}")
        print(f"gold_source_span={entry['source_start']}:{entry['source_end']}")
        q=query(seed,c["task"],base_ws,c["forbidden"])
        print("query_terms="+"|".join(t for t,_ in q))
        for name,ws in [("GSA_FULL_OBJECT",full_ws),("GSA_LATER_LAYER",later_ws)]:
            r,s,ranked,nwin=rank_entry(ws,entry,q)
            rr=0 if r is None else 1/r
            print(",".join([
              "RESULT",c["id"],name,
              f"candidates={len(ranked)}",
              f"gold_windows={nwin}",
              f"target_rank={r if r is not None else 'NA'}",
              f"target_score={s if s is not None else 'NA'}",
              f"MRR={rr:.6f}",
              f"H10={int(r is not None and r<=10)}",
              f"H20={int(r is not None and r<=20)}",
              f"H50={int(r is not None and r<=50)}",
            ]))
    except Exception as e:
        print("IMPLEMENTATION_STOP,"+c["id"]+","+type(e).__name__+","+str(e).replace("\n"," "))
print("NO_RETUNING_AFTER_OUTPUT=1")
