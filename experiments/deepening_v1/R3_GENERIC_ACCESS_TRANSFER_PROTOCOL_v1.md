# R3 Frozen Generic-Access Transfer Protocol v1

Date frozen: 2026-09-27
Status: PRE-OUTCOME NATURAL/WORKFLOW REPLAY

## Purpose

Carry the five frozen R3 historical inquiries from a realistic 1903 starting locus through the previously frozen Generic Seed-Task Access Policy v1.

This is not a new retrieval policy. The retrieval parameters and ranking rule are inherited unchanged from the 2026-09-24 generic policy:

- 180-word windows;
- 90-word stride;
- top K = 12 query terms;
- TF x IDF query weighting;
- weighted lexical overlap ranking;
- full-object and native later-layer scopes;
- no target-derived query terms;
- no post-outcome retuning.

The new work only freezes R3 case inputs and evaluation anchors before outcomes are opened.

## Native collection

The declared collection is the two-volume Project Gutenberg Yule-Cordier edition:

- Volume I, pg10636.txt;
- Volume II, pg12410.txt, which contains the second 1903 volume and the 1920 Notes and Addenda.

The 1920 Notes and Addenda heading in Volume II defines the native later-layer boundary.

For IDF, the base corpus is:
- all of Volume I;
- the pre-Addenda portion of Volume II.

The full-object scope is both complete volumes. The later-layer scope is only the native 1920 Addenda portion of Volume II.

## Entry-state rule

Each R3 case starts from a source-grounded 1903 seed paragraph. The seed is extracted around a frozen phrase that belongs to the earlier locus. The seed paragraph is input; later target text is not.

The access task wording is answer-neutral and asks for later treatment of the earlier issue. It does not name the later scholar or the hidden answer unless that name already occurs in the seed.

## Frozen cases

### Pashai

Seed anchor:
"speaking here from hearsay"

Access task:
"Find later editorial treatment bearing on the source attribution and route reconstruction in the earlier Pashai note."

Evaluation-only carrier groups:
- corroboration carrier: "Sir Henry Yule was undoubtedly right in assuming that Marco Polo had never personally visited"
- route-challenge carrier: "may very well have made his way over the Hindu"

### Arbre Sec

Seed anchor:
"There can be no doubt that the tree described is"

Access task:
"Find later editorial treatment bearing on the identification and editorial uptake of the Arbre Sec in the earlier note."

Evaluation-only carrier groups:
- competing identification: "Cypress of Zoroaster"
- editorial reply: "If General Houtum Schindler had seen the third edition"

### Great Desert

Seed anchor:
"It is at the entrance of the great Desert"

Access task:
"Find later editorial treatment bearing on the Great Desert folklore/source interpretation and the distance or marches described in the earlier note."

Evaluation-only carrier groups:
- folklore/source carrier: "faithful reflex of old folklore beliefs he must have heard on the spot"
- measurement carrier: "plane-table survey checked by cyclometer readings"

### Urumtsi

Seed anchor:
"The Chinese Governor of Urumtsi found some years ago"

Access task:
"Find later editorial correction bearing on the Governor of Urumtsi passage in the earlier note."

Evaluation-only carrier group:
- correction: "Governor of Urumtsi founded instead of found"

### Tun-o-Kain

Seed anchor:
"No city in particular is indicated as visited by the traveller"

Access task:
"Find later editorial treatment bearing on the route through Tun-o-Kain in the earlier note and determine whether later discussion settles or preserves competing positions."

Evaluation-only carrier groups:
- Sykes revision: "Major Sykes had adopted Sir Henry Yule's theory"
- support for Yule: "Support to Yule's theory has been brought by Sven Hedin"
- unresolved competition: "cannot decide with full certainty whether Marco Polo travelled"

## Evaluation

Target anchors are used only after ranking.

For each case and each scope report:
- candidate count;
- query terms;
- minimum rank for every evaluation-only carrier group;
- reciprocal rank for every group;
- Hit@10/20/50 for every group;
- whether one 180-word window exposes all registered carrier groups;
- whether the top 10/20/50 windows collectively expose all registered carrier groups.

Interpretation is capability-separated:

1. DISCOVERABILITY:
   whether the registered carrier groups are surfaced within the inspection budget.

2. CARRIER EXPOSURE:
   whether one returned chunk or a bounded composition of returned chunks contains all registered textual carriers.

Neither metric alone proves proposition-level semantic correctness or information-theoretic loss.

## Leakage rule

After query construction, no query term may overlap a case's evaluation-only terms that are absent from its 1903 seed. If such overlap occurs from task wording or implementation error, the case stops as INVALID_LEAKAGE.

## Falsification and null rule

No query tuning, stopword change, window-size change, stride change, target-specific source name, or carrier-specific synonym may be added after outcomes are opened.

If all five cases remain discoverable and carrier-complete, retain the null: this workflow does not instantiate the controlled proposition-binding failure.

If discoverability fails while the later carrier remains globally present, classify it as access/retrieval failure, not binding deletion.

If chunking prevents complete carrier exposure while the underlying Addenda retains the carriers, classify it as workflow-level exposure/profile change, not source-level deletion.


## Implementation note

The first CI attempt stopped before opening any outcome because the longer Tun-o-Kain seed anchor crossed Gutenberg emphasis markup around the place name. The seed anchor was shortened to the same source locus (`reached the Province of TUN-O-KAIN`) without changing the seed passage, task, workflow parameters, evaluation anchors, or success rules.

Implementation note 2: the shorter place-name anchor was still interrupted by Gutenberg emphasis markup. It was replaced with a format-stable sentence from the same 1903 Tun-o-Kain paragraph. No scientific input, task, parameter, evaluation anchor, or success rule changed.
