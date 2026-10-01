from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from lxml import etree as ET

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import extract_population as h0

EXPECTED_POPULATION_SHA256 = "7944aac0d711c1b3d9f2bc09cfd3662fa79bafb5f5ed2faecdb274af9dd80613"
CHECKPOINT_ORDER = ("T0", "T1", "T2", "T3")
HONORIFICS = {"mr", "mrs", "miss", "ms", "sir", "lady", "lord", "dr", "rev"}
UNCERTAINTY = (
    "possibly",
    "may be",
    "might be",
    "probably",
    "presumably",
    "unknown",
    "unidentified",
    "not sure",
    "unclear",
    "more research needed",
    "check",
)
TOKEN_RE = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*", re.UNICODE)
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(x) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def norm(s: str) -> str:
    return h0.norm(s)


def tokens(s: str):
    out = [x.casefold() for x in TOKEN_RE.findall(unicodedata.normalize("NFC", s))]
    return [x for x in out if x]


def core_tokens(s: str):
    return [x for x in tokens(s) if x not in HONORIFICS]


def core_key(s: str):
    return " ".join(core_tokens(s))


def last_key(s: str):
    c = core_tokens(s)
    return c[-1] if c else ""


def strip_ref(v: str | None):
    return h0.strip_ref(v)


def uncertainty_hits(text: str):
    n = norm(text)
    hits = [p for p in UNCERTAINTY if p in n]
    if "?" in text:
        hits.append("?")
    return sorted(set(hits))


def parse_si_rich(raw: bytes):
    root = ET.fromstring(
        raw,
        ET.XMLParser(
            resolve_entities=False,
            no_network=True,
            recover=False,
            collect_ids=False,
        ),
    )
    tree = root.getroottree()
    persons = {}
    exact_index = defaultdict(set)
    last_index = defaultdict(set)

    for el in root.iter():
        if h0.lname(el) != "person":
            continue
        pid = el.get(XML_ID)
        if not pid:
            continue
        names = []
        notes = []
        explicit_refs = set()
        note_records = []
        for d in el.iterdescendants():
            tag = h0.lname(d)
            if tag == "persName":
                txt = " ".join(" ".join(d.itertext()).split())
                if txt:
                    names.append(txt)
            if tag == "note":
                txt = " ".join(" ".join(d.itertext()).split())
                refs = set()
                for nd in d.iterdescendants():
                    rv = nd.get("ref")
                    if rv:
                        for part in rv.split():
                            x = strip_ref(part)
                            if x:
                                refs.add(x)
                if txt:
                    notes.append(txt)
                    note_records.append(
                        {
                            "text": txt,
                            "refs": sorted(refs),
                            "uncertainty": uncertainty_hits(txt),
                        }
                    )
            rv = d.get("ref")
            if rv:
                for part in rv.split():
                    x = strip_ref(part)
                    if x:
                        explicit_refs.add(x)

        rec = {
            "id": pid,
            "names": names,
            "name_norms": sorted({norm(x) for x in names if norm(x)}),
            "name_cores": sorted({core_key(x) for x in names if core_key(x)}),
            "name_last": sorted({last_key(x) for x in names if last_key(x)}),
            "notes": notes,
            "note_records": note_records,
            "uncertainty_hits": sorted(
                set(x for note in note_records for x in note["uncertainty"])
            ),
            "explicit_refs": sorted(explicit_refs),
            "path": tree.getpath(el),
        }
        persons[pid.casefold()] = rec
        for k in rec["name_cores"]:
            exact_index[k].add(pid)
        for k in rec["name_last"]:
            last_index[k].add(pid)

    return {
        "persons": persons,
        "exact_index": {k: sorted(v) for k, v in exact_index.items()},
        "last_index": {k: sorted(v) for k, v in last_index.items()},
    }


def compatible_name(surface: str, person: dict):
    src = {x for x in core_tokens(surface) if len(x) >= 2}
    if not src:
        return False
    for name in person["names"]:
        nt = {x for x in core_tokens(name) if len(x) >= 2}
        if src & nt:
            return True
        if norm(surface) == norm(name):
            return True
    return False


