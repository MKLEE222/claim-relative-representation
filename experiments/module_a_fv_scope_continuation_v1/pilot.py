"""Post-inspection, source-grounded C18 continuation pilot. No LLM or new gold.
Uses all native apparatus units. Local snapshots omit their global ordinal;
source-linked baselines retain that ordinal and charge source reopening.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,re,sys,urllib.request
from pathlib import Path
from lxml import etree as E

PIN='5a208f869ff1213defa000e3181d5315a072a15f'
APP_PATH='collationChunks/C18/output/Collation_C18-complete.xml'
MS_PATH='collationChunks/C18/msColl_C18.xml'
EXPECTED={APP_PATH:'bca0548912ab1d7b2676360d33a6468290296d7e',MS_PATH:'8e537331ebf46dd4f013da9afcbe38c14092b6fd'}

def canonical(value: object) -> bytes:
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def name(e): return E.QName(e).localname

def xmlparse(raw): return E.fromstring(raw,E.XMLParser(collect_ids=False,resolve_entities=False,no_network=True))
def valid_fragment(raw: str): return xmlparse(('<unit>'+raw.replace('&','&amp;')+'</unit>').encode())
def no_space(s): return re.sub(r'\s+','',s)

def current_view(app) -> dict:
    return {'app_attributes':dict(app.attrib),'namespace_bindings':app.nsmap,
      'children':[{'tag':name(g),'attrs':dict(g.attrib),
                   'readings':[{'tag':name(r),'attrs':dict(r.attrib),'raw':''.join(r.itertext())} for r in g]} for g in app]}

def current_answer(view) -> list:
    # Recover the published normalized comparison, not independent literary truth.
    return [{'normalized_descriptor':g['attrs'].get('n'),
             'witnesses':[r['attrs'].get('wit') for r in g['readings']]} for g in view['children']]

class ScopeParser:
    def __init__(self,initial=None):
        self.active=dict(initial or {}); self.spans={}; self.segments=[]; self.events=[]; self.unit=None
    def text(self,s):
        if s:
            if s.strip(): self.segments.append({'text':s,'unit':self.unit,'active_ids':list(self.active),
                 'scope_attributes':{k:dict(v) for k,v in self.active.items()}})
            for sid in self.active:
                if sid in self.spans: self.spans[sid]['texts'].append(s)
    def walk(self,node):
        tag=name(node)
        if tag=='sga-add':
            start,end=node.get('sID'),node.get('eID')
            if bool(start)==bool(end): raise ValueError('ambiguous addition marker')
            if start:
                if start in self.active or start in self.spans: raise ValueError('duplicate start '+start)
                attrs=dict(node.attrib); self.active[start]=attrs
                self.spans[start]={'attrs':attrs,'start_unit':self.unit,'end_unit':None,'texts':[]}
                self.events.append(('start',start,self.unit,attrs))
            else:
                if end not in self.active: raise ValueError('unbound close '+end)
                self.active.pop(end)
                if end in self.spans: self.spans[end]['end_unit']=self.unit
                self.events.append(('end',end,self.unit,dict(node.attrib)))
        self.text(node.text)
        for child in node:
            self.walk(child); self.text(child.tail)
    def feed(self,node,unit): self.unit=unit; self.walk(node)

def signature(segments):
    # Preserve what kind of annotation covers EACH text segment. Whitespace is
    # not a historical target. Missing hand never implies any particular author.
    labels=[]
    for s in segments:
        if not s['text'].strip(): continue
        attrs=s['scope_attributes']
        state=tuple(sorted((v.get('place','NOT_ENCODED'),v.get('hand','NOT_ENCODED')) for v in attrs.values()))
        labels.append((no_space(s['text']),state))
    return labels

def coarse(segments):
    states={bool(s['active_ids']) for s in segments if s['text'].strip()}
    return 'NO_TEXT' if not states else 'MIXED' if len(states)>1 else 'INSIDE_ENCODED_ADDITION' if True in states else 'OUTSIDE_ENCODED_ADDITION'

def lexical_check(raws):
    """Independent scanner: build global intervals, do containment after parsing;
    does not use ScopeParser's active stack or any computed gold labels.
    """
    offsets=[]; pos=0; all_raw=[]
    for raw in raws: offsets.append(pos); all_raw.append(raw); pos+=len(raw)
    text=''.join(all_raw); starts={}; intervals={}; markers=[]
    tagre=re.compile(r'<[^>]*>')
    for m in tagre.finditer(text):
        if not m.group().startswith('<sga-add'): continue
        e=xmlparse(m.group().replace('&','&amp;').encode())
        if e.get('sID'):
            sid=e.get('sID'); assert sid not in starts; starts[sid]=(m.end(),dict(e.attrib))
        elif e.get('eID'):
            sid=e.get('eID'); lo,attrs=starts.pop(sid); intervals[sid]=(lo,m.start(),attrs)
    assert not starts
    byunit=[]
    for raw,off in zip(raws,offsets):
        segments=[]; last=0
        for m in list(tagre.finditer(raw))+[None]:
            end=len(raw) if m is None else m.start(); part=raw[last:end]
            if part.strip():
                lo,hi=off+last,off+end
                ids=[sid for sid,(a,b,_) in intervals.items() if a<=lo and hi<=b]
                segments.append({'text':part,'active_ids':ids,'scope_attributes':{sid:intervals[sid][2] for sid in ids}})
            if m is not None: last=m.end()
        byunit.append(segments)
    return byunit,intervals

def main():
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,default=Path(__file__).with_name('sources'));p.add_argument('--out',type=Path,default=Path(__file__).with_name('results'));p.add_argument('--download-sources',action='store_true');args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    if args.download_sources:
        for rel in EXPECTED:
            dest=args.sources/rel;dest.parent.mkdir(parents=True,exist_ok=True)
            url=f'https://raw.githubusercontent.com/FrankensteinVariorum/collationWorkspace/{PIN}/{rel}'
            req=urllib.request.Request(url,headers={'User-Agent':'CRR-module-A-pilot/1.0'})
            with urllib.request.urlopen(req,timeout=90) as response: raw=response.read()
            dest.write_bytes(raw)
    source_bytes={rel:(args.sources/rel).read_bytes() for rel in EXPECTED}
    for rel,blob in EXPECTED.items():
        raw=source_bytes[rel]; got=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
        if got!=blob: raise RuntimeError('source hash mismatch '+rel)
    root=xmlparse(source_bytes[APP_PATH]);apps=list(root)
    if len(apps)!=493: raise RuntimeError('unexpected apparatus population')
    raw_ms=[];views=[];cur=[]
    for app in apps:
        assert all(name(g)=='rdgGrp' for g in app)
        v=current_view(app);views.append(v);cur.append(current_answer(v))
        matches=app.xpath('.//rdg[@wit="fMS"]');assert len(matches)<=1
        raw_ms.append(''.join(matches[0].itertext()) if matches else '')
    # Source-native full-stream baseline.
    parser=ScopeParser();contexts=[];profiles=[];details=[]
    for i,raw in enumerate(raw_ms):
        contexts.append(json.loads(json.dumps(parser.active)))
        begin=len(parser.segments);parser.feed(valid_fragment(raw),i)
        segs=parser.segments[begin:];profiles.append(coarse(segs));details.append(segs)
    if parser.active: raise RuntimeError('unclosed additions in native full apparatus')
    original=ScopeParser(); original.feed(xmlparse(source_bytes[MS_PATH]),None)
    if original.active: raise RuntimeError('unclosed additions in raw source')
    if set(original.spans)!=set(parser.spans): raise RuntimeError('source/output addition inventory differs')
    mismatches=[]
    for sid,span in parser.spans.items():
        ref=original.spans[sid]
        same_attr=span['attrs']==ref['attrs'];same_text=no_space(''.join(span['texts']))==no_space(''.join(ref['texts']))
        if not (same_attr and same_text): mismatches.append({'sid':sid,'attrs_equal':same_attr,'text_equal':same_text,'source':' '.join(''.join(ref['texts']).split()),'apparatus':' '.join(''.join(span['texts']).split())})
    independent,intervals=lexical_check(raw_ms)
    independent_mismatches=[i for i in range(len(apps)) if coarse(independent[i])!=profiles[i]]
    detailed_mismatches=[i for i in range(len(apps)) if signature(independent[i])!=signature(details[i])]
    if detailed_mismatches: raise RuntimeError('independent detailed context check disagrees '+str(detailed_mismatches))
    if independent_mismatches: raise RuntimeError('independent membership check disagrees '+str(independent_mismatches))
    # Natural collisions in the COMPLETE local view, not just repeated words.
    groups=collections.defaultdict(list)
    for i,v in enumerate(views): groups[canonical(v)].append(i)
    collisions=[]
    for payload,ids in groups.items():
        if len({profiles[i] for i in ids})<=1: continue
        if any(profiles[i] in ('NO_TEXT','MIXED') for i in ids): continue
        if len({sha(canonical(cur[i])) for i in ids})!=1: raise AssertionError('current answer differs in collision')
        members=[]
        for i in ids:
            active_ids=sorted({sid for s in details[i] for sid in s['active_ids']})
            members.append({'app_ordinal_1_based':i+1,'profile':profiles[i],'raw_ms':raw_ms[i],
                  'active_ids':active_ids,'initial_context':contexts[i],
                  'encoded_spans':[{'sid':sid,'attrs':parser.spans[sid]['attrs'],
                         'source_text':' '.join(''.join(original.spans[sid]['texts']).split()),
                         'start_app_1_based':parser.spans[sid]['start_unit']+1,'end_app_1_based':parser.spans[sid]['end_unit']+1} for sid in active_ids]})
        native_xml=[E.tostring(apps[i],with_tail=False) for i in ids]
        assert len(set(native_xml))==1, 'canonical collision not byte-identical in native XML'
        collisions.append({'native_app_xml_sha256':sha(native_xml[0]),'native_app_xml_bytes':len(native_xml[0]),'view_sha256':sha(payload),'view_bytes':len(payload),'complete_local_view':json.loads(payload),
                           'current_answer':cur[ids[0]],'members':members})
    collisions.sort(key=lambda c:min(m['app_ordinal_1_based'] for m in c['members']))
    source_bad={m['sid'] for m in mismatches}
    collision_bad=source_bad & {sid for c in collisions for m in c['members'] for sid in m['active_ids']}
    if collision_bad: raise RuntimeError('collision depends on source mismatch '+str(collision_bad))
    # Decoder runs only from its declared serialized interface. Context is a
    # source-derived open-scope state, not an answer string for the next question.
    state_pass=[];state_details=[]
    for i,raw in enumerate(raw_ms):
        packet=json.loads(canonical({'view':views[i],'open_scopes':contexts[i]}))
        rdgs=[r for g in packet['view']['children'] for r in g['readings'] if r['attrs'].get('wit')=='fMS']
        local=ScopeParser(packet['open_scopes']); local.feed(valid_fragment(rdgs[0]['raw'] if rdgs else ''),0)
        state_pass.append(coarse(local.segments)==profiles[i] and signature(local.segments)==signature(details[i]))
        state_details.append({'app_ordinal_1_based':i+1,'current_answer_preserved':current_answer(packet['view'])==cur[i],
                   'profile':profiles[i],'context_bytes':len(canonical(contexts[i])),'decoder_matches_full_stream':state_pass[-1]})
    # Ordinary positional locator + source reopening baseline. Re-read file,
    # then stream to the requested source ordinal. The ordinal is retained input,
    # not supplied by the hidden gold panel.
    requests=[{'source_commit':PIN,'path':APP_PATH,'app_ordinal_1_based':i+1} for i in range(len(apps))]
    reopened=xmlparse(source_bytes[APP_PATH]);route_parser=ScopeParser();route=[];route_detailed=[]
    for i,app in enumerate(reopened):
        ms=app.xpath('.//rdg[@wit="fMS"]'); raw=''.join(ms[0].itertext()) if ms else ''
        begin=len(route_parser.segments);route_parser.feed(valid_fragment(raw),i)
        route.append(coarse(route_parser.segments[begin:]));route_detailed.append(signature(route_parser.segments[begin:]))
    linked_pass=[route[req['app_ordinal_1_based']-1]==profiles[i] and route_detailed[req['app_ordinal_1_based']-1]==signature(details[i]) for i,req in enumerate(requests)]
    # Matched wrong-context test on all natural collision members. Swap with
    # the lowest-ordinal member requiring the opposite continuation.
    controls=[]
    for c in collisions:
        for m in c['members']:
            i=m['app_ordinal_1_based']-1
            other=next(n for n in c['members'] if n['profile']!=m['profile'])
            wrong=ScopeParser(other['initial_context']);wrong.feed(valid_fragment(raw_ms[i]),0)
            controls.append({'app_ordinal_1_based':i+1,'wrong_context_from':other['app_ordinal_1_based'],
                'current_answer_unchanged':current_answer(json.loads(canonical(views[i])))==current_answer(json.loads(canonical(views[other['app_ordinal_1_based']-1]))),'wrong_context_profile':coarse(wrong.segments),
                'fails_reference':coarse(wrong.segments)!=profiles[i],
                'correct_context_bytes':len(canonical(contexts[i])), 'wrong_context_bytes':len(canonical(other['initial_context']))})
    # Separate equal-byte correct/wrong locator control. A fixed-width ordinal
    # is a conventional version-bound source coordinate, not historical evidence.
    locator_controls=[]
    for c in collisions:
        for m in c['members']:
            i=m['app_ordinal_1_based']-1
            n=next(n for n in c['members'] if n['profile']!=m['profile'])
            correct={'commit':PIN,'path':APP_PATH,'app_ordinal':f'{i+1:06d}'}
            wrong=dict(correct,app_ordinal=f"{n['app_ordinal_1_based']:06d}")
            assert len(canonical(correct))==len(canonical(wrong))
            correct_result=route[int(json.loads(canonical(correct))['app_ordinal'])-1]
            wrong_result=route[int(json.loads(canonical(wrong))['app_ordinal'])-1]
            locator_controls.append({'app_ordinal_1_based':i+1,'wrong_ordinal':n['app_ordinal_1_based'],
                'correct':correct_result,'wrong':wrong_result,'correct_matches':correct_result==profiles[i],
                'wrong_fails':wrong_result!=profiles[i],'equal_locator_bytes':len(canonical(correct)),
                'current_answer_unchanged':cur[i]==cur[n['app_ordinal_1_based']-1]})
    # Scope-swap matches interface, NOT bytes: empty vs nonempty contexts differ.
    dist=collections.Counter(s['end_unit']-s['start_unit'] for s in parser.spans.values())
    samples=[m for c in collisions for m in c['members']]
    result={'study':'MODULE_A_FV_C18_SCOPE_CONTINUATION_PILOT_V1','authority':'POST_INSPECTION_DEVELOPMENT_NOT_CONFIRMATORY',
      'upstream_commit':PIN,'sources':{p:{'git_blob':EXPECTED[p],'sha256':sha(b),'bytes':len(b)} for p,b in source_bytes.items()},
      'population':{'apparatus_units':len(apps),'ms_nonempty_text_units':sum(x!='NO_TEXT' for x in profiles),
             'addition_spans':len(parser.spans),'cross_app_spans':sum(s['end_unit']>s['start_unit'] for s in parser.spans.values()),
             'span_app_distance_distribution':dict(sorted(dist.items())),'initial_context_nonempty_units':sum(bool(c) for c in contexts)},
      'source_verification':{'addition_ids_equal':True,'checked_additions':len(parser.spans),'attribute_or_text_mismatches':mismatches,
            'independent_interval_membership_mismatches':independent_mismatches,'independent_detailed_profile_mismatches':detailed_mismatches},
      'natural_collision_classes':len(collisions),'collision_checkpoint_count':len(samples),'collisions':collisions,
      'comparators':{'NATIVE_FULL_STREAM':{'resolved':len(profiles),'denominator':len(apps),'source_bytes':len(source_bytes[APP_PATH])},
        'COMPLETE_LOCAL_APP_ONLY':{'current_answers_preserved':len(apps),'proven_ambiguous_natural_classes':len(collisions),
              'proven_ambiguous_checkpoint_count':len(samples),'safe_action_on_these':'ABSTAIN_OR_REQUEST_PROVENANCE',
              'not_claimed':'Not a classification of every remaining checkpoint as sufficient'},
        'ORDINARY_PINNED_SOURCE_LINK':{'continuation_matches':sum(linked_pass),'denominator':len(apps),
              'nonempty_text_matches':sum(ok and profiles[i]!='NO_TEXT' for i,ok in enumerate(linked_pass)),'no_text_controls':sum(x=='NO_TEXT' for x in profiles),'one_cold_reopen_source_bytes':len(source_bytes[APP_PATH]),'cold_source_calls_per_episode':1,
              'batch_cached_source_calls':1,'all_link_payload_bytes':len(canonical(requests)),
              'method':'Pinned source path and 1-based app ordinal; ordinary full-source scan'},
        'OPEN_SCOPE_STATE':{'continuation_matches':sum(state_pass),'denominator':len(apps),
              'state_population_json_bytes':len(canonical(contexts)),
              'nonempty_text_matches':sum(ok and profiles[i]!='NO_TEXT' for i,ok in enumerate(state_pass)),'no_text_controls':sum(x=='NO_TEXT' for x in profiles),'extra_per_checkpoint_min':min(len(canonical(c)) for c in contexts),'extra_per_checkpoint_max':max(len(canonical(c)) for c in contexts),
              'construction_requires_full_stream':True,'construction_source_bytes':len(source_bytes[APP_PATH]),
              'not_claimed':'Not globally minimal and not a new parser/invention'},
        'WRONG_PINNED_LOCATOR_CONTROL':{'tested':len(locator_controls),'correct_matches':sum(x['correct_matches'] for x in locator_controls),'wrong_fails':sum(x['wrong_fails'] for x in locator_controls),'all_current_answers_unchanged':all(x['current_answer_unchanged'] for x in locator_controls),'matched_locator_bytes_and_source_reopen_cost':True,'details':locator_controls},
        'WRONG_SCOPE_CONTROL':{'fails_reference':sum(c['fails_reference'] for c in controls),'tested':len(controls),
             'all_current_answers_unchanged':all(c['current_answer_unchanged'] for c in controls),'matched_interface_not_matched_bytes':True,'details':controls}},
      'claim_boundary':['Natural source records under controlled record-local checkpoint export; not a naturally broken scholarly edition.',
       'Current output is native normalized comparison. Continuation is encoded insertion membership/place, not original-author truth.',
       'Complete local payload equality excludes global app ordinal, navigation/history or hidden original object handles.',
       'All restored-source paths are credited; native linked infrastructure is NOT shown insufficient.',
       'No actual later editorial retraction or selective belief-revision event was run.',
       'No autonomous question generation, long-horizon experiment or independent corpus replication was run.',
       'Three token classes can share the same underlying added passage and are not independent historical replicates.',
       'Source mismatch entries, if present, are retained; only source-verified collision spans support the main pilot witness.'],
      'execution':{'python':sys.version.split()[0],'lxml':E.LXML_VERSION,'llm_calls':0}}
    assert all(state_pass) and all(linked_pass)
    (args.out/'results.json').write_bytes(json.dumps(result,indent=2,ensure_ascii=False).encode()+b'\n')
    (args.out/'checkpoint_results.json').write_bytes(json.dumps(state_details,indent=2).encode()+b'\n')
    print(json.dumps({k:result[k] for k in ['study','population','source_verification','natural_collision_classes','collision_checkpoint_count','comparators']},indent=2,ensure_ascii=False))
    scientific=dict(result);scientific.pop('execution');print('SCIENTIFIC_PAYLOAD_SHA256='+sha(canonical(scientific)))
    print('RESULTS_SHA256='+sha((args.out/'results.json').read_bytes()))

if __name__=='__main__': main()
