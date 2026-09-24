# EP_KS_01 result - generic seed/task access transfer v1

Date: 2026-09-24
Authoritative CI run: 35958872698

## Holdout status

EP_KS_01 was preregistered as a **design-aware near-holdout / pre-outcome transfer test**.

The Tanner episode was known during framework design, but the retrieval outcome under Generic Seed-Task Access Policy v1 was unseen.

## Source integrity

The live Project Gutenberg Volume II hash exactly matched the frozen source-registry hash:

c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c

No target-only evaluation term entered the query.

Frozen query terms:

truth | later | might | editorial | transmission | grandeur | personally | conqueror | injury | surpassing | moved | observed

## Results

### GSA_FULL_OBJECT

- candidates: 3124
- target rank: 2946
- target score: 0
- Hit@50: 0

### GSA_LATER_LAYER

- candidates: 482
- target rank: 304
- target score: 0
- Hit@50: 0

## Disposition

**FAIL_TRANSFER for practical retrieval under v1.**

The task-adapted later-layer horizon reduced the candidate universe substantially:

\[
3124 \rightarrow 482
\]

but it did not create a lexical bridge to the Tanner target.

The target received score 0 in both conditions.

Therefore the rank improvement must not be interpreted as successful retrieval; it is largely a consequence of shrinking the search horizon.

## Mechanistic finding

The seed uses the historical referent form **Kinsay**.

The later Tanner passage uses **Hang Chau**.

The native 1903 editorial context itself contains an explicit referent bridge in Chapter LXXVI Note 1, identifying Kinsay/King-sze/Lin-ngan with present-day Hang-chau.

This reveals a previously separated access problem:

\[
scope\ adaptation \neq referent\ mediation.
\]

A representation can place the target inside the correct historical layer while retrieval still fails because the same referent is carried by different lexical forms.

## Next-step discipline

No v1 parameter will be tuned.

A new exploratory policy may use an explicit **native seed-side alias/identity statement** as an admissible carrier.

Because this mechanism was identified after seeing the v1 failure, such a policy is development on Kinsay, not confirmation.

Any general alias-bridge claim requires a later untouched replication.
