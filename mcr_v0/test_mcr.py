"""MCR-V0 development-only invariants. No human, LLM or native corpus metric."""
from __future__ import annotations

from dataclasses import replace
import unittest

from mcr_v0 import (
    Claim, EvidenceUnit, DocumentaryEdge, EpistemicProposal, EvidenceGraph,
    dense_topk, graph_expansion_baseline, encode, llm_context,
    LinearPairRoleProbe, RoleTrainingExample,
)


def unit(
    uid: str, embedding: tuple[float, float], *,
    claim_scope: tuple[str, ...] = ("c1",),
    verification: str = "PAGE_VERIFIED",
    role: str = "PRIMARY",
    token_cost: int = 1,
) -> EvidenceUnit:
    return EvidenceUnit(
        unit_id=uid,
        text="Synthetic textual witness " + uid,
        embedding=embedding,
        source_id="synthetic-volume-" + uid,
        source_anchor="synthetic-locus-" + uid,
        edition="v1",
        documentary_role=role,
        verification=verification,
        claim_scope=claim_scope,
        token_cost=token_cost,
    )


def proposal(source: str, target: str, kind: str, *,
             claim_id: str = "c1", confidence: float = 1.0) -> EpistemicProposal:
    return EpistemicProposal(
        source_id=source, target_id=target, kind=kind,
        claim_id=claim_id, confidence=confidence, origin="simulated",
    )


def fixture() -> EvidenceGraph:
    claim = Claim("c1", "Which textual attribution is supported?", (1.0, 0.0))
    witnesses = (
        unit("assertion", (0.99, 0.01)),
        unit("decoy", (0.98, 0.02)),
        unit("objection", (0.20, 0.98)),
        unit("correction", (0.10, 0.99)),
    )
    return EvidenceGraph(
        claim=claim,
        units=witnesses,
        documentary=(
            DocumentaryEdge("correction", "objection", "CITES",
                            "synthetic-documented-citation", True),
        ),
        proposals=(
            proposal("assertion", "c1", "SUPPORT"),
            proposal("objection", "assertion", "UNDERCUT"),
            proposal("correction", "objection", "REHABILITATE"),
        ),
        externally_attested_roster_complete=False,
    )


