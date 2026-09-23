from __future__ import annotations

import csv
import sys
from pathlib import Path

REQUIRED = {
    "item_id","primitive_labels","claim_binding","attribution_actor",
    "attribution_status","temporal_relation","representation_status",
    "uncertainty_note","coder_id","coded_without_provisional_decision"
}

def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def splitset(x):
    return {v.strip() for v in (x or "").split("|") if v.strip()}

def by_id(rows):
    return {r["item_id"]: r for r in rows}

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: score_coder_agreement.py coder_a.csv coder_b.csv")
    a = read(sys.argv[1])
    b = read(sys.argv[2])

    for name, rows in (("A", a), ("B", b)):
        if not rows:
            raise SystemExit(f"coder {name}: empty file")
        if set(rows[0].keys()) != REQUIRED:
            raise SystemExit(f"coder {name}: schema mismatch")
        for r in rows:
            if r["coded_without_provisional_decision"].strip().lower() not in {"yes","true","1"}:
                raise SystemExit(f'coder {name}: leakage declaration missing for {r["item_id"]}')

    A, B = by_id(a), by_id(b)
    if set(A) != set(B):
        raise SystemExit("coder item sets differ")

    exact = 0
    jaccards = []
    binding = 0
    repstat = 0
    disagreements = []

    all_labels = set()
    for item in sorted(A):
        sa, sb = splitset(A[item]["primitive_labels"]), splitset(B[item]["primitive_labels"])
        all_labels |= sa | sb
        if sa == sb:
            exact += 1
        union = sa | sb
        j = 1.0 if not union else len(sa & sb) / len(union)
        jaccards.append(j)
        if A[item]["claim_binding"] == B[item]["claim_binding"]:
            binding += 1
        if A[item]["representation_status"] == B[item]["representation_status"]:
            repstat += 1
        if sa != sb or A[item]["claim_binding"] != B[item]["claim_binding"] or A[item]["representation_status"] != B[item]["representation_status"]:
            disagreements.append(item)

    n = len(A)
    print(f"items={n}")
    print(f"primitive_exact={exact}/{n} ({exact/n:.3f})")
    print(f"primitive_mean_jaccard={sum(jaccards)/n:.3f}")
    print(f"claim_binding_exact={binding}/{n} ({binding/n:.3f})")
    print(f"representation_status_exact={repstat}/{n} ({repstat/n:.3f})")
    print("disagreement_items=" + ("|".join(disagreements) if disagreements else "NONE"))

    for label in sorted(all_labels):
        pa = {i for i,r in A.items() if label in splitset(r["primitive_labels"])}
        pb = {i for i,r in B.items() if label in splitset(r["primitive_labels"])}
        both = len(pa & pb)
        either = len(pa | pb)
        print(f"label={label} both={both} either={either}")

if __name__ == "__main__":
    main()
