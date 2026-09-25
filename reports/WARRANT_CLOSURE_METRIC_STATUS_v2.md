# Warrant Closure Metric Status v2

Date: 2026-09-25
Status: RESOLVED

The precautionary concern about the E1/E1D/E1W abs(start-target.start) < STRIDE target rule has been audited.

Because target and candidate windows are generated from the same zero-origin stride-90 grid, all starts are multiples of 90. Therefore |s_c-s_t|<90 can hold only when s_c=s_t.

The historical code was therefore matching the exact target sliding window, not an adjacent window.

The candidate logs printed only the first 20 of 180 tokens, which explains why the target anchors were not always visible in the displayed snippet.

## Downstream disposition

The authoritative access results remain usable:

- generic declared collection: PM03 rank 5835;
- sequence-guided domain chain: PM03 ordinal 1 / 12.

The pre-LLM Stage-B active-evidence result is unblocked and may treat PM03 as absent/present respectively under budget 12.

No LLM judge has been run.