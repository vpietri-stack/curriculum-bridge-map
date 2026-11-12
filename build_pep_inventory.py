import json,pathlib,re
R=pathlib.Path(__file__).parent/'sources'/'pep_api'
OUT=pathlib.Path(__file__).parent/'sources'/'pep_inventory.json'
BOOKS=[(369,3,'Fall'),(45677,3,'Spring'),(45792,4,'Fall'),(45840,4,'Spring'),(45818,5,'Fall'),(45856,5,'Spring'),(45882,6,'Fall')]
APPENDIX_PAGES={369:{'words':(83,86),'expressions':(89,91)},45677:{'words':(80,83),'expressions':(87,89)},45792:{'words':(80,83),'expressions':(86,88)},45840:{'words':(80,83),'expressions':(86,88)},45818:{'words':(80,83),'expressions':(87,89)},45856:{'words':(81,85),'expressions':(89,91)},45882:{'words':(81,85),'expressions':(89,92)}}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def clean(s):return re.sub(r'\s+',' ',s or '').strip()
def normalize(s):return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
units=[]
for bid,grade,semester in BOOKS:
    b=load(R/f'{bid}.json'); pages=b['pages']; bypid={p['pid']:p for p in pages}
    sections=[]
    for u in b['units']:
        pid=u['classes'][0]['first_pid'];p=bypid.get(pid)
        if p:sections.append((p['ordinal'],u))
    sections.sort(key=lambda x:x[0])
    ranges=[]
    for i,(start,u) in enumerate(sections):
        end=sections[i+1][0] if i+1<len(sections) else 10**6
        ranges.append((start,end,u))
    def page_regions(p):
        f=R/f"{bid}_{p['pid']}.json"
        return [clean(x.get('text_en')) for x in load(f).get('regions',[])] if f.exists() else []
    page_text={p['pid']:page_regions(p) for p in pages}
    appendices={}
    for start,end,u in ranges:
        title=u['title'].lower()
        if title.startswith('appendix'):
            for p in pages:
                if start<=p['ordinal']<end:
                    first=' '.join(page_text[p['pid']][:4]).lower()
                    if 'words in each unit' in first:appendices['words']=(p['ordinal'],end)
                    if 'useful expressions' in first:appendices['expressions']=(p['ordinal'],end)
    # Earlier books put multiple appendices inside one metadata section.
    for kind,phrase in [('words','words in each unit'),('expressions','useful expressions')]:
        if kind not in appendices:
            candidates=[p['ordinal'] for p in pages if phrase in ' '.join(page_text[p['pid']][:4]).lower()]
            if candidates:
                start=candidates[0]; stops=[p['ordinal'] for p in pages if p['ordinal']>start and any(z in ' '.join(page_text[p['pid']][:4]).lower() for z in ['vocabulary','useful expressions','pronunciation'])]
                appendices[kind]=(start,min(stops) if stops else start+4)
    for kind,span in APPENDIX_PAGES.get(bid,{}).items():
        selected=[p['ordinal'] for p in pages if p['page'].strip().isdigit() and span[0]<=int(p['page'].strip())<span[1]]
        if selected:appendices[kind]=(min(selected),max(selected)+1)
    targets={n:{'words':[],'expressions':[]} for n in range(1,7)}
    for kind in ['words','expressions']:
        if kind not in appendices:continue
        start,end=appendices[kind];current=None
        for p in pages:
            if not start<=p['ordinal']<end:continue
            for text in page_text[p['pid']]:
                m=re.fullmatch(r'Unit\s*(\d+)',text,re.I)
                if m:current=int(m[1]);continue
                if not current or current not in targets:continue
                if kind=='words' and re.fullmatch(r'Numbers',text,re.I):current=None;continue
                if not text or re.search(r'^(words in each unit\.?|useful expressions|appendix\s*\d*|vocabulary|Aua)$',text,re.I):continue
                text={'ping pong ping pong':'ping pong'}.get(text,text)
                if kind=='words' and (len(text)>35 or re.search(r'[.!?]',text)):continue
                if kind=='expressions' and (len(text)>160 or len(text)<4):continue
                targets[current][kind].append({'text':text,'appendixPage':p['page'],'appendixUrl':f'https://www.ai2book.com/diandu/book/{bid}?p={p["pid"]}'})
    for start,end,u in ranges:
        m=re.match(r'Unit\s*(\d+)\s*(.*)',u['title'],re.I)
        if not m:continue
        num=int(m[1]);unitpages=[p for p in pages if start<=p['ordinal']<end]
        if not unitpages:continue
        rows=[]
        for p in unitpages:
            url=f'https://www.ai2book.com/diandu/book/{bid}?p={p["pid"]}'
            for text in page_text[p['pid']]:rows.append({'text':text,'page':p['page'],'url':url})
        for kind in ['words','expressions']:
            for item in targets.get(num,{}).get(kind,[]):
                needle=normalize(item['text'])
                occurrence=next((r for r in rows if needle and re.search(r'\b'+re.escape(needle)+r'\b',normalize(r['text']))),None)
                item['page']=occurrence['page'] if occurrence else item['appendixPage']
                item['url']=occurrence['url'] if occurrence else item['appendixUrl']
                item['evidence']='target'
        units.append({'id':f'PEP-{grade}-{semester}-{num}','grade':grade,'semester':semester,'number':num,'title':m[2].strip(),'bookId':bid,'url':f'https://www.ai2book.com/diandu/book/{bid}?p={unitpages[0]["pid"]}','vocabulary':targets.get(num,{}).get('words',[]),'structures':targets.get(num,{}).get('expressions',[]),'pages':rows})
    print(bid,'appendices',appendices,'targets',[len(targets[n]['words']) for n in range(1,7)],flush=True)
OUT.write_text(json.dumps(units,ensure_ascii=False),encoding='utf-8')
print('units',len(units),flush=True)
