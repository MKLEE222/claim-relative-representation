from __future__ import annotations

import collections
import hashlib
import itertools
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UPSTREAM="whitmanarchive/whitman-LG_1855_variorum"
PATH="source/authority/anc.02134.xml"
PARENT="fe63fcfbeca16f85583a29355c2d3a44e09b280f"
CHILD="8c6aba338bd3b8a52ec74d014ec1afc8137cc4a9"
EXPECTED_BLOB={
    PARENT:"41de695ece50bf10d414cf71e688464250e8b4d8",
    CHILD:"6a7e23ba67c2e4064312bea4d3598cdbe19e753b",
}
CERTS=("high","low")

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()

def local(tag):
    return tag.rsplit("}",1)[-1]

def fetch(ref):
    url=f"https://raw.githubusercontent.com/{UPSTREAM}/{ref}/{PATH}"
    req=urllib.request.Request(url,headers={"User-Agent":"CRR-module-D2/1.0"})
    with urllib.request.urlopen(req,timeout=90) as r:
        raw=r.read()
    got=git_blob(raw)
    if got!=EXPECTED_BLOB[ref]:
        raise RuntimeError(f"source drift {ref}: {got}")
    return raw

def parse(raw):
    root=ET.fromstring(raw)
    rows=[]
    for g in root.iter():
        if local(g.tag)!="linkGrp" or g.attrib.get("type")!="relation":
            continue
        ms_file=(g.attrib.get("corresp") or "").strip()
        for e in list(g):
            if local(e.tag)!="link":
                continue
            target=(e.attrib.get("target") or "").strip()
            parts=target.split()
            if len(parts)!=2:
                raise RuntimeError(f"unexpected target: {target!r}")
            cert=(e.attrib.get("cert") or "").strip()
            if cert not in CERTS:
                raise RuntimeError(f"unexpected cert {cert!r}")
            rows.append({"print_target":parts[0],"ms_file":ms_file,"ms_target":parts[1],"certainty":cert})
    return rows

def key(r):
    return (r["print_target"],r["ms_file"],r["ms_target"])

def state(rows):
    m=collections.defaultdict(list)
    for r in rows:
        m[key(r)].append(r["certainty"])
    return {k:tuple(sorted(v)) for k,v in m.items()}

def q0(rows):
    m=collections.defaultdict(list)
    for r in rows:
        m[r["print_target"]].append((r["ms_file"],r["ms_target"]))
    return {p:tuple(sorted(v)) for p,v in m.items()}

def projection(rows):
    m=collections.defaultdict(list)
    for r in rows:
        m[r["print_target"]].append(r)
    out={}
    for p,rs in m.items():
        eps=tuple(sorted((r["ms_file"],r["ms_target"]) for r in rs))
        h=sum(r["certainty"]=="high" for r in rs)
        l=sum(r["certainty"]=="low" for r in rs)
        out[p]={"endpoints":eps,"high_count":h,"low_count":l,
                "status":"MIXED" if h and l else "HIGH_ONLY" if h else "LOW_ONLY"}
    return out

def delta(P,C):
    ps,cs=state(P),state(C)
    changed=[];unchanged=[];added=[];removed=[]
    for k in sorted(set(ps)|set(cs)):
        a=ps.get(k,());b=cs.get(k,())
        base={"print_target":k[0],"ms_file":k[1],"ms_target":k[2]}
        if a==b: unchanged.append({**base,"certainty":list(a)})
        elif not a: added.append({**base,"new":list(b)})
        elif not b: removed.append({**base,"old":list(a)})
        else: changed.append({**base,"old":list(a),"new":list(b)})
    return changed,unchanged,added,removed

