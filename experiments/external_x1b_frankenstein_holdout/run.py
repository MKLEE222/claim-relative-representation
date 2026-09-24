from __future__ import annotations

import collections
import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="5a208f869ff1213defa000e3181d5315a072a15f"
BASE=f"https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{COMMIT}/"
CHUNK="C17"

INPUTS={
    "f1818":f"collationChunks/{CHUNK}/input/1818_fullFlat_{CHUNK}.xml",
    "f1823":f"collationChunks/{CHUNK}/input/1823_fullFlat_{CHUNK}.xml",
    "f1831":f"collationChunks/{CHUNK}/input/1831_fullFlat_{CHUNK}.xml",
    "fThomas":f"collationChunks/{CHUNK}/input/Thomas_fullFlat_{CHUNK}.xml",
    "fMS":f"collationChunks/{CHUNK}/input/msColl_{CHUNK}.xml",
}
OUTPUT=f"collationChunks/{CHUNK}/output/Collation_{CHUNK}-complete.xml"

MARKERS=["surface","zone","lb","pb","p","head","mod","del","sga-add","milestone","anchor"]
EXPECTED=set(INPUTS)

def fetch(path):
    req=urllib.request.Request(BASE+path,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def local(tag):
    return tag.rsplit("}",1)[-1]

def count_input(data):
    root=ET.fromstring(data)
    c=collections.Counter(local(e.tag) for e in root.iter())
    return {m:c[m] for m in MARKERS}

def count_literal_markers(text):
    out={}
    for m in MARKERS:
        out[m]=len(re.findall(r"<"+re.escape(m)+r"(?:\s|/|>)",text))
    return out

raw_inputs={w:fetch(p) for w,p in INPUTS.items()}
raw_output=fetch(OUTPUT)

input_counts={w:count_input(data) for w,data in raw_inputs.items()}

root=ET.fromstring(raw_output)
apps=[e for e in root.iter() if local(e.tag)=="app"]
rdgs=[e for e in root.iter() if local(e.tag)=="rdg"]

witness_text=collections.defaultdict(list)
coverage=collections.Counter()
for app in apps:
    present=set()
    for rdg in app.iter():
        if local(rdg.tag)!="rdg":
            continue
        wit=rdg.attrib.get("wit")
        if not wit:
            continue
        present.add(wit)
        witness_text[wit].append("".join(rdg.itertext()))
    coverage[len(present)]+=1

observed=set(witness_text)
output_counts={
    w:count_literal_markers("\n".join(witness_text.get(w,[])))
    for w in sorted(EXPECTED)
}

print("FRANKENSTEIN_X1B_C17_HOLDOUT")
print("external_commit="+COMMIT)
print("output_sha256="+hashlib.sha256(raw_output).hexdigest())
print("app_count="+str(len(apps)))
print("rdg_count="+str(len(rdgs)))
print("witnesses="+"|".join(sorted(observed)))
print("app_witness_coverage="+"|".join(f"{k}:{coverage[k]}" for k in sorted(coverage)))

all_exact=True
for w in sorted(EXPECTED):
    exact=True
    diffs=[]
    for m in MARKERS:
        a=input_counts[w][m]
        b=output_counts[w][m]
        if a!=b:
            exact=False
            diffs.append(f"{m}:{a}->{b}")
    all_exact = all_exact and exact
    print("INPUT_VECTOR,"+w+","+"|".join(f"{m}:{input_counts[w][m]}" for m in MARKERS))
    print("OUTPUT_VECTOR,"+w+","+"|".join(f"{m}:{output_counts[w][m]}" for m in MARKERS))
    print("STRUCTURE_EXACT,"+w+","+str(int(exact))+",diffs="+";".join(diffs))

align_pass = len(apps)>0 and EXPECTED.issubset(observed)

print("FV_ALIGN="+("PASS" if align_pass else "FAIL"))
print("FV_SOURCE_STRUCTURE_EXACT="+("PASS" if all_exact else "FAIL"))
print("GLOBAL_REPRESENTATION_RANKING=NOT_TESTED")

assert align_pass
