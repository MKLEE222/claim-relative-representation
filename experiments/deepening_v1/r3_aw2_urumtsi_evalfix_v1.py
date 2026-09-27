from __future__ import annotations
import hashlib, re, urllib.request

URL="https://www.gutenberg.org/cache/epub/12410/pg12410.txt"
EXPECTED="c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c"
IDS=[201,200,202]

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read()

raw=fetch()
sha=hashlib.sha256(raw).hexdigest()
if sha!=EXPECTED: raise RuntimeError(f"source drift: {sha}")
text=raw.decode("utf-8",errors="replace")

m=re.search(r"SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE",text,re.I)
if not m: raise RuntimeError("Addenda boundary not found")
start=m.start()
stops=[]
for pat in [r"\nBIBLIOGRAPHY\b",r"\nSUPPLEMENTARY NOTE\b",r"\nINDEX\b"]:
    z=re.search(pat,text[start:],re.I)
    if z: stops.append(start+z.start())
stop=min(stops) if stops else len(text)
region=text[start:stop]

lines=region.splitlines()
pointer_units=[]
for i,line in enumerate(lines):
    s=line.strip()
    if not s: continue
    if re.match(r"^(?:[IVXLCDM]+(?:\.|,)\s*)?(?:P|PP)\.\s*\d+",s,re.I):
        context=" ".join(x.strip() for x in lines[i:i+5] if x.strip())
        pointer_units.append({"line_index":i,"head":s,"context":context})

def page_match(head,n):
    mm=re.search(r"\b(?:P|PP)\.\s*([^\n]+)",head,re.I)
    if not mm: return False
    return n in [int(x) for x in re.findall(r"\d+",mm.group(1))]

def normalize_eval(s):
    return s.replace("_","")

def is_target(u):
    s=normalize_eval(u["context"])
    return bool(re.search(r"\bfounded\b.*\bfound\b|\bfound\b.*\bfounded\b",s,re.I))

print("R3_AW2_URUMTSI_NATIVE_POINTER_REPAIR_EVALFIX")
print("candidate_generation_changed=0")
print("identifiers=201|200|202")
for n in IDS:
    hits=[u for u in pointer_units if page_match(u["head"],n)]
    target=[u for u in hits if is_target(u)]
    print(",".join(["RESULT",f"page={n}",f"matched_units={len(hits)}",f"target_units={len(target)}",f"target_in_set={int(bool(target))}"]))
    for j,u in enumerate(hits,1):
        print(f"CAND,page={n},ordinal={j},line={u['line_index']},head="+u["head"].replace(",",";"))

correct=[u for u in pointer_units if page_match(u["head"],201)]
sham200=[u for u in pointer_units if page_match(u["head"],200)]
sham202=[u for u in pointer_units if page_match(u["head"],202)]
ok201=any(is_target(u) for u in correct)
ok200=any(is_target(u) for u in sham200)
ok202=any(is_target(u) for u in sham202)
print(f"CORRECT_RECOVERS_TARGET={int(ok201)}")
print(f"SHAM_200_RECOVERS_TARGET={int(ok200)}")
print(f"SHAM_202_RECOVERS_TARGET={int(ok202)}")
print(f"SELECTIVE_REPAIR_PASS={int(ok201 and not ok200 and not ok202)}")
print("AW1_LATER_LAYER_CANDIDATES=482")
print("AW1_URUMTSI_RANK=65")
