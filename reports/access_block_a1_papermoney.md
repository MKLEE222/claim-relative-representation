# Access Block A1 - Native/workflow paper-money ecological result

Date: 2026-09-24

Authoritative runs:
- E1: GitHub Actions 35954991944
- E1D: GitHub Actions 35955133063
- E1W corrected PM02-bound run: GitHub Actions 35955334992

## Provenance

All authoritative runs fetched the live Project Gutenberg native texts directly.

Observed SHA-256:
- Volume I: 7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5
- Volume II: c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

These equal the hashes frozen in the source registry before the access experiments.

The ecological anchor therefore uses the independently existing native digital objects, not an experiment-authored surrogate.

## Result sequence

### E1 - scope plus generic seed similarity

Current-object-only:
- PM03 outside scope.

Two-volume collection:
- PM03 inside scope;
- rank 5835 / 6033;
- Hit@20 = 0.

Conclusion:
availability is not practical retrievability under the frozen generic seed-similarity policy.

### E1D - source chaining without sequence restriction

Named-source chain:
- 203 candidates;
- PM03 ordinal 185.

Named-source + seed-domain filter:
- 48 candidates;
- PM03 ordinal 36.

Conclusion:
a retrieval policy can reduce inspection burden substantially while still leaving PM03 difficult to surface.

### E1W - sequence-guided scholarly chaining

The native Volume-II object explicitly identifies its 1920 Addenda section. The workflow therefore uses the task request for "later treatment" to enter that native later layer before applying seed-derived chaining.

Named-source chain within Addenda:
- 26 candidates;
- PM03 ordinal 7.

Named-source + PM02 seed-domain filter within Addenda:
- 12 candidates;
- PM03 ordinal 1.

No query used the target-only name LAUFER.

## Mechanistic interpretation

The paper-money carrier now supports a three-stage distinction:

1. **Availability**
   - the evidence must be inside the allowed object horizon.

2. **Retrievability**
   - a retrieval/navigation policy must surface it within a feasible inspection budget.

3. **Relevance recognition**
   - a scholar must recognize the surfaced candidate as evidentially relevant.

Only stages 1-2 were tested here.

The result rejects both of the following simplistic stories:

- "more context automatically solves discovery";
- "representation alone determines discoverability."

Instead, the observed mechanism is task/workflow-relative:

native edition structure + sequence-aware navigation + seed-grounded chaining -> lower retrieval burden.

## Anti-idealization value

No source-aligned CEDL relation field was used to retrieve PM03.

The successful workflow used only:
- native Gutenberg text;
- native Addenda section structure;
- the task requirement to seek later treatment;
- source/topic terms already present in PM02.

The CEDL reference was used only to identify the PM03 evaluation target after candidate generation.

## Claim ceiling

This is an ecological workflow result, but not yet a confirmatory generalized claim.

Why:
- the sequence-guided workflow was designed after E1/E1D diagnostics;
- only one carrier family has been demonstrated;
- human relevance recognition is untested.

Therefore the result is **exploratory Tier-3 candidate evidence**.

Before promotion:
1. freeze the workflow family;
2. run an unchanged or rule-equivalent holdout replication on another case;
3. preserve null/failed holdout results;
4. then consider a human recognition stage.

## Implementation note

An intermediate E1W run located the Addenda correctly but used an earlier non-PM02 Bretschneider occurrence when deriving seed context, yielding an empty domain-term set. That run is not authoritative for the domain policy.

The corrected run anchors seed context on PM02-specific "Broussonetia" before extracting Bretschneider/domain terms. The corrected run is 35955334992.
