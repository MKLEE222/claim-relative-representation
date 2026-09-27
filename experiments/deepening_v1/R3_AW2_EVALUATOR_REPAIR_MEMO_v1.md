# R3-AW2 evaluator repair memo v1

Date: 2026-09-27
Status: IMPLEMENTATION REPAIR AFTER INVALID TARGET CHECK

The first AW2 run generated the native candidate sets correctly:

- page 201 -> exactly one unit:
  `P. 201, Line 12. Read the Governor of Urumtsi _founded_ instead of _found_.`
- page 200 -> zero units;
- page 202 -> one different `pp. 202` unit.

However, the evaluation regex used word boundaries directly on Gutenberg emphasis markup. Because underscore is a regex word character, `_founded_` and `_found_` failed the target detector.

This is an evaluator implementation error, not a scientific null.

Repair:
- candidate generation is unchanged;
- page identifiers 201 / 200 / 202 are unchanged;
- pointer extraction is unchanged;
- before target evaluation only, Gutenberg underscore emphasis markers are stripped;
- the same founded/found target predicate is then applied.

No additional candidate is admitted and no workflow parameter changes.
