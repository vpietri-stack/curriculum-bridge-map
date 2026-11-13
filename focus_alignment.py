"""Editorial PEP topic index for the focused G3/G4 comparison.

Each PEP unit contributes only the vocabulary and language examples that belong
to the selected topic. Source links and evidence type stay on every row.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent

# Topic -> textbook units. This is a topic-level editorial mapping, not a
# whole-unit recommendation: item filters below select the actual evidence.
UNITS = {
 'greetings':'3-Fall-1 3-Spring-1',
 'kindness':'3-Fall-1 3-Spring-1 3-Spring-2 4-Fall-2 4-Fall-4',
 'colours':'3-Fall-5 4-Spring-4',
 'numbers':'3-Fall-6 3-Spring-6',
 'school':'3-Spring-1 3-Spring-3 4-Spring-1',
 'rules':'4-Spring-1 4-Spring-2',
 'position':'3-Spring-5',
 'family':'3-Fall-2 4-Fall-1 4-Fall-2',
 'body':'3-Fall-1 3-Spring-2 3-Spring-3',
 'senses':'3-Spring-3 3-Spring-2',
 'animals':'3-Fall-3 3-Fall-4 3-Spring-2 4-Spring-5 4-Spring-6',
 'feelings':'3-Spring-2 4-Fall-1 4-Fall-2',
 'food':'3-Fall-4 3-Spring-4 4-Spring-5 4-Spring-6',
 'toys':'3-Spring-5 3-Fall-6',
 'possessions':'3-Spring-5 4-Fall-6',
 'shapes':'',
 'transport':'3-Spring-5 4-Fall-3 4-Fall-4',
 'places':'3-Fall-3 4-Fall-3 4-Fall-4',
 'jobs':'4-Fall-1 4-Fall-4 3-Spring-1',
 'leisure':'4-Fall-2 4-Fall-3 4-Fall-5 3-Spring-2',
 'actions':'3-Spring-2 4-Fall-4 4-Fall-5 4-Spring-2',
 'health':'3-Spring-4 4-Spring-2 4-Spring-6',
 'home':'3-Spring-5 4-Spring-2 4-Fall-1',
 'ability':'3-Fall-1 3-Fall-4 4-Fall-5',
 'time':'3-Fall-6 4-Spring-3 4-Fall-5',
 'clothes':'4-Fall-6 4-Spring-4',
 'nature':'3-Fall-4 3-Fall-5 4-Fall-6',
 'weather':'4-Fall-5 4-Fall-6',
 'shopping':'3-Fall-6 3-Spring-6 4-Spring-4',
 'sequence':'3-Spring-4 4-Spring-2 4-Spring-6',
 'descriptions':'3-Fall-3 3-Spring-2 4-Fall-2',
 'community':'4-Fall-3 4-Fall-4',
 'story':'',
 'phonics':'',
}

# Meaningful target words only. Each entry is still checked against the linked
# PEP target list before it can appear in the published comparison.
WORDS = {
 'greetings':'name nice friend where from UK China Canada USA',
 'kindness':'nice share smile listen help say friend love kind helpful together',
 'colours':'colour orange green red blue make purple brown yellow pink white black colourful',
 'numbers':'old five year one two three four ten six seven eight nine twelve eleven thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty',
 'school':'school teacher student classmate class in class eraser find ruler pen pencil book bag paper computer learn classroom blackboard desk chair door window fan wall workbook hand out newspaper maths art PE',
 'rules':'sorry late rule ready hurry up class classroom turn off tidy understand safe helpful loud follow first homework',
 'position':'at home on shelf in box under there over place put',
 'family':'mum dad grandma grandpa grandfather grandmother mother father sister family cousin brother baby uncle aunt child',
 'body':'ear hand eye mouth arm body leg tail face nose tongue',
 'senses':'see smell taste hear touch nose tongue eye ear hand',
 'animals':'dog pet cat fish bird rabbit zoo fox panda red panda cute monkey tiger elephant lion animal giraffe tall fast farm pig cow horse sheep chicken bee mouse',
 'feelings':'love tired kind funny strong quiet',
 'food':'apple banana orange grape farm water fruit breakfast bread egg milk noodle juice rice meat vegetable healthy plate soup candy yummy tomato carrot potato green bean feed pick pass knife fork chopstick waste food delicious clear the table set the table bowl spoon salad',
 'toys':'boat ball doll car old keep cool cap box cake',
 'possessions':'old keep mine whose sweater sock shirt coat',
 'transport':'boat car bus stop driver delivery worker walk',
 'places':'zoo playground park hospital shop toilet bus stop library gym museum community favourite place supermarket',
 'jobs':'job doctor farmer nurse office worker factory worker firefighter driver cleaner cook delivery worker police officer teacher',
 'leisure':'play game football basketball sport fly kite swim read sing dance',
 'actions':'sing dance talk play cook clean sweep make the bed fly swim run wash',
 'health':'healthy vegetable fruit eat wash safe sleep',
 'home':'home room living room bedroom kitchen study bathroom shelf box chore cook clean sweep floor',
 'time':'clock o’clock o\'clock time minute breakfast dinner lunch tomorrow week',
 'clothes':'sweater sock wear shirt coat dress T-shirt glove trousers clothes shorts jacket skirt shoe hat sunglasses size try on',
 'nature':'plant garden air water flower grass tree sun sea spring summer autumn fall leaf winter snow rain',
 'weather':'weather sunny hot cold windy cloudy rainy snowy cool warm rain snowman degree',
 'shopping':'shop buy pay back expensive cheap take large size list try on pair clothes trousers shorts jacket skirt shoe hat sunglasses',
 'sequence':'first then week pick feed pass clear the table set the table',
 'descriptions':'long short fat thin slow tall fast cute strong quiet big small beautiful',
 'community':'community neighbour people child everyone firefighter driver cleaner delivery worker police officer',
}

# Indices refer to PEP target sentence lists in catalog.json. A hand-reviewed
# index avoids treating a whole mixed-theme textbook unit as one topic.
STRUCTURES = {
 '3-Fall-1':{'greetings':[0,1,2,3],'kindness':[4,5,6,7,8]},
 '3-Fall-2':{'family':[0,1,2,3,4]},
 '3-Fall-3':{'greetings':[0,1],'animals':[2,3,4,5,7,8,9,10]},
 '3-Fall-4':{'food':[0,1,2,3],'nature':[4,5,6],'animals':[3,4]},
 '3-Fall-5':{'colours':[0,1,2,3,4,5],'nature':[5]},
 '3-Fall-6':{'numbers':[0,1,3],'time':[7],'shopping':[4,5,6],'toys':[8]},
 '3-Spring-1':{'greetings':[0,1,2,3],'kindness':[4,5,6]},
 '3-Spring-2':{'descriptions':[0,1],'animals':[0,1],'family':[2,3,4],'actions':[4,5],'feelings':[1,5]},
 '3-Spring-3':{'school':[0,1,2,3,4,5,6],'senses':[4,5,6]},
 '3-Spring-4':{'food':[0,1,2,3,4],'health':[4]},
 '3-Spring-5':{'possessions':[0,1,2,3],'position':[4,5,6,7],'toys':[0,2,3]},
 '3-Spring-6':{'numbers':[0,1,2,3],'shopping':[4,5,6,7]},
 '4-Fall-1':{'jobs':[0,1],'family':[2,3],'home':[2,3]},
 '4-Fall-2':{'greetings':[0,1,4,5],'descriptions':[2,3,5],'kindness':[3,5],'leisure':[5]},
 '4-Fall-3':{'places':[0,1,2,3,5],'leisure':[0,4],'community':[0,2,5],'position':[0,1,2,3]},
 '4-Fall-4':{'jobs':[0,1,2],'community':[0,1,2,4],'actions':[3,4]},
 '4-Fall-5':{'weather':[1,2,3,4,7],'leisure':[5,8],'places':[6],'time':[3]},
 '4-Fall-6':{'clothes':[0,1,2,3],'weather':[3,4,5],'nature':[4,5,6,7,8,9],'possessions':[0,1]},
 '4-Spring-1':{'rules':[0,1,2,3,4],'school':[2,3,4]},
 '4-Spring-2':{'rules':[0,1,2,3],'home':[0,1,2],'health':[3],'sequence':[1]},
 '4-Spring-3':{'time':[0,1,2,3,4,5],'school':[2,4]},
 '4-Spring-4':{'shopping':[0,1,2,3,4,5],'clothes':[0,1,2,4]},
 '4-Spring-5':{'animals':[0,1,2],'food':[2,3,4]},
 '4-Spring-6':{'food':[0,1,2,3,4],'health':[4],'sequence':[0,1,4]},
}

def norm(s): return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()

def words_for(tag):
    # Multiword targets are found by normalized substring in the editorial list.
    return ' '+norm(WORDS.get(tag,''))+' '

def word_allowed(tag, text):
    return bool(text and (' '+norm(text)+' ') in words_for(tag))

def source_phrase(s):
    s=norm(s)
    return s.replace('i m','im').replace('my name s','my name is').replace('what s','what is')

def relation(source, pep, kind):
    a,b=source_phrase(source),source_phrase(pep)
    if not a or not b:return None
    if a==b:return 'exact'
    if kind=='vocab':
        if a.rstrip('s')==b.rstrip('s') and min(len(a),len(b))>3:return 'related'
        return None
    if (a in {'hello','hi'} and b.startswith(a+' ')) or (b in {'hello','hi'} and a.startswith(b+' ')):return 'related'
    if re.search(r'\([^)]{1,25}\)',source):
        slots=re.findall(r'\(([^)]{1,25})\)',source)
        template=source_phrase(re.sub(r'\([^)]{1,25}\)',' ZZZ ',source))
        pattern=re.escape(template)
        for key in slots:
            key=norm(key)
            if key in {'six','age'}:replacement=r'(?:[0-9]+|one|two|three|four|five|six|seven|eight|nine|ten)'
            elif key in {'blue','colour','color'}:replacement=r'(?:red|blue|yellow|green|orange|purple|pink|grey|gray|black|white|brown)'
            elif key=='name':replacement=r'(?!from\b|one\b|two\b|three\b|four\b|five\b|six\b|seven\b|eight\b|nine\b|ten\b)[a-z]+(?: [a-z]+)?'
            else:replacement=r'[a-z]+(?: [a-z]+)?'
            pattern=pattern.replace('zzz',replacement,1)
        pattern='^'+pattern+'$'
        if re.fullmatch(pattern,b):return 'exact'
        if 'six' in slots and b.startswith('im ') and 'year' in b:return 'related'
    # Templates and named examples represent the same sentence frame.
    if a in b or b in a:
        if min(len(a),len(b))>=6:return 'related'
    groups=[('im name','my name is'),('i am name','my name is'),('let us share','we can share')]
    if any((x in a and y in b) or (y in a and x in b) for x,y in groups):return 'related'
    return None

def pep_rows(pep,tag):
    key=f"{pep['grade']}-{pep['semester']}-{pep['number']}"
    if key not in UNITS.get(tag,'').split():return []
    rows=[]
    for x in pep['vocabulary']:
        if word_allowed(tag,x['text']):rows.append({'text':x['text'],'type':'vocab','pepId':pep['id'],'page':str(x['page']).strip(),'url':x['url'],'evidence':'target'})
    for i in STRUCTURES.get(key,{}).get(tag,[]):
        x=pep['structures'][i]
        if norm(x['text']) in {'great','use again','be careful'} or '.Thank' in x['text']:continue
        rows.append({'text':x['text'],'type':'structure','pepId':pep['id'],'page':str(x['page']).strip(),'url':x['url'],'evidence':'target'})
    # Main dialogues supply additional evidence when a target sentence is
    # instantiated with a name, an object, or an age. Keep them available for
    # item-level evidence without flooding the suggested lesson list.
    target_norm={norm(r['text']) for r in rows if r['type']=='structure'}
    topical_words={w for w in norm(WORDS.get(tag,'')).split() if len(w)>=4 and w not in {'make','good','from','there','these','have','this','that','with','they','what','when','where','some','nice','like','play','book','class'}}
    if tag=='greetings':topical_words|={'name','nice','from','hello'}
    if tag=='colours':topical_words|={'red','blue','pink'}
    for x in pep['reading']:
        n=norm(x['text'])
        target_variant=any(n==t or (len(n)>7 and n in t) or (len(t)>7 and t in n) for t in target_norm)
        lexical=len(n.split())>=3 and bool(set(n.split()) & topical_words)
        if len(x['text'])<=95 and (target_variant or lexical):
            rows.append({'text':x['text'],'type':'structure','pepId':pep['id'],'page':str(x['page']).strip(),'url':x['url'],'evidence':'main reading/dialogue'})
    return rows

CARD_RULES={
 'Naming objects':{'structure'},'Classroom story':{'structure'},
 'Describing animals':{'structure'},'Animal products':{'vocab'},
 'Animal story':{'structure'},'Animal review':set(),
 'Food preferences':{'structure'},'Food requests':{'structure'},
 'Food story':{'structure'},'Food review':set(),
 'Possession':{'structure'},'Wants and presents':{'structure'},
 'Birthday story':{'structure'},'There is and there are':{'structure'},
 'Going out':{'structure'},'Animal habitats':{'structure'},
 'Zoo story':{'structure'},'Actions now':{'structure'},
 'Permission to play':{'structure'},'Playground story':{'structure'},
 'Ability':{'structure'},'Types of homes':{'vocab'},'Home story':{'structure'},
 'Actions and imperatives':{'structure'},'Leisure preferences':{'structure'},
 'Holiday story':{'structure'},'Stories and review':set(),
}

def for_card(rows,c,pep):
    name=c['name']
    if name in {'School objects','School and learning'}:
        return [r for r in rows if r['type']=='vocab' or (r['pepId']=='PEP-3-Spring-3' and r['type']=='structure' and any(k in norm(r['text']) for k in ('eraser','excuse me','here you are','no problem')))]
    if name=='Naming objects':
        extra=[]
        p=next((p for p in pep if p['id']=='PEP-4-Spring-5'),None)
        if p:
            for i in (2,3):
                x=p['structures'][i]
                extra.append({'text':x['text'],'type':'structure','pepId':p['id'],'page':str(x['page']).strip(),'url':x['url'],'evidence':'target'})
        return [r for r in rows if r['type']=='structure' and any(k in norm(r['text']) for k in ('what are these','they re','what about this'))]+extra
    if name=='Classroom story':
        return [r for r in rows if r['pepId']=='PEP-4-Spring-1' and (r['type']=='vocab' or any(k in norm(r['text']) for k in ('late for class','on duty','desks and chairs')))]
    if name in CARD_RULES:return [r for r in rows if r['type'] in CARD_RULES[name]]
    return rows

def build():
    src=json.loads((ROOT/'focus_sources.json').read_text(encoding='utf-8'))
    pep=src['pepUnits']; source=src['sourceUnits']
    pep_by_id={p['id']:p for p in pep}
    paths={'Power Up':[],'iShow':[]}
    out=[]
    for u in source:
        path=paths[u['course']]
        if u['course']=='iShow' and u['level']=='Play 1':
            # Act 3 already sits at the beginning of the same learning path.
            pass
        prior=[x for old in path for c in old['topics'] for x in c['sourceItems']]
        done=[]; topics=[]
        for c in u['topics']:
            known=prior+done+c['sourceItems']
            rows=[]
            for p in pep:
                if p['grade']<=u['gradeMax']:
                    rows+=pep_rows(p,c['tag'])
            rows=for_card(rows,c,pep)
            shared=[]; additions=[]
            for r in rows:
                matches=[(x,relation(x['text'],r['text'],r['type'])) for x in known if x['type']==r['type']]
                exact=next((x for x,rel in matches if rel=='exact'),None)
                related=next((x for x,rel in matches if rel=='related'),None)
                entry={**r,'relation':'exact' if exact else 'related' if related else 'new','sourceMatch':(exact or related or {}).get('text')}
                (shared if exact else additions).append(entry)
            # Dedupe target/reading equivalents, retaining target as the lead
            # evidence and a reading link as an extra reference.
            def dedupe(items):
                seen={}; ans=[]
                for x in items:
                    key=(x['pepId'],x['type'],norm(x['text']))
                    if key in seen:
                        lead=seen[key]
                        if x['evidence']!=lead['evidence']:
                            lead.setdefault('alsoEvidence',[]).append({'evidence':x['evidence'],'url':x['url'],'page':x['page']})
                    else:seen[key]=x;ans.append(x)
                return ans
            topics.append({**c,'shared':dedupe(shared),'additions':dedupe(additions)})
            done+=c['sourceItems']
        out.append({**u,'topics':topics})
        path.append(u)
    return {'sourceUnits':out,'pepUnits':pep,'fullCatalog':'catalog.json'}

if __name__=='__main__':
    data=build()
    (ROOT/'focus.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(len(data['sourceUnits']),'units',sum(len(c['additions']) for u in data['sourceUnits'] for c in u['topics']),'suggestions')
