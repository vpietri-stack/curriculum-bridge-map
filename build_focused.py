"""Build the editorial topic-card edition without discarding the full catalog."""
import json,pathlib,re,collections
from focus_topics import PU1_PANEL_TOPICS,PU1_WELCOME,PU1_OCR_FIXES,PU1_EXTRA_PATTERNS,ISHOW_TOPIC_ORDER,TOPIC_TAGS
from powerup_patterns import PATTERNS

ROOT=pathlib.Path(__file__).parent
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def norm(s):return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def unique(rows):
 seen=set();out=[]
 for row in rows:
  k=(row['type'],norm(row['text']))
  if k not in seen:seen.add(k);out.append(row)
 return out
def item(text,kind,source,page=None,session=None):
 return {'text':text.strip(),'type':kind,'source':source,'page':page,'session':session}
def card(name,tag):return {'name':name,'tag':tag,'sourceItems':[],'sourceSections':[]}

blocks=read(ROOT/'sources'/'teacher_blocks.json')
full=read(ROOT/'catalog.json')
def add_card(unit,name,tag=None):
 for c in unit['topics']:
  if c['name']==name:return c
 c=card(name,tag or TOPIC_TAGS.get(name,'story'));unit['topics'].append(c);return c

def split_block(text):
 for wrong,right in PU1_OCR_FIXES.items():text=re.sub(r'(?<![A-Za-z])'+re.escape(wrong)+r'(?![A-Za-z])',lambda m:right,text)
 text=text.replace('hockey ride a skateboard','hockey, ride a skateboard')
 out=[]
 for part in re.split(r'[,;]+',text):
  p=re.sub(r'\s+',' ',part).strip(' .')
  if not 2<=len(p)<=70:continue
  if re.search(r'\b(e\.g|article \+|adjective \+|irregular|imperatives|grammar)\b',p,re.I):continue
  if not re.search(r'[a-zA-Z]',p) or norm(p) in {'oh','yes'}:continue
  if '?' in p or '!' in p or '...' in p or norm(p) in {'thank you','here you are','i m sorry'} or re.search(r"\b(I|You|We|He|She|They)\b.*\b(is|are|can|got|like|do)\b",p):kind='structure'
  else:kind='vocab'
  if len(p)>45 and kind=='vocab':continue
  out.append((p,kind))
 return out

