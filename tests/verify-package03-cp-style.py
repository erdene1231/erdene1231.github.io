"""Check lexical refactoring, all complete C++ programs, literal samples and independent representative oracles."""
import bisect, collections, concurrent.futures, heapq, json, random, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from package03_cp_style import code_blocks,identifiers,rename,stable_hash
source=Path(sys.argv[1])if len(sys.argv)>1 else Path('/workspace/package02-cp-style-before/catalog-recovery.json')
old={r['id']:r['body']for r in json.loads(source.read_text())['tutorials']};out=Path('/workspace/package03-cp-style-test');out.mkdir(exist_ok=True)
records=[];jobs=[]
for f in sorted((ROOT/'audit/package03-cp-style').glob('*.json')):
 d=json.loads(f.read_text());body=d['body'];mapping=d['mapping'];ids=set().union(*(identifiers(b['text'])for b in code_blocks(old[d['id']])))
 assert len(set(mapping.values()))==len(mapping) and not(set(mapping.values())&ids)
 for lang in ['mn','en']:
  a=old[d['id']]if lang=='mn'else old[d['id']]['translations']['en'];b=body if lang=='mn'else body['translations']['en'];before=code_blocks(a);after=code_blocks(b)
  assert len(before)==len(after)
  for x,y in zip(before,after):assert rename(x['text'],mapping)==y['text'],d['id']
  for s in b['sections']:
   pieces=[]
   for block in s['blocks']:
    if block.get('language')!='C++17':continue
    code=block['text']
    if '#include' in code and 'int main('in code and code.count('{')==code.count('}') and code.rstrip().endswith('}'):
     assert any(''.join(pieces[j:])==code for j in range(len(pieces))),(d['id'],'fragments');pieces=[]
    else:pieces.append(code)
 for k,v in old[d['id']].items():
  if k not in ['sections','translations']:assert body[k]==v,(d['id'],k)
 assert stable_hash(body)==d['reviewed_body_sha256']
 programs=[]
 for sec in body['sections']:
  for i,b in enumerate(sec['blocks']):
   if b.get('language')=='C++17' and '#include' in b.get('text','')and 'int main('in b['text'] and b['text'].count('{')==b['text'].count('}') and b['text'].rstrip().endswith('}'):
    samples=[];inp=''
    for n in sec['blocks'][i+1:]:
     if n.get('language')=='C++17':break
     if n.get('language')=='Input':inp=n['text']
     if n.get('language')=='Output':samples.append((inp,n['text']));inp=''
    programs.append((b['text'],samples))
 records.append({'id':d['id'],'changed':d['changed'],'renamed_identifiers':len(mapping),'programs':len(programs),'injective_identifier_only':True,'MN_EN_fragments_exact':True,'metadata_preserved':True})
 if d['changed']:
  for i,(code,samples)in enumerate(programs):jobs.append((d['id'],i,code,samples))

def run(exe,inp):return subprocess.run([str(exe)],input=inp,capture_output=True,text=True,check=True,timeout=10).stdout.split()
def check(job):
 id,i,code,samples=job;src=out/f'{id}-{i}.cpp';exe=out/f'{id}-{i}';src.write_text(code)
 built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(src),'-o',str(exe)],capture_output=True,text=True)
 assert built.returncode==0,(id,built.stderr);assert not built.stderr,(id,built.stderr)
 for inp,expected in samples:assert run(exe,inp)==expected.split(),(id,'sample')
 return {'id':id,'program':i,'sha256':stable_hash(code),'samples':len(samples),'warnings':0}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:results=list(pool.map(check,jobs))
rng=random.Random(20261028);oracle=[]
for id in ['binary-search','dsu','dijkstra']:
 exe=out/f'{id}-0';cases=0
 for _ in range(100):
  if id=='binary-search':
   a=sorted(rng.choices(range(-100,101),k=rng.randrange(80)));queries=[rng.randrange(-110,111)for _ in range(30)];inp=f'{len(a)}\n'+ ' '.join(map(str,a))+'\n30\n'+'\n'.join(map(str,queries));expected=[str(bisect.bisect_left(a,x))for x in queries]
  elif id=='dsu':
   n=rng.randrange(1,30);edges=[(rng.randrange(n),rng.randrange(n))for _ in range(60)];groups=[{i}for i in range(n)];expected=[]
   for u,v in edges:
    a=next(s for s in groups if u in s);b=next(s for s in groups if v in s)
    if a is not b:groups.remove(a);groups.remove(b);groups.append(a|b)
    expected.extend([str(len(groups)),str(max(map(len,groups)))])
   inp=f'{n} {len(edges)}\n'+'\n'.join(f'{u+1} {v+1}'for u,v in edges)
  else:
   n=rng.randrange(1,20);edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(30))for _ in range(60)];dist=[10**30]*n;dist[0]=0
   for _ in range(n-1):
    for u,v,w in edges:
     if dist[u]+w<dist[v]:dist[v]=dist[u]+w
   expected=[str(d)if d<10**30 else '-1'for d in dist];inp=f'{n} {len(edges)}\n'+'\n'.join(f'{u+1} {v+1} {w}'for u,v,w in edges)
  assert run(exe,inp)==expected,(id,inp);cases+=1
 oracle.append({'lesson':id,'cases':cases,'independent_reference':{'binary-search':'Python bisect','dsu':'Explicit component sets','dijkstra':'Repeated Bellman-Ford relaxation'}[id]})
report={'status':'passed','reviewed_lessons':len(records),'changed_lessons':sum(r['changed']for r in records),'unchanged_lessons':[r['id']for r in records if not r['changed']],'compiled_programs':len(results),'sample_runs':sum(r['samples']for r in results),'representative_oracles':oracle,'programs':results,'lessons':records,'scope':'Exact injective identifier renaming only in code; all strings/comments/operators/control flow preserved. Samples plus three independent representative oracles. Existing broader algorithm evidence remains applicable; no new blanket solution audit.'}
(ROOT/'audit/PACKAGE03-CP-STYLE-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['programs','lessons']}))
