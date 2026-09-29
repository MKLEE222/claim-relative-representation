# VGW runtime N-Triples LANGTAG terminator correction v1

Date: 2026-09-29
Status: POST-FRESH IMPLEMENTATION CORRECTION / SCIENTIFIC CONTRACT UNCHANGED.

## Trigger

After the authoritative VGW fresh attempt became INVALID because of a runtime lexer failure, the
first blank-node terminator bug was corrected post-exposure.

A full post-fresh grammar coverage audit was then run against the exact five distribution SHA-256
values from the first DATA_OPEN event.

Audit result:

    total lexical failures = 2490

Per distribution:

    de_la_faille_1970      0
    works_after_1970       0
    van_gogh_museum     1888
    krollermuller_museum   0
    rkd_collections       602

All 2490 failures are one and only one lexical class:

    language-tagged literal immediately followed by statement terminator dot

Examples:

    "Milano"@nl.
    "Vienna (city)"@en.

No second lexical failure class was observed.

## Frozen correction

When parsing a language-tag suffix after a literal:

1. consume the leading '@';
2. consume the language tag characters;
3. stop before either:
   - whitespace; or
   - the final N-Triples statement terminator dot;
4. leave the terminal dot for the statement parser.

The parser must not remove or reinterpret the language tag.

The correction changes no RDF node, predicate, literal lexical value or scientific relation.

## Scientific invariants

This correction does NOT change:
- frozen VGW URI constants;
- RDF relation reconstruction;
- F-number extraction;
- baseline/current join;
- source/version binding;
- Production cardinality;
- current Van Gogh attribution classification;
- E13 previous_attribution recognition;
- stable event addressability;
- eligibility;
- natural-null semantics;
- Module-R transition semantics;
- R1-R8;
- comparator budgets;
- any outcome category.

## Required regression and closure

Before a further corrected reproduction:

1. original Module-R synthetic controls must remain PASS;
2. VGW-shaped synthetic controls must remain PASS;
3. blank-node terminal-dot regression must remain PASS;
4. dedicated LANGTAG regressions must pass for:
   - no-space terminal dot;
   - ordinary whitespace before terminal dot;
   - multiple representative language tags;
5. full grammar coverage audit over the exact five first-opening SHA-256 distributions must return:

       total_failures = 0

Only after all five conditions pass may another corrected reproduction be run.

The authoritative fresh disposition remains:

    INVALID

and cannot be changed by this correction.
