"""Independent parent/path oracle for the original weighted LCA lesson."""
import collections,hashlib,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];d=json.loads((ROOT/'audit/package03-lessons/lca.json').read_text());blocks=d['body']['sections'][7]['blocks'];code=(ROOT/'audit/package03-work/lca-path.cpp').read_text();rng=random.Random(20261028);cases=queries=0
with tempfile.TemporaryDirectory()as tmp:
 src=Path(tmp)/'lca.cpp';exe=Path(tmp)/'lca';src.write_text(code)
 def compile(path,extra=[]):
  p=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',*extra,str(src),'-o',str(path)],capture_output=True,text=True);assert p.returncode==0 and not p.stderr,p.stderr
 compile(exe)
 def run(inp,path=exe):return subprocess.run([str(path)],input=inp,capture_output=True,text=True,timeout=15,check=True).stdout.split()
 sample=next(b['text']for b in blocks if b.get('language')=='Input');expected=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample)==expected.split()
 def check(n,edges,pairs):
  global cases,queries
  adj=[[]for _ in range(n)];par=[-1]*n;depth=[0]*n;weight=[0]*n
  for u,v,w in edges:adj[u].append((v,w));adj[v].append((u,w))
  par[0]=0;queue=collections.deque([0])
  while queue:
   u=queue.popleft()
   for v,w in adj[u]:
    if par[v]!=-1:continue
    par[v]=u;depth[v]=depth[u]+1;weight[v]=w;queue.append(v)
  expected=[]
  for a,b in pairs:
   u,v=a,b;weights=[]
   while depth[u]>depth[v]:weights.append(weight[u]);u=par[u]
   while depth[v]>depth[u]:weights.append(weight[v]);v=par[v]
   while u!=v:weights.extend([weight[u],weight[v]]);u=par[u];v=par[v]
   expected.extend(map(str,[u+1,min(weights)if weights else 0,max(weights)if weights else 0,sum(weights)]))
  inp=f'{n} {len(pairs)}\n'+'\n'.join(f'{u+1} {v+1} {w}'for u,v,w in edges)+'\n'+'\n'.join(f'{a+1} {b+1}'for a,b in pairs)+'\n';assert run(inp)==expected,(n,edges[:10],pairs[:10]);cases+=1;queries+=len(pairs)
 for n in range(1,36):
  # Relabel vertices, keeping root0; parents may have larger labels than children.
  for mode in range(3):
   order=[0]+rng.sample(list(range(1,n)),n-1);edges=[(order[i],order[rng.randrange(i)],rng.choice([-10**9,-7,0,5,10**9])if mode==0 else rng.randrange(-100,101))for i in range(1,n)];rng.shuffle(edges);pairs=[(a,b)for a in range(n)for b in range(n)];check(n,edges,pairs)
 n=200000
 for mode in ['chain','star']:
  edges=[(i-1 if mode=='chain'else 0,i,-10**9 if i%3==0 else 10**9)for i in range(1,n)];check(n,edges,[(0,0),(n-1,n-1),(0,n-1),(n-1,0),(n//2,n-1),(n-2,n-1)])
 check(3,[(0,2,-5),(2,1,-8)],[])  # q=0, parent label larger than child
 ubsan=Path(tmp)/'lca-ubsan';compile(ubsan,['-fsanitize=undefined','-fno-sanitize-recover=all']);assert run(sample,ubsan)==next(b['text']for b in blocks if b.get('language')=='Output').split()
report={'status':'passed','program_sha256':hashlib.sha256(code.encode()).hexdigest(),'compile_warnings':0,'sample_passed':True,'independent_oracle':'Explicit parent-by-parent LCA and collection of each actual path edge; no binary-lifting table in the reference','trees':cases,'queries':queries,'max_n':200000,'coverage':['same vertex','root','ancestor/descendant','both directions','negative/zero/positive extrema','large signed sums','parent labels larger than child','chain','star','q=0'],'sample_UBSan':True,'no_production_writes':True}
(ROOT/'audit/PACKAGE03-LCA-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
