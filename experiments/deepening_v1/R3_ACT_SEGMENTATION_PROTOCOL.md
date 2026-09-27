# R3 act-segmentation protocol v1

Date frozen: 2026-09-27
Status: active; introduced before full 1920 intervention coding.

## Why entry-level labels are insufficient

One Cordier Addenda entry can contain several distinct scholarly acts by different actors.

Examples already visible in the source:
- the Kinsay p. 193 entry transmits Moule's atlas re-identification and, separately, Tanner's argument about whether Polo visited Hang-chou;
- the Sarai entry transmits distinct objections from Friedmann and Pelliot;
- the paper-money entry transmits Laufer's correction of Bretschneider and his positive rehabilitation of Polo.

Therefore the study uses two nested units:

1. EDITORIAL_ENTRY
   The Addenda unit headed by a backward pointer to the earlier edition.

2. INTERVENTION_ACT
   A source-attributed proposition within an entry that bears a specific relation to an earlier proposition, identification, attribution, source claim, or another intervention act.

Entry remains the denominator for "how many Addenda entries contain X".
Act is the unit for "how many distinct scholarly interventions of type X occur".

Act counts are clustered within entries and are never treated as independent samples.

## Act schema

Each act records:

- entry_id;
- act_id;
- mediator_actor: the 1920 editorial voice that transmits/frames the act, normally Cordier;
- proposition_actor: the scholar/source responsible for the proposition where explicit;
- target_layer;
- target_locus;
- target_actor/proposition;
- relation_labels;
- evidence_span;
- source_authority;
- verification_status;
- humanistic_object;
- confidence_note.

## Voice separation

Do not collapse:
- Cordier quotes Laufer;
- Laufer argues X;
- X bears relation R to Bretschneider.

These are distinct edges:

Cordier --TRANSMITS--> Laufer proposition
Laufer proposition --CORRECTS/CRITICIZES--> Bretschneider proposition

Likewise, "I cannot very well accept this theory" is Cordier's own evaluative act, not Pelliot's.

## Entry-level aggregation

An entry-level relation label is present if at least one verified act in that entry carries the label.

Multi-act entries may therefore have several labels without pretending that one proposition performed all of them.

## Humanistic importance

This distinction is necessary for:
- editorial responsibility;
- controversy trajectories;
- distinguishing editor voice from cited authority;
- reconstructing how knowledge enters an edition.

A representation that preserves the quoted words but loses who is speaking or what earlier proposition is targeted may preserve topic while destroying responsibility history.
