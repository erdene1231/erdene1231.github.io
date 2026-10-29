import itertools,json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(151);cases=0
with tempfile.TemporaryDirectory()as tmp:
 bins={}
 for name in ['dsu','kruskal','prim']:
  out=str(Path(tmp)/name);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/spanning-{name}.cpp'),'-o',out],check=True);bins[name]=out
 def run(name,s):
  global cases
  p=subprocess.run([bins[name]],input=s,text=True,capture_output=True,check=True);assert not p.stderr,p.stderr;cases+=1;return p.stdout.splitlines()
 def oracle(n,es):
  best=None
  for ss in itertools.combinations(es,n-1):
   seen={1}
   while True:
    nxt=seen|{b for a,b,w in ss if a in seen}|{a for a,b,w in ss if b in seen}
    if nxt==seen:break
    seen=nxt
   if len(seen)==n:
    s=sum(w for a,b,w in ss);best=s if best is None else min(best,s)
  return best
 def check(n,es):
  want=oracle(n,es);s=f'{n} {len(es)}\n'+''.join(f'{a} {b} {w}\n'for a,b,w in es)
  for name in ['kruskal','prim']:
   out=run(name,s)
   if want is None:assert out==['IMPOSSIBLE'],(n,es,out)
   else:
    assert int(out[0])==want,(name,es,out,want);chosen=[tuple(map(int,x.split()))for x in out[1:]];assert len(chosen)==n-1 and sum(w for a,b,w in chosen)==want
    pool=list(es)
    for a,b,w in chosen:
     e=next((e for e in pool if e[2]==w and {e[0],e[1]}=={a,b}),None);assert e is not None;pool.remove(e)
    assert oracle(n,chosen)==want
 source=[(5,6,2),(1,2,3),(3,6,3),(1,5,5),(2,3,5),(2,5,6),(4,6,7),(3,4,9)]
 assert oracle(6,source)==20 and -oracle(6,[(a,b,-w)for a,b,w in source])==32;check(6,source)
 for n,es in [(1,[]),(2,[]),(1,[(1,1,-10)]),(3,[(1,2,-4),(2,3,-5),(1,3,0)]),(3,[(1,2,4000000000),(2,3,4000000000)]),(2,[(1,1,-9),(1,2,4),(1,2,-3)])]:check(n,es)
 for _ in range(220):
  n=rng.randint(1,7);es=[(rng.randint(1,n),rng.randint(1,n),rng.randint(-9,9))for _ in range(rng.randint(0,11))];check(n,es)
 for _ in range(30):
  n=30;groups=list(range(n+1));ops=[];want=[]
  for i in range(150):
   a,b=rng.randint(1,n),rng.randint(1,n);t=rng.randint(1,2);ops.append((t,a,b))
   if t==1:
    x,y=groups[a],groups[b];groups=[x if v==y else v for v in groups]
   else:want.append(str(int(groups[a]==groups[b])))
  assert run('dsu',f'{n} {len(ops)}\n'+''.join(f'{t} {a} {b}\n'for t,a,b in ops))==want
 n=200000;s=f'{n} {n-1}\n'+''.join(f'{i} {i+1} 1000000000\n'for i in range(1,n))
 for name in ['kruskal','prim']:assert int(run(name,s)[0])==(n-1)*1000000000
report={'status':'passed','programs':3,'UBSan_oracle_runs':cases,'oracle':'Exhaustive edge-subset spanning-tree enumeration; independent DSU set labels; selected-edge validity','source_minimum':20,'source_maximum':32,'stress':'200000-node chain, 64-bit totals; negative/tied/parallel/self-loop/disconnected/singleton cases'}
(R/'audit/PACKAGE03-SPANNING-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
