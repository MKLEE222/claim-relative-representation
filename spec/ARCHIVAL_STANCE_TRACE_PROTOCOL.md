# Archival Scholarly Trace Protocol v1

Date frozen: 2026-09-25
Status: PRE-LLM, SOURCE-FACING

## Purpose

Before any LLM adjudication, extract historically observed scholarly stance traces that are explicit in the source record.

These traces are not treated as gold epistemic labels.

They answer:

> What evaluative acts did historical editors/scholars explicitly perform in the surviving documentary record?

This layer sits between documentary recovery and final computational adjudication:

\[
G_D
\rightarrow
A_{trace}
\rightarrow
\text{final LLM judge (later)}
\]

## Why this layer exists

A model should not be the first component to decide that one passage criticizes, endorses, corrects, or qualifies another when the historical source explicitly says so.

The source record can first supply observable evaluative speech-act traces.

## Trace requirements

Every trace must contain:

- source event;
- historical actor;
- target actor/proposition if explicit;
- trace type;
- verbatim cue;
- page/witness anchor;
- verification status.

## Non-equivalence rule

The following are explicitly prohibited:

- ST_CRITICISM == E_UNDERCUT
- ST_ENDORSEMENT == E_SUPPORT
- ST_PRIOR_CRITIC_CORRECTION == E_REHABILITATE
- ST_SCOPE_SHIFT == E_ACCRETION

The left-hand side records a historical actor's explicit stance.

The right-hand side is this study's later claim-relative adjudication.

The final LLM judge may consider archival traces together with the underlying passages, but it must still independently apply the frozen adjudication contract.

## Verification

Confirmatory use requires PAGE_VERIFIED source wording.

Digital-only traces may be exploratory but cannot anchor the paper-money confirmatory closure.

## Active-trace exposure

For a fixed evidence budget, a retrieval/navigation condition exposes a trace only when the source event carrying that trace enters the active evidence packet.

Thus we can deterministically compare:

\[
A_{trace}(E_{active}^{(1)})
\quad\text{vs}\quad
A_{trace}(E_{active}^{(2)})
\]

without yet assigning a warrant state.

## Claim ceiling

This layer can establish:
- which historically explicit evaluative acts are exposed under each active evidence state;
- whether a navigation condition suppresses or exposes later scholarly correction traces.

It cannot establish:
- our own epistemic entitlement state;
- what a human scholar would decide;
- what the later LLM judge must decide.
