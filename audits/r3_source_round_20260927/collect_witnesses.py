"""Materialize witnesses, not historical judgments. No OCR or LLM invocation."""
from __future__ import annotations
import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path
import fitz

OUT = Path('audits/r3_source_round_20260927/generated')
SOURCES = {
    'pg10636.txt': ('https://www.gutenberg.org/cache/epub/10636/pg10636.txt', '7b0cbb0bc47a48d7594314b56d890e3e43ac05666b8c70d98f10719501cf6fb5'),
    'pg12410.txt': ('https://www.gutenberg.org/cache/epub/12410/pg12410.txt', 'c1ce61dd8c6c6a326c42fb7ac3b1a63767bf1685ec88354f83dd321e1748921c'),
    'cordier_1920.pdf': ('https://resources.warburg.sas.ac.uk/pdf/ndb90b2753728.pdf', None),
    'yule_1903_v1.pdf': ('https://archive.org/download/bookofsermarcopo001polo/bookofsermarcopo001polo.pdf', None),
}
QUERIES = {
    'tree': ('tree described',),
    'schindler': ('schindler',),
    'pashai': ('personally', 'visited'),
    'route': ('tabbas', 'suppose'),
    'goblins': ('goblins', 'peculiar'),
    'folklore': ('folklore', 'spot'),
    'polo_annals': ('pauthier', 'commissioner'),
}

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def fetch(url: str) -> bytes:
    last = None
    for attempt in range(2):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'CRR-source-audit/1.0'})
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except Exception as exc:
            last = exc
            time.sleep(2)
    raise RuntimeError(str(last))

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = {'role': 'source_materialization_only', 'visual_verification_performed_by_script': False,
              'pymupdf': fitz.VersionBind, 'sources': []}
    for name, (url, expected) in SOURCES.items():
        rec = {'source_id': name, 'url': url, 'expected_sha256': expected}
        try:
            raw = fetch(url)
            rec.update(bytes=len(raw), sha256=sha(raw))
            if expected is not None and sha(raw) != expected:
                rec['status'] = 'HASH_MISMATCH'
                ledger['sources'].append(rec)
                continue
            if name.endswith('.txt'):
                (OUT / name).write_bytes(raw)
                rec['status'] = 'FROZEN_TEXT_MATCH'
            else:
                doc = fitz.open(stream=raw, filetype='pdf')
                texts = [page.get_text() for page in doc]
                rec['page_count'] = len(doc)
                hits = {}
                for key, terms in QUERIES.items():
                    hits[key] = [i for i, text in enumerate(texts)
                                 if all(t in ' '.join(text.lower().split()) for t in terms)]
                rec['anchor_page_indices_0_based'] = hits
                if name == 'cordier_1920.pdf':
                    selected = set(range(16, 27)) | set(range(36, 45)) | {47, 48, 61, 62}
                    (OUT / name).write_bytes(raw)
                else:
                    selected = {0, 8, 10, 12}
                    for indices in hits.values():
                        for i in indices[:10]:
                            selected.update(range(max(0, i-1), min(len(doc), i+2)))
                selected = sorted(i for i in selected if i < len(doc))
                page_records = []
                extract = fitz.open()
                for i in selected:
                    extract.insert_pdf(doc, from_page=i, to_page=i)
                    page_records.append({'extract_page_1_based': len(page_records)+1,
                                         'source_page_index_0_based': i,
                                         'text': texts[i]})
                stem = name.removesuffix('.pdf')
                extract.save(OUT / (stem + '_selected_pages.pdf'), garbage=4, deflate=True)
                (OUT / (stem + '_page_text.json')).write_text(json.dumps(page_records, ensure_ascii=False, indent=2), encoding='utf-8')
                rec['selected_page_indices_0_based'] = selected
                rec['status'] = 'PDF_MATERIALIZED_NOT_VISUALLY_VERIFIED'
            print(name, rec['status'], rec['sha256'], flush=True)
        except Exception as exc:
            rec.update(status='BLOCKED_SOURCE_FETCH_OR_PARSE', error=str(exc))
            print(name, rec['status'], str(exc), flush=True)
        ledger['sources'].append(rec)
    (OUT / 'source_materialization.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')
    print('NO_RETRIEVAL_OR_JUDGE_OUTCOME_COMPUTED', flush=True)

if __name__ == '__main__':
    main()
