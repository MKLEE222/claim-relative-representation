from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from pathlib import Path

import fitz

OUT = Path("experiments/deepening_v1/reviewer_bundle_v1")
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "1903": {
        "url": "https://archive.org/download/bookofsermarcopo001polo/bookofsermarcopo001polo.pdf",
        "sha256": "6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7",
        "pages": [408, 425, 461, 462, 500, 501],
    },
    "1920": {
        "url": "https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf",
        "sha256": "dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941",
        "pages": [38, 39, 40, 41, 42, 43, 44, 47, 48, 61, 62, 63],
    },
}

CASES = [
    (
        "R3R2-01",
        "Pashai",
        "Which earlier proposition does Stein corroborate, and which does he challenge?",
        [("1903", 461, "164"), ("1903", 462, "165"), ("1920", 47, "34"), ("1920", 48, "35")],
    ),
    (
        "R3R2-02",
        "Arbre Sec",
        "Whose commitment is the cypress identification, and does the inspected entry establish Cordier's adoption of it?",
        [("1903", 408, "113"), ("1903", 425, "128"), ("1920", 44, "31")],
    ),
    (
        "R3R2-03",
        "Great Desert",
        "Which evidence in the 1920 discussion supports distance/marches, and which supports the local-folklore source attribution?",
        [("1903", 501, "202"), ("1920", 61, "48"), ("1920", 62, "49")],
    ),
    (
        "R3R2-04",
        "Urumtsi",
        "What action description is changed by the 1920 erratum?",
        [("1903", 500, "201"), ("1920", 63, "50")],
    ),
    (
        "R3R2-05",
        "Tun-o-Kain",
        "Does the 1920 entry present one settled route replacement or preserve competing positions?",
        [
            ("1903", 425, "128"),
            ("1920", 38, "25"),
            ("1920", 39, "26"),
            ("1920", 40, "27"),
            ("1920", 41, "28"),
            ("1920", 42, "29"),
            ("1920", 43, "30"),
        ],
    ),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "claim-relative-representation-review-bundle/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


source_meta = {}
page_files = {}

for source_id, spec in SOURCES.items():
    raw = fetch(spec["url"])
    got = digest(raw)
    if got != spec["sha256"]:
        raise RuntimeError(f"{source_id} source drift: {got}")
    doc = fitz.open(stream=raw, filetype="pdf")
    source_meta[source_id] = {
        "url": spec["url"],
        "sha256": got,
        "page_count": len(doc),
        "selected_pdf_indices_0_based": spec["pages"],
    }

    for page_index in spec["pages"]:
        if page_index < 0 or page_index >= len(doc):
            raise RuntimeError(
                f"{source_id} page index out of range: {page_index}"
            )
        page = doc[page_index]
        stem = f"{source_id}_pdfindex_{page_index:04d}"

        png_path = OUT / (stem + ".png")
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        pix.save(png_path)

        text_path = OUT / (stem + ".txt")
        text_path.write_text(page.get_text(), encoding="utf-8")

        if png_path.stat().st_size < 10000:
            raise RuntimeError(f"suspiciously small render: {png_path}")

        page_files[(source_id, page_index)] = {
            "png": png_path.name,
            "text": text_path.name,
        }

manifest_rows = []
for review_id, episode, question, pages in CASES:
    for source_id, page_index, printed_page in pages:
        record = page_files[(source_id, page_index)]
        manifest_rows.append(
            {
                "review_id": review_id,
                "episode": episode,
                "question": question,
                "source_year": source_id,
                "printed_page": printed_page,
                "pdf_index_0_based": page_index,
                "page_image": record["png"],
                "page_text": record["text"],
            }
        )

with (OUT / "CASE_PAGE_MANIFEST.csv").open(
    "w", newline="", encoding="utf-8"
) as handle:
    writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0]))
    writer.writeheader()
    writer.writerows(manifest_rows)

readme = [
    "# R3 Independent Historical Second-Pass Review Bundle v1",
    "",
    "Status: BLINDED SOURCE MATERIAL. REGISTERED ANSWERS AND COMPUTATIONAL OUTCOMES ARE NOT INCLUDED.",
    "",
    "## Reviewer instruction",
    "",
    "Answer each case from the supplied source pages.",
    "You are not being asked to validate the authors' ontology or computational experiments.",
    "If the inspected source does not support a determinate answer, return UNRESOLVED.",
    "Do not infer endorsement merely from quotation, inclusion, citation, or editorial transmission.",
    "",
    "Use the PNG page images as the authoritative source witness.",
    "The TXT files are navigation/accessibility extracts from the same PDF page.",
    "",
    "## Cases",
    "",
]

