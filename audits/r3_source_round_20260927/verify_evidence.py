"""Verify provenance/coverage bindings, not historical interpretation. Run on unpacked delivery bundle."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bundle', type=Path, required=True)
ROOT = parser.parse_args().bundle.resolve()

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def load(name: str):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def main() -> None:
    material = load('source_materialization.json')
    expected = {x['source_id']: x['sha256'] for x in material['sources'] if 'sha256' in x}
    raw = {k: (ROOT / 'sources' / k).read_bytes() for k in ('pg10636.txt', 'pg12410.txt')}
    assert all(sha(v) == expected[k] for k, v in raw.items()), 'Source hash drift'
    text = {k: v.decode('utf-8') for k, v in raw.items()}  # Keep original CRLF offsets.
    anchors = load('exact_anchors.json')['anchors']
    ids = set()
    pages = load('page_review_manifest.json')['pages']
    reviewed = {(p['year'], p['pdf_page_index_0_based']) for p in pages}
    for a in anchors:
        assert a['anchor_id'] not in ids
        ids.add(a['anchor_id'])
        source = a['source_file']
        assert a['source_sha256'] == expected[source]
        excerpt = text[source][a['char_start']:a['char_end']]
        assert excerpt == a['raw_excerpt'], a['anchor_id']
        assert sha(excerpt.encode('utf-8')) == a['raw_excerpt_sha256']
        for p in a['visual_pages']:
            assert (p['year'], p['pdf_page_index_0_based']) in reviewed
    for p in pages:
        assert sha((ROOT / p['page_image_file']).read_bytes()) == p['png_sha256']
    frame = load('frozen_frame_intervals.json')['entries']
    assert len(frame) == len({e['entry_id'] for e in frame}) == 223
    for e in load('reviewed_entry_texts.json')['entries']:
        assert sha(e['entry_text'].encode('utf-8')) == e['entry_sha256']
        assert ' '.join(text['pg12410.txt'][e['source_start']:e['source_end']].split()) == e['entry_text']
    coverage = load('frame_coverage_audit.json')
    s = text['pg12410.txt']
    start = re.search(r'SER\s+MARCO\s+POLO\s+NOTES\s+AND\s+ADDENDA\s+TO\s+SIR\s+HENRY\s+YULE', s, re.I).start()
    found = [start + m.start() for m in re.finditer(r'(?m)^Introduction,\s*p{1,2}\.[^\n]*', s[start:])]
    assert found == [h['source_char_start'] for h in coverage['omissions']]
    for h in coverage['omissions']:
        assert s[h['source_char_start']:h['source_char_end']] == h['head']
        actual = [e['entry_id'] for e in frame if e['source_start'] <= h['source_char_start'] < e['source_end']]
        assert actual == h['covered_by_frozen_entries'] == []
    contrasts = load('proposition_contrasts.json')['observations']
    for c in contrasts:
        assert set(c['support_anchor_ids']) <= ids
        assert c['evidence_authority'] == 'AI_ASSISTED_SOURCE_CONTRAST_WITH_PAGE_IMAGES'
    if (ROOT / 'delivery_manifest.json').exists():
        for f in load('delivery_manifest.json')['files']:
            assert sha((ROOT / f['path']).read_bytes()) == f['sha256'], f['path']
    result = {
        'status': 'PROVENANCE_AND_COVERAGE_BINDINGS_VALIDATED',
        'exact_anchors_checked': len(anchors), 'reviewed_images_hash_checked': len(pages),
        'old_frame_intervals_checked': len(frame), 'uncovered_introduction_heads': len(found),
        'historical_observations_reference_checked': len(contrasts),
        'historical_semantic_correctness_proven_by_script': False,
        'independent_human_adjudication': False, 'new_llm_calls': 0, 'new_retrieval_runs': 0,
    }
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
