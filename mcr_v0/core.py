"""MCR v0: an LLM-facing, claim-conditioned mediated-text evidence representation.

This module computes a budgeted *proposed evidence state*, NOT historical truth,
human warrant, or verified model accuracy. Frozen text embeddings and model-
proposed epistemic edges are external inputs. Source-verified documentary edges
(G_D) and proposed epistemic relations (G_E_hat) remain strictly separate.

Python 3.10+ / standard library. All internal tests are SYNTHETIC_DEV.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import json
import math
from typing import Iterable

VERIFIED = frozenset({"PAGE_VERIFIED", "OBJECT_VERIFIED"})
DOCUMENT_ROLES = frozenset({"PRIMARY", "EDITION", "TRANSLATION", "COMMENTARY", "OTHER"})
DOC_RELATIONS = frozenset({"CITES", "DERIVED_FROM", "VARIANT_OF", "TRANSLATES", "ATTACHED_NOTE", "IDENTIFIES_REFERENT"})
EPI_RELATIONS = frozenset({"SUPPORT", "UNDERCUT", "REHABILITATE", "QUALIFY"})
ALLOWED_ORIGINS = frozenset({"model_predicted", "source_attested", "simulated"})


def _vector(value: tuple[float, ...], name: str) -> tuple[float, ...]:
    out = tuple(float(x) for x in value)
    if not out or not all(math.isfinite(x) for x in out):
        raise ValueError(f"{name}: nonempty finite vector required")
    return out


def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if len(a) != len(b):
        raise ValueError("embedding dimensions differ")
    an = math.sqrt(sum(x * x for x in a))
    bn = math.sqrt(sum(x * x for x in b))
    if an == 0.0 or bn == 0.0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (an * bn)


@dataclass(frozen=True)
class Claim:
    claim_id: str
    question: str
    embedding: tuple[float, ...]
    requires_primary_wording: bool = False
    requires_documentary_bridge: bool = False

    def __post_init__(self) -> None:
        if not self.claim_id or not self.question:
            raise ValueError("claim ID and question required")
        object.__setattr__(self, "embedding", _vector(self.embedding, "claim"))


@dataclass(frozen=True)
class EvidenceUnit:
    unit_id: str
    text: str
    embedding: tuple[float, ...]
    source_id: str
    source_anchor: str
    edition: str
    documentary_role: str
    verification: str
    claim_scope: tuple[str, ...]
    token_cost: int = 1

    def __post_init__(self) -> None:
        if not all((self.unit_id, self.text, self.source_id, self.source_anchor, self.edition)):
            raise ValueError("unit text and source identifiers cannot be empty")
        if self.documentary_role not in DOCUMENT_ROLES:
            raise ValueError("unknown documentary role")
        if self.verification not in VERIFIED | {"PROVISIONAL_DIGITAL_ONLY", "BLOCKED"}:
            raise ValueError("unknown witness verification status")
        if type(self.token_cost) is not int or self.token_cost < 1:
            raise ValueError("token_cost must be positive integer")
        if not self.claim_scope or not all(self.claim_scope):
            raise ValueError("claim_scope required, never infer binding from text")
        object.__setattr__(self, "embedding", _vector(self.embedding, "evidence"))


@dataclass(frozen=True)
class DocumentaryEdge:
    """A source-verified relation in G_D. NEVER an epistemic implication."""

    child_id: str
    parent_id: str
    kind: str
    source_anchor: str
    verified: bool

    def __post_init__(self) -> None:
        if self.kind not in DOC_RELATIONS or not self.source_anchor:
            raise ValueError("invalid documentary link")
        if type(self.verified) is not bool:
            raise ValueError("verified must be boolean")


@dataclass(frozen=True)
class EpistemicProposal:
    """A source-anchored *candidate* G_E_hat relation, not a gold verdict."""

    source_id: str
    target_id: str  # a witness, or the exact Claim.claim_id for SUPPORT
    kind: str
    claim_id: str
    confidence: float
    origin: str
    source_anchor: str = ""

    def __post_init__(self) -> None:
        if self.kind not in EPI_RELATIONS or self.origin not in ALLOWED_ORIGINS:
            raise ValueError("unknown relation or origin; gold labels forbidden")
        if not self.source_id or not self.target_id or not self.claim_id:
            raise ValueError("explicit source, target and claim IDs required")
        if not math.isfinite(self.confidence) or not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
        if self.origin == "source_attested" and not self.source_anchor:
            raise ValueError("source-attested stance requires native span anchor")


@dataclass(frozen=True)
class EvidenceGraph:
    claim: Claim
    units: tuple[EvidenceUnit, ...]
    documentary: tuple[DocumentaryEdge, ...]
    proposals: tuple[EpistemicProposal, ...]
    externally_attested_roster_complete: bool = False

    def __post_init__(self) -> None:
        ids = [u.unit_id for u in self.units]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate evidence unit")
        if any(len(u.embedding) != len(self.claim.embedding) for u in self.units):
            raise ValueError("embedding space mismatch")
        known = set(ids)
        for d in self.documentary:
            if d.child_id not in known or d.parent_id not in known:
                raise ValueError("documentary link points outside declared evidence graph")
        for e in self.proposals:
            if e.source_id not in known:
                raise ValueError("proposal source missing")
            if e.kind == "SUPPORT":
                if e.target_id != e.claim_id:
                    raise ValueError("SUPPORT requires exact claim target")
            elif e.target_id not in known:
                raise ValueError("non-support proposal must target existing evidence")
            # Other claim proposals MAY appear in the graph; they must be filtered.
        if type(self.externally_attested_roster_complete) is not bool:
            raise ValueError("roster flag must be an externally supplied boolean")


def _eligible(graph: EvidenceGraph, unit: EvidenceUnit) -> tuple[bool, str]:
    claim = graph.claim
    if claim.claim_id not in unit.claim_scope:
        return False, "CLAIM_BINDING_NOT_ESTABLISHED"
    if unit.verification not in VERIFIED:
        return False, "SOURCE_NOT_VERIFIED"
    if claim.requires_primary_wording and unit.documentary_role != "PRIMARY":
        return False, "NOT_PRIMARY_WORDING"
    if claim.requires_documentary_bridge:
        bridge = any(
            d.child_id == unit.unit_id and d.verified
            and d.kind in {"IDENTIFIES_REFERENT", "CITES", "DERIVED_FROM", "ATTACHED_NOTE"}
            for d in graph.documentary
        )
        if not bridge:
            return False, "DOCUMENTARY_BRIDGE_UNAVAILABLE"
    return True, ""


def _qualified(graph: EvidenceGraph) -> tuple[dict[str, EvidenceUnit], dict[str, str]]:
    allowed, excluded = {}, {}
    for unit in graph.units:
        ok, reason = _eligible(graph, unit)
        if ok:
            allowed[unit.unit_id] = unit
        else:
            excluded[unit.unit_id] = reason
    return allowed, excluded


def _active_relations(
    graph: EvidenceGraph,
    allowed: dict[str, EvidenceUnit],
) -> tuple[EpistemicProposal, ...]:
    return tuple(
        sorted(
            (e for e in graph.proposals
             if e.claim_id == graph.claim.claim_id
             and e.source_id in allowed
             and (e.kind == "SUPPORT" or e.target_id in allowed)),
            key=lambda e: (e.kind, e.source_id, e.target_id, e.origin),
        )
    )


def _base_relevance(graph: EvidenceGraph, allowed: dict[str, EvidenceUnit]) -> dict[str, float]:
    return {
        uid: max(0.0, cosine(graph.claim.embedding, u.embedding))
        for uid, u in allowed.items()
    }


def _state_objective(
    ids: frozenset[str],
    relevance: dict[str, float],
    relations: tuple[EpistemicProposal, ...],
) -> float:
    """V0 *heuristic* budget score, not a new optimality / learning theorem.

    Include semantic similarity, typed edge co-coverage and penalties for
    omitting known candidate counters to selected premises.
    """
    score = sum(relevance[uid] for uid in ids)
    for e in relations:
        if e.kind == "SUPPORT":
            if e.source_id in ids:
                score += 0.20 * e.confidence
            continue
        if e.target_id in ids and e.source_id in ids:
            score += 1.10 * e.confidence
        elif e.target_id in ids and e.source_id not in ids:
            score -= 1.30 * e.confidence
        elif e.source_id in ids:
            score -= 0.25 * e.confidence
    return score


def _select_budget(
    allowed: dict[str, EvidenceUnit],
    relevance: dict[str, float],
    relations: tuple[EpistemicProposal, ...],
    budget: int,
) -> tuple[tuple[str, ...], bool]:
    """Exact objective maximization for <=16 units; GREEDY otherwise.

    The objective is NOT the scientific correctness metric. Output always
    identifies whether selection was exact for THIS heuristic objective.
    """
    ids = sorted(allowed)
    if len(ids) <= 16:
        best = (0.0, ())  # empty packet must remain a legal choice
        for n in range(1, len(ids) + 1):
            for chosen in combinations(ids, n):
                if sum(allowed[x].token_cost for x in chosen) > budget:
                    continue
                score = _state_objective(frozenset(chosen), relevance, relations)
                cand = (round(score, 12), chosen)
                if cand > best:
                    best = cand
        return tuple(best[1]), True
    chosen: set[str] = set()
    spent = 0
    while True:
        old = _state_objective(frozenset(chosen), relevance, relations)
        gains = []
        for uid in ids:
            if uid in chosen or spent + allowed[uid].token_cost > budget:
                continue
            new = _state_objective(frozenset(chosen | {uid}), relevance, relations)
            gains.append(((new - old) / allowed[uid].token_cost, uid, new - old))
        if not gains:
            break
        gains.sort(key=lambda x: (-x[0], x[1]))
        _, uid, improvement = gains[0]
        if improvement <= 0:
            break
        chosen.add(uid)
        spent += allowed[uid].token_cost
    return tuple(sorted(chosen)), False


def dense_topk(graph: EvidenceGraph, budget: int) -> tuple[str, ...]:
    """Dense cosine baseline, using EXACTLY the same qualified source set."""
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    allowed, _ = _qualified(graph)
    scores = _base_relevance(graph, allowed)
    order = sorted(allowed, key=lambda x: (-scores[x], x))
    selected, total = [], 0
    for uid in order:
        cost = allowed[uid].token_cost
        if total + cost <= budget:
            selected.append(uid)
            total += cost
    return tuple(selected)


def graph_expansion_baseline(graph: EvidenceGraph, budget: int) -> tuple[str, ...]:
    """Strong simple baseline with same G_E_hat edges, not an ablated oracle.

    Starts at highest dense witness, then expands its counterevidence/replies,
    then fills leftover budget by dense cosine. It has the same source gates.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be nonnegative integer")
    allowed, _ = _qualified(graph)
    if not allowed:
        return ()
    scores = _base_relevance(graph, allowed)
    rels = _active_relations(graph, allowed)
    candidates = sorted(allowed, key=lambda x: (-scores[x], x))
    selected = []
    spent = 0
    for seed in candidates:
        if seed not in selected and spent + allowed[seed].token_cost <= budget:
            selected.append(seed)
            spent += allowed[seed].token_cost
            break
    for _ in range(len(candidates)):
        additions = sorted(
            {e.source_id for e in rels
             if e.kind != "SUPPORT" and e.target_id in selected
             and e.source_id not in selected},
            key=lambda x: (-scores[x], x),
        )
        if not additions:
            break
        changed = False
        for uid in additions:
            if uid not in selected and spent + allowed[uid].token_cost <= budget:
                selected.append(uid)
                spent += allowed[uid].token_cost
                changed = True
        if not changed:
            break
    for uid in candidates:
        if uid not in selected and spent + allowed[uid].token_cost <= budget:
            selected.append(uid)
            spent += allowed[uid].token_cost
    return tuple(sorted(selected))


