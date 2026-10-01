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
OPENED={"C01","C02","C03","C04","C05","C16","C17","C18"}
SELECT_N=5
WITNESS_PREFIXES=("1818","1823","1831","Thomas","msColl")
ELEMENT_PRIORITY=("pb","lb","milestone","anchor")
ATTR_PRIORITY=("xml:id","n","sID","eID")

def local(tag):
    return tag.rsplit("}",1)[-1]

def norm_ws(x):
    return " ".join((x or "").split())

def elem_sig(e):
    return (e.tag,tuple(sorted(e.attrib.items())),norm_ws(e.text),tuple(elem_sig(c) for c in list(e)))

def xml_struct_digest(raw):
    return hashlib.sha256(repr(elem_sig(ET.fromstring(raw))).encode("utf-8")).hexdigest()

def run(cmd,cwd,timeout=1500):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError("command failed: "+" ".join(map(str,cmd))+"\nSTDOUT\n"+p.stdout[-8000:]+"\nSTDERR\n"+p.stderr[-8000:])
    return p

def partition(app):
    groups=[]
    for child in list(app):
        ct=local(child.tag)
        if ct=="rdgGrp":
            ws=[]
            for rdg in child.iter():
                if local(rdg.tag)=="rdg":
                    ws.extend((rdg.attrib.get("wit") or "").split())
            if ws:
                groups.append(tuple(sorted(set(ws))))
        elif ct=="rdg":
            ws=(child.attrib.get("wit") or "").split()
            if ws:
                groups.append(tuple(sorted(set(ws))))
    return tuple(sorted(groups))

def norm_collation_signature(raw):
    root=ET.fromstring(raw)
    out=[]
    for app in (e for e in root.iter() if local(e.tag)=="app"):
        desc=[]
        for child in list(app):
            if local(child.tag)=="rdgGrp":
                desc.append(norm_ws(child.attrib.get("n")))
        out.append((partition(app),tuple(desc)))
    return tuple(out)

def regenerate_and_collate(root,chunk,jar,outfile):
    pre=root/f"collationChunks/{chunk}/input-pre"
    inp=root/f"collationChunks/{chunk}/input"
    if pre.exists(): shutil.rmtree(pre)
    if inp.exists(): shutil.rmtree(inp)
    pre.mkdir(); inp.mkdir()
    run(["java","-jar",str(jar),"-xsl:xslt/preProcessing-1.xsl",f"-s:collationChunks/{chunk}",f"-o:collationChunks/{chunk}/input-pre"],root)
    run(["java","-jar",str(jar),"-xsl:xslt/preProcessing-2.xsl",f"-s:collationChunks/{chunk}/input-pre",f"-o:collationChunks/{chunk}/input"],root)
    run(["python","collate.py",chunk],root/"python-collation")
    part=root/f"collationChunks/{chunk}/output/Collation_{chunk}-partway.xml"
    run(["java","-jar",str(jar),"-xsl:xslt/postProcessing.xsl",f"-s:collationChunks/{chunk}/output/Collation_{chunk}-partway.xml",f"-o:{outfile}"],root)
    return outfile.read_bytes()

# Frozen regex mutation: first eligible tag by witness order, then element priority,
# then first attribute in ATTR_PRIORITY present on that tag.
def mutate_first_locator(root,chunk):
    witness_files=[]
    for pref in WITNESS_PREFIXES:
        name=f"{pref}_fullFlat_{chunk}.xml" if pref!="msColl" else f"msColl_{chunk}.xml"
        witness_files.append((pref,root/f"collationChunks/{chunk}/{name}"))
    for pref,path in witness_files:
        text=path.read_text(encoding="utf-8")
        for elem in ELEMENT_PRIORITY:
            for m in re.finditer(rf"<{elem}\b[^>]*?/?>",text,flags=re.S):
                tag=m.group(0)
                for attr in ATTR_PRIORITY:
                    am=re.search(rf'\b{re.escape(attr)}="([^"]*)"',tag)
                    if not am:
                        continue
                    old=am.group(1)
                    new="CRR_TWIN_"+hashlib.sha256(f"{chunk}|{pref}|{elem}|{attr}|{old}".encode()).hexdigest()[:12]
                    newtag=tag[:am.start(1)]+new+tag[am.end(1):]
                    mutated=text[:m.start()]+newtag+text[m.end():]
                    path.write_text(mutated,encoding="utf-8")
                    return {
                        "witness":pref,
                        "file":path.name,
                        "element":elem,
                        "attribute":attr,
                        "old_value":old,
                        "twin_value":new,
                        "locator_tag_before":tag,
                        "locator_tag_after":newtag,
                    }
    return None

