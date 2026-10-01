from __future__ import annotations

import collections
import hashlib
import io
import itertools
import json
import re
import sys
import tarfile
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path('audits/cold_start_20260926/generated')
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = OUT / 'sources'
SOURCES.mkdir(exist_ok=True)
PROVENANCE = []


def download(name, url, expected_blob=None):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'CRR-claim-audit/1.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read()
            break
        except Exception as exc:
            last = exc
            if attempt == 2:
                raise RuntimeError(f'BLOCKED_TRANSPORT {name}: {last}') from exc
            time.sleep(2 ** attempt)
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if expected_blob and blob != expected_blob:
        raise RuntimeError(f'SOURCE_IDENTITY_FAILURE {name}: {blob}')
    (SOURCES / name).write_bytes(data)
    PROVENANCE.append({'file': name, 'url': url, 'bytes': len(data),
                       'sha256': hashlib.sha256(data).hexdigest(), 'git_blob_sha1': blob})
    return data


def local(tag):
    return tag.rsplit('}', 1)[-1]


def normalized(text, mode):
    if mode != 'raw':
        text = re.sub(r'<[^>]*>', '', text)
    if mode == 'stripped_case_amp':
        text = text.casefold().replace('&', 'and')
    return ' '.join(text.split())


def canonical(groups):
    return tuple(sorted(tuple(sorted(set(group))) for group in groups if group))


def frankenstein():
    url = ('https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/'
           '5a208f869ff1213defa000e3181d5315a072a15f/'
           'collationChunks/C18/output/Collation_C18-complete.xml')
    raw = download('frankenstein_C18.xml', url, 'bca0548912ab1d7b2676360d33a6468290296d7e')
    root = ET.fromstring(raw)
    apps = [e for e in root.iter() if local(e.tag) == 'app']
    modes = {m: {'mismatches': 0, 'within_group_splits': 0, 'between_group_merges': 0,
                 'examples': []} for m in ('raw', 'stripped', 'stripped_case_amp')}
    multiple_groups = 0
    missing_witness = 0
    duplicate_witness_apps = 0
    for ai, app in enumerate(apps):
        groups, records, descriptors = [], [], []
        for child in app:
            if local(child.tag) not in {'rdgGrp', 'rdg'}:
                continue
            gid = len(groups)
            readings = ([child] if local(child.tag) == 'rdg' else
                        [x for x in child.iter() if local(x.tag) == 'rdg'])
            witness_group = []
            descriptors.append(child.attrib.get('n'))
            for reading in readings:
                ids = tuple(sorted(reading.attrib.get('wit', '').split()))
                missing_witness += not bool(ids)
                witness_group.extend(ids)
                records.append((gid, ids, ''.join(reading.itertext())))
            groups.append(witness_group)
        reference = canonical(groups)
        multiple_groups += len(reference) > 1
        flattened_ids = [w for _, ids, _ in records for w in ids]
        duplicate_witness_apps += len(flattened_ids) != len(set(flattened_ids))
        for mode, metric in modes.items():
            by_text = collections.defaultdict(list)
            texts_in_group = collections.defaultdict(set)
            groups_for_text = collections.defaultdict(set)
            for gid, ids, text in records:
                key = normalized(text, mode)
                by_text[key].extend(ids)
                texts_in_group[gid].add(key)
                groups_for_text[key].add(gid)
            decoded = canonical(by_text.values())
            split = any(len(v) > 1 for v in texts_in_group.values())
            merge = any(len(v) > 1 for v in groups_for_text.values())
            metric['within_group_splits'] += split
            metric['between_group_merges'] += merge
            if decoded != reference:
                metric['mismatches'] += 1
                if len(metric['examples']) < 4:
                    metric['examples'].append({'app_index_zero_based': ai,
                        'native_partition': reference, 'decoded_partition': decoded,
                        'native_normalization_descriptors': descriptors,
                        'readings': [{'witness': ids, 'raw': text[:450],
                                      'normalized': normalized(text, mode)[:450]}
                                     for _, ids, text in records]})
    return {'app_units': len(apps), 'multi_group_apps': multiple_groups,
            'missing_witness_readings': missing_witness,
            'duplicate_witness_apps': duplicate_witness_apps, 'decoders': modes,
            'scope': 'Post-result diagnostics; neither a new holdout nor the full project normalizer. Failure of one decoder is not an information-impossibility proof.'}


