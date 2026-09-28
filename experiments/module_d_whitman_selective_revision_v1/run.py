from __future__ import annotations

import collections
import hashlib
import itertools
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UPSTREAM = "whitmanarchive/whitman-LG_1855_variorum"
PATH = "source/authority/anc.02134.xml"
PARENT = "7cdf5ddc9d0cfff83289f687613ee3d0510e6520"
CHILD = "fe63fcfbeca16f85583a29355c2d3a44e09b280f"
EXPECTED_BLOB = {
    PARENT: "013041d1f51d20c6a59fdfbc494e6dd9c03fae0a",
    CHILD: "41de695ece50bf10d414cf71e688464250e8b4d8",
}
CERTS = ("high", "low")

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()

def local(tag):
    return tag.rsplit("}", 1)[-1]

def fetch(ref):
    url=f"https://raw.githubusercontent.com/{UPSTREAM}/{ref}/{PATH}"
    req=urllib.request.Request(url, headers={"User-Agent":"CRR-module-D1/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        raw=r.read()
    got=git_blob(raw)
    if got != EXPECTED_BLOB[ref]:
        raise RuntimeError(f"source drift {ref}: {got}")
    return raw

def parse(raw):
    root=ET.fromstring(raw)
    rows=[]
    for g in root.iter():
        if local(g.tag) != "linkGrp" or g.attrib.get("type") != "relation":
            continue
        ms_file=(g.attrib.get("corresp") or "").strip()
        for link in list(g):
            if local(link.tag) != "link":
                continue
            target=(link.attrib.get("target") or "").strip()
            parts=target.split()
            if len(parts) != 2:
                raise RuntimeError(f"unexpected target shape: {target!r}")
            cert=(link.attrib.get("cert") or "").strip()
            if cert not in CERTS:
                raise RuntimeError(f"unexpected certainty: {cert!r}")
            rows.append({
                "print_target": parts[0],
                "ms_file": ms_file,
                "ms_target": parts[1],
                "certainty": cert,
            })
    return rows

def key(r):
    return (r["print_target"], r["ms_file"], r["ms_target"])

def state(rows):
    out=collections.defaultdict(list)
    for r in rows:
        out[key(r)].append(r["certainty"])
    return {k: tuple(sorted(v)) for k,v in out.items()}

def q0(rows):
    by=collections.defaultdict(list)
    for r in rows:
        by[r["print_target"]].append((r["ms_file"],r["ms_target"]))
    return {k: tuple(sorted(v)) for k,v in by.items()}

def locus_projection(rows):
    by=collections.defaultdict(list)
    for r in rows:
        by[r["print_target"]].append(r)
    out={}
    for p,rs in by.items():
        endpoints=tuple(sorted((r["ms_file"],r["ms_target"]) for r in rs))
        high=sum(r["certainty"]=="high" for r in rs)
        low=sum(r["certainty"]=="low" for r in rs)
        out[p]={
            "endpoints": endpoints,
            "high_count": high,
            "low_count": low,
            "status": "MIXED" if high and low else "HIGH_ONLY" if high else "LOW_ONLY",
        }
    return out

def derive_delta(parent_rows, child_rows):
    ps,cs=state(parent_rows),state(child_rows)
    allk=sorted(set(ps)|set(cs))
    changed=[]; unchanged=[]; added=[]; removed=[]
    for k in allk:
        a=ps.get(k,()); b=cs.get(k,())
        rec={"print_target":k[0],"ms_file":k[1],"ms_target":k[2]}
        if a==b:
            unchanged.append({**rec,"certainty":list(a)})
        elif not a:
            added.append({**rec,"new":list(b)})
        elif not b:
            removed.append({**rec,"old":list(a)})
        else:
            changed.append({**rec,"old":list(a),"new":list(b)})
    return changed,unchanged,added,removed

def apply_full_binding(parent_state, changed, added, removed):
    out=dict(parent_state)
    for x in changed:
        k=(x["print_target"],x["ms_file"],x["ms_target"])
        if out.get(k) != tuple(x["old"]):
            raise RuntimeError("changed-record old state mismatch")
        out[k]=tuple(x["new"])
    for x in removed:
        k=(x["print_target"],x["ms_file"],x["ms_target"])
        if out.get(k) != tuple(x["old"]):
            raise RuntimeError("removed-record old state mismatch")
        out.pop(k)
    for x in added:
        k=(x["print_target"],x["ms_file"],x["ms_target"])
        if k in out:
            raise RuntimeError("added key already exists")
        out[k]=tuple(x["new"])
    return out

def enumerate_locus_assignments(proj, patch_changed, patch_removed, patch_added):
    """All endpoint->cert assignments compatible with a locus aggregate, then natural patch.

    This arm does not retain endpoint-specific cert binding. It may infer binding when
    counts + identity-rich patch make the solution unique.
    """
    endpoints=list(proj["endpoints"])
    n=len(endpoints)
    if n > 20:
        raise RuntimeError("locus too large for exact finite enumeration")
    changed_by_ep={(x["ms_file"],x["ms_target"]):x for x in patch_changed}
    removed_by_ep={(x["ms_file"],x["ms_target"]):x for x in patch_removed}
    added_by_ep={(x["ms_file"],x["ms_target"]):x for x in patch_added}
    candidates=[]
    for highs in itertools.combinations(range(n), proj["high_count"]):
        highset=set(highs)
        assign={ep:("high" if i in highset else "low") for i,ep in enumerate(endpoints)}
        valid=True
        for ep,x in changed_by_ep.items():
            old=x["old"]
            if len(old)!=1 or assign.get(ep)!=old[0]:
                valid=False; break
        if not valid: continue
        for ep,x in removed_by_ep.items():
            old=x["old"]
            if len(old)!=1 or assign.get(ep)!=old[0]:
                valid=False; break
        if not valid: continue
        child=dict(assign)
        for ep,x in changed_by_ep.items():
            if len(x["new"])!=1:
                valid=False; break
            child[ep]=x["new"][0]
        if not valid: continue
        for ep in removed_by_ep:
            child.pop(ep,None)
        for ep,x in added_by_ep.items():
            if len(x["new"])!=1:
                valid=False; break
            child[ep]=x["new"][0]
        if valid:
            candidates.append(tuple(sorted((ep[0],ep[1],cert) for ep,cert in child.items())))
    return sorted(set(candidates))

def independent_regex_parse(raw):
    import re
    text=raw.decode("utf-8")
    rows=[]
    for gm in re.finditer(r'<linkGrp\b[^>]*\btype="relation"[^>]*\bcorresp="([^"]+)"[^>]*>(.*?)</linkGrp>', text, re.S):
        ms_file=gm.group(1)
        body=gm.group(2)
        for lm in re.finditer(r'<link\b([^>]*?)/>',body,re.S):
            attrs=lm.group(1)
            cert=(re.search(r'\bcert="([^"]+)"',attrs) or [None,""])[1]
            target=(re.search(r'\btarget="([^"]+)"',attrs) or [None,""])[1]
            parts=target.split()
            if len(parts)==2:
                rows.append({"print_target":parts[0],"ms_file":ms_file,"ms_target":parts[1],"certainty":cert})
    return rows

def main():
    outdir=Path(__file__).with_name("results")
    outdir.mkdir(parents=True,exist_ok=True)
    praw,craw=fetch(PARENT),fetch(CHILD)
    P,C=parse(praw),parse(craw)
    PS,CS=state(P),state(C)
    PQ,CQ=q0(P),q0(C)
    changed,unchanged,added,removed=derive_delta(P,C)

    # Independent parser/source-reopen cross-check.
    C2=independent_regex_parse(craw)
    source_reopen_exact=state(C2)==CS and len(C2)==len(C)

    # Full-binding update.
    full_after=apply_full_binding(PS,changed,added,removed)
    full_exact=full_after==CS
    natural_delta_keys={
        (x["print_target"],x["ms_file"],x["ms_target"])
        for x in changed+added+removed
    }
    collateral=[
        k for k in set(PS)&set(full_after)
        if k not in natural_delta_keys and PS[k]!=full_after[k]
    ]

    # Endpoint-only retains Q0 and can learn only statuses explicitly present in patch.
    endpoint_only_known={}
    for x in changed:
        if len(x["new"])==1:
            endpoint_only_known[(x["print_target"],x["ms_file"],x["ms_target"])]=x["new"][0]
    for x in added:
        if len(x["new"])==1:
            endpoint_only_known[(x["print_target"],x["ms_file"],x["ms_target"])]=x["new"][0]
    endpoint_only_unresolved=sum(
        len(v) for k,v in CS.items() if k not in endpoint_only_known
    )

    # Locus-status finite determinacy, globally and at naturally affected loci.
    PP=locus_projection(P)
    affected_loci=sorted({x["print_target"] for x in changed+added+removed})
    locus_results={}
    unique_global=0
    unresolved_global=0
    exact_global=0
    for p,proj in PP.items():
        ch=[x for x in changed if x["print_target"]==p]
        ad=[x for x in added if x["print_target"]==p]
        rm=[x for x in removed if x["print_target"]==p]
        cand=enumerate_locus_assignments(proj,ch,rm,ad)
        child_rows=[r for r in C if r["print_target"]==p]
        truth=tuple(sorted((r["ms_file"],r["ms_target"],r["certainty"]) for r in child_rows))
        unique=len(cand)==1
        exact=unique and cand[0]==truth
        if unique: unique_global+=1
        else: unresolved_global+=1
        if exact: exact_global+=1
        if p in affected_loci:
            locus_results[p]={
                "parent_projection":proj,
                "candidate_child_states":len(cand),
                "unique":unique,
                "exact_child_state":exact,
                "child_truth":truth,
            }

    # Wrong-binding control according to frozen rule.
    wrong_control="WRONG_BINDING_CONTROL_NOT_IDENTIFIABLE"
    wrong_details=None
    if len(changed)>=2:
        news=[tuple(x["new"]) for x in changed]
        for shift in range(1,len(changed)):
            perm=news[shift:]+news[:shift]
            wrong=[dict(x,new=list(v)) for x,v in zip(changed,perm)]
            if any(tuple(a["new"])!=tuple(b["new"]) for a,b in zip(changed,wrong)):
                wrong_after=apply_full_binding(PS,wrong,added,removed)
                wrong_control="WRONG_BINDING_FAILS" if wrong_after!=CS else "WRONG_BINDING_UNEXPECTED_PASS"
                wrong_details={"shift":shift,"wrong_exact":wrong_after==CS}
                break

    delta_packet={"changed":changed,"added":added,"removed":removed}
    full_parent_rows=[
        {"print_target":k[0],"ms_file":k[1],"ms_target":k[2],"certainty":list(v)}
        for k,v in sorted(PS.items())
    ]

    # Dependency-aware counts.
    affected_files=sorted({x["ms_file"] for x in changed+added+removed})
    change_dirs=collections.Counter()
    for x in changed:
        if len(x["old"])==1 and len(x["new"])==1:
            change_dirs[f'{x["old"][0]}->{x["new"][0]}']+=1

    result={
        "study":"MODULE_D1_WHITMAN_NATURAL_SELECTIVE_EPISTEMIC_REVISION_V1",
        "authority":"PRE_DIFF_FROZEN_DEVELOPMENT_EVENT_NOT_INDEPENDENT_TRANSFER",
        "source":{
            "repo":UPSTREAM,"path":PATH,
            "parent":{"commit":PARENT,"git_blob":EXPECTED_BLOB[PARENT],"sha256":sha256(praw),"bytes":len(praw)},
            "child":{"commit":CHILD,"git_blob":EXPECTED_BLOB[CHILD],"sha256":sha256(craw),"bytes":len(craw)},
            "child_commit_message":"adjusted certainty",
        },
        "population":{
            "parent_records":len(P),"child_records":len(C),
            "parent_logical_identities":len(PS),"child_logical_identities":len(CS),
            "duplicate_parent_records":len(P)-len(PS),
            "duplicate_child_records":len(C)-len(CS),
        },
        "natural_delta":{
            "cert_changed":len(changed),"unchanged":len(unchanged),
            "added":len(added),"removed":len(removed),
            "affected_print_targets":len(affected_loci),
            "affected_manuscript_files":len(affected_files),
            "change_directions":dict(change_dirs),
            "changed_records":changed,"added_records":added,"removed_records":removed,
        },
        "current_task":{
            "endpoint_multiset_parent_child_equal":PQ==CQ,
            "parent_print_targets":len(PQ),"child_print_targets":len(CQ),
        },
        "arms":{
            "R_FULL_BINDING":{
                "complete_child_state_exact":full_exact,
                "changed_target_correct":all(full_after.get((x["print_target"],x["ms_file"],x["ms_target"]))==tuple(x["new"]) for x in changed),
                "unaffected_stability":all(full_after.get(k)==PS[k] for k in PS if k not in natural_delta_keys and k in full_after),
                "collateral_changes":len(collateral),
            },
            "R_ENDPOINT_ONLY":{
                "q0_endpoint_task_exact":PQ==CQ,
                "changed_statuses_learned_from_delta":len(endpoint_only_known),
                "child_relation_status_items_unresolved":endpoint_only_unresolved,
                "complete_child_state_exact":endpoint_only_unresolved==0,
            },
            "R_LOCUS_STATUS":{
                "printed_targets_with_unique_child_binding":unique_global,
                "printed_targets_with_unresolved_child_binding":unresolved_global,
                "printed_targets_exact_child_binding":exact_global,
                "affected_locus_results":locus_results,
                "affected_loci_all_exact":bool(affected_loci) and all(v["exact_child_state"] for v in locus_results.values()),
                "complete_global_child_state_exact":exact_global==len(PP),
            },
            "R_SOURCE_REOPEN":{
                "independent_parser_exact":source_reopen_exact,
                "complete_child_state_exact":source_reopen_exact,
                "child_source_bytes":len(craw),
            },
        },
        "wrong_binding_control":{"disposition":wrong_control,"details":wrong_details},
        "costs":{
            "natural_delta_packet_json_bytes":len(canonical(delta_packet)),
            "full_parent_state_json_bytes":len(canonical(full_parent_rows)),
            "parent_source_bytes":len(praw),"child_source_bytes":len(craw),
        },
        "dispositions":{
            "NATURAL_EPISTEMIC_REVISION_OBSERVED":len(changed)>0,
            "SELECTIVE_REVISION_FULL_BINDING":full_exact and not collateral,
            "AGGREGATE_STATUS_NONDETERMINING":bool(affected_loci) and not all(v["exact_child_state"] for v in locus_results.values()),
            "AGGREGATE_STATUS_SUFFICIENT_FOR_THIS_EVENT":bool(affected_loci) and all(v["exact_child_state"] for v in locus_results.values()),
            "SOURCE_REOPEN_EXACT":source_reopen_exact,
            "WRONG_BINDING_FAILS":wrong_control=="WRONG_BINDING_FAILS",
        },
        "claim_boundary":[
            "The child certainty value is an editorial epistemic status, not independent genetic truth.",
            "The event was selected from its commit message before the file delta was opened.",
            "Whitman relation data were already exposed in prior project development; this is not independent transfer.",
            "A coarse locus-status representation may be sufficient for this particular event when pre-state homogeneity plus an identity-rich patch uniquely determines the updated binding.",
            "Global locus-status ambiguity outside the affected locus is not attributed to this revision event.",
        ],
    }
    out=outdir/"results.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "population":result["population"],
        "natural_delta":result["natural_delta"],
        "current_task":result["current_task"],
        "arms":result["arms"],
        "wrong_binding_control":result["wrong_binding_control"],
        "costs":result["costs"],
        "dispositions":result["dispositions"],
        "results_sha256":sha256(out.read_bytes()),
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
