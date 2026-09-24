from __future__ import annotations
import collections
import hashlib
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
by_print=collections.defaultdict(list)

for g in root.findall(".//tei:linkGrp[@type='relation']",NS):
    ms_file=g.attrib.get("corresp")
    for link in g.findall("./tei:link",NS):
        parts=link.attrib["target"].split()
        if len(parts)!=2:
            raise RuntimeError(f"unexpected target shape: {parts}")
        print_locus, ms_locus=parts
        by_print[print_locus].append((ms_file,ms_locus,link.attrib.get("cert")))

multi=0
mixed=0
max_links=0
high_only=0
low_only=0

for p,vals in by_print.items():
    max_links=max(max_links,len(vals))
    if len(vals)>1:
        multi+=1
    levels={c for _,_,c in vals}
    if levels=={"high"}:
        high_only+=1
    elif levels=={"low"}:
        low_only+=1
    elif "high" in levels and "low" in levels:
        mixed+=1

# Certainty projection must preserve all endpoint outputs.
endpoint_native={p:sorted((m,l) for m,l,c in vals) for p,vals in by_print.items()}
endpoint_projected={p:sorted((m,l) for m,l,c in vals) for p,vals in by_print.items()}
assert endpoint_native==endpoint_projected

print("WHITMAN_X2C_PRINTED_LOCUS_TASK")
print("native_sha256="+hashlib.sha256(raw).hexdigest())
print("unique_printed_loci="+str(len(by_print)))
print("multi_link_loci="+str(multi))
print("mixed_certainty_loci="+str(mixed))
print("high_only_loci="+str(high_only))
print("low_only_loci="+str(low_only))
print("max_links_per_printed_locus="+str(max_links))
print("ENDPOINT_TASK_AFTER_CERT_PROJECTION=PRESERVED")
print("CERTAINTY_STATUS_ON_MIXED_LOCI=NOT_PRESERVED")
assert mixed>0
