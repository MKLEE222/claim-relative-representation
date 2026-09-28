from __future__ import annotations

import collections
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

VAR_REPO = "whitmanarchive/whitman-LG_1855_variorum"
VAR_COMMIT = "25a00b7ebbdbc5246fce65a333bc761a5c22dad4"
REL_PATH = "source/authority/anc.02134.xml"
PRINT_PATH = "source/tei/ppp.01880.xml"
REL_BLOB = "11d6f7508c8bfd120d390d31c49d2399e38b5337"
PRINT_BLOB = "676c84cb48cdb2edaa6f72f68ae9d489a2beff22"

SOURCES = {
    "manuscripts": {
        "repo": "whitmanarchive/whitman-manuscripts",
        "commit": "249bc14594fa1c0428e7ca39f52753de21ce604b",
        "tree": "1871715fbcef5f9721e80f385471a86ad52ef463",
    },
    "notebooks": {
        "repo": "whitmanarchive/whitman-notebooks",
        "commit": "682c04c0998739b8edfd75e0e7496592777e2898",
        "tree": "90ce5a76b2358d3350e889b6988af8e26bcdd835",
    },
}

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-whitman-route-v2/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def parse_ids(raw):
    root = ET.fromstring(raw)
    return {e.attrib[XML_ID] for e in root.iter() if XML_ID in e.attrib}

def load_repo(label, spec):
    tree_url = f"https://api.github.com/repos/{spec['repo']}/git/trees/{spec['tree']}?recursive=1"
    archive_url = f"https://github.com/{spec['repo']}/archive/{spec['commit']}.tar.gz"
    tree_raw = fetch(tree_url)
    tree_obj = json.loads(tree_raw)
    if tree_obj.get("sha") != spec["tree"]:
        raise RuntimeError(f"{label} tree drift")
    tree_map = {
        x["path"]: x["sha"]
        for x in tree_obj.get("tree", [])
        if x.get("type") == "blob"
    }
    archive_raw = fetch(archive_url)
    extracted = {}
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            parts = Path(m.name).parts
            if len(parts) < 2:
                continue
            f = tf.extractfile(m)
            if f is not None:
                extracted[str(Path(*parts[1:]))] = f.read()
    return {
        "spec": spec,
        "tree_map": tree_map,
        "files": extracted,
        "archive_sha256": sha256(archive_raw),
    }

