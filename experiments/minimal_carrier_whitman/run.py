from __future__ import annotations
import collections
import hashlib
import itertools
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="25a00b7ebbdbc5246fce65a333bc761a5c22dad4"
PATH="source/authority/anc.02134.xml"
URL=f"https://raw.githubusercontent.com/whitmanarchive/whitman-LG_1855_variorum/{COMMIT}/{PATH}"
NS={"tei":"http://www.tei-c.org/ns/1.0"}

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=30) as r:
    raw=r.read()

root=ET.fromstring(raw)
records=[]
by_local=collections.defaultdict(set)

for g in root.findall(".//tei:linkGrp[@type='relation']",NS):
    ms_file=g.attrib.get("corresp")
    for link in g.findall("./tei:link",NS):
        parts=link.attrib.get("target","").split()
        if len(parts)!=2:
            continue
        p,m=parts
        c=link.attrib.get("cert")
        records.append((p,ms_file,m,c))
        by_local[m].add(ms_file)

reused_local={m:fs for m,fs in by_local.items() if len(fs)>1}

carriers=("PRINT_LOCUS","MS_FILE","MS_LOCUS","CERTAINTY")
sufficient=[]
for k in range(len(carriers)+1):
    for comb in itertools.combinations(carriers,k):
        S=set(comb)
        ok={"PRINT_LOCUS","MS_FILE","MS_LOCUS"} <= S
        if ok:
            sufficient.append(frozenset(S))

minimal=[]
for S in sufficient:
    if not any(T < S for T in sufficient):
        minimal.append(S)

print("MC_WW_01_ENDPOINT_CARRIERS")
print("sha256="+hashlib.sha256(raw).hexdigest())
print("records="+str(len(records)))
print("reused_ms_local_ids_across_files="+str(len(reused_local)))
print("CERTAINTY_IN_ENDPOINT_OUTPUT=0")
for S in sorted(sufficient,key=lambda z:(len(z),sorted(z))):
    print("SUFFICIENT,"+"+".join(sorted(S)))
for S in sorted(minimal,key=lambda z:(len(z),sorted(z))):
    print("MINIMAL,"+"+".join(sorted(S)))

assert records
assert reused_local
assert minimal==[frozenset({"PRINT_LOCUS","MS_FILE","MS_LOCUS"})]
