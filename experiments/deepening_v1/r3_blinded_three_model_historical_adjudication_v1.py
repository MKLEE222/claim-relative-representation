from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

try:
    import fitz
except Exception:
    raise SystemExit(
        "PyMuPDF is required. Install once with: python -m pip install pymupdf==1.26.4"
    )

MODELS_DEFAULT = ["qwen2.5:7b", "gemma3:12b", "llama3.1:8b"]
OLLAMA_URL_DEFAULT = "http://127.0.0.1:11434"
TEMPERATURE = 0
SEED = 20260927
NUM_CTX = 16384
NUM_PREDICT = 1600

SOURCES = {
    "1903": {
        "url": "https://archive.org/download/bookofsermarcopo001polo/bookofsermarcopo001polo.pdf",
        "sha256": "6f1d7f6040bf2e3333405f604f3231d1b97a4bb6c405343a28bc2d9fb335a3f7",
    },
    "1920": {
        "url": "https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf",
        "sha256": "dfa29f55b41714d79ac2c3107e3e23094e9dfc27114f53e7bf4a20147ba71941",
    },
}

CASES = {
    "R3R2-01": {
        "inquiry_id": "R3Q-PASH-STANCE",
        "episode": "Pashai",
        "question": "Which earlier proposition does Stein corroborate, and which does he challenge?",
        "pages": [
            ("1903", 461, "164"),
            ("1903", 462, "165"),
            ("1920", 47, "34"),
            ("1920", 48, "35"),
        ],
        "components": {
            "corroborated_target_identity": [
                "SOURCE_ATTRIBUTION_NON_EYEWITNESS",
                "ROUTE_NECESSITY",
                "OTHER",
                "UNRESOLVED",
            ],
            "corroboration_relation_direction": [
                "CORROBORATES",
                "CRITICIZES",
                "NEUTRAL",
                "OTHER",
                "UNRESOLVED",
            ],
            "challenged_target_identity": [
                "SOURCE_ATTRIBUTION_NON_EYEWITNESS",
                "ROUTE_NECESSITY",
                "OTHER",
                "UNRESOLVED",
            ],
            "challenge_relation_direction": [
                "CORROBORATES",
                "CRITICIZES",
                "NEUTRAL",
                "OTHER",
                "UNRESOLVED",
            ],
            "alternative_modality": [
                "ASSERTED_CERTAIN",
                "ALMOST_CERTAIN",
                "PROBABLE",
                "POSSIBLE",
                "OTHER",
                "UNRESOLVED",
            ],
            "later_actor_responsibility": [
                "STEIN_AS_REPORTED_BY_CORDIER",
                "CORDIER",
                "BOTH",
                "OTHER",
                "UNRESOLVED",
            ],
        },
    },
    "R3R2-02": {
        "inquiry_id": "R3Q-ARBR-COMMIT",
        "episode": "Arbre Sec",
        "question": "Whose commitment is the cypress identification, and does the inspected entry establish Cordier's adoption of it?",
        "pages": [
            ("1903", 408, "113"),
            ("1903", 425, "128"),
            ("1920", 44, "31"),
        ],
        "components": {
            "cypress_commitment_holder": [
                "HOUTUM_SCHINDLER",
                "CORDIER",
                "BOTH",
                "OTHER",
                "UNRESOLVED",
            ],
            "cordier_transmission_reply_role": [
                "TRANSMITS_AND_REPLIES",
                "ADOPTS",
                "REJECTS",
                "OTHER",
                "UNRESOLVED",
            ],
            "cordier_adoption_status": [
                "ESTABLISHED",
                "NOT_ESTABLISHED",
                "UNRESOLVED",
            ],
        },
    },
    "R3R2-03": {
        "inquiry_id": "R3Q-DES-EVIDENCE",
        "episode": "Great Desert",
        "question": "Which evidence in the 1920 discussion supports distance/marches, and which supports the local-folklore source attribution?",
        "pages": [
            ("1903", 501, "202"),
            ("1920", 61, "48"),
            ("1920", 62, "49"),
        ],
        "components": {
            "distance_marches_evidence_assignment": [
                "SURVEY_MEASUREMENTS",
                "LOCAL_FOLKLORE",
                "BOTH",
                "OTHER",
                "UNRESOLVED",
            ],
            "folklore_source_evidence_assignment": [
                "SURVEY_MEASUREMENTS",
                "LOCAL_FOLKLORE",
                "BOTH",
                "OTHER",
                "UNRESOLVED",
            ],
            "later_actor_source_responsibility": [
                "STEIN_AS_REPORTED_BY_CORDIER",
                "CORDIER",
                "BOTH",
                "OTHER",
                "UNRESOLVED",
            ],
            "proposition_specific_evidence_distinction": [
                "DISTINCT_BINDINGS",
                "SAME_EVIDENCE_FOR_BOTH",
                "OTHER",
                "UNRESOLVED",
            ],
        },
    },
    "R3R2-04": {
        "inquiry_id": "R3Q-URM-ERRATUM",
        "episode": "Urumtsi",
        "question": "What action description is changed by the 1920 erratum?",
        "pages": [
            ("1903", 500, "201"),
            ("1920", 63, "50"),
        ],
        "components": {
            "earlier_action_reading": [
                "FOUND",
                "FOUNDED",
                "OTHER",
                "UNRESOLVED",
            ],
            "replacement_action_reading": [
                "FOUND",
                "FOUNDED",
                "OTHER",
                "UNRESOLVED",
            ],
            "correction_direction": [
                "FOUND_TO_FOUNDED",
                "FOUNDED_TO_FOUND",
                "OTHER",
                "UNRESOLVED",
            ],
        },
    },
    "R3R2-05": {
        "inquiry_id": "R3Q-TUN-CONTROVERSY",
        "episode": "Tun-o-Kain",
        "question": "Does the 1920 entry present one settled route replacement or preserve competing positions?",
        "pages": [
            ("1903", 425, "128"),
            ("1920", 38, "25"),
            ("1920", 39, "26"),
            ("1920", 40, "27"),
            ("1920", 41, "28"),
            ("1920", 42, "29"),
            ("1920", 43, "30"),
        ],
        "components": {
            "controversy_resolution_state": [
                "COMPETING_POSITIONS",
                "SETTLED_REPLACEMENT",
                "OTHER",
                "UNRESOLVED",
            ],
            "sykes_relation_direction": [
                "REVISES_OR_CRITICIZES_YULE",
                "SUPPORTS_YULE",
                "NEUTRAL",
                "OTHER",
                "UNRESOLVED",
            ],
            "hedin_relation_direction": [
                "SUPPORTS_YULE",
                "SUPPORTS_SYKES_REVISION",
                "NEUTRAL",
                "OTHER",
                "UNRESOLVED",
            ],
            "hedin_modality": [
                "EXTREMELY_PROBABLE",
                "PROBABLE",
                "POSSIBLE",
                "ASSERTED_CERTAIN",
                "OTHER",
                "UNRESOLVED",
            ],
            "quoted_scholar_vs_editor_responsibility": [
                "SCHOLARS_AS_REPORTED_BY_CORDIER",
                "CORDIER_OWNS_POSITIONS",
                "MIXED",
                "OTHER",
                "UNRESOLVED",
            ],
        },
    },
}

