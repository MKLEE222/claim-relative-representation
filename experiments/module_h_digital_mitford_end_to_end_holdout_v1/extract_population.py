from __future__ import annotations

import hashlib
import html
import json
import re
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

from lxml import etree as ET

JOURNAL_REPO = "DigitalMitford/DM_Journal_1819-1823"
SI_REPO = "DigitalMitford/DM_SiteIndex"
JOURNAL_PATH = "1819-1823MRMJournal.xml"
SI_PATH = "si_Full_Staged/si.xml"
GOLD_PATH = "PossibleMissingSI.md"

CHECKPOINTS = {
    "T0": {
        "journal_commit": "63aaa047b2d47cfc6508243de923a06a50f47ad1",
        "journal_blob": "73685378fe4f9dc8d020de852429aa24f3840118",
        "si_commit": "d3709c5fd56557aa5c6159216befa300b64492d1",
        "si_blob": "680a120a84cd540e45757319fb78881670da921c",
        "gold_commit": "949015ba5e40924e91a79a2623041faffa3f05e0",
        "gold_blob": "31a074d4fd947f423d6d8c376ae15a390e721991",
    },
    "T1": {
        "journal_commit": "9b163a79ff3520c569cd59d1052cde4dd90c46ad",
        "journal_blob": "96ab590429a251c30cd50061ba927cb1aaa9ac12",
        "si_commit": "8f9bd9307167821aa2ca8980302d535b7624a1ee",
        "si_blob": "680a120a84cd540e45757319fb78881670da921c",
        "gold_commit": "3079aced583df6b6e078d9765ac474fc9a40ec21",
        "gold_blob": "119986d3c6273373889b465355796cc2b7d7274a",
    },
    "T2": {
        "journal_commit": "5af102123dbd35165b3c86c07795eed79a26870a",
        "journal_blob": "15cc24698161364481f77c5f6581b8ba2d77381a",
        "si_commit": "8f9bd9307167821aa2ca8980302d535b7624a1ee",
        "si_blob": "680a120a84cd540e45757319fb78881670da921c",
        "gold_commit": "04ac6104870a71dd882bed6b49d9366287fd8433",
        "gold_blob": "ecaaeaa5427fa78d6a8023755c7f0ef226376f7f",
    },
    "T3": {
        "journal_commit": "fd8e86cfab62b18dc44a4a7f163a5fc10ea98c00",
        "journal_blob": "6a89e117d8d7772e59dfdfa60aad9f5e81b59661",
        "si_commit": "791a8bfeb470a44493c2d145427ac34c21cd13f6",
        "si_blob": "2cc9623e9cd0426e5a4af529cbf2f53aefd4310b",
        "gold_commit": "a9f9531bfa8d476c657fae502ec1591c434689d5",
        "gold_blob": "e464300acbdcfab9ae342675c9874426ede06e95",
    },
}

EXPOSED = [
    "lovejoy_martha", "martha lovejoy",
    "parry_mrs", "mrs. parry", "mrs parry",
    "bailey_mr", "mr. bailey", "mr bailey",
    "dobbs_mr", "dobbs_mrs", "mr. dobbs", "mr dobbs", "mrs. dobbs", "mrs dobbs",
    "wheeler_james", "wheeler_j", "wheeler_john", "wheeler_mr", "wheeler_kate", "miss wheeler",
    "webb_mary", "webb_mary_elder", "webb_mary_younger",
    "mr. bayley", "mr bayley", "bayley_p",
    "mr. brocas", "mr brocas", "brocas_bernard",
    "mr. c. kemble", "mr c kemble", "kemble_c",
    "bisset_r", "robert bisset",
    "nicholls_john", "john bowyer nichols", "john wright",
    "cook1", "cook2",
]

CHECK_RE = re.compile(r"^\s*[-*]\s*\[([ xX])\]\s*(.*)$")
TAG_RE = re.compile(r"<[^>]+>")
ID_RE = re.compile(r"(?<![A-Za-z0-9])#?([A-Za-z][A-Za-z0-9.-]*_[A-Za-z0-9_.-]+)(?![A-Za-z0-9])")
HONORIFICS = {"mr", "mrs", "miss", "ms", "sir", "lady", "lord", "dr", "rev"}


