from __future__ import annotations
import csv, hashlib, json, re, urllib.request
from pathlib import Path

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r: return r.read()

raw=fetch()
sha=hashlib.sha256(raw).hexdigest()
if sha!=EXPECTED: raise RuntimeError(f"source drift: {sha}")
text=raw.decode("utf-8",errors="replace")

title=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
if not title: raise RuntimeError("Addenda publication title not found")

# Actual notes content begins after the synopsis at the repeated source heading.
content_matches=list(re.finditer(r"(?mi)^\s*MARCO\s+POLO\s+AND\s+HIS\s+BOOK\.\s*\n\s*INTRODUCTORY\s+NOTICES\.\s*$",text[title.end():]))
if not content_matches: raise RuntimeError("actual Addenda content start not found")
content_start=title.end()+content_matches[-1].start()

# Actual terminal section markers. We inspect all line-initial occurrences after content start.
def occurrences(pattern):
    return [(content_start+m.start(),m.group(0).strip()) for m in re.finditer(pattern,text[content_start:],re.I|re.M)]

bib_occ=occurrences(r"^\s*BIBLIOGRAPHY\s+OF\s+MARCO\s+POLO['’]S\s+BOOK(?:\.\[?\d*\]?|\.)?\s*$")
sup_occ=occurrences(r"^\s*SUPPLEMENTARY\s+NOTE\.\s*$")
idx_occ=occurrences(r"^\s*INDEX\s*$")
if not bib_occ: raise RuntimeError("actual bibliography section marker not found")
if not sup_occ: raise RuntimeError("actual supplementary note marker not found")
if not idx_occ: raise RuntimeError("actual index marker not found")

# Choose ordered late-source section markers: bibliography before Temple supplement before final index.
index_pos=idx_occ[-1][0]
sup_candidates=[x for x in sup_occ if x[0]<index_pos]
supp_pos,supp_head=sup_candidates[-1]
bib_candidates=[x for x in bib_occ if x[0]<supp_pos]
bib_pos,bib_head=bib_candidates[-1]

end_m=re.search(r"(?mi)^\s*\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK.*$",text[index_pos:])
end_pos=index_pos+end_m.start() if end_m else len(text)

sections=[
 {"section_id":"L1-01","section_type":"ADDENDA_BODY","start":content_start,"end":bib_pos,"head":"MARCO POLO AND HIS BOOK / INTRODUCTORY NOTICES"},
 {"section_id":"L1-02","section_type":"BIBLIOGRAPHY","start":bib_pos,"end":supp_pos,"head":bib_head},
 {"section_id":"L1-03","section_type":"SUPPLEMENTARY_NOTE","start":supp_pos,"end":index_pos,"head":supp_head},
 {"section_id":"L1-04","section_type":"INDEX","start":index_pos,"end":end_pos,"head":"INDEX"},
 {"section_id":"L1-05","section_type":"POST_END_WRAPPER","start":end_pos,"end":len(text),"head":"PROJECT_GUTENBERG_WRAPPER"},
]
section_by_type={s["section_type"]:s for s in sections}

def section_at(pos):
    for s in sections:
        if s["start"]<=pos<s["end"]: return s
    return None

rows=[]
serial=0
def emit(level,kind,pos,line,parent="",parent_status="",notes=""):
    global serial
    serial+=1
    s=section_at(pos)
    rows.append({
      "_tmp":serial,
      "node_id":f"TMP-{serial}",
      "level":level,
      "kind":kind,
      "section_id":s["section_id"] if s else "",
      "section_type":s["section_type"] if s else "",
      "source_char_start":pos,
      "source_char_end":pos+len(line),
      "source_line":" ".join(line.strip().split()),
      "parent_id":parent,
      "parent_status":parent_status,
      "review_status":"PENDING_HUMAN_FRAME_REVIEW",
      "notes":notes,
    })
    return rows[-1]["node_id"]

add=section_by_type["ADDENDA_BODY"]
add_text=text[add["start"]:add["end"]]

NUM=r"_?\d+[a-z]?_?"
intro_re=re.compile(rf"(?mi)^\s*Introduction\s*,?\s*p{{1,2}}\.\s*{NUM}[^\n]*$")
roman_re=re.compile(
  rf"(?mi)^\s*(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?"
  rf"[IVXLCDM]+(?:\.|,)\s*[^\n]{{0,180}}?\bp{{1,2}}\.\s*{NUM}[^\n]{{0,140}}$"
)
page_re=re.compile(rf"(?mi)^\s*(?:P|PP)\.\s*{NUM}[^\n]*$")

l2=[]
seen_positions=set()
for kind,rx in [("INTRODUCTION_PAGE_HEADING",intro_re),("ROMAN_PAGE_HEADING",roman_re)]:
    for m in rx.finditer(add_text):
        pos=add["start"]+m.start()
        if pos in seen_positions: continue
        seen_positions.add(pos)
        nid=emit("L2",kind,pos,m.group(0),notes="structural top-level candidate; historical-unit validity pending review")
        l2.append((pos,nid," ".join(m.group(0).strip().split())))