PERTURBATIONS = ["P0_CANONICAL", "P1_SOURCES_FIRST", "P2_REVERSE_PAGE_ORDER"]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "claim-relative-representation-llm-review/1.0"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def post_json(url: str, payload: dict, timeout: int = 600) -> dict:
    raw = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=raw,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(url: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def token_norm(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def page_label(source_id: str, pdf_index: int, printed_page: str) -> str:
    return f"S{source_id}_PRINTED_{printed_page}_PDFINDEX_{pdf_index}"


def load_source_pages() -> tuple[dict, dict]:
    docs = {}
    metadata = {}
    for source_id, spec in SOURCES.items():
        raw = fetch(spec["url"])
        got = sha256(raw)
        if got != spec["sha256"]:
            raise RuntimeError(f"source drift for {source_id}: {got}")
        docs[source_id] = fitz.open(stream=raw, filetype="pdf")
        metadata[source_id] = {
            "url": spec["url"],
            "sha256": got,
            "page_count": len(docs[source_id]),
        }

    pages = {}
    for case in CASES.values():
        for source_id, pdf_index, printed_page in case["pages"]:
            label = page_label(source_id, pdf_index, printed_page)
            if label in pages:
                continue
            doc = docs[source_id]
            if pdf_index < 0 or pdf_index >= len(doc):
                raise RuntimeError(f"page index out of range: {source_id} {pdf_index}")
            text = doc[pdf_index].get_text()
            pages[label] = {
                "source_id": source_id,
                "pdf_index": pdf_index,
                "printed_page": printed_page,
                "text": text,
                "text_sha256": sha256(text.encode("utf-8")),
            }
    return pages, metadata


def component_schema(case: dict) -> dict:
    props = {}
    for key, allowed in case["components"].items():
        props[key] = {
            "type": "object",
            "additionalProperties": False,
            "required": ["value", "evidence_pages", "supporting_quote", "confidence"],
            "properties": {
                "value": {"enum": allowed},
                "evidence_pages": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string"},
                },
                "supporting_quote": {"type": "string", "maxLength": 350},
                "confidence": {"enum": ["HIGH", "MEDIUM", "LOW"]},
            },
        }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["components", "case_note"],
        "properties": {
            "components": {
                "type": "object",
                "additionalProperties": False,
                "required": list(case["components"].keys()),
                "properties": props,
            },
            "case_note": {"type": "string", "maxLength": 900},
        },
    }


