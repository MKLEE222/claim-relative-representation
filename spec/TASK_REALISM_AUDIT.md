# Task Realism Audit v1

Date frozen: 2026-09-24
Status: PRE-EXPERIMENT AUDIT

## Purpose

The project uses instrumented microtasks, not a claim that humanities research decomposes uniquely into a fixed pipeline.

A task is admissible only if it is both:

1. recognizable as a source-facing scholarly operation; and
2. precise enough to support controlled representation experiments.

## External grounding

The task family is anchored in established activity-centered accounts of humanities scholarship.

Unsworth's scholarly primitives include discovering, annotating, comparing, referring, sampling, illustrating, and representing. Palmer et al. refine this tradition into searching, collecting, reading, writing, collaborating, and cross-cutting information activities. Later DH workflow studies emphasize that humanities researchers rely strongly on browsing, rereading, assessing, chaining, collecting, and contextualized movement among source materials.

References:
- John Unsworth, "Scholarly Primitives: What Methods Do Humanities Researchers Have in Common, and How Might Our Tools Reflect This?" (2000).
- DHQ discussion of Unsworth/Palmer and activity-centered design: https://www.digitalhumanities.org/dhq/vol/8/2/000173/000173.html
- DHQ contextual workflow study: https://www.digitalhumanities.org/dhq/vol/12/3/000399/000399.html
- DHQ case-study protocol on scholarly activities and computational methods: https://www.digitalhumanities.org/dhq/vol/14/3/000477/000477.html

These sources justify activity-centered task design. They do not validate the project's CEDL ontology or experimental effects.

## Task realism criteria

Each task must satisfy all six criteria.

### R1 - recognizable scholarly operation
A humanist could plausibly perform the operation while inspecting source material.

### R2 - source-facing
The task is answerable from declared source/representation inputs rather than from benchmark labels.

### R3 - answer-neutral prompt
The prompt does not presuppose the expected relation or final humanistic judgment.

### R4 - separable instrument
The operation can be tested independently without pretending it is the whole interpretive process.

### R5 - compositional relevance
Its output can legitimately feed a later scholarly operation.

### R6 - ecological restraint
The project does not claim that laboratory microtask performance equals full historical interpretation.

## Natural task surface versus analytic coding

To avoid forcing participants into the project's ontology, every human-facing task has two layers.

### Natural task surface

The evaluator answers a scholarly question in ordinary language and identifies the evidence used.

Examples:

- "Who is responsible for this statement, and what in the supplied material supports that attribution?"
- "How, if at all, does the later passage bear on the earlier passage?"
- "Do these passages concern the same historical proposition or only related subject matter?"
- "What additional context, if any, is needed before you can answer?"

### Analytic coding layer

A separate blinded coding step maps the natural response onto the frozen analytical vocabulary:

- primitive CEDL relation;
- claim binding;
- recoverability class;
- recovery depth;
- recovery basis;
- residual uncertainty.

The same person should not silently convert an uncertain natural answer into a definite ontology label.

## Mapping of current task family

| Instrumented task | Scholarly operation analogue | Main activity grounding | Status |
|---|---|---|---|
| tau_locate | find a relevant passage/source | searching, chaining, browsing, accessing | REALISTIC |
| tau_attribute | establish source/voice responsibility | referring, assessing, contextual reading | REALISTIC |
| tau_sequence | establish edition/version order | comparing, referring, contextual reading | REALISTIC |
| tau_bind | determine whether evidence bears on the same referent/claim | referring, comparing, assessing | REALISTIC |
| tau_relation | assess how one source passage bears on another | comparing, assessing, rereading | REALISTIC WITH INSTRUMENTATION |
| tau_adjudicate | make the later humanistic warrant decision | interpretive synthesis | HELD SEALED |

tau_relation is retained only because its human-facing prompt is natural-language. The primitive relation vocabulary belongs to the analytic coding layer, not to the participant-facing task.

## Task composition

The project does not impose one fixed linear workflow.

A task may consume outputs from multiple prior operations:

locate, attribute, sequence, bind -> relation -> adjudicate

but an evaluator may also recover a relation directly from a passage without separately externalizing every upstream operation.

The task graph records analytical dependencies, not a psychological theory of reading.

## Realism failure conditions

A task is rejected or redesigned if:

- it can only be understood using project-specific ontology terms;
- it asks the evaluator to reproduce an author-coded answer;
- it requires an artificial operation with no plausible source-work analogue;
- its "success" depends on the final retain/revise/defer/withhold outcome;
- it is presented as representative of all humanities research.
