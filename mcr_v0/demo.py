"""Run: python -m mcr_v0.demo

EXPLICITLY FICTIONAL / SYNTHETIC_DEV. No historical truth, LLM inference,
benchmark success rate or causal mediation claim comes from this demonstration.
"""
from __future__ import annotations

import json

from .core import (
    Claim, EvidenceUnit, DocumentaryEdge, EpistemicProposal, EvidenceGraph,
    dense_topk, graph_expansion_baseline, encode, llm_context,
)


def make_synthetic_example() -> EvidenceGraph:
    c = Claim(
        claim_id="fictional-c",
        question="Do the available textual witnesses justify the recorded pigment identification?",
        embedding=(1.0, 0.0),
    )
    def w(id_: str, text: str, vec: tuple[float, float], role: str) -> EvidenceUnit:
        return EvidenceUnit(
            id_, text, vec, "fictional-volume", "fictional-page/" + id_,
            "synthetic-edition-1", role, "PAGE_VERIFIED", ("fictional-c",),
        )
    witnesses = (
        w("base", "An earlier catalogue says the pigment is copper-based.", (.99, .01), "EDITION"),
        w("unrelated", "Another note discusses a copper ornament.", (.98, .02), "COMMENTARY"),
        w("challenge", "A later annotation disputes the pigment identification.", (.2, .98), "COMMENTARY"),
        w("response", "A subsequent critical note corrects the earlier objection.", (.1, .99), "COMMENTARY"),
    )
    def e(src: str, tgt: str, kind: str) -> EpistemicProposal:
        return EpistemicProposal(
            src, tgt, kind, "fictional-c", 1.0, "simulated",
        )
    return EvidenceGraph(
        c, witnesses,
        (DocumentaryEdge("response", "challenge", "CITES", "fictional-citation", True),),
        (
            e("base", "fictional-c", "SUPPORT"),
            e("challenge", "base", "UNDERCUT"),
            e("response", "challenge", "REHABILITATE"),
        ),
        externally_attested_roster_complete=False,
    )


def main() -> None:
    graph = make_synthetic_example()
    budget = 3
    state = encode(graph, budget)
    summary = {
        "evidence_class": "SYNTHETIC_DEV_NOT_LLM_MEASUREMENT",
        "cosine_topk_same_sources": dense_topk(graph, budget),
        "graph_expansion_same_relation_inputs": graph_expansion_baseline(graph, budget),
        "mcr_selected": state["selected_unit_ids"],
        "channels": state["channels"],
        "reported_limits": state["reported_limits"],
        "warrant_verdict": state["warrant_verdict"],
        "selection_objective_exact_for_this_tiny_graph":
            state["v0_objective_exact_for_current_graph"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    print("\n--- LLM-facing evidence context, not a certified historical answer ---")
    print(llm_context(state))


if __name__ == "__main__":
    main()
