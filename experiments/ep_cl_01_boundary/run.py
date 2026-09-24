from __future__ import annotations

import collections
import hashlib
import math
import re
import urllib.request
from dataclasses import dataclass

URL="https://www.gutenberg.org/cache/epub/10636/pg10636.txt"
EXPECTED_SHA="7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5"

CHAPTER="CHAPTER XXX. CONCERNING THE BLACK STONES THAT ARE DUG IN CATHAY, AND ARE BURNT FOR FUEL."
NEXT_CHAPTER="CHAPTER XXXI."
SEED_A="black stones existing in beds in the mountains"
SEED_B="those stones burn better and cost less"
TARGET_A="Baron Richthofen"
TARGET_B="world’s wealth and power"

TASK="Find the editorial material attached to this passage that bears on how the coal observation is contextualized by the editor."

WINDOW=180
STRIDE=90
K=12

STOP={
"the","and","that","this","with","from","have","has","had","were","was","are","for","not","but",
"his","her","their","there","which","into","than","then","they","them","you","your","its","who",
"whom","what","when","where","how","all","any","some","more","most","such","only","been","being",
"will","would","could","should","about","over","under","after","before","between","also","very",
"upon","our","out","off","one","two","same","find","editorial","material","attached","passage",
"bears","contextualized","editor"
}
FORBIDDEN={"richthofen","wealth","power","revolution","anthracite"}

@dataclass
class W:
    start:int
    words:list[str]

def get():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def toks(s):
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}",s.lower())

def windows(text):
    ts=toks(text)
    out=[]
    for s in range(0,max(1,len(ts)-WINDOW+1),STRIDE):
        ch=ts[s:s+WINDOW]
        if len(ch)>=WINDOW//2:
            out.append(W(s,ch))
    return out

def idf(ws):
    n=len(ws)
    df=collections.Counter()
    for w in ws:
        for t in set(w.words):
            df[t]+=1
    return {t:math.log((n+1)/(c+1))+1 for t,c in df.items()}

def score(w,q):
    c=collections.Counter(w.words)
    return sum(weight*min(c.get(term,0),3) for term,weight in q)

def target_window(ws):
    a=set(toks(TARGET_A)); b=set(toks(TARGET_B))
    for w in ws:
        s=set(w.words)
        if a<=s and b<=s:
            return w
    raise RuntimeError("coal target not found in local chapter")

raw=get()
sha=hashlib.sha256(raw).hexdigest()
assert sha==EXPECTED_SHA
text=raw.decode("utf-8",errors="replace")

chapter_start=text.find(CHAPTER)
if chapter_start<0:
    raise RuntimeError("coal chapter heading not found")
chapter_end=text.find(NEXT_CHAPTER,chapter_start+len(CHAPTER))
if chapter_end<0:
    raise RuntimeError("next chapter boundary not found")
chapter=text[chapter_start:chapter_end]

sa=chapter.lower().find(SEED_A.lower())
sb=chapter.lower().find(SEED_B.lower(),sa)
if sa<0 or sb<0:
    raise RuntimeError("coal seed anchors not found")
seed_end=chapter.find("\n",sb)
if seed_end<0:
    seed_end=min(len(chapter),sb+800)
seed=chapter[sa:seed_end]

# M_LOCAL_ATTACHMENT support gate.
marker_match=re.search(r"\{(\d+)\}",seed)
support_marker=marker_match.group(1) if marker_match else None
note_match=None
if support_marker:
    note_match=re.search(rf"NOTE\s+{re.escape(support_marker)}\.—",chapter[seed_end:],flags=re.I)

support = support_marker is not None and note_match is not None
print("EP_CL_01_LOCAL_ATTACHMENT_BOUNDARY")
print("source_sha256="+sha)
print("support_primitive=M_LOCAL_ATTACHMENT")
print("support_feasible="+str(int(support)))
print("seed_marker="+(support_marker or "NONE"))

if not support:
    print("STATUS=MEDIATION_SUPPORT_UNAVAILABLE")
    print("TARGET_OUTCOME_OPENED=0")
    raise SystemExit(0)

note_start=seed_end+note_match.start()
print("matching_note_label=NOTE_"+support_marker)

local_ws=windows(chapter)
tgt=target_window(local_ws)

# CL-SPAN
print("RESULT,CL_SPAN,target_in_scope=0,candidates=1,target_rank=NA")

# CL-LOCAL-LINEAR: query from seed + task only.
iw=idf(local_ws)
c=collections.Counter(t for t in toks(seed+" "+TASK) if t not in STOP and len(t)>=4)
q=sorted(((t,n*iw.get(t,1.0)) for t,n in c.items()),key=lambda z:(-z[1],z[0]))[:K]
leak=set(t for t,w in q) & FORBIDDEN
if leak:
    raise RuntimeError(f"target leakage: {sorted(leak)}")
ranked=sorted(((score(w,q),w) for w in local_ws),key=lambda z:(-z[0],z[1].start))
linear_rank=None
for i,(s,w) in enumerate(ranked,1):
    if abs(w.start-tgt.start)<STRIDE:
        linear_rank=i
        break
print("query_terms="+"|".join(t for t,w in q))
print("target_only_query_overlap=0")
print(f"RESULT,CL_LOCAL_LINEAR,target_in_scope=1,candidates={len(ranked)},target_rank={linear_rank if linear_rank is not None else 'NA'}")

# CL-ATTACHMENT: the note unit is the sole bridge target.
note_end=len(chapter)
# one-note chapter in this locus; if another NOTE appears before chapter end, it would close unit.
next_note=re.search(r"\nNOTE\s+\d+\.—",chapter[note_start+10:],flags=re.I)
if next_note:
    note_end=note_start+10+next_note.start()
note_unit=chapter[note_start:note_end]
target_in_note = TARGET_A.lower() in note_unit.lower() and (
    TARGET_B.lower() in note_unit.lower() or "world's wealth and power" in note_unit.lower()
)
print(f"RESULT,CL_ATTACHMENT,target_in_scope={int(target_in_note)},candidates=1,target_rank={1 if target_in_note else 'NA'}")
print("CLAIM_STATE_OPENED=0")
