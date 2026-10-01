from __future__ import annotations

import csv, hashlib, json, re, time, urllib.request
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

raw=fetch(); sha=hashlib.sha256(raw).hexdigest()
if sha!=EXPECTED: raise RuntimeError(f"source drift: {sha}")
text=raw.decode("utf-8",errors="replace")
sm=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
if not sm: raise RuntimeError("addenda start missing")
start=sm.start()
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

markers=[]
for name,pat in [
    ("INTRODUCTORY_NOTICES",r"MARCO\s+POLO\s+AND\s+HIS\s+BOOK\s+INTRODUCTORY\s+NOTICES"),
    ("PROLOGUE",r"THE\s+BOOK\s+OF\s+MARCO\s+POLO\.\s+PROLOGUE"),
    ("BOOK_FIRST",r"BOOK\s+FIRST\.\s+ACCOUNT\s+OF\s+REGIONS"),
    ("BOOK_SECOND",r"BOOK\s+SECOND"),
    ("BOOK_THIRD",r"BOOK\s+THIRD"),
]:
    for m in re.finditer(pat,region,re.I|re.S): markers.append((m.start(),name))
markers.sort()
def section_at(pos):
    sec="PREFACE_OR_FRONT_MATTER"
    for p,n in markers:
        if p<=pos: sec=n
        else: break
    return sec

MONTHS=r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"

def exclusion_reason(head):
    if re.search(rf"^[IVXLCDM]+\.,\s*(?:{MONTHS}|(?:18|19)\d{{2}})\b",head,re.I):
        return "F1_EXTERNAL_PERIODICAL_ISSUE"
    if re.search(r"^[A-Z]\.\s*Chap\.",head,re.I):
        return "F2_LETTERED_SOURCE_SUBITEM"
    if re.search(r"\bp{1,2}\.\s*[^,]{0,40}\),",head,re.I):
        return "F3_CLOSING_PAREN_CITATION_CONTINUATION"
    if re.search(r"^[IVXLCDM]+\.,\s*pp?\.\s*[^\n]{0,90}\bin\s+(?:Mr\.|Dr\.|Prof\.|Sir\s+\w+['’]s|[A-Z][a-z]+['’]s)\s+paper\b",head,re.I):
        return "F4_EXPLICIT_NAMED_PAPER_PAGE"
    return ""

raw_candidates=[]
for i,m in enumerate(heads):
    s=m.start(); e=heads[i+1].start() if i+1<len(heads) else len(region)
    block=region[s:e].strip()
    raw_candidates.append({
        "raw_candidate_id":f"YC1920-{i+1:04d}",
        "section_context":section_at(s),
        "head":m.group("head").strip(),
        "region_start":s,"region_end":e,
        "source_start":start+s,"source_end":start+e,
        "block":block,
    })

accepted=[]
excluded=[]
for c in raw_candidates:
    reason=exclusion_reason(c["head"])
    if reason:
        rec={k:v for k,v in c.items() if k!="block"}
        rec["reason"]=reason
        rec["block_sha256"]=hashlib.sha256(c["block"].encode()).hexdigest()
        rec["merged_into"]=accepted[-1]["root_candidate_id"] if accepted else ""
        excluded.append(rec)
        if accepted:
            accepted[-1]["source_end"]=c["source_end"]
            accepted[-1]["merged_raw_candidate_ids"].append(c["raw_candidate_id"])
            accepted[-1]["entry_text_raw"] += "\n" + c["block"]
        continue
    accepted.append({
        "entry_id":f"YC1920E-{len(accepted)+1:04d}",
        "root_candidate_id":c["raw_candidate_id"],
        "section_context":c["section_context"],
        "head":c["head"],
        "source_start":c["source_start"],
        "source_end":c["source_end"],
        "merged_raw_candidate_ids":[],
        "entry_text_raw":c["block"],
    })

for a in accepted:
    a["entry_text"]=" ".join(a.pop("entry_text_raw").split())
    a["entry_sha256"]=hashlib.sha256(a["entry_text"].encode()).hexdigest()
    a["merged_raw_candidate_ids"]="|".join(a["merged_raw_candidate_ids"])
    a["human_frame_status"]=""
    a["human_frame_note"]=""
    a["relation_labels"]=""
    a["relation_evidence_span"]=""
    a["verification_authority"]="TRANSCRIPTION_ONLY"

out=Path("experiments/deepening_v1/results"); out.mkdir(parents=True,exist_ok=True)
with (out/"r3_structural_frame_v2.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(accepted[0])); w.writeheader(); w.writerows(accepted)
with (out/"r3_structural_exclusions_v2.csv").open("w",newline="",encoding="utf-8") as f:
    fields=list(excluded[0]) if excluded else ["raw_candidate_id","reason"]
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(excluded)

meta={
    "source_sha256":sha,
    "raw_candidate_count":len(raw_candidates),
    "structurally_accepted_count":len(accepted),
    "structurally_excluded_count":len(excluded),
    "exclusion_counts":{},
    "accepted_section_counts":{},
    "relation_labels_assigned":0,
}
for e in excluded: meta["exclusion_counts"][e["reason"]]=meta["exclusion_counts"].get(e["reason"],0)+1
for a in accepted: meta["accepted_section_counts"][a["section_context"]]=meta["accepted_section_counts"].get(a["section_context"],0)+1
(out/"r3_structural_frame_v2_meta.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_STRUCTURAL_FRAME_V2")
for k,v in meta.items():
    if not isinstance(v,dict): print(f"{k}={v}")
for k,v in sorted(meta["exclusion_counts"].items()): print(f"EXCLUDE,{k},{v}")
for k,v in sorted(meta["accepted_section_counts"].items()): print(f"SECTION,{k},{v}")