def render_component_instructions(case: dict) -> str:
    rows = []
    for key, allowed in case["components"].items():
        rows.append(f"- {key}: choose exactly one of {allowed}")
    return "\n".join(rows)


def render_sources(case: dict, pages: dict, reverse: bool) -> str:
    items = list(case["pages"])
    if reverse:
        items = list(reversed(items))
    blocks = []
    for source_id, pdf_index, printed_page in items:
        label = page_label(source_id, pdf_index, printed_page)
        text = pages[label]["text"]
        blocks.append(
            f"### {label}\n"
            f"Source year: {source_id}\n"
            f"Printed page: {printed_page}\n"
            f"PDF index: {pdf_index}\n\n"
            f"{text}"
        )
    return "\n\n".join(blocks)


def build_prompt(case_id: str, perturbation: str, pages: dict) -> str:
    case = CASES[case_id]
    source_text = render_sources(
        case,
        pages,
        reverse=(perturbation == "P2_REVERSE_PAGE_ORDER"),
    )

    rules = """You are a blinded historical source adjudicator.

Use ONLY the supplied source-page text. Do not use outside knowledge, prior conversation, repository context, expected answers, or assumptions about the experiment.

For every atomic field:
1. choose exactly one allowed normalized value;
2. cite at least one supplied page label;
3. copy a short exact supporting phrase from the supplied source text, ideally 5-20 words;
4. give HIGH, MEDIUM, or LOW confidence.

If the source does not determine a field, choose UNRESOLVED. Do not infer editorial adoption merely from quotation, citation, inclusion, or transmission. Preserve qualification and uncertainty. Distinguish a quoted/reported scholar's position from the editor who transmits it.

Return only JSON matching the supplied schema."""

    question = (
        f"Case: {case_id} / {case['episode']}\n"
        f"Historical question: {case['question']}\n\n"
        "Atomic fields and allowed values:\n"
        + render_component_instructions(case)
    )

    if perturbation == "P1_SOURCES_FIRST":
        body = rules + "\n\nSOURCE PAGES\n\n" + source_text + "\n\nQUESTION AND FIELDS\n\n" + question
    else:
        body = rules + "\n\nQUESTION AND FIELDS\n\n" + question + "\n\nSOURCE PAGES\n\n" + source_text

    return body


def validate_result(case_id: str, parsed: dict, pages: dict) -> tuple[bool, list[str]]:
    case = CASES[case_id]
    errors = []
    if not isinstance(parsed, dict):
        return False, ["response is not an object"]
    components = parsed.get("components")
    if not isinstance(components, dict):
        return False, ["components missing"]

    valid_labels = {
        page_label(source_id, pdf_index, printed_page)
        for source_id, pdf_index, printed_page in case["pages"]
    }
    source_norm_by_label = {
        label: token_norm(pages[label]["text"])
        for label in valid_labels
    }

    for key, allowed in case["components"].items():
        obj = components.get(key)
        if not isinstance(obj, dict):
            errors.append(f"{key}: missing object")
            continue
        value = obj.get("value")
        if value not in allowed:
            errors.append(f"{key}: invalid value {value!r}")
        ev_pages = obj.get("evidence_pages")
        if not isinstance(ev_pages, list) or not ev_pages:
            errors.append(f"{key}: evidence_pages missing")
            ev_pages = []
        unknown = [x for x in ev_pages if x not in valid_labels]
        if unknown:
            errors.append(f"{key}: unknown evidence pages {unknown}")
        quote = obj.get("supporting_quote")
        if not isinstance(quote, str) or not quote.strip():
            errors.append(f"{key}: supporting_quote missing")
        else:
            qn = token_norm(quote)
            if len(qn.split()) < 2:
                errors.append(f"{key}: supporting_quote too short")
            elif ev_pages and not any(
                qn in source_norm_by_label.get(label, "")
                for label in ev_pages
            ):
                errors.append(f"{key}: quote not found in cited page text")
        if obj.get("confidence") not in {"HIGH", "MEDIUM", "LOW"}:
            errors.append(f"{key}: invalid confidence")

    extra = sorted(set(components) - set(case["components"]))
    if extra:
        errors.append(f"extra component keys: {extra}")

    return len(errors) == 0, errors


