import json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];random.seed(120117);cases=0;source_dfs=[(1,2),(1,4),(2,3),(2,5),(3,5)];source_bfs=[(1,2),(1,4),(2,3),(2,5),(3,6),(5,6)];source_connect=[(1,3),(1,4),(3,4),(2,5)];source_cycles=[(1,3),(1,4),(2,3),(2,5),(3,4),(3,5)];source_bip=[(1,2),(1,4),(2,3),(2,5),(3,5),(4,5)]
fixtures={'dfs':{'n':5,'edges':source_dfs,'order':[1,2,3,5,4]},'bfs':{'n':6,'edges':source_bfs,'dist':[0,1,2,1,2,3]},'connectivity':{'n':5,'edges':source_connect,'components':[[1,3,4],[2,5]]},'cycles':{'n':5,'edges':source_cycles,'cycle':[3,2,5,3]},'coloring':{'n':5,'edges':source_bip,'conflict':[2,5]}}
(R/'audit/package03-work/traversal-fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
def adj(n,edges,dr):
 a=[[]for _ in range(n+1)]
 for u,v in edges:
  a[u].append(v)
  if not dr:a[v].append(u)
 return a
with tempfile.TemporaryDirectory()as tmp:
 exes={}
 for name in ['dfs-rec','dfs-iter','bfs','applications']:
  exe=tmp+'/'+name;exes[name]=exe;subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wconversion','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/traversal-{name}.cpp'),'-o',exe],check=True)
 def run(name,inp):
  global cases
  r=subprocess.run([exes[name]],input=inp,text=True,capture_output=True,check=True,timeout=25);assert not r.stderr,r.stderr;cases+=1;return r.stdout.splitlines()
 sample=[(5,source_dfs),(6,source_bfs),(5,source_connect),(5,source_cycles),(5,source_bip),(1,[]),(2,[(1,2),(1,2)]),(1,[(1,1)])]
 for n,edges in sample+[(random.randint(1,8),None)for _ in range(130)]:
  if edges is None:edges=[(random.randint(1,n),random.randint(1,n))for _ in range(random.randrange(20))]
  for dr in [0,1]:
   a=adj(n,edges,dr);s=random.randint(1,n);t=random.randint(1,n);vis=set();order=[]
   def dfs(u):
    if u in vis:return
    vis.add(u);order.append(u)
    for v in a[u]:dfs(v)
   dfs(s);inp=f'{n} {len(edges)} {dr} {s}\n'+'\n'.join(f'{u} {v}'for u,v in edges)+'\n'
   for name in ['dfs-rec','dfs-iter']:assert list(map(int,run(name,inp)[0].split()))==order
   dist=[[0 if u==v else 10**9 for v in range(n+1)]for u in range(n+1)]
   for u in range(1,n+1):
    for v in a[u]:dist[u][v]=min(dist[u][v],1)
   for k in range(1,n+1):
    for u in range(1,n+1):
     for v in range(1,n+1):dist[u][v]=min(dist[u][v],dist[u][k]+dist[k][v])
   inp=f'{n} {len(edges)} {dr} {s} {t}\n'+'\n'.join(f'{u} {v}'for u,v in edges)+'\n';out=run('bfs',inp);got=list(map(int,out[1].split()));expect=[d if d<10**9 else -1 for d in dist[s][1:]];assert got==expect
   visit=list(map(int,out[0].split()));assert set(visit)==vis and len(visit)==len(vis);assert [got[u-1]for u in visit]==sorted(got[u-1]for u in visit)
   if got[t-1]==-1:assert out[2]=='IMPOSSIBLE'
   else:
    path=list(map(int,out[2].split()));assert path[0]==s and path[-1]==t and len(path)==got[t-1]+1;assert all(v in a[u]for u,v in zip(path,path[1:]))
  # Undirected applications: DSU and exhaustive color assignments are independent of traversal.
  par=list(range(n+1));cycle=False
  def find(u):
   while par[u]!=u:u=par[u]
   return u
  for u,v in edges:
   x,y=find(u),find(v)
   if x==y:cycle=True
   else:par[y]=x
  groups=[]
  for u in range(1,n+1):
   if not any(u in g for g in groups):groups.append([v for v in range(1,n+1)if find(v)==find(u)])
  labels=[next(i+1 for i,g in enumerate(groups)if u in g)for u in range(1,n+1)]
  possible=any(all(((mask>>(u-1))&1)!=((mask>>(v-1))&1)for u,v in edges)for mask in range(1<<n));out=run('applications',f'{n} {len(edges)}\n'+'\n'.join(f'{u} {v}'for u,v in edges)+'\n');assert int(out[0])==len(groups);assert list(map(int,out[1].split()))==labels;assert list(map(int,out[2].split()))==[int(cycle)]*2;assert (out[3]=='BIPARTITE')==possible
  if possible:
   colors=list(map(int,out[4].split()));assert len(colors)==n and all(colors[u-1]!=colors[v-1]for u,v in edges)
 # Exact pedagogical traces.
 out=run('dfs-rec','5 5 0 1\n'+'\n'.join(f'{u} {v}'for u,v in source_dfs)+'\n');assert out[0]=='1 2 3 5 4'
 out=run('bfs','6 6 0 1 6\n'+'\n'.join(f'{u} {v}'for u,v in source_bfs)+'\n');assert out[0]=='1 2 4 3 5 6'and out[1]=='0 1 2 1 2 3'and out[2]=='1 2 3 6'
 # Deep inputs: explicit storage rather than call-stack dependence.
 n=200000;edge_text='\n'.join(f'{i} {i+1}'for i in range(1,n));out=run('dfs-iter',f'{n} {n-1} 0 1\n'+edge_text+'\n');assert list(map(int,out[0].split()))==list(range(1,n+1));out=run('bfs',f'{n} {n-1} 0 1 {n}\n'+edge_text+'\n');assert list(map(int,out[1].split()))==list(range(n));out=run('applications',f'{n} {n-1}\n'+edge_text+'\n');assert out[0]=='1'and out[2]=='0 0'and out[3]=='BIPARTITE'
 # A modest recursion example, not a platform-independent recursion-depth promise.
 n=1000;out=run('dfs-rec',f'{n} {n-1} 0 1\n'+'\n'.join(f'{i} {i+1}'for i in range(1,n))+'\n');assert len(out[0].split())==n
report={'status':'passed','programs':4,'ubsan_oracle_runs':cases,'independent_oracles':['recursive traversal order','Floyd-Warshall distances/path edge checks','DSU cycle/components','exhaustive2color masks'],'stress':'200000-node chain for iterative DFS/BFS/applications;1000-node recursive fixture without universal stack-depth claim','source_traces':'DFS1,2,3,5,4; BFS1,2,4,3,5,6; distances0,1,2,1,2,3'};(R/'audit/PACKAGE03-TRAVERSAL-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
