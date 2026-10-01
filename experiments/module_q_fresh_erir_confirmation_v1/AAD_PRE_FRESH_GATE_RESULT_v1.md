# Module Q — AAD pre-fresh synthetic gate result v1

Date: 2026-09-29
Status: PASS / AAD EPISODE XML STILL UNOPENED AT THIS RESULT.

## 1. Frozen protocol

Protocol:

    experiments/module_q_fresh_erir_confirmation_v1/AAD_PRE_FRESH_PROTOCOL_v1.md

Protocol commit:

    0a90d12ab5d72f12d819ea37cf11524ccede5a03

## 2. Workflow

Workflow:

    module-q-aad-pre-fresh-v1

Authoritative successful run:

    36525975857

Head:

    fdd9464acbf2c3315c803e374015065659adace4

The preceding failed run 36525932543 stopped at import because the new workflow omitted the
existing lxml runtime dependency. No AAD-shaped fixture or AAD episode XML was opened in that
failed run. The workflow dependency was then added without changing any scientific contract or
test expectation.

## 3. Frozen Module P regression

Before running the AAD-shaped fixture, the workflow reran:

    experiments/module_p_evidence_release_revision_v1/test_revision_contract_v1.py

Result:

    PASS

Thus the AAD-shaped gate did not execute on a known-broken Module-P baseline.

## 4. Positive synthetic fixture

The fixture contains no real AAD episode content.

It instantiates only the project-level shape already established from the ODD/generic generator:

    transcription
      -> letter
        -> letter_message

plus:
- correspAction type=sent;
- history/origin/origDate;
- a non-letter envelope sibling carrying an unrelated machine date.

Observed object contract:

    SINGLE_PRIMARY_DOCUMENT_OBJECT
    boundary = EXPLICIT_LETTER_DIV

Observed evidence contract:

    SINGLE_ORIGIN_ADMISSIBLE
    origin count = 1

Observed pre-event state:

    EXACT 1900-01-01

Observed post-event state:

    ALTERNATIVE_SET
      sent     1900-01-01
      origDate 1900-01-02

Transition class:

    P-U1_CONFLICT_FORMATION

P1-P7:

    all PASS

Reference end-to-end:

    PASS

## 5. Object-boundary control

The machine date inside the synthetic envelope sibling was detected as excluded and did not enter
the active root warrant.

Active root roles:

    sent

Thus the pre-fresh fixture specifically tests the AAD-like coexistence of letter and
envelope/enclosure structures without silently widening the scholarly object.

## 6. Natural-null discipline

Paired synthetic null:

    sent     1900-01-01
    origDate 1900-01-01

Observed:

    ADMISSIBLE_NULL_EVENT

It was not promoted to substantive ERIR.

## 7. Consequence

The frozen Module-L / Module-P engine can consume the AAD-shaped serialization without a
project-specific outcome adapter.

Therefore the pre-fresh gate authorizes the one-shot opening of the frozen AAD population:

    auden-in-austria-digital/aad-data
    34c3958686ab03614dedd8d979ffe94b6c0f2a28
    data/xml/editions/
    148 direct XML files

The fresh run must preserve NULL / BOUNDED_PARTIAL / PASS / INVALID exactly as declared.

## 8. Claim ceiling

This gate is synthetic portability evidence only.

It does not predict that AAD contains any ERIR-eligible natural episode.

At the time represented by this result, no:

    data/xml/editions/*.xml

episode had been opened.
