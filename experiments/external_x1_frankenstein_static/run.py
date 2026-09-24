from __future__ import annotations
import collections
import hashlib
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="5a208f869ff1213defa000e3181d5315a072a15f"
BASE=f"https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{COMMIT}/"

INPUTS={
    "f1818":"collationChunks/C16/input/1818_fullFlat_C16.xml",
    "f1823":"collationChunks/C16/input/1823_fullFlat_C16.xml",
    "f1831":"collationChunks/C16/input/1831_fullFlat_C16.xml",
    "fThomas":"collationChunks/C16/input/Thomas_fullFlat_C16.xml",
    "fMS":"collationChunks/C16/input/msColl_C16.xml",
}
OUTPUT="collationChunks/C16/output/Collation_C16-complete.xml"

SELECTED={"surface","zone","lb","milestone","pb","p","head","hi","mod","del","sga-add","longToken","anchor"}

def fetch(path):
    req=urllib.request.Request(BASE+path,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def local(tag):
    return tag.rsplit("}",1)[-1]

def elem_counts(data):
    root=ET.fromstring(data)
    c=collections.Counter(local(e.tag) for e in root.iter())
    return c

raw_inputs={k:fetch(p) for k,p in INPUTS.items()}
raw_out=fetch(OUTPUT)

print("FRANKENSTEIN_X1A_STATIC_AUDIT")
print("external_commit="+COMMIT)

all_tagsets={}
for wit,data in raw_inputs.items():
    c=elem_counts(data)
    tagset={k for k,v in c.items() if v}
    all_tagsets[wit]=tagset
    selected="|".join(f"{k}:{c[k]}" for k in sorted(SELECTED) if c[k])
    print(",".join([
        "INPUT",wit,
        f"bytes={len(data)}",
        f"sha256={hashlib.sha256(data).hexdigest()}",
        f"distinct_elements={len(tagset)}",
        f"selected={selected}"
    ]))

intersection=set.intersection(*all_tagsets.values())
union=set.union(*all_tagsets.values())
print("TAGSET_INTERSECTION="+("|".join(sorted(intersection))))
print("TAGSET_UNION_SIZE="+str(len(union)))

root=ET.fromstring(raw_out)
apps=[e for e in root.iter() if local(e.tag)=="app"]
rdgg=[e for e in root.iter() if local(e.tag)=="rdgGrp"]
rdgs=[e for e in root.iter() if local(e.tag)=="rdg"]

wits=collections.Counter()
coverage=collections.Counter()
for app in apps:
    present=set()
    for e in app.iter():
        if local(e.tag)=="rdg":
            wit=e.attrib.get("wit")
            if wit:
                present.add(wit)
                wits[wit]+=1
    coverage[len(present)]+=1

out_text=raw_out.decode("utf-8",errors="replace")
escaped_markers={}
for marker in ["&lt;pb","&lt;lb","&lt;milestone","&lt;surface","&lt;mod","&lt;del","&lt;sga-add","&lt;longToken","&lt;anchor"]:
    escaped_markers[marker]=out_text.count(marker)

print("OUTPUT_BYTES="+str(len(raw_out)))
print("OUTPUT_SHA256="+hashlib.sha256(raw_out).hexdigest())
print("APP_COUNT="+str(len(apps)))
print("RDGGRP_COUNT="+str(len(rdgg)))
print("RDG_COUNT="+str(len(rdgs)))
print("WITNESSES="+"|".join(sorted(wits)))
print("APP_WITNESS_COVERAGE="+"|".join(f"{k}:{coverage[k]}" for k in sorted(coverage)))
print("ESCAPED_SOURCE_MARKERS="+"|".join(f"{k}:{v}" for k,v in escaped_markers.items()))

# Scientific invariants for this static audit
assert set(wits) >= {"f1818","f1823","f1831","fThomas","fMS"}
assert len(apps)>0 and len(rdgs)>0
assert all(len(all_tagsets[w])>0 for w in all_tagsets)
assert "surface" in all_tagsets["fMS"]
assert "surface" not in all_tagsets["f1818"]
assert escaped_markers["&lt;pb"]>0
assert escaped_markers["&lt;lb"]>0

print("X1A_STRUCTURE_HETEROGENEITY=PASS")
print("X1A_COMMON_ALIGNMENT_APPARATUS=PASS")
print("X1A_SOURCE_MARKER_CARRYTHROUGH=PASS")
print("X1A_GLOBAL_INFORMATION_PRESERVATION=NOT_TESTED")
