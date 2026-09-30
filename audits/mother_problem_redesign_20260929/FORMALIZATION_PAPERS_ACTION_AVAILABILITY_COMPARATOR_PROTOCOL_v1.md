# Formalization Papers action-availability comparator audit v1

Date: 2026-09-30
Status: POST-FRESH / EXPOSED MECHANISM AUDIT.

## 1. Goal

Decompose false scholarly-action availability across progressively stronger representations.

The corrected Formalization Papers population already establishes:
- 52 valid connected composition chains;
- natural T8 roots with non-live/nonfunctional response targets;
- 52 registered history-ablation rejections.

This audit asks which representational distinction blocks which false positive.

It does not create a new fresh claim.

## 2. Compared interfaces

### B_RELATION_TARGET

A response is available iff:
- it has exactly one project-native isResponseTo review target;
- it has exactly one project-native refersTo update target.

This comparator knows relation type and exact target identity.

It does NOT require:
- review/update target to be currently live;
- update to be current;
- retained transition history.

### B_LIVE_TARGET

A response is available iff:
- the exact review target is currently live;
- the exact update target is the current update.

It knows:
- relation type;
- exact target identity;
- live/current target state.

It does NOT inspect retained transition history.

### Q_FULL_HISTORY

The frozen qualified engine.

A response additionally requires retained history establishing:
- the targeted review entered the scholarly state;
- the targeted update entered the scholarly state.

The generator is:

    RECORD_RESPONSE

only when all target/history conditions close.

## 3. Denominators

### D_POSITIVE

All unique connected response contexts from T0/T1 eligible chains.

Decision extensions are deduplicated by:

    (root, review_np, update_np, response_np)

The full-history state must qualify the response under Q_FULL_HISTORY.

### D_NONLIVE

All unique response acts represented in frozen T8 ambiguities as:

    RESPONSE_UPDATE_TARGET_NOT_LIVE

These ambiguities arise only after the parser/classifier has already established:
- one functional review target;
- one functional update target;
- live review target;
- non-live update target.

Thus B_RELATION_TARGET considers the response available while B_LIVE_TARGET should not.

### D_NONFUNCTIONAL

All unique response acts represented as:

    RESPONSE_NONFUNCTIONAL_TARGET

B_RELATION_TARGET must reject these because functional target cardinality is not satisfied.

### D_HISTORY_ABLATED

For every D_POSITIVE context:
- execute its registered review and update;
- retain the exact same current formalization/update and live review target;
- erase only retained transition history.

Require:

    current formalization/update projection identical

B_RELATION_TARGET and B_LIVE_TARGET do not inspect history.

Q_FULL_HISTORY must reject with:

    RESPONSE_TARGET_HISTORY_UNRESOLVED

## 4. Metrics

For D_POSITIVE report availability by all three interfaces.

For D_NONLIVE report false action availability:
- B_RELATION_TARGET false positive count;
- B_LIVE_TARGET false positive count;
- Q_FULL_HISTORY false positive count.

For D_HISTORY_ABLATED report false action availability:
- B_RELATION_TARGET;
- B_LIVE_TARGET;
- Q_FULL_HISTORY.

For D_NONFUNCTIONAL report rejection count.

## 5. Required interpretation

The audit supports a separation only if:

### Positive preservation

All D_POSITIVE responses remain available under all three interfaces.

### Live-target separation

On D_NONLIVE:

    B_RELATION_TARGET available
    B_LIVE_TARGET unavailable
    Q_FULL_HISTORY unavailable

This identifies the incremental role of live-version/target state.

### History separation

On D_HISTORY_ABLATED:

    B_RELATION_TARGET available
    B_LIVE_TARGET available
    Q_FULL_HISTORY unavailable

while the current formalization/update projection is unchanged.

This identifies the incremental role of retained transition history beyond current live targets.

### Nonfunctional discipline

D_NONFUNCTIONAL must not be counted as an executable action by the functional-target comparator.

## 6. False-positive language

A false positive here means:

> a comparator declares a later scholarly response action available in a state that the
> prospectively frozen target/version/history qualification contract rejects.

Natural D_NONLIVE negatives are inherited from the pre-data T8 grammar.

D_HISTORY_ABLATED negatives are inherited from the pre-data P4 counterfactual.

Thus the negative labels are not created by the comparator output.

## 7. Claim ceiling

This is an exposed comparator/mechanism audit.

It may establish:

    relation target identity
    !=
    live target validity
    !=
    retained-history qualification

for the frozen Formalization Papers ecology.

It does not establish:
- universal necessity for every scholarly action family;
- prevalence outside this population;
- a literal prospective comparator confirmation;
- that all history fields are minimally necessary.
