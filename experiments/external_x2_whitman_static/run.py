from __future__ import annotations
import collections
import hashlib
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="25a00b7ebbdbc5246fce65a333bc761a5c22dad4"
PATH="source/authority/anc.02134.xml"
URL=f"https://raw.githubusercontent.com/whitmanarchive/whitman-LG_1855_variorum/{COMMIT}/{PATH}"

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=30) as r:
    raw=r.read()

root=ET.fromstring(raw)
ns={"tei":"http://www.tei-c.org/ns/1.0"}

groups=root.findall(".//tei:linkGrp[@type='relation']",ns)
links=root.findall(".//tei:linkGrp[@type='relation']/tei:link",ns)

cert=collections.Counter((x.attrib.get("cert") or "MISSING") for x in links)
mixed=0
group_sizes=[]
target_shapes=collections.Counter()
missing_target=0

for g in groups:
    glinks=g.findall("./tei:link",ns)
    levels={x.attrib.get("cert") or "MISSING" for x in glinks}
    if len(levels)>1:
        mixed+=1
    group_sizes.append(len(glinks))

for x in links:
    target=x.attrib.get("target","")
    if not target:
        missing_target+=1
    parts=target.split()
    target_shapes[len(parts)]+=1

print("WHITMAN_X2A_NATIVE_RELATION_AUDIT")
print("external_commit="+COMMIT)
print("sha256="+hashlib.sha256(raw).hexdigest())
print("relation_groups="+str(len(groups)))
print("links="+str(len(links)))
print("certainty="+"|".join(f"{k}:{v}" for k,v in sorted(cert.items())))
print("mixed_certainty_groups="+str(mixed))
print("group_size_min="+str(min(group_sizes) if group_sizes else 0))
print("group_size_max="+str(max(group_sizes) if group_sizes else 0))
print("target_token_shapes="+"|".join(f"{k}:{v}" for k,v in sorted(target_shapes.items())))
print("missing_targets="+str(missing_target))

assert cert["high"]>0
assert cert["low"]>0
assert mixed>0
assert missing_target==0
print("X2A_EXPLICIT_RELATION=PASS")
print("X2A_NATIVE_CERTAINTY_VARIATION=PASS")
print("X2A_RELATION_WITHOUT_CERTAINTY_PROJECTION=ELIGIBLE_FOR_LATER_TEST")
