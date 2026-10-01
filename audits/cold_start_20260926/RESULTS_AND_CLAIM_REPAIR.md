# Cold-start audit: results and claim repair

Date: 2026-09-26
Audited main commit: `3f4f31792a59bdb2d1a2bd57893f417d2d3c6a07`
Diagnostic execution: GitHub Actions `36244824296`
Diagnostic code/workflow commit: `b1216920d575c603d6994314d02750c8183a0130`
Artifact: `crr-cold-start-diagnostic-20260926`
Artifact SHA-256: `3b8d7915ce95e1f0050704dfb708fd83f0a29867bbc60c708f80b8c2593f6801`

**Authority:** post-result source/code audit, not another holdout. Original experiments, failed judge outputs, protocols and main manuscript are unchanged. Successful CI means execution completed, not that the previous scientific claims survived.

## Executive decision

The material supports continued manuscript development, but the previous blanket claim that minimality and warrant closure were already secure was too strong. Three categories require separation: observed failures of specified decoders; information loss under a fully specified projection; and consequences conditional on a chosen interpretation. The manuscript should not trade these categories against one another.

## 1. Frankenstein: a weak decoder was being read as an impossibility result

The original pinned C18 apparatus reproduces 493 comparison units, 267 multigroup units and 166 disagreements between native grouping and whitespace-only equality of serialized reading content. All 166 original disagreements split a native group; none merge distinct groups.

This reading content includes escaped documentary XML, not just linguistic text. Two explicitly post-result diagnostics give:

| Decoder | Grouping mismatches / 493 | Units with within-group splits | Units with between-group merges |
|---|---:|---:|---:|
| Original whitespace-only serialized content | 166 | 166 | 0 |
| Remove serialized XML tags; collapse whitespace | 25 | 21 | 4 |
| Above plus case folding and ampersand-to-and | 5 | 1 | 4 |

No missing witness IDs or repeated witness IDs within an app were found.

Example: zero-based app 79 groups manuscript `benevo<lb .../>lent` separately from print `benevolent`, with native normalized descriptors `benevo lent` and `benevolent`. Removing the line marker joins the word and incorrectly merges the native groups. The residuals concern concrete normalization choices; they are not evidence of an irreducible layer of editorial meaning.

**Retain:** the original exact-string decoder fails; operation-specific normalization changes both false distinctions and lost distinctions.

**Withdraw:** the 166 count proves that no reading-based decoder can reconstruct the groups, or that native group membership is universally necessary.

**Required repair:** reproduce the project's own normalization/alignment contract, retain IDs and source mappings, and test a declared reconstruction algorithm. A failed algorithm and nonexistence of any adequate algorithm are different claims. `rdgGrp@n` copied from the target groups cannot be an independent predictor.

## 2. Whitman: the full retained key matters

The old script enumerates subsets but marks them sufficient through the hard-coded condition `{'PRINT_LOCUS','MS_FILE','MS_LOCUS'} <= S`. That is a schema-obligation check, not an empirical recovery search.

The native file has 1,444 valid two-endpoint link records; there are no malformed target lists and no missing group file identities in this population. Actual conditional ambiguity is:

| Retained key | Distinct keys | Keys associated with multiple manuscript files | Records at ambiguous keys |
|---|---:|---:|---:|
| manuscript-local locus | 297 | 91 | 1,096 |
| printed locus + manuscript-local locus | 1,417 | 25 | 52 |
| printed locus + manuscript-local locus + certainty | 1,423 | 20 | 41 |

A concrete last-row witness is `(ppp.01880.xml#l1045, #l01, high)`, which occurs with both `duk.00261.xml` and `uva.00262.xml`.

**Retain:** manuscript-local names are not globally unique; the ambiguity persists even after the printed locus and certainty are supplied in a record-local interface.

**Do not yet claim:** a globally unique minimum for every whole-document decoder. Group positions, file organization and authorized external maps must be included in the declared projection. Uniqueness on a finite corpus does not supply a lawful inverse lookup table.

**Required repair:** implement the endpoint-set decoder on projected records, compare complete outputs, and attach an explicit collision witness for every asserted necessity. State whether scope is one link record or an entire document.

## 3. Faust: full provenance includes source sets

The pinned archive contains 22 relevant XML files, with zero parse failures in this run. It contains 1,089 eligible `temp-pre` assertions, all with source URIs. Importantly, **53 assertions contain more than one source element**. The original use of `find` instead of `findall` retains only the first source.

The 1,959 adjacent constraint occurrences comprise 1,015 unique directed constraints. There are 641 nodes, 20 nontrivial strongly connected components and 118 nodes in those components. Their internal constraints comprise 612 occurrences but only 207 unique directed edges. These are different denominators, not interchangeable sample sizes.

Conditional source-set ambiguity:

| Key/domain | Ambiguous keys |
|---|---:|
| file / all assertions | 5 |
| file + ordered item sequence / all assertions | 8 |
| file / internal conflict-edge occurrences | 4 |
| file + directed edge / internal conflict-edge occurrences | 3 |

