import json,pathlib,re,zipfile,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).parent
DIR=pathlib.Path(r'G:\My Drive\I2\english teaching\I2\PU - Think\power up 单词表')
FILES={'PU1':'power up 1 单词表.xlsx','PU2':'Power up2 单词表.xlsx','PU3':'power up 3 单词表.xlsx'}
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read(path):
    with zipfile.ZipFile(path) as z:
        ss=[''.join(t.text or '' for t in x.iter('{%s}t'%N['m'])) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        names=[x.get('name') for x in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',N)]
        for sheetno,sheetname in enumerate(names,1):
          path=f'xl/worksheets/sheet{sheetno}.xml'
          if path not in z.namelist():continue
          root=ET.fromstring(z.read(path))
          for row in root.findall('.//m:sheetData/m:row',N):
            d={}
            for c in row.findall('m:c',N):
                v=c.find('m:v',N)
                if v is not None:d[re.match('[A-Z]+',c.get('r')).group()]=ss[int(v.text)] if c.get('t')=='s' else v.text
                elif c.find('m:is',N) is not None:d[re.match('[A-Z]+',c.get('r')).group()]=''.join(x.text or '' for x in c.find('m:is',N).iter('{%s}t'%N['m']))
            yield sheetname,d
out={}
for level,name in FILES.items():
    unit=0; groups={}
    for sheet,row in read(DIR/name):
        sm=re.search(r'Unit\s*(\d+)',sheet,re.I)
        if sm:unit=int(sm[1])
        text=' '.join(row.values())
        m=re.search(r'Unit\s*(\d+)',text,re.I)
        if m and not row.get('D'):unit=int(m[1])
        word=(row.get('D') or '').strip()
        if word and word.lower() not in ['单词','word'] and unit:
            if word not in [x['word'] for x in groups.setdefault(unit,[])]:groups[unit].append({'word':word,'example':row.get('H','')})
    out[level]=groups
    print(level,{n:len(v) for n,v in groups.items()})
(ROOT/'sources'/'wordlist_support.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf-8')