def candidates_for_surface(surface: str, si: dict):
    ex = set(si["exact_index"].get(core_key(surface), []))
    su = set(si["last_index"].get(last_key(surface), [])) if last_key(surface) else set()
    return {
        "exact": ex,
        "surname": su,
        "all": ex | su,
    }


def build_groups(journal: dict, si: dict, interface: str):
    mentions = journal["mentions"]
    surface_refs = defaultdict(set)
    for m in mentions:
        if m["ref"]:
            surface_refs[m["surface_norm"]].add(m["ref"])

    grouped = defaultdict(list)
    for m in mentions:
        if m["ref"]:
            key = "ref:" + m["ref"].casefold()
        else:
            key = "surface:" + core_key(m["surface"])
        grouped[key].append(m)

    out = {}
    for key, ms in grouped.items():
        refs = sorted({m["ref"] for m in ms if m["ref"]})
        existing_refs = sorted(
            {
                r
                for r in refs
                if r.casefold() in si["persons"]
            }
        )
        missing_refs = sorted(
            {
                r
                for r in refs
                if r.casefold() not in si["persons"]
            }
        )

        exact_candidates = set()
        surname_candidates = set()
        all_candidates = set()
        for m in ms:
            cand = candidates_for_surface(m["surface"], si)
            exact_candidates |= cand["exact"]
            surname_candidates |= cand["surname"]
            all_candidates |= cand["all"]

        q1 = bool(missing_refs)
        q4 = any(
            len(surface_refs[m["surface_norm"]]) > 1
            for m in ms
        )
        q5 = False
        mismatch_refs = []
        for r in existing_refs:
            person = si["persons"][r.casefold()]
            compatible_any = any(compatible_name(m["surface"], person) for m in ms)
            if not compatible_any:
                q5 = True
                mismatch_refs.append(r)

        unique_existing_ref = len({x.casefold() for x in existing_refs}) == 1 and not missing_refs
        q3 = len(all_candidates) > 1 and not unique_existing_ref

        relevant_ids = existing_refs if existing_refs else sorted(all_candidates)
        q2_hits = {}
        for pid in relevant_ids:
            p = si["persons"].get(pid.casefold())
            if p and p["uncertainty_hits"]:
                q2_hits[pid] = p["uncertainty_hits"]
        q2 = bool(q2_hits)

        triggers = []
        if q1:
            triggers.append("Q1_MISSING_TARGET")
        if q2:
            triggers.append("Q2_EXPLICIT_UNCERTAINTY")
        if q3:
            triggers.append("Q3_CANDIDATE_COLLISION")
        if q4:
            triggers.append("Q4_REFERENCE_INCONSISTENCY")
        if q5:
            triggers.append("Q5_STATE_NAME_MISMATCH")

        if interface == "R_REF_ONLY":
            triggers = [x for x in triggers if x in {
                "Q1_MISSING_TARGET",
                "Q4_REFERENCE_INCONSISTENCY",
                "Q5_STATE_NAME_MISMATCH",
            }]

        if interface == "R_REF_ONLY":
            if q1 or q5:
                warrant = "SOURCE_INCOMPATIBLE"
                warrant_target = None
            elif len(existing_refs) == 1:
                warrant = "RESOLVED_TO_ID"
                warrant_target = existing_refs[0]
            elif not refs and len(exact_candidates) == 1:
                warrant = "RESOLVED_TO_ID"
                warrant_target = next(iter(exact_candidates))
            else:
                warrant = "UNRESOLVED"
                warrant_target = None
        else:
            if q1 or q5:
                warrant = "SOURCE_INCOMPATIBLE"
                warrant_target = None
            elif q3 or q4:
                warrant = "AMBIGUOUS"
                warrant_target = None
            elif q2:
                # Explicit unresolved status blocks a clean identity resolution
                # under the frozen conservative contract.
                warrant = "AMBIGUOUS" if len(all_candidates | set(existing_refs)) > 1 else "UNRESOLVED"
                warrant_target = None
            elif len(existing_refs) == 1:
                warrant = "RESOLVED_TO_ID"
                warrant_target = existing_refs[0]
            elif not refs and len(exact_candidates) == 1:
                warrant = "RESOLVED_TO_ID"
                warrant_target = next(iter(exact_candidates))
            else:
                warrant = "UNRESOLVED"
                warrant_target = None

        names_for_candidates = set()
        for pid in all_candidates | set(existing_refs):
            p = si["persons"].get(pid.casefold())
            if p:
                names_for_candidates |= set(p["name_norms"])

        relevant_person_fingerprint = []
        for pid in sorted(set(existing_refs) | all_candidates):
            p = si["persons"].get(pid.casefold())
            if not p:
                continue
            relevant_person_fingerprint.append(
                {
                    "id": p["id"],
                    "names": p["name_norms"],
                    "notes": [norm(x) for x in p["notes"]],
                    "refs": p["explicit_refs"],
                }
            )

        fp_obj = {
            "mentions": sorted(
                (m["surface_norm"], m["ref"], m["path"])
                for m in ms
            ),
            "persons": relevant_person_fingerprint,
        }

        out[key] = {
            "group_key": key,
            "mentions": ms,
            "surfaces": sorted({m["surface_norm"] for m in ms}),
            "refs": refs,
            "existing_refs": existing_refs,
            "missing_refs": missing_refs,
            "exact_candidate_ids": sorted(exact_candidates),
            "surname_candidate_ids": sorted(surname_candidates),
            "candidate_ids": sorted(all_candidates),
            "candidate_name_norms": sorted(names_for_candidates),
            "q2_hits": q2_hits,
            "mismatch_refs": mismatch_refs,
            "triggers": triggers,
            "live_question": bool(triggers),
            "warrant": warrant,
            "warrant_target": warrant_target,
            "fingerprint": sha256(canonical(fp_obj)),
            "source_locator_count": len(ms),
        }
    return out


