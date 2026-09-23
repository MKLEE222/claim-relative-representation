from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    with open(ROOT / path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def splitset(value):
    return {x for x in (value or "").split("|") if x}

events = rows("data/yule_cordier_claim_events.csv")
alignment = rows("data/yule_cordier_papermoney_alignment_v0.csv")
claims = rows("spec/claim_dependencies.csv")
interventions = rows("spec/interventions.csv")
controls = rows("controls/matched_controls.csv")
restorations = rows("controls/restoration_plan.csv")

errors = []
warnings = []

event_ids = [r["event_id"] for r in events]
if len(event_ids) != len(set(event_ids)):
    errors.append("duplicate event_id")
event_set = set(event_ids)

align_refs = {r["event_ref"] for r in alignment}
unknown = align_refs - event_set
if unknown:
    errors.append(f"alignment references unknown events: {sorted(unknown)}")

claim_map = {r["claim_id"]: r for r in claims}
int_map = {r["intervention_id"]: r for r in interventions}

for c in claims:
    missing = splitset(c["source_events"]) - event_set
    if missing:
        errors.append(f'{c["claim_id"]} uses unknown source events {sorted(missing)}')

for p in controls:
    if p["target_claim_id"] not in claim_map or p["control_claim_id"] not in claim_map:
        errors.append(f'{p["pair_id"]}: unknown claim')
        continue
    if p["intervention_id"] not in int_map:
        errors.append(f'{p["pair_id"]}: unknown intervention')
        continue
    coord = int_map[p["intervention_id"]]["coordinate"]
    tdeps = splitset(claim_map[p["target_claim_id"]]["dependency_coordinates"])
    cdeps = splitset(claim_map[p["control_claim_id"]]["dependency_coordinates"])
    if coord not in tdeps:
        errors.append(f'{p["pair_id"]}: target does not depend on {coord}')
    if coord in cdeps:
        errors.append(f'{p["pair_id"]}: control also depends on {coord}')

for r in restorations:
    if r["target_claim_id"] not in claim_map or r["intervention_id"] not in int_map:
        errors.append(f'{r["restoration_id"]}: unknown target/intervention')
        continue
    coord = int_map[r["intervention_id"]]["coordinate"]
    deps = splitset(claim_map[r["target_claim_id"]]["dependency_coordinates"])
    if r["restore_coordinate"] != coord:
        errors.append(f'{r["restoration_id"]}: restoration coordinate mismatch')
    if coord not in deps:
        errors.append(f'{r["restoration_id"]}: restored coordinate absent from target dependency')

verified_excerpt = []
object_checked = []
pending_excerpt = []
for r in alignment:
    s = r["verification_status"].lower()
    if "page-image-verified" in s and "pending" not in s:
        verified_excerpt.append(r["event_ref"])
    elif "object-structure-checked" in s:
        object_checked.append(r["event_ref"])
    else:
        pending_excerpt.append(r["event_ref"])

print("CEDL scientific-object validation")
print(f"events={len(events)} claims={len(claims)} interventions={len(interventions)}")
print(f"source edges with page-image-verified excerpt={len(verified_excerpt)}: {verified_excerpt}")
print(f"digital-object structure checks={len(object_checked)}: {object_checked}")
print(f"page-anchored but excerpt pending={len(pending_excerpt)}: {pending_excerpt}")
print(f"matched negative-control designs={len(controls)}")
print(f"restoration designs={len(restorations)}")

if pending_excerpt:
    warnings.append("Gate V remains incomplete for events whose page anchor exists but verbatim excerpt has not yet been extracted into the alignment ledger.")
if any(r["realism_status"] != "verified_real_operation" for r in interventions):
    warnings.append("Gate T remains empirical-pending: interventions are frozen as candidate real operations but have not yet been bound to documented transformation witnesses.")
if any(r["empirical_status"] != "observed" for r in restorations):
    warnings.append("Gate R has only design validity; no restoration outcome has yet been observed.")

for w in warnings:
    print("BLOCKED:", w)

if errors:
    for e in errors:
        print("FAIL:", e)
    sys.exit(1)

print("STRUCTURAL_CHECK=PASS")
print("EMPIRICAL_DISPOSITION=SOURCE_VALIDATION_IN_PROGRESS")


# Coding-packet leakage and coverage checks
blind_packet = rows("coding/blind_packet_v1.csv")
coder_template = rows("coding/independent_coder_template.csv")

if len(blind_packet) != len(events):
    errors.append(f"blind packet size {len(blind_packet)} != event ledger size {len(events)}")

packet_refs = {r["event_ref"] for r in blind_packet}
if packet_refs != event_set:
    errors.append(f"blind packet event coverage mismatch: missing={sorted(event_set-packet_refs)}, extra={sorted(packet_refs-event_set)}")

for forbidden in ("provisional_decision", "author_claim_hypothesis", "relation_to_claim"):
    if forbidden in blind_packet[0]:
        errors.append(f"blind packet leaks forbidden field: {forbidden}")

allowed_template_fields = {
    "item_id","primitive_labels","claim_binding","attribution_actor",
    "attribution_status","temporal_relation","representation_status",
    "uncertainty_note","coder_id","coded_without_provisional_decision"
}
if set(coder_template[0].keys()) != allowed_template_fields:
    errors.append("independent coder template fields changed without contract update")

print(f"blind relation-coding items={len(blind_packet)}")
print("BLIND_PACKET_LEAKAGE_CHECK=PASS" if not any("blind packet" in e for e in errors) else "BLIND_PACKET_LEAKAGE_CHECK=FAIL")


# Primitive-ontology coverage check against the pre-existing author ledger
projection = rows("coding/author_ledger_projection_v1.csv")
allowed_primitives = {
    "ASSERTS_CONTENT","ATTRIBUTES_SOURCE","SUPPORTS","CHALLENGES",
    "QUALIFIES_AUTHORITY","DISTINGUISHES_WITNESSES",
    "UPDATES_IDENTIFICATION","ACCRETES_INTERPRETATION",
    "LINKS_PRIOR","DIGITAL_ASSEMBLES"
}

if len(projection) != len(events):
    errors.append(f"author-ledger projection size {len(projection)} != event ledger size {len(events)}")

proj_refs = {r["event_ref"] for r in projection}
if proj_refs != event_set:
    errors.append("author-ledger projection does not cover exactly the event ledger")

for r in projection:
    labels = splitset(r["primitive_labels"])
    bad = labels - allowed_primitives
    if bad:
        errors.append(f'{r["event_ref"]}: unknown primitive labels {sorted(bad)}')
    if r["residual_unmapped"].strip().lower() != "no":
        warnings.append(f'{r["event_ref"]}: ontology has an unmapped residual')

print(f"author-ledger primitive coverage={len(projection)}/{len(events)}")


# Humanistic significance and transformation-analogue checks
h_registry = rows("data/humanistic_significance_v1.csv")
if not h_registry:
    errors.append("humanistic significance registry missing")
elif any(r["status"] != "PASS" for r in h_registry):
    errors.append("one or more humanistic claim families lack independent significance PASS")

analogue_ok = all(r["realism_status"].startswith("analogue_verified") for r in interventions)
if not analogue_ok:
    errors.append("one or more intervention coordinates lack a documented real-use analogue")

print(f"humanistic_significance_pass={sum(r['status']=='PASS' for r in h_registry)}/{len(h_registry)}")
print(f"transformation_analogue_coverage={sum(r['realism_status'].startswith('analogue_verified') for r in interventions)}/{len(interventions)}")

if all(r["status"] == "PASS" for r in h_registry):
    print("GATE_H=PASS")
if analogue_ok:
    print("GATE_T_DESIGN=PASS")
