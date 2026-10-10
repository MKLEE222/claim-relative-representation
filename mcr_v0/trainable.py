"""Tiny trainable claim/statement-pair role-proposal head for frozen LLM vectors.

This is a CPU-only, transparent *development* baseline, not an LLM itself.
Pass real pretrained embeddings from an independent frozen encoder at inference.
Labels are used in fit() ONLY. predict() never accepts labels or warrant truth.
For serious NLP experiments replace/compare against a pretrained cross-encoder.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random

from .core import Claim, EvidenceUnit, EpistemicProposal

RELATION_CLASSES = ("UNRELATED", "SUPPORT", "UNDERCUT", "REHABILITATE", "QUALIFY")


@dataclass(frozen=True)
class RoleTrainingExample:
    """Supervision unit. Gold stays in a separate TRAINING file, never query input."""
    claim_vector: tuple[float, ...]
    source_vector: tuple[float, ...]
    target_vector: tuple[float, ...]
    role_gold: str


def pair_features(
    claim_vector: tuple[float, ...],
    source_vector: tuple[float, ...],
    target_vector: tuple[float, ...],
) -> tuple[float, ...]:
    q = tuple(float(x) for x in claim_vector)
    s = tuple(float(x) for x in source_vector)
    t = tuple(float(x) for x in target_vector)
    if not q or len(q) != len(s) or len(s) != len(t):
        raise ValueError("vectors must share a positive dimension")
    if not all(math.isfinite(v) for v in q + s + t):
        raise ValueError("nonfinite vector")
    return (
        (1.0,)
        + q + s + t
        + tuple(abs(a - b) for a, b in zip(s, t))
        + tuple(a * b for a, b in zip(s, t))
        + tuple(a * b for a, b in zip(q, s))
        + tuple(a * b for a, b in zip(q, t))
    )


class LinearPairRoleProbe:
    """Supervised softmax role head, no outcome labels at inference.

    Regular softmax regression is a PRIOR-ART BASELINE, not MCR's novelty.
    Training labels can encode historical scholarly disagreement and MUST be
    separately annotated; automatically derived labels are only synthetic dev.
    """

    def __init__(self, embedding_dim: int, seed: int = 20261010) -> None:
        if type(embedding_dim) is not int or embedding_dim < 1:
            raise ValueError("embedding_dim must be positive integer")
        self.embedding_dim = embedding_dim
        self.n_features = 1 + 7 * embedding_dim
        r = random.Random(seed)
        self.weights = [
            [(r.random() - 0.5) * 0.002 for _ in range(self.n_features)]
            for _ in RELATION_CLASSES
        ]
        self.training_examples_seen = 0

    def probabilities(
        self,
        q: tuple[float, ...],
        src: tuple[float, ...],
        tgt: tuple[float, ...],
    ) -> dict[str, float]:
        feat = pair_features(q, src, tgt)
        if len(feat) != self.n_features:
            raise ValueError("embedding_dim mismatch")
        logits = [sum(w * x for w, x in zip(weights, feat)) for weights in self.weights]
        shift = max(logits)
        exps = [math.exp(z - shift) for z in logits]
        total = sum(exps)
        return {name: num / total for name, num in zip(RELATION_CLASSES, exps)}

    def fit(
        self,
        examples: list[RoleTrainingExample],
        *,
        epochs: int = 100,
        rate: float = 0.05,
        weight_decay: float = 0.0,
    ) -> list[float]:
        if not examples:
            raise ValueError("nonempty independently labelled TRAINING set required")
        if type(epochs) is not int or epochs < 1 or not math.isfinite(rate) or rate <= 0:
            raise ValueError("bad training hyperparameters")
        if not math.isfinite(weight_decay) or weight_decay < 0:
            raise ValueError("bad weight decay")
        for ex in examples:
            if ex.role_gold not in RELATION_CLASSES:
                raise ValueError("unknown training role")
            if len(pair_features(ex.claim_vector, ex.source_vector, ex.target_vector)) != self.n_features:
                raise ValueError("training embedding_dim mismatch")
        curve = []
        for _ in range(epochs):
            grad = [[0.0] * self.n_features for _ in RELATION_CLASSES]
            loss = 0.0
            for ex in examples:
                x = pair_features(ex.claim_vector, ex.source_vector, ex.target_vector)
                probs = self.probabilities(
                    ex.claim_vector, ex.source_vector, ex.target_vector,
                )
                loss -= math.log(max(probs[ex.role_gold], 1e-300))
                for j, name in enumerate(RELATION_CLASSES):
                    err = probs[name] - float(name == ex.role_gold)
                    for k, feature in enumerate(x):
                        grad[j][k] += err * feature
            n = len(examples)
            for j, row in enumerate(self.weights):
                for k, old in enumerate(row):
                    row[k] -= rate * (grad[j][k] / n + weight_decay * old)
            curve.append(loss / n)
        self.training_examples_seen += len(examples)
        return curve

    def propose(
        self,
        claim: Claim,
        source: EvidenceUnit,
        target: EvidenceUnit | None,
        *,
        min_probability: float = 0.0,
    ) -> EpistemicProposal | None:
        """Predict an unverified relation. target=None predicts to claim ID.

        Relation proposals are NOT documentary facts and cannot authorize a
        stronger historical inference in their own right.
        """
        if claim.claim_id not in source.claim_scope:
            raise ValueError("source not explicitly bound to claim")
        if target is not None and claim.claim_id not in target.claim_scope:
            raise ValueError("target not explicitly bound to claim")
        if not 0 <= min_probability <= 1:
            raise ValueError("bad decision threshold")
        target_embedding = target.embedding if target is not None else claim.embedding
        probabilities = self.probabilities(
            claim.embedding, source.embedding, target_embedding,
        )
        role = max(RELATION_CLASSES, key=lambda r: (probabilities[r], -RELATION_CLASSES.index(r)))
        if role == "UNRELATED" or probabilities[role] < min_probability:
            return None
        # Hard typing: a SUPPORT edge points to a CLAIM. Other edge types
        # necessarily point to another document/evidence unit.
        if target is None and role != "SUPPORT":
            return None
        if target is not None and role == "SUPPORT":
            return None
        return EpistemicProposal(
            source_id=source.unit_id,
            target_id=claim.claim_id if target is None else target.unit_id,
            kind=role,
            claim_id=claim.claim_id,
            confidence=probabilities[role],
            origin="model_predicted",
            source_anchor="",
        )
