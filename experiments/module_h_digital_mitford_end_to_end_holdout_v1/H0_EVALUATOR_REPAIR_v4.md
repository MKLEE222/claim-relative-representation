# Module H0 evaluator repair note v4

Date: 2026-09-28
Status: PRE-OUTCOME IMPLEMENTATION REPAIR AND BLINDING HARDENING.

Fourth failed run:
36384940450

The run terminated before H0 population extraction produced scientific output.

Failure:
the Site Index is well-formed, but iteration includes XML comment/processing nodes whose tag is not a string. The helper lname() passed those nodes to lxml QName and raised a ValueError.

Repair:
- lname() returns an empty local-name for non-string tags;
- ordinary XML element handling is unchanged.

Blinding hardening before the first successful H0 outcome:
- the three surfaces documented in H0_ACCIDENTAL_GOLD_EXPOSURE_v1.md are tagged POST_FREEZE_ACCIDENTAL_EXPOSURE;
- they remain in complete population accounting and all-population sensitivity output;
- they are excluded only from CLEAN CONFIRMATORY headline denominators;
- stdout is aggregate-only; item-level episode identities remain inside the uploaded population artifact and are not printed during H0.

No checkpoint, source blob, original pre-freeze exposure set, gold parsing rule, source matching rule, person criterion, uncertainty lexicon, discovery operator, metric definition, or scientific success criterion changes.
