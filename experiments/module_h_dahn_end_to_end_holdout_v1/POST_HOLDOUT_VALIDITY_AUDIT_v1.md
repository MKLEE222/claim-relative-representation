# Module H Paul holdout post-execution validity audit v1

Date: 2026-09-28
Status: SCIENTIFIC INVALIDATION OF THE PRIMARY HOLDOUT CLAIM. RAW EXECUTION IS PRESERVED.

## 1. Frozen execution

Prospective Paul holdout run:
36394087908

Artifact:
module-h-dahn-prospective-holdout-v1

Artifact ID:
10957178522

Artifact ZIP SHA-256:
9935273725e8db8a074990f640686f68a610a0d4f513240d7a49fd051c3c3d84

Frozen evaluator Git blob:
3cfb747de03df433692415457f22293e0adefc49

Raw execution:
- 1,515 parsed documents
- 0 parse errors
- 79 primary discovery episodes
- 77 full trajectories
- I_RSTAR 77/77 end-to-end
- I_NATIVE 77/77 end-to-end
- all pre-registered Boolean gates returned true

These computational outputs remain unchanged.

## 2. Post-holdout validity failure

After the holdout outcome was produced, a source-level audit inspected the first reported episode:

Correspondence/Paul_d_Estournelles_de_Constant/Corpus/Lettre0001_15aout1914.xml

The document contains:
- the primary letter;
- multiple embedded div type="annex" copies of other letters/documents;
- each annex may have its own opener/dateline/date.

The frozen evaluator extracted C_DATELINE using a whole-document XPath over every opener/dateline date.

This includes dates belonging to annex documents.

In Lettre0001, the raw holdout episode therefore treated dates such as:
- 1914-08-06
- 1914-08-17
- 1914-08-13

from embedded annex letters as current-document temporal carriers for the main 1914-08-15 letter.

That violates the scientific contract in PROTOCOL.md:

    C_DATELINE = current-document manuscript/body date

and can manufacture H-D1 temporal conflicts that are not conflicts among carriers of the same current document.

## 3. Scientific disposition

The raw 77/77 result CANNOT be used as evidence that Module H passed the mother-problem adequacy gate.

Disposition:

    PAUL_HOLDOUT_COMPUTATIONAL_EXECUTION = COMPLETE

    PAUL_HOLDOUT_CURRENT_DOCUMENT_CARRIER_VALIDITY = FAILED

    MODULE_H_MOTHER_PROBLEM_GATE = NOT ESTABLISHED

    RSTAR_77_OF_77 = INSTRUMENT_INVALID FOR CONFIRMATORY CLAIM

This is not a negative result about R*.
It is a validity failure in episode construction.

## 4. No rescue on Paul

The protocol stop rule prohibits:
- changing the holdout parser after seeing Paul outcomes;
- dropping invalid-looking Paul episodes post hoc;
- redefining the denominator and rerunning the same holdout as confirmatory evidence.

Therefore the following are NOT authorized as Module H v1 confirmation:
- excluding annex dates and rerunning Paul;
- keeping only Paul letters without annexes;
- reporting a favorable post hoc subset.

Paul may now be used only as development material for a future independently frozen study.

## 5. Required repair for future holdout

A future generic current-document date extractor must define a document boundary before any new holdout body inspection.

At minimum it must:
- identify the primary letter/document container according to DAHN's generic TEI structure;
- include dateline dates only from that current-document container;
- exclude div type="annex" and other embedded document containers;
- independently verify the boundary with a second parser;
- preserve annex dates as related/contextual evidence only if a later protocol explicitly licenses them.

The corrected rule must be developed on already-exposed Berlin/Paul material.

## 6. Consequence for the research program

A-G remain unchanged.

The prior claim-level audit remains correct:

    full mother problem not yet empirically closed.

The failed Paul holdout is valuable because it reveals that:

    source-document identity itself is part of the representation/admissibility contract.

Before asking whether temporal claims conflict, a system must know which embedded document each claim belongs to.

This observation may become part of the theory only after a clean independent test; it is not promoted from this invalid holdout alone.

## 7. Next action

Use exposed Berlin/Paul data to freeze a generic document-boundary extractor.

Then select a still-unopened DAHN correspondence collection as a new prospective holdout.

Do not reuse Paul for confirmatory closure.