for review_id, episode, question, pages in CASES:
    readme.extend(
        [
            "### " + review_id + " - " + episode,
            "",
            question,
            "",
            "Inspect:",
        ]
    )
    for source_id, page_index, printed_page in pages:
        filename = page_files[(source_id, page_index)]["png"]
        readme.append(
            "- "
            + source_id
            + ", printed p. "
            + printed_page
            + ", PDF index "
            + str(page_index)
            + ": "
            + filename
        )
    readme.append("")

readme.extend(
    [
        "## Required response fields",
        "",
        "For each case provide:",
        "1. ordinary historical-prose answer;",
        "2. exact supporting phrase(s) or local span(s);",
        "3. responsible actor/source for each proposition distinguished;",
        "4. modality/uncertainty, if present;",
        "5. confidence: HIGH / MEDIUM / LOW;",
        "6. unresolved ambiguity or alternative reading, if any.",
        "",
        "## Independence declaration",
        "",
        "Record reviewer name or anonymized reviewer ID, completion date,",
        "whether you saw the authors' registered answers before review (YES/NO),",
        "whether you helped construct the five inquiry questions or computational projections (YES/NO),",
        "and any additional sources consulted.",
        "",
        "A review qualifies for the current gate only if the reviewer had not seen the registered answers",
        "and did not construct the proposition panel or controlled projection outcomes.",
    ]
)

(OUT / "README_REVIEWER.md").write_text(
    "\n".join(readme), encoding="utf-8"
)

form = [
    "# R3 Independent Review Response Form v1",
    "",
    "Reviewer ID:",
    "Date completed:",
    "Saw registered answers before review (YES/NO):",
    "Participated in inquiry/projection construction (YES/NO):",
    "Additional sources consulted:",
    "",
]

for review_id, episode, question, _ in CASES:
    form.extend(
        [
            "## " + review_id + " - " + episode,
            "",
            "Question: " + question,
            "",
            "Answer:",
            "",
            "Supporting source phrase(s)/span(s):",
            "",
            "Responsible actor/source per proposition:",
            "",
            "Modality/uncertainty:",
            "",
            "Confidence (HIGH/MEDIUM/LOW):",
            "",
            "Unresolved ambiguity / alternative reading:",
            "",
            "---",
            "",
        ]
    )

(OUT / "RESPONSE_FORM.md").write_text(
    "\n".join(form), encoding="utf-8"
)

(OUT / "SOURCE_HASHES.json").write_text(
    json.dumps(source_meta, indent=2), encoding="utf-8"
)

forbidden = [
    "required_output",
    "required_bindings",
    "r3_verified_proposition_panel",
    "proposition_binding_repair",
    "proposition_binding_separation",
    "target_rank=65",
    "selective_repair_pass",
]

text_files = [
    path
    for path in OUT.iterdir()
    if path.suffix.lower() in {".md", ".txt", ".csv", ".json"}
]
combined = "\n".join(
    path.read_text(encoding="utf-8", errors="replace").lower()
    for path in text_files
)

for token in forbidden:
    if token.lower() in combined:
        raise RuntimeError(
            f"answer-side leakage token found in bundle: {token}"
        )

checks = []
for path in sorted(OUT.iterdir()):
    if path.is_file():
        checks.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )

(OUT / "BUNDLE_CHECKSUMS.json").write_text(
    json.dumps(checks, indent=2), encoding="utf-8"
)

print("R3_SECOND_PASS_REVIEW_BUNDLE_V1")
print("source_1903_sha256=" + source_meta["1903"]["sha256"])
print("source_1920_sha256=" + source_meta["1920"]["sha256"])
print("unique_page_images=" + str(len(page_files)))
print("case_page_links=" + str(len(manifest_rows)))
print("registered_answer_files_included=0")
print("answer_side_leakage_check=PASS")
print("REVIEW_MATERIAL_ENGINEERING=COMPLETE")
print("INDEPENDENT_SECOND_PASS=NOT_COMPLETE")
