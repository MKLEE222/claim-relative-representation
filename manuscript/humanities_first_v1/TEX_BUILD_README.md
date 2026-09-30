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

Current visual review on 30 September 2026: the authoritative Markdown produced a 17-page A4 PDF after the converter was repaired to read the current title and render fourth-level headings. Both current figures and all three tables appear. The final log has no overfull boxes or LaTeX errors, and all 17 pages were inspected as rendered images. The built-in compiler reported a Windows platform-directory error, so this review uses the installed D-drive XeLaTeX. The PDF is a reading and visual-review copy, not the DHQ upload format: DHQ currently accepts DHQ XML, TEI XML, RTF, OpenOffice, or Word for initial article submission, with figures embedded for review. The PDF itself is not checked into the GitHub branch; it is reproducible from these sources.

The [evidence and reproducibility companion](EVIDENCE_AND_REPRODUCIBILITY.md) records the fixed-page-image quotation check and the status of the computational analyses. Generating a PDF does not establish independent historical validation, permission to redistribute the Formalization Papers records, author declarations, or compliance with DHQ's AI-use policy.