def build_text_interface(journal_raw: bytes, si_raw: bytes):
    # No NER is added after freeze, so addressable person-question operation is unsupported.
    return {
        "live_questions": [],
        "groups": {},
        "operation_status": "OPERATION_UNSUPPORTED_WITHOUT_DECLARED_NER",
        "journal_text_bytes": len(journal_raw),
        "si_text_bytes": len(si_raw),
    }


def gold_source_keys(ep: dict, cp: str, journal: dict, si_basic: dict):
    tr = ep["trajectory"][cp]
    body = tr.get("body")
    if not body:
        return {"ids": set(), "surfaces": set(), "names": set(), "matches": []}
    row = {"body": body, "stable_text": ep["stable_text"]}
    matches = h0.candidate_source_matches(row, journal, si_basic)
    ids = set()
    surfaces = set()
    names = set()
    for m in matches:
        mid = m.get("id")
        if mid:
            ids.add(mid.casefold())
        if m.get("surface"):
            surfaces.add(norm(m["surface"]))
        if m.get("name"):
            names.add(norm(m["name"]))
    return {
        "ids": ids,
        "surfaces": surfaces,
        "names": names,
        "matches": matches,
    }


def group_matches_gold(group: dict, gkeys: dict):
    gids = {x.casefold() for x in group["refs"] + group["candidate_ids"] + group["existing_refs"]}
    gsurfaces = set(group["surfaces"])
    gnames = set(group["candidate_name_norms"])
    return bool(
        gids & gkeys["ids"]
        or gsurfaces & gkeys["surfaces"]
        or gnames & gkeys["names"]
    )


