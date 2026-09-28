# Module I origin-evidence contract v1

Date: 2026-09-28
Status: PRE-HOLDOUT CONTRACT FROZEN FROM EXPOSED BERLIN/PAUL SOURCE AUDIT.

## 1. Development evidence

A full scan of the chosen-language origin paragraph found:
- Berlin: 7 documents with more than one origDate;
- Paul: 3 documents with more than one origDate.

The multiple origDate elements do not have one uniform semantics.

Observed exposed patterns include:

### Range endpoints
- 'between 30 November and 2 December 1763' encoded as two point origDate elements;
- 'July-August 1921' / 'February-March 1922' encoded as two month origDate elements;
- lower/upper open constraints encoded in separate origDate elements.

### Explicit alternatives
- '23 June 1832 ... or 23 January 1832';
- '7 July 1832 or 27 July 1832';
- '7 August 1832 ... or 5 August 1832'.

### Primary estimate plus supporting temporal constraint
- 'spring 1805' plus a second origDate stating the letter must be after 1 March 1805.

Therefore element cardinality alone does not determine whether multiple origDate values mean:
- one continuous range;
- discrete alternatives;
- or a claim plus evidential constraint.

## 2. Frozen conservative rule

For Module I v2, OPEN_ORIGIN is executable only when the chosen canonical origin paragraph contains exactly ONE machine-readable origDate element.

If the chosen paragraph contains:
- zero machine-readable origDate elements: `NO_ORIGIN_EVIDENCE`;
- more than one machine-readable origDate element: `COMPOSITE_ORIGIN_UNRESOLVED`.

A `COMPOSITE_ORIGIN_UNRESOLVED` document:
- remains in the total parsed population;
- remains in the primary-discovery manifest if its t0 state is discovery-eligible;
- is NOT admitted to FULL_TRAJECTORY;
- is reported with the exclusion reason;
- is not simplified, convex-hulled, or converted to an alternative set in Module I.

## 3. Rationale

The aim is not to claim that multi-origDate editorial statements are uninterpretable.

The aim is to avoid introducing an unvalidated semantic decoder into the final prospective holdout.

A later study may model composite origin propositions with explicit discourse semantics, but such a decoder would be a new research object and cannot be developed on the final holdout.

## 4. Independence requirement

Oracle and runtime must independently:
- choose the same language paragraph;
- count machine-readable origDate elements;
- either extract the one admissible origin claim or classify the origin as composite unresolved.

A disagreement is `CONTRACT_UNRESOLVED`.

## 5. Holdout rule

This contract is frozen before any StaBi/Correspondence XML body is opened.

No holdout-specific composition rule may be added.

If the rule reduces the prospective full-trajectory pool below 5, the Module I mother-problem gate fails rather than being repaired.