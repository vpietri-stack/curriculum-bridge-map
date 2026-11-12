import collections,json,pathlib,re
from difflib import SequenceMatcher
from powerup_patterns import PATTERNS
ROOT=pathlib.Path(__file__).parent; OCR=ROOT/'sources'/'teacher_ocr'
SUPPORT=json.loads((ROOT/'sources'/'wordlist_support.json').read_text(encoding='utf-8'))
KEYS=['PU1a','PU1b','PU2a','PU2b','PU3a','PU3b','PU4']
THEMES=[('Days and time',r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekday|weekend|week|clock|hour|minute|morning|afternoon|evening|night)\b'),('Frequency and routines',r'\b(always|sometimes|usually|often|never|once|twice|ever|daily|routine)\b|how often'),('Hobbies and leisure',r'\b(skate|skating|comic|film|movie|music|sport|dance|swim|swimming|hobby|game|badminton|basketball|football|chess|tennis|shopping)\b'),('Rules and safety',r'\b(must|mustn.t|should|rule|safe|safety|helmet|protect|accident|goggles?|gloves?|pads?)\b'),('Family and friends',r'\b(family|mother|father|parent|grandparent|grandparents|grandma|grandpa|brother|sister|cousin|aunt|uncle|friend)\b'),('Animals and nature',r'\b(animal|farm|dog|cat|bird|fish|bear|lion|tiger|panda|whale|rabbit|forest|river|lake|plant|flower|tree|sea)\b'),('Food and drink',r'\b(food|breakfast|lunch|dinner|eat|drink|bread|rice|fruit|vegetable|milk|tea|coffee|juice|cook|cooking|meal)\b'),('Weather and seasons',r'\b(weather|season|rain|wind|snow|sun|sunny|cloud|spring|summer|autumn|winter|storm)\b'),('Places and travel',r'\b(town|city|country|trip|travel|street|station|museum|airport|hotel|beach|mountain|bus|train|plane)\b'),('School and learning',r'\b(school|class|classroom|teacher|book|lesson|pencil|paper|learn|homework|subject|maths|english|presentation|assembly hall)\b'),('Body and health',r'\b(body|head|face|arm|leg|eye|ear|hand|bone|muscle|health|healthy|exercise|skin|tooth|teeth|doctor)\b'),('Shopping and money',r'\b(shop|shopping|buy|bought|money|price|cost|yuan)\b'),('Feelings and descriptions',r'\b(happy|sad|angry|afraid|excited|beautiful|pretty|big|small|young|old|tall|short)\b'),('Story and narrative',r'\b(suddenly|blanket|leave|lights|mirror|shelf)\b')]
def norm(s):return re.sub('[^a-z0-9]+','',s.lower())
def theme(s):
 n=re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
 special={'feed':'Animals and nature','write an email':'Hobbies and leisure','watch films':'Hobbies and leisure','listen to a cd':'Hobbies and leisure','watch a dvd':'Hobbies and leisure','warm up':'Body and health','sun cream':'Body and health','alarm':'Days and time','outside':'Places and travel','downstairs':'Places and travel','direction':'Places and travel','around':'Places and travel','shelf':'Home and objects','blanket':'Home and objects','lights':'Home and objects','mirror':'Home and objects'}
 if n in special:return special[n]
 for label,pattern in THEMES:
  if re.search(pattern,s,re.I):return label
 return 'Other unit vocabulary'
def item_pages(pages,term):
 needle=norm(term)
 if not needle:return []
 exact=[p for p in pages if needle in p['norm']]
 if exact:return exact
 if len(needle)<5:return []
 return [p for p in pages if any(SequenceMatcher(None,needle,norm(line)).ratio()>.88 for line in p['lines'] if len(norm(line))<len(needle)+8)]
units={}
for key in KEYS:
 level=key[:3];current=5 if key.endswith('b') else 0
 for f in sorted(OCR.glob(f'{key}_*.json')):
  page=json.loads(f.read_text(encoding='utf-8'));lines=[x['text'] for x in page['items']]
  for line in lines:
   m=re.search(r'Unit\s*(\d+)\s*learning\s*outcomes',line,re.I)
   if m:current=int(m[1]);break
  else:
   if any(re.search(r'\bUnit\s*learning\s*outcomes',x,re.I) for x in lines) and not any(re.search('Welcome|Meet Diversicus',x,re.I) for x in lines[:6]):current+=1
  if current==0:continue
  u=units.setdefault((level,current),{'id':f'{level}-{current}','course':'Power Up','level':level,'number':current,'title':'','vocabulary':[],'structures':[],'source':'Teacher Book','pages':[]})
  if any(re.search(r'Unit\s*'+str(current)+r'\s*learning\s*outcomes|\bUnit\s*learning\s*outcomes',x,re.I) for x in lines):u['title']=lines[0]
  u['pages'].append({'file':key,'pdfPage':page['pdf_page'],'lines':lines,'norm':norm(' '.join(lines))})
for (level,num),u in units.items():
 if not u['title']:u['title']=f'Unit {num}'
 for record in SUPPORT.get(level,{}).get(str(num),[]):
  term=record['word'].strip()
  matches=item_pages(u['pages'],term)
  if not matches:continue
  p=matches[0]
  u['vocabulary'].append({'text':term,'theme':theme(term),'source':f'{p["file"]} Teacher Book, scan p. {p["pdfPage"]}','evidence':'teacher book + word list check'})
blocks=json.loads((ROOT/'sources'/'teacher_blocks.json').read_text(encoding='utf-8'))
for b in blocks:
 u=units.get((b['level'],b['unit']))
 if not u:continue
 source=f'{b["file"]} Teacher Book, scan p. {b["pdfPage"]}'
 text=b['text'].strip(); section=b['section']
 if re.search('Language practice|Grammar',section,re.I):
  parts=[x.strip() for x in re.split(r'(?<=[?!])\s*|(?<=\.)\s+',text) if len(x.strip())>=8]
  for part in parts:
   if not re.search(r'[?.!]$',part):continue
   if len(part)>180:part=part[:180].rsplit(' ',1)[0]
   u['structures'].append({'text':part,'concept':section,'source':source,'evidence':'teacher book new language'})
 elif b['level']=='PU4':
  for part in re.split(r'[,;]+',text):
   term=part.strip(' .')
   if not (3<=len(term)<=32) or re.search(r'[?!]',term):continue
   if re.search(r'[^a-zA-Z\s/()\-]',term):continue
   if not any(norm(x['text'])==norm(term) for x in u['vocabulary']):
    u['vocabulary'].append({'text':term,'theme':theme(term),'source':source,'evidence':'teacher book new language OCR'})
for unit_id,sections in PATTERNS.items():
 level,num=unit_id.split('-');u=units.get((level,int(num)))
 if not u:continue
 u['structures']=[]
 for section_index,(concept,patterns) in enumerate(sections,1):
  grammar_blocks=[b for b in blocks if b['level']==level and b['unit']==int(num) and re.search(r'Language\s*practice|Grammar spotlight|Grammar reference',b['section'],re.I)]
  source_block=grammar_blocks[section_index-1] if len(grammar_blocks)>=section_index else None
  source=f"{source_block['file']} Teacher Book, scan p. {source_block['pdfPage']}" if source_block else 'Teacher Book unit overview'
  for pattern in patterns:u['structures'].append({'text':pattern,'concept':concept,'source':source,'evidence':'edited teaching pattern based on teacher book'})
for u in units.values():
 titles={'PU1-3':'Fun on the farm','PU3-4':'Fun in the jungle','PU4-2':'Our beautiful planet','PU4-3':"Let's celebrate!",'PU4-4':'Time of our lives','PU4-8':'Space travel','PU4-9':'Great bakers'}
 u['title']=titles.get(u['id'],u['title'])
 replacements={'go sking':['go skiing'],'push street':['push','street'],'writer moon':['writer','moon'],'harm in amazement':['harm','in amazement'],'sledge (n) snowball':['sledge','snowball'],'science fiction scientist':['science fiction','scientist'],'hourglass hunt':['hourglass','hunt'],'flour honey':['flour','honey'],'give out handbag':['give out','handbag'],'forsure':['for sure']}
 remove={'indefinite pronouns','past simple','past continuous','tag questions','short questions'}
 if u['level']=='PU4':
  fixed=[]
  for item in u['vocabulary']:
   if item['text'].lower() in remove:continue
   for term in replacements.get(item['text'].lower(),[item['text']]):fixed.append({**item,'text':term,'theme':theme(term)})
  u['vocabulary']=fixed
 del u['pages']
 for key in ['vocabulary','structures']:
  seen=set();out=[]
  for item in u[key]:
   k=norm(item['text'])
   if k not in seen:seen.add(k);out.append(item)
  u[key]=out
out=sorted(units.values(),key=lambda x:(int(x['level'][-1]),x['number']))
(ROOT/'sources'/'powerup_inventory.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf-8')
print('units',len(out),'vocab',sum(len(x['vocabulary']) for x in out),'structures',sum(len(x['structures']) for x in out))
print([(x['id'],x['title'],len(x['vocabulary']),len(x['structures'])) for x in out])
