from __future__ import annotations

import csv
import json
from pathlib import Path
import unittest

from representation_ops import COORDINATE_FIELD, intervene, restore, changed_fields

ROOT = Path(__file__).resolve().parents[1]

def read_csv(path):
    with open(ROOT / path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

class InterventionInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / "representation/baseline_fixture_v1.json").read_text(encoding="utf-8"))
        cls.interventions = read_csv("spec/interventions.csv")
        cls.claims = {r["claim_id"]: r for r in read_csv("spec/claim_dependencies.csv")}
        cls.controls = read_csv("controls/matched_controls.csv")

    def test_one_coordinate_invariance(self):
        for spec in self.interventions:
            coord = spec["coordinate"]
            field = COORDINATE_FIELD[coord]
            for record in self.fixture:
                changed = changed_fields(record, intervene(record, coord))
                self.assertEqual(
                    changed, {field},
                    msg=f'{spec["intervention_id"]}/{record["event_ref"]} changed {changed}, expected only {field}'
                )

    def test_text_key_is_never_changed(self):
        for spec in self.interventions:
            coord = spec["coordinate"]
            for record in self.fixture:
                out = intervene(record, coord)
                self.assertEqual(record["text_key"], out["text_key"])

    def test_exact_restoration(self):
        for spec in self.interventions:
            coord = spec["coordinate"]
            for record in self.fixture:
                altered = intervene(record, coord)
                recovered = restore(altered, record, coord)
                self.assertEqual(record, recovered)

    def test_negative_control_dependency_separation(self):
        coord_by_id = {r["intervention_id"]: r["coordinate"] for r in self.interventions}
        for pair in self.controls:
            coord = coord_by_id[pair["intervention_id"]]
            target = set(filter(None, self.claims[pair["target_claim_id"]]["dependency_coordinates"].split("|")))
            control = set(filter(None, self.claims[pair["control_claim_id"]]["dependency_coordinates"].split("|")))
            self.assertIn(coord, target, msg=f'{pair["pair_id"]}: target lacks intervention coordinate')
            self.assertNotIn(coord, control, msg=f'{pair["pair_id"]}: control shares intervention coordinate')

if __name__ == "__main__":
    unittest.main(verbosity=2)
