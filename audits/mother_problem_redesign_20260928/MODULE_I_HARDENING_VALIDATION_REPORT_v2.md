# Module I pre-holdout evaluator hardening validation report v2

Date: 2026-09-28
Status: FINAL PRE-HOLDOUT VALIDATION. STABI XML BODIES REMAIN UNOPENED.

## 1. Why the old evaluator was rejected

The earlier Module I implementation was not accepted for confirmatory use because several pass conditions were partially definitional:
- discovery policy and discovery gold reused the same eligibility function;
- runtime warrant and gold warrant reused the same function;
- null-event stability was implemented by copying state;
- collateral revision was assigned rather than measured from a full-state diff;
- unresolved-alternative persistence was inferred from final warrant equality;
- transition audit was inferred from interface type rather than reconstructed from history.

Module H's earlier 77/77 result remains invalid for a separate document-boundary failure involving annex dates.

## 2. Final architecture

Independent oracle: oracle_v2.py
- stdlib xml.etree.ElementTree;
- independent primary-document boundary, t0 carriers, D1/D2, Q0, origin contract, root/post warrant, required live alternatives and null-event expected non-effect;
- imports no runtime/evaluator logic.

Runtime: runtime_v2.py
- lxml;
- separately implemented parsing, eligibility and warrant logic;
- explicit mutable research state;
- actual OPEN_ORIGIN and controlled-null transitions;
- applicability checks;
- evidence/event/transition ledgers;
- structural temporal-state diff and measured collateral mutations;
- delayed audit reconstructed from retained history.

Evaluator: evaluator_v2.py
- compares serialized runtime traces against independent oracle outputs only.

Runner: run.py
- oracle determines denominator/gold;
- runtime produces trajectories;
- parser/source-contract disagreement becomes CONTRACT_UNRESOLVED;
- no full oracle-eligible episode is silently dropped for runtime failure.

## 3. Pre-holdout repairs

Document boundary:
- current-document datelines are restricted to the selected primary div type=letter;
- sibling/nested annex documents are excluded;
- independent parsers must agree on the primary-document boundary signature.

Controlled null event:
- natural revisionDesc maintenance is not a full-trajectory gate;
- every episode receives CONTROL_NULL_V1 / REFRESH_NON_TEMPORAL_METADATA_INDEX with temporal_targets empty;
- it is executed through the runtime transition operator;
- stability is measured from actual temporal before/after diff;
- it is a causal control, not natural historical evidence.

Composite origin evidence:
- exposed Berlin/Paul audit showed multi-origDate paragraphs encode heterogeneous semantics: range endpoints, explicit alternatives, and estimate-plus-constraint;
- exactly one machine-readable origDate is admissible;
- zero means NO_ORIGIN_EVIDENCE;
- more than one means COMPOSITE_ORIGIN_UNRESOLVED;
- composite documents remain in population/primary manifest but cannot enter FULL_TRAJECTORY.

## 4. Adversarial validation

Authoritative hardening CI run: 36417199855
Head: 65d05821be73010c8d3ffef8ad4774fe9d159b17

Detected failures:
- F1 annex contamination: DETECTED
- F2 wrong origin binding: DETECTED
- F3 wrong warrant: DETECTED
- F4 collateral temporal mutation: DETECTED
- F5 dropped source-bound live alternative: DETECTED
- F6 neutral event mutates temporal warrant: DETECTED
- F7 missing transition history: DETECTED
- F8 wrong document boundary: DETECTED
- F9 composite origin silently simplified: DETECTED

Negative compatible-date control: no question invented.
Independent synthetic exact branch: D2 root, INTERVAL root warrant, EXACT post-origin warrant, R* end-to-end PASS.
The synthetic exact branch is implementation coverage only, not empirical evidence.

## 5. Berlin exposed development verification

Population:
- 190 parsed; 0 parse errors;
- 29 primary discovery episodes;
- 20 full trajectories after conservative origin contract;
- 0 full-trajectory contract unresolved.

R*:
- Q0/discovery/applicability/warrant/selective update/alternative persistence/null stability/provenance/history/end-to-end: 20/20.

Ablations:
- I_NO_ALTERNATIVES end-to-end: 0/20;
- I_NO_BINDING end-to-end: 0/20;
- I_NO_HISTORY end-to-end: 0/20.

Result SHA-256: 0a15dd4237cca184b468e3e86070a72acffd66db12b3e3c28450cf90f4de9b50
Source-audit SHA-256: 13ff01a464efcc377f29e30b2578047bbcc7f5175adc3bf9de6c87f656e357dc
Artifact ID: 10968172665
Artifact ZIP digest: d77a24015ec6c3f67a72b5461464d650dbbaac15640e24a641901b9cb02f84fe

Natural full-trajectory post-origin warrant types:
- INTERVAL 16;
- ALTERNATIVE_SET 4;
- EXACT 0.

