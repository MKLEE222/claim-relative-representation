# EP_EXT_01 results - Scrivener explicit-pointer holdout

Date: 2026-09-24
Authoritative CI run: 35960821675

## Selection

Episode was frozen before outcome using the structural rule:

first single-page, single-line lexical "for X read Y" correction after page 20, excluding chapter-number navigation corrections.

Selected native correction:

P. 87, l. 19, for Synaxaria read Menologies.

## Native source

Project Gutenberg eBook #36548.

HTML SHA-256:
efcdb75d3db84ee083fea2209dc3a018936cc5d0715587b4772b24b940d10749

## Result

### SCR-FULL-POINTER

Page + line + lexical substitution exposed.

State:
EXACT_LOCALIZATION

Candidates:
1

### SCR-PAGE-ONLY

Line coordinate removed; page + old/new reading retained.

On native page 87:

- occurrences of "Synaxaria": 1

State:
EXACT_LOCALIZATION

Candidates:
1

### SCR-POINTER-FREE

Page and line removed; only lexical substitution retained.

Across the body:

- occurrences of "Synaxaria": 2
- target occurrence ordinal: 2

State:
MULTIPLE_CANDIDATES

## Minimal sufficient pointer result

For this frozen localization task:

\[
\{page,\ old\ reading\}
\]

is sufficient to isolate the target occurrence.

The line coordinate is redundant under the native page segmentation and lexical substitution.

Removing the page coordinate creates ambiguity:

\[
1 \rightarrow 2\ candidate\ loci.
\]

## Interpretation

This is a clean external example of contract-relative productive compression.

The result does **not** say the full page+line pointer is useless.

It says that for this specific localization task and native object, one coordinate can be removed without changing the admissible target set, while removing a second coordinate crosses the task-equivalence boundary.

Thus:

\[
full\ pointer
\equiv_{\tau_{localize}}
page+old\ reading
\]

but:

\[
page+old\ reading
\not\equiv_{\tau_{localize}}
old\ reading\ only.
\]

## Scientific value

The holdout is useful because it supplies the opposite of a "more metadata is always better" result.

Some representational detail is genuinely redundant for a frozen task.

The framework must therefore identify minimal sufficient carrier sets rather than reward maximal retention.

## Boundary

No textual-critical truth was adjudicated.

The experiment concerns only localization of an editor-authored correction pointer.
