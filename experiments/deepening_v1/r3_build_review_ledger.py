from __future__ import annotations

import csv
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

start_match=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
if not start_match:
    raise RuntimeError("addenda start missing")
start=start_match.start()

stop_candidates=[]
for pat in [r"\nBIBLIOGRAPHY\b",r"\nSUPPLEMENTARY NOTE\b",r"\nINDEX\b"]:
    m=re.search(pat,text[start:],re.I)
    if m: stop_candidates.append(start+m.start())
stop=min(stop_candidates) if stop_candidates else len(text)
region=text[start:stop]

head_re=re.compile(
    r"(?m)^(?P<head>(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?"
    r"[IVXLCDM]+(?:\.|,)[^\n]{0,120}?\bp{1,2}\.\s*[^\n]{0,80})$"
)
heads=list(head_re.finditer(region))

# Section markers are descriptive context only; they never decide validity.
section_patterns=[
    ("INTRODUCTORY_NOTICES",r"MARCO\s+POLO\s+AND\s+HIS\s+BOOK\s+INTRODUCTORY\s+NOTICES"),
    ("PROLOGUE",r"THE\s+BOOK\s+OF\s+MARCO\s+POLO\.\s+PROLOGUE"),
    ("BOOK_FIRST",r"BOOK\s+FIRST\.\s+ACCOUNT\s+OF\s+REGIONS"),
    ("BOOK_SECOND",r"BOOK\s+SECOND"),
    ("BOOK_THIRD",r"BOOK\s+THIRD"),
]
markers=[]
for name,pat in section_patterns:
    for m in re.finditer(pat,region,re.I|re.S):
        markers.append((m.start(),name))
markers.sort()

def section_at(pos):
    current="PREFACE_OR_FRONT_MATTER"
    for p,name in markers:
        if p<=pos: current=name
        else: break
    return current

def parse_page_refs(head):
    # Descriptive extraction only.
    m=re.search(r"\bp{1,2}\.\s*(.+)$",head,re.I)
    return m.group(1).strip() if m else ""

rows=[]
for i,m in enumerate(heads):
    s=m.start()
    e=heads[i+1].start() if i+1<len(heads) else len(region)
    block=region[s:e].strip()
    head=m.group("head").strip()
    rows.append({
        "candidate_id":f"YC1920-{i+1:04d}",
        "section_context":section_at(s),
        "head":head,
        "page_ref_raw":parse_page_refs(head),
        "source_char_start":start+s,
        "source_char_end":start+e,
        "block_sha256":hashlib.sha256(block.encode("utf-8")).hexdigest(),
        "entry_text":" ".join(block.split()),
        # Human coding fields, intentionally blank.
        "frame_status":"",
        "frame_exclusion_reason":"",
        "target_status":"",
        "earlier_locus":"",
        "earlier_actor_source":"",
        "later_actor_source":"",
        "relation_labels":"",
        "relation_evidence_span":"",
        "humanistic_consequence":"",
        "verification_authority":"TRANSCRIPTION_ONLY",
        "review_pass_1":"",
        "review_pass_2":"",
        "adjudication_note":"",
    })

outdir=Path("experiments/deepening_v1/results")
outdir.mkdir(parents=True,exist_ok=True)

csv_path=outdir/"r3_inventory_review_ledger_v1.csv"
with csv_path.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

meta={
    "study":"R3_A_REVIEW_LEDGER_V1",
    "source_sha256":sha,
    "row_count":len(rows),
    "section_context_counts":{},
    "coding_fields_blank":True,
    "notes":[
        "Section context is descriptive and does not decide frame validity.",
        "Cue flags from the candidate enumerator are intentionally absent from this coding ledger.",
        "Every exclusion must preserve a reason and denominator trace."
    ]
}
for r in rows:
    meta["section_context_counts"][r["section_context"]]=meta["section_context_counts"].get(r["section_context"],0)+1
(outdir/"r3_inventory_review_ledger_v1_meta.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_A_REVIEW_LEDGER_V1")
print("rows="+str(len(rows)))
for k,v in sorted(meta["section_context_counts"].items()):
    print(f"SECTION,{k},{v}")
print("RELATION_LABELS_ASSIGNED=0")
