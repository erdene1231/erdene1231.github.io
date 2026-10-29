import json,random,subprocess,tempfile,itertools,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(170);runs=0
with tempfile.TemporaryDirectory()as tmp:
 bins={}
 for name in ['scc','2sat','coins']:
  out=str(Path(tmp)/name);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/scc-{name}.cpp'),'-o',out],check=True);bins[name]=out
 def run(name,s):
  global runs
  p=subprocess.run([bins[name]],input=s,text=True,capture_output=True,check=True);assert not p.stderr,p.stderr;runs+=1;return p.stdout.splitlines()
 def reach(n,es):
  a=[[False]*n for _ in range(n)]
  for u in range(n):a[u][u]=True
  for u,v in es:a[u][v]=True
  for k in range(n):
   for i in range(n):
    for j in range(n):a[i][j]|=a[i][k]and a[k][j]
  return a
 source=[(0,1),(0,3),(1,0),(1,4),(2,1),(2,6),(4,3),(5,4),(5,2),(6,5)]
 for n,es in [(7,source),(1,[]),(1,[(0,0),(0,0)]),(4,[]),(3,[(0,1),(0,1),(1,0),(1,2)])]+[(rng.randint(1,11),None)for _ in range(160)]:
  if es is None:es=[(rng.randrange(n),rng.randrange(n))for _ in range(rng.randrange(35))]
  out=run('scc',f'{n} {len(es)}\n'+''.join(f'{a+1} {b+1}\n'for a,b in es));k=int(out[0]);comp=list(map(int,out[1].split()));rel=reach(n,es);assert len(comp)==n and len(set(comp))==k and set(comp)==set(range(1,k+1))
  for a in range(n):
   for b in range(n):assert (comp[a]==comp[b])==(rel[a][b]and rel[b][a])
  want={(comp[a],comp[b])for a,b in es if comp[a]!=comp[b]};got=[tuple(map(int,s.split()))for s in out[6:]];assert int(out[5])==len(got)==len(set(got))and set(got)==want;assert all(a<b for a,b in got)
  if n==7 and es==source:
   assert list(map(int,out[2].split()))==[4,5,2,1,6,7,3];assert list(map(int,out[3].split()))==[1,2,9,4,3,11,10];assert list(map(int,out[4].split()))==[8,7,14,5,6,12,13]
 def holds(values,clauses):return all((values[abs(a)-1]if a>0 else not values[-a-1])or(values[abs(b)-1]if b>0 else not values[-b-1])for a,b in clauses)
 L1=[(2,-1),(-1,-2),(1,3),(-2,-3),(1,4)];L2=[(1,2),(1,-2),(-1,3),(-1,-3)]
 for n,cs in [(4,L1),(3,L2),(1,[]),(1,[(1,1),(-1,-1)]),(1,[(1,-1)]),(2,[(1,2),(1,2)])]+[(rng.randint(1,7),None)for _ in range(230)]:
  if cs is None:cs=[(rng.choice([-1,1])*rng.randint(1,n),rng.choice([-1,1])*rng.randint(1,n))for _ in range(rng.randrange(22))]
  valid=[v for v in itertools.product([0,1],repeat=n)if holds(v,cs)];out=run('2sat',f'{n} {len(cs)}\n'+''.join(f'{a} {b}\n'for a,b in cs))
  if not valid:assert out==['IMPOSSIBLE']
  else:
   val=list(map(int,out[0].split()));assert len(val)==n and set(val)<={0,1}and holds(val,cs)
   if cs==L1:assert val==[0,0,1,1]
 for _ in range(100):
  n=rng.randint(1,7);es=[(rng.randrange(n),rng.randrange(n))for _ in range(rng.randrange(19))];coins=[rng.randrange(10)for _ in range(n)];adj=[[]for _ in range(n)]
  for a,b in es:adj[a].append(b)
  seen={(u,1<<u)for u in range(n)};q=collections.deque(seen)
  while q:
   u,mask=q.popleft()
   for v in adj[u]:
    x=(v,mask|1<<v)
    if x not in seen:seen.add(x);q.append(x)
  want=max(sum(coins[i]for i in range(n)if mask>>i&1)for u,mask in seen);assert run('coins',f'{n} {len(es)}\n'+' '.join(map(str,coins))+'\n'+''.join(f'{a+1} {b+1}\n'for a,b in es))==[str(want)]
 n=200000;edges=''.join(f'{i} {i+1}\n'for i in range(1,n));out=run('scc',f'{n} {n-1}\n'+edges);assert int(out[0])==n and int(out[5])==n-1
 assert run('coins',f'{n} {n-1}\n'+('1000000000 '*n)+'\n'+edges)==[str(n*1000000000)]
 n=100000;cs='1 1\n'+''.join(f'{-i} {i+1}\n'for i in range(1,n));assert set(run('2sat',f'{n} {n}\n'+cs)[0].split())=={'1'}
report={'status':'passed','programs':3,'UBSan_oracle_runs':runs,'oracles':'Independent transitive closure SCC equivalence and quotient edges; exhaustive2^nSAT assignments; exhaustive(node,visited-mask)coin walks','source':'exact DFS entry/exit/finishing order; L1assignment0,0,1,1; L2unsatisfiable','stress':'200000-node iterative chain/coin total2e14;100000-variable forced implication chain; isolated/selfloop/multiedge/tautology/unit contradiction cases'}
(R/'audit/PACKAGE03-SCC-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
