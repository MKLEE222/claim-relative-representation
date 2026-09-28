# Module G results — confirmatory transfer on published Codex Zacynthius corrigenda

Date: 2026-09-28  
Status: EXECUTED PRE-SOURCE-INSPECTION CONFIRMATORY TRANSFER STUDY.

Authoritative execution:
- pre-outcome implementation-failure run: 36382187686
- authoritative repaired run: 36382242263
- artifact: module-g-zacynthius-confirmatory-corrigenda-v1
- artifact ID: 10953530625
- artifact ZIP SHA-256: 490380ba2aaaccf4270375ef4a701f6d02e6c9942b75674b7f72d5f749664b5a
- results SHA-256: 00ac1c0646ec700a3101894f5eeff4006f10b894278f4f4ed3fb0451c8fa214a

Protocol freeze:
- commit 08054df5a1f71d713f2fe4ab2c48be593b4c8b4d
- committed before frozen-parent XML bodies were inspected

Source-contract freeze:
- commit 5872a3ff4cfe739650aaa9ab69f2abc80a5d032e
- committed after schema/source audit but before 48-cell matrix execution

Evaluator repair:
- first run stopped during source-contract verification before any matrix cell was evaluated
- repair only changed rubric direct-text indexing from an empty descendant-word key to the already-declared plain-text key
- no scientific population, arm, rule, metric or threshold changed

## 1. Independent-project transfer population

The study uses the complete published correction set under:

    DIGITAL EDITION: UNDERTEXT (and TRANSLATION)

on the public Codex Zacynthius corrigenda page.

Four correction events are retained:

- CZ-C1: fol. IIIr — omitted section-number insertion
- CZ-C2: fol. XIIIv, Extract 060-1 — Greek reading + linked translation replacement
- CZ-C3: fol. XVr, Extract 072-2 — source/title identification replacement
- CZ-C4: fol. XVIIIv, Extract 081-2 — translation + CPG reference revision

No correction was dropped after XML inspection.

Codex Zacynthius did not participate in the mechanism-development chain that produced Modules E/F.

## 2. Frozen parent representation

Parent repository:

    itsee-birmingham/codex-zacynthius-xml

Parent commit:

    2bc9ef70a5d3635e98b5a6b327833c57a5b0a67f

This is the first public commit of all XML transcriptions.

All five parent blobs were fetched, SHA-1 verified, size verified and parsed successfully.

PARENT_SNAPSHOT_COMPATIBLE = YES.

## 3. Strict full-channel outcomes: 2/4 clean executable

Under the strongest non-reopen interface:

    S_TEI
    + E_PUBLISHED_FULL
    + A_NONE

the four frozen events resolve as follows.

| Correction | Frozen parent state | Target | Result | Exact transition | Strict outcome |
|---|---|---:|---:|---:|---|
| CZ-C1 | clean omission state | exact | exact | yes | FULL_EXECUTABLE_EXACT |
| CZ-C2 | partial preintegration | exact | exact | no | LINKED_PARTIAL_ONLY |
| CZ-C3 | clean old state | exact | exact | yes | FULL_EXECUTABLE_EXACT |
| CZ-C4 | linked reference mismatch | exact | exact | no | FULL_SOURCE_STATE_MISMATCH |

Therefore:

    FULL_CORRIGENDA_EXECUTABILITY = 2/4

This is not rounded upward and not repaired with another source version.

## 4. CZ-C1 — independent target-binding transfer

Published correction class:
location-specific insertion before a rubricated source anchor at fol. IIIr.

### Full TEI + published event

    S_TEI + E_PUBLISHED_FULL + A_NONE

Candidate target groups:
1

Result:
- target exact: YES
- result exact: YES
- transition exact: YES

### Full TEI + targetless operation

    S_TEI + E_TARGETLESS_OPERATION + A_NONE

The operation payload retains the inserted section-number result but removes the source anchor/location.

Under the frozen source contract there is no pre-bound correction identity in S_TEI.

Result:

    REPRESENTATION_CANNOT_EXPRESS_LOCATOR

Thus:

    same inserted values
    !=
    same executable correction

without correction-to-source binding.

### Correction-source reopening

    S_TEI
    + E_TARGETLESS_OPERATION
    + A_CORRIGENDA_REOPEN

restores the full published locator/event and returns:

- one target
- exact result
- exact transition

Therefore the missing binding may be supplied by lawful correction-source access.

TARGET_BINDING_TRANSFER = YES.

## 5. CZ-C1 — TEI structure is not reducible to flattened readable content

Under:

    S_TEXT_ONLY + E_PUBLISHED_FULL + A_NONE

the event still names the published folio/structural context, but the retained representation has discarded:
- folio attributes
- hierarchy
- rubric markup
- XML IDs

