from __future__ import annotations
import copy
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
projected=copy.deepcopy(root)

before=[]
for x in root.findall(".//tei:linkGrp[@type='relation']/tei:link",NS):
    before.append((x.attrib.get("target"),x.attrib.get("cert")))

removed=0
for x in projected.findall(".//tei:linkGrp[@type='relation']/tei:link",NS):
    if "cert" in x.attrib:
        del x.attrib["cert"]
        removed+=1

after=[]
for x in projected.findall(".//tei:linkGrp[@type='relation']/tei:link",NS):
    after.append((x.attrib.get("target"),x.attrib.get("cert")))

groups_before=[g.attrib.get("corresp") for g in root.findall(".//tei:linkGrp[@type='relation']",NS)]
groups_after=[g.attrib.get("corresp") for g in projected.findall(".//tei:linkGrp[@type='relation']",NS)]

assert [t for t,c in before]==[t for t,c in after]
assert groups_before==groups_after
assert len(before)==len(after)
assert removed==len(before)
assert all(c is None for t,c in after)

print("WHITMAN_X2B_CERT_PROJECTION")
print("native_sha256="+hashlib.sha256(raw).hexdigest())
print("links="+str(len(before)))
print("cert_attributes_removed="+str(removed))
print("targets_changed=0")
print("group_corresp_changed=0")
print("WW_LINK_STRUCTURAL_STATE=PRESERVED")
print("WW_CERTAINTY_EXPLICIT_STATE=REMOVED")
print("HUMAN_REJUDGMENT=NOT_TESTED")