def build_pu1():
 out=[]
 welcome={'id':'PU1-0','course':'Power Up','level':'PU1','number':0,'title':'Hello','gradeMax':4,'source':'PU1 Teacher’s Book, welcome unit','topics':[]}
 for entry in PU1_WELCOME:
  c=add_card(welcome,entry['name'],entry['tag'])
  c['sourceSections']=[f"Teacher Book scan pp. {', '.join(map(str,entry['pdfPages']))}"]
  c['sourceItems']=[item(w,'vocab',c['sourceSections'][0],entry['pdfPages'][0]) for w in entry['words'].split(', ')]
  c['sourceItems'] += [item(s,'structure',c['sourceSections'][0],entry['pdfPages'][-1]) for s in entry['structures']]
 out.append(welcome)
 titles={x['number']:x['title'] for x in full['units'] if x['course']=='Power Up' and x['level']=='PU1'}
 for n in range(1,10):
  u={'id':f'PU1-{n}','course':'Power Up','level':'PU1','number':n,'title':titles[n],'gradeMax':4,'source':'PU1 Teacher’s Book','topics':[]}
  panels=[b for b in blocks if b['level']=='PU1' and b['unit']==n]
  names=PU1_PANEL_TOPICS[n]
  assert len(panels)==len(names),(n,len(panels),len(names))
  lp_index=0
  for b,name in zip(panels,names):
   c=add_card(u,name)
   src=f"{b['file']} Teacher Book, scan p. {b['pdfPage']} ({b['section']})"
   if src not in c['sourceSections']:c['sourceSections'].append(src)
   if re.search(r'Language\s*practice',b['section'],re.I):
    lp_index+=1
    concept,patterns=PATTERNS[u['id']][lp_index-1]
    c['sourceItems'] += [item(p,'structure',src,b['pdfPage']) for p in patterns]
   else:
    c['sourceItems'] += [item(text,kind,src,b['pdfPage']) for text,kind in split_block(b['text'])]
  for (unit_no,name),patterns in PU1_EXTRA_PATTERNS.items():
   if unit_no!=n:continue
   c=add_card(u,name)
   src=next((s for s in c['sourceSections'] if 'Cross-curricular' in s or 'Language' in s),c['sourceSections'][0])
   m=re.search(r'scan p\. (\d+)',src);page=int(m[1]) if m else None
   c['sourceItems'] += [item(p,'structure',src,page) for p in patterns]
  for c in u['topics']:c['sourceItems']=unique(c['sourceItems'])
  if n==1:
   story=add_card(u,'Classroom story')
   story['sourceItems'].append(item('Oh, yes.','structure',story['sourceSections'][-1],40))
  if n==2:
   c=add_card(u,'Family')
   c['sourceItems']=[x for x in c['sourceItems'] if norm(x['text']) not in {'he s she s','she he'}]
   c['sourceItems'].append(item("He’s my (brother). / She’s my (sister).",'structure',c['sourceSections'][1],None))
   eggs=[x for x in c['sourceItems'] if norm(x['text'])=='eggs']
   c['sourceItems']=[x for x in c['sourceItems'] if norm(x['text'])!='eggs']
   if eggs:
    farm=add_card(u,'Farm story','story');farm['sourceItems']+=eggs;farm['sourceSections']+=list(dict.fromkeys(x['source'] for x in eggs))
  if n==5:
   c=add_card(u,'Birthday story')
   c['sourceItems']=[x for x in c['sourceItems'] if norm(x['text'])!='can i have']
  if n==6:
   c=add_card(u,'There is and there are')
   c['sourceItems']=[x for x in c['sourceItems'] if norm(x['text']) not in {'there is are','there isn t aren t','idon t know'}]
   c['sourceItems'].append(item("I don’t know.",'structure',c['sourceSections'][0],None))
   town=add_card(u,'Town and transport')
   plants=[x for x in town['sourceItems'] if norm(x['text']) in {'flower','garden','tree'}]
   town['sourceItems']=[x for x in town['sourceItems'] if x not in plants]
   if plants:
    nature=add_card(u,'Plants in town','nature');nature['sourceItems']+=plants;nature['sourceSections']+=list(dict.fromkeys(x['source'] for x in plants))
  if n==7:
   c=add_card(u,'Actions now')
   c['sourceItems']=[x for x in c['sourceItems'] if norm(x['text']) not in {'iam ing','they are yes'}]
   c['sourceItems'].append(item("I’m (painting). / They’re (singing).",'structure',c['sourceSections'][0],None))
  if n==8:
   ability=add_card(u,'Ability')
   ability['sourceItems'] += [item(s,'structure',ability['sourceSections'][0],58) for s in ['I can (dance).','Can you (dance)?','Yes, I can.','No, I can’t.']]
   days=add_card(u,'Days and time')
   src=days['sourceSections'][0]
   days['sourceItems'] += [item(w,'vocab',src,59) for w in ['morning','afternoon','evening','Saturday','Sunday']]
  if n==9:
   c=add_card(u,'Actions and imperatives')
   c['sourceItems']=[x for x in c['sourceItems'] if 'toble' not in x['text'].lower()]
   land=add_card(u,'Landscapes')
   travel=[x for x in land['sourceItems'] if norm(x['text']) in {'hotel','stay in'}]
   land['sourceItems']=[x for x in land['sourceItems'] if x not in travel]
   if travel:
    holiday=add_card(u,'Holiday travel','transport');holiday['sourceItems']+=travel;holiday['sourceSections']+=list(dict.fromkeys(x['source'] for x in travel))
  for c in u['topics']:c['sourceItems']=unique(c['sourceItems'])
  out.append(u)
 return out

