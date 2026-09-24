# EP_CL_01 - Coal local-attachment boundary experiment

Date frozen: 2026-09-24
Status: PRE-OUTCOME BOUNDARY TEST

## Scientific role

Coal is a boundary carrier.

Unlike paper money and Kinsay, the relevant editorial material is attached locally to the base observation in the same 1903 chapter.

The experiment asks whether the framework correctly stops using broad cross-layer retrieval when a simpler native documentary route exists.

## Task

Starting from Polo's coal/fuel passage in Chapter XXX:

> Find the editorial material attached to this passage that bears on how the coal observation is contextualized by the editor.

The task does not name Richthofen, industrial power, or the expected relation class.

## Native source

Project Gutenberg Volume I, eBook #10636.

Frozen source anchor:
- chapter heading: "CONCERNING THE BLACK STONES THAT ARE DUG IN CATHAY"
- seed tail: "those stones burn better and cost less.{1}"

Evaluation-only target anchors:
- "Baron Richthofen"
- "world's wealth and power" / typographic equivalent

## Support gate

Primary primitive:
M_LOCAL_ATTACHMENT

The primitive is support-feasible only if:

1. the seed paragraph contains an explicit numbered note marker;
2. a matching NOTE 1 unit occurs before the next chapter boundary.

If either condition fails:
- status = MEDIATION_SUPPORT_UNAVAILABLE;
- no target-specific retrieval rescue is allowed.

## Conditions

### CL-SPAN

Seed passage only.

Purpose:
show that the attached note is not inside a focal-span-only horizon.

### CL-LOCAL-LINEAR

Whole native Chapter XXX, but no attachment following.

A frozen seed/task lexical retrieval policy ranks 180-word windows.

Purpose:
measure retrievability when the note is merely present in local scope.

### CL-ATTACHMENT

Follow the supported M_LOCAL_ATTACHMENT bridge from marker {1} to NOTE 1.

Purpose:
measure the documentary-navigation route supplied by the native representation.

## Outcomes

Report:
- support-feasibility status;
- local note marker;
- matching note label;
- target in scope for each condition;
- target rank under local linear retrieval;
- candidate count;
- attachment-follow candidate count;
- attachment target ordinal;
- target-only query leakage.

## Expected boundary interpretation

The preferred boundary witness is not "coal behaves like paper money."

It is:

- broad cross-layer mediation is unnecessary;
- a locally supported documentary attachment route is sufficient for the access task.

A null or blocked support result is retained.

## Claim ceiling

This experiment concerns access to the editorial note.

It does not yet adjudicate whether the note constitutes interpretive accretion or whether that accretion is warranted.
