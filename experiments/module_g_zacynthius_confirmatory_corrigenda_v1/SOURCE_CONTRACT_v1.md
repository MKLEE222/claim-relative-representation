# Module G source contract v1 — frozen after schema audit, before matrix execution

Date: 2026-09-28
Status: SOURCE-SCHEMA CONTRACT. SCIENTIFIC POPULATION AND CLAIM RULES REMAIN THOSE OF PROTOCOL.md.

## 1. Timing

PROTOCOL.md was committed at:

    08054df5a1f71d713f2fe4ab2c48be593b4c8b4d

before any frozen-parent XML body was inspected.

This source contract was written after inspecting the XML schema/content required to implement the already-frozen protocol, but before executing the 48-cell matrix.

It does not:
- remove any correction;
- change the parent commit;
- add any later source;
- change a success threshold;
- add a correction-specific XPath.

## 2. Generic folio normalization

Published corrigenda use Roman folio labels:

    IIIr, XIIIv, XVr, XVIIIv

The TEI uses machine labels such as:

    3r
    P13v-CZ
    P15r-CZ
    P18v-CZ

The evaluator applies one global mapping:

1. Roman numeral -> Arabic integer;
2. preserve recto/verso suffix r/v;
3. for TEI page labels strip optional leading P;
4. strip project suffix beginning at "-";
5. compare the resulting form, e.g. XIIIv -> 13v.

This rule is applied to all four corrections.

## 3. Generic extract normalization

Published extract identifiers such as:

    060-1
    072-2
    081-2

are matched only against TEI element attribute:

    n="<extract-id>"

on elements with:

    type="comment"

No hand-authored file or XPath is assigned to an extract.

The same locator is allowed to identify linked Greek/translation targets in separate files.

## 4. Generic lexical normalization

Parent source bytes remain authoritative and unchanged.

Candidate matching uses two declared keys.

### N1 — TEI lexical key

For TEI word elements:
- concatenate all descendant text within one <w>;
- remove whitespace introduced inside that word by line-break markup;
- include expansion text such as <ex>;
- NFC normalize;
- casefold;
- join words with one space.

For non-word metadata/note text:
- itertext;
- NFC;
- collapse whitespace;
- casefold.

### N2 — Greek base-letter diagnostic key

When the published corrigendum omits Greek diacritics but TEI contains them:
- derive NFD from N1;
- remove Unicode combining marks;
- NFC recompose.

N2 is applied globally to every Greek correction, not only CZ-C4.
Every match records whether N1 or N2 was required.

No punctuation deletion or fuzzy edit-distance matching is allowed.

### Corrigendum notation normalization

In published Greek correction strings only:
- square brackets are editorial supply notation and are removed while retaining enclosed letters;
- parentheses in abbreviations are removed while retaining enclosed letters;
- whitespace is collapsed;
- then N1/N2 normalization applies.

Thus, for example:

    απο αριθ(μων)

maps to a comparison key equivalent to:

    απο αριθμων

without changing the source witness.

## 5. Generic structural index

For every parsed TEI file, the evaluator constructs mechanically:

- current folio from the most recent <pb>;
- current extract/comment identity from <ab type="comment" n="...">;
- element path generated from document structure;
- text/word stream for that element;
- all <hi rend="rubric"> text spans;
- all attributes and note text inside the indexed element.

No correction-derived entries are inserted into this index.

## 6. Text-only projection

S_TEXT_ONLY is generated from the same five parent files by:

- preserving file identity;
- preserving linear lexical/text sequence;
- dropping element names;
- dropping attributes;
- dropping xml:id;
- dropping hierarchy and folio/extract structural labels.

It does not inherit the structural index as hidden decoder knowledge.

Published locators unavailable in this projection cannot be used to filter candidates.

## 7. Pre-matrix parent-state audit

These facts are recorded before matrix execution.

### CZ-C1 — fol. IIIr insertion

The frozen gospel TEI contains one rubricated:

    ευαγγελιον

at folio 3r.

The published alpha/beta section-number insertion described by the corrigendum is not represented immediately before that rubricated target in the parent structure.

Parent classification:

    OLD_OMISSION_STATE_COMPATIBLE

### CZ-C2 — fol. XIIIv, Extract 060-1

The frozen Greek extract 060-1 is uniquely present at folio 13v.

Its local source stream already contains:

    γεννασθαι

followed by the older:

    του κοσμου σρς

rather than the published corrected combined reading:

    γεννασθαι του κοινου σρς

The translation extract still contains the old sense:

    the Saviour of the world

Parent classification:

    PARTIAL_PREINTEGRATION

This event must not be counted as a clean full old->new transition on this snapshot.

### CZ-C3 — fol. XVr, Extract 072-2

The frozen Greek and translation extract 072-2 are uniquely present at folio 15r.

Both retain the old identification:
- Greek label equivalent to "from Numbers";
- metadata/translation source identification "On Numbers".

Parent classification:

    CLEAN_OLD_STATE_PRESENT

Occurrences of "Sermon 115" elsewhere in the edition do not count as this target because they belong to other extract identities.

### CZ-C4 — fol. XVIIIv, Extract 081-2

The frozen Greek and translation extract 081-2 are uniquely present at folio 18v.

The translation/source label still renders the relevant phrase as:

    response

and therefore has not incorporated the published "in a Hymn" correction.

However, the frozen TEI relation/reference state uses:

    CPG7039

for this extract.

The published corrigendum says a reference:

    CPG7058 -> CPG7072

No CPG7058 value occurs in the frozen parent XML.

Parent classification:

    LINKED_REFERENCE_STATE_MISMATCH

The translation component may be executable, but the complete linked published correction cannot be counted as an exact transition on this parent snapshot.

## 8. Replacement exactness rule

For REPLACE events, a clean exact transition requires:

1. full published target is uniquely identified;
2. every source-side field explicitly asserted by the corrigendum is compatible with the frozen parent target;
3. every corrected field is specified;
4. applying the overlay would not require guessing an unreported intermediate state.

If only part of a linked correction is compatible:

    LINKED_PARTIAL_ONLY

If an explicitly asserted old field conflicts with the frozen parent:

    FULL_SOURCE_STATE_MISMATCH

Do not change the parent snapshot to avoid these outcomes.

## 9. Insertion exactness rule

For INSERT/omission corrections, exact transition requires:
- unique insertion anchor from the available interface;
- corrected insertion payload from the event;
- absence of the published inserted content at that anchor in the parent state.

No claim is made that absence from a text-only projection proves absence from the manuscript image.

## 10. Targetless insertion

If E_TARGETLESS_OPERATION removes the only published source anchor for an insertion event, the evaluator does not invent a semantic anchor.

The cell is non-determining and reports:

    REPRESENTATION_CANNOT_EXPRESS_LOCATOR

unless S_TEI or another declared interface component independently contains an explicit correction-target binding. S_TEI has no such pre-bound correction identity.

## 11. No rescue

The following are prohibited in Module G v1:
- later XML versions;
- Cambridge rendered HTML as a replacement parent;
- manuscript-image adjudication;
- correction-specific fuzzy search;
- changing CPG7039 to 7058 by assumption;
- treating partial CZ-C2 state as a clean old state;
- dropping CZ-C2/CZ-C4 from the four-event population.

These may motivate a later source-history study, but not a repair of Module G.