def apply_full(ps,changed,added,removed):
    out=dict(ps)
    for x in changed:
        k=(x["print_target"],x["ms_file"],x["ms_target"])
        if out.get(k)!=tuple(x["old"]): raise RuntimeError("old state mismatch")
        out[k]=tuple(x["new"])
    for x in removed:
        k=(x["print_target"],x["ms_file"],x["ms_target"])
        if out.get(k)!=tuple(x["old"]): raise RuntimeError("remove mismatch")
        out.pop(k)
    for x in added:
        k=(x["print_target"],x["ms_file"],x["ms_target"])
        if k in out: raise RuntimeError("add collision")
        out[k]=tuple(x["new"])
    return out

def locus_candidates(parent_proj, changed, added, removed):
    """Enumerate child endpoint-cert states compatible with coarse parent state + identity-rich natural patch."""
    if parent_proj is None:
        if changed or removed:
            return []
        child={}
        for x in added:
            if len(x["new"])!=1: return []
            child[(x["ms_file"],x["ms_target"])]=x["new"][0]
        return [tuple(sorted((a,b,c) for (a,b),c in child.items()))]
    endpoints=list(parent_proj["endpoints"])
    if len(endpoints)>20:
        raise RuntimeError("locus too large for exact enumeration")
    cb={(x["ms_file"],x["ms_target"]):x for x in changed}
    rb={(x["ms_file"],x["ms_target"]):x for x in removed}
    ab={(x["ms_file"],x["ms_target"]):x for x in added}
    candidates=set()
    for highs in itertools.combinations(range(len(endpoints)),parent_proj["high_count"]):
        hs=set(highs)
        assign={ep:("high" if i in hs else "low") for i,ep in enumerate(endpoints)}
        ok=True
        for ep,x in cb.items():
            if len(x["old"])!=1 or assign.get(ep)!=x["old"][0]: ok=False;break
        if not ok: continue
        for ep,x in rb.items():
            if len(x["old"])!=1 or assign.get(ep)!=x["old"][0]: ok=False;break
        if not ok: continue
        child=dict(assign)
        for ep,x in cb.items():
            if len(x["new"])!=1: ok=False;break
            child[ep]=x["new"][0]
        if not ok: continue
        for ep in rb: child.pop(ep,None)
        for ep,x in ab.items():
            if len(x["new"])!=1: ok=False;break
            child[ep]=x["new"][0]
        if ok:
            candidates.add(tuple(sorted((a,b,c) for (a,b),c in child.items())))
    return sorted(candidates)

def regex_parse(raw):
    import re
    text=raw.decode()
    rows=[]
    gre=re.compile(r'<linkGrp\b[^>]*\btype="relation"[^>]*\bcorresp="([^"]+)"[^>]*>(.*?)</linkGrp>',re.S)
    lre=re.compile(r'<link\b([^>]*?)/>',re.S)
    for gm in gre.finditer(text):
        f=gm.group(1)
        for lm in lre.finditer(gm.group(2)):
            attrs=lm.group(1)
            cm=re.search(r'\bcert="([^"]+)"',attrs)
            tm=re.search(r'\btarget="([^"]+)"',attrs)
            if not(cm and tm): continue
            parts=tm.group(1).split()
            if len(parts)==2:
                rows.append({"print_target":parts[0],"ms_file":f,"ms_target":parts[1],"certainty":cm.group(1)})
    return rows

