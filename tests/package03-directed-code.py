import json,random,subprocess,tempfile,itertools,collections,heapq
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(160);runs=0
with tempfile.TemporaryDirectory()as tmp:
 bins={}
 for name in ['topo','dag','shortest','coins','jump','floyd']:
  out=str(Path(tmp)/name);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/directed-{name}.cpp'),'-o',out],check=True);bins[name]=out
 def run(name,s):
  global runs
  p=subprocess.run([bins[name]],input=s,text=True,capture_output=True,check=True);assert not p.stderr,p.stderr;runs+=1;return p.stdout.splitlines()
 def kahn(n,es):
  indeg=[0]*(n+1);adj=[[]for _ in range(n+1)]
  for a,b in es:indeg[b]+=1;adj[a].append(b)
  q=collections.deque(u for u in range(1,n+1)if indeg[u]==0);ord=[]
  while q:
   u=q.popleft();ord.append(u)
   for v in adj[u]:
    indeg[v]-=1
    if indeg[v]==0:q.append(v)
  return ord
 for _ in range(110):
  n=rng.randint(1,12);es=[(rng.randint(1,n),rng.randint(1,n))for _ in range(rng.randrange(25))];out=run('topo',f'{n} {len(es)}\n'+''.join(f'{a} {b}\n'for a,b in es))
  if len(kahn(n,es))<n:assert out==['IMPOSSIBLE']
  else:
   seq=list(map(int,out[0].split()));assert sorted(seq)==list(range(1,n+1));pos={u:i for i,u in enumerate(seq)};assert all(pos[a]<pos[b]for a,b in es)
 for _ in range(100):
  n=rng.randint(1,8);es=[(a,b,rng.randint(-10,10))for a in range(1,n+1)for b in range(a+1,n+1)if rng.random()<.3];s,t=rng.randint(1,n),rng.randint(1,n);adj=[[]for _ in range(n+1)]
  for a,b,w in es:adj[a].append((b,w))
  paths=[]
  def walk(u,seq,w):
   if u==t:paths.append((seq,w));return
   for v,c in adj[u]:walk(v,seq+[v],w+c)
  walk(s,[s],0);out=run('dag',f'{n} {len(es)} {s} {t}\n'+''.join(f'{a} {b} {w}\n'for a,b,w in es));assert int(out[0])==len(paths)
  if not paths:assert out[1:3]==['UNREACHABLE','UNREACHABLE']
  else:
   assert list(map(int,out[1].split()))==[min(w for p,w in paths),max(w for p,w in paths)];assert list(map(int,out[2].split()))==[min(len(p)-1 for p,w in paths),max(len(p)-1 for p,w in paths)];assert set(map(int,out[3].split()))==set.intersection(*(set(p)for p,w in paths))
 assert run('dag','3 2 1 2\n2 3 1\n3 2 1\n')==['CYCLIC']
 for _ in range(70):
  n=rng.randint(1,7);s=rng.randint(1,n);es=[(a,b,rng.randint(1,9))for a in range(1,n+1)for b in range(a+1,n+1)if rng.random()<.4];adj=[[]for _ in range(n+1)]
  for a,b,w in es:adj[a].append((b,w));adj[b].append((a,w))
  ds=[None]*(n+1);ways=[0]*(n+1)
  def walks(u,seen,w):
   if ds[u]is None or w<ds[u]:ds[u]=w;ways[u]=1
   elif w==ds[u]:ways[u]+=1
   for v,c in adj[u]:
    if v not in seen:walks(v,seen|{v},w+c)
  walks(s,{s},0);out=run('shortest',f'{n} {len(es)} {s}\n'+''.join(f'{a} {b} {w}\n'for a,b,w in es));assert out==['INF 0'if ds[u]is None else f'{ds[u]} {ways[u]}'for u in range(1,n+1)]
 for _ in range(55):
  n=rng.randrange(13);cs=rng.sample(range(1,7),rng.randint(1,5));values=[]
  def rec(s,k):
   if s==n:values.append(k);return
   for c in cs:
    if s+c<=n:rec(s+c,k+1)
  rec(0,0);assert run('coins',f'{n} {len(cs)}\n'+ ' '.join(map(str,cs))+'\n')==[f'{min(values)if values else -1} {len(values)}']
 succ=[0,3,5,7,6,2,2,1,6,3];assert run('jump','9 3\n'+' '.join(map(str,succ[1:]))+'\n4 6\n4 11\n4 0\n')==['2','5','4']
 for _ in range(90):
  n=rng.randint(1,40);succ=[0]+[rng.randint(1,n)for _ in range(n)];qs=[(rng.randint(1,n),rng.choice([0,1,2,100,10**18,rng.randrange(1000)]))for _ in range(20)];want=[]
  for x,k in qs:
   seen={};seq=[];u=x
   while u not in seen:seen[u]=len(seq);seq.append(u);u=succ[u]
   mu=seen[u];ix=k if k<len(seq)else mu+(k-mu)%(len(seq)-mu);want.append(str(seq[ix]))
  assert run('jump',f'{n} {len(qs)}\n'+' '.join(map(str,succ[1:]))+'\n'+''.join(f'{x} {k}\n'for x,k in qs))==want
  x=qs[0][0];seen={};u=x;t=0
  while u not in seen:seen[u]=t;t+=1;u=succ[u]
  expected=f'{u} {seen[u]} {t-seen[u]}';assert run('floyd',f'{n} {x}\n'+' '.join(map(str,succ[1:]))+'\n')==[expected,expected]
 # Exact counts must reach2^58 without32bit overflow.
 n=60;es=[(a,b,1)for a in range(1,n+1)for b in range(a+1,n+1)];out=run('dag',f'{n} {len(es)} 1 {n}\n'+''.join(f'{a} {b} {w}\n'for a,b,w in es));assert int(out[0])==2**58
 n=200000;out=run('topo',f'{n} {n-1}\n'+''.join(f'{i} {i+1}\n'for i in range(1,n)));assert len(out[0].split())==n
 assert run('floyd','6 1\n2 3 4 5 6 4\n')==['4 3 3','4 3 3']
report={'status':'passed','programs':6,'UBSan_oracle_runs':runs,'oracles':'Kahn cycle/order; exhaustive DAG path enumeration and vertex intersections; all simple positive paths; coin sequence enumeration; visited functional walks with cycle arithmetic','stress':'200000-node iterative topo; exact2^58path count;1e18successor queries;cycles/disconnected/negative DAG weights/singletons/zero steps'}
(R/'audit/PACKAGE03-DIRECTED-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