## 6. Paul exposed development verification

Population:
- 1515 parsed; 0 parse errors;
- 26 primary discovery episodes;
- 21 full trajectories after conservative origin contract;
- 0 full-trajectory contract unresolved.

R*:
- Q0/discovery/applicability/warrant/selective update/alternative persistence/null stability/provenance/history/end-to-end: 21/21.

Ablations:
- I_NO_ALTERNATIVES end-to-end: 0/21;
- I_NO_BINDING end-to-end: 0/21;
- I_NO_HISTORY end-to-end: 0/21.

Result SHA-256: 451d3570957dfb6b65b4339560789f196be034bc40863d8e97c8124dcb4d9ddd
Source-audit SHA-256: 42a10a331e1bd93a7c2cd72aa74c218bf10549852f8d0ec77b8ef7d37f39a914
Artifact ID: 10967982832
Artifact ZIP digest: 961a0003b91a06826a58cd9d3375ec2cbc7140e9ad363159fdefb86ba75085df

Natural full-trajectory post-origin warrant types:
- ALTERNATIVE_SET 13;
- INTERVAL 8;
- EXACT 0.

## 7. Source-level audit

Twenty deterministic exposed development episodes were reviewed against raw XML.
Coverage includes D1, D2, INTERVAL, ALTERNATIVE_SET, source-bound unresolved alternatives, Paul annexes, and real machine/text inconsistencies.

Examples confirmed from source:
- Paul Lettre0426: docDate/sent/origDate 1916-10-16; primary-letter dateline 1918-10-16; annex is separate and excluded.
- Paul Lettre0235: docDate/sent/origDate 1917-03-15; visible dateline says 15 March; machine when-iso is 1917-03-13.
- Paul Lettre0518: docDate/sent/origDate 1919-04-16; primary dateline 1919-04-18; annex date is excluded.
- Paul Lettre0124: docDate/sent/origDate 1916-02-24; primary dateline 1908-02-24.
- Berlin Brief007: docDate/sent/origDate 1818-03-28; primary dateline machine value 1818-03-08; visible day is overwritten.

No Module-H-style annex contamination was found in the repaired deterministic sample.

## 8. Multi-origDate audit

Chosen-language origin paragraphs with more than one origDate:
- Berlin 7;
- Paul 3.

Observed semantics are heterogeneous, which is the empirical basis for COMPOSITE_ORIGIN_UNRESOLVED.
No composite-origin episode is used as a clean later-evidence event.

## 9. Natural development coverage limitation

The exposed Berlin/Paul FULL_TRAJECTORY populations contain no natural post-origin EXACT warrant.
Natural source-level validation therefore covers INTERVAL and ALTERNATIVE_SET.
EXACT execution is covered only by the independent synthetic contract test.
This limitation is retained explicitly.

## 10. Frozen evaluator SHA-256 identities

Recorded by CI at head 65d05821be73010c8d3ffef8ad4774fe9d159b17:

oracle_v2.py
e6ea25a48a93735446f537022935ac6f91ee23594d845277e30e787dbb950923

runtime_v2.py
a5c6d6f7da6da7a82f08a0d93963391659a01bc2100a42b542677e0faa6c601c

evaluator_v2.py
d6ea112af6d765720350c86858f4622c8b403fd6e1668674587e276fe90ac9a0

run.py
a86a4ac67b9fbabce21d4e7d2b84c20641c9b01c9597a74d4867dfe5877a756d

test_hardening_v2.py
ceab53bc483a34f08f559c00729463226b632cb7ad6c955602fe9ba0bc654772

These files are scientifically frozen for the prospective StaBi execution.
Any byte change requires a new evaluator version and forfeits the planned one-time execution under this freeze.

## 11. Claim boundary

Validated before holdout:
- document boundary;
- independent parser agreement;
- independent discovery oracle;
- independent warrant oracle;
- actual OPEN_ORIGIN;
- applicability;
- actual controlled-null transition;
- measured collateral diff;
- source-bound alternative persistence;
- ledger-based delayed audit;
- D1/D2;
- natural INTERVAL/ALTERNATIVE_SET development cases;
- synthetic EXACT branch;
- F1-F9 adversarial detection.

Not claimed:
- autonomous open-ended discovery beyond frozen D1/D2;
- independent historical truth of editorial origDate;
- universal/minimal representation;
- natural null events in Module I;
- natural EXACT post-origin development coverage.

## 12. Decision

The previous Module I evaluator is retired.
The hardened evaluator is PRE-HOLDOUT VALIDATED AND FROZEN.
The fresh StaBi holdout remains unopened at the time of this report.

A separate one-time holdout workflow may be created only if it:
- verifies all five frozen SHA-256 identities before execution;
- uses only the frozen StaBi prefix;
- runs in holdout mode;
- uploads complete results and source-audit manifest;
- does not automatically rerun on later pushes.