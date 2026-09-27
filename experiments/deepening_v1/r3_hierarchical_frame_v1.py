from __future__ import annotations
import csv, hashlib, json, re, urllib.request
from pathlib import Path

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read()

raw=fetch()
sha=hashlib.sha256(raw).hexdigest()
if sha!=EXPECTED: raise RuntimeError(f"source drift: {sha}")
text=raw.decode("utf-8",errors="replace")

start_m=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
if not start_m: raise RuntimeError("addenda title not found")
start=start_m.start()

def first_line_marker(pattern,label):
    ms=list(re.finditer(pattern,text[start:],re.I|re.M))
    if not ms: return None
    return (start+ms[0].start(),label,ms[0].group(0).strip())

marker_specs=[
    (r"^\s*BIBLIOGRAPHY\s*$","BIBLIOGRAPHY"),
    (r"^\s*SUPPLEMENTARY\s+NOTE\b.*$","SUPPLEMENTARY_NOTE"),
    (r"^\s*INDEX\s*$","INDEX"),
    (r"^\s*\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK.*$","POST_END_WRAPPER"),
]
markers=[x for x in (first_line_marker(p,l) for p,l in marker_specs) if x]
markers.sort()

# Some source sections can occur in an order not assumed by the old stop regexes.
sections=[]
bounds=[(start,"ADDENDA_BODY","ADDENDA_TITLE")]+markers+[(len(text),"EOF","")]
for i,(pos,label,raw_head) in enumerate(bounds[:-1]):
    end=bounds[i+1][0]
    sections.append({"section_id":f"L1-{i+1:02d}","section_type":label,"start":pos,"end":end,"head":raw_head})
section_by_type={s["section_type"]:s for s in sections}

def section_at(pos):
    for s in sections:
        if s["start"]<=pos<s["end"]: return s
    return None

rows=[]

def emit(level,kind,pos,line,section,parent="",parent_status="",notes=""):
    s=section_at(pos)
    rows.append({
      "node_id":f"{level}-{len(rows)+1:04d}",
      "level":level,
      "kind":kind,
      "section_id":s["section_id"] if s else "",
      "section_type":s["section_type"] if s else "",
      "source_char_start":pos,
      "source_char_end":pos+len(line),
      "source_line":line.strip(),
      "parent_id":parent,
      "parent_status":parent_status,
      "review_status":"PENDING_HUMAN_FRAME_REVIEW",
      "notes":notes,
    })
    return rows[-1]["node_id"]

# L2 candidate patterns in the Addenda body.
add=section_by_type.get("ADDENDA_BODY")
if not add: raise RuntimeError("ADDENDA_BODY missing")
add_text=text[add["start"]:add["end"]]

intro_re=re.compile(r"(?mi)^\s*Introduction\s*,?\s*p{1,2}\.\s*[^\n]+$")
roman_re=re.compile(
  r"(?mi)^\s*(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?"
  r"[IVXLCDM]+(?:\.|,)[^\n]{0,160}?\bp{1,2}\.\s*[^\n]{0,120}$"
)
page_re=re.compile(r"(?mi)^\s*(?:P|PP)\.\s*\d+[^\n]*$")

l2=[]
seen=set()
for kind,rx in [("INTRODUCTION_PAGE_HEADING",intro_re),("ROMAN_PAGE_HEADING",roman_re)]:
    for m in rx.finditer(add_text):
        pos=add["start"]+m.start()
        key=(pos,m.group(0).strip())
        if key in seen: continue
        seen.add(key)
        nid=emit("L2",kind,pos,m.group(0),add["section_id"],notes="structural candidate; intellectual-unit validity requires review")
        l2.append((pos,nid,m.group(0).strip()))
l2.sort()

# L4 bare page pointer candidates in Addenda body.
for m in page_re.finditer(add_text):
    pos=add["start"]+m.start()
    line=m.group(0).strip()
    # Skip if the same line is already represented by an L2 pattern.
    if any(p==pos and h==line for p,_,h in l2):
        continue
    prior=[x for x in l2 if x[0]<pos]
    parent=prior[-1][1] if prior else ""
    emit("L4","BARE_PAGE_POINTER_TARGET",pos,m.group(0),add["section_id"],parent=parent,
         parent_status="PROVISIONAL_NEAREST_PRECEDING_L2_REVIEW_REQUIRED",
         notes="may be independent entry or nested explicit target unit")