def _weighted_mean(
    elements: Iterable[tuple[tuple[float, ...], float]],
    dimensions: int,
) -> tuple[float, ...]:
    pairs = [(v, w) for v, w in elements if w > 0]
    if not pairs:
        return tuple(0.0 for _ in range(dimensions))
    denom = sum(w for _, w in pairs)
    return tuple(sum(v[k] * w for v, w in pairs) / denom for k in range(dimensions))


def encode(graph: EvidenceGraph, token_budget: int) -> dict:
    """Build an LLM-facing evidence representation and explicit source limits.

    A role channel is a vector over the SELECTED evidence only. Predicted
    relations change a PROPOSED representation, NOT humanistic truth.
    """
    if type(token_budget) is not int or token_budget < 0:
        raise ValueError("token_budget must be a nonnegative integer")
    allowed, excluded = _qualified(graph)
    relevance = _base_relevance(graph, allowed)
    relations = _active_relations(graph, allowed)
    selected, exact = _select_budget(allowed, relevance, relations, token_budget)
    selected_set = set(selected)
    dims = len(graph.claim.embedding)
    roles: dict[str, list[tuple[tuple[float, ...], float]]] = {
        "affirmation": [], "challenge": [], "response": [], "qualification": [],
        "unclassified": [],
    }
    assigned: set[str] = set()
    for edge in relations:
        if edge.source_id not in selected_set:
            continue
        if edge.kind != "SUPPORT" and edge.target_id not in selected_set:
            continue
        role = {"SUPPORT": "affirmation", "UNDERCUT": "challenge",
                "REHABILITATE": "response", "QUALIFY": "qualification"}[edge.kind]
        roles[role].append((allowed[edge.source_id].embedding, edge.confidence))
        assigned.add(edge.source_id)
    for uid in selected:
        if uid not in assigned:
            roles["unclassified"].append((allowed[uid].embedding, max(relevance[uid], 0.01)))
    channels = {r: list(_weighted_mean(items, dims)) for r, items in roles.items()}
    selected_links = []
    missing_links = []
    for edge in relations:
        if edge.kind == "SUPPORT":
            if edge.source_id in selected_set:
                selected_links.append(edge)
            continue
        if edge.target_id in selected_set and edge.source_id not in selected_set:
            missing_links.append({
                "missing_unit": edge.source_id, "target": edge.target_id,
                "kind": edge.kind, "reason": "BUDGET_OR_SELECTION_OMISSION",
            })
        if edge.source_id in selected_set and edge.target_id not in selected_set:
            missing_links.append({
                "missing_unit": edge.target_id, "target": edge.source_id,
                "kind": edge.kind, "reason": "RELATIONAL_CONTEXT_OMITTED",
            })
        if edge.source_id in selected_set and edge.target_id in selected_set:
            selected_links.append(edge)
    unverified_relations = [
        {"source": e.source_id, "target": e.target_id, "kind": e.kind,
         "reason": "SOURCE_OR_CLAIM_BINDING_NOT_VERIFIED"}
        for e in graph.proposals
        if e.claim_id == graph.claim.claim_id
        and (e.source_id not in allowed or
             (e.kind != "SUPPORT" and e.target_id not in allowed))
    ]
    support_ids = {e.source_id for e in relations if e.kind == "SUPPORT"}
    no_support_in_packet = bool(support_ids) and not any(x in selected_set for x in support_ids)
    documented = [
        {"child": d.child_id, "parent": d.parent_id, "kind": d.kind,
         "source_anchor": d.source_anchor, "verified": d.verified}
        for d in graph.documentary
        if d.child_id in selected_set or d.parent_id in selected_set
    ]
    packet = [{
        "unit_id": uid,
        "text": allowed[uid].text,
        "source_id": allowed[uid].source_id,
        "source_anchor": allowed[uid].source_anchor,
        "edition": allowed[uid].edition,
        "documentary_role": allowed[uid].documentary_role,
        "verification": allowed[uid].verification,
        "token_cost": allowed[uid].token_cost,
        "cosine_relevance": relevance[uid],
    } for uid in selected]
    external_limits = []
    if not graph.externally_attested_roster_complete:
        external_limits.append("SOURCE_ROSTER_COMPLETENESS_NOT_ATTESTED")
    if missing_links or no_support_in_packet:
        external_limits.append("COUNTEREVIDENCE_OR_SUPPORT_PACKET_INCOMPLETE")
    if unverified_relations:
        external_limits.append("SOME_PROPOSED_RELATIONS_HAVE_UNVERIFIED_SOURCES")
    if not exact:
        external_limits.append("HEURISTIC_GREEDY_SELECTION_NOT_EXACT_FOR_V0_OBJECTIVE")
    return {
        "schema": "mcr-claim-conditioned-representation-v0",
        "evidence_class": "PROPOSED_LLM_INPUT_NOT_ADJUDICATED",
        "claim_id": graph.claim.claim_id,
        "claim_question": graph.claim.question,
        "channels": channels,
        "packet": packet,
        "selected_unit_ids": list(selected),
        "selected_proposed_epistemic_links": [
            {"source": e.source_id, "target": e.target_id,
             "kind": e.kind, "confidence": e.confidence,
             "origin": e.origin, "source_anchor": e.source_anchor}
            for e in selected_links
        ],
        "documentary_links": documented,
        "excluded_units": excluded,
        "unverified_relation_proposals": unverified_relations,
        "uncovered_proposal_links": missing_links,
        "known_support_omitted": no_support_in_packet,
        "source_roster_complete_externally_attested":
            graph.externally_attested_roster_complete,
        "reported_limits": external_limits,
        "selection_objective": _state_objective(frozenset(selected), relevance, relations),
        "v0_objective_exact_for_current_graph": exact,
        "token_budget": token_budget,
        "tokens_used": sum(allowed[uid].token_cost for uid in selected),
        "warrant_verdict": "NOT_ADJUDICATED",
    }