def fetch(repo: str, commit: str, path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "CRR-module-H0/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = TAG_RE.sub(" ", s)
    s = s.replace("::", " :: ")
    s = " ".join(s.split())
    return s.casefold().strip()


def key_text(body: str) -> str:
    return norm(body.split("::", 1)[0])


def strip_ref(v: str | None) -> str | None:
    if not v:
        return None
    v = v.strip()
    if " " in v:
        v = v.split()[0]
    return v[1:] if v.startswith("#") else v


def lname(el) -> str:
    return ET.QName(el).localname


def parse_journal(raw: bytes):
    # The frozen Journal snapshots contain malformed outer XML in some checkpoints.
    # H0 therefore extracts only complete literal persName fragments from immutable
    # source text. No recovery tree or source rewrite is used.
    text = raw.decode("utf-8")
    pers_re = re.compile(r"<persName\b([^>]*)>([\s\S]*?)</persName\s*>")
    ref_re = re.compile(r"\bref\s*=\s*([\"'])(.*?)\1", re.S)
    comment_re = re.compile(r"<!--[\s\S]*?-->")
    mentions = []
    by_id = defaultdict(list)
    by_surface = defaultdict(list)
    ordinal = 0
    for m in pers_re.finditer(text):
        ordinal += 1
        attrs = m.group(1)
        inner = comment_re.sub(" ", m.group(2))
        surface = html.unescape(TAG_RE.sub(" ", inner))
        surface = " ".join(surface.split())
        if not surface:
            continue
        rm = ref_re.search(attrs)
        ref = strip_ref(rm.group(2) if rm else None)
        rec = {
            "surface": surface,
            "surface_norm": norm(surface),
            "ref": ref,
            "path": f"raw_char:{m.start()}-{m.end()}",
            "ordinal": ordinal,
        }
        mentions.append(rec)
        if ref:
            by_id[ref.casefold()].append(rec)
        by_surface[rec["surface_norm"]].append(rec)
    if not mentions:
        raise RuntimeError("Journal raw-span parser found no complete persName fragments")
    return {
        "mentions": mentions,
        "by_id": dict(by_id),
        "by_surface": dict(by_surface),
    }


def parse_si(raw: bytes):
    root = ET.fromstring(raw, ET.XMLParser(resolve_entities=False, no_network=True, recover=False, collect_ids=False))
    persons = {}
    name_index = defaultdict(set)
    for el in root.iter():
        if lname(el) != "person":
            continue
        pid = el.get("{http://www.w3.org/XML/1998/namespace}id")
        if not pid:
            continue
        names = []
        for d in el.iterdescendants():
            if lname(d) == "persName":
                txt = " ".join(" ".join(d.itertext()).split())
                if txt:
                    names.append(txt)
        note_texts = []
        for d in el.iterdescendants():
            if lname(d) == "note":
                txt = " ".join(" ".join(d.itertext()).split())
                if txt:
                    note_texts.append(txt)
        rec = {
            "id": pid,
            "names": names,
            "names_norm": sorted({norm(x) for x in names if norm(x)}),
            "notes": note_texts,
        }
        persons[pid.casefold()] = rec
        for n in rec["names_norm"]:
            name_index[n].add(pid)
    return {
        "persons": persons,
        "name_index": {k: sorted(v) for k, v in name_index.items()},
    }


def parse_gold(raw: bytes):
    text = raw.decode("utf-8")
    rows = []
    seen = Counter()
    for line_no, line in enumerate(text.splitlines(), 1):
        m = CHECK_RE.match(line)
        if not m:
            continue
        checked = m.group(1).lower() == "x"
        body = m.group(2).strip()
        k = key_text(body)
        seen[k] += 1
        rows.append({
            "line_no": line_no,
            "checked": checked,
            "body": body,
            "stable_text": k,
            "ordinal": seen[k],
            "key": f"{k}@@{seen[k]}",
        })
    dup_keys = {k for k, n in seen.items() if n > 1}
    return rows, dup_keys


def exposed(row) -> bool:
    h = norm(row["body"])
    return any(norm(x) in h for x in EXPOSED)


def candidate_source_matches(row, journal, si):
    body = row["body"]
    body_norm = norm(body)
    ids = {x.casefold() for x in ID_RE.findall(body)}

    matches = {}
    # Direct ID matches are strongest.
    for x in ids:
        if x in si["persons"]:
            matches[f"id:{si['persons'][x]['id']}"] = {
                "type": "si_id",
                "id": si["persons"][x]["id"],
            }
        if x in journal["by_id"]:
            for rec in journal["by_id"][x]:
                matches[f"journal_id:{x}:{rec['path']}"] = {
                    "type": "journal_ref",
                    "id": rec["ref"],
                    "surface": rec["surface"],
                    "path": rec["path"],
                }

    # Match exact known person names/surfaces contained in the checklist prefix.
    prefix = row["stable_text"]
    for n, pids in si["name_index"].items():
        if len(n) < 3:
            continue
        if n == prefix or n in prefix or prefix in n:
            for pid in pids:
                matches[f"si_name:{pid}:{n}"] = {
                    "type": "si_name",
                    "id": pid,
                    "name": n,
                }

    for surf, recs in journal["by_surface"].items():
        if len(surf) < 3:
            continue
        if surf == prefix or surf in prefix or prefix in surf:
            for rec in recs:
                matches[f"journal_surface:{rec['path']}"] = {
                    "type": "journal_surface",
                    "id": rec["ref"],
                    "surface": rec["surface"],
                    "path": rec["path"],
                }

    # Conservative honorific/surname fallback for short checklist labels.
    toks = [re.sub(r"[^a-z0-9'-]", "", t) for t in prefix.split()]
    toks = [t for t in toks if t]
    if 1 <= len(toks) <= 4:
        core = [t for t in toks if t not in HONORIFICS]
        if core:
            last = core[-1]
            if len(last) >= 3:
                for surf, recs in journal["by_surface"].items():
                    stoks = [re.sub(r"[^a-z0-9'-]", "", t) for t in surf.split()]
                    if last in stoks:
                        for rec in recs:
                            matches.setdefault(
                                f"journal_fallback:{rec['path']}",
                                {
                                    "type": "journal_surface_fallback",
                                    "id": rec["ref"],
                                    "surface": rec["surface"],
                                    "path": rec["path"],
                                },
                            )

    return list(matches.values())


def main():
    outdir = Path(__file__).with_name("results_population")
    outdir.mkdir(parents=True, exist_ok=True)

    cps = {}
    for name, spec in CHECKPOINTS.items():
        jraw = fetch(JOURNAL_REPO, spec["journal_commit"], JOURNAL_PATH)
        sraw = fetch(SI_REPO, spec["si_commit"], SI_PATH)
        graw = fetch(JOURNAL_REPO, spec["gold_commit"], GOLD_PATH)

        for label, raw, expected in [
            ("journal", jraw, spec["journal_blob"]),
            ("si", sraw, spec["si_blob"]),
            ("gold", graw, spec["gold_blob"]),
        ]:
            got = git_blob(raw)
            if got != expected:
                raise RuntimeError(f"{name} {label} blob drift: {got} != {expected}")

        gold_rows, dup_keys = parse_gold(graw)
        cps[name] = {
            "journal": parse_journal(jraw),
            "si": parse_si(sraw),
            "gold_rows": gold_rows,
            "dup_stable_texts": sorted(dup_keys),
            "meta": {
                "journal_sha256": sha256(jraw),
                "si_sha256": sha256(sraw),
                "gold_sha256": sha256(graw),
                "journal_bytes": len(jraw),
                "si_bytes": len(sraw),
                "gold_bytes": len(graw),
            },
        }

    # Track by stable_text only when unique at each checkpoint.
    gold_maps = {}
    for cp, data in cps.items():
        m = defaultdict(list)
        for r in data["gold_rows"]:
            m[r["stable_text"]].append(r)
        gold_maps[cp] = m

    all_stable = sorted(set().union(*(set(m) for m in gold_maps.values())))
    episodes = []
    counts = Counter()

    for stable in all_stable:
        trajectory = {}
        ambiguous = False
        first_cp = None
        first_row = None

        for cp in ("T0", "T1", "T2", "T3"):
            rows = gold_maps[cp].get(stable, [])
            if len(rows) > 1:
                trajectory[cp] = {"status": "AMBIGUOUS_GOLD_MATCH", "count": len(rows)}
                ambiguous = True
            elif len(rows) == 1:
                r = rows[0]
                trajectory[cp] = {
                    "status": "RESOLVED" if r["checked"] else "OPEN",
                    "line_no": r["line_no"],
                    "body": r["body"],
                }
                if first_cp is None:
                    first_cp = cp
                    first_row = r
            else:
                trajectory[cp] = {"status": "ABSENT"}

        if first_row is None:
            continue

        rec = {
            "stable_text": stable,
            "first_checkpoint": first_cp,
            "first_checked": first_row["checked"],
            "trajectory": trajectory,
            "pre_freeze_exposed": exposed(first_row),
            "gold_key_ambiguous": ambiguous,
            "source_matches": {},
            "eligible": False,
            "eligibility_reason": None,
        }

        if first_cp == "T3":
            rec["eligibility_reason"] = "FIRST_APPEARS_AT_T3"
            counts["first_T3"] += 1
            episodes.append(rec)
            continue
        if first_row["checked"]:
            rec["eligibility_reason"] = "CHECKED_AT_FIRST_APPEARANCE"
            counts["checked_first"] += 1
            episodes.append(rec)
            continue
        if rec["pre_freeze_exposed"]:
            rec["eligibility_reason"] = "PRE_FREEZE_EXPOSED"
            counts["exposed"] += 1
            episodes.append(rec)
            continue
        if ambiguous:
            rec["eligibility_reason"] = "AMBIGUOUS_GOLD_KEY"
            counts["ambiguous_key"] += 1
            episodes.append(rec)
            continue

        # Source matching at the checkpoint of first appearance.
        source_matches = candidate_source_matches(
            first_row,
            cps[first_cp]["journal"],
            cps[first_cp]["si"],
        )
        rec["source_matches"][first_cp] = source_matches

        if not source_matches:
            rec["eligibility_reason"] = "NO_PERSON_SOURCE_MATCH"
            counts["no_source_match"] += 1
            episodes.append(rec)
            continue

        # Person matching is guaranteed by Journal persName or SI person indexes.
        rec["eligible"] = True
        rec["eligibility_reason"] = "ELIGIBLE_UNEXPOSED_PERSON_QUESTION"
        counts["eligible"] += 1
        counts[f"eligible_first_{first_cp}"] += 1
        episodes.append(rec)

    eligible = [x for x in episodes if x["eligible"]]
    final_status = Counter(x["trajectory"]["T3"]["status"] for x in eligible)

    result = {
        "study": "MODULE_H0_DIGITAL_MITFORD_POPULATION_FREEZE_V1",
        "authority": "AUTOMATIC_POPULATION_EXTRACTION_AFTER_PROTOCOL_FREEZE",
        "protocol_commit": "a2e913031d63636c196af7b54aaa06c0b6fafae6",
        "checkpoints": {k: v["meta"] for k, v in cps.items()},
        "gold_line_counts": {k: len(v["gold_rows"]) for k, v in cps.items()},
        "episode_counts": dict(counts),
        "eligible_count": len(eligible),
        "eligible_final_gold_status": dict(final_status),
        "episodes": episodes,
        "claim_boundary": [
            "PossibleMissingSI.md is used only by this evaluator, never as system input.",
            "Pre-freeze exposed identities are excluded from confirmatory headline metrics.",
            "This H0 stage freezes population/source matching only; it does not evaluate R* discovery performance.",
            "No manually inspected unexposed item is used to tune matching after this run.",
        ],
    }

    out = outdir / "population.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Console intentionally emits aggregates and stable texts only for eligible episodes.
    print(json.dumps({
        "gold_line_counts": result["gold_line_counts"],
        "episode_counts": result["episode_counts"],
        "eligible_count": result["eligible_count"],
        "eligible_final_gold_status": result["eligible_final_gold_status"],
        "eligible_stable_texts": [x["stable_text"] for x in eligible],
        "population_sha256": sha256(out.read_bytes()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
