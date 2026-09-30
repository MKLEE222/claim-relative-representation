# Evidence and reproducibility

Companion to *After Revision: Corrections, Replies, and Scholarly Continuation in Digital Editions*. This page identifies the sources, analytic population, and reproducible checks behind the article. It distinguishes documentary interpretation from tests of the consequences of that interpretation.

## Historical witnesses and source anchors

The close readings use Henry Yule and Henri Cordier, *The Book of Ser Marco Polo*, third edition, volume I (1903), and Henri Cordier, *Ser Marco Polo: Notes and Addenda* (1920). References in the article use **printed page numbers**. The scan-page numbers below identify pages in the fixed local PDF copies used for the final quotation check; they are not interchangeable with printed pagination or zero-based PDF indexes.

| Reading in the article | Printed page | Scan page in checked copy | Evidentiary role |
| --- | --- | --- | --- |
| Polo's mulberry-bark description | Yule and Cordier 1903, I:423 | 723 | Earlier material identification |
| Bretschneider's criticism, transmitted in an editorial note | Yule and Cordier 1903, I:430 | 732 | Prior criticism addressed by Laufer |
| Earlier citation of Houtum-Schindler's 1898 paper | Yule and Cordier 1903, I:113 | 405 | Basis of Cordier's later bibliographical reply; this page concerns a different geographical question |
| Arbre Sec and the Oriental Plane discussion | Yule and Cordier 1903, I:128 | 420 | Earlier identification and objection context |
| Houtum-Schindler's cypress proposal and Cordier's reply | Cordier 1920, 31 | 45 | Competing proposal and bibliographical response |
| Laufer's response, transmitted by Cordier | Cordier 1920, 70–72 | 84–86 | Correction of Bretschneider and endorsement of the mulberry account |

The page images confirm the short quoted cues used in the article: “He seems to be mistaken” (1903, I:430); “Laufer writes to me,” “a singular error of Bretschneider,” and “Marco Polo is perfectly correct” (1920, 70); and Cordier's statement that he had read Houtum-Schindler's paper (1920, 31). Laufer also concedes that Bretschneider is right about paper made from *Broussonetia* before rejecting his exclusion of mulberry paper. The article therefore treats Laufer's intervention as a targeted correction and endorsement, and treats Cordier as its transmitter. On the inspected Arbre Sec page, Cordier's reply does not establish his adoption of the cypress identification.

The digitized witnesses are linked in the article's bibliography. [Proposition-level source records](../../data/r3_verified_proposition_panel_v1.csv) and [historical claim events](../../data/yule_cordier_claim_events.csv) record the interpretive mapping used for the tests. The source readings are authorial interpretations. The computational checks below do not independently adjudicate them.

## Representational comparisons

The Paper Money comparison holds the declared current-assertion projection fixed while removing the recorded relation by which Bretschneider's criticism entered the represented history. The target statement remains present. The specified later correction is supported in the full view and unresolved in the reduced view under the declared evidence horizon. This is a **controlled comparison of representations**, not a claim that a historical digital edition actually lost this information.

Arbre Sec supplies a different action: Cordier's bibliographical reply can be recorded as addressing Houtum-Schindler's proposal without changing the represented identification. These contrasts and their action requirements are documented in the [natural-sequence result](../../audits/mother_problem_redesign_20260929/NATURAL_ACT_LEVEL_COMPOSITION_RESULT_v2.md) and the [action-relative qualification result](../../audits/mother_problem_redesign_20260929/CROSS_ECOLOGY_GENERATOR_QUALIFICATION_SIGNATURE_RESULT_v1.md).

The [finite equivalence and sequence checks](../../audits/mother_problem_redesign_20260929/ACTION_RELATIVE_STATE_EQUIVALENCE_SEQUENCE_CLOSURE_RESULT_v1.md) cover 120 specified action contexts, 393 required-condition probes, 19 nonrequired-history probes, 52 connected Formalization Papers sequences, and two Yule–Cordier sequences. These are conformance and contrast counts for registered contexts, not numbers of independent historical documents or prevalence estimates. The requirement that a correction be grounded in its earlier critical relation is an explicit interpretive choice of the stated inquiry.

## Formalization Papers source and population

The second documentary setting is the supplementary repository accompanying Bucur and colleagues' 2023 study, [*Nanopublication-Based Semantic Publishing and Reviewing*](https://doi.org/10.7717/peerj-cs.1159). The analysis fixed the [v1.0 source repository](https://github.com/LaraHack/formalization_papers_supplemental) at commit `2f68d8498aeeb724e3438deda13e74ae7fb076d8`. The first-opened archive had SHA-256 `c2349aa34350dc5f02f3ad7ccfc1ff6f879e88950fee948b0d5ffa206d4ca9e3`. The population comprises ten source record files, fifteen graph-derived roots, eight complete eligible roots, and seven roots retained with ambiguous or nonfunctional dispositions. The fixed grammar yields 52 connected eligible chains; chains can share roots and records.

The first prospective execution was invalidated by parser discrepancies. The [corrected reproduction](../../audits/mother_problem_redesign_20260929/FORMALIZATION_PAPERS_CORRECTED_REPRODUCTION_RESULT_v2.md) addressed date-time lexical precision and multi-valued creator relations and reconstructed the fixed source population and eligible chains. It is reported as a **corrected reproduction**, not a fresh prospective confirmation. The later [information-view comparison](../../audits/mother_problem_redesign_20260929/FORMALIZATION_PAPERS_ACTION_AVAILABILITY_COMPARATOR_RESULT_v1.md) is a post-exposure mechanism diagnostic. Its distinct test populations are 52 valid response contexts, 47 naturally occurring non-live-target acts, 52 controlled history-ablated contexts, and one nonfunctional-target control. The denominators must remain separate.

## Reproducing the reported checks and figures

The repository retains the executable [corrected-reproduction workflow](../../.github/workflows/formalization_papers_corrected_reproduction_v1.yml), [action-availability comparison workflow](../../.github/workflows/formalization_papers_action_availability_comparator_v1.yml), and [equivalence/sequence workflow](../../.github/workflows/action_relative_equivalence_sequence_closure_v1.yml), alongside the linked result reports and frozen inputs. The article's two current figures are generated from the [R sources](figures/); the [manuscript build instructions](TEX_BUILD_README.md) describe how to regenerate their PDF versions and typeset the article. These links are intended for verification of exact inputs, rules, outputs, and denominators rather than as an invitation to treat repeated tests as new independent observations.

No TEI, PROV, CRMinf, or CiTO implementation is evaluated as a competing baseline. The article asks which relations and source access a representation must make recoverable for specified inquiries; those standards can carry some or all of the needed information in suitable implementations. A separate [technical provenance ledger](SOURCE_NOTES_AND_SUBMISSION_GAPS.md) retains workflow identifiers, checksums, correction history, and nonconfirmatory analyses.

## Reuse and disclosure boundaries

This repository links to the Formalization Papers source instead of redistributing its raw records in the submission package. On inspection of its fixed commit, the repository root contains no license file and GitHub exposes no repository license metadata. Permission or applicable reuse terms for republication of those source records or screenshots therefore remain to be confirmed before any such redistribution. Quoted historical passages are short and individually cited; any reproduced facsimile images require a separate rights check.

The article's historical readings have not received stable independent human adjudication. A blinded model-based corroboration attempt was nonconfirmatory and is retained in the technical record; it is not presented as validation of the readings.

