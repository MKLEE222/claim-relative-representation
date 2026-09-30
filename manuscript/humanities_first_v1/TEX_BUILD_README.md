# Manuscript build and verification

The editable argument is `MANUSCRIPT_v2.md`. `build_manuscript_tex.py` converts it mechanically into `MANUSCRIPT_v2.tex`. The TeX source includes the two figure PDFs generated from the checked-in R sources in `figures/`.

From the `manuscript/humanities_first_v1/` directory, with R, Python 3, and XeLaTeX available:

```text
Rscript figures/make_figure_1.R figures
Rscript figures/make_figure_2.R figures
python build_manuscript_tex.py
xelatex --disable-installer -interaction=nonstopmode -halt-on-error MANUSCRIPT_v2.tex
xelatex --disable-installer -interaction=nonstopmode -halt-on-error MANUSCRIPT_v2.tex
```

The R scripts use base/grid only and write SVG, PDF, and PNG outputs to the supplied existing directory. The paper uses the generated figure PDFs. The converter uses Times New Roman and Arial, so those fonts or suitable replacements must be available for identical layout. No TeX package installation was performed in the checked local build.

Local acceptance on 30 September 2026: XeLaTeX produced a 14-page A4 PDF; both figures and all three tables appeared; the final log had no overfull boxes or LaTeX errors. The source, PDF, and audit record are kept in the author's D-drive workspace. The Codex built-in compiler reported a Windows platform-directory error, so this acceptance uses the existing D-drive XeLaTeX and direct rendered-PDF inspection. The PDF itself is not checked into the GitHub branch; it is reproducible from these sources.

The accompanying `COLD_START_ADVERSARIAL_ACCEPTANCE_20260930.md` distinguishes closed editorial issues from remaining submission gates. Generating a PDF does not close the fixed-image quotation check, independent historical validation, dataset reuse-term verification, or author declarations.

