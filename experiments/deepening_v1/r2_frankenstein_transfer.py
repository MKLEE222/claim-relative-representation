from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

COMMIT="5a208f869ff1213defa000e3181d5315a072a15f"
URL=f"https://github.com/FrankensteinVariorum/collationWorkspace/archive/{COMMIT}.tar.gz"
EXCLUDE={"C16","C17","C18"}
SELECT_N=5

def local(tag):
    return tag.rsplit("}",1)[-1]

def norm_ws(x):
    return " ".join((x or "").split())

def git_blob_sha1(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii")+raw).hexdigest()

def elem_sig(e):
    return (e.tag,tuple(sorted(e.attrib.items())),norm_ws(e.text),tuple(elem_sig(c) for c in list(e)))

def xml_struct_digest(raw):
    return hashlib.sha256(repr(elem_sig(ET.fromstring(raw))).encode("utf-8")).hexdigest()

def run(cmd,cwd,timeout=1200):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError("command failed: "+" ".join(map(str,cmd))+"\nSTDOUT\n"+p.stdout[-8000:]+"\nSTDERR\n"+p.stderr[-8000:])
    return p

def target_partition(app):
    groups=[]
    for child in list(app):
        ct=local(child.tag)
        if ct=="rdgGrp":
            w=[]
            for rdg in child.iter():
                if local(rdg.tag)=="rdg":
                    w.extend((rdg.attrib.get("wit") or "").split())
            if w:
                groups.append(frozenset(w))
        elif ct=="rdg":
            w=(child.attrib.get("wit") or "").split()
            if w:
                groups.append(frozenset(w))
    return frozenset(groups)

def inner_markup(rdg):
    parts=[rdg.text or ""]
    for child in list(rdg):
        parts.append(ET.tostring(child,encoding="unicode"))
    return "".join(parts)

TAG_RE=re.compile(r"<[^>]+>")

def decoder_key(raw,mode):
    x=norm_ws(raw)
    if mode in {"STRIP_XML","STRIP_XML_CASE_AMP"}:
        x=norm_ws(TAG_RE.sub(" ",x))
    if mode=="STRIP_XML_CASE_AMP":
        x=x.casefold().replace("&"," and ")
        x=norm_ws(x)
    return x

def predicted_partition(app,mode):
    by={}
    for rdg in (e for e in app.iter() if local(e.tag)=="rdg"):
        w=(rdg.attrib.get("wit") or "").split()
        if not w:
            continue
        k=decoder_key(inner_markup(rdg),mode)
        by.setdefault(k,set()).update(w)
    return frozenset(frozenset(v) for v in by.values() if v)

def classify(target,pred):
    split=any(sum(1 for p in pred if g & p)>1 for g in target)
    merge=any(sum(1 for g in target if g & p)>1 for p in pred)
    return split,merge

def partition_signature(raw):
    root=ET.fromstring(raw)
    return [target_partition(app) for app in (e for e in root.iter() if local(e.tag)=="app")]

def descriptor_signature(raw):
    root=ET.fromstring(raw)
    out=[]
    for app in (e for e in root.iter() if local(e.tag)=="app"):
        vals=[]
        for child in list(app):
            if local(child.tag)=="rdgGrp":
                vals.append(norm_ws(child.attrib.get("n")))
        out.append(tuple(vals))
    return out

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=90) as r:
    archive=r.read()