def ambiguity(rows, key_function, value_function):
    groups = collections.defaultdict(set)
    group_rows = collections.Counter()
    for row in rows:
        key = key_function(row)
        groups[key].add(value_function(row))
        group_rows[key] += 1
    ambiguous = {k: v for k, v in groups.items() if len(v) > 1}
    return {'keys': len(groups), 'ambiguous_keys': len(ambiguous),
            'records_at_ambiguous_keys': sum(group_rows[k] for k in ambiguous),
            'examples': [{'key': k, 'values': sorted(v, key=repr)}
                         for k, v in sorted(ambiguous.items(), key=lambda item: repr(item[0]))[:5]]}


def whitman():
    url = ('https://raw.githubusercontent.com/whitmanarchive/whitman-LG_1855_variorum/'
           '25a00b7ebbdbc5246fce65a333bc761a5c22dad4/source/authority/anc.02134.xml')
    raw = download('whitman_anc02134.xml', url)
    root = ET.fromstring(raw)
    ns = {'t': 'http://www.tei-c.org/ns/1.0'}
    records, malformed = [], []
    total_links, missing_file = 0, 0
    for gi, group in enumerate(root.findall('.//t:linkGrp[@type="relation"]', ns)):
        file_id = group.attrib.get('corresp', '')
        for li, link in enumerate(group.findall('./t:link', ns)):
            total_links += 1
            tokens = link.attrib.get('target', '').split()
            if len(tokens) != 2:
                malformed.append({'group': gi, 'link': li, 'target': tokens})
                continue
            missing_file += not bool(file_id)
            records.append({'print': tokens[0], 'local': tokens[1], 'file': file_id,
                            'cert': link.attrib.get('cert', '')})
    result = {'links': total_links, 'valid_records': len(records),
              'malformed': malformed, 'missing_file_records': missing_file}
    for name, fields in [('local', ('local',)), ('print_local', ('print', 'local')),
                         ('print_local_cert', ('print', 'local', 'cert'))]:
        result[name + '_to_file'] = ambiguity(records, lambda r: tuple(r[f] for f in fields),
                                               lambda r: r['file'])
    result['scope'] = 'Observed mapping ambiguity only. Uniqueness does not supply a lawful decoder, and absence of a field does not by itself prove minimality.'
    return result


