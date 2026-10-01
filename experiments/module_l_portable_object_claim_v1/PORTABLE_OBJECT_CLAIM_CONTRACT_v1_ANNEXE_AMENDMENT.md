# Portable object/claim contract v1 — pre-fresh annex lexical amendment

Date frozen: 2026-09-28
Status: PRE-FRESH HARDENING AMENDMENT. FROZEN FROM ALREADY-EXPOSED DAHN MATERIAL BEFORE ANY NEW INDEPENDENT EPISODE XML IS OPENED.

## 1. Reason

The portable v1 contract excludes material under:

    div type="annex"

During exposed regression inspection, already-exposed DAHN TEI was observed to use the French spelling:

    div type="annexe"

for the same editorial enclosure/annex function.

Treating only the English spelling as excluded would make object identity depend on an encoding-language spelling accident and could reintroduce the exact class of annex contamination that Modules H/J were designed to prevent.

## 2. Frozen normalization

For Module L and later portable studies, the annex predicate is:

    normalized @type in {"annex", "annexe"}

where normalization is lowercase + surrounding-whitespace removal.

Both values are exclusion containers.

Consequences:
- a div type="letter" below either annex spelling cannot establish Route A;
- a date below either annex spelling cannot enter active root temporal claims;
- such dates are diagnostic EXCLUDED_ANNEX;
- no first-object or nested-letter rescue is allowed.

## 3. Scope boundary

This amendment does not introduce open-ended synonym matching.

Values such as:
- attachment
- enclosure
- appendix
- supplement

are not automatically treated as annexes unless a future generic contract is separately frozen before outcome exposure.

The present amendment is limited to a semantic spelling equivalence observed in already-exposed development material.

## 4. Mandatory control

Add a pre-fresh fault/control case in which:
- one valid primary letter exists;
- an annexe sibling or ancestor contains another div type="letter" and a temporal date.

The portable engine must:
- keep exactly one primary scholarly object;
- exclude the nested annex letter from Route A;
- classify its date as EXCLUDED_ANNEX;
- preserve oracle/runtime agreement.
