from __future__ import annotations
import copy
import hashlib
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="502eca65120dd6189ceaf41d4e5017775e6e4677"
PATH="xml/macrogenesis/wa/15_2/I.xml"
URL=f"https://raw.githubusercontent.com/faustedition/faust-xml/{COMMIT}/{PATH}"
NS={"f":"http://www.faustedition.net/ns"}

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=30) as r:
    raw=r.read()

root=ET.fromstring(raw)

def signature(r):
    out=[]
    for rel in r.findall("./f:relation",NS):
        items=tuple(x.attrib.get("uri") for x in rel.findall("./f:item",NS))
        src=rel.find("./f:source",NS)
        out.append((
            rel.attrib.get("name"),
            items,
            None if src is None else src.attrib.get("uri"),
            None if src is None else " ".join((src.text or "").split())
        ))
    return out

base=signature(root)

loc=copy.deepcopy(root)
for src in loc.findall("./f:relation/f:source",NS):
    src.text=None
loc_sig=signature(loc)

strip=copy.deepcopy(root)
for rel in strip.findall("./f:relation",NS):
    src=rel.find("./f:source",NS)
    if src is not None:
        rel.remove(src)
strip_sig=signature(strip)

assert [(n,i) for n,i,u,l in base]==[(n,i) for n,i,u,l in loc_sig]==[(n,i) for n,i,u,l in strip_sig]
assert [u for n,i,u,l in base]==[u for n,i,u,l in loc_sig]
assert all(l is None or l=="" for n,i,u,l in loc_sig)
assert all(u is None and l is None for n,i,u,l in strip_sig)

print("FAUST_X3B_SOURCE_LOCATOR_PROJECTION")
print("native_sha256="+hashlib.sha256(raw).hexdigest())
print("relations="+str(len(base)))
print("ordered_item_sequences_changed=0")
print("X3B_L_SOURCE_URI_CHANGED=0")
print("X3B_L_SOURCE_LOCATORS_REMOVED="+str(sum(1 for n,i,u,l in base if l)))
print("X3B_S_RELATION_LOCAL_SOURCES_REMOVED="+str(sum(1 for n,i,u,l in base if u)))
print("FA_TEMPORAL_STRUCTURAL_STATE=PRESERVED")
print("FA_SOURCE_WORK_UNDER_X3B_L=PRESERVED")
print("FA_SOURCE_LOCATOR_UNDER_X3B_L=REMOVED")
print("FA_SOURCE_WORK_UNDER_X3B_S=CONTEXTUAL_RECOVERY_NOT_TESTED")
