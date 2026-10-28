"""Exact lesson C++17 programs against independent list/scan specifications."""
from pathlib import Path
import json,subprocess,tempfile,random,hashlib
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['stack-queue','set-map']:
  body=json.loads((ROOT/f'audit/package02-lessons/{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];source=(ROOT/f'audit/package02-work/{id}.cpp').read_text();pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]==source;assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
  exe=Path(tmp)/id;build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(ROOT/f'audit/package02-work/{id}.cpp'),'-o',str(exe)],capture_output=True,text=True,check=True);assert not build.stderr,build.stderr
  def run(text):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=12,check=True).stdout.split()
  count=0;operations=0
  if id=='stack-queue':
   cases=[[],['S-','Q-'],['S+ 5','S+ 5','S-','S-','S-'],['Q+ -1','Q+ 0','Q-','Q-','Q-'],[f'{t}+ {v}'for t in ['S','Q']for v in [10,20,30]]+['S-','Q-']*4]
   for _ in range(180):cases.append([rng.choice(['S-','Q-',f'S+ {rng.randint(-3,3)}',f'Q+ {rng.randint(-3,3)}'])for _ in range(rng.randint(0,500))])
   cases.append([f'S+ {i}'for i in range(50000)]+[f'Q+ {i}'for i in range(50000)]+['S-','Q-']*50000)
   for commands in cases:
    # List slicing gives a direct order specification, independent of std adaptors.
    stack=[];queue=[];expected=[];head=0
    for c in commands:
     if c.startswith('S+'):stack.append(int(c.split()[1]))
     elif c.startswith('Q+'):queue.append(int(c.split()[1]))
     elif c=='S-':
      expected.append(str(stack[-1])if stack else'EMPTY');stack=stack[:-1]
     else:
      expected.append(str(queue[head])if head<len(queue)else'EMPTY');head+=head<len(queue)
    assert run(str(len(commands))+'\n'+'\n'.join(commands)+'\n')==expected;count+=1;operations+=len(commands)
   # Independently check the stated monotonic-stack exercise's equality rule/dominance.
   arrays=[[],[5,5,5],[1,2,3],[3,2,1]]+[[rng.randrange(10)for _ in range(rng.randrange(40))]for _ in range(200)]
   for a in arrays:
    tops=[];actual=[]
    for i,x in enumerate(a):
     while tops and a[tops[-1]]>=x:tops.pop()
     actual.append(tops[-1]+1 if tops else 0);tops.append(i)
    expected=[next((j+1 for j in range(i-1,-1,-1)if a[j]<a[i]),0)for i in range(len(a))];assert actual==expected
   extra={'monotonic_stack_proof_examples':len(arrays)};oracle='Independent arrival-order lists for both structures, empty/drain/refill/duplicates/interleaving and200000commands; nearest-smaller extension checked against backward scans'
  else:
   cases=[([],[]),([],[0,-1,1]),([7,2,7,5,2,7],[7,9,2]),([5]*30,[5,6,6]),([-10**9,0,10**9],[-10**9,0,10**9,1])]
   cases +=[([rng.randrange(-12,13)for _ in range(rng.randrange(150))],[rng.randrange(-20,21)for _ in range(rng.randrange(100))])for _ in range(180)]
   for values,queries in cases:
    expected=[str(sum(x==q for x in values))for q in queries];distinct=sorted(set(values));expected+=[str(len(distinct))]
    for x in distinct:expected +=[str(x),str(sum(v==x for v in values))]
    text=f'{len(values)} {len(queries)}\n'+' '.join(map(str,values))+'\n'+' '.join(map(str,queries))+'\n';assert run(text)==expected;count+=1;operations+=len(values)+len(queries)
   for values,queries in [([10**9]*200000,[-10**9]*200000),(list(range(200000)),list(range(200000)))]:
    text=f'{len(values)} {len(queries)}\n'+' '.join(map(str,values))+'\n'+' '.join(map(str,queries))+'\n';got=run(text)
    if len(set(values))==1:expected=['0']*200000+['1',str(10**9),'200000']
    else:expected=['1']*200000+['200000']+[token for x in range(200000)for token in(str(x),'1')]
    assert got==expected;count+=1;operations+=len(values)+len(queries)
   extra={};oracle='Direct full-log scan for query counts and independently sorted unique report; repeated missingqueries verify no insertions;200000arrivals/queries all-equal andall-distinct boundaries'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split();reports.append({'lesson':id,'cases':count,'operations':operations,**extra,'sample_passed':True,'compile_warnings':0,'program_sha256':hashlib.sha256(source.encode()).hexdigest(),'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Local complete programs, exact MN/EN fragments and explicit monotonic-stack extension; editor/semantic/publication gates separate'};(ROOT/'audit/PACKAGE02-CONTAINERS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
