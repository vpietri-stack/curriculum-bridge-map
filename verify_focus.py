"""Focused data checks for the specific source and comparison errors reported."""
import json
from pathlib import Path
from focus_alignment import relation, vocab_in_structure

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
assert 'k-kick' in source('IS-Act3-1','Phonics')
assert not any('firefighter' in s or 'where is the' in s for s in source('IS-Act3-1','Phonics'))
assert {'pilot','librarian','doctor','firefighter'}<=source('IS-Act3-1','Jobs')
assert 'student' not in source('IS-Act3-1','Jobs')
assert 'my name is wu binbin.' in texts(topic('PU1-0','Greetings')['additions'])
assert 'where are you from?' in texts(topic('PU1-0','Greetings')['additions'])
assert 'colour' in texts(topic('PU1-0','Colours')['shared'])
assert 'old' in texts(topic('PU1-0','Numbers and age')['shared'])
assert 'nice' in texts(topic('IS-Play1-1','Greetings')['shared'])
assert 'nice' not in texts(topic('IS-Play1-1','Greetings')['additions'])
jobs=topic('IS-Act3-1','Jobs')
assert "she's a doctor." in texts(jobs['shared'])
assert "she's a teacher." in texts(jobs['shared'])
assert "he's a pe teacher." in texts(jobs['additions'])
assert "she's a nurse." not in texts(jobs['shared'])
assert relation("He/She's a (guide)","She's a doctor.",'structure','jobs',{'guide','doctor'},{'guide','doctor'})=='exact'
assert relation("He/She's a (guide)","She's a nurse.",'structure','jobs',{'guide','doctor'},{'guide','doctor'}) is None
assert relation("It's (blue).","It's healthy.",'structure','health',{'blue','healthy'},{'healthy'}) is None
assert "it's healthy." in texts(topic('PU1-7','Healthy body')['additions'])
assert 'where are you from?' in texts(topic('IS-Play1-1','Greetings')['additions'])
assert "i'm from the uk." in texts(topic('IS-Play1-1','Greetings')['additions'])
assert {'ten','six','seven','eight'}<=texts(topic('IS-Play1-1','Numbers and age')['shared'])
assert 'nine' in texts(topic('IS-Play1-1','Numbers and age')['additions'])
assert not any('want to play' in s for s in source('IS-Act3-3','Numbers and age'))
assert not any(x['sourceMatch'] and 'phone call' in x['sourceMatch'].lower() for u in d['sourceUnits'] for c in u['topics'] for x in c['shared'])
assert all(units[k]['gradeMax']==4 for k in ('PU1-0','IS-Act3-1','IS-Play1-1'))
assert any(r['pepId'].startswith('PEP-4') for c in units['IS-Act3-1']['topics'] for r in c['shared']+c['additions'])
assert all(p['grade']<=4 for p in d['pepUnits'])
paths={'Power Up':[],'iShow':[]}
for u in d['sourceUnits']:
    known=list(paths[u['course']])
    for c in u['topics']:
        assert c['sourceItems'],(u['id'],c['name'])
        known+=c['sourceItems']
        spoken=[x['text'] for x in known if x['type']=='structure']
        for r in c['additions']:
            if r['type']=='vocab':
                assert not any(vocab_in_structure(s,r['text']) for s in spoken),(u['id'],c['name'],r['text'])
        for r in c['shared']+c['additions']:
            assert pep[r['pepId']]['grade']<=u['gradeMax'],(u['id'],c['name'],r['pepId'])
            assert r['url'].startswith('https://www.ai2book.com/diandu/book/')
            assert r['evidence'] in {'target','main reading/dialogue'}
    paths[u['course']]+=list(x for c in u['topics'] for x in c['sourceItems'])
print('Focused source, alignment, grade-cap and link checks passed.')
