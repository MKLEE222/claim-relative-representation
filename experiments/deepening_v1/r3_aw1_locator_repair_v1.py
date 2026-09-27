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
  "target_a":"Stein","target_b":"Kafiristan",
  "forbidden":{"kafiristan"},
 },
 {
  "id":"R3Q-ARBR-COMMIT",
  "task":"Whose commitment is the cypress identification, and does the inspected entry establish Cordier's adoption of it?",
  "seed_a":"Arbre Sec","seed_b":"Oriental Plane",
  "target_a":"Houtum-Schindler","target_b":"Cypress",
  "forbidden":{"houtum-schindler","houtum","schindler","cypress"},
 },
 {
  "id":"R3Q-DES-EVIDENCE",
  "task":"Which evidence in the 1920 discussion supports distance and marches, and which supports the local-folklore source attribution?",
  "seed_a":"Great Desert","seed_b":"evil spirits",
  "target_a":"plane-table","target_b":"cyclometer",
  "forbidden":{"plane-table","plane","table","cyclometer"},
 },
]

@dataclass
class W:
    scope:str
    start:int
    words:list[str]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r: return r.read()

def toks(s):
    base=re.findall(r"[A-Za-z][A-Za-z'-]{2,}",s.lower())
    out=[]
    for x in base:
        out.append(x)
        if "-" in x: out.extend(p for p in x.split("-") if len(p)>=3)
    return out

def all_positions(low, needle):
    n=needle.lower(); out=[]; p=0
    while True:
        p=low.find(n,p)
        if p<0: break
        out.append(p); p+=max(1,len(n))
    return out

def locate_local_span_closest_pair(text,a,b):
    low=text.lower()
    aa=all_positions(low,a); bb=all_positions(low,b)
    if not aa: raise RuntimeError(f"seed anchor A not found: {a}")
    if not bb: raise RuntimeError(f"seed anchor B not found: {b}")
    pairs=[(abs(x-y),min(x,y),x,y) for x in aa for y in bb]
    dist,_,pa,pb=min(pairs)
    if dist>12000: raise RuntimeError(f"no local anchor pair within 12000 chars: {a} / {b}; nearest={dist}")
    lo=max(0,min(pa,pb)-1800); hi=min(len(text),max(pa,pb)+2200)
    return text[lo:hi],pa,pb,dist

def locate_addenda(text):
    m=re.search(r"NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE[’']S\s+EDITION",text,flags=re.I)
    if not m: m=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,flags=re.I)
    if not m: raise RuntimeError("native Addenda boundary not found")
    return m.start()

def windows(scope,text):
    ts=toks(text); out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2: out.append(W(scope,s,ch))
    return out

def find_target(ws,a,b):
    aa=set(toks(a)); bb=set(toks(b))
    ms=[w for w in ws if aa<=set(w.words) and bb<=set(w.words)]
    if not ms: raise RuntimeError(f"target evaluation window not found: {a} / {b}")
    return ms[0]

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

def rank(ws,target,q):
    ranked=sorted(((score(w,q),w) for w in ws),key=lambda z:(-z[0],z[1].scope,z[1].start))
    for i,(s,w) in enumerate(ranked,1):
        if w.scope==target.scope and abs(w.start-target.start)<STRIDE: return i,s,ranked
    return None,None,ranked

raw={k:fetch(v) for k,v in URLS.items()}
for k,b in raw.items():
    got=hashlib.sha256(b).hexdigest()
    if got!=EXPECTED[k]: raise RuntimeError(f"source drift {k}: {got}")
text={k:v.decode("utf-8",errors="replace") for k,v in raw.items()}
boundary=locate_addenda(text["V2"]); later=text["V2"][boundary:]
base_ws=windows("V1",text["V1"])
full_ws=windows("V1",text["V1"])+windows("V2",text["V2"])
later_ws=windows("LATER",later)

print("R3_AW1_LOCATOR_REPAIR_FOR_STOPPED_CASES")
print("repair_rule=closest occurrence pair of the unchanged frozen seed anchors")
print("scientific_policy_changed=0")
for c in CASES:
    print("CASE="+c["id"])
    try:
        seed,pa,pb,dist=locate_local_span_closest_pair(text["V1"],c["seed_a"],c["seed_b"])
        print(f"seed_anchor_distance_chars={dist}")
        q=query(seed,c["task"],base_ws,c["forbidden"])
        target_full=find_target(full_ws,c["target_a"],c["target_b"])
        target_later=find_target(later_ws,c["target_a"],c["target_b"])
        print("query_terms="+"|".join(t for t,_ in q))
        for name,ws,target in [("GSA_FULL_OBJECT",full_ws,target_full),("GSA_LATER_LAYER",later_ws,target_later)]:
            r,s,ranked=rank(ws,target,q); rr=0 if r is None else 1/r
            print(",".join(["RESULT",c["id"],name,f"candidates={len(ranked)}",f"target_rank={r if r is not None else 'NA'}",f"target_score={s if s is not None else 'NA'}",f"MRR={rr:.6f}",f"H10={int(r is not None and r<=10)}",f"H20={int(r is not None and r<=20)}",f"H50={int(r is not None and r<=50)}"]))
    except Exception as e:
        print("IMPLEMENTATION_STOP,"+c["id"]+","+type(e).__name__+","+str(e).replace("\n"," "))
print("NO_RETUNING_AFTER_OUTPUT=1")
