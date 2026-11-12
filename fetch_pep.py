import concurrent.futures as cf, json, pathlib, requests, time
ROOT=pathlib.Path(__file__).parent
DEST=ROOT/'sources'/'pep_api';DEST.mkdir(parents=True,exist_ok=True)
BOOKS=[369,45677,45792,45840,45818,45856,45882]
def get(url):
    for attempt in range(3):
        try:
            r=requests.get(url,timeout=25);r.raise_for_status();return r.json()
        except Exception:
            if attempt==2:raise
            time.sleep(attempt+1)
def page(task):
    bid,pid=task;path=DEST/f'{bid}_{pid}.json'
    if path.exists():return
    obj=get(f'https://www.ai2book.com/api/v1/reader/books/{bid}/pages/{pid}')
    path.write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8')
tasks=[]
for bid in BOOKS:
    path=DEST/f'{bid}.json'
    if not path.exists():path.write_text(json.dumps(get(f'https://www.ai2book.com/api/v1/reader/books/{bid}'),ensure_ascii=False),encoding='utf-8')
    book=json.loads(path.read_text(encoding='utf-8'))
    print(bid,len(book['pages']),'pages',flush=True)
    tasks += [(bid,p['pid']) for p in book['pages'] if not p.get('missing')]
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    futures=[pool.submit(page,t) for t in tasks]
    for i,f in enumerate(cf.as_completed(futures),1):
        f.result()
        if i%50==0:print(i,'/',len(tasks),flush=True)
