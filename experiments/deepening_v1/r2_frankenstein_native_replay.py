from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

COMMIT="5a208f869ff1213defa000e3181d5315a072a15f"
URL=f"https://github.com/FrankensteinVariorum/collationWorkspace/archive/{COMMIT}.tar.gz"
CHUNK="C18"
WITNESS_FILES=[
    "1818_fullFlat_C18.xml",
    "1823_fullFlat_C18.xml",
    "1831_fullFlat_C18.xml",
    "Thomas_fullFlat_C18.xml",
    "msColl_C18.xml",
]
TARGET_REL="collationChunks/C18/output/Collation_C18-complete.xml"
TARGET_BLOB_SHA1="bca0548912ab1d7b2676360d33a6468290296d7e"

def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii")+raw).hexdigest()

def local(tag: str) -> str:
    return tag.rsplit("}",1)[-1]

def norm_text(x: str | None) -> str:
    return " ".join((x or "").split())

def elem_sig(e: ET.Element):
    return (
        e.tag,
        tuple(sorted(e.attrib.items())),
        norm_text(e.text),
        tuple(elem_sig(c) for c in list(e)),
    )

def xml_struct_digest(raw: bytes) -> str:
    root=ET.fromstring(raw)
    payload=repr(elem_sig(root)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def app_partition_signature(raw: bytes):
    root=ET.fromstring(raw)
    out=[]
    for app in (e for e in root.iter() if local(e.tag)=="app"):
        groups=[]
        for child in list(app):
            ct=local(child.tag)
            if ct=="rdgGrp":
                w=[]
                for rdg in child.iter():
                    if local(rdg.tag)=="rdg":
                        w.extend((rdg.attrib.get("wit") or "").split())
                if w:
                    groups.append(tuple(sorted(set(w))))
            elif ct=="rdg":
                w=(child.attrib.get("wit") or "").split()
                if w:
                    groups.append(tuple(sorted(set(w))))
        out.append(tuple(sorted(groups)))
    return out

def descriptor_signature(raw: bytes):
    root=ET.fromstring(raw)
    out=[]
    for app in (e for e in root.iter() if local(e.tag)=="app"):
        vals=[]
        for g in list(app):
            if local(g.tag)=="rdgGrp":
                vals.append(norm_text(g.attrib.get("n")))
        out.append(tuple(vals))
    return out

def run(cmd, cwd: Path, timeout=900):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError(
            "command failed: "+" ".join(map(str,cmd))+
            "\nSTDOUT\n"+p.stdout[-8000:]+"\nSTDERR\n"+p.stderr[-8000:]
        )
    return p

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=90) as r:
    archive=r.read()