def question_metrics(clean_eps, cp, groups, journal, si_basic):
    questions = [g for g in groups.values() if g["live_question"]]
    gold_open = []
    gold_matches = {}
    for i, ep in enumerate(clean_eps):
        if ep["trajectory"][cp]["status"] != "OPEN":
            continue
        keys = gold_source_keys(ep, cp, journal, si_basic)
        if not keys["matches"]:
            continue
        gold_open.append(i)
        matched = [g["group_key"] for g in questions if group_matches_gold(g, keys)]
        gold_matches[i] = matched

    detected = sum(bool(gold_matches[i]) for i in gold_open)
    exact_bound = sum(len(gold_matches[i]) == 1 for i in gold_open)

    matched_questions = set()
    for vals in gold_matches.values():
        matched_questions.update(vals)

    return {
        "generated_question_count": len(questions),
        "source_materialized_open_gold_count": len(gold_open),
        "detected_open_gold_count": detected,
        "source_bound_exact_gold_count": exact_bound,
        "recall": detected / len(gold_open) if gold_open else None,
        "source_bound_exact_rate": exact_bound / len(gold_open) if gold_open else None,
        "checklist_matched_generated_question_count": len(matched_questions),
        "checklist_precision": len(matched_questions) / len(questions) if questions else None,
        "source_licensed_rate": 1.0 if questions else None,
        "gold_matches": gold_matches,
    }


def episode_state(ep, cp, groups, journal, si_basic, carried_groups=None):
    keys = gold_source_keys(ep, cp, journal, si_basic)
    current = [g for g in groups.values() if group_matches_gold(g, keys)] if keys["matches"] else []

    # R* may retain a source-bound group that temporarily disappears from the current source.
    combined = list(current)
    if carried_groups:
        seen = {g["group_key"] for g in combined}
        for g in carried_groups.values():
            if g["group_key"] in seen:
                continue
            if group_matches_gold(g, keys):
                combined.append(g)

    if not combined:
        return {
            "state": "NO_SOURCE_MATCH",
            "target": None,
            "group_count": 0,
            "fingerprint": None,
        }

    resolved = {
        g["warrant_target"]
        for g in combined
        if g["warrant"] == "RESOLVED_TO_ID" and g["warrant_target"]
    }
    non_resolved = [g for g in combined if g["warrant"] != "RESOLVED_TO_ID"]

    if len(resolved) == 1 and not non_resolved:
        state = "RESOLVED_TO_ID"
        target = next(iter(resolved))
    elif len(resolved) == 1 and all(g["warrant"] == "RESOLVED_TO_ID" for g in combined):
        state = "RESOLVED_TO_ID"
        target = next(iter(resolved))
    elif any(g["warrant"] == "SOURCE_INCOMPATIBLE" for g in combined):
        state = "SOURCE_INCOMPATIBLE"
        target = None
    elif any(g["warrant"] == "AMBIGUOUS" for g in combined) or len(resolved) > 1:
        state = "AMBIGUOUS"
        target = None
    else:
        state = "UNRESOLVED"
        target = None

    return {
        "state": state,
        "target": target,
        "group_count": len(combined),
        "fingerprint": sha256(canonical(sorted(g["fingerprint"] for g in current))) if current else None,
        "matched_group_keys": sorted(g["group_key"] for g in current),
    }


def first_status_cp(ep, status):
    for cp in CHECKPOINT_ORDER:
        if ep["trajectory"][cp]["status"] == status:
            return cp
    return None


def cp_index(cp):
    return CHECKPOINT_ORDER.index(cp)


