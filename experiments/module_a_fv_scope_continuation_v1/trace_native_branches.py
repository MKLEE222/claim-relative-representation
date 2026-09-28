"""Source-native next-step feasibility trace; NOT autonomous question discovery."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
from lxml import etree as E

ROOT=Path(__file__).parent
NS='{http://www.w3.org/XML/1998/namespace}'
source=(ROOT/'sources/collationChunks/C18/msColl_C18.xml').read_bytes()
text=source.decode(); tree=E.fromstring(source,E.XMLParser(collect_ids=False,no_network=True))
results=json.loads((ROOT/'results/results.json').read_text())
# Independent boundary matching on the supplied XML. Does not read the pilot's
# recorded source_text fields and does not use an answer lookup.
def scope(sid):
    starts=[e for e in tree.iter('sga-add') if e.get('sID')==sid]
    if len(starts)!=1: raise ValueError('nonunique/missing source start')
    node=starts[0]
    p0=re.search(r'<sga-add\b[^>]*\bsID="'+re.escape(sid)+r'"[^>]*/>',text)
    p1=re.search(r'<sga-add\b[^>]*\beID="'+re.escape(sid)+r'"[^>]*/>',text)
    if not(p0 and p1 and p0.end()<=p1.start()): raise ValueError('invalid source span')
    inner=text[p0.end():p1.start()]
    frag=E.fromstring(('<fragment>'+inner+'</fragment>').encode(),E.XMLParser(collect_ids=False,no_network=True))
    excerpt=text[p0.start():p1.end()]
    return {'sid':sid,'attributes':dict(node.attrib),'text':' '.join(''.join(frag.itertext()).split()),
            'xml_excerpt':excerpt,'source_character_span':[p0.start(),p1.end()],
            'source_line_span':[text.count('\n',0,p0.start())+1,text.count('\n',0,p1.end())+1],
            'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),
            'cancellations':[{'element':E.QName(e).localname,'text':' '.join(''.join(e.itertext()).split())}
                             for e in frag.iter() if E.QName(e).localname in {'del','mdel'}]}
traces=[]
for c in results['collisions']:
    for checkpoint in c['members']:
        # Source-grounded context is an explicit consumer input, obtained by the
        # native-linked baseline. Local-only snapshots cannot identify the SID.
        ctx=checkpoint['initial_context'];steps=[]
        for sid in ctx:
            rec=scope(sid)
            steps.append({'operation':'INSPECT_ENCLOSING_ADDITION','input_sid':sid,'response':rec})
            native_id=rec['attributes'].get(NS+'id')
            incoming=[e for e in tree.iter('sga-add') if native_id and e.get('next')=='#'+native_id]
            if incoming:
                for e in incoming:
                    preceding=scope(e.get('sID'))
                    steps.append({'operation':'FOLLOW_ENCODED_PREDECESSOR','trigger':dict(e.attrib),
                        'response':preceding,
                        'licensed_followup':'Does the selected insertion continue an earlier explicitly linked fragment?',
                        'joined_text':preceding['text']+' '+rec['text']})
            if rec['cancellations']:
                steps.append({'operation':'INSPECT_INTERNAL_CANCELLATION','trigger':rec['cancellations'],
                    'licensed_followup':'Which characters are cancelled inside this encoded addition?',
                    'response':rec['cancellations']})
        traces.append({'app_ordinal_1_based':checkpoint['app_ordinal_1_based'],
           'scope_status':checkpoint['profile'],'steps':steps,
           'not_a_claim':'Outside an sga-add span does not establish an unrevised historical inscription.'})
report={'authority':'POST_INSPECTION_SOURCE_OPERATION_FEASIBILITY_ONLY',
  'source_sha256':hashlib.sha256(source).hexdigest(),'source_bytes':len(source),'traces':traces,
  'limits':['Not an LLM or human question-generation experiment.',
            'Only the declared native next-link and nested-cancellation rules were executed.',
            'No later historical evidence revision was invented.',
            'Two checkpoints share one source addition; they are not independent episodes.']}
p=ROOT/'results/native_branch_traces.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for r in traces:
 print(r['app_ordinal_1_based'],r['scope_status'],[s['operation'] for s in r['steps']])
 for step in r['steps']:
  if 'joined_text' in step: print('  CHAIN',step['joined_text'])
  if step['operation']=='INSPECT_INTERNAL_CANCELLATION': print('  CANCELLED',step['response'])
print('TRACE_SHA256='+hashlib.sha256(p.read_bytes()).hexdigest())
