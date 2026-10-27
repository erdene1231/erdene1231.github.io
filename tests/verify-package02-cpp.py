"""Validate the32reviewed blocks via8identical MN/EN programs and helper prefixes."""
import concurrent.futures,hashlib,json,math,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Apply only local guarded proposals, never publish them.
result=subprocess.run(['node','--input-type=module','-e',"import fs from'node:fs';import{proposedTutorialRows}from'./tools/package02_tutorial_proposals.mjs';process.stdout.write(JSON.stringify(proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials)));"],cwd=ROOT,capture_output=True,text=True,check=True)
rows=json.loads(result.stdout);original_ids={'dynamic-programming','dsu','fenwick-tree','graph-basics','lazy-segment-tree','number-theory','segment-tree','two-pointers'};ids=[p['id']for p in json.loads((ROOT/'audit/PACKAGE02-TUTORIAL-PROPOSALS.json').read_text())['patches']if p['id']in original_ids];assert set(ids)==original_ids;rng=random.Random(41027);reports=[]
with tempfile.TemporaryDirectory(prefix='part04-tutorial-cpp-')as td:
 def build(id):
  d=next(r['body']for r in rows if r['body']['id']==id);codes=lambda v:[b['text']for s in v['sections']for b in s['blocks']if b['type']=='code'and b.get('language')=='C++17'];mn,en=codes(d),codes(d['translations']['en']);assert mn==en and len(mn)==2,id;snippet,program=mn;assert program[:program.index('int main(')].strip()==snippet.strip(),id
  assert '\t' not in program;assert all(not line.startswith(' ')or(len(line)-len(line.lstrip()))%4==0 for line in program.splitlines()),id
  src=Path(td)/(id+'.cpp');exe=Path(td)/id;src.write_text(program);p=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(src),'-o',str(exe)],capture_output=True,text=True,check=True);assert not p.stderr,(id,p.stderr)
  blocks=[b for s in d['sections']for b in s['blocks']];input=next(b['text']for b in blocks if b['type']=='code'and b.get('language')=='Input');expected=next(b['text']for b in blocks if b['type']=='code'and b.get('language')=='Output');run=subprocess.run([str(exe)],input=input,capture_output=True,text=True,check=True,timeout=3);assert run.stdout.split()==expected.split(),id
  return id,exe,{'id':id,'reviewed_blocks':4,'unique_program_sha256':hashlib.sha256(program.encode()).hexdigest(),'helper_sha256':hashlib.sha256(snippet.encode()).hexdigest(),'both_languages_identical':True,'helper_is_exact_program_prefix':True,'compile_warnings':0,'samples':1,'oracle_cases':0}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:built=list(pool.map(build,ids))
 def run(exe,data):return subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=3).stdout.split()
 for id,exe,report in built:
  if id=='graph-basics':
   assert run(exe,'3 0\n')==['0:','1:','2:'];report['boundary_cases']=1;reports.append(report);continue
  for case in range(25):
   n=rng.randint(1,12)
   if id=='dynamic-programming':
    n=rng.choice([0,1,2,40,100]+list(range(3,25)));expected=[str(sum(math.comb(n-t,t)for t in range(n//2+1))%1000000007)];data=str(n)+'\n'
   elif id=='dsu':
    labels=list(range(n));commands=[];expected=[]
    for _ in range(50):
     op=rng.choice(['union','same','size']);u=rng.randrange(n)
     if op=='size':commands.append(f'size {u}');expected.append(str(labels.count(labels[u])))
     else:
      v=rng.randrange(n);commands.append(f'{op} {u} {v}')
      if op=='same':expected.append('YES'if labels[u]==labels[v]else'NO')
      else:
       old,new=labels[v],labels[u];labels=[new if label==old else label for label in labels]
    data=f'{n} {len(commands)}\n'+'\n'.join(commands)+'\n'
   elif id in ['fenwick-tree','segment-tree','lazy-segment-tree']:
    initial=[rng.randint(-10,10)for _ in range(n)];values=initial[:];commands=[];expected=[]
    for _ in range(50):
     left,right=sorted([rng.randrange(n),rng.randrange(n)])
     if rng.randrange(2):commands.append(f'sum {left} {right}');expected.append(str(sum(values[left:right+1])))
     elif id=='lazy-segment-tree':
      delta=rng.randint(-10,10);commands.append(f'add {left} {right} {delta}')
      for index in range(left,right+1):values[index]+=delta
     elif id=='fenwick-tree':
      delta=rng.randint(-10,10);commands.append(f'add {left} {delta}');values[left]+=delta
     else:
      value=rng.randint(-20,20);commands.append(f'set {left} {value}');values[left]=value
    data=f'{n} {len(commands)}\n'+' '.join(map(str,initial))+'\n'+'\n'.join(commands)+'\n'
   elif id=='number-theory':
    value=rng.choice([1,2,97,360,30030,rng.randint(1,100000)]);tokens=run(exe,str(value)+'\n');assert len(tokens)%2==0;product=1;previous=1
    for p,e in zip(map(int,tokens[::2]),map(int,tokens[1::2])):
     assert p>previous and e>0 and all(p%d for d in range(2,math.isqrt(p)+1));previous=p;product*=p**e
    assert product==value;report['oracle_cases']+=1;continue
   else:
    n=rng.randint(0,12);values=[rng.randint(0,8)for _ in range(n)];limit=rng.choice([-1,0,rng.randint(1,20)]);expected=[str(sum(sum(values[left:right])<=limit for left in range(n)for right in range(left+1,n+1)))];data=f'{n}\n'+' '.join(map(str,values))+f'\n{limit}\n'
   assert run(exe,data)==expected,(id,case,data,expected);report['oracle_cases']+=1
  reports.append(report)
report={'status':'passed','local_proposals_only':True,'seed':41027,'reviewed_blocks':32,'unique_programs':8,'samples':8,'oracle_cases':sum(r['oracle_cases']for r in reports),'boundary_cases':1,'programs':reports};(ROOT/'audit/PACKAGE02-TUTORIAL-CPP-TESTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='programs'}))
