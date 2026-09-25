# Warrant Closure Metric Status

Date: 2026-09-25
Status: BLOCKED PENDING STRICT TARGET-IDENTITY AUDIT

The pre-LLM warrant closure must not rely on the original proximity-based target ordinal/rank metric.

Reason:
the original evaluation counted a candidate as a target hit when its sliding-window start was within one stride of a target window. A neighboring candidate could therefore be counted even when it did not itself visibly contain the target anchors.

The strict audit is now frozen in:

experiments/ecological_anchor_target_identity_audit/

Until it completes on the frozen Gutenberg hashes:

- PM03 presence in the guided top-12 packet is NOT treated as confirmatory;
- reports/pm_warrant_stage_b_deterministic.md is provisional and not manuscript-authoritative;
- no LLM judge may run.

This block is methodological, not a negative scientific result.
