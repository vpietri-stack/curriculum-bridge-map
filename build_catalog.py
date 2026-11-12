import json,pathlib,re
ROOT=pathlib.Path(__file__).parent
def load(name):return json.loads((ROOT/'sources'/name).read_text(encoding='utf-8'))
ishow=load('ishow_inventory.json'); powerup=load('powerup_inventory.json'); pep=load('pep_inventory.json')
for u in pep:
    lines=[];seen=set();by_page={}
    for row in u.pop('pages'):
        by_page.setdefault((row['page'],row['url']),[]).append(row['text'])
    continuation=False
    for (page,url),texts in by_page.items():
        opening=' '.join(texts[:6]).lower()
        heading=bool(re.search(r"let.s talk|reading time|read and write|story time|read and talk|listen and read",opening))
        in_reading=heading or (continuation and not re.search(r"let.s learn|let.s spell|project|unit \d+",opening))
        continuation=bool(re.search(r'reading time|read and write|story time',opening)) and len(texts)>4
        if not in_reading:continue
        start=next((i+1 for i,t in enumerate(texts[:6]) if re.search(r"let.s talk|reading time|read and write|story time|read and talk|listen and read",t,re.I)),1) if heading else 0
        for raw in texts[start:]:
            if re.search(r'listen and|ask and answer|talk and write|fill in|tick the|read and|look and|make up|work in pairs|read the story|then write|listen,',raw,re.I):continue
            for text in re.split(r'(?<=[.!?])\s+(?=[A-Z])',raw):
                text=re.sub(r'\s+',' ',text).strip()
                if not 10<=len(text)<=160 or not re.search(r'[?.!]$',text):continue
                if re.match(r'^(read|listen|look|work|draw|write|match|circle|tick|fill|check|say the|ask|make a|answer|choose|complete|find out|dear parents)',text,re.I):continue
                if re.match(r'^\d+[.) ]',text) or '...' in text or text.count('_')>1:continue
                key=re.sub(r'[^a-z0-9]','',text.lower())
                if key in seen:continue
                seen.add(key);lines.append({'text':text,'page':page,'url':url,'evidence':'main reading/dialogue'})
    u['reading']=lines
    u['title']=u['title'].replace('natureand','nature and')
catalog={'version':'2026-11-12','courseOrder':['Power Up','iShow','PEP'],'levelOrder':{'Power Up':['PU1','PU2','PU3','PU4'],'iShow':['Act 3','Play 1','Play 2','Play 3','Play 4'],'PEP':['Grade 3 Fall','Grade 3 Spring','Grade 4 Fall','Grade 4 Spring','Grade 5 Fall','Grade 5 Spring','Grade 6 Fall']},'units':powerup+ishow,'pep':pep,'notes':{'edition':'Revised PEP English, three-year starting point. Grade 6 Spring is not yet available in the revised ai2book sequence.','method':'PEP vocabulary and useful expressions are indexed from each book appendix; main reading/dialogue matches use book page text. Power Up unit records come from Teacher Book pages, checked against the separate word lists for spelling. iShow comes from TLS files.'}}
(ROOT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('courses',len(powerup),len(ishow),len(pep),'reading lines',sum(len(u['reading']) for u in pep),'bytes',(ROOT/'catalog.json').stat().st_size)
