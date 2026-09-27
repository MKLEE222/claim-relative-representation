from __future__ import annotations

import csv, hashlib, json, re, time, urllib.request
from pathlib import Path

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"
BATCH_SIZE=20

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

# Same structural exclusion contract as R3_FRAME_REFINEMENT_PROTOCOL v1.
MONTHS=r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
def exclusion_reason(head):
    if re.search(rf"^[IVXLCDM]+\.,\s*(?:{MONTHS}|(?:18|19)\d{{2}})\b",head,re.I):
        return "F1_EXTERNAL_PERIODICAL_ISSUE"
    if re.search(r"^[A-Z]\.\s*Chap\.",head,re.I):
        return "F2_LETTERED_SOURCE_SUBITEM"
    if re.search(r"\bp{1,2}\.\s*[^,]{0,40}\),",head,re.I):
        return "F3_CLOSING_PAREN_CITATION_CONTINUATION"
    if re.search(r"^[IVXLCDM]+\.,\s*pp?\.\s*[^\n]{0,90}\bin\s+(?:(?:Mr\.|Dr\.|Prof\.)\s+[A-Z][A-Za-z'’.-]+|Sir\s+[A-Z][A-Za-z'’.-]+|[A-Z][A-Za-z'’.-]+['’]s)\s+paper\b",head,re.I):
        return "F4_EXPLICIT_NAMED_PAPER_PAGE"
    return ""

raws=[]
for i,m in enumerate(heads):
    s=m.start(); e=heads[i+1].start() if i+1<len(heads) else len(region)
    raws.append({"raw_id":f"YC1920-{i+1:04d}","head":m.group("head").strip(),"block":region[s:e].strip(),"source_start":start+s,"source_end":start+e})

entries=[]
exclusions=[]
for r in raws:
    reason=exclusion_reason(r["head"])
    if reason:
        exclusions.append({"raw_id":r["raw_id"],"head":r["head"],"reason":reason,"merged_into":entries[-1]["entry_id"] if entries else ""})
        if entries:
            entries[-1]["text_raw"] += "\n"+r["block"]
            entries[-1]["source_end"]=r["source_end"]
            entries[-1]["merged"].append(r["raw_id"])
        continue
    entries.append({
        "entry_id":f"YC1920E-{len(entries)+1:04d}",
        "root_raw_id":r["raw_id"],"head":r["head"],
        "source_start":r["source_start"],"source_end":r["source_end"],
        "merged":[],"text_raw":r["block"],
    })

for e in entries:
    e["entry_text"]=" ".join(e.pop("text_raw").split())
    e["entry_sha256"]=hashlib.sha256(e["entry_text"].encode()).hexdigest()
    e["merged_raw_ids"]="|".join(e.pop("merged"))

out=Path("experiments/deepening_v1/results/r3_coding_batches_v1")
out.mkdir(parents=True,exist_ok=True)
manifest=[]
for bi in range(0,len(entries),BATCH_SIZE):
    rows=entries[bi:bi+BATCH_SIZE]
    batch_id=f"B{bi//BATCH_SIZE+1:02d}"
    p=out/f"{batch_id}.json"
    payload={
        "batch_id":batch_id,
        "source_sha256":sha,
        "entry_count":len(rows),
        "relation_ontology_version":"R3 relation ontology amendment v2",
        "entries":rows,
        "coding_instruction":"Code entry then intervention acts. Relation evidence must quote the entry. Leave unresolved when responsibility/target/relation is not explicit enough."
    }
    p.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    manifest.append({
        "batch_id":batch_id,
        "first_entry":rows[0]["entry_id"],
        "last_entry":rows[-1]["entry_id"],
        "entries":len(rows),
        "file":str(p),
        "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
    })

Path("experiments/deepening_v1/results/r3_coding_batches_v1_manifest.json").write_text(
    json.dumps({"source_sha256":sha,"total_entries":len(entries),"exclusions":exclusions,"batches":manifest},ensure_ascii=False,indent=2),encoding="utf-8"
)
print("R3_CODING_BATCHES_V1")
print("entries="+str(len(entries)))
print("exclusions="+str(len(exclusions)))
print("batches="+str(len(manifest)))
for m in manifest: print(f"BATCH,{m['batch_id']},{m['first_entry']},{m['last_entry']},{m['entries']},{m['sha256']}")
