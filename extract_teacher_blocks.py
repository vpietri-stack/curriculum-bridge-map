import glob,json,pathlib,re
R=pathlib.Path(__file__).parent/'sources'/'teacher_ocr'
OUT=pathlib.Path(__file__).parent/'sources'/'teacher_blocks.json'
GROUPS=['PU1a','PU1b','PU2a','PU2b','PU3a','PU3b','PU4']
blocks=[]
for key in GROUPS:
    files=sorted(R.glob(f'{key}_*.json'))
    current=5 if key.endswith('b') else 0
    for file in files:
        page=json.loads(file.read_text(encoding='utf-8')); items=page['items'];texts=[x['text'] for x in items]
        for text in texts:
            m=re.search(r'Unit\s*(\d+)\s*learning\s*outcomes',text,re.I)
            if m:current=int(m[1]);break
        else:
            if any(re.search(r'\bUnit\s*learning\s*outcomes',x,re.I) for x in texts) and not any(re.search('Welcome|Meet Diversicus',x,re.I) for x in texts[:6]):current+=1
        heading=next((x for x in texts[:7] if re.search(r'Vocabulary|Language practice|Cross-curricular|Literature|Communication|Sounds|Grammar',x,re.I)),texts[0] if texts else '')
        new=[x for x in items if re.search(r'^New\s*language',x['text'],re.I)]
        for marker in new:
            x0=marker['box'][0][0];y0=marker['box'][0][1]
            recycled=[x['box'][0][1] for x in items if x['box'][0][1]>y0 and abs(x['box'][0][0]-x0)<60 and re.search(r'^(Recycled\s*language|Materials|Language focus)',x['text'],re.I)]
            y1=min(recycled) if recycled else y0+100
            lines=[x['text'] for x in items if y0<=x['box'][0][1]<y1 and abs(x['box'][0][0]-x0)<90]
            text=' '.join(lines)
            text=re.sub(r'^New\s*language\s*','',text,flags=re.I)
            blocks.append({'level':key[:3],'unit':current,'file':key,'pdfPage':page['pdf_page'],'section':heading,'text':text})
OUT.write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')
from collections import Counter
print('blocks',len(blocks),Counter((x['level'],x['unit']) for x in blocks))
