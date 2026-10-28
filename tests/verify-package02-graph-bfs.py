"""Exact tutorial graph programs; independent DSU and all-pairs distance oracles."""
from pathlib import Path
import json,subprocess,tempfile,random,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
def components(n,edges):
 parent=list(range(n+1));size=[1]*(n+1)
 def root(x):
  while parent[x]!=x:
   parent[x]=parent[parent[x]];x=parent[x]
  return x
 for a,b in edges:
  a,b=root(a),root(b)
  if a==b:continue
  if size[a]<size[b]:a,b=b,a
  parent[b]=a;size[a]+=size[b]
 return len({root(x)for x in range(1,n+1)})
def shortest(n,edges,s,t):
 dist=[[n+1]*n for _ in range(n)]
 for i in range(n):dist[i][i]=0
 for a,b in edges:
  if a!=b:dist[a-1][b-1]=dist[b-1][a-1]=1
 for k in range(n):
  for i in range(n):
   for j in range(n):dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
 return dist[s-1][t-1]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['graph-basics','bfs']:
  body=json.loads((ROOT/f'audit/package02-lessons/{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];source=(ROOT/f'audit/package02-work/{id}.cpp').read_text();pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]==source;assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
  exe=Path(tmp)/id;build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(ROOT/f'audit/package02-work/{id}.cpp'),'-o',str(exe)],capture_output=True,text=True,check=True);assert not build.stderr,build.stderr
  def run(text):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=15,check=True).stdout.split()
  count=0
  if id=='graph-basics':
   def check(n,edges):
    out=list(map(int,run(f'{n} {len(edges)}\n'+''.join(f'{a} {b}\n'for a,b in edges))));c=components(n,edges);assert out[0]==c-1 and len(out)==1+2*out[0];new=list(zip(out[1::2],out[2::2]));assert all(1<=a<=n and 1<=b<=n and a!=b for a,b in new);old={tuple(sorted(e))for e in edges};assert all(tuple(sorted(e))not in old for e in new);assert len({tuple(sorted(e))for e in new})==len(new);assert components(n,edges+new)==1
   for n in range(1,6):
    possible=list(itertools.combinations(range(1,n+1),2))
    for bits in itertools.product([False,True],repeat=len(possible)):check(n,[e for e,yes in zip(possible,bits)if yes]);count+=1
   for _ in range(160):
    n=rng.randint(1,60);edges=[(a,b)for a,b in itertools.combinations(range(1,n+1),2)if rng.random()<0.08];check(n,edges);count+=1
   check(4,[(1,1),(1,2),(1,2),(3,4)]);count+=1
   n=200000
   for edges in [[],[(i,i+1)for i in range(1,n)],[(1,i)for i in range(2,n+1)],[(i,i+1)for i in range(1,n)if i!=n//2]]:check(n,edges);count+=1
   extra={'program_graphs':count,'exhaustive_simple_graph_max_vertices':5,'maximum_vertices':n};oracle='Independent disjoint-set oracle for component lower bound; verify new edges, exact minimum count and resulting global connectivity. Every simple graph through5vertices; random, loop/parallel and200000vertex chain/star/edgeless/disconnected cases'
  else:
   def check(n,edges,s,t,expected=None):
    out=run(f'{n} {len(edges)} {s} {t}\n'+''.join(f'{a} {b}\n'for a,b in edges));length=shortest(n,edges,s,t)if expected is None else expected
    if length>n:assert out==['IMPOSSIBLE'];return
    out=list(map(int,out));path=out[1:];assert out[0]==len(path)==length+1 and path[0]==s and path[-1]==t;assert len(set(path))==len(path);links={tuple(sorted(e))for e in edges};assert all(tuple(sorted(e))in links for e in zip(path,path[1:]));assert all(1<=v<=n for v in path)
   for n in range(1,5):
    possible=list(itertools.combinations(range(1,n+1),2))
    for bits in itertools.product([False,True],repeat=len(possible)):
     edges=[e for e,yes in zip(possible,bits)if yes]
     for s in range(1,n+1):
      for t in range(1,n+1):check(n,edges,s,t);count+=1
   for _ in range(200):
    n=rng.randint(1,14);edges=[(a,b)for a,b in itertools.combinations(range(1,n+1),2)if rng.random()<0.2];check(n,edges,rng.randint(1,n),rng.randint(1,n));count+=1
   check(4,[(1,1),(1,2),(1,2),(2,3),(3,4)],1,4);count+=1
   n=200000;chain=[(i,i+1)for i in range(1,n)]
   for edges,s,t,d in[(chain,1,n,n-1),(chain,n,1,n-1),([],1,n,n+1),([],n,n,0),([(1,i)for i in range(2,n+1)],2,n,2),([(i,i+1)for i in range(1,n)if i!=n//2],1,n,n+1)]:check(n,edges,s,t,d);count+=1
   # Explicit conceptual witness: an unweighted one-edge route need not minimize weights.
   assert shortest(3,[(1,2),(1,3),(3,2)],1,2)==1 and 10>1+1
   extra={'program_routes':count,'exhaustive_all_pairs_max_vertices':4,'maximum_vertices':n,'weighted_limitation_witness':True};oracle='Independent Floyd-Warshall distances; validate endpoints, every route edge and minimum length without demanding a particular tie choice. All pairs of every simple graph through4vertices, random/multiedge and200000vertex extremes'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split();reports.append({'lesson':id,**extra,'sample_passed':True,'compile_warnings':0,'undefined_behavior_sanitizer':'passed for all executions','program_sha256':hashlib.sha256(source.encode()).hexdigest(),'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Local complete C++17 programs and exact MN/EN fragments; semantics/native editor/publication gates separate'};(ROOT/'audit/PACKAGE02-GRAPH-BFS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
