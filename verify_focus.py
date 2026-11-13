"""Focused data checks for the specific source and comparison errors reported."""
import json
from pathlib import Path

root=Path(__file__).parent
d=json.loads((root/'focus.json').read_text(encoding='utf-8'))
units={u['id']:u for u in d['sourceUnits']}
pep={p['id']:p for p in d['pepUnits']}

def topic(unit,name):return next(c for c in units[unit]['topics'] if c['name']==name)
def texts(rows):return {x['text'].lower() for x in rows}
def source(unit,name):return texts(topic(unit,name)['sourceItems'])

assert list(units)[:2]==['PU1-0','PU1-1']
assert {"what's your name?","i'm (name)."}<=source('PU1-0','Greetings')
assert {'crayon','paper'}<=source('PU1-1','School and learning')
assert {'share','work together'}<=source('PU1-1','Being kind')
assert 'name' not in texts(topic('PU1-1','School and learning')['additions'])
assert 'share' in texts(topic('PU1-1','Being kind')['shared'])
assert {'airport','library'}<=source('IS-Act3-1','Places')
assert {'pilot','librarian','doctor','firefighter'}<=source('IS-Act3-1','Jobs')
assert 'student' not in source('IS-Act3-1','Jobs')
assert 'my name is wu binbin.' in texts(topic('PU1-0','Greetings')['additions'])
assert 'where are you from?' in texts(topic('PU1-0','Greetings')['additions'])
assert all(p['grade']<=4 for p in d['pepUnits'])
for u in d['sourceUnits']:
    for c in u['topics']:
        assert c['sourceItems'],(u['id'],c['name'])
        for r in c['shared']+c['additions']:
            assert pep[r['pepId']]['grade']<=u['gradeMax'],(u['id'],c['name'],r['pepId'])
            assert r['url'].startswith('https://www.ai2book.com/diandu/book/')
            assert r['evidence'] in {'target','main reading/dialogue'}
print('Focused source, alignment, grade-cap and link checks passed.')
