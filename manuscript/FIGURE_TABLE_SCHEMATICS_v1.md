# Figure and Table Schematics v1

Date: 2026-09-26
Status: schematic only; user retains final visual design control

## Figure 1 — Task-relative representation adequacy

Purpose:
show the complete paper logic without implying that each arrow is empirical in the same way.

Schematic:

```text
SOURCE / SCHOLARLY OBJECT
          |
          v
  DIGITAL REPRESENTATION R
          |
          | exposes / suppresses carriers
          v
  DOCUMENTARY RELATIONS G_D
  - attribution
  - attachment
  - sequence
  - citation
  - referent
  - certainty / modality
          |
          | source-grounded mediation
          v
  ACTIVE EVIDENCE E_tau
          |
          | task contract (tau, K)
          v
  SCHOLARLY OPERATION
          |
          +--------------------------+
          |                          |
          v                          v
  TASK OUTPUT                  ACTIVE ARGUMENT GRAPH
                                     |
                                     | fixed formal semantics
                                     v
                              FORMAL CLAIM STATUS
```

Annotation:
“Representation adequacy is evaluated relative to task, not globally.”

---

## Figure 2 — Paper-money argument reinstatement

Schematic:

```text
PM01 / A0
Polo material assertion
      ^
      |
      | attacks
      |
PM02 / A1
Bretschneider objection
      ^
      |
      | attacks
      |
PM03 / A2
Laufer correction
```

Condition overlays:

```text
GENERIC:
A1 -> A0
Grounded extension: {A1}
A0 = OUT

GUIDED / RESCUE:
A2 -> A1 -> A0
Grounded extension: {A2, A0}
A0 = IN
```

Do not visually imply historical truth; label:
“formal acceptance under grounded semantics.”

---

## Figure 3 — Selective restoration design

Schematic:

```text
GENERIC_BASE          [PM03 absent] -> OUT
      |
      +-- add PM03 ----------------> IN

GENERIC_SHAM          [other donor] -> OUT

GUIDED_BASE           [PM03 active] -> IN
      |
      +-- remove PM03 -------------> OUT
```

Caption logic:
same frozen focal claim; selective add-back/removal of the source-bound correction relation.

---

## Table 1 — Cross-case task/carrier map

Columns:

| Case | Frozen task | Native relation/carrier | Minimal / required carrier | Evidence authority | Result role |
|---|---|---|---|---|---|
| Paper money | expose later correction relevant to material claim | cited source + native sequence | source + sequence / PM03 unit | primary historical case | load-bearing consequence |
| Kinsay | recover later eyewitness-status evidence | referent identity + native sequence | referent bridge | exploratory after failure | mediation mechanism |
| Coal | locate editorial accretion attached to fuel observation | local note attachment | native note marker | boundary case | local attachment suffices |
| Scrivener | locate corrigendum target | page / line / old reading | page + old reading | external holdout | productive compression |
| Frankenstein C18 | recover native reading partition | witness ID + rdgGrp membership | witness ID + rdgGrp membership | untouched external holdout | relation structure > string equality |
| Whitman | recover linked manuscript locus | print locus + ms file + ms locus | same | mechanism | task-dependent redundancy |
| Faust | recover conflict graph / source identity | ordered items / source URI | task-specific | mechanism | task-dependent carrier family |

---

## Table 2 — Minimal-carrier quantitative summary

Rows should include:

- Frankenstein C18: 493 app units; 166 exact-text partition mismatches.
- Whitman: 1444 link records; 91 manuscript local IDs reused across files.
- Faust: 20 nontrivial SCCs; 612 internal conflict edges; file context does not determine source URI.
- Scrivener: full page+line pointer reduces to page+old reading for frozen localization; reading-only ambiguous.

Do not pool into a score or leaderboard.

---

## Table 3 — LLM stress-test boundary

| Model | Perturbation stability | Packet sensitivity | Final role |
|---|---|---|---|
| Qwen2.5 7B | fail on sham packet | unstable | model-sensitive |
| Gemma3 12B | pass | none; all RETAIN | stable-insensitive |
| Llama3.1 8B | pass | none; all RETAIN | stable-insensitive |

Interpretation:
stability alone is not evidence of relation-sensitive adequacy.

Do not title this table “LLM failure.”
Suggested title:
“Stress test of computational use of evidential relations.”