PLACES={'airport','library','supermarket','zoo','museum','bakery','fire station','hospital','toy store','police station','playground','restaurant','toy shop'}
JOBS={'pilot','librarian','shop assistant','zookeeper','guide','baker','firefighter','doctor','cashier','police officer','teacher'}
SCHOOL={'classroom','classmate','chair','board','eraser','glue stick','notebook','crayon','marker','book','backpack','pen','pencil','pencil case','ruler'}
COLOURS={'red','yellow','blue','green','orange','purple','pink','white','black','brown','grey'}
FAMILY={'family','mom','mum','dad','father','mother','sister','brother','grandma','grandpa'}
WEATHER={'rainy','sunny','windy','cloudy','snowy','warm','hot','cold'}
TRANSPORT={'train','bus','car','plane','bike','taxi','metro','boat','scooter','skateboard'}
ANIMALS={'monkey','parrot','panda','elephant','giraffe','alligator','rhino','tiger','frog','horse','snake','turtle','bear','bird','fish','dinosaur'}
FOOD={'sandwiches','oranges','donuts','ice cream','cupcake','cupcakes','rice','noodles','salad','soup','hamburger','cake','bread','pizza','apples','eggs','cookies','hot dogs','bananas','hamburgers','milk','vegetables','fruit'}
TOYS={'blocks','boat','train','board game','robot','balloon','plane','dinosaur','ball','doll','teddy bear','truck','top','kite','rocket','toy'}
SPORT={'soccer','basketball','tennis','ping-pong','hide-and-seek','jump rope','tag','slide','swing','jungle gym','seesaw','sand box','sport'}
CLOTHES={'pants','jacket','dress','sunglasses','raincoat','suitcase','hat'}
BODY={'bones','horns','wings','claws','teeth','fins','tail'}

def choose_available(u,*names):
 available=ISHOW_TOPIC_ORDER.get(u['id'],[])
 return next((name for name in names if name in available),None)
def classify_word(u,x):
 s=norm(x['text'])
 if s in {'hide and seek','ping pong'}:return choose_available(u,'Playground','Sport and music')
 if s in {'ok1'}:return 'DROP'
 if s=='playground':return choose_available(u,'Playground')
 if s in {'rock','water','log'}:return choose_available(u,'Nature','Beach activities','Position')
 if s in {'first','then','later','at last'}:return choose_available(u,'Sequencing','Cooking and ingredients')
 if s=='play':return choose_available(u,'Toys and presents','Sport and music')
 if s in COLOURS:return choose_available(u,'Colours','Descriptions')
 if s in JOBS:return choose_available(u,'Jobs','School objects','Community')
 if s in PLACES:return choose_available(u,'Places','Museum','Travel','School objects','Zoo animals')
 if s in FAMILY:return choose_available(u,'Family')
 if s in WEATHER:return choose_available(u,'Weather')
 if re.fullmatch(r'\d+',s) or s in {'monday','tuesday','wednesday','thursday','friday','saturday','sunday'}:return choose_available(u,'Days and time','Numbers and age')
 if s in SCHOOL:return choose_available(u,'School objects','Naming objects')
 if s in CLOTHES:return choose_available(u,'Clothes','Shopping','Travel')
 if s in TOYS:return choose_available(u,'Toys and presents','Shopping','Travel')
 if s in ANIMALS:return choose_available(u,'Zoo animals','Farm animals','Dinosaurs','Nature','Animal actions','Beach activities')
 if s in FOOD:return choose_available(u,'Food and drink','Food preferences','Food requests','Healthy body')
 if s in TRANSPORT:return choose_available(u,'Travel','Town and transport','Toys and presents')
 if s in SPORT:return choose_available(u,'Playground','Sport and music','Beach activities')
 if s in BODY:return choose_available(u,'Dinosaurs','Zoo animals','Nature')
 if s in {'morning','afternoon','evening','name','your','my','fine','ok'}:return choose_available(u,'Greetings','Days and time')
 if s in {'quiet','run','walk','open','close','pick'}:return choose_available(u,'Rules','Animal actions')
 if s in {'flower','tree','bug','garden','sea','shells','rocks','rock','water','grass','log'}:return choose_available(u,'Nature','Beach activities','Dinosaurs','Zoo animals')
 if s in {'under','behind','on','in'}:return choose_available(u,'Position')
 if s in {'big','small','fast','faster','long','longer','short','shorter','slow','slower'}:return choose_available(u,'Descriptions','Nature','Dinosaurs','Beach activities')
 if s in {'jump','fly','swim','climb','eat','swing'}:return choose_available(u,'Animal actions','Sport and music','Beach activities')
 if s in {'wash your hands','roll the dough','cut into shapes','bake','decorate','first','then','later','at last'}:return choose_available(u,'Cooking and ingredients','Sequencing')
 if s in {'this','that'}:return choose_available(u,'Naming objects','School objects')
 if s in {'by','need'}:return choose_available(u,'Travel')
 return None

