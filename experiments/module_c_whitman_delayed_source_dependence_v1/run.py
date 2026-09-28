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

ENVIRONMENTS = {
    "E2019": {
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
    },
    "ECURRENT": {
        "manuscripts": {
            "repo": "whitmanarchive/whitman-manuscripts",
            "commit": "2fe2c934f0b63ce66d4e43f36798767785f2b70c",
            "tree": "6a0372f5d3e111226f6a96bedaa8724ef18c5854",
        },
        "notebooks": {
            "repo": "whitmanarchive/whitman-notebooks",
            "commit": "a7b000f613e4c4fcf38cec4d58aebd6c857ffe37",
            "tree": "b1c6b7d631c04fae49939f24cadd66eba697b6cc",
        },
    },
}

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-C/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()

def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def parse_ids(raw):
    root = ET.fromstring(raw)
    return {e.attrib[XML_ID] for e in root.iter() if XML_ID in e.attrib}

def load_repo(spec):
    tree_raw = fetch(
        f"https://api.github.com/repos/{spec['repo']}/git/trees/{spec['tree']}?recursive=1"
    )
    tree_obj = json.loads(tree_raw)
    if tree_obj.get("sha") != spec["tree"]:
        raise RuntimeError(f"tree drift for {spec['repo']} {spec['commit']}")
    tree_map = {
        x["path"]: x["sha"]
        for x in tree_obj.get("tree", [])
        if x.get("type") == "blob"
    }
    archive_raw = fetch(
        f"https://github.com/{spec['repo']}/archive/{spec['commit']}.tar.gz"
    )
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            parts = Path(m.name).parts
            if len(parts) < 2:
                continue
            f = tf.extractfile(m)
            if f is not None:
                files[str(Path(*parts[1:]))] = f.read()
    return {
        "tree_map": tree_map,
        "files": files,
        "archive_sha256": sha256(archive_raw),
        "spec": spec,
    }

def load_environment(spec):
    return {label: load_repo(repo_spec) for label, repo_spec in spec.items()}

def route_file(env, filename):
    path = f"source/tei/{filename}"
    hits = [label for label, repo in env.items() if path in repo["tree_map"]]
    if len(hits) == 0:
        return {"status": "MISSING_FILE", "repository": None, "path": path}
    if len(hits) > 1:
        return {"status": "AMBIGUOUS_REPOSITORY", "repository": sorted(hits), "path": path}
    label = hits[0]
    repo = env[label]
    raw = repo["files"].get(path)
    if raw is None:
        raise RuntimeError(f"tree/archive mismatch {label}:{path}")
    expected = repo["tree_map"][path]
    got = git_blob(raw)
    if got != expected:
        raise RuntimeError(f"blob mismatch {label}:{path}")
    return {
        "status": "FILE_OK",
        "repository": label,
        "path": path,
        "blob": expected,
        "bytes": len(raw),
        "ids": parse_ids(raw),
    }