There are therefore concrete provenance ambiguities after more context is retained; the original mixed-file finding was directionally useful but did not test the full claimed projection. Source locators are another potentially retained carrier and must also be accounted for before declaring source URI uniquely necessary.

**Required repair:** represent every assertion's complete source set, preserve native ordering semantics, test the full retained projection and report occurrence versus unique-edge denominators. Do not hard-code `TASK_A_MINIMAL=ORDERED_ITEMS` as a discovered result.

## 4. The formal graph is not empirical rescue of the judge null

The argument-reinstatement protocol explicitly postdates the failed LLM study. Its three-node directed stance graph gives OUT-to-IN by construction. This is an application of established grounded semantics, not an additional empirical confirmation that scholarly warrant changed.

A diagnostic graph-mapping sensitivity check gives:

| Illustrative mapping | Without PM03 | With PM03 |
|---|---|---|
| Directed archival stance chain | OUT | IN |
| Mutual base rebuttal; directed counter-objection | UNDECIDED | IN |
| Mutual rebuttal and counter-rebuttal | UNDECIDED | UNDECIDED |

These alternatives are not asserted to be equally correct historical readings. They show which modeling decision must be justified from the sources. The grounded implementation was independently checked against enumeration of complete extensions on all 512 directed three-node graphs, including self-attacks. This checks computation, not the historical graph mapping.

A node outside the grounded extension is not automatically OUT. OUT means attacked by an IN node; the remaining nodes are UNDECIDED.

**Placement:** a transparent post-result analytical illustration, preferably discussion/appendix, not the abstract's decisive empirical success.

## 5. Uploaded LLM run: valid null, unproven failure diagnosis

The user's archive SHA-256 and frozen JSONL SHA-256 match their recorded values. All 45 call IDs match the frozen input. Raw receipts show `done_reason=stop` for all 45 calls; no cited evidence ID falls outside its supplied packet.

| Model | Prompt-evaluation tokens min/max | Maximum generated tokens | Frozen outcome |
|---|---:|---:|---|
| Qwen2.5 7B | 4,285 / 6,118 | 174 | one packet perturbation-sensitive |
| Gemma3 12B | 4,270 / 6,014 | 298 | all packets RETAIN |
| Llama3.1 8B | 4,083 / 5,691 | 155 | all packets RETAIN |

Configured context is 16,384 and generation maximum is 1,024. These receipts supply no positive evidence of limit-induced truncation; they are not a tokenizer-level proof of complete ingestion.

Each packet contains six merged units, but candidate text lengths are 2,103, 2,401, 2,129, 2,111 and 2,383 whitespace-delimited words for generic, guided, rescue, sham and removal respectively. Equal unit count is not equal reading budget. This is a diagnostic limitation, not a demonstrated explanation of the null.

Most importantly, the prompt asks whether a statement is *admissible as evidence*. Admissibility, truth, belief, undefeated support and grounded acceptance are not interchangeable. A challenged report may remain admissible while deserving less weight. All-RETAIN therefore does not by itself show that a model ignored the objection or failed reasoning. Some rationales explicitly mention the objection.

**Retain:** selective restoration was not supported by the frozen test; Qwen is perturbation-sensitive; the other two models show no categorical contrast.

**Withdraw:** the test proves the models are bad warrant instruments, or that their null validates the newly selected formal semantics. No additional judge run is needed for these repairs.

## 6. Literature boundary

The revised related work must explicitly address:

- Birnbaum and Spadini (2020), *Reassessing the locus of normalization in machine-assisted collation*, DHQ 14(3): normalization affects alignment and interpretation, and includes Frankenstein examples.
- Fan, Geerts and Zheng (2012), *View determinacy for preserving selected information in data transformations*, Information Systems 37(1):1-12, DOI 10.1016/j.is.2011.09.001: selected information preservation and query-relative reconstruction are established formal objects.
- CIDOC CRMinf: an existing cultural-heritage ontology for premises, conclusions, inference and belief adoption. A new nameset for the same functions is not a contribution.
- Dung (1995), DOI 10.1016/0004-3702(94)00041-X, and structured-argument approaches distinguishing rebuttal, undercutting and preferences.

The candidate contribution is an executable, source-bound audit connecting concrete scholarly tasks to retained relations, permitted reconstruction and failure witnesses. It is not the discovery that representation is interpretive or task-relative. That narrower contribution still needs direct native-baseline and certificate tests.

## Bounded strengthening route

1. Rebuild the carrier tests as actual decoders plus explicit full-projection collision witnesses, not declared field membership. Prioritize Whitman and Faust, which already contain natural ambiguous bindings.
2. Run the native Frankenstein normalization contract as the primary comparator; keep all post-result diagnostics separately labeled.
3. Make the historical Yule-Cordier question and source limits the narrative center; distinguish discovery, criticism exposure and claim admissibility. Keep the judge null and the later formal illustration as separate outcomes.
4. Complete manuscript v0.1 with these boundaries. Stop expanding the corpus and stop model shopping. Submission readiness is determined by these closed evidence obligations, not another percentage or green CI badge.