def classify_structure(u,x):
 s=norm(x['text'])
 if u['id']=='IS-Act3-3':
  return 'Numbers and age' if re.search(r'how many|there are [0-9]|there is [0-9]',s) else 'Playground'
 if u['id']=='IS-Act3-5':
  if s.endswith('thank you'):return 'Opening and review'
  if re.search(r'how many|there are [0-9]|there is [0-9]|there are (one|two|three|four|five)|\bi have [0-9]',s):return 'Numbers and age'
  if re.search(r'which one do you like|how much|\bbuy\b|\bplease\b',s):return 'Shopping'
  return 'Toys and presents'
 if s.startswith('this is student'):return choose_available(u,'Greetings') or 'Opening and review'
 if (re.search(r'hello|^hi\b|good morning|nice to meet|your name|my name|how are you|i m fine',s) and not re.search(r'our library|fire station|hospital|toy store',s)) or re.search(r'^(thank you|goodbye|i m ok|yes thank you)\b',s) or s.endswith('thank you'):return choose_available(u,'Greetings') or 'Opening and review'
 if re.search(r'what does .* do|he s a (pilot|cashier|guide|teacher)|who are you going to see|going to see|see a (guide|pilot|librarian)',s):return choose_available(u,'Jobs')
 if re.search(r'how s the weather|it s (rainy|sunny|windy|cloudy|snowy)|weather in',s):return choose_available(u,'Weather')
 if re.search(r'what are you wearing|i m wearing',s):return choose_available(u,'Clothes')
 if re.search(r'where is|next to|under the|behind|on the|in the',s):return choose_available(u,'Position','Places','Museum','Zoo animals')
 if re.search(r'where are you going|going to the|how do .* go|take the (bus|metro|taxi)|go to .* by',s):return choose_available(u,'Travel','Places','Museum')
 if re.search(r'what.*job|doctor|teacher|firefighter|librarian',s):return choose_available(u,'Jobs','School objects')
 if re.search(r'be quiet|don t run|walk slowly|open your|close your|pick up',s):return choose_available(u,'Rules')
 if re.search(r'how old|years old|how many|there are [0-9]|there is [0-9]',s):return choose_available(u,'Numbers and age','Playground','Toys and presents')
 if re.search(r'what colour|red|blue|yellow|green|orange|purple|pink|white|black|brown',s):return choose_available(u,'Colours')
 if re.search(r'family|my mom|my dad|my sister|my brother',s):return choose_available(u,'Family')
 if re.search(r'what.*eat|like.*(pizza|bread|cake|fruit)|do you like|i don t like',s):return choose_available(u,'Food preferences','Food and drink')
 if re.search(r'can i have|what do you want to eat|here you are',s):return choose_available(u,'Food requests','Shopping')
 if re.search(r'make cookies|wash your hands|roll the dough|cut into shapes|decorate',s):return choose_available(u,'Cooking and ingredients')
 if re.search(r'^first\b|^then\b|^later\b|^at last\b',s):return choose_available(u,'Sequencing')
 if re.search(r'can .* (jump|fly|swim|run|climb|eat)|monkeys can|parrots can',s):return choose_available(u,'Animal actions','Zoo animals')
 if re.search(r'this dinosaur|these dinosaurs|dinosaur has|dinosaur',s):return choose_available(u,'Dinosaurs')
 if re.search(r'what s this|what s that|this is a|that s a',s):return choose_available(u,'Naming objects','Zoo animals','School objects')
 if re.search(r'i have a|who has a|what do you have|there is a .*toy',s):return choose_available(u,'Toys and presents','Possession')
 if re.search(r'slide|swing|playground|jump rope|play tag|playing',s):return choose_available(u,'Playground','Sport and music','Beach activities')
 if re.search(r'can .* buy|which one do you like|please$',s):return choose_available(u,'Shopping','Toys and presents')
 if re.search(r'i see|what do you see',s):return choose_available(u,'Travel','Museum','Zoo animals')
 return None

