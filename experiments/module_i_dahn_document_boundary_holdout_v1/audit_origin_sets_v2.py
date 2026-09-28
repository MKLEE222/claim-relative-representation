from __future__ import annotations

import argparse
import io
import json
import tarfile
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

UPSTREAM_REPO="FloChiff/DAHNProject"
UPSTREAM_COMMIT="e7d4a81d42ea10a3d672e5c0869f033a8c2c8149"
XML_LANG="{http://www.w3.org/XML/1998/namespace}lang"

def local(tag):
    return tag.rsplit("}",1)[-1]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"CRR-module-I-origin-audit/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r:
        return r.read()

def choose_origin_paragraph(root):
    history=next((x for x in root.iter() if local(x.tag)=="history"),None)
    if history is None:
        return None,None
    origin=next((x for x in list(history) if local(x.tag)=="origin"),None)
    if origin is None:
        return None,None
    ps=[x for x in list(origin) if local(x.tag)=="p"]
    if not ps:
        return origin,""
    for wanted in ("en","de","fr"):
        for p in ps:
            if (p.attrib.get(XML_LANG) or "").lower()==wanted:
                return p,wanted
    return ps[0],(ps[0].attrib.get(XML_LANG) or "").lower()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prefix",required=True)
    args=ap.parse_args()
    if "StaBi/Correspondence" in args.prefix:
        raise SystemExit("holdout prefix forbidden in development origin audit")

    raw=fetch(f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz")
    rows=[]
    total=0
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            parts=Path(m.name).parts
            if len(parts)<2:
                continue
            rel=str(Path(*parts[1:]))
            if not rel.startswith(args.prefix) or not rel.endswith(".xml"):
                continue
            f=tf.extractfile(m)
            if f is None:
                continue
            total+=1
            root=ET.fromstring(f.read())
            p,lang=choose_origin_paragraph(root)
            if p is None:
                continue
            ods=[x for x in p.iter() if local(x.tag)=="origDate"]
            if len(ods)>1:
                rows.append({
                    "path":rel,
                    "lang":lang,
                    "count":len(ods),
                    "paragraph":" ".join(" ".join(p.itertext()).split()),
                    "origDates":[
                        {
                            "attrs":dict(x.attrib),
                            "text":" ".join(" ".join(x.itertext()).split())
                        } for x in ods
                    ]
                })
    print(json.dumps({
        "prefix":args.prefix,
        "parsed":total,
        "multi_origdate_documents":len(rows),
        "rows":rows,
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