with tempfile.TemporaryDirectory(prefix="fv_r2_transfer_") as td:
    td=Path(td)
    with tarfile.open(fileobj=io.BytesIO(archive),mode="r:gz") as tf:
        names=set(tf.getnames())
        tf.extractall(td)

    roots=[p for p in td.iterdir() if p.is_dir()]
    if len(roots)!=1:
        raise RuntimeError(f"unexpected extracted roots: {roots}")
    root=roots[0]

    # Selector inspects filenames only.
    eligible=[]
    for i in range(1,32):
        c=f"C{i:02d}"
        if c in EXCLUDE:
            continue
        needed=[
            f"{root.name}/collationChunks/{c}/input/1818_fullFlat_{c}.xml",
            f"{root.name}/collationChunks/{c}/input/1823_fullFlat_{c}.xml",
            f"{root.name}/collationChunks/{c}/input/1831_fullFlat_{c}.xml",
            f"{root.name}/collationChunks/{c}/input/Thomas_fullFlat_{c}.xml",
            f"{root.name}/collationChunks/{c}/input/msColl_{c}.xml",
            f"{root.name}/collationChunks/{c}/output/Collation_{c}-complete.xml",
        ]
        if all(x in names for x in needed):
            eligible.append(c)
    selected=eligible[:SELECT_N]
    if not selected:
        raise RuntimeError("no eligible transfer chunks")

    # One compatibility shim, identical in semantics to C18 reproduction.
    aligner=root/"python-collation/collatex/edit_graph_aligner.py"
    s=aligner.read_text(encoding="utf-8")
    s=s.replace(
        "for token_position in self.token_index.get_range_for_witness(witness.sigil):",
        "for token_position in self.token_index.get_range_for_witness(witness.sigil).intiter():"
    )
    s=s.replace(
        "for p in self.token_index.get_range_for_witness(witness.sigil):",
        "for p in self.token_index.get_range_for_witness(witness.sigil).intiter():"
    )
    aligner.write_text(s,encoding="utf-8")
    tokenindex=root/"python-collation/collatex/tokenindex.py"
    s=tokenindex.read_text(encoding="utf-8").replace(
        "return self.get_range_for_witness(witness.sigil)[0]",
        "return next(self.get_range_for_witness(witness.sigil).intiter())"
    )
    tokenindex.write_text(s,encoding="utf-8")

    jar=root/"xslt/SaxonHE12-0J/saxon-he-12.0.jar"
    results=[]
    for c in selected:
        target_path=root/f"collationChunks/{c}/output/Collation_{c}-complete.xml"
        target_raw=target_path.read_bytes()
        target_blob=git_blob_sha1(target_raw)

        input_dir=root/f"collationChunks/{c}/input"
        pre_dir=root/f"collationChunks/{c}/input-pre"
        witness_names=[
            f"1818_fullFlat_{c}.xml",
            f"1823_fullFlat_{c}.xml",
            f"1831_fullFlat_{c}.xml",
            f"Thomas_fullFlat_{c}.xml",
            f"msColl_{c}.xml",
        ]
        pinned={n:(input_dir/n).read_bytes() for n in witness_names}
        pinned_dig={n:xml_struct_digest(b) for n,b in pinned.items()}

        shutil.rmtree(pre_dir)
        shutil.rmtree(input_dir)
        pre_dir.mkdir(); input_dir.mkdir()
        run(["java","-jar",str(jar),"-xsl:xslt/preProcessing-1.xsl",f"-s:collationChunks/{c}",f"-o:collationChunks/{c}/input-pre"],root)
        run(["java","-jar",str(jar),"-xsl:xslt/preProcessing-2.xsl",f"-s:collationChunks/{c}/input-pre",f"-o:collationChunks/{c}/input"],root)
        pre_equal={n:xml_struct_digest((input_dir/n).read_bytes())==pinned_dig[n] for n in witness_names}

        published_copy=td/f"published_{c}.xml"
        published_copy.write_bytes(target_raw)
        run(["python","collate.py",c],root/"python-collation",timeout=1500)
        partway=root/f"collationChunks/{c}/output/Collation_{c}-partway.xml"
        replay=td/f"replay_{c}.xml"
        run(["java","-jar",str(jar),"-xsl:xslt/postProcessing.xsl",f"-s:collationChunks/{c}/output/Collation_{c}-partway.xml",f"-o:{replay}"],root,timeout=1500)
        replay_raw=replay.read_bytes()

        target_parts=partition_signature(target_raw)
        replay_parts=partition_signature(replay_raw)
        n=max(len(target_parts),len(replay_parts))
        native_mismatch=sum(1 for i in range(n) if (target_parts[i] if i<len(target_parts) else None)!=(replay_parts[i] if i<len(replay_parts) else None))
        target_desc=descriptor_signature(target_raw)
        replay_desc=descriptor_signature(replay_raw)
        nd=max(len(target_desc),len(replay_desc))
        desc_mismatch=sum(1 for i in range(nd) if (target_desc[i] if i<len(target_desc) else None)!=(replay_desc[i] if i<len(replay_desc) else None))

        root_target=ET.fromstring(target_raw)
        apps=[e for e in root_target.iter() if local(e.tag)=="app"]
        diag={}
        for mode in ["SERIALIZED_EQUALITY","STRIP_XML","STRIP_XML_CASE_AMP"]:
            mismatch=split=merge=both=0
            examples=[]
            for ai,app in enumerate(apps):
                t=target_partition(app); p=predicted_partition(app,mode)
                if t!=p:
                    mismatch+=1
                    sp,mg=classify(t,p)
                    split+=int(sp); merge+=int(mg); both+=int(sp and mg)
                    if len(examples)<10:
                        examples.append({"app_index":ai,"false_split":sp,"false_merge":mg,"target":[sorted(x) for x in sorted(t,key=lambda z:sorted(z))],"predicted":[sorted(x) for x in sorted(p,key=lambda z:sorted(z))]})
            diag[mode]={
                "app_count":len(apps),
                "partition_mismatch_count":mismatch,
                "false_split_units":split,
                "false_merge_units":merge,
                "both_units":both,
                "examples":examples,
            }

        results.append({
            "chunk":c,
            "target_blob_sha1":target_blob,
            "preprocessing_all_match":all(pre_equal.values()),
            "published_app_count":len(target_parts),
            "replay_app_count":len(replay_parts),
            "native_partition_mismatch_count":native_mismatch,
            "native_descriptor_mismatch_count":desc_mismatch,
            "native_structural_digest_equal":xml_struct_digest(target_raw)==xml_struct_digest(replay_raw),
            "generic_decoders":diag,
        })

out={
    "study":"R2_FV_TRANSFER",
    "authority":"prospective within-project transfer after selector freeze",
    "source":{"commit":COMMIT,"archive_sha256":hashlib.sha256(archive).hexdigest()},
    "selector":{
        "eligible_chunks":eligible,
        "excluded_development_chunks":sorted(EXCLUDE),
        "selected_first_five":selected,
        "selection_uses_target_content":False,
    },
    "results":results,
    "claim_boundary":[
        "Chunks are within one project/book ecology and are not independent books.",
        "Native replay agreement reproduces the upstream workflow; it does not independently validate every editorial judgment.",
        "Generic decoder mismatches diagnose those fixed decoders, not information-theoretic impossibility.",
        "This experiment does not yet establish source-location preservation."
    ],
}
Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r2_frankenstein_transfer.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")

print("R2_FV_TRANSFER")
print("eligible="+str(len(eligible)))
print("selected="+"|".join(selected))
for r in results:
    print(f"CHUNK,{r['chunk']},apps={r['published_app_count']},native_mismatch={r['native_partition_mismatch_count']},descriptor_mismatch={r['native_descriptor_mismatch_count']},struct_equal={int(r['native_structural_digest_equal'])}")
    for mode,x in r["generic_decoders"].items():
        print(f"DECODER,{r['chunk']},{mode},mismatch={x['partition_mismatch_count']},split={x['false_split_units']},merge={x['false_merge_units']},both={x['both_units']}")
