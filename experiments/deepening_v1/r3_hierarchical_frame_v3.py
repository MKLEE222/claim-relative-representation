from __future__ import annotations
import csv, hashlib, json, re, urllib.request
from pathlib import Path

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"
MONTHS=r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r: return r.read()

def exclusion_reason(head):
    h=head.lstrip()
    if re.search(rf"^[IVXLCDM]+\.,\s*(?:{MONTHS}|(?:18|19)\d{{2}})\b",h,re.I): return "F1_EXTERNAL_PERIODICAL_ISSUE"
    if re.search(r"^[A-Z]\.\s*Chap\.",h,re.I): return "F2_LETTERED_SOURCE_SUBITEM"
    if re.search(r"\bp{1,2}\.\s*[^,]{0,40}\),",h,re.I): return "F3_CITATION_CONTINUATION"
    if re.search(r"^[IVXLCDM]+\.,\s*pp?\.\s*[^\n]{0,90}\bin\s+(?:Mr\.|Dr\.|Prof\.|Sir\s+\w+['’]s|[A-Z][a-z]+['’]s)\s+paper\b",h,re.I): return "F4_EXPLICIT_NAMED_PAPER_PAGE"
    return ""

raw=fetch(); sha=hashlib.sha256(raw).hexdigest()
if sha!=EXPECTED: raise RuntimeError(f"source drift: {sha}")
text=raw.decode("utf-8",errors="replace")

title=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
if not title: raise RuntimeError("title missing")
cms=list(re.finditer(r"(?mi)^\s*MARCO\s+POLO\s+AND\s+HIS\s+BOOK\.\s*\n\s*INTRODUCTORY\s+NOTICES\.\s*$",text[title.end():]))
if not cms: raise RuntimeError("content start missing")
content_start=title.end()+cms[-1].start()

def occ(pattern):
    return [(content_start+m.start(),m.group(0).strip()) for m in re.finditer(pattern,text[content_start:],re.I|re.M)]

bib_occ=occ(r"^\s*BIBLIOGRAPHY\s+OF\s+MARCO\s+POLO['’]S\s+BOOK(?:\.\[?\d*\]?|\.)?\s*$")
sup_occ=occ(r"^\s*SUPPLEMENTARY\s+NOTE\.\s*$")
idx_occ=occ(r"^\s*INDEX\s*$")
if not (bib_occ and sup_occ and idx_occ): raise RuntimeError("terminal section markers missing")
index_pos=idx_occ[-1][0]
supp_pos,supp_head=[x for x in sup_occ if x[0]<index_pos][-1]
bib_pos,bib_head=[x for x in bib_occ if x[0]<supp_pos][-1]
end_m=re.search(r"(?mi)^\s*\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK.*$",text[index_pos:])
end_pos=index_pos+end_m.start() if end_m else len(text)

sections=[
 {"section_id":"L1-01","section_type":"ADDENDA_BODY","start":content_start,"end":bib_pos},
 {"section_id":"L1-02","section_type":"BIBLIOGRAPHY","start":bib_pos,"end":supp_pos},
 {"section_id":"L1-03","section_type":"SUPPLEMENTARY_NOTE","start":supp_pos,"end":index_pos},
 {"section_id":"L1-04","section_type":"INDEX","start":index_pos,"end":end_pos},
 {"section_id":"L1-05","section_type":"POST_END_WRAPPER","start":end_pos,"end":len(text)},
]
def section_at(pos):
    return next((s for s in sections if s["start"]<=pos<s["end"]),None)

rows=[]; excluded=[]; temp=0
def emit(level,kind,pos,line,parent="",parent_status="",notes=""):
    global temp
    temp+=1
    s=section_at(pos)
    rec={
      "_tmp":temp,"node_id":f"TMP-{temp}","level":level,"kind":kind,
      "section_id":s["section_id"] if s else "","section_type":s["section_type"] if s else "",
      "source_char_start":pos,"source_char_end":pos+len(line),
      "source_line":" ".join(line.strip().split()),
      "parent_id":parent,"parent_status":parent_status,
      "review_status":"PENDING_HUMAN_FRAME_REVIEW","notes":notes,
    }
    rows.append(rec); return rec["node_id"]

NUM=r"_?\d+[a-z]?_?"
add=sections[0]; add_text=text[add["start"]:add["end"]]
intro_re=re.compile(rf"(?mi)^\s*Introduction\s*,?\s*p{{1,2}}\.\s*{NUM}[^\n]*$")
roman_re=re.compile(rf"(?mi)^\s*(?:BOOK\s+[A-Z]+\.\s*)?(?:PART\s+[IVXLCDM]+\.\s*)?[IVXLCDM]+(?:\.|,)\s*[^\n]{{0,180}}?\bp{{1,2}}\.\s*{NUM}[^\n]{{0,140}}$")
# Case-sensitive source-authored page target heading.
upper_page_re=re.compile(rf"(?m)^\s*(?:P|Pp)\.\s*{NUM}[^\n]*$")

l2=[]; occupied=set()
for m in intro_re.finditer(add_text):
    pos=add["start"]+m.start(); occupied.add(pos)
    nid=emit("L2","INTRODUCTION_PAGE_HEADING",pos,m.group(0),notes="source structural candidate")
    l2.append((pos,nid))

for m in roman_re.finditer(add_text):
    pos=add["start"]+m.start(); line=m.group(0)
    why=exclusion_reason(" ".join(line.strip().split()))
    if why:
        excluded.append({"source_char_start":pos,"source_line":" ".join(line.strip().split()),"reason":why})
        continue
    occupied.add(pos)
    nid=emit("L2","ROMAN_PAGE_HEADING",pos,line,notes="source structural candidate after F1-F4 exclusion")
    l2.append((pos,nid))