with tempfile.TemporaryDirectory(prefix="fv_r2_") as td:
    td=Path(td)
    with tarfile.open(fileobj=io.BytesIO(archive),mode="r:gz") as tf:
        tf.extractall(td)
    roots=[p for p in td.iterdir() if p.is_dir()]
    if len(roots)!=1:
        raise RuntimeError(f"unexpected extracted roots: {roots}")
    root=roots[0]

    # Compatibility shim only: ClusterShell >=1.9 iterates RangeSet as strings,
    # while vendored CollateX 2.2 was written against integer iteration.
    # Use the documented intiter() API to preserve the historical integer-position semantics.
    tokenindex=root/"python-collation/collatex/tokenindex.py"
    tokenindex_text=tokenindex.read_text(encoding="utf-8")
    old_iter="for token_position in self.token_index.get_range_for_witness(witness.sigil):"
    new_iter="for token_position in self.token_index.get_range_for_witness(witness.sigil).intiter():"
    if old_iter not in tokenindex_text:
        raise RuntimeError("RangeSet compatibility target not found")
    tokenindex.write_text(tokenindex_text.replace(old_iter,new_iter),encoding="utf-8")

    target_path=root/TARGET_REL
    target_raw=target_path.read_bytes()
    target_blob=git_blob_sha1(target_raw)
    if target_blob!=TARGET_BLOB_SHA1:
        raise RuntimeError(f"published C18 target drift: {target_blob}")

    pinned_inputs={}
    input_dir=root/f"collationChunks/{CHUNK}/input"
    for name in WITNESS_FILES:
        p=input_dir/name
        if not p.exists():
            raise RuntimeError(f"missing pinned input: {name}")
        pinned_inputs[name]=p.read_bytes()

    pinned_input_digests={name:xml_struct_digest(raw) for name,raw in pinned_inputs.items()}

    # Rebuild both preprocessing stages from the pinned raw chunk directory.
    pre_dir=root/f"collationChunks/{CHUNK}/input-pre"
    shutil.rmtree(pre_dir)
    shutil.rmtree(input_dir)
    pre_dir.mkdir()
    input_dir.mkdir()

    jar=root/"xslt/SaxonHE12-0J/saxon-he-12.0.jar"
    if not jar.exists():
        raise RuntimeError("Saxon jar missing from pinned upstream repository")

    run(["java","-jar",str(jar),"-xsl:xslt/preProcessing-1.xsl",f"-s:collationChunks/{CHUNK}",f"-o:collationChunks/{CHUNK}/input-pre"],root)
    run(["java","-jar",str(jar),"-xsl:xslt/preProcessing-2.xsl",f"-s:collationChunks/{CHUNK}/input-pre",f"-o:collationChunks/{CHUNK}/input"],root)

    regenerated_inputs={}
    for name in WITNESS_FILES:
        p=input_dir/name
        if not p.exists():
            raise RuntimeError(f"preprocessing did not regenerate {name}")
        regenerated_inputs[name]=p.read_bytes()

    preproc_equal={
        name: xml_struct_digest(regenerated_inputs[name])==pinned_input_digests[name]
        for name in WITNESS_FILES
    }

    # Preserve published target and run native Python CollateX stage on regenerated inputs.
    published_copy=td/"published_C18_complete.xml"
    published_copy.write_bytes(target_raw)

    run(["python","collate.py",CHUNK],root/"python-collation",timeout=1200)
    partway=root/f"collationChunks/{CHUNK}/output/Collation_{CHUNK}-partway.xml"
    if not partway.exists():
        raise RuntimeError("native CollateX replay produced no partway output")

    replay_complete=td/"replay_C18_complete.xml"
    run([
        "java","-jar",str(jar),
        "-xsl:xslt/postProcessing.xsl",
        f"-s:collationChunks/{CHUNK}/output/Collation_{CHUNK}-partway.xml",
        f"-o:{replay_complete}",
    ],root,timeout=1200)

    replay_raw=replay_complete.read_bytes()
    target_struct=xml_struct_digest(target_raw)
    replay_struct=xml_struct_digest(replay_raw)

    target_parts=app_partition_signature(target_raw)
    replay_parts=app_partition_signature(replay_raw)
    n=min(len(target_parts),len(replay_parts))
    partition_mismatch=[i for i in range(n) if target_parts[i]!=replay_parts[i]]
    if len(target_parts)!=len(replay_parts):
        partition_mismatch.extend(range(n,max(len(target_parts),len(replay_parts))))

    target_desc=descriptor_signature(target_raw)
    replay_desc=descriptor_signature(replay_raw)
    n2=min(len(target_desc),len(replay_desc))
    descriptor_mismatch=[i for i in range(n2) if target_desc[i]!=replay_desc[i]]
    if len(target_desc)!=len(replay_desc):
        descriptor_mismatch.extend(range(n2,max(len(target_desc),len(replay_desc))))

    examples=[]
    for i in partition_mismatch[:10]:
        examples.append({
            "app_index":i,
            "published":target_parts[i] if i<len(target_parts) else None,
            "replay":replay_parts[i] if i<len(replay_parts) else None,
        })

    out={
        "study":"R2_FV_REPLAY",
        "authority":"retrospective native-pipeline reproduction",
        "source":{
            "commit":COMMIT,
            "archive_sha256":hashlib.sha256(archive).hexdigest(),
            "published_target_blob_sha1":target_blob,
        },
        "environment":{
            "python":run(["python","--version"],root).stdout.strip() or run(["python","--version"],root).stderr.strip(),
            "java":run(["java","-version"],root).stderr.splitlines()[0] if True else "",
        },
        "preprocessing":{
            "files":WITNESS_FILES,
            "structural_match_to_pinned_input":preproc_equal,
            "all_match":all(preproc_equal.values()),
        },
        "native_replay":{
            "published_app_count":len(target_parts),
            "replay_app_count":len(replay_parts),
            "partition_mismatch_count":len(partition_mismatch),
            "descriptor_mismatch_count":len(descriptor_mismatch),
            "structural_digest_equal":target_struct==replay_struct,
            "published_structural_sha256":target_struct,
            "replay_structural_sha256":replay_struct,
            "partition_examples":examples,
        },
        "claim_boundary":[
            "Exact native replay agreement is a reproduction of the project pipeline, not an independent scholarly gold standard.",
            "A mismatch may reflect environment/dependency drift or historical manual workflow state and must not be silently converted into our preferred normalization.",
            "Target rdgGrp@n values are used only for comparison after replay; they are never supplied to the replay algorithm."
        ],
    }

Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r2_frankenstein_native_replay.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")

print("R2_FV_NATIVE_REPLAY")
print("archive_sha256="+out["source"]["archive_sha256"])
print("preprocessing_all_match="+str(int(out["preprocessing"]["all_match"])))
print("published_app_count="+str(len(target_parts)))
print("replay_app_count="+str(len(replay_parts)))
print("partition_mismatch_count="+str(len(partition_mismatch)))
print("descriptor_mismatch_count="+str(len(descriptor_mismatch)))
print("structural_digest_equal="+str(int(target_struct==replay_struct)))
