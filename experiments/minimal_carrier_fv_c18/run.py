from __future__ import annotations
import collections
import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET

COMMIT="5a208f869ff1213defa000e3181d5315a072a15f"
PATH="collationChunks/C18/output/Collation_C18-complete.xml"
URL=f"https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{COMMIT}/{PATH}"
EXPECTED_BLOB="bca0548912ab1d7b2676360d33a6468290296d7e"

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read()

def local(tag):
    return tag.rsplit("}",1)[-1]

def norm_text(e):
    return " ".join("".join(e.itertext()).split())

def wits(e):
    raw=e.attrib.get("wit","").strip()
    return tuple(sorted(x for x in raw.split() if x))

def canon(groups):
    gs=[]
    for g in groups:
        s=tuple(sorted(set(g)))
        if s:
            gs.append(s)
    return tuple(sorted(gs))

raw=fetch()
root=ET.fromstring(raw)
apps=[e for e in root.iter() if local(e.tag)=="app"]

native=[]
text_based=[]
multi=0
mismatch=[]
all_witnesses=set()

for ai,app in enumerate(apps):
    native_groups=[]
    readings=[]
    for child in list(app):
        ct=local(child.tag)
        if ct=="rdgGrp":
            gw=[]
            for rdg in child.iter():
                if local(rdg.tag)!="rdg":
                    continue
                ids=wits(rdg)
                gw.extend(ids)
                all_witnesses.update(ids)
                readings.append((ids,norm_text(rdg)))
            if gw:
                native_groups.append(gw)
        elif ct=="rdg":
            ids=wits(child)
            all_witnesses.update(ids)
            readings.append((ids,norm_text(child)))
            native_groups.append(list(ids))

    n=canon(native_groups)
    native.append(n)
    if len(n)>1:
        multi+=1

    by_text=collections.defaultdict(list)
    for ids,txt in readings:
        by_text[txt].extend(ids)
    t=canon(by_text.values())
    text_based.append(t)
    if t!=n:
        mismatch.append((ai,n,t))

support = len(apps)>0 and len(all_witnesses)>0
group_sufficient=support
text_sufficient=support and not mismatch
witness_alone_sufficient=support and multi==0

mins=[]
if group_sufficient and not witness_alone_sufficient:
    mins.append("WITNESS_ID+RDGGRP_MEMBERSHIP")
if text_sufficient and not witness_alone_sufficient:
    mins.append("WITNESS_ID+READING_TEXT")

print("MC_FV_C18_MINIMAL_CARRIER")
print("sha256="+hashlib.sha256(raw).hexdigest())
print("app_units="+str(len(apps)))
print("witnesses="+"|".join(sorted(all_witnesses)))
print("multi_group_apps="+str(multi))
print("text_partition_mismatches="+str(len(mismatch)))
print("D_GROUP_SUFFICIENT="+str(int(group_sufficient)))
print("D_TEXT_SUFFICIENT="+str(int(text_sufficient)))
print("WITNESS_ID_ALONE_SUFFICIENT="+str(int(witness_alone_sufficient)))
print("MINIMAL_FAMILIES="+"|".join(mins))
if mismatch:
    for ai,n,t in mismatch[:5]:
        print(f"MISMATCH,app={ai},native={n},text={t}")

assert support
assert group_sufficient
assert multi>0
