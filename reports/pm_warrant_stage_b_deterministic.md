# Paper-Money Stage-B Deterministic Result

Date: 2026-09-25
Status: PRE-LLM RESULT

## Frozen inputs

Candidate budget:
12

Generic declared-collection retrieval:
PM03 rank = 5835.

Sequence-guided domain chain:
PM03 ordinal = 1 of 12.

These are prior authoritative access results, not recomputed for this stage.

## Active evidence states

### GENERIC_TOP12

Active frozen case events:

- PM01
- PM02

PM03 is not in the active candidate budget.

Historically explicit stance traces exposed:

- PMT01 — Bretschneider criticism of Polo's material identification.

### GUIDED_TOP12

Active frozen case events:

- PM01
- PM02
- PM03

Historically explicit stance traces exposed:

- PMT01 — Bretschneider criticism;
- PMT02 — Laufer's explicit correction of Bretschneider;
- PMT03 — Laufer's explicit endorsement of Polo's material identification.

## Deterministic consequence

The two conditions therefore differ before any LLM adjudication:

\[
A_{trace}(E_{generic})=\{PMT01\}
\]

\[
A_{trace}(E_{guided})=\{PMT01,PMT02,PMT03\}
\]

with:

\[
A_{trace}(E_{guided})\setminus A_{trace}(E_{generic})
=
\{PMT02,PMT03\}.
\]

This establishes an active-evidence consequence without assigning our own E_* relation or warrant state.

## Interpretation

The generic condition exposes an explicit historical criticism but not the later explicit correction/endorsement within the fixed budget.

The guided condition exposes both the criticism and the later archival correction/endorsement.

This is the strongest result currently authorized before the final LLM layer.

## Not claimed

No claim is made here that:
- PMT01 equals E_UNDERCUT;
- PMT02 equals E_REHABILITATE;
- PMT03 equals E_SUPPORT;
- the two conditions must receive different warrant states.

Those are final adjudication questions.

## Next gate

Freeze anonymous packet construction and the LLM judge contract.

Do not execute the judge until every prompt/schema/stability test is frozen.