The lexical anchor:

    ευαγγελιον

occurs 82 times in the mechanically flattened five-file parent corpus:

- L299-lectionary.xml: 71
- Zacynthius-catena.xml: 10
- Zacynthius-gospel.xml: 1

Therefore:

    candidate targets = 82

and the correction is non-determining.

The same correction is exact under S_TEI.

This is not a claim that TEI is universally necessary.
It is a finite demonstration that structural addressability carries task-relevant information not present in this text-only projection.

## 6. CZ-C3 — second clean correction, different mechanism

CZ-C3 targets:
- fol. XVr
- Extract 072-2
- old identification corresponding to "On Numbers"
- corrected identification "Sermon 115"

Under:

    S_TEI + E_PUBLISHED_FULL + A_NONE

the correction is exactly executable.

The same is true under:

    S_TEI + E_TARGETLESS_OPERATION + A_NONE

because the old source-side values are sufficiently distinctive inside the structured TEI state to recover one target group.

This is an important null against an overbroad locator-necessity claim:

> Published locator binding is not always required when the retained state and source-side values already determine the target.

However:

    S_TEXT_ONLY + E_PUBLISHED_FULL + A_NONE

has two compatible lexical assignments and is ambiguous.

Thus CZ-C3 independently supports a representation-structure contribution without supporting universal locator necessity.

## 7. CZ-C2 — target/result recoverable, but transition not clean

The frozen parent at Extract 060-1 is not the pure old state assumed by the public correction notice.

Greek parent state already contains:

    γεννασθαι

followed by the older:

    του κοσμου σρς

while the translation still retains the older sense "the Saviour of the world".

The published corrected combined reading instead requires the common-Saviour reading.

Therefore this snapshot is:

    PARTIAL_PREINTEGRATION

Across interfaces that uniquely identify the target:

- target can be exact
- corrected result can be specified exactly
- a clean parent->child transition matching the published correction cannot be claimed

Strict outcome:

    LINKED_PARTIAL_ONLY

This is a source-version/applicability result, not an evaluator failure.

## 8. CZ-C4 — exact target and result do not license an exact published transition

The full published locator uniquely identifies Extract 081-2 in the frozen Greek and translation TEI.

The translation side still reflects the uncorrected interpretation and therefore the published corrected result is meaningful.

But the linked reference state differs from the correction notice:

Published corrigendum precondition:

    CPG7058 -> CPG7072

Frozen parent TEI:

    CPG7039

No CPG7058 value occurs in the frozen parent XML.

Therefore:

- target exact: YES
- corrected result specified: YES
- exact published parent->child transition: NO

Strict outcome:

    FULL_SOURCE_STATE_MISMATCH

No later XML or rendered edition was introduced to repair this mismatch.

## 9. New separation: target/result determinacy is not transition applicability

CZ-C2 and CZ-C4 establish a distinction not isolated in the earlier Whitman/Urumtsi modules.

For a correction event E and retained parent state S:

    Target(E,S) = exact

and:

    Result(E,S) = exact

do not imply:

    Transition(E,S) = warranted

if E's source-side/precondition state does not match S.

Therefore a dynamic correction interface needs at least three separable checks:

1. target binding
2. event applicability / parent-state compatibility
3. corrected result specification

before selective update can be treated as warranted.

A bounded transition condition is:

    Applicable(E,S_t)
    AND
    DeterminateTarget(E,S_t,A_t)
    AND
    DeterminateResult(E,S_t,A_t)

Only then is the declared update licensed.

## 10. Text-only projection results

S_TEXT_ONLY deliberately keeps readable linear content while dropping XML structure.

Observed structure-dependent witnesses:

- CZ-C1: full event gives 82 candidates under text-only vs one target under TEI
- CZ-C3: full event gives 2 compatible lexical assignments under text-only vs one target group under TEI

Therefore:

    STATE_STRUCTURE_CONTRIBUTION = YES

with two frozen witnesses.

This does not imply that XML markup is always needed; CZ-C2 and CZ-C4 contain sufficiently distinctive lexical/source anchors for target recovery in several text-only cells.

## 11. Correction-source access is substitutable but not omnipotent

For CZ-C1:

    S_TEI
    + E_TARGETLESS_OPERATION
    + A_NONE

is non-determining.

Reopening the published corrigendum makes it exact.

Therefore:

    ACCESS_REPAIRS_CHANNEL_ABLATION = YES

However, source reopening does not repair CZ-C2's partial parent state or CZ-C4's reference-state mismatch.

This parallels Module E:

    access can restore missing event information
    but cannot retroactively make an incompatible parent state compatible.

## 12. Wrong controls

### Global lexical-match control