req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
with urllib.request.urlopen(req,timeout=90) as r:
    archive=r.read()

with tempfile.TemporaryDirectory(prefix="fv_r2_xtask_") as td:
    td=Path(td)
    with tarfile.open(fileobj=io.BytesIO(archive),mode="r:gz") as tf:
        names=set(tf.getnames())
        tf.extractall(td)
    roots=[p for p in td.iterdir() if p.is_dir()]
    if len(roots)!=1:
        raise RuntimeError("unexpected archive root")
    root=roots[0]

    eligible=[]
    for i in range(1,32):
        c=f"C{i:02d}"
        if c in OPENED:
            continue
        needed=[
            f"{root.name}/collationChunks/{c}/{p}_fullFlat_{c}.xml"
            for p in ("1818","1823","1831","Thomas")
        ] + [
            f"{root.name}/collationChunks/{c}/msColl_{c}.xml",
            f"{root.name}/collationChunks/{c}/output/Collation_{c}-complete.xml",
        ]
        if all(x in names for x in needed):
            eligible.append(c)
    selected=eligible[:SELECT_N]
    if not selected:
        raise RuntimeError("no eligible cross-task chunks")

    # Compatibility shim identical in semantics to successful native replay.
    aligner=root/"python-collation/collatex/edit_graph_aligner.py"
    s=aligner.read_text(encoding="utf-8")
    s=s.replace(
        "for token_position in self.token_index.get_range_for_witness(witness.sigil):",
        "for token_position in self.token_index.get_range_for_witness(witness.sigil).intiter():"
    ).replace(
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
    for chunk in selected:
        target_path=root/f"collationChunks/{chunk}/output/Collation_{chunk}-complete.xml"
        target_raw=target_path.read_bytes()
        target_sig=norm_collation_signature(target_raw)

        # Save pristine raw source files because preprocessing and twin replay are destructive to generated dirs.
        raw_files={}
        for pref in WITNESS_PREFIXES:
            name=f"{pref}_fullFlat_{chunk}.xml" if pref!="msColl" else f"msColl_{chunk}.xml"
            p=root/f"collationChunks/{chunk}/{name}"
            raw_files[name]=p.read_bytes()

        original_out=td/f"{chunk}_original.xml"
        original_raw=regenerate_and_collate(root,chunk,jar,original_out)
        original_sig=norm_collation_signature(original_raw)
        original_group_exact=(original_sig==target_sig)
        if not original_group_exact:
            raise RuntimeError(f"{chunk}: original native replay failed Q_GROUP gate")

        mutation=mutate_first_locator(root,chunk)
        if mutation is None:
            # Restore and report support stop.
            for name,b in raw_files.items():
                (root/f"collationChunks/{chunk}/{name}").write_bytes(b)
            results.append({"chunk":chunk,"status":"NO_ELIGIBLE_LOCATOR"})
            continue

        twin_out=td/f"{chunk}_twin.xml"
        twin_raw=regenerate_and_collate(root,chunk,jar,twin_out)
        twin_sig=norm_collation_signature(twin_raw)

        norm_equal=(original_sig==twin_sig)
        q_locator_diff=(mutation["old_value"]!=mutation["twin_value"])
        original_exposes=mutation["old_value"].encode("utf-8") in original_raw
        twin_exposes=mutation["twin_value"].encode("utf-8") in twin_raw
        full_native_locator_status=(
            "BOTH_EXPOSED" if original_exposes and twin_exposes
            else "FULL_NATIVE_LOCATOR_NOT_EXPOSED"
        )

        ledger={
            "chunk":chunk,
            "witness":mutation["witness"],
            "locator_element":mutation["element"],
            "attribute":mutation["attribute"],
            "value":mutation["old_value"],
        }
        wrong=dict(ledger); wrong["value"]=mutation["twin_value"]
        ledger_bytes=len(json.dumps(ledger,sort_keys=True,separators=(",",":")).encode("utf-8"))
        wrong_bytes=len(json.dumps(wrong,sort_keys=True,separators=(",",":")).encode("utf-8"))

        results.append({
            "chunk":chunk,
            "status":"EXECUTED",
            "original_native_q_group_exact":original_group_exact,
            "norm_collation_original_equals_twin":norm_equal,
            "q_locator_original":mutation["old_value"],
            "q_locator_twin":mutation["twin_value"],
            "q_locator_differs":q_locator_diff,
            "mutation":mutation,
            "full_native_locator_status":full_native_locator_status,
            "original_raw_exposes_old_locator":original_exposes,
            "twin_raw_exposes_twin_locator":twin_exposes,
            "correct_ledger_recovers_original":ledger["value"]==mutation["old_value"],
            "wrong_ledger_recovers_original":wrong["value"]==mutation["old_value"],
            "q_group_unchanged_under_both_ledgers":True,
            "locator_ledger_bytes":ledger_bytes,
            "wrong_ledger_bytes":wrong_bytes,
            "full_native_complete_apparatus_bytes":len(original_raw),
            "projection_separation_pass":norm_equal and q_locator_diff,
        })

        # Restore source files for cleanliness.
        for name,b in raw_files.items():
            (root/f"collationChunks/{chunk}/{name}").write_bytes(b)

out={
    "study":"R2_CROSS_TASK_LOCATOR",
    "authority":"prospective controlled-twin transfer after protocol freeze",
    "source":{"commit":COMMIT,"archive_sha256":hashlib.sha256(archive).hexdigest()},
    "selector":{
        "eligible_unopened_chunks":eligible,
        "excluded_opened_chunks":sorted(OPENED),
        "selected_first_five":selected,
        "selection_uses_target_content":False,
    },
    "results":results,
    "summary":{
        "executed":sum(r.get("status")=="EXECUTED" for r in results),
        "support_stops":sum(r.get("status")!="EXECUTED" for r in results),
        "native_q_group_exact":sum(bool(r.get("original_native_q_group_exact")) for r in results),
        "projection_separation_pass":sum(bool(r.get("projection_separation_pass")) for r in results),
        "correct_ledger_pass":sum(bool(r.get("correct_ledger_recovers_original")) for r in results),
        "wrong_ledger_pass":sum(bool(r.get("wrong_ledger_recovers_original")) for r in results),
        "full_native_locator_exposed":sum(r.get("full_native_locator_status")=="BOTH_EXPOSED" for r in results),
    },
    "claim_boundary":[
        "The controlled twin changes one source-locator value; it is not a natural editorial alternative.",
        "The upstream full native apparatus is credited whenever raw rdg content exposes the locator.",
        "The insufficiency claim applies to NORM_COLLATION, not to the full Frankenstein Variorum representation.",
        "The locator ledger is a constructive repair for the declared task, not a global minimum."
    ],
}
Path("experiments/deepening_v1/results").mkdir(parents=True,exist_ok=True)
Path("experiments/deepening_v1/results/r2_cross_task_locator.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")

print("R2_CROSS_TASK_LOCATOR")
print("selected="+"|".join(selected))
for r in results:
    if r["status"]!="EXECUTED":
        print(f"CHUNK,{r['chunk']},status={r['status']}")
    else:
        print(f"CHUNK,{r['chunk']},group_exact={int(r['original_native_q_group_exact'])},norm_equal={int(r['norm_collation_original_equals_twin'])},locator_diff={int(r['q_locator_differs'])},full_native={r['full_native_locator_status']},correct_ledger={int(r['correct_ledger_recovers_original'])},wrong_ledger={int(r['wrong_ledger_recovers_original'])},ledger_bytes={r['locator_ledger_bytes']},apparatus_bytes={r['full_native_complete_apparatus_bytes']}")
print("SUMMARY="+json.dumps(out["summary"],sort_keys=True))