# Supplementary contribution and its page-addressed subnotes.
sup=section_by_type.get("SUPPLEMENTARY_NOTE")
temple_id=""
if sup:
    sup_text=text[sup["start"]:sup["end"]]
    if re.search(r"RICHARD\s+C\.\s+TEMPLE|RICHARD\s+TEMPLE",sup_text,re.I):
        temple_id=emit("L3","SIGNED_TEMPLE_CONTRIBUTION",sup["start"],text[sup["start"]:text.find("\n",sup["start"])],
                       sup["section_id"],notes="one responsibility-distinct contribution; nested subnotes not independent contributors")
    for m in page_re.finditer(sup_text):
        pos=sup["start"]+m.start()
        emit("L4","SUPPLEMENTARY_PAGE_SUBNOTE",pos,m.group(0),sup["section_id"],parent=temple_id,
             parent_status="NESTED_UNDER_L3_CONTRIBUTION",
             notes="page-addressed subnote; proposition acts may be multiple/unheaded")

# Sort by source order and reassign stable source-order node IDs per level.
rows.sort(key=lambda r:(r["source_char_start"],r["level"],r["kind"]))
counters={}
old_to_new={}
for r in rows:
    counters[r["level"]]=counters.get(r["level"],0)+1
    new=f"{r['level']}-{counters[r['level']]:04d}"
    old_to_new[r["node_id"]]=new
    r["node_id"]=new
for r in rows:
    if r["parent_id"] in old_to_new: r["parent_id"]=old_to_new[r["parent_id"]]

# Known-boundary coverage checks from the source audit.
known=[
 ("INTRO_P6",r"Introduction\s+p\.\s*6"),
 ("URUMTSI_P201",r"P\.\s*201,\s*Line\s*12"),
 ("CEYLON_INDENTED_ROMAN",r"XIV\.\s*,?\s*p\.\s*313|XIV\.\s+p\.\s*313"),
]
coverage={}
for name,pat in known:
    mm=re.search(pat,text,re.I)
    if not mm:
        coverage[name]={"source_present":False,"candidate_cover":False}
    else:
        cover=[r["node_id"] for r in rows if r["source_char_start"]<=mm.start()<=r["source_char_end"]+5]
        coverage[name]={"source_present":True,"source_char_start":mm.start(),"candidate_cover":bool(cover),"nodes":cover}

counts={}
for r in rows:
    key=f"{r['level']}:{r['kind']}"
    counts[key]=counts.get(key,0)+1
section_counts={s["section_type"]:0 for s in sections}
for r in rows:
    section_counts[r["section_type"]]=section_counts.get(r["section_type"],0)+1

meta={
 "source_sha256":sha,
 "sections":sections,
 "candidate_count":len(rows),
 "counts":counts,
 "section_candidate_counts":section_counts,
 "known_boundary_coverage":coverage,
 "l5_quotation_count_authorized":None,
 "l6_proposition_act_count_authorized":None,
 "replacement_denominator_authorized":False,
 "authority":"structural candidate map only; human frame review pending",
}

out=Path("experiments/deepening_v1/results")
out.mkdir(parents=True,exist_ok=True)
with (out/"hierarchical_frame_candidates_v1.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
(out/"hierarchical_frame_meta_v1.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_HIERARCHICAL_FRAME_V1")
print("source_sha256="+sha)
for s in sections:
    print(f"SECTION,{s['section_id']},{s['section_type']},{s['start']},{s['end']}")
for k,v in sorted(counts.items()):
    print(f"COUNT,{k},{v}")
for k,v in coverage.items():
    print(f"COVER,{k},source_present={int(v.get('source_present',False))},candidate_cover={int(v.get('candidate_cover',False))},nodes={'|'.join(v.get('nodes',[]))}")
print("CANDIDATE_COUNT="+str(len(rows)))
print("L5_COUNT_AUTHORIZED=0")
print("L6_COUNT_AUTHORIZED=0")
print("REPLACEMENT_DENOMINATOR_AUTHORIZED=0")
