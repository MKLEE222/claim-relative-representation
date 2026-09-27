# R3 frame scope and responsibility: round 2

Date: 2026-09-27. Base: a78bbe1568f2b8fc1253df0433b55f140099b9fe.
Authority: retrospective AI-assisted historical inspection and offline structural audit. No new retrieval, LLM judge, independent human coding, or prevalence estimate.

Delivery: R3_Frame_And_Responsibility_Audit_2026-09-27.zip, 8,836,094 bytes; SHA-256 24ca6e2f7023dff59bd61887914fffa877ecaf1c8c170a006ecbe405c17d90c7. The conversation attachment contains both frozen text objects, the original 223-entry intervals, code, exact spans, section crosswalk, page images and the extracted-page PDF. No original experimental object was overwritten.

## Executed checks

All 223 original entry intervals reproduce their stored normalized-text SHA-256 against the original CRLF-preserving source. The broader scan emits 276 heading candidates with dispositions and 18 contiguous audit sections. These are inspection partitions, not 18 equivalent intellectual units.

The source study records 15 exact spans, seven bounded analytical records and ten visually inspected page images. All ten PDF-extract renders are pixel-identical to the reviewed images. This validates integrity, not the correctness of the historical interpretation.

## New heading boundaries

Beyond the eight Introduction headings identified in the previous round, three genuine headings occur inside old entries without being represented as boundaries:

| Heading | Source character start in pg12410 | Old containing entry | 1920 printed page |
|---|---:|---|---:|
| XXXIX., P. 197. | 2121660 | YC1920E-0048 | 47 |
| P. 201, Line 12. Read ... founded instead of found. | 2128622 | YC1920E-0051 | 50 |
| Indented XIV., p.313 Ceylon passage | 2251771 | YC1920E-0181 | 110 |

Their layouts were visually verified at original PDF indices 60, 63 and 123. Case-sensitive p./pp. matching, a required chapter prefix and indentation respectively explain these misses.

The eleven additional top-level heading candidates do not license replacing 223 by 234 as a complete population. Unheaded acts, quotation extents, shared notes and other structural classes remain review obligations.

## Cross-section contamination

The earlier stop expressions did not match indented section headings. Exact interval intersections show:

- YC1920E-0222 includes 16,067 source characters assigned to the following bibliography section.
- YC1920E-0223 includes 46,256 source characters assigned to the printed index, transcriber's notes and post-END Gutenberg wrapper.

The last candidate thus joins a signed scholarly supplement to printed and modern electronic paratext. The preceding one absorbs a bibliography rather than only its manuscript-catalogue note. Bibliography is historically relevant but a different source unit, not material that should silently become part of the preceding entry. The audit separately enumerates 46 numbered bibliographical groups, not 46 independent works.

Old ranks remain recorded on their exact frozen bytes. Reproducibility does not certify a clean or uniform historical-entry population. Claims on a corrected scope require a separately versioned frame and evaluation. No effect of cleaning on rankings was measured here.

## A small erratum with a proposition-level consequence

1903 I p.201 says the governor of Urumtsi 'found' a town; the note ends H.C. Cordier 1920 p.50 directs the reader to substitute 'founded'. Both printed loci were checked, at 1903 original PDF index 500 and 1920 index 63; both corresponding digital spans match.

The correction changes the action described from finding to founding. This establishes an editorial amendment and its target, not the historical truth or date of the founding. Merging the erratum into the preceding desert-sounds commentary obscures a distinct intervention.

## Ceylon and voice boundaries

At 1920 p.110, the transmitted Laufer discussion of dog-headed peoples is followed by a separate indented Ceylon heading, a quoted royal-jewel description and a comparison from Chau Ju-kwa. The source supports juxtaposition, not an explicit endorsement of every detail or identification of the jewels as the same object. A single actor label on the merged interval risks transferring Laufer's responsibility across a real entry boundary. No downstream coder error was measured.

## Temple: nested contribution, responsibility and target-relative relations

The Supplementary Note occupies printed pp.144-150. Cordier introduces material sent by Richard C. Temple; Temple invokes his administrative role in 1894-1903 and his Census Report, recommends recasting several 1903 notes, and signs on 29 November 1919. These are claimed grounds of authority and a proposal, not independent validation of the cited works or evidence that a later edition implemented the proposal.

There are ten explicit page-addressed subnotes within this contribution. They are nested units, not ten independent contributors or top-level equivalents. Unheaded subdivisions and the general note contain further acts, so ten is not a complete intervention count.

At p.145 Temple rejects 'no king or chief' and invokes village chiefs with a Census Report citation. At p.149 a categorical denial of the cannibalism charge is followed by a differently modal explanation of its origin. His navigation note affirms a coastal-travel proposition while doubting a distinct journey claim. These propositions must retain separate evidence and modality.

The earlier digital witness contains the cannibalism allegation in the narrative, while its commentary already says the traditional charge is generally rejected. Temple's denial therefore opposes one earlier layer while aligning on the denial with another. A single direction-of-change label for the whole earlier edition is inadequate. The earlier Volume II print locus was not inspected this round: this is LATER_PRINT/EARLIER_DIGITAL, not PAGE_VERIFIED_BOTH. No first historical rejection or ethnographic truth is established.

The source's corrective rhetoric also coexists with colonial-administrative claims to expertise. This is an interpretation of the inspected contribution, not an independent history of that administration. Recording a correction must not automatically endorse the authority that advances it.

## Disposition

No new whole-book denominator is authorized. The 244 provisional spans mix top-level candidates and nested subnotes and must not become a pooled sample size. No old labels, sources, seed selections, negative LLM outputs or ranks were changed.

The next historical inventory must distinguish publication sections, contributions, page-addressed subnotes, embedded quotations and proposition-level targets. Only after those boundaries are audited should a corrected retrieval population be frozen. An extraction error in our reference construction cannot serve as evidence of inherent loss in the source representation.

## Reproduction

From the delivery directory:

    python build_frame_audit.py .
    python verify_evidence.py .

The first requires only the standard library. The verifier optionally uses PyMuPDF and Pillow for pixel comparison; it does not adjudicate historical labels.

Source hashes:
- pg10636.txt: 7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5
- pg12410.txt: c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c
- 1920 PDF: dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941
- 1903 I PDF copy: 6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7

The 1903 page was read from the previous selected-page artifact with the original index retained. The Census Report and the 1871/1875 editions were not newly inspected.