def main():
    outdir=Path(__file__).with_name("results")
    outdir.mkdir(parents=True,exist_ok=True)
    praw,craw=fetch(PARENT),fetch(CHILD)
    P,C=parse(praw),parse(craw)
    PS,CS=state(P),state(C)
    changed,unchanged,added,removed=delta(P,C)
    PQ,CQ=q0(P),q0(C)
    PP=projection(P)

    patch_keys={(x["print_target"],x["ms_file"],x["ms_target"]) for x in changed+added+removed}
    full=apply_full(PS,changed,added,removed)
    collateral=[k for k in set(PS)&set(full) if k not in patch_keys and PS[k]!=full[k]]

    affected=sorted({x["print_target"] for x in changed+added+removed})
    locus_results={}
    exact=ambiguous=impossible=0
    topology_changed=cert_only=0
    for p in affected:
        ch=[x for x in changed if x["print_target"]==p]
        ad=[x for x in added if x["print_target"]==p]
        rm=[x for x in removed if x["print_target"]==p]
        cand=locus_candidates(PP.get(p),ch,ad,rm)
        truth=tuple(sorted((r["ms_file"],r["ms_target"],r["certainty"]) for r in C if r["print_target"]==p))
        if len(cand)==1 and cand[0]==truth:
            cls="EXACT";exact+=1
        elif not cand:
            cls="NO_COMPATIBLE_STATE";impossible+=1
        else:
            cls="AMBIGUOUS";ambiguous+=1
        if ad or rm: topology_changed+=1
        else: cert_only+=1
        locus_results[p]={
            "parent_projection":PP.get(p),
            "cert_changed":len(ch),"added":len(ad),"removed":len(rm),
            "candidate_child_states":len(cand),
            "disposition":cls,
            "child_truth":truth,
        }

    # Endpoint-only: patch gives status only for changed/added relations, all untouched statuses remain unknown.
    known={(x["print_target"],x["ms_file"],x["ms_target"]):tuple(x["new"]) for x in changed+added}
    unresolved=sum(len(v) for k,v in CS.items() if k not in known)

    # Independent source reopening.
    source_reopen=state(regex_parse(craw))==CS

    # Wrong certainty-binding control if new cert multiset admits nontrivial reassignment.
    wrong={"disposition":"WRONG_CERT_BINDING_CONTROL_NOT_IDENTIFIABLE"}
    if len(changed)>=2:
        news=[tuple(x["new"]) for x in changed]
        for shift in range(1,len(changed)):
            perm=news[shift:]+news[:shift]
            if any(perm[i]!=news[i] for i in range(len(news))):
                wrong_changed=[dict(x,new=list(perm[i])) for i,x in enumerate(changed)]
                try:
                    wrong_state=apply_full(PS,wrong_changed,added,removed)
                    wrong={"disposition":"WRONG_BINDING_FAILS" if wrong_state!=CS else "WRONG_BINDING_UNEXPECTED_PASS",
                           "shift":shift,"wrong_exact":wrong_state==CS}
                except RuntimeError as e:
                    wrong={"disposition":"WRONG_BINDING_FAILS","shift":shift,"reason":str(e)}
                break

    directions=collections.Counter()
    for x in changed:
        if len(x["old"])==len(x["new"])==1:
            directions[f'{x["old"][0]}->{x["new"][0]}']+=1
    affected_files=sorted({x["ms_file"] for x in changed+added+removed})
    per_file=collections.Counter(x["ms_file"] for x in changed+added+removed)

    patch={"changed":changed,"added":added,"removed":removed}
    parent_state=[{"print_target":k[0],"ms_file":k[1],"ms_target":k[2],"certainty":list(v)} for k,v in sorted(PS.items())]

    result={
      "study":"MODULE_D2_WHITMAN_NATURAL_COMBINED_REVISION_V1",
      "authority":"PRE_DIFF_FROZEN_DEVELOPMENT_PRESSURE_TEST_NOT_INDEPENDENT_TRANSFER",
      "source":{
        "repo":UPSTREAM,"path":PATH,
        "parent":{"commit":PARENT,"git_blob":EXPECTED_BLOB[PARENT],"sha256":sha256(praw),"bytes":len(praw)},
        "child":{"commit":CHILD,"git_blob":EXPECTED_BLOB[CHILD],"sha256":sha256(craw),"bytes":len(craw)},
        "child_commit_message":"adjusted certainty and some relations",
      },
      "population":{"parent_records":len(P),"child_records":len(C),
                    "parent_identities":len(PS),"child_identities":len(CS),
                    "parent_duplicates":len(P)-len(PS),"child_duplicates":len(C)-len(CS)},
      "natural_delta":{
        "cert_changed":len(changed),"added":len(added),"removed":len(removed),"unchanged":len(unchanged),
        "affected_print_targets":len(affected),"affected_source_files":len(affected_files),
        "certainty_directions":dict(directions),
        "delta_records_by_source_file":dict(per_file),
      },
      "current_task":{
        "endpoint_state_equal":PQ==CQ,
        "parent_print_targets":len(PQ),"child_print_targets":len(CQ),
        "print_targets_added":len(set(CQ)-set(PQ)),
        "print_targets_removed":len(set(PQ)-set(CQ)),
        "print_targets_endpoint_changed":sum(PQ.get(p)!=CQ.get(p) for p in set(PQ)|set(CQ)),
      },
      "R_FULL_RELATION_STATE":{
        "complete_child_state_exact":full==CS,
        "changed_cert_correct":all(full.get((x["print_target"],x["ms_file"],x["ms_target"]))==tuple(x["new"]) for x in changed),
        "added_correct":all(full.get((x["print_target"],x["ms_file"],x["ms_target"]))==tuple(x["new"]) for x in added),
        "removed_correct":all((x["print_target"],x["ms_file"],x["ms_target"]) not in full for x in removed),
        "unaffected_stability":all(full.get(k)==PS[k] for k in PS if k not in patch_keys and k in full),
        "collateral_changes":len(collateral),
      },
      "R_CERT_ONLY_STATE":{
        "affected_loci":len(affected),
        "cert_only_affected_loci":cert_only,
        "topology_changed_affected_loci":topology_changed,
        "affected_loci_exact":exact,
        "affected_loci_ambiguous":ambiguous,
        "affected_loci_no_compatible_state":impossible,
        "all_affected_exact":exact==len(affected),
        "locus_results":locus_results,
      },
      "R_ENDPOINT_ONLY":{
        "child_endpoint_task_exact_from_child_patch":True,
        "status_items_known_from_changed_or_added_delta":sum(len(v) for v in known.values()),
        "child_status_items_unresolved":unresolved,
        "complete_child_state_exact":unresolved==0,
      },
      "R_SOURCE_REOPEN":{"complete_child_state_exact":source_reopen,"child_source_bytes":len(craw)},
      "wrong_control":wrong,
      "costs":{
        "natural_delta_json_bytes":len(canonical(patch)),
        "parent_full_state_json_bytes":len(canonical(parent_state)),
        "parent_source_bytes":len(praw),"child_source_bytes":len(craw),
      },
      "dispositions":{
        "NATURAL_COMBINED_REVISION_OBSERVED":bool(changed) and bool(added or removed),
        "SELECTIVE_COMBINED_REVISION":full==CS and not collateral,
        "COARSE_STATE_NONDETERMINING_ON_AFFECTED_LOCUS":ambiguous>0,
        "COARSE_STATE_SUFFICIENT_ON_ALL_AFFECTED_LOCI":exact==len(affected),
        "SOURCE_REOPEN_EXACT":source_reopen,
        "WRONG_BINDING_FAILS":wrong["disposition"]=="WRONG_BINDING_FAILS",
      },
      "claim_boundary":[
        "The child editorial state is not treated as independent genetic truth.",
        "D2 was selected by commit message and parent identity before opening the file delta.",
        "This is already-exposed Whitman infrastructure, not independent transfer.",
        "Affected-locus determinacy is evaluated from parent endpoint set + high/low counts plus the identity-rich natural patch.",
        "Any ambiguity at an affected locus is a finite state/event-channel result, not a universal minimality theorem.",
      ],
    }
    out=outdir/"results.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    summary={k:v for k,v in result.items() if k!="R_CERT_ONLY_STATE"}
    summary["R_CERT_ONLY_STATE"]={k:v for k,v in result["R_CERT_ONLY_STATE"].items() if k!="locus_results"}
    summary["results_sha256"]=sha256(out.read_bytes())
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