class McrStructuralTests(unittest.TestCase):

    def test_n1_source_gate_and_no_laundered_similarity(self):
        g = fixture()
        changed = tuple(
            replace(u, verification="BLOCKED") if u.unit_id == "assertion" else u
            for u in g.units
        )
        out = encode(replace(g, units=changed), 3)
        self.assertNotIn("assertion", out["selected_unit_ids"])
        self.assertEqual(out["excluded_units"]["assertion"], "SOURCE_NOT_VERIFIED")
        self.assertEqual(out["warrant_verdict"], "NOT_ADJUDICATED")
        self.assertTrue(out["unverified_relation_proposals"])

    def test_n2_counterevidence_is_not_relevance_only(self):
        g = fixture()
        self.assertIn("decoy", dense_topk(g, 3))
        # Simple graph expansion is also a capable rival and MUST get same edges.
        self.assertEqual(set(graph_expansion_baseline(g, 3)),
                         {"assertion", "objection", "correction"})
        out = encode(g, 3)
        self.assertEqual(set(out["selected_unit_ids"]),
                         {"assertion", "objection", "correction"})
        self.assertNotEqual(out["channels"]["challenge"], [0.0, 0.0])
        self.assertTrue(out["v0_objective_exact_for_current_graph"])

    def test_n3_response_channel_keeps_objection_visible(self):
        g = fixture()
        baseline = replace(
            g, proposals=g.proposals[:-1],
        )
        before = encode(baseline, 3)
        after = encode(g, 3)
        self.assertEqual(after["warrant_verdict"], "NOT_ADJUDICATED")
        self.assertNotEqual(after["channels"]["response"], [0.0, 0.0])
        self.assertNotEqual(after["channels"]["challenge"], [0.0, 0.0])
        self.assertEqual(before["channels"]["response"], [0.0, 0.0])
        self.assertEqual(
            {(x["source"], x["target"]) for x in after["selected_proposed_epistemic_links"]},
            {("assertion", "c1"), ("objection", "assertion"),
             ("correction", "objection")},
        )

    def test_n4_irrelevant_sham_does_not_change_claim_state(self):
        g = fixture()
        sham = proposal("decoy", "assertion", "UNDERCUT", claim_id="unrelated")
        a = encode(g, 3)
        b = encode(replace(g, proposals=g.proposals + (sham,)), 3)
        self.assertEqual(a, b)

    def test_n5_budget_truncation_reports_missing_relations(self):
        g = fixture()
        out = encode(g, 2)
        self.assertIn("COUNTEREVIDENCE_OR_SUPPORT_PACKET_INCOMPLETE",
                      out["reported_limits"])
        self.assertTrue(out["uncovered_proposal_links"] or out["known_support_omitted"])
        self.assertEqual(out["warrant_verdict"], "NOT_ADJUDICATED")
        self.assertLessEqual(out["tokens_used"], 2)
        tiny = encode(g, 0)
        self.assertEqual(tiny["packet"], [])
        self.assertTrue(tiny["known_support_omitted"])

    def test_n6_provisional_source_and_model_edges_are_not_truth(self):
        g = fixture()
        bad = tuple(
            replace(u, verification="PROVISIONAL_DIGITAL_ONLY")
            if u.unit_id == "objection" else u
            for u in g.units
        )
        out = encode(replace(g, units=bad), 3)
        self.assertIn("objection", out["excluded_units"])
        self.assertEqual(out["channels"]["challenge"], [0.0, 0.0])
        self.assertIn("SOME_PROPOSED_RELATIONS_HAVE_UNVERIFIED_SOURCES",
                      out["reported_limits"])
        self.assertEqual(out["warrant_verdict"], "NOT_ADJUDICATED")
        with self.assertRaises(ValueError):
            EpistemicProposal("assertion", "c1", "SUPPORT", "c1", 1.0, "gold_reference")

    def test_n7_claim_binding_and_primary_text_boundary(self):
        g = fixture()
        other = Claim("other", "What is authorially attested?", (1.0, 0.0))
        out = encode(replace(g, claim=other), 4)
        self.assertEqual(out["selected_unit_ids"], [])
        self.assertEqual(len(out["excluded_units"]), len(g.units))
        primary = unit("original", (1.0, 0.0), role="PRIMARY")
        translation = unit("translated", (1.0, 0.0), role="TRANSLATION")
        d = DocumentaryEdge("translated", "original", "DERIVED_FROM", "synthetic-bridge", True)
        exact = Claim("c1", "What exact word appears in the original?", (1.0, 0.0),
                      requires_primary_wording=True)
        p = encode(EvidenceGraph(exact, (primary, translation), (d,), ()), 2)
        self.assertEqual(p["excluded_units"]["translated"], "NOT_PRIMARY_WORDING")
        self.assertIn("original", p["selected_unit_ids"])

    def test_n8_determinism_and_dont_conflate_documentary_edges(self):
        g = fixture()
        reordered = replace(g, units=tuple(reversed(g.units)),
                            proposals=tuple(reversed(g.proposals)))
        self.assertEqual(encode(g, 3), encode(reordered, 3))
        text = llm_context(encode(g, 3))
        self.assertIn("NOT automatic truth", text)
        self.assertIn("No humanistic warrant verdict", text)
        self.assertIn("synthetic-documented-citation", text)
        self.assertNotIn("GOLD_WARRANT", text)
        # Having a verified documentary link NEVER generates a SUPPORT edge.
        doc_only = replace(g, proposals=())
        o = encode(doc_only, 3)
        self.assertEqual(o["channels"]["affirmation"], [0.0, 0.0])
        self.assertEqual(o["selected_proposed_epistemic_links"], [])

    def test_documentary_bridge_is_precondition_not_predicted_warrant(self):
        g = fixture()
        claim = replace(g.claim, requires_documentary_bridge=True)
        without = encode(replace(g, claim=claim, documentary=()), 3)
        self.assertEqual(without["selected_unit_ids"], [])
        with_link = encode(replace(g, claim=claim), 3)
        self.assertIn("correction", with_link["selected_unit_ids"])
        self.assertNotIn("assertion", with_link["selected_unit_ids"])

    def test_source_roster_not_magically_complete(self):
        g = fixture()
        out = encode(g, 3)
        self.assertIn("SOURCE_ROSTER_COMPLETENESS_NOT_ATTESTED",
                      out["reported_limits"])
        privileged = encode(replace(g, externally_attested_roster_complete=True), 3)
        self.assertNotIn("SOURCE_ROSTER_COMPLETENESS_NOT_ATTESTED",
                         privileged["reported_limits"])
        self.assertEqual(privileged["warrant_verdict"], "NOT_ADJUDICATED")

    def test_zero_vectors_and_illegal_roles_rejected(self):
        with self.assertRaises(ValueError):
            Claim("bad", "claim", ())
        with self.assertRaises(ValueError):
            proposal("assertion", "c1", "SUPPORT", confidence=2.0)
        with self.assertRaises(ValueError):
            encode(fixture(), -1)


class TrainableRoleProbeTests(unittest.TestCase):
    def test_trainable_probe_reduces_its_own_toy_loss(self):
        q=(1.0, 0.0)
        examples = [
            RoleTrainingExample(q, (1.,0.), (1.,0.), "SUPPORT"),
            RoleTrainingExample(q, (-1.,0.), (1.,0.), "UNDERCUT"),
            RoleTrainingExample(q, (0.,1.), (-1.,0.), "REHABILITATE"),
            RoleTrainingExample(q, (0.,-1.), (0.,1.), "QUALIFY"),
            RoleTrainingExample(q, (-0.3,-0.2), (0.2,-0.4), "UNRELATED"),
        ]
        p = LinearPairRoleProbe(2, seed=17)
        losses=p.fit(examples,epochs=180,rate=0.18)
        self.assertLess(losses[-1], losses[0])
        self.assertEqual(p.training_examples_seen, 5)
        p2 = LinearPairRoleProbe(2, seed=17)
        p2.fit(examples,epochs=180,rate=0.18)
        self.assertEqual(p.weights, p2.weights)
        g=fixture()
        probs=p.probabilities(g.claim.embedding, g.units[0].embedding, g.claim.embedding)
        self.assertAlmostEqual(sum(probs.values()),1.0,places=10)
        possible=p.propose(g.claim,g.units[0],None)
        if possible is not None:
            self.assertEqual(possible.origin, "model_predicted")
            self.assertEqual(possible.kind,"SUPPORT")
        with self.assertRaises(ValueError):
            p.fit([RoleTrainingExample(q,(1.,0.),q,"historically_true")])

    def test_no_human_gold_in_inference_signature(self):
        g=fixture()
        p=LinearPairRoleProbe(2)
        result=p.propose(g.claim,g.units[0],g.units[1])
        if result is not None:
            self.assertEqual(result.origin,"model_predicted")
            self.assertNotIn(result.origin,{"gold_reference","human_adjudicated"})


if __name__ == "__main__":
    unittest.main()
