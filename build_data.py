import glob, html, json, os, re, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ROOT=Path(__file__).parent
TLS=Path(r'G:\My Drive\I2\english teaching\I2\curriculum maps')
def rows(path):
    with zipfile.ZipFile(path) as z:
        ss=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            ss=[''.join(t.text or '' for t in si.iter('{%s}t'%N['m'])) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        root=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        for row in root.findall('.//m:sheetData/m:row',N):
            out={}
            for c in row.findall('m:c',N):
                v=c.find('m:v',N); inline=c.find('m:is',N)
                if v is not None: value=ss[int(v.text)] if c.get('t')=='s' else v.text
                elif inline is not None: value=''.join(t.text or '' for t in inline.iter('{%s}t'%N['m']))
                else: continue
                out[re.match('[A-Z]+',c.get('r')).group()]=re.sub(r'\s+',' ',value or '').strip()
            yield out
def short(s,n=230): return (s or '')[:n].strip(' /,;')
concepts=[('present continuous',r'present continuous|现在进行时|what are you doing|what is he doing'),('present simple',r'present simple|一般现在时|every day|how often'),('past simple',r'past simple|一般过去时|yesterday|last week'),('future plans',r'going to|will\s+\w+|future'),('superlatives',r'superlative|最高级|youngest|biggest|best'),('comparatives',r'comparative|比较级|bigger than|smaller than'),('modals and rules',r'\bmust\b|mustn.t|\bshould\b|\bcould\b|\bcan\b'),('prepositions',r'preposition|方位介词|next to|opposite|under|above'),('questions',r'question|疑问句|\bwhat\b|\bwhere\b|\bwho\b|\bwhen\b|\bwhy\b'),('pronouns',r'pronoun|代词'),('plural nouns',r'plural|复数'),('frequency',r'frequency|频率|often|sometimes'),('there is / there are',r'there is|there are'),('have got / has got',r'have got|has got'),('imperatives',r'imperative|指令|don.t run')]
def language_focus(s): return ', '.join(label for label,pattern in concepts if re.search(pattern,s,re.I)) or 'Topic language and conversation'
def word_list(s):
    parts=re.split(r'[/,;·\n]+',s)
    words=[]
    for part in parts:
        part=re.sub(r'[^A-Za-z\- ]','',part).strip().lower()
        if 2<=len(part)<=24 and len(part.split())<=3 and part not in words: words.append(part)
    return ', '.join(words[:22])
tls=[]
for p in sorted(TLS.glob('*.xlsx')):
    name=p.name
    rr=list(rows(p))
    if name.lower().startswith('ishow'):
        level=re.search(r'(A3|P[1-4])',name).group()
        groups=[]; current=None
        for row in rr:
            m=re.match(r'Topic\s*(\d+)\s*(.*)',row.get('A',''),re.I)
            if m:
                current={'id':f'IS-{level}-{m[1]}','course':'iShow','level':level,'number':int(m[1]),'title':m[2],'vocab':[],'structures':[],'focus':[],'source':name}; groups.append(current)
            if current:
                for col,key in [('F','vocab'),('G','structures'),('E','focus')]:
                    if row.get(col): current[key].append(row[col])
        for g in groups:
            source_text=' '.join(g['structures']+g['focus'])
            g['vocab']=word_list(' · '.join(dict.fromkeys(g['vocab'])))
            g['structures']=language_focus(source_text)
            g['focus']=short(g['focus'][0] if g['focus'] else '',180)
        tls+=groups
    else:
        level=re.search(r'PU[1-3]',name).group()
        groups={}
        for row in rr:
            m=re.search(r'Unit\s*(\d+)\s*(?:Lesson\s*\d+)?',row.get('C',''),re.I)
            if not m: continue
            num=int(m[1]); g=groups.setdefault(num,{'id':f'{level}-{num}','course':'Power Up','level':level,'number':num,'title':'','vocab':[],'structures':[],'grammar':[],'focus':[],'source':name})
            for col,key in [('F','vocab'),('G','structures'),('I','grammar'),('E','focus')]:
                if row.get(col): g[key].append(row[col])
        for g in groups.values():
            g['title']=short(g['focus'][0] if g['focus'] else f'Unit {g["number"]}',100)
            source_text=' '.join(g['grammar'])
            g['vocab']=word_list(' · '.join(dict.fromkeys(g['vocab'])))
            g['structures']=language_focus(source_text)
            g['grammar']=g['structures']
            g['focus']=short(g['focus'][0] if g['focus'] else '',180)
        tls+=list(groups.values())
books=[(369,3,'Upper','2024'),(45677,3,'Lower','2025'),(45792,4,'Upper','2025'),(45840,4,'Lower','2026'),(45818,5,'Upper','2026'),(45856,5,'Lower','2026'),(45882,6,'Upper','2026')]
pep=[]
for bid,grade,term,year in books:
    source=(ROOT/'sources'/f'pep-{bid}.html').read_text(encoding='utf-8-sig')
    for m in re.finditer(r'<li>\s*Unit\s*(\d+)\s*([^：<]+)：\s*<a href="([^"]+)"',source,re.I):
        pep.append({'id':f'PEP-{grade}{term[0]}-{m[1]}','grade':grade,'term':term,'year':year,'number':int(m[1]),'title':html.unescape(m[2].strip()),'url':'https://www.ai2book.com'+html.unescape(m[3]),'bookUrl':f'https://www.ai2book.com/diandu/book/{bid}'})
out={'tls':tls,'pep':pep,'notes':{'pepEdition':'2024 revised PEP (three-year starting point); ai2book lists revised books through Grade 6 upper as of 12 Nov 2026. Grade 6 lower is omitted until a revised listing is available.','sourceUrl':'https://www.ai2book.com/diandu/'}}
(ROOT/'data.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(len(tls),'TLS topics/units;',len(pep),'PEP units')
