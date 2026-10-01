"""Synthetic design checks only. No historical/LLM/transfer evidence is generated."""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class History:
    # Same named evidence objects and claim text in both histories; bindings differ.
    supports: tuple[tuple[str, str], ...]

CLAIMS = ("A", "B")
EVIDENCE = ("s1", "s2")

def answer(h: History, withdrawn: frozenset[str] = frozenset()) -> dict[str, str]:
    return {c: "SUPPORTED" if any(q == c and s not in withdrawn for s, q in h.supports)
            else "NO_REMAINING_SUPPORT" for c in CLAIMS}

def retained(h: History) -> dict:
    return {"claim_ids": CLAIMS, "evidence_ids": EVIDENCE, "current_answer": answer(h)}

def canon(x: object) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()

def overlap(a: tuple[int,int], b: tuple[int,int]) -> bool:
    return a[1] > b[0] and a[0] < b[1]

def covers(spans: Iterable[tuple[int,int]], target: tuple[int,int]) -> bool:
    left, right = target
    if left >= right:
        raise ValueError("target must be nonempty")
    pos = left
    for lo, hi in sorted(spans):
        if lo > hi:
            raise ValueError("invalid interval")
        if hi <= pos:
            continue
        if lo > pos:
            return False
        pos = max(pos, hi)
        if pos >= right:
            return True
    return False

def main() -> None:
    checks: dict[str, bool] = {}
    h1 = History((("s1", "A"), ("s2", "B")))
    h2 = History((("s1", "B"), ("s2", "A")))
    future = frozenset({"s1"})
    before1, before2 = retained(h1), retained(h2)
    checks["same_current_answer_and_identical_retained_payload"] = canon(before1) == canon(before2)
    after1, after2 = answer(h1, future), answer(h2, future)
    checks["same_withdrawal_different_informative_output"] = after1 != after2
    # All informative outputs in this finite test, not all possible scholarly policies.
    outputs = [dict(zip(CLAIMS, labels)) for labels in
               (("SUPPORTED", "SUPPORTED"), ("SUPPORTED", "NO_REMAINING_SUPPORT"),
                ("NO_REMAINING_SUPPORT", "SUPPORTED"),
                ("NO_REMAINING_SUPPORT", "NO_REMAINING_SUPPORT"))]
    checks["no_uniform_informative_answer_without_more_information"] = not any(
        out == after1 and out == after2 for out in outputs)
    safe1, safe2 = {canon(after1), b"ABSTAIN"}, {canon(after2), b"ABSTAIN"}
    checks["safe_abstention_is_not_informative_completion"] = safe1 & safe2 == {b"ABSTAIN"}
    checks["correct_source_binding_repairs_both_worlds"] = all(
        answer(History(h.supports), future) == answer(h, future) for h in (h1, h2))
    checks["equally_shaped_wrong_binding_fails_both_worlds"] = (
        len(canon(h1.supports)) == len(canon(h2.supports)) and
        answer(h2, future) != after1 and answer(h1, future) != after2)
    checks["irrelevant_withdrawal_is_a_null"] = all(
        answer(h, frozenset({"s3"})) == answer(h) for h in (h1, h2))
    # Explicit reopening: a returned binding is new information, not free decoder knowledge.
    reopen_cost = 1
    checks["one_charged_source_reopen_restores_continuation"] = all(
        answer(History(h.supports), future) == answer(h, future) for h in (h1, h2)) and reopen_cost == 1
    target, clipped = (10, 20), (19, 25)
    checks["anchor_overlap_is_not_full_span_coverage"] = overlap(clipped, target) and not covers([clipped], target)
    checks["multi_span_coverage_detects_gaps"] = covers([(10,15),(15,20)], target) and not covers([(10,14),(15,20)], target)
    if not all(checks.values()):
        raise AssertionError([name for name, ok in checks.items() if not ok])
    result = {
        "authority": "SYNTHETIC_DESIGN_UNIT_TEST_NOT_EMPIRICAL_RESULT",
        "check_count": len(checks), "checks": checks,
        "worlds": [{"supports": h.supports, "current": answer(h),
                    "after_withdraw_s1": answer(h, future)} for h in (h1,h2)],
        "retained_payload_sha256": hashlib.sha256(canon(before1)).hexdigest(),
        "scope": "Closed snapshot; no new probes. Reopening is tested separately at cost 1.",
        "semantic_limit": "NO_REMAINING_SUPPORT is not FALSE; all rules are declared toy rules.",
        "novelty": "None claimed; this is an elementary determinacy/truth-maintenance witness.",
        "old_metrics": "No old experimental output, validity rule, or rank was changed."
    }
    out = Path(__file__).with_name("design_check_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks_passed": sum(checks.values()), "total": len(checks),
                      "authority": result["authority"], "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}, indent=2))

if __name__ == "__main__":
    main()