def main():
    pop_path = HERE / "results_population" / "population.json"
    if not pop_path.exists():
        raise RuntimeError("H0 population.json missing; run extract_population.py first")
    pop_raw = pop_path.read_bytes()
    got = sha256(pop_raw)
    if got != EXPECTED_POPULATION_SHA256:
        raise RuntimeError(f"H0 population drift: {got}")

    population = json.loads(pop_raw)
    clean_eps = [
        x for x in population["episodes"]
        if x.get("eligible")
        and not x.get("post_freeze_accidental_exposure", False)
    ]
    all_eligible = [x for x in population["episodes"] if x.get("eligible")]

    if len(clean_eps) != 214 or len(all_eligible) != 218:
        raise RuntimeError("H0 eligible denominator drift")

    sources = {}
    for cp, spec in h0.CHECKPOINTS.items():
        jraw = h0.fetch(h0.JOURNAL_REPO, spec["journal_commit"], h0.JOURNAL_PATH)
        sraw = h0.fetch(h0.SI_REPO, spec["si_commit"], h0.SI_PATH)
        if h0.git_blob(jraw) != spec["journal_blob"]:
            raise RuntimeError(f"{cp} Journal drift")
        if h0.git_blob(sraw) != spec["si_blob"]:
            raise RuntimeError(f"{cp} SI drift")
        journal = h0.parse_journal(jraw)
        si_basic = h0.parse_si(sraw)
        si_rich = parse_si_rich(sraw)
        sources[cp] = {
            "journal_raw": jraw,
            "si_raw": sraw,
            "journal": journal,
            "si_basic": si_basic,
            "si_rich": si_rich,
            "R_STAR": build_groups(journal, si_rich, "R_STAR"),
            "R_REF_ONLY": build_groups(journal, si_rich, "R_REF_ONLY"),
            "R_TEXT": build_text_interface(jraw, sraw),
        }

    # Discovery evaluation.
    discovery = {"R_STAR": {}, "R_REF_ONLY": {}, "R_TEXT": {}}
    rstar_gold_matches_by_cp = {}
    for cp in CHECKPOINT_ORDER:
        for arm in ("R_STAR", "R_REF_ONLY"):
            m = question_metrics(
                clean_eps,
                cp,
                sources[cp][arm],
                sources[cp]["journal"],
                sources[cp]["si_basic"],
            )
            discovery[arm][cp] = {k: v for k, v in m.items() if k != "gold_matches"}
            if arm == "R_STAR":
                rstar_gold_matches_by_cp[cp] = m["gold_matches"]

        # R_TEXT has no addressable person-operation without a declared NER.
        source_open = 0
        for ep in clean_eps:
            if ep["trajectory"][cp]["status"] != "OPEN":
                continue
            keys = gold_source_keys(ep, cp, sources[cp]["journal"], sources[cp]["si_basic"])
            if keys["matches"]:
                source_open += 1
        discovery["R_TEXT"][cp] = {
            "generated_question_count": 0,
            "source_materialized_open_gold_count": source_open,
            "detected_open_gold_count": 0,
            "source_bound_exact_gold_count": 0,
            "recall": 0.0 if source_open else None,
            "source_bound_exact_rate": 0.0 if source_open else None,
            "checklist_matched_generated_question_count": 0,
            "checklist_precision": None,
            "source_licensed_rate": None,
            "operation_status": "OPERATION_UNSUPPORTED_WITHOUT_DECLARED_NER",
        }

    # First-detection latency for R* and R_REF_ONLY.
    detection = {}
    for arm in ("R_STAR", "R_REF_ONLY"):
        rows = []
        for idx, ep in enumerate(clean_eps):
            first_open = first_status_cp(ep, "OPEN")
            if not first_open:
                continue
            first_source = None
            first_detect = None
            for cp in CHECKPOINT_ORDER:
                if cp_index(cp) < cp_index(first_open):
                    continue
                if ep["trajectory"][cp]["status"] != "OPEN":
                    continue
                keys = gold_source_keys(ep, cp, sources[cp]["journal"], sources[cp]["si_basic"])
                if keys["matches"] and first_source is None:
                    first_source = cp
                qs = [
                    g for g in sources[cp][arm].values()
                    if g["live_question"] and group_matches_gold(g, keys)
                ] if keys["matches"] else []
                if qs and first_detect is None:
                    first_detect = cp
            rows.append(
                {
                    "first_open": first_open,
                    "first_source_materialized": first_source,
                    "first_detected": first_detect,
                    "detected_no_later_than_source": (
                        first_source is not None
                        and first_detect is not None
                        and cp_index(first_detect) <= cp_index(first_source)
                    ),
                    "delay_steps_from_source": (
                        cp_index(first_detect) - cp_index(first_source)
                        if first_source and first_detect
                        else None
                    ),
                }
            )
        source_mat = [r for r in rows if r["first_source_materialized"]]
        timely = sum(r["detected_no_later_than_source"] for r in source_mat)
        detection[arm] = {
            "episode_count": len(rows),
            "source_materialized_episode_count": len(source_mat),
            "timely_detected_count": timely,
            "timely_detection_rate": timely / len(source_mat) if source_mat else None,
            "missed_source_materialized_count": sum(
                r["first_source_materialized"] is not None and r["first_detected"] is None
                for r in rows
            ),
            "latency_distribution": dict(
                Counter(
                    str(r["delay_steps_from_source"])
                    for r in rows
                    if r["delay_steps_from_source"] is not None
                )
            ),
        }

    # Sustained R* and no-history states.
    carried = {}
    rstar_episode_states = defaultdict(dict)
    nohist_episode_states = defaultdict(dict)
    ref_episode_states = defaultdict(dict)

    for cp in CHECKPOINT_ORDER:
        current = sources[cp]["R_STAR"]
        for k, g in current.items():
            carried[k] = g

        for i, ep in enumerate(clean_eps):
            rstar_episode_states[i][cp] = episode_state(
                ep, cp, current, sources[cp]["journal"], sources[cp]["si_basic"], carried
            )
            nohist_episode_states[i][cp] = episode_state(
                ep, cp, current, sources[cp]["journal"], sources[cp]["si_basic"], None
            )
            ref_episode_states[i][cp] = episode_state(
                ep, cp, sources[cp]["R_REF_ONLY"], sources[cp]["journal"], sources[cp]["si_basic"], None
            )

    # Human resolution / source-materialization audit.
    resolution = {}
    for arm_name, states in (
        ("R_STAR", rstar_episode_states),
        ("R_NO_HISTORY", nohist_episode_states),
        ("R_REF_ONLY", ref_episode_states),
    ):
        resolved_gold = []
        still_open = []
        absent_final = []
        for i, ep in enumerate(clean_eps):
            final = ep["trajectory"]["T3"]["status"]
            if final == "RESOLVED":
                gold_cp = first_status_cp(ep, "RESOLVED")
                st = states[i][gold_cp]
                materialized = st["state"] == "RESOLVED_TO_ID"
                resolved_gold.append(
                    {
                        "gold_resolved_cp": gold_cp,
                        "state_at_gold_resolution": st["state"],
                        "source_materialized": materialized,
                        "target": st.get("target"),
                    }
                )
            elif final == "OPEN":
                st = states[i]["T3"]
                still_open.append(
                    {
                        "state": st["state"],
                        "forced_closed": st["state"] == "RESOLVED_TO_ID",
                    }
                )
            elif final == "ABSENT":
                absent_final.append(states[i]["T3"]["state"])

        resolution[arm_name] = {
            "gold_resolved_count": len(resolved_gold),
            "source_materialized_at_gold_resolution_count": sum(x["source_materialized"] for x in resolved_gold),
            "source_materialized_at_gold_resolution_rate": (
                sum(x["source_materialized"] for x in resolved_gold) / len(resolved_gold)
                if resolved_gold else None
            ),
            "editor_resolved_but_source_not_materialized_count": sum(
                not x["source_materialized"] for x in resolved_gold
            ),
            "gold_final_open_count": len(still_open),
            "gold_final_open_forced_closed_count": sum(x["forced_closed"] for x in still_open),
            "gold_final_open_preserved_unresolved_or_ambiguous_count": sum(
                x["state"] in {"UNRESOLVED", "AMBIGUOUS", "SOURCE_INCOMPATIBLE", "NO_SOURCE_MATCH"}
                for x in still_open
            ),
            "final_absent_count": len(absent_final),
            "final_absent_state_distribution": dict(Counter(absent_final)),
        }

    # Null-event stability using evaluator-only exact episode source fingerprints.
    null_metrics = {}
    for arm_name, states in (
        ("R_STAR", rstar_episode_states),
        ("R_NO_HISTORY", nohist_episode_states),
        ("R_REF_ONLY", ref_episode_states),
    ):
        eligible_intervals = 0
        stable_intervals = 0
        violations = 0
        for i, ep in enumerate(clean_eps):
            for a, b in zip(CHECKPOINT_ORDER[:-1], CHECKPOINT_ORDER[1:]):
                if ep["trajectory"][a]["status"] != ep["trajectory"][b]["status"]:
                    continue
                sa = states[i][a]
                sb = states[i][b]
                if sa["fingerprint"] is None or sb["fingerprint"] is None:
                    continue
                if sa["fingerprint"] != sb["fingerprint"]:
                    continue
                eligible_intervals += 1
                same = (sa["state"], sa.get("target")) == (sb["state"], sb.get("target"))
                if same:
                    stable_intervals += 1
                else:
                    violations += 1
        null_metrics[arm_name] = {
            "null_interval_count": eligible_intervals,
            "stable_null_interval_count": stable_intervals,
            "gratuitous_change_count": violations,
            "null_stability_rate": stable_intervals / eligible_intervals if eligible_intervals else None,
        }

    # Delayed reuse: require at least two current T3 Journal occurrences in the matched source group.
    delayed = {}
    for arm_name, states, group_arm in (
        ("R_STAR", rstar_episode_states, "R_STAR"),
        ("R_NO_HISTORY", nohist_episode_states, "R_STAR"),
        ("R_REF_ONLY", ref_episode_states, "R_REF_ONLY"),
    ):
        total = 0
        exact = 0
        resolved_total = 0
        resolved_exact = 0
        unresolved_total = 0
        unresolved_exact = 0
        for i, ep in enumerate(clean_eps):
            keys = gold_source_keys(ep, "T3", sources["T3"]["journal"], sources["T3"]["si_basic"])
            if not keys["matches"]:
                continue
            matched = [
                g for g in sources["T3"][group_arm].values()
                if group_matches_gold(g, keys)
            ]
            distinct_locs = {
                m["path"]
                for g in matched
                for m in g["mentions"]
            }
            if len(distinct_locs) < 2:
                continue

            total += 1
            # Strong current-source reference is the R* no-history state at T3.
            truth = nohist_episode_states[i]["T3"]
            pred = states[i]["T3"]
            ok = (pred["state"], pred.get("target")) == (truth["state"], truth.get("target"))
            exact += ok
            if truth["state"] == "RESOLVED_TO_ID":
                resolved_total += 1
                resolved_exact += ok
            else:
                unresolved_total += 1
                unresolved_exact += ok

        delayed[arm_name] = {
            "eligible_episode_count": total,
            "exact_count": exact,
            "exact_rate": exact / total if total else None,
            "resolved_episode_count": resolved_total,
            "resolved_exact_count": resolved_exact,
            "unresolved_episode_count": unresolved_total,
            "unresolved_exact_count": unresolved_exact,
        }

    # Collateral update audit: count per-episode state changes and whether gold/source changed.
    selective = {}
    for arm_name, states in (
        ("R_STAR", rstar_episode_states),
        ("R_NO_HISTORY", nohist_episode_states),
        ("R_REF_ONLY", ref_episode_states),
    ):
        changes = 0
        unsupported_changes = 0
        for i, ep in enumerate(clean_eps):
            for a, b in zip(CHECKPOINT_ORDER[:-1], CHECKPOINT_ORDER[1:]):
                sa, sb = states[i][a], states[i][b]
                if (sa["state"], sa.get("target")) == (sb["state"], sb.get("target")):
                    continue
                changes += 1
                gold_changed = ep["trajectory"][a]["status"] != ep["trajectory"][b]["status"]
                source_changed = (
                    sa["fingerprint"] is None
                    or sb["fingerprint"] is None
                    or sa["fingerprint"] != sb["fingerprint"]
                )
                if not gold_changed and not source_changed:
                    unsupported_changes += 1
        selective[arm_name] = {
            "state_change_count": changes,
            "unsupported_or_collateral_change_count": unsupported_changes,
        }

    # Positive R* pass criteria from the frozen protocol.
    rstar_timely = detection["R_STAR"]["timely_detection_rate"]
    rstar_no_incompat_resolve = resolution["R_STAR"]["gold_final_open_forced_closed_count"] == 0
    rstar_null = null_metrics["R_STAR"]["gratuitous_change_count"] == 0
    rstar_delayed = delayed["R_STAR"]["exact_rate"]
    resolved_materialized = resolution["R_STAR"]["source_materialized_at_gold_resolution_rate"]

    # 'Every source-materialized live question detected' is strict.
    discovery_all = rstar_timely == 1.0
    no_false_close = rstar_no_incompat_resolve
    null_all = rstar_null
    delayed_all = (rstar_delayed == 1.0) if rstar_delayed is not None else False

    ablation_separation = (
        detection["R_REF_ONLY"]["timely_detection_rate"] != detection["R_STAR"]["timely_detection_rate"]
        or discovery["R_TEXT"]["T0"]["recall"] != discovery["R_STAR"]["T0"]["recall"]
        or resolution["R_REF_ONLY"]["gold_final_open_forced_closed_count"]
           != resolution["R_STAR"]["gold_final_open_forced_closed_count"]
        or delayed["R_NO_HISTORY"]["exact_rate"] != delayed["R_STAR"]["exact_rate"]
    )

    bounded_pass = all([
        discovery_all,
        no_false_close,
        null_all,
        delayed_all,
        ablation_separation,
    ])

    result = {
        "study": "MODULE_H_DIGITAL_MITFORD_END_TO_END_HOLDOUT_V1",
        "authority": "PROSPECTIVE_FRESH_END_TO_END_HOLDOUT",
        "protocol_commit": "a2e913031d63636c196af7b54aaa06c0b6fafae6",
        "source_contract_commit": "9aeff5135cdf5619d39aecb61089d94d228b39b0",
        "h0_population_sha256": got,
        "population": {
            "all_eligible": len(all_eligible),
            "clean_confirmatory": len(clean_eps),
            "post_freeze_accidental_exposure": len(all_eligible) - len(clean_eps),
            "clean_final_gold_status": dict(
                Counter(ep["trajectory"]["T3"]["status"] for ep in clean_eps)
            ),
        },
        "discovery": discovery,
        "first_detection": detection,
        "resolution": resolution,
        "null_event_stability": null_metrics,
        "selective_update": selective,
        "delayed_reuse": delayed,
        "positive_sufficiency": {
            "every_source_materialized_question_timely_detected": discovery_all,
            "no_final_open_forced_closed": no_false_close,
            "all_null_events_stable": null_all,
            "all_delayed_reuse_exact": delayed_all,
            "principled_ablation_separation_observed": ablation_separation,
            "R_STAR_BOUNDED_HOLDOUT_PASS": bounded_pass,
            "source_materialized_human_resolution_rate": resolved_materialized,
        },
        "claim_boundary": [
            "PossibleMissingSI.md is evaluator-only and never enters R* or the ablations.",
            "Checklist precision is against a potentially non-exhaustive human editorial log and is not treated as exhaustive false-positive truth.",
            "Human RESOLVED status is not historical truth unless the frozen source state materializes a compatible resolution.",
            "R_TEXT is an operation-support ablation without an added NER/linker and cannot be used to claim raw text is universally insufficient.",
            "The clean confirmatory denominator excludes only the pre-freeze exposure ledger and separately documented post-freeze accidental search contamination.",
            "Digital Mitford episodes are a finite dependent editorial population from one project.",
        ],
    }

    outdir = HERE / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Keep stdout aggregate-only. Item-level episode trajectories remain in population artifact.
    compact = {
        "population": result["population"],
        "discovery": result["discovery"],
        "first_detection": result["first_detection"],
        "resolution": result["resolution"],
        "null_event_stability": result["null_event_stability"],
        "selective_update": result["selective_update"],
        "delayed_reuse": result["delayed_reuse"],
        "positive_sufficiency": result["positive_sufficiency"],
        "results_sha256": sha256(out.read_bytes()),
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