def scc(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
    index, low, stack, on_stack, components = {}, {}, [], set(), []
    def visit(v):
        index[v] = low[v] = len(index)
        stack.append(v)
        on_stack.add(v)
        for w in sorted(adjacency[v]):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            component = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.add(w)
                if w == v:
                    break
            components.append(component)
    for v in sorted(vertices):
        if v not in index:
            visit(v)
    return components


def faust():
    url = 'https://codeload.github.com/faustedition/faust-xml/tar.gz/502eca65120dd6189ceaf41d4e5017775e6e4677'
    raw = download('faust_xml.tar.gz', url)
    ns = {'f': 'http://www.faustedition.net/ns'}
    records, parse_failures = [], []
    xml_files = multiple_source_relations = underspecified = 0
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        for member in archive.getmembers():
            if not member.isfile() or '/xml/macrogenesis/' not in member.name or not member.name.endswith('.xml'):
                continue
            xml_files += 1
            name = member.name.split('/', 1)[1]
            stream = archive.extractfile(member)
            if stream is None:
                raise RuntimeError('Cannot read archive member ' + name)
            try:
                root = ET.fromstring(stream.read())
            except ET.ParseError as exc:
                parse_failures.append({'file': name, 'error': str(exc)})
                continue
            for ri, relation in enumerate(root.findall('.//f:relation[@name="temp-pre"]', ns)):
                items = tuple(x.attrib.get('uri', '') for x in relation.findall('./f:item', ns))
                if len(items) < 2 or not all(items):
                    underspecified += 1
                    continue
                source_elements = relation.findall('./f:source', ns)
                sources = tuple(sorted(set(s.attrib.get('uri', '') for s in source_elements if s.attrib.get('uri'))))
                multiple_source_relations += len(source_elements) > 1
                records.append({'file': name, 'relation_index': ri, 'items': items,
                                'sources': sources,
                                'first_source': source_elements[0].attrib.get('uri') if source_elements else None})
    edges = []
    for record in records:
        for a, b in zip(record['items'], record['items'][1:]):
            edges.append(dict(record, edge=(a, b)))
    vertices = {v for e in edges for v in e['edge']}
    components = [c for c in scc(vertices, {e['edge'] for e in edges}) if len(c) > 1]
    membership = {v: i for i, c in enumerate(components) for v in c}
    conflict_edges = [e for e in edges if e['edge'][0] in membership and
                      membership[e['edge'][0]] == membership.get(e['edge'][1])]
    result = {'xml_files': xml_files, 'parse_failures': parse_failures,
              'relations': len(records), 'underspecified_relations': underspecified,
              'relations_with_multiple_source_elements': multiple_source_relations,
              'relations_without_source_uri': sum(not r['sources'] for r in records),
              'directed_constraint_occurrences': len(edges),
              'unique_directed_constraints': len({e['edge'] for e in edges}),
              'nodes': len(vertices), 'nontrivial_scc': len(components),
              'conflict_nodes': len(membership), 'conflict_edge_occurrences': len(conflict_edges),
              'unique_conflict_edges': len({e['edge'] for e in conflict_edges})}
    result['file_to_source_set'] = ambiguity(records, lambda r: r['file'], lambda r: r['sources'])
    result['file_items_to_source_set'] = ambiguity(records, lambda r: (r['file'], r['items']), lambda r: r['sources'])
    result['conflict_file_to_source_set'] = ambiguity(conflict_edges, lambda r: r['file'], lambda r: r['sources'])
    result['conflict_file_edge_to_source_set'] = ambiguity(conflict_edges, lambda r: (r['file'], r['edge']), lambda r: r['sources'])
    result['scope'] = 'Conditional source-set variation is not yet certified recovery or global necessity; full retained projection and source-authorized decoder must be specified.'
    return result


def grounded(nodes, edges):
    current = set()
    while True:
        defended = {x for x in nodes if all(any((z, y) in edges for z in current)
                    for y in nodes if (y, x) in edges)}
        if current == defended:
            return current
        current = defended


def formal_sensitivity():
    nodes = {0, 1, 2}
    variants = {
        'directed_archival_stance_chain': {(1, 0), (2, 1)},
        'mutual_base_rebuttal': {(1, 0), (0, 1), (2, 1)},
        'mutual_rebuttal_and_counter_rebuttal': {(1, 0), (0, 1), (2, 1), (1, 2)},
    }
    result = {}
    for name, edges in variants.items():
        result[name] = {}
        for state, active in [('without_PM03', {0, 1}), ('with_PM03', nodes)]:
            active_edges = {(a, b) for a, b in edges if a in active and b in active}
            inside = grounded(active, active_edges)
            outside = {b for a, b in active_edges if a in inside}
            undecided = active - inside - outside
            result[name][state] = {'IN': sorted(inside), 'OUT': sorted(outside),
                                  'UNDECIDED': sorted(undecided),
                                  'focal_status': 'IN' if 0 in inside else 'OUT' if 0 in outside else 'UNDECIDED'}
    possible_edges = list(itertools.product(sorted(nodes), repeat=2))
    checked = 0
    for mask in range(1 << len(possible_edges)):
        edges = {e for i, e in enumerate(possible_edges) if mask & (1 << i)}
        complete = []
        for bits in range(1 << len(nodes)):
            subset = {i for i in nodes if bits & (1 << i)}
            if any(a in subset and b in subset for a, b in edges):
                continue
            acceptable = {x for x in nodes if all(any((z, y) in edges for z in subset)
                          for y in nodes if (y, x) in edges)}
            if acceptable == subset:
                complete.append(subset)
        least = set.intersection(*complete)
        if least != grounded(nodes, edges):
            raise AssertionError('Grounded checker disagrees on graph ' + str(mask))
        checked += 1
    return {'mapping_sensitivity': result, 'independent_definition_checks': checked,
            'scope': 'Illustrative model-mapping sensitivity, not new historical adjudication. Graph alternatives require source-level justification before use.'}


def main():
    result = {'status': 'POST_RESULT_DIAGNOSTIC', 'base_commit': '3f4f31792a59bdb2d1a2bd57893f417d2d3c6a07'}
    for name, function in [('frankenstein', frankenstein), ('whitman', whitman), ('faust', faust), ('formal', formal_sensitivity)]:
        result[name] = function()
        (OUT / 'audit_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    result['source_provenance'] = PROVENANCE
    (OUT / 'audit_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
