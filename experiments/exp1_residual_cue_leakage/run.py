from __future__ import annotations
import csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATTERNS = {
    "attribution": [
        r"bretschneider", r"laufer", r"tanner", r"moule", r"richthofen",
        r"queen", r"pauthier", r"g\.\s*text", r"h\.\s*c\.", r"writes to me",
        r"written statement", r"rev\."
    ],
    "temporal_order": [
        r"regarding .*statement", r"p\.\s*\d+", r"later", r"addenda?", r"prior",
        r"after", r"in 1901", r"1915", r"1919", r"1903", r"1920", r"earlier"
    ],
    "evidence_relation": [
        r"error", r"correct", r"wrong", r"only one", r"merely", r"shows",
        r"conclud", r"neither .* nor .* but", r"future", r"probable",
        r"mistaken", r"witnessed the truth"
    ],
    "claim_binding": [
        r"paper[- ]?money", r"mulberry", r"bark", r"kinsay", r"hang\s*chau",
        r"revenue", r"marco polo", r"coal", r"black stones", r"fuel"
    ],
}

def load():
    with open(ROOT / "experiments/exp1_residual_cue_leakage/inputs.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def hits(text, patterns):
    found=[]
    for p in patterns:
        if re.search(p, text, flags=re.I):
            found.append(p)
    return found

rows=load()
print("EXP1A_RESIDUAL_CUE_LEAKAGE")
print("event_ref,coordinate,residual_cue,cue_count")
counts={k:0 for k in PATTERNS}
n=len(rows)
for row in rows:
    for coord, pats in PATTERNS.items():
        h=hits(row["text"], pats)
        if h:
            counts[coord]+=1
        print(f'{row["event_ref"]},{coord},{"YES" if h else "NO"},{len(h)}')
print("SUMMARY")
for coord in PATTERNS:
    print(f"{coord}={counts[coord]}/{n}")