CZ-C1's lexical anchor occurs 82 times across the five parent files.

A global insertion strategy that ignores published source binding would:
- reach the intended occurrence
- also hit 81 collateral occurrences
- destructively mutate the parent source if implemented in place

Thus:

    GLOBAL_MATCH_FAILS_SELECTIVITY = YES

CZ-C2, CZ-C3 and CZ-C4 do not produce collateral global-match witnesses under the frozen parent; their source-side values are sufficiently selective in this corpus.

### Locator shuffle

A cyclic locator shuffle among CZ-C2/C3/C4 gives one syntactically valid structural target group for each wrong locator.

But in all three cases:

    source_side_compatible = false

Thus a locator-shaped field is not sufficient by itself; the selected target must also satisfy the event's source-side precondition.

## 13. Linked correction atomicity

The preregistered linked-event candidates were CZ-C2 and CZ-C4.

Neither can support a clean complete linked transition on the frozen parent:

- CZ-C2: partial preintegration
- CZ-C4: CPG pre-state mismatch

Therefore:

    LINKED_CORRECTION_ATOMICITY = NO

This is retained as a confirmatory null.

It does not show linked correction transactions are impossible.
It shows the frozen parent cannot warrant those two complete transitions under the published event assumptions.

## 14. Scientific dispositions

PARENT_SNAPSHOT_COMPATIBLE = YES

FULL_CORRIGENDA_EXECUTABILITY = 2/4

TARGET_BINDING_TRANSFER = YES
- witness: CZ-C1

STATE_STRUCTURE_CONTRIBUTION = YES
- witnesses: CZ-C1, CZ-C3

ACCESS_REPAIRS_CHANNEL_ABLATION = YES
- witness: CZ-C1

LINKED_CORRECTION_ATOMICITY = NO

PROVENANCE_PRESERVING_TRANSFER = YES

GLOBAL_MATCH_FAILS_SELECTIVITY = YES
- witness: CZ-C1

## 15. Confirmatory interpretation

Module G is a previously unused editorial project selected after the dynamic-sufficiency mechanism was already fixed.

Therefore the following mechanism-level evidence is confirmatory with respect to the pre-source-inspection claims:

### Confirmed

1. Correction values can be insufficient without correction-to-target binding.
2. Representation structure can carry task-relevant target distinctions beyond readable text content.
3. Missing event detail can sometimes be supplied by lawful correction-source access.
4. A provenance-preserving overlay can represent correction without rewriting the parent witness.
5. Global value matching can produce a correct local result while violating selectivity.

### Not confirmed as universal

1. Every correction requires explicit locator binding — CZ-C3 is a natural null.
2. Every published corrigendum is directly executable against a frozen source snapshot — strict result is 2/4.
3. Linked multi-field corrections are cleanly atomic on this snapshot — 0/2 strict linked events.
4. Correction-source reopening repairs source-version incompatibility — it does not.

The appropriate overall characterization is:

    BOUNDED CONFIRMATORY MECHANISM TRANSFER
    WITH SOURCE-VERSION/APPLICABILITY NULLS

not:

    4/4 replication pass.

## 16. Consequence for dynamic sufficiency

The earlier dynamic interface was:

    I_t = (S_t, E_t, A_t)

Module G adds an explicit applicability gate:

    Applicable(E_t, S_t)

A warranted update therefore requires both:

    information sufficiency

and:

    transition compatibility.

One useful decomposition is:

    WarrantedUpdate
    =
    TargetDeterminacy
    AND EventApplicability
    AND ResultDeterminacy
    AND Selectivity
    AND ProvenancePreservation

with transition auditability remaining an additional task when historical update history itself matters.

This is stronger than a field checklist and more precise than saying only that "more provenance" is useful.

## 17. Claim ceiling

Supported:

> In an independently selected scholarly edition and its complete published digital-corrigenda set, the previously developed state/event/access mechanism transfers in bounded form: target binding and retained representation structure can determine whether a correction is selectively executable, and correction-source access can substitute for missing event detail. The study also shows that exact target and corrected-result recovery are insufficient when the published correction's assumed parent state is incompatible with the frozen source snapshot.

Not supported:
- all four corrections are clean replications;
- all digital corrections require structured markup;
- the frozen XML is the only legitimate project state;
- the corrigenda establish independent historical truth;
- a universal minimal correction representation;
- four statistically independent replications.

## 18. Stop

Do not rerun Module G with:
- a later parent version;
- only CZ-C1/C3;
- a rendered Cambridge page;
- an image-derived parent state;
- broader fuzzy matching.

The partial/mismatch outcomes are part of the confirmatory result.

A later source-history study may investigate why CZ-C2/C4 and the frozen XML snapshot differ, but it must be a new study and must not replace Module G.
