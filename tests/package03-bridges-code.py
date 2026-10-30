import itertools,json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(51982)
def components(n,e,edge=-1,vertex=0):
 a=[[]for _ in range(n+1)]
 for i,(u,v)in enumerate(e):
  if i==edge or vertex in(u,v):continue
  a[u].append(v);a[v].append(u)
 seen={vertex};cnt=0
 for r in range(1,n+1):
  if r in seen:continue
  cnt+=1;seen.add(r);q=[r]
  for u in q:
   for v in a[u]:
    if v not in seen:seen.add(v);q.append(v)
 return cnt
with tempfile.TemporaryDirectory()as t:
 t=Path(t);src=R/'audit/package03-work/bridges-articulation.cpp';b=t/'solve';subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wshadow','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(b)],check=True)
 def run(n,e):
  s=f'{n} {len(e)}\n'+''.join(f'{u} {v}\n'for u,v in e);p=subprocess.run([str(b)],input=s,text=True,capture_output=True,check=True,timeout=30);assert not p.stderr;ls=p.stdout.splitlines();assert len(ls)==4;be=list(map(int,ls[1].split()));cu=list(map(int,ls[3].split()));assert int(ls[0])==len(be) and int(ls[2])==len(cu);return be,cu
 cases=[(0,[]),(1,[]),(1,[(1,1)]),(2,[(1,2),(1,2)]),(3,[(1,2),(1,2),(2,3),(2,2)]),(7,[(1,2),(2,3),(3,1),(3,4),(4,5),(5,6),(6,4)])]
 for n in range(1,6):
  edges=list(itertools.combinations(range(1,n+1),2))
  for mask in range(1<<len(edges)):cases.append((n,[x for i,x in enumerate(edges)if mask>>i&1]))
 for _ in range(200):
  n=rng.randrange(1,10);cases.append((n,[(rng.randrange(1,n+1),rng.randrange(1,n+1))for _ in range(rng.randrange(0,20))]))
 for n,e in cases:
  base=components(n,e);wantb=[i+1 for i in range(len(e))if components(n,e,edge=i)>base];wantc=[v for v in range(1,n+1)if components(n,e,vertex=v)>base];got=run(n,e);assert got==(wantb,wantc),(n,e,got,wantb,wantc)
 n=200000
 for kind in ['path','star','parallel']:
  e=[(i,i+1)for i in range(1,n)]if kind=='path'else[(1,i)for i in range(2,n+1)]if kind=='star'else[(1,2)]*200000
  be,cu=run(n,e)
  if kind=='path':assert be==list(range(1,n))and cu==list(range(2,n))
  elif kind=='star':assert be==list(range(1,n))and cu==[1]
  else:assert be==[]and cu==[]
 # Repeated runs must reset working arrays and edge labels remain stable.
 s=src.read_text().split('int main() {')[0]+'''int main(){Lowlink g(3);g.add(1,2);g.add(1,2);g.add(2,3);for(int i=0;i<2;i++){g.run();for(int x:g.bridge)cout<<x;cout<<' ';for(int v=1;v<=3;v++)cout<<g.cut[v];cout<<'\\n';}}''';(t/'h.cpp').write_text(s);subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined',str(t/'h.cpp'),'-o',str(t/'h')],check=True);p=subprocess.run([str(t/'h')],text=True,capture_output=True,check=True);assert p.stdout=='001 010\n001 010\n'and not p.stderr
 data={'status':'passed','CXX17_UBSan':True,'independent_vertex_and_edge_removal_component_oracle':True,'small_graph_cases':len(cases),'exhaustive_simple_graphs_through_n':5,'random_multigraphs':200,'parallel_selfloops_disconnected_and_empty':True,'max_vertices':200000,'path_star_parallel_stress':True,'repeated_run_reset':True};(R/'audit/PACKAGE03-BRIDGES-CODE.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