def main():
    outdir = Path(__file__).with_name("results_route_v2")
    outdir.mkdir(parents=True, exist_ok=True)

    rel_raw = fetch(f"https://raw.githubusercontent.com/{VAR_REPO}/{VAR_COMMIT}/{REL_PATH}")
    print_raw = fetch(f"https://raw.githubusercontent.com/{VAR_REPO}/{VAR_COMMIT}/{PRINT_PATH}")
    if git_blob(rel_raw) != REL_BLOB:
        raise RuntimeError("relation drift")
    if git_blob(print_raw) != PRINT_BLOB:
        raise RuntimeError("printed source drift")

    repos = {k: load_repo(k, v) for k, v in SOURCES.items()}

    root = ET.fromstring(rel_raw)
    records = []
    for g in root.findall(".//tei:linkGrp[@type='relation']", NS):
        ms_file = (g.attrib.get("corresp") or "").strip()
        for link in g.findall("./tei:link", NS):
            parts = (link.attrib.get("target") or "").split()
            if len(parts) != 2:
                raise RuntimeError("unexpected target shape")
            ptoken, mtoken = parts
            pfile, plocus = ptoken.split("#", 1)
            records.append({
                "print_file": pfile,
                "print_locus": plocus,
                "ms_file": ms_file,
                "ms_locus": mtoken[1:] if mtoken.startswith("#") else mtoken,
                "certainty": (link.attrib.get("cert") or "").strip(),
            })

    printed_ids = parse_ids(print_raw)

    file_route = {}
    all_files = sorted({r["ms_file"] for r in records})
    for ms_file in all_files:
        path = f"source/tei/{ms_file}"
        hits = [label for label, repo in repos.items() if path in repo["tree_map"]]
        if len(hits) == 1:
            file_route[ms_file] = {"status": "ROUTED", "repository": hits[0], "path": path}
        elif len(hits) == 0:
            file_route[ms_file] = {"status": "SOURCE_FILE_UNRESOLVED", "repository": None, "path": path}
        else:
            file_route[ms_file] = {"status": "AMBIGUOUS_SOURCE_REPOSITORY", "repository": hits, "path": path}

    if any(v["status"] == "AMBIGUOUS_SOURCE_REPOSITORY" for v in file_route.values()):
        raise RuntimeError("unexpected cross-repo filename ambiguity")

    id_cache = {}
    for ms_file, route in file_route.items():
        if route["status"] != "ROUTED":
            continue
        label = route["repository"]
        repo = repos[label]
        raw = repo["files"].get(route["path"])
        if raw is None:
            raise RuntimeError(f"tree/archive mismatch for {label}:{route['path']}")
        expected = repo["tree_map"][route["path"]]
        got = git_blob(raw)
        if got != expected:
            raise RuntimeError(f"blob mismatch for {label}:{route['path']}")
        id_cache[ms_file] = parse_ids(raw)
        route["blob"] = expected
        route["bytes"] = len(raw)
        route["xml_id_count"] = len(id_cache[ms_file])

    rows = []
    counts = collections.defaultdict(collections.Counter)
    unresolved_files = collections.Counter()
    unresolved_ids = collections.Counter()
    for r in records:
        print_ok = r["print_file"] == "ppp.01880.xml" and r["print_locus"] in printed_ids
        route = file_route[r["ms_file"]]
        file_ok = route["status"] == "ROUTED"
        id_ok = file_ok and r["ms_locus"] in id_cache[r["ms_file"]]
        complete = print_ok and file_ok and id_ok

        if not file_ok:
            unresolved_files[r["ms_file"]] += 1
        elif not id_ok:
            unresolved_ids[r["ms_file"]] += 1

        for key, val in [
            ("printed", print_ok),
            ("file", file_ok),
            ("local_id", id_ok),
            ("complete", complete),
        ]:
            counts[r["certainty"]][f"{key}_{'ok' if val else 'fail'}"] += 1

        rows.append({
            **r,
            "route_status": route["status"],
            "repository": route.get("repository"),
            "printed_locus_resolves": print_ok,
            "manuscript_file_resolves": file_ok,
            "manuscript_locus_resolves": id_ok,
            "complete_route_resolves": complete,
        })

    by_repo_files = collections.Counter(
        v["repository"]
        for v in file_route.values()
        if v["status"] == "ROUTED"
    )

    result = {
        "study": "MODULE_B2_WHITMAN_SOURCE_ROUTE_V2",
        "authority": "POST_V1_SOURCE_CONTRACT_REPAIR_ON_EXPOSED_DEVELOPMENT_DATA",
        "population": {
            "relation_links": len(records),
            "distinct_corresp_files": len(all_files),
            "routed_files_by_repository": dict(by_repo_files),
            "unresolved_files": sum(v["status"] == "SOURCE_FILE_UNRESOLVED" for v in file_route.values()),
        },
        "source_snapshots": {
            label: {
                "repo": repo["spec"]["repo"],
                "commit": repo["spec"]["commit"],
                "tree": repo["spec"]["tree"],
                "archive_sha256": repo["archive_sha256"],
            }
            for label, repo in repos.items()
        },
        "route_results": {
            "complete_links": sum(x["complete_route_resolves"] for x in rows),
            "unresolved_links": sum(not x["complete_route_resolves"] for x in rows),
            "by_certainty": {k: dict(v) for k, v in counts.items()},
            "unresolved_file_counts": dict(unresolved_files),
            "unresolved_local_id_counts": dict(unresolved_ids),
            "file_route": file_route,
        },
        "claim_boundary": [
            "This v2 audit repairs only the source-routing contract; it does not change the certainty-binding experiment.",
            "The two repositories are pinned to contemporaneous 2019 snapshots.",
            "A source file or xml:id absent from these snapshots is an access/version finding, not proof that the editorial relation is false.",
            "No later repository state is used in the primary metric.",
        ],
    }

    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "route_records.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "population": result["population"],
        "route_results": {
            "complete_links": result["route_results"]["complete_links"],
            "unresolved_links": result["route_results"]["unresolved_links"],
            "by_certainty": result["route_results"]["by_certainty"],
            "unresolved_file_counts": result["route_results"]["unresolved_file_counts"],
            "unresolved_local_id_counts": result["route_results"]["unresolved_local_id_counts"],
        },
        "results_sha256": sha256(out.read_bytes()),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