l2.sort()

for m in page_re.finditer(add_text):
    pos=add["start"]+m.start()
    if pos in seen_positions: continue
    prior=[x for x in l2 if x[0]<pos]
    parent=prior[-1][1] if prior else ""
    emit("L4","BARE_PAGE_POINTER_TARGET",pos,m.group(0),parent=parent,
         parent_status="PROVISIONAL_NEAREST_PRECEDING_L2_REVIEW_REQUIRED",
         notes="explicit target unit; may be independent intervention or nested subunit")

sup=section_by_type["SUPPLEMENTARY_NOTE"]
sup_text=text[sup["start"]:sup["end"]]
temple_id=""
if re.search(r"RICHARD\s+C\.\s+TEMPLE|RICHARD\s+TEMPLE",sup_text,re.I):
    first_line=text[sup["start"]:text.find("\n",sup["start"])]
    temple_id=emit("L3","SIGNED_TEMPLE_CONTRIBUTION",sup["start"],first_line,
                   notes="responsibility-distinct contribution; contains nested and unheaded acts")
for m in page_re.finditer(sup_text):
    pos=sup["start"]+m.start()
    emit("L4","SUPPLEMENTARY_PAGE_SUBNOTE",pos,m.group(0),parent=temple_id,
         parent_status="NESTED_UNDER_L3_CONTRIBUTION",
         notes="nested page-addressed unit; not independent contributor")

# Stable IDs after source-order sort.
rows.sort(key=lambda r:(r["source_char_start"],r["_tmp"]))
counts_by_level={}
mapping={}
for r in rows:
    lvl=r["level"]; counts_by_level[lvl]=counts_by_level.get(lvl,0)+1
    new=f"{lvl}-{counts_by_level[lvl]:04d}"
    mapping[r["node_id"]]=new
    r["node_id"]=new
for r in rows:
    if r["parent_id"] in mapping: r["parent_id"]=mapping[r["parent_id"]]
    del r["_tmp"]

# Known source-audit sanity checks.
known_patterns={
 "INTRO_P6":r"Introduction\s*,?\s*p\.\s*_?6_?",
 "URUMTSI_P201":r"P\.\s*201,\s*Line\s*12",
 "CEYLON_INDENTED_ROMAN":r"XIV\.\s*,?\s*p\.\s*_?313_?",
}
coverage={}
for name,pat in known_patterns.items():
    ms=[m for m in re.finditer(pat,text,re.I) if content_start<=m.start()<bib_pos]
    if not ms:
        coverage[name]={"source_present":False,"candidate_cover":False,"nodes":[]}
        continue
    # use latest occurrence within Addenda body when source has earlier table/synopsis mentions
    m=ms[-1]
    nodes=[r["node_id"] for r in rows if r["source_char_start"]<=m.start()<=r["source_char_end"]+10]
    coverage[name]={"source_present":True,"source_char_start":m.start(),"candidate_cover":bool(nodes),"nodes":nodes}

counts={}
for r in rows:
    k=f"{r['level']}:{r['kind']}"; counts[k]=counts.get(k,0)+1

meta={
 "source_sha256":sha,
 "publication_title_start":title.start(),
 "actual_content_start":content_start,
 "sections":sections,
 "candidate_count":len(rows),
 "counts":counts,
 "known_boundary_coverage":coverage,
 "temple_page_subnote_count":sum(1 for r in rows if r["kind"]=="SUPPLEMENTARY_PAGE_SUBNOTE"),
 "l5_quotation_count_authorized":None,
 "l6_proposition_act_count_authorized":None,
 "replacement_denominator_authorized":False,
 "authority":"structural candidate map only; human frame review pending",
}

out=Path("experiments/deepening_v1/results")
out.mkdir(parents=True,exist_ok=True)
with (out/"hierarchical_frame_candidates_v2.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
(out/"hierarchical_frame_meta_v2.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_HIERARCHICAL_FRAME_V2")
print("source_sha256="+sha)
print("PUBLICATION_TITLE_START="+str(title.start()))
print("ACTUAL_CONTENT_START="+str(content_start))
for s in sections:
    print(f"SECTION,{s['section_id']},{s['section_type']},{s['start']},{s['end']}")
for k,v in sorted(counts.items()):
    print(f"COUNT,{k},{v}")
for k,v in coverage.items():
    print(f"COVER,{k},source_present={int(v.get('source_present',False))},candidate_cover={int(v.get('candidate_cover',False))},nodes={'|'.join(v.get('nodes',[]))}")
print("TEMPLE_PAGE_SUBNOTE_COUNT="+str(meta["temple_page_subnote_count"]))
print("CANDIDATE_COUNT="+str(len(rows)))
print("L5_COUNT_AUTHORIZED=0")
print("L6_COUNT_AUTHORIZED=0")
print("REPLACEMENT_DENOMINATOR_AUTHORIZED=0")
