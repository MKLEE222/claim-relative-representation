# MC_FV_C18 - Frankenstein minimal-carrier holdout

Date frozen: 2026-09-24
Status: SEALED BEFORE C18 OUTPUT OPENING

## External object

Frankenstein Variorum
Pinned commit:
5a208f869ff1213defa000e3181d5315a072a15f

Untouched output at freeze:
collationChunks/C18/output/Collation_C18-complete.xml

Blob:
bca0548912ab1d7b2676360d33a6468290296d7e

Only directory/file metadata were inspected before this freeze.

## Scholarly task

For each collation locus, recover the partition of participating witnesses into the reading-equivalence groups encoded by the external project's apparatus.

The task does not ask for source-page geography or literary interpretation.

## Candidate carriers

### WITNESS_ID
Native rdg @wit identity.

### RDGGRP_MEMBERSHIP
Native rdgGrp grouping structure.

### READING_TEXT
Text content carried by each rdg.

## Reference output

For each app:
the canonical partition of witness identifiers induced by the native rdgGrp structure.

If an app contains a direct rdg outside rdgGrp, that reading forms its own native group.

## Frozen decoders

### D_GROUP
Requires:
WITNESS_ID + RDGGRP_MEMBERSHIP

Output:
native witness groups directly.

### D_TEXT
Requires:
WITNESS_ID + READING_TEXT

Within each app, normalize reading text only by Unicode whitespace collapse and group witnesses whose normalized reading strings are identical.

No punctuation, spelling, markup, or case normalization is added after outcome.

## Hypotheses

H1:
D_GROUP is sufficient whenever the native task is instantiated.

H2:
D_TEXT may or may not reproduce the native rdgGrp partition.

If H2 succeeds across all C18 app units, the holdout exhibits two minimal carrier families:

\[
\{WITNESS\_ID,RDGGRP\_MEMBERSHIP\}
\]

and

\[
\{WITNESS\_ID,READING\_TEXT\}.
\]

If H2 fails on any app, only the group-based family is supported.

## Strict-subset checks

- WITNESS_ID alone fails if any app has more than one native reading group.
- RDGGRP_MEMBERSHIP alone cannot return witness identities.
- READING_TEXT alone cannot return witness identities.

No task weakening is allowed.

## Outcome retention

Both equivalence and mismatch are retained.

A text-decoder mismatch is scientifically informative: it would show that editorial grouping contains distinctions not reducible to exact reading-string equality.