def build_ishow():
 out=[]
 for raw in read(ROOT/'sources'/'ishow_inventory.json'):
  if raw['level'] not in ('Act 3','Play 1'):continue
  u={k:raw[k] for k in ('id','course','level','number','title','source')}
  u['gradeMax']=4;u['topics']=[]
  for name in ISHOW_TOPIC_ORDER[u['id']]:add_card(u,name)
  review=[]
  # The TLS phonics cell also repeats ordinary lesson dialogue after the
  # sound/blend material. Keep only the phonics prefix, including its chants.
  structures={norm(x['text']) for x in raw['structures']}
  phonics_cutoff=next((i for i,x in enumerate(raw['phonics']) if norm(x['text']) in structures),len(raw['phonics']))
  phonics_cutoff=min(phonics_cutoff,{'IS-Play1-5':5,'IS-Play1-8':6}.get(u['id'],phonics_cutoff))
  for field,kind in (('vocabulary','vocab'),('structures','structure'),('phonics','phonics')):
   for i,x in enumerate(raw[field]):
    if kind=='vocab' and norm(x['text'])=='ok1':continue
    if kind=='structure' and '_' in x['text']:continue
    if kind=='structure' and norm(x['text']) in {'this is','that s','there is a','there are'}:continue
    if kind=='phonics' and i>=phonics_cutoff:continue
    if str(x.get('session','')).startswith('10.'):review.append((x,kind));continue
    name='Phonics' if kind=='phonics' else classify_word(u,x) if kind=='vocab' else classify_structure(u,x)
    if not name:
     session=str(x.get('session','')).split('.')[-1]
     order=[t for t in ISHOW_TOPIC_ORDER[u['id']] if t!='Phonics']
     name=order[min(max(int(session or '1')-1,0),len(order)-1)] if order else 'Stories and review'
    c=add_card(u,name)
    src=x['source']
    if src not in c['sourceSections']:c['sourceSections'].append(src)
    corrected=x['text'].replace('deorations','decorations')
    c['sourceItems'].append(item(corrected,kind,src,None,x.get('session')))
  for c in u['topics']:c['sourceItems']=unique(c['sourceItems'])
  u['topics']=[c for c in u['topics'] if c['sourceItems']]
  u['topics'].sort(key=lambda c:2 if c['name']=='Phonics' else 1 if c['name']=='Opening and review' else 0)
  out.append(u)
  if review:
   r={'id':u['id'].rsplit('-',1)[0]+'-review','course':'iShow','level':u['level'],'number':10,'title':'Review and project','gradeMax':u['gradeMax'],'source':u['source'],'topics':[card('Stories and review','story')]}
   c=r['topics'][0]
   for x,kind in review:
    if x['source'] not in c['sourceSections']:c['sourceSections'].append(x['source'])
    c['sourceItems'].append(item(x['text'],kind,x['source'],None,x.get('session')))
   c['sourceItems']=unique(c['sourceItems']);out.append(r)
 return out

if __name__=='__main__':
 source=build_pu1()+build_ishow()
 out={'sourceUnits':source,'pepUnits':[p for p in full['pep'] if p['grade']<=4]}
 (ROOT/'focus_sources.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 print('units',len(source),'topics',sum(len(u['topics']) for u in source),'source items',sum(len(c['sourceItems']) for u in source for c in u['topics']))
 print([(u['id'],len(u['topics']),sum(len(c['sourceItems']) for c in u['topics'])) for u in source])