def available_models(ollama_url: str) -> set[str]:
    data = get_json(ollama_url.rstrip("/") + "/api/tags")
    names = set()
    for model in data.get("models", []):
        for key in ("name", "model"):
            value = model.get(key)
            if value:
                names.add(value)
    return names


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        nargs="+",
        default=MODELS_DEFAULT,
    )
    parser.add_argument(
        "--ollama-url",
        default=OLLAMA_URL_DEFAULT,
    )
    parser.add_argument(
        "--out-dir",
        default="experiments/deepening_v1/llm_second_pass_v1",
    )
    args = parser.parse_args()

    if args.models != MODELS_DEFAULT:
        raise SystemExit(
            "Protocol v1 freezes exactly these models: "
            + ", ".join(MODELS_DEFAULT)
        )

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    avail = available_models(args.ollama_url)
    missing = [m for m in args.models if m not in avail]
    if missing:
        raise SystemExit(
            "Frozen model(s) unavailable in Ollama: "
            + ", ".join(missing)
            + "\nAvailable: "
            + ", ".join(sorted(avail))
        )

    pages, source_meta = load_source_pages()

    calls = []
    for case_id in CASES:
        for perturbation in PERTURBATIONS:
            prompt = build_prompt(case_id, perturbation, pages)
            calls.append(
                {
                    "case_id": case_id,
                    "inquiry_id": CASES[case_id]["inquiry_id"],
                    "episode": CASES[case_id]["episode"],
                    "perturbation": perturbation,
                    "prompt": prompt,
                    "prompt_sha256": sha256(prompt.encode("utf-8")),
                    "schema": component_schema(CASES[case_id]),
                }
            )

    calls_path = out / "blind_calls_v1.jsonl"
    calls_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in calls) + "\n",
        encoding="utf-8",
    )

    freeze = {
        "protocol": "R3_BLINDED_THREE_MODEL_HISTORICAL_ADJUDICATION_PROTOCOL_v1",
        "models": args.models,
        "perturbations": PERTURBATIONS,
        "temperature": TEMPERATURE,
        "seed": SEED,
        "num_ctx": NUM_CTX,
        "num_predict": NUM_PREDICT,
        "source_meta": source_meta,
        "unique_source_pages": {
            label: {
                "source_id": rec["source_id"],
                "pdf_index": rec["pdf_index"],
                "printed_page": rec["printed_page"],
                "text_sha256": rec["text_sha256"],
            }
            for label, rec in sorted(pages.items())
        },
        "calls_sha256": sha256(calls_path.read_bytes()),
        "registered_answer_loaded_by_runner": False,
    }
    (out / "execution_freeze_v1.json").write_text(
        json.dumps(freeze, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    results_path = out / "raw_results_v1.jsonl"
    if results_path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing frozen results: {results_path}"
        )

    endpoint = args.ollama_url.rstrip("/") + "/api/generate"
    records = []

    total = len(args.models) * len(calls)
    done = 0
    for model in args.models:
        for call in calls:
            done += 1
            call_id = f"{model}::{call['case_id']}::{call['perturbation']}"
            print(f"[{done}/{total}] {call_id}", flush=True)
            payload = {
                "model": model,
                "prompt": call["prompt"],
                "stream": False,
                "format": call["schema"],
                "options": {
                    "temperature": TEMPERATURE,
                    "seed": SEED,
                    "num_ctx": NUM_CTX,
                    "num_predict": NUM_PREDICT,
                },
            }
            record = {
                "call_id": call_id,
                "model": model,
                "case_id": call["case_id"],
                "inquiry_id": call["inquiry_id"],
                "perturbation": call["perturbation"],
                "prompt_sha256": call["prompt_sha256"],
                "schema_valid": False,
                "validation_errors": [],
            }
            try:
                response = post_json(endpoint, payload)
                raw_response = response.get("response", "")
                record["ollama_done_reason"] = response.get("done_reason")
                record["raw_response"] = raw_response
                try:
                    parsed = json.loads(raw_response)
                    valid, errors = validate_result(
                        call["case_id"], parsed, pages
                    )
                    record["parsed"] = parsed
                    record["schema_valid"] = valid
                    record["validation_errors"] = errors
                except Exception as exc:
                    record["validation_errors"] = [
                        "JSON_PARSE_ERROR: " + repr(exc)
                    ]
            except Exception as exc:
                record["execution_error"] = repr(exc)
                record["validation_errors"] = [
                    "EXECUTION_ERROR: " + repr(exc)
                ]

            records.append(record)
            with results_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    result_bytes = results_path.read_bytes()
    summary = {
        "expected_calls": total,
        "observed_calls": len(records),
        "schema_valid_calls": sum(1 for r in records if r["schema_valid"]),
        "schema_invalid_calls": sum(1 for r in records if not r["schema_valid"]),
        "raw_results_sha256": sha256(result_bytes),
        "all_calls_completed": len(records) == total,
        "registered_answer_loaded_by_runner": False,
    }
    (out / "runner_summary_v1.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))
    if summary["schema_invalid_calls"]:
        print(
            "Run completed with invalid calls. Do not retune prompts. "
            "Analyze as frozen execution failure/sensitivity.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
