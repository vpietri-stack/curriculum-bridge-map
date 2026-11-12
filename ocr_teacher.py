import argparse,json,pathlib,sys,time
import fitz,numpy as np
from rapidocr_onnxruntime import RapidOCR
ROOT=pathlib.Path(__file__).parent
SOURCES={
 'PU1a':r'G:\My Drive\I2\english teaching\I2\PU - Think\PU1\books\PU1 Teacher Book U1-U5.pdf',
 'PU1b':r'G:\My Drive\I2\english teaching\I2\PU - Think\PU1\books\PU1 Teacher Book U6-U9.pdf',
 'PU2a':r'G:\My Drive\I2\english teaching\I2\PU - Think\PU2\Books\PU 2 Teacher book U1-U5.pdf',
 'PU2b':r'G:\My Drive\I2\english teaching\I2\PU - Think\PU2\Books\PU 2 Teacher book U6-U9.pdf',
 'PU3a':r"G:\My Drive\I2\english teaching\I2\PU - Think\PU3\books\PU 3 Teacher's book unit 1 to 5.pdf",
 'PU3b':r"G:\My Drive\I2\english teaching\I2\PU - Think\PU3\books\PU 3 Teacher's book unit 6 to 9.pdf",
 'PU4':r'G:\My Drive\I2\english teaching\I2\PU - Think\PU4\PU 4 books\PU 4 TB.pdf',
}
ap=argparse.ArgumentParser();ap.add_argument('key',choices=SOURCES);args=ap.parse_args()
dest=ROOT/'sources'/'teacher_ocr';dest.mkdir(parents=True,exist_ok=True)
doc=fitz.open(SOURCES[args.key]);ocr=RapidOCR()
print(args.key,len(doc),'pages',flush=True)
for i in range(len(doc)):
    if i<17 and args.key.endswith('a'):continue
    path=dest/f'{args.key}_{i+1:03}.json'
    if path.exists():continue
    pix=doc[i].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False)
    arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
    result,_=ocr(arr)
    items=[{'text':x[1],'score':round(float(x[2]),3),'box':x[0]} for x in (result or [])]
    path.write_text(json.dumps({'pdf_page':i+1,'items':items},ensure_ascii=False),encoding='utf-8')
    if (i+1)%20==0:print(i+1,'/',len(doc),flush=True)
