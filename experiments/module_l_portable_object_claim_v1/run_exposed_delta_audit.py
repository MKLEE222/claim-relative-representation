from __future__ import annotations

import io
import json
import sys
import tarfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
J_DIR = HERE.parent / "module_j_dahn_object_bound_holdout_v1"
if str(J_DIR) not in sys.path:
    sys.path.insert(0, str(J_DIR))

import run_reaudit as jr
import oracle_j
import oracle_l

CTX = {
    "source_repository": jr.UPSTREAM_REPO,
    "source_version": jr.UPSTREAM_COMMIT,
    "population_scope": "EXPOSED_DAHN_DELTA_AUDIT_ONLY",
}


def claim_core(c):
    return (
        c.get("role"),
        tuple(c.get("interval") or []),
        c.get("source_locator_contract"),
    )


def multiset_diff(a, b):
    ca, cb = Counter(map(claim_core, a)), Counter(map(claim_core, b))
    added = []
    removed = []
    for k in sorted(set(ca) | set(cb), key=str):
        if cb[k] > ca[k]:
            added.extend([k] * (cb[k] - ca[k]))
        if ca[k] > cb[k]:
            removed.extend([k] * (ca[k] - cb[k]))
    def row(x):
        return {"role": x[0], "interval": list(x[1]), "locator_contract": x[2]}
    return [row(x) for x in added], [row(x) for x in removed]


def iter_xml(prefix, archive_raw):
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tf:
        members = []
        for m in tf.getmembers():
            if not m.isfile():
                continue
            parts = Path(m.name).parts
            if len(parts) < 2:
                continue
            rel = str(Path(*parts[1:]))
            if rel.startswith(prefix) and rel.lower().endswith(".xml"):
                members.append((rel, m))
        for rel, m in sorted(members, key=lambda x: x[0]):
            f = tf.extractfile(m)
            if f is not None:
                yield rel, f.read()


def main():
    archive_url = f"https://github.com/{jr.UPSTREAM_REPO}/archive/{jr.UPSTREAM_COMMIT}.tar.gz"
    archive_raw = jr.fetch(archive_url)

    report = {
        "study": "MODULE_L_EXPOSED_J_TO_L_DELTA_AUDIT_V1",
        "interpretation": (
            "EXPOSED DIAGNOSTIC ONLY. Explains contract-induced J-to-L changes before any "
            "new independent population is opened."
        ),
        "source_context": CTX,
        "archive_sha256": jr.sha256(archive_raw),
        "corpora": {},
    }

    for name, prefix in jr.EXPOSED_PREFIXES.items():
        changed = []
        errors = []
        summary = Counter()

        for path, raw in iter_xml(prefix, archive_raw):
            try:
                j = oracle_j.parse_document(path, raw)
                l = oracle_l.parse_document(path, raw, CTX)
            except Exception as e:
                errors.append({"path": path, "error": repr(e)})
                continue

            js = (j.get("object_contract") or {}).get("status")
            ls = (l.get("object_contract") or {}).get("status")
            je = bool((j.get("eligibility") or {}).get("eligible"))
            le = bool((l.get("eligibility") or {}).get("eligible"))
            jf = bool(j.get("full_trajectory_eligible"))
            lf = bool(l.get("full_trajectory_eligible"))

            labels = []
            if js != ls:
                labels.append(f"OBJECT:{js}->{ls}")
                summary[f"OBJECT:{js}->{ls}"] += 1
            if je != le:
                labels.append(f"DISCOVERY:{int(je)}->{int(le)}")
                summary[f"DISCOVERY:{int(je)}->{int(le)}"] += 1
            if jf != lf:
                labels.append(f"FULL:{int(jf)}->{int(lf)}")
                summary[f"FULL:{int(jf)}->{int(lf)}"] += 1

            if labels:
                added, removed = multiset_diff(j.get("claims", []), l.get("claims", []))
                changed.append({
                    "path": path,
                    "labels": labels,
                    "j_object_status": js,
                    "l_object_status": ls,
                    "j_boundary_kind": (j.get("object_contract") or {}).get("boundary_kind"),
                    "l_boundary_kind": (l.get("object_contract") or {}).get("boundary_kind"),
                    "j_eligible": je,
                    "l_eligible": le,
                    "j_trigger": (j.get("eligibility") or {}).get("trigger"),
                    "l_trigger": (l.get("eligibility") or {}).get("trigger"),
                    "j_full": jf,
                    "l_full": lf,
                    "j_full_reasons": j.get("full_trajectory_exclusion_reasons"),
                    "l_full_reasons": l.get("full_trajectory_exclusion_reasons"),
                    "added_active_claims": added,
                    "removed_active_claims": removed,
                    "j_origin_contract": j.get("origin_contract_status"),
                    "l_origin_contract": l.get("origin_contract_status"),
                })

        report["corpora"][name] = {
            "prefix": prefix,
            "errors": errors,
            "change_summary": dict(summary),
            "changed_documents": changed,
        }

    out_dir = HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "j_to_l_delta_audit_v1.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if any(x["errors"] for x in report["corpora"].values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
