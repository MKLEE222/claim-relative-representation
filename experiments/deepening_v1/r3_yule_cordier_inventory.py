from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"

def fetch():
    last=None
    for attempt in range(5):
        try:
            req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
            with urllib.request.urlopen(req,timeout=45) as r:
                return r.read()
        except Exception as e:
            last=e
            if attempt<4: time.sleep(2**attempt)
    raise RuntimeError(last)

raw=fetch()
sha=hashlib.sha256(raw).hexdigest()
if sha!=EXPECTED:
    raise RuntimeError(f"source drift: {sha}")
text=raw.decode("utf-8",errors="replace")

start=text.find("SER MARCO POLO\n\nNOTES AND ADDENDA TO SIR HENRY YULE’S EDITION")
if start<0:
    # tolerate line wrapping / apostrophe variants
    m=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
    if not m: raise RuntimeError("addenda start not found")
    start=m.start()

# Stop before the addenda bibliography/index when possible.
stop_candidates=[]
for pat in [r"\nBIBLIOGRAPHY\b",r"\nSUPPLEMENTARY NOTE\b",r"\nINDEX\b"]:
    m=re.search(pat,text[start:],re.I)
    if m: stop_candidates.append(start+m.start())
stop=min(stop_candidates) if stop_candidates else len(text)
region=text[start:stop]

# Retrospective entry heads in the Addenda typically begin with a Roman chapter/section
# and one or more page references, e.g. "XXIV., pp. 423, 430."
head_re=re.compile(
    r"(?m)^(?P<head>(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?"
    r"[IVXLCDM]+(?:\.|,)[^\n]{0,120}?\bp{1,2}\.\s*[^\n]{0,80})$"
)
heads=list(head_re.finditer(region))

entries=[]
for i,m in enumerate(heads):
    s=m.start()
    e=heads[i+1].start() if i+1<len(heads) else len(region)
    block=region[s:e].strip()
    # bounded candidate excerpt; full offsets retained for later source verification.
    entries.append({
        "candidate_id":f"YC1920-{i+1:04d}",
        "head":m.group("head").strip(),
        "region_char_start":s,
        "region_char_end":e,
        "source_char_start":start+s,
        "source_char_end":start+e,
        "block_sha256":hashlib.sha256(block.encode("utf-8")).hexdigest(),
        "preview":" ".join(block.split())[:1200],
        "cue_flags":{
            "regarding":bool(re.search(r"\bregarding\b",block,re.I)),
            "referring":bool(re.search(r"\breferring\b",block,re.I)),
            "error":bool(re.search(r"\berror|erroneous|mistaken|wrong\b",block,re.I)),
            "correct":bool(re.search(r"\bcorrect|right\b",block,re.I)),
            "doubt":bool(re.search(r"\bdoubt|doubtful|probably|perhaps\b",block,re.I)),
            "confirms":bool(re.search(r"\bconfirm|uphold|supported\b",block,re.I)),
        },
        "classification_status":"UNREAD_CANDIDATE",
    })

out={
    "study":"R3_YULE_CORDIER_RETROSPECTIVE_INVENTORY_V1",
    "authority":"candidate enumeration only; no humanistic relation classification yet",
    "source":{"url":URL,"sha256":sha},
    "region":{"source_char_start":start,"source_char_end":stop,"chars":len(region)},
    "candidate_count":len(entries),
    "cue_summary":{
        key:sum(int(x["cue_flags"][key]) for x in entries)
        for key in ["regarding","referring","error","correct","doubt","confirms"]
    },
    "candidates":entries,
    "limits":[
        "Regex heads define a reproducible candidate frame, not verified historical relations.",
        "Cue flags are navigation aids only and never determine classification.",
        "Final load-bearing relation labels require source/page-image verification.",
        "Entries without dramatic evaluative cues remain in the denominator."
    ],
}
Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r3_yule_cordier_inventory_candidates.json").write_text(
    json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8"
)
print("R3_YULE_CORDIER_CANDIDATE_INVENTORY")
print("source_sha256="+sha)
print("candidate_count="+str(len(entries)))
for k,v in out["cue_summary"].items():
    print(f"CUE,{k},{v}")
print("CLASSIFIED_RELATIONS=0")
