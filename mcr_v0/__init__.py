"""Mediated Claim Representation V0 (development-only DH x LLM interface)."""
from .core import (
    Claim, EvidenceUnit, DocumentaryEdge, EpistemicProposal, EvidenceGraph,
    dense_topk, graph_expansion_baseline, encode, llm_context, dump_state_json,
)
from .trainable import LinearPairRoleProbe, RoleTrainingExample

__all__ = [
    "Claim", "EvidenceUnit", "DocumentaryEdge", "EpistemicProposal",
    "EvidenceGraph", "dense_topk", "graph_expansion_baseline",
    "encode", "llm_context", "dump_state_json",
    "LinearPairRoleProbe", "RoleTrainingExample",
]
