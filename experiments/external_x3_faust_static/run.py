from __future__ import annotations
import collections
import hashlib
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="502eca65120dd6189ceaf41d4e5017775e6e4677"
PATH="xml/macrogenesis/wa/15_2/I.xml"
URL=f"https://raw.githubusercontent.com/faustedition/faust-xml/{COMMIT}/{PATH}"

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=30) as r:
    raw=r.read()

root=ET.fromstring(raw)
ns={"f":"http://www.faustedition.net/ns"}
rels=root.findall("./f:relation",ns)

names=collections.Counter()
source_uris=collections.Counter()
source_locators=collections.Counter()
item_sizes=collections.Counter()
item_uris=collections.Counter()
missing_source=0
missing_items=0

for rel in rels:
    names[rel.attrib.get("name","MISSING")]+=1
    src=rel.find("./f:source",ns)
    if src is None or not src.attrib.get("uri"):
        missing_source+=1
    else:
        source_uris[src.attrib["uri"]]+=1
        locator=" ".join((src.text or "").split())
        source_locators[locator or "EMPTY"]+=1
    items=rel.findall("./f:item",ns)
    item_sizes[len(items)]+=1
    if len(items)<2:
        missing_items+=1
    for it in items:
        item_uris[it.attrib.get("uri","MISSING")]+=1

print("FAUST_X3A_SOURCE_QUALIFIED_TEMPORAL_AUDIT")
print("external_commit="+COMMIT)
print("sha256="+hashlib.sha256(raw).hexdigest())
print("relations="+str(len(rels)))
print("relation_names="+"|".join(f"{k}:{v}" for k,v in sorted(names.items())))
print("distinct_source_uris="+str(len(source_uris)))
print("source_uris="+"|".join(sorted(source_uris)))
print("distinct_source_locators="+str(len(source_locators)))
print("item_count_distribution="+"|".join(f"{k}:{v}" for k,v in sorted(item_sizes.items())))
print("distinct_item_uris="+str(len(item_uris)))
print("missing_source="+str(missing_source))
print("relations_with_fewer_than_2_items="+str(missing_items))

assert len(rels)>0
assert missing_source==0
assert missing_items==0
assert names["temp-pre"]>0
assert any(k>2 for k in item_sizes)
print("X3A_SOURCE_BINDING=PASS")
print("X3A_TEMPORAL_RELATION=PASS")
print("X3A_MULTI_ITEM_ORDER_CONSTRAINTS=PASS")
print("X3A_UNIQUE_HISTORICAL_ORDER=NOT_CLAIMED")