def main():
    outdir = Path(__file__).with_name("results")
    outdir.mkdir(parents=True, exist_ok=True)

    rel_raw = fetch(
        f"https://raw.githubusercontent.com/{VAR_REPO}/{VAR_COMMIT}/{REL_PATH}"
    )
    print_raw = fetch(
        f"https://raw.githubusercontent.com/{VAR_REPO}/{VAR_COMMIT}/{PRINT_PATH}"
    )
    if git_blob(rel_raw) != REL_BLOB:
        raise RuntimeError("relation source drift")
    if git_blob(print_raw) != PRINT_BLOB:
        raise RuntimeError("printed source drift")

    relation_root = ET.fromstring(rel_raw)
    printed_ids = parse_ids(print_raw)

    records = []
    for g in relation_root.findall(".//tei:linkGrp[@type='relation']", NS):
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

    envs = {name: load_environment(spec) for name, spec in ENVIRONMENTS.items()}
    file_routes = {name: {} for name in envs}
    for env_name, env in envs.items():
        for filename in sorted({r["ms_file"] for r in records}):
            file_routes[env_name][filename] = route_file(env, filename)

    rows = []
    trajectories = collections.Counter()
    by_certainty = collections.defaultdict(collections.Counter)
    reason_transitions = collections.Counter()
    file_trajectory_sets = collections.defaultdict(set)

    env_counts = {name: collections.Counter() for name in envs}

    for r in records:
        states = {}
        for env_name in envs:
            route = file_routes[env_name][r["ms_file"]]
            print_ok = r["print_file"] == "ppp.01880.xml" and r["print_locus"] in printed_ids
            if route["status"] == "MISSING_FILE":
                state = "MISSING_FILE"
            elif route["status"] == "AMBIGUOUS_REPOSITORY":
                state = "AMBIGUOUS_REPOSITORY"
            else:
                state = "RESOLVED" if r["ms_locus"] in route["ids"] else "MISSING_LOCAL_ID"
            states[env_name] = state
            env_counts[env_name][state] += 1
            env_counts[env_name]["PRINT_OK" if print_ok else "PRINT_FAIL"] += 1

        a, b = states["E2019"], states["ECURRENT"]
        a_ok, b_ok = a == "RESOLVED", b == "RESOLVED"
        if a_ok and b_ok:
            traj = "STABLE_RESOLVED"
        elif (not a_ok) and b_ok:
            traj = "REPAIRED_OVER_TIME"
        elif a_ok and (not b_ok):
            traj = "BROKEN_OVER_TIME"
        else:
            traj = "STABLE_UNRESOLVED"

        trajectories[traj] += 1
        by_certainty[r["certainty"]][traj] += 1
        reason_transitions[(a, b)] += 1
        file_trajectory_sets[traj].add(r["ms_file"])
        rows.append({**r, "E2019": a, "ECURRENT": b, "trajectory": traj})

    # Branch-specific continuation executability: low-certainty links.
    low = [x for x in rows if x["certainty"] == "low"]
    high = [x for x in rows if x["certainty"] == "high"]

    def route_summary(subset):
        return {
            "links": len(subset),
            "resolved_E2019": sum(x["E2019"] == "RESOLVED" for x in subset),
            "resolved_ECURRENT": sum(x["ECURRENT"] == "RESOLVED" for x in subset),
            "stable_resolved": sum(x["trajectory"] == "STABLE_RESOLVED" for x in subset),
            "repaired_over_time": sum(x["trajectory"] == "REPAIRED_OVER_TIME" for x in subset),
            "broken_over_time": sum(x["trajectory"] == "BROKEN_OVER_TIME" for x in subset),
            "stable_unresolved": sum(x["trajectory"] == "STABLE_UNRESOLVED" for x in subset),
        }

    # File-level repository motion independent of local IDs.
    file_motion = collections.Counter()
    file_details = []
    for filename in sorted({r["ms_file"] for r in records}):
        a = file_routes["E2019"][filename]
        b = file_routes["ECURRENT"][filename]
        a_ok = a["status"] == "FILE_OK"
        b_ok = b["status"] == "FILE_OK"
        if a_ok and b_ok:
            cls = "FILE_STABLE_PRESENT"
        elif (not a_ok) and b_ok:
            cls = "FILE_ADDED_OR_ROUTED"
        elif a_ok and (not b_ok):
            cls = "FILE_REMOVED_OR_AMBIGUOUS"
        else:
            cls = "FILE_STABLE_UNRESOLVED"
        file_motion[cls] += 1
        file_details.append({
            "ms_file": filename,
            "class": cls,
            "E2019": {k: v for k, v in a.items() if k != "ids"},
            "ECURRENT": {k: v for k, v in b.items() if k != "ids"},
        })

    result = {
        "study": "MODULE_C_WHITMAN_DELAYED_SOURCE_DEPENDENCE_V1",
        "authority": "NATURAL_VERSIONED_DEVELOPMENT_STRESS_TEST",
        "fixed_relation": {
            "repo": VAR_REPO,
            "commit": VAR_COMMIT,
            "path": REL_PATH,
            "git_blob": REL_BLOB,
            "sha256": sha256(rel_raw),
            "links": len(records),
        },
        "environments": {
            env_name: {
                label: {
                    "repo": repo["spec"]["repo"],
                    "commit": repo["spec"]["commit"],
                    "tree": repo["spec"]["tree"],
                    "archive_sha256": repo["archive_sha256"],
                }
                for label, repo in env.items()
            }
            for env_name, env in envs.items()
        },
        "current_endpoint_strings": {
            "unchanged_by_construction": True,
            "unique_print_loci": len({r["print_locus"] for r in records}),
            "link_count": len(records),
        },
        "link_trajectories": {
            "counts": dict(trajectories),
            "by_certainty": {k: dict(v) for k, v in by_certainty.items()},
            "reason_transitions": {
                f"{a}->{b}": n for (a, b), n in sorted(reason_transitions.items())
            },
            "distinct_source_files_by_trajectory": {
                k: len(v) for k, v in file_trajectory_sets.items()
            },
        },
        "environment_state_counts": {
            k: dict(v) for k, v in env_counts.items()
        },
        "low_certainty_continuation": route_summary(low),
        "high_certainty_comparator": route_summary(high),
        "file_motion": {
            "counts": dict(file_motion),
            "details": file_details,
        },
        "dispositions": {
            "ENDPOINT_STRINGS_STABLE": True,
            "SOURCE_ROUTE_EXECUTABILITY_CHANGED": (
                trajectories["REPAIRED_OVER_TIME"] + trajectories["BROKEN_OVER_TIME"] > 0
            ),
            "LOW_CERTAINTY_CONTINUATION_CHANGED": (
                route_summary(low)["repaired_over_time"] + route_summary(low)["broken_over_time"] > 0
            ),
            "NATURAL_VERSION_DRIFT_OBSERVED": (
                trajectories["REPAIRED_OVER_TIME"] + trajectories["BROKEN_OVER_TIME"] > 0
            ),
            "DEPLOYED_ARCHIVE_FAILURE": False,
            "INDEPENDENT_TRANSFER": False,
        },
        "claim_boundary": [
            "The relation inventory and printed side are fixed while source repositories change.",
            "This audits GitHub source snapshots, not the deployed Whitman Archive service.",
            "A missing route is not evidence that the editorial relation is false.",
            "No alias/fuzzy-ID repair is introduced after outcome.",
            "Links sharing files are dependent observations; counts are finite-population route counts, not independent replicates.",
        ],
    }

    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "route_trajectories.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "link_trajectories": result["link_trajectories"],
        "low_certainty_continuation": result["low_certainty_continuation"],
        "high_certainty_comparator": result["high_certainty_comparator"],
        "file_motion_counts": result["file_motion"]["counts"],
        "dispositions": result["dispositions"],
        "results_sha256": sha256(out.read_bytes()),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
