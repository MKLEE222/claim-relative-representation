"""Mechanical conversion of the reviewed Markdown draft to a XeLaTeX manuscript.

The Markdown remains the editorial source. This script only prepares a typeset copy.
"""

from pathlib import Path
import re


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "MANUSCRIPT_v2.md"
TARGET = BASE / "MANUSCRIPT_v2.tex"
REPO = "https://github.com/MKLEE222/claim-relative-representation/blob/audit/cold-start-20260926/manuscript/humanities_first_v1/"


def escape(text):
    mapping = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
               "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
               "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(mapping.get(char, char) for char in text)


def url_arg(url):
    if not url.startswith(("https://", "http://")):
        url = REPO + url
    return url.replace("%", r"\%").replace("#", r"\#").replace("&", r"\&").replace("_", r"\_")


def inline(text):
    tokens = []

    def hold(value):
        token = f"ZXLATEXTOKEN{len(tokens)}ZX"
        tokens.append((token, value))
        return token

    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)",
                  lambda m: hold(r"\href{" + url_arg(m.group(2)) + "}{" + inline(m.group(1)) + "}"), text)
    text = re.sub(r"https?://[^\s)]+", lambda m: hold(r"\url{" + m.group(0).rstrip(".,") + "}") + m.group(0)[len(m.group(0).rstrip(".,")):], text)
    text = re.sub(r"`([^`]+)`", lambda m: hold(r"\texttt{" + escape(m.group(1)) + "}"), text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: hold(r"\textbf{" + inline(m.group(1)) + "}"), text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: hold(r"\emph{" + inline(m.group(1)) + "}"), text)
    text = escape(text)
    for token, value in tokens:
        text = text.replace(token, value)
    return text


def caption_text(line, kind):
    return re.sub(r"^\*\*" + kind + r" \d+\.\*\*\s*", "", line)


def table_tex(block, caption, number):
    rows = []
    for line in block:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    if number in (1, 2):
        spec = r">{\raggedright\arraybackslash}p{.23\linewidth}>{\raggedright\arraybackslash}p{.25\linewidth}>{\raggedright\arraybackslash}p{.43\linewidth}"
    else:
        spec = r">{\raggedright\arraybackslash}p{.38\linewidth}*{3}{>{\centering\arraybackslash}p{.17\linewidth}}"
    result = [r"\begin{table}[H]", r"\centering", r"\footnotesize", r"\renewcommand{\arraystretch}{1.18}", r"\setlength{\tabcolsep}{3pt}",
              r"\begin{tabular}{" + spec + "}", r"\toprule"]
    for idx, row in enumerate(rows):
        result.append(" & ".join(inline(cell).replace(r"\_", r"\_\allowbreak{}") for cell in row) + r" \\")
        if idx == 0:
            result.append(r"\midrule")
    result += [r"\bottomrule", r"\end{tabular}",
               r"\caption{" + inline(caption_text(caption, "Table")) + "}",
               r"\label{tab:" + str(number) + "}", r"\end{table}"]
    return "\n".join(result)


def figure_tex(image_line, caption, number):
    filename = f"figures/figure_{number}_" + (
        "scholarly_continuation.pdf" if number == 1 else "current_state_vs_continuation.pdf")
    return "\n".join([r"\begin{figure}[H]", r"\centering",
                      r"\includegraphics[width=\linewidth]{" + filename + "}",
                      r"\caption{" + inline(caption_text(caption, "Figure")) + "}",
                      r"\label{fig:" + str(number) + "}", r"\end{figure}"])


PREAMBLE = r"""\documentclass[11pt,a4paper]{article}
\usepackage[a4paper,margin=25mm,headheight=14pt]{geometry}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\usepackage{amsmath,amssymb}
\newcommand{\Beta}{\mathsf{B}}
\newcommand{\Kappa}{\mathsf{K}}
\usepackage{graphicx}
\usepackage{booktabs,array,tabularx,float}
\usepackage{microtype}
\usepackage{hyperref}
\usepackage{fancyhdr}
\hypersetup{colorlinks=true,linkcolor=black,urlcolor=blue,citecolor=black}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small After Revision}
\fancyhead[R]{\small Digital editions and scholarly continuation}
\fancyfoot[C]{\thepage}
\setlength{\parskip}{0.35em}
\setlength{\parindent}{1.25em}
\emergencystretch=2em
\tolerance=1800
\begin{document}
\begin{center}
{\LARGE\bfseries After Revision: Scholarly Continuation in Digital Editions\par}
\vspace{0.7em}
\end{center}
\vspace{1em}
"""


def build():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    out = [PREAMBLE]
    i = 0
    references_mode = False
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("*Integrated second working draft"):
            i += 1
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            if references_mode:
                out.append(r"\endgroup")
                references_mode = False
            number = re.match(r"\d+\.\s+(.*)", title)
            if number:
                out.append(r"\section{" + inline(number.group(1)) + "}")
            else:
                out.append(r"\section*{" + inline(title) + "}")
            if title == "References":
                out.append(r"\begingroup\small\raggedright\setlength{\parindent}{0pt}\setlength{\parskip}{0.35em}")
                references_mode = True
            i += 1
            continue
        if line.startswith("### "):
            title = re.sub(r"^\d+\.\d+\s+", "", line[4:].strip())
            out.append(r"\subsection{" + inline(title) + "}")
            i += 1
            continue
        if line.startswith("\\["):
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                i += 1
                if block[-1].strip() == r"\]":
                    break
            out.append("\n".join(block))
            continue
        if line.startswith("    "):
            block = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                block.append(lines[i][4:] if lines[i].startswith("    ") else "")
                i += 1
            out.append("\\begin{verbatim}\n" + "\n".join(block).rstrip() + "\n\\end{verbatim}")
            continue
        if line.startswith("| "):
            block = []
            while i < len(lines) and lines[i].startswith("| "):
                block.append(lines[i])
                i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines) or not lines[i].startswith("**Table "):
                raise ValueError("Table caption missing")
            caption = lines[i]
            number = int(re.search(r"\*\*Table (\d+)\.", caption).group(1))
            out.append(table_tex(block, caption, number))
            i += 1
            continue
        if line.startswith("!["):
            match = re.search(r"figure_(\d+)_", line)
            if not match:
                raise ValueError("Unknown figure: " + line)
            number = int(match.group(1))
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines) or not lines[i].startswith("**Figure "):
                raise ValueError("Figure caption missing")
            out.append(figure_tex(line, lines[i], number))
            i += 1
            continue
        if line.startswith("> "):
            out.append(r"\begin{quote}" + "\n" + inline(line[2:]) + "\n" + r"\end{quote}")
            i += 1
            continue
        block = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "| ", "![", "\\[", "> ", "    ")):
            block.append(lines[i].strip())
            i += 1
        paragraph = inline(" ".join(block)) + "\n"
        if references_mode:
            paragraph = r"\hangindent=1.5em\hangafter=1 " + paragraph
        out.append(paragraph)
    if references_mode:
        out.append(r"\endgroup")
    out.append("\\end{document}\n")
    TARGET.write_text("\n\n".join(out), encoding="utf-8")
    print(f"Wrote {TARGET} ({len(out)} blocks)")


if __name__ == "__main__":
    build()