l2.sort()

for m in upper_page_re.finditer(add_text):
    pos=add["start"]+m.start()
    if pos in occupied: continue
    prior=[x for x in l2 if x[0]<pos]
    parent=prior[-1][1] if prior else ""
    emit("L4","UPPERCASE_EXPLICIT_PAGE_TARGET",pos,m.group(0),parent=parent,
         parent_status="PROVISIONAL_NEAREST_PRECEDING_L2_REVIEW_REQUIRED",
         notes="explicit page-addressed target; independence level requires human review")

sup=sections[2]; sup_text=text[sup["start"]:sup["end"]]
temple_id=""
if re.search(r"RICHARD\s+C\.\s+TEMPLE|RICHARD\s+TEMPLE",sup_text,re.I):
    temple_id=emit("L3","SIGNED_TEMPLE_CONTRIBUTION",sup["start"],text[sup["start"]:text.find("\n",sup["start"])],
                   notes="responsibility wrapper; not pooled with nested subnotes")
for m in upper_page_re.finditer(sup_text):
    pos=sup["start"]+m.start()
    emit("L4","SUPPLEMENTARY_PAGE_SUBNOTE",pos,m.group(0),parent=temple_id,
         parent_status="NESTED_UNDER_L3_CONTRIBUTION",
         notes="source-authored uppercase page-addressed subnote")

# Stable IDs.
rows.sort(key=lambda r:(r["source_char_start"],r["_tmp"]))
counter={}; mp={}
for r in rows:
    counter[r["level"]]=counter.get(r["level"],0)+1
    new=f"{r['level']}-{counter[r['level']]:04d}"; mp[r["node_id"]]=new; r["node_id"]=new
for r in rows:
    if r["parent_id"] in mp: r["parent_id"]=mp[r["parent_id"]]
    del r["_tmp"]

# Sanity checks against candidate source lines rather than arbitrary prose occurrences.
def line_has(kind,pat):
    return [r["node_id"] for r in rows if r["kind"]==kind and re.search(pat,r["source_line"],re.I)]
coverage={
 "INTRO_P6":line_has("INTRODUCTION_PAGE_HEADING",r"Introduction\s*,?\s*p\.\s*_?6_?"),
 "URUMTSI_P201":line_has("UPPERCASE_EXPLICIT_PAGE_TARGET",r"P\.\s*201,\s*Line\s*12"),
 "CEYLON_INDENTED_ROMAN":line_has("ROMAN_PAGE_HEADING",r"XIV\.\s*,?\s*p\.\s*_?313_?"),
}
counts={}
for r in rows:
    k=f"{r['level']}:{r['kind']}"; counts[k]=counts.get(k,0)+1
exc={}
for e in excluded: exc[e["reason"]]=exc.get(e["reason"],0)+1

l2_count=sum(1 for r in rows if r["level"]=="L2")
addenda_l4=sum(1 for r in rows if r["kind"]=="UPPERCASE_EXPLICIT_PAGE_TARGET")
temple_l4=sum(1 for r in rows if r["kind"]=="SUPPLEMENTARY_PAGE_SUBNOTE")
span_candidates=l2_count+addenda_l4+temple_l4
node_count=len(rows)

valid=all(bool(v) for v in coverage.values()) and temple_l4==10 and sum(exc.values())==5

meta={
 "source_sha256":sha,
 "sections":sections,
 "counts":counts,
 "excluded_roman_false_heads":exc,
 "known_boundary_coverage":coverage,
 "l2_count":l2_count,
 "addenda_explicit_target_l4_count":addenda_l4,
 "temple_nested_l4_count":temple_l4,
 "hierarchical_span_candidate_count":span_candidates,
 "structural_node_count_including_l3_wrapper":node_count,
 "structural_sanity_pass":valid,
 "l5_quotation_count_authorized":None,
 "l6_proposition_act_count_authorized":None,
 "replacement_denominator_authorized":False,
}

out=Path("experiments/deepening_v1/results"); out.mkdir(parents=True,exist_ok=True)
with (out/"hierarchical_frame_candidates_v3.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with (out/"hierarchical_frame_excluded_v3.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["source_char_start","source_line","reason"]); w.writeheader(); w.writerows(excluded)
(out/"hierarchical_frame_meta_v3.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

print("R3_HIERARCHICAL_FRAME_V3")
for k,v in sorted(counts.items()): print(f"COUNT,{k},{v}")
for k,v in sorted(exc.items()): print(f"EXCLUDE,{k},{v}")
for k,v in coverage.items(): print(f"COVER,{k},pass={int(bool(v))},nodes={'|'.join(v)}")
print("L2_COUNT="+str(l2_count))
print("ADDENDA_EXPLICIT_TARGET_L4_COUNT="+str(addenda_l4))
print("TEMPLE_NESTED_L4_COUNT="+str(temple_l4))
print("HIERARCHICAL_SPAN_CANDIDATE_COUNT="+str(span_candidates))
print("STRUCTURAL_NODE_COUNT_INCLUDING_L3_WRAPPER="+str(node_count))
print("STRUCTURAL_SANITY_PASS="+str(int(valid)))
print("L5_COUNT_AUTHORIZED=0")
print("L6_COUNT_AUTHORIZED=0")
print("REPLACEMENT_DENOMINATOR_AUTHORIZED=0")
