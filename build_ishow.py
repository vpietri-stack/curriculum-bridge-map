import json,pathlib,re,zipfile,xml.etree.ElementTree as ET
BASE=pathlib.Path(r'G:\My Drive\I2\english teaching\I2\curriculum maps')
ROOT=pathlib.Path(__file__).parent
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
FILES=[('Act 3','iShow 2.0 A3 TLS 60 Sessions.xlsx'),('Play 1','iShow 2.0 P1 TLS 60 Sessions.xlsx'),('Play 2','iShow 2.0 P2 TLS 60 Sessions.xlsx'),('Play 3','iShow 2.0 P3 TLS 60 Sessions.xlsx'),('Play 4','iShow 2.0 P4 TLS 60 Sessions.xlsx')]
def rows(path):
 with zipfile.ZipFile(path) as z:
  ss=[''.join(t.text or '' for t in si.iter('{%s}t'%N['m'])) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  root=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
  for row in root.findall('.//m:sheetData/m:row',N):
   out={'row':int(row.get('r'))}
   for c in row.findall('m:c',N):
    v=c.find('m:v',N);inline=c.find('m:is',N)
    if v is not None:val=ss[int(v.text)] if c.get('t')=='s' else v.text
    elif inline is not None:val=''.join(t.text or '' for t in inline.iter('{%s}t'%N['m']))
    else:continue
    out[re.match('[A-Z]+',c.get('r')).group()]=val.strip()
   yield out
def words(s):
 return [re.sub(r'\s+',' ',x).strip(' .;') for x in re.split(r'[,;\n]+',s) if 2<=len(x.strip())<=60]
def structures(s):
 s=re.sub(r'(?m)^\s*[A-Z](?:/[A-Z])?:\s*','',s)
 return [re.sub(r'\s+',' ',x).strip(' .;') for x in re.split(r'[\n]+',s) if 5<=len(x.strip())<=170]
out=[]
for level,filename in FILES:
 current=None
 for row in rows(BASE/filename):
  m=re.match(r'Topic\s*(\d+)\s*(.*)',re.sub(r'\s+',' ',row.get('A','')),re.I)
  if m:
   current={'id':f'IS-{level.replace(" ","")}-{m[1]}','course':'iShow','level':level,'number':int(m[1]),'title':m[2].strip(),'source':filename,'vocabulary':[],'structures':[],'phonics':[]}
   out.append(current)
  if not current or not row.get('C'):continue
  session=row.get('C','');context=re.sub(r'\s+',' ',row.get('E','')).strip()
  for text in words(row.get('F','')):
   kind='phonics' if session.endswith('.5') or re.match(r'^[A-Za-z]{1,2}-[A-Za-z]',text) else 'vocabulary'
   current[kind].append({'text':text,'source':f'{filename}, row {row["row"]}','session':session,'context':context})
  for text in structures(row.get('G','')):
   kind='phonics' if session.endswith('.5') else 'structures'
   current[kind].append({'text':text,'source':f'{filename}, row {row["row"]}','session':session,'context':context})
 for topic in [x for x in out if x['level']==level]:
  for key in ['vocabulary','structures','phonics']:
   seen=set();items=[]
   for item in topic[key]:
    k=item['text'].lower()
    if k not in seen:items.append(item);seen.add(k)
   topic[key]=items
(ROOT/'sources'/'ishow_inventory.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf-8')
print(len(out),'topics',sum(len(x['vocabulary']) for x in out),'vocab entries',sum(len(x['structures']) for x in out),'structure lines',sum(len(x['phonics']) for x in out),'phonics/review items')
