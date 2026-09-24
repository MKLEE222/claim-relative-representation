# Minimal Sufficient Carrier Search Contract v1

Date frozen: 2026-09-24
Status: PRE-EXPERIMENT CONTRACT

## Question

For a frozen scholarly task tau and recovery contract K, which source-grounded carrier sets preserve the registered task output?

Let C_tau be a finite, preregistered family of carrier coordinates.

For S subseteq C_tau, let P_S(R) denote the representation exposed after retaining only the coordinates in S plus background explicitly declared by the task contract.

S is task-sufficient when one frozen decoder can reproduce the full-reference task output for every registered instance:

\[
D_S(P_S(R),input_\tau)=Y^*_\tau.
\]

S is minimal sufficient when no strict subset of S is sufficient.

The family is:

\[
\mathcal M_{\tau,K}
=
\{S: S\text{ sufficient and no }S'\subset S\text{ sufficient}\}.
\]

## Important scope

This is not a claim about:
- globally minimal representations;
- minimum file size;
- semantic completeness;
- historical truth.

It is a task-relative carrier result.

## Stage 0 - support feasibility

Before subset search:

1. the scholarly task must be executable on the intact native/workflow representation;
2. every candidate carrier must actually exist under the frozen representation contract;
3. the target/output function must be frozen.

If the intact task cannot be instantiated, return SUPPORT_UNAVAILABLE.

Do not search carrier subsets.

## Stage 1 - fixed task output

The task input and output do not change across subsets.

Removing a carrier while simultaneously weakening the task is prohibited.

This separates:
- representation under-measurement;
from
- legitimate task restriction.

## Stage 2 - subset evaluation

For each S subseteq C_tau:

- construct the declared projection without target-dependent repairs;
- run the frozen decoder;
- compare against the intact reference output;
- record exact match / ambiguity / unsupported / contradiction.

A subset is sufficient only if it succeeds on every registered task instance in the declared evaluation population.

## Stage 3 - minimality

A sufficient subset is minimal only if every strict subset fails.

Failure may arise because:
- the task input can no longer address the right record;
- an output coordinate is absent;
- multiple outputs remain compatible with the projection;
- source binding becomes ambiguous;
- the decoder becomes undefined.

## Multiple minimal families

More than one minimal sufficient carrier set may exist.

This is expected under carrier substitution.

Do not collapse multiple families into a scalar representation rank.

## Native versus derived carriers

Candidate carriers are typed:

- NATIVE: directly present in the external/project source;
- WORKFLOW: deterministically derived before outcome evaluation;
- CONTROLLED: introduced only for mechanism testing.

A derived carrier may be task-sufficient without being globally equivalent to its source representation.

## Cost is separate

Two minimal carrier sets can have different access/reconstruction burden.

Minimality here concerns information/task sufficiency, not minimum human time or storage size unless separately measured.

## Evidence authorities

- untouched holdout subset search: transfer evidence;
- already-inspected object subset search: mechanism/development evidence;
- schema tautology alone: construction evidence only.

No pooled success rate across materials.

## Prior-method ancestry

The contract deliberately reuses:
- support-feasibility-before-complexity;
- fixed-target comparison;
- contract-relative adequacy;
- exact held-out opening discipline.

These are methodological ancestry.

The present scientific object is the carrier family required by a scholarly representation task.