def llm_context(state: dict) -> str:
    """Compile a bounded context; it cannot certify predictions as historical truth."""
    if state.get("schema") != "mcr-claim-conditioned-representation-v0":
        raise ValueError("bad MCR state schema")
    lines = [
        "TASK: Explain the claim using only the supplied cited evidence.",
        "Never infer historical truth from an asserted or model-predicted edge.",
        "Explicitly distinguish source wording, editorial interpretation and",
        "unverified relation hypotheses. State uncertainty if material evidence",
        "or a counterevidence link is missing; do not invent an absent source.",
        "CLAIM: " + state["claim_question"],
        "EVIDENCE:",
    ]
    for w in state["packet"]:
        lines.append(
            f"[{w['unit_id']}] {w['text']} "
            f"(source={w['source_id']}, locator={w['source_anchor']}, "
            f"edition={w['edition']}, verified={w['verification']})"
        )
    lines.append("PROPOSED RELATIONS (NOT automatic truth):")
    for e in state["selected_proposed_epistemic_links"]:
        lines.append(
            f"{e['source']} --{e['kind']}--> {e['target']} "
            f"(origin={e['origin']}, model_confidence={e['confidence']:.3f})"
        )
    lines.append("SOURCE-VERIFIED DOCUMENTARY LINKS:")
    for d in state["documentary_links"]:
        if d["verified"]:
            lines.append(f"{d['child']} --{d['kind']}--> {d['parent']} [{d['source_anchor']}]")
    lines.append("BOUNDARIES:")
    lines.extend("- " + r for r in state["reported_limits"])
    lines.append("No humanistic warrant verdict is supplied by this representation.")
    return "\n".join(lines)


def dump_state_json(state: dict) -> str:
    return json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
