from __future__ import annotations
import csv, json
from pathlib import Path
import unittest

from interaction_ops import wrap, apply, changed_paths

ROOT=Path(__file__).resolve().parents[1]

def rows(p):
    with open(ROOT/p,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

class InteractionConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=json.loads((ROOT/"representation/baseline_fixture_v1.json").read_text(encoding="utf-8"))
        cls.interactions=rows("spec/interaction_blocks_v1.csv")

    def test_registered_constructors_exist(self):
        for i in self.interactions:
            base=wrap(self.fixture[0])
            apply(base,i["T1"])
            apply(base,i["T2"])

    def test_text_identity_preserved(self):
        for i in self.interactions:
            for rec in self.fixture:
                base=wrap(rec)
                for state in (
                    apply(base,i["T1"]),
                    apply(base,i["T2"]),
                    apply(apply(base,i["T1"]),i["T2"]),
                ):
                    self.assertEqual(base["record"]["text_key"],state["record"]["text_key"])

    def test_declared_commutation(self):
        for i in self.interactions:
            if i["order"]!="commuting":
                continue
            for rec in self.fixture:
                base=wrap(rec)
                left=apply(apply(base,i["T1"]),i["T2"])
                right=apply(apply(base,i["T2"]),i["T1"])
                self.assertEqual(left,right,msg=i["interaction_id"])

    def test_joint_changed_paths_are_union(self):
        expected={
            "TD_TEMPORAL":{"record.temporal_order"},
            "TR_BINDING":{"record.claim_binding"},
            "TR_EVIDENCE":{"record.evidence_relation"},
            "TA_SPAN":{"context_scope"},
        }
        for i in self.interactions:
            for rec in self.fixture:
                base=wrap(rec)
                r10=apply(base,i["T1"])
                r01=apply(base,i["T2"])
                r11=apply(r10,i["T2"])
                self.assertEqual(changed_paths(base,r10),expected[i["T1"]])
                self.assertEqual(changed_paths(base,r01),expected[i["T2"]])
                self.assertEqual(
                    changed_paths(base,r11),
                    expected[i["T1"]] | expected[i["T2"]],
                    msg=i["interaction_id"],
                )

if __name__=="__main__":
    unittest.main(verbosity=2)